"""TestSpec testing framework - helper functions."""
from enum import Enum
import traceback
from typing import Any


def no_assigned_action(*args: Any, **kwargs: Any) -> Any:
    """A placeholder function that raises a NotImplementedError when called.

    This function serves as a sentinel value to indicate that no action has been assigned.
    It can be used in scenarios where a callable is expected, but no specific implementation
    is provided during initialization. It raises a NotImplementedError to signal that the
    function is not intended to be called in its current state.

    This function can be used as a placeholder for the `action` attribute in the TestAction class
    that is replaced by a real function or method before the test is run.

    Args:
        *args: Positional arguments (not used).
        **kwargs: Keyword arguments (not used).

    Raises:
        NotImplementedError: Always raised to indicate that no action is assigned.
    """
    raise NotImplementedError("No action assigned for this test.")


def _process_exception(
        err: BaseException,
        exception: type[BaseException] | None,
        exception_tag: str | Enum | None,
        label: str) -> list[str]:
    """Process exception tag validation.

    This method checks if the provided exception matches the expected type
    and tag.

    Args:
        err (BaseException):
            The exception to check.
        exception (type[BaseException]):
            The expected exception type.
        exception_tag (str | Enum):
            The expected tag to look for in the exception.
        label (str):
            A title or context for the exception being processed.

    Returns:
        list[str]: A list of error messages if the expected exception and exception_tag
            is not found, empty otherwise.
    """
    errors: list[str] = []
    if exception is None:
        errors.append(f'Unexpected Exception raised while {label}: {repr(err)}')
        errors.append("stacktrace = ")
        errors.append("\n".join(traceback.format_tb(tb=err.__traceback__)))
    elif not isinstance(err, exception):
        errors.append(
            f'Unexpected exception type while {label}: '
            f'expected={exception}, found = {type(err)}: {repr(err)}')
    elif exception_tag:
        # Case 1: The expected tag is an Enum member.
        # This requires the exception object to have a 'tag_code' attribute.
        if isinstance(exception_tag, Enum):
            if not hasattr(err, 'tag_code'):
                errors.append(
                    f"Exception {type(err)} is missing the 'tag_code' attribute "
                    "required for Enum tag validation.")
            else:
                actual_tag = getattr(err, 'tag_code')
                if actual_tag != exception_tag:
                    errors.append(f"Unexpected exception tag: expected={exception_tag}, "
                                  f"found={actual_tag}")
        # Case 2: The expected tag is a string.
        # This performs a substring search in the exception's string representation.
        else:
            if str(exception_tag) not in str(err):
                errors.append(
                    f"Correct exception type, but tag '{exception_tag}' "
                    f"not found in exception message: {repr(err)}"
                )

    return errors
