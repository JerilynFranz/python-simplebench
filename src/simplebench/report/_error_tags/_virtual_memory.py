"""Virtual memory related error tags."""
from simplebench.doc_utils import enum_docstrings
from simplebench.exceptions import ErrorTag


@enum_docstrings
class _VirtualMemoryErrorTag(ErrorTag):
    """Error tags related to virtual memory information validation."""
    INVALID_TOTAL_TYPE = "INVALID_TOTAL_TYPE"
    """The total virtual memory value is not of type int."""
    INVALID_TOTAL_VALUE = "INVALID_TOTAL_VALUE"
    """The total virtual memory value is negative."""
    INVALID_AVAILABLE_TYPE = "INVALID_AVAILABLE_TYPE"
    """The available virtual memory value is not of type int."""
    INVALID_AVAILABLE_VALUE = "INVALID_AVAILABLE_VALUE"
    """The available virtual memory value is negative."""
    INVALID_PERCENT_TYPE = "INVALID_PERCENT_TYPE"
    """The percent virtual memory value is not of type float."""
    INVALID_PERCENT_OUT_OF_RANGE = "INVALID_PERCENT_OUT_OF_RANGE"
    """The percent virtual memory value is not between 0 and 100."""
    INVALID_USED_TYPE = "INVALID_USED_TYPE"
    """The used virtual memory value is not of type int."""
    INVALID_USED_VALUE = "INVALID_USED_VALUE"
    """The used virtual memory value is negative."""
    INVALID_FREE_TYPE = "INVALID_FREE_TYPE"
    """The free virtual memory value is not of type int."""
    INVALID_FREE_VALUE = "INVALID_FREE_VALUE"
    """The free virtual memory value is negative."""
