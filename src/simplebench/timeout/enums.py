"""Enums for the simplebench.timeout module."""
from enum import Enum

from ..enums import enum_docstrings


@enum_docstrings
class TimeoutState(str, Enum):
    """Enums for the simplebench.timeout module."""
    EXECUTED = "EXECUTED"
    """The operation completed successfully within the time limit."""
    EXECUTING = "EXECUTING"
    """The operation is currently in progress."""
    TIMED_OUT = "TIMED_OUT"
    """The operation exceeded the allowed time limit."""
    INTERRUPTED = "INTERRUPTED"
    """The operation was interrupted before completion."""
    CANCELED = "CANCELED"
    """The operation was canceled before completion."""
    FAILED = "FAILED"
    """The operation failed due to an exception other than timeout."""
