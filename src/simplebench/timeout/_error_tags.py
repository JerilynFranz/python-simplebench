"""timeout exceptions for the simplebench package."""

from enum import auto
from simplebench.doc_utils import enum_docstrings
from simplebench.exceptions import ErrorTag


@enum_docstrings
class _TimeoutErrorTag(ErrorTag):
    """ErrorTags for timeout-related errors."""

    NON_CALLABLE_FUNCTION_ARGUMENT = auto()
    """The provided function argument is not callable."""
    INVALID_EXCEPTION_ARG_TYPE = auto()
    """The provided exception argument is not a valid exception type."""
    INVALID_TIMER_TYPE = auto()
    """The provided timer is not of type `threading.Timer`."""
    INVALID_TIMEOUT_INTERVAL_TYPE = auto()
    """The provided timeout interval is not a float or int."""
    INVALID_TIMEOUT_INTERVAL_VALUE = auto()
    """The provided timeout interval is not greater than zero."""
    INVALID_SWALLOW_EXCEPTION_TYPE = auto()
    """The provided swallow_exception flag is not a boolean."""
    INVALID_STATE_TYPE = auto()
    """The provided timeout state is not of type `TimeoutState`."""
    TIMEOUT_EXCEEDED = auto()
    """The operation exceeded the allowed time limit."""
    TARGET_THREAD_ID_NOT_SET = auto()
    """The target thread ID has not been set."""
    TIMER_NOT_SET = auto()
    """The timeout timer has not been set."""
    TIMEOUT_INTERVAL_NOT_SET = auto()
    """The timeout interval has not been set."""
    SWALLOW_EXCEPTION_NOT_SET = auto()
    """The timeout swallow_exception flag has not been set."""
    STATE_NOT_SET = auto()
    """The timeout state has not been set."""
    TIMED_OUT = auto()
    """The operation has timed out."""
