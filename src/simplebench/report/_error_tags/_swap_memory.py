"""Swap memory related error tags."""

from enum import auto
from simplebench.doc_utils import enum_docstrings
from simplebench.exceptions import ErrorTag


@enum_docstrings
class _SwapMemoryErrorTag(ErrorTag):
    """Error tags related to swap memory information validation."""

    INVALID_TOTAL_TYPE = auto()
    """The total swap memory value is not of type int."""
    INVALID_TOTAL_VALUE = auto()
    """The total swap memory value is negative."""
    INVALID_USED_TYPE = auto()
    """The used swap memory value is not of type int."""
    INVALID_USED_VALUE = auto()
    """The used swap memory value is negative."""
    INVALID_FREE_TYPE = auto()
    """The free swap memory value is not of type int."""
    INVALID_FREE_VALUE = auto()
    """The free swap memory value is negative."""
    INVALID_SWAP_PERCENT_TYPE = auto()
    """The swap memory percent value is not of type float."""
    INVALID_SWAP_PERCENT_OUT_OF_RANGE = auto()
    """The swap memory percent value is not between 0 and 100."""
    INVALID_SWAP_IN_TYPE = auto()
    """The swap in value is not of type int."""
    INVALID_SWAP_IN_VALUE = auto()
    """The swap in value is negative."""
    INVALID_SWAP_OUT_TYPE = auto()
    """The swap out value is not of type int."""
    INVALID_SWAP_OUT_VALUE = auto()
    """The swap out value is negative."""
