"""TestSpec testing framework - test actions."""
import logging
from dataclasses import dataclass
from enum import Enum
from types import TracebackType
from typing import Any, Callable, NoReturn, Optional

from .assertions import Assert, expected_argument_required, validate_assertion
from .base import TestSpec
from .constants import NO_EXPECTED_VALUE
from .deferred import Deferred, _resolve_deferred_value
from .helpers import _process_exception, no_assigned_action

log = logging.getLogger(__name__)


@dataclass
class TestAction(TestSpec):
    """A generic unit test specification class.

    It allow tests to be specified declaratively while providing a large amount
    of flexibility.

    :param name: Identifying name for the test.
    :type name: str
    :param action: A reference to a callable function or method to be invoked for the test.
                   If no action is assigned, the special function `no_assigned_action` is used which
                   raises NotImplementedError when called.
                   Defaults to no_assigned_action.
    :type action: Callable[..., Any] | Deferred, optional
    :param args: Sequence of positional arguments to be passed to the `action` function or method.
                 Defaults to [].
    :type args: Sequence[Any] | Deferred, optional
    :param kwargs: Dictionary containing keyword arguments to be passed to the `action` function or method.
                   Defaults to {}.
    :type kwargs: dict[str, Any] | Deferred, optional
    :param assertion: The assertion operator to use when comparing the expected and found values.
                      Defaults to Assert.EQUAL.
    :type assertion: Assert, optional
    :param expected: Expected value (if any) for the `action` function or method.
                     This is used with the `assertion` operator to validate the return value of the function or method.
                     If there is no expected value, the special class NoExpectedValue is used to flag it.
                     This is used so that the specific return value of None can be distinguished from no
                     particular value or any value at all is expected to be returned from the function or method.
                     Defaults to NO_EXPECTED_VALUE.
    :type expected: Any, optional
    :param obj: Optional object to be validated. Defaults to None.
    :type obj: Optional[Any], optional
    :param validate_obj: Function to validate the optional object. Defaults to None.
    :type validate_obj: Optional[Callable[[Any], bool] | Deferred], optional
    :param validate_result: Function to validate the result of the action. Defaults to None.
    :type validate_result: Optional[Callable[[Any], bool] | Deferred], optional
    :param exception: Expected exception type (if any) to be raised by the action. Defaults to None.
    :type exception: Optional[type[BaseException]], optional
    :param exception_tag: Expected tag (if any) to be found in the exception message. Defaults to None.
    :type exception_tag: Optional[str], optional
    :param on_fail: Function to call on test failure. Defaults to _fail method which raises AssertionError.
    :type on_fail: Callable[[str], NoReturn] | None, optional
    :param extra: Extra data for use by test frameworks. It is not used by the TestAction class itself.
                  Defaults to None.
    :type extra: Any, optional
    """
    __test__ = False  # Prevent pytest from trying to collect this class as a test case

    name: str
    """Identifying name for the test."""
    action: Callable[..., Any] | Deferred = no_assigned_action
    """A reference to a callable function or method to be invoked for the test."""
    args: Optional[list[Any]] | Deferred = None
    """Sequence of positional arguments to be passed to the `action` function or method."""
    kwargs: Optional[dict[str, Any]] | Deferred = None
    """Dictionary containing keyword arguments to be passed to the `action` function or method."""
    assertion: Assert = Assert.EQUAL
    """The assertion operator to use when comparing the expected and found values. (default is Assert.EQUAL)"""
    expected: Any = NO_EXPECTED_VALUE
    """Expected value (if any) that is associated with the `action` function or method.

    This is used with the `assertion` operator to validate the return value of the function or method.
    """
    obj: Optional[Any] = None
    """Optional object to be validated."""
    validate_obj: Optional[Callable[[Any], bool] | Deferred] = None
    """Function to validate the optional object."""
    validate_result: Optional[Callable[[Any], bool] | Deferred] = None
    """Function to validate the result of the action."""
    exception: Optional[type[BaseException]] = None
    """Expected exception type (if any) to be raised by the action."""
    exception_tag: Optional[str | Enum] = None
    """Expected tag (if any) to be found in the exception message."""
    display_on_fail: str | Callable[[], str] = ""
    """String or function to display additional information on test failure."""
    on_fail: Callable[[str], NoReturn] | None = None
    """Function to call on test failure. (default is pytest.fail)

    The function must accept a single string argument containing the failure message
    and must not return (i.e., it should raise an exception or terminate the test).
    """
    extra: Any = None
    """Extra data for use by test frameworks. It is not used by the TestAction class itself. Default is None."""

    _creation_traceback: Optional[TracebackType] = None
    """The traceback at the point where the TestAction was created."""

    def run(self) -> None:  # pylint: disable=too-many-branches
        """Run the test based on the provided TestSpec entry.

        This function executes the action specified in the entry, checks the result against
        the expected value, and reports any errors.

        :param self: The test configuration entry containing all necessary information for the test.
        :type self: TestSpec
        """
        # hide traceback for this function in pytest output
        __tracebackhide__ = True  # pylint: disable=unused-variable
        test_description: str = f"{self.name}"
        errors: list[str] = []
        try:
            # Use empty list/dict if the self field is None
            action = _resolve_deferred_value(self.action)
            pos_args = _resolve_deferred_value(self.args, [])
            kw_args = _resolve_deferred_value(self.kwargs, {})
            obj = _resolve_deferred_value(self.obj)
            expected = _resolve_deferred_value(self.expected)
            validate_result = _resolve_deferred_value(self.validate_result)
            validate_obj = _resolve_deferred_value(self.validate_obj)
            found: Any = action(*pos_args, **kw_args)
            if self.exception:
                errors.append("returned result instead of raising exception")

            else:
                if validate_result and not validate_result(found):
                    errors.append(f"failed result validation: found={found}")
                if validate_obj and not validate_obj(obj):
                    errors.append(f"failed object validation: obj={obj}")
                if not expected_argument_required(self.assertion) or expected is not NO_EXPECTED_VALUE:
                    assertion_result = validate_assertion(self.assertion, expected, found)
                    if assertion_result:
                        errors.append(assertion_result)
                        if callable(self.display_on_fail):
                            errors.append(self.display_on_fail())
                        elif isinstance(self.display_on_fail, str):
                            errors.append(self.display_on_fail)
        except BaseException as err:  # pylint: disable=broad-exception-caught
            new_errors = _process_exception(
                err=err,
                exception=self.exception,
                exception_tag=self.exception_tag,
                label="running test"
            )
            errors.extend(new_errors)

        if errors:
            if self.on_fail:
                self.on_fail(test_description + ": " + "\n".join(errors))
            else:
                self._fail(test_description + ": " + "\n".join(errors))
