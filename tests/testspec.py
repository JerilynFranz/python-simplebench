"""TestSpec testing framework."""

from collections.abc import Callable
from dataclasses import dataclass
from enum import Enum
import traceback
from typing import Any, Optional, Sequence

import pytest

# Sentinel value used to indicate that no expected value is set
NO_EXPECTED_VALUE = object()
"""
A sentinel value used to indicate that no expected value is set.
"""


@dataclass
class TestSpec():
    """A generic unit test specification class.

    It allow tests to be specified declaratively while providing a large amount
    of flexibility.

    Args:
        name (str):
            Identifying name for the test.
        action (Callable[..., Any]):
            A reference to a callable function or method to be invoked for the test.
        args (Sequence[Any], default = []):
            Sequence of positional arguments to be passed to the `action` function or method.
        kwargs (dict[str, Any], default = {}):
            Dictionary containing keyword arguments to be passed to the `action` function or method.
        expected (Any, default=NO_EXPECTED_VALUE ):
            Expected value (if any) that is expected to be returned by the `action` function or method.
            If there is no expected value, the special class NoExpectedValue is used to flag it.
            This is used so that the specific return value of None can be distinguished from no
            particular value or any value at all is expected to be returned from the function or method.
        obj: Optional[Any] = None
        validate_obj: Optional[Callable[[Any], bool]] = None
        validate_result: Optional[Callable[[Any], bool]] = None
        exception: Optional[type[Exception]] = None
        exception_tag: Optional[str] = None
        display_on_fail: Optional[Callable[[], str]] = None
    """
    name: str
    """Identifying name for the test."""
    action: Callable[..., Any]
    """A reference to a callable function or method to be invoked for the test."""
    args: Optional[list[Any]] = None
    """Sequence of positional arguments to be passed to the `action` function or method."""
    kwargs: Optional[dict[str, Any]] = None
    """Dictionary containing keyword arguments to be passed to the `action` function or method."""
    expected: Any = NO_EXPECTED_VALUE
    """Expected value (if any) that is expected to be returned by the `action` function or method."""
    obj: Optional[Any] = None
    """Optional object to be validated."""
    validate_obj: Optional[Callable[[Any], bool]] = None
    """Function to validate the optional object."""
    validate_result: Optional[Callable[[Any], bool]] = None
    """Function to validate the result of the action."""
    exception: Optional[type[Exception]] = None
    """Expected exception type (if any) to be raised by the action."""
    exception_tag: Optional[str | Enum] = None
    """Expected tag (if any) to be found in the exception message."""
    display_on_fail: Optional[Callable[[], str]] = None
    """Function to display additional information on test failure."""

    def run(self) -> None:  # pylint: disable=too-many-branches
        """Run the test based on the provided TestSpec entry.

        This function executes the action specified in the entry, checks the result against
        the expected value, and reports any errors.

        Args:
            self (TestSpec): The test configuration entry containing all necessary information for the test.
        """
        # hide traceback for this function in pytest output
        __tracebackhide__ = True  # pylint: disable=unused-variable
        test_description: str = f"{self.name}"
        errors: list[str] = []
        try:
            # Use empty list/dict if the self field is None
            pos_args = self.args if self.args is not None else []
            kw_args = self.kwargs if self.kwargs is not None else {}
            found: Any = self.action(*pos_args, **kw_args)
            if self.exception:
                errors.append("returned result instead of raising exception")

            else:
                if self.validate_result and not self.validate_result(found):
                    errors.append(f"failed result validation: found={found}")
                if self.validate_obj and not self.validate_obj(self.obj):
                    errors.append(f"failed object validation: obj={self.obj}")
                if self.expected is not NO_EXPECTED_VALUE and self.expected != found:
                    errors.append(f"expected={self.expected}, found={found}")
                    if callable(self.display_on_fail):
                        errors.append(self.display_on_fail())
                    elif isinstance(self.display_on_fail, str):
                        errors.append(self.display_on_fail)
        except Exception as err:  # pylint: disable=broad-exception-caught
            if self.exception is None:
                errors.append(f"Did not expect exception. Caught exception {repr(err)}")
                errors.append("stacktrace = ")
                errors.append("\n".join(traceback.format_tb(tb=err.__traceback__)))

            elif not isinstance(err, self.exception):
                errors.append(
                    f"Unexpected exception type: expected={self.exception}, "
                    f"found = {type(err)}"
                )
            elif self.exception_tag:
                # Case 1: The expected tag is an Enum member.
                # This requires the exception object to have a 'tag_code' attribute.
                if isinstance(self.exception_tag, Enum):
                    if not hasattr(err, 'tag_code'):
                        errors.append(
                            "Exception is missing the 'tag_code' attribute required for Enum tag validation.")
                    else:
                        actual_tag = getattr(err, 'tag_code')
                        if actual_tag != self.exception_tag:
                            errors.append(f"Unexpected exception tag: expected={self.exception_tag}, "
                                          f"found={actual_tag}")
                # Case 2: The expected tag is a string.
                # This performs a substring search in the exception's string representation.
                else:
                    if str(self.exception_tag) not in str(err):
                        errors.append(
                            f"Correct exception type, but tag '{self.exception_tag}' "
                            f"not found in exception message: {repr(err)}"
                        )
        if errors:
            pytest.fail(test_description + ": " + "\n".join(errors))


def run_tests_list(test_specs: Sequence[TestSpec]) -> None:
    """Run a list of tests based on the provided TestSpec entries.

    This function iterates over the list of TestSpec entries and runs each test using
    the `run_test` function. It allows for a clean and organized way to execute multiple tests.

    Args:
        test_specs (list[TestSpec]): A list of TestSpec entries, each representing a test to be run.
    """
    for spec in test_specs:
        spec.run()
