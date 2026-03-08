"""Virtual memory related error tags."""

from enum import auto
from simplebench.doc_utils import enum_docstrings
from simplebench.exceptions import ErrorTag


@enum_docstrings
class _VirtualMemoryErrorTag(ErrorTag):
    """Error tags related to virtual memory information validation."""

    INVALID_TOTAL_TYPE = auto()
    """The total virtual memory value is not of type int."""
    INVALID_TOTAL_VALUE = auto()
    """The total virtual memory value is negative."""
    INVALID_AVAILABLE_TYPE = auto()
    """The available virtual memory value is not of type int."""
    INVALID_AVAILABLE_VALUE = auto()
    """The available virtual memory value is negative."""
    INVALID_PERCENT_TYPE = auto()
    """The percent virtual memory value is not of type float."""
    INVALID_PERCENT_OUT_OF_RANGE = auto()
    """The percent virtual memory value is not between 0 and 100."""
    INVALID_USED_TYPE = auto()
    """The used virtual memory value is not of type int."""
    INVALID_USED_VALUE = auto()
    """The used virtual memory value is negative."""
    INVALID_FREE_TYPE = auto()
    """The free virtual memory value is not of type int."""
    INVALID_FREE_VALUE = auto()
    """The free virtual memory value is negative."""
