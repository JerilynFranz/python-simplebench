"""TestSpec testing framework - Pytest shim for test actions.

This module provides a PytestAction class that serves as a bridge between
the TestAction class and the pytest testing framework. It allows for the
declarative specification of tests while assigning unique identifiers to
each test case for Pytest.
"""

from collections.abc import Callable
from typing import Any, NoReturn, Optional, Union

from .assertions import Assert
from .base import TestSpec
from .constants import NO_EXPECTED_VALUE
from .helpers import no_assigned_action
from .idspec import idspec
from .test_action import TestAction


class PytestAction(TestSpec):
    """A generic unit test specification class for pytest actions.

    It allows tests to be specified declaratively while providing a large amount
    of flexibility. This is a thin wrapper around :class:`TestAction` that adds pytest-specific
    functionality, such as assigning unique ids to each test case.

    :param str ident: Id for the test.
    :param str name: Identifying name for the test.
    :param Optional[Callable[..., Any]] action: A reference to a callable function or method to be invoked for the test.
                    If no action is assigned, the special function `no_assigned_action` is used which
                    raises NotImplementedError when called.
                    Defaults to no_assigned_action.
    :param Optional[list[Any]] args: Sequence of positional arguments to be passed to the `action` function or method.
                    Defaults to [].
    :param Optional[dict[str, Any]] kwargs: Dictionary containing keyword arguments to be passed to the `action`
                    function or method. Defaults to {}.
    :param Optional[Assert] assertion: The assertion operator to use when comparing the expected and found values.
                        Defaults to Assert.EQUAL.
    :param Any expected: Expected value (if any) for the `action` function or method.
                        This is used with the `assertion` operator to validate the return value of the
                        function or method.
                        If there is no expected value, the special class NoExpectedValue is used to flag it.
                        This is used so that the specific return value of None can be distinguished from no
                        particular value or any value at all is expected to be returned from the function or method.
                        Defaults to NO_EXPECTED_VALUE.
    :param Optional[Any] obj: Optional object to be validated. Defaults to None.
    :param Optional[Callable[[Any], bool]] validate_obj: Function to validate the optional object. Defaults to None.
    :param Optional[Callable[[Any], bool]] validate_result: Function to validate the result of the action.
                        Defaults to None.
    :param Optional[str] validate_attr: Validate a property of the result instead of the result itself.
                        Defaults to None.
    :param Optional[type[BaseException]] exception: Expected exception type (if any) to be raised by the action.
                        Defaults to None.
    :param Optional[str] exception_tag: Expected tag (if any) to be found in the exception message. Defaults to None.
    :param Optional[Callable[[str], NoReturn]] on_fail: Function to call on test failure. Defaults to _fail
                        method which raises AssertionError.
    :param Optional[Any] extra: Extra data for use by test frameworks. It is not used by the TestAction class itself.
                    Defaults to None.
    """

    __test__ = False  # Prevent pytest from collecting this class as a test case

    def __new__(
        cls,
        ident: str,
        *,
        name: str = '',
        action: Callable[..., Any] = no_assigned_action,
        args: Optional[list[Any]] = None,
        kwargs: Optional[dict[str, Any]] = None,
        assertion: Assert = Assert.EQUAL,
        expected: Any = NO_EXPECTED_VALUE,
        obj: Optional[Any] = None,
        validate_obj: Optional[Callable[[Any], bool]] = None,
        validate_result: Optional[Callable[[Any], bool]] = None,
        validate_attr: Optional[str] = None,
        exception: Optional[type[BaseException]] = None,
        exception_tag: Optional[str] = None,
        display_on_fail: Union[str, Callable[[], str]] = '',
        on_fail: Optional[Callable[[str], NoReturn]] = None,
        extra: Any = None,
    ) -> Any:
        """Run the test action using pytest.


        It allow tests to be specified declaratively while providing a large amount
        of flexibility.
        :param str ident: Id for the test.
        :param str name: Identifying name for the test.
        :param Optional[Callable[..., Any]] action: A reference to a callable function or method to be invoked
                        for the test.
                        If no action is assigned, the special function `no_assigned_action` is used which
                        raises NotImplementedError when called.
                        Defaults to no_assigned_action.
        :param Optional[list[Any]] args: Sequence of positional arguments to be passed to the `action` function
                        or method. Defaults to [].
        :param Optional[dict[str, Any]] kwargs: Dictionary containing keyword arguments to be passed to the `action`
                        function or method. Defaults to {}.
        :param Optional[Assert] assertion: The assertion operator to use when comparing the expected and found values.
                          Defaults to Assert.EQUAL.
        :param Any expected: Expected value (if any) for the `action` function or method.
                         This is used with the `assertion` operator to validate the return value of the
                         function or method.
                         If there is no expected value, the special class NoExpectedValue is used to flag it.
                         This is used so that the specific return value of None can be distinguished from no
                         particular value or any value at all is expected to be returned from the function or method.
                         Defaults to NO_EXPECTED_VALUE.
        :param Optional[Any] obj: Optional object to be validated. Defaults to None.
        :param Optional[Callable[[Any], bool]] validate_obj: Function to validate the optional object.
                        Defaults to None.
        :param Optional[Callable[[Any], bool]] validate_result: Function to validate the result of the action.
                        Defaults to None.
        :param Optional[str] validate_attr: Validate a property of the result instead of the result itself.
                        Defaults to None.
        :param Optional[type[BaseException]] exception: Expected exception type (if any) to be raised by the action.
                        Defaults to None.
        :param Optional[str] exception_tag: Expected tag (if any) to be found in the exception message.
                        Defaults to None.
        :param Optional[Callable[[str], NoReturn]] on_fail: Function to call on test failure.
                        Defaults to _fail method which raises AssertionError.
        :param Optional[Any] extra: Extra data for use by test frameworks. It is not used by the TestAction class
                        itself. Defaults to None.
        """
        return idspec(
            ident,
            TestAction(
                name=name,
                action=action,
                args=args,
                kwargs=kwargs,
                assertion=assertion,
                expected=expected,
                obj=obj,
                validate_obj=validate_obj,
                validate_result=validate_result,
                validate_attr=validate_attr,
                exception=exception,
                exception_tag=exception_tag,
                display_on_fail=display_on_fail,
                on_fail=on_fail,
                extra=extra,
            ),
        )

    def run(self) -> Any:
        """Run the test action using pytest.

        :return: The result of the test action.
        :rtype: Any
        """
        raise NotImplementedError(
            'PytestAction instances are not meant to be run directly.')
