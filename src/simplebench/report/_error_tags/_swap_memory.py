"""Swap memory related error tags."""

from simplebench.doc_utils import enum_docstrings
from simplebench.exceptions import ErrorTag


@enum_docstrings
class _SwapMemoryErrorTag(ErrorTag):
    """Error tags related to swap memory information validation."""

    INVALID_TOTAL_TYPE = 'INVALID_TOTAL_TYPE'
    """The total swap memory value is not of type int."""
    INVALID_TOTAL_VALUE = 'INVALID_TOTAL_VALUE'
    """The total swap memory value is negative."""
    INVALID_USED_TYPE = 'INVALID_USED_TYPE'
    """The used swap memory value is not of type int."""
    INVALID_USED_VALUE = 'INVALID_USED_VALUE'
    """The used swap memory value is negative."""
    INVALID_FREE_TYPE = 'INVALID_FREE_TYPE'
    """The free swap memory value is not of type int."""
    INVALID_FREE_VALUE = 'INVALID_FREE_VALUE'
    """The free swap memory value is negative."""
    INVALID_SWAP_PERCENT_TYPE = 'INVALID_SWAP_PERCENT_TYPE'
    """The swap memory percent value is not of type float."""
    INVALID_SWAP_PERCENT_OUT_OF_RANGE = 'INVALID_SWAP_PERCENT_OUT_OF_RANGE'
    """The swap memory percent value is not between 0 and 100."""
    INVALID_SWAP_IN_TYPE = 'INVALID_SWAP_IN_TYPE'
    """The swap in value is not of type int."""
    INVALID_SWAP_IN_VALUE = 'INVALID_SWAP_IN_VALUE'
    """The swap in value is negative."""
    INVALID_SWAP_OUT_TYPE = 'INVALID_SWAP_OUT_TYPE'
    """The swap out value is not of type int."""
    INVALID_SWAP_OUT_VALUE = 'INVALID_SWAP_OUT_VALUE'
    """The swap out value is negative."""
