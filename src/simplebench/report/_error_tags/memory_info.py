"""ErrorTags for memory info report representation."""
from simplebench.doc_utils import enum_docstrings
from simplebench.exceptions import ErrorTag


@enum_docstrings
class _MemoryInfoErrorTag(ErrorTag):
    """Error tags for memory info report representation validation errors."""
    INVALID_HASH_ID_TYPE = "INVALID_HASH_ID_TYPE"
    """The hash_id value is not of type str."""
    INVALID_HASH_ID_VALUE = "INVALID_HASH_ID_VALUE"
    """The hash_id value is not a valid 64-character hexadecimal string."""
    INVALID_TOTAL_PHYSICAL_TYPE = "INVALID_TOTAL_PHYSICAL_TYPE"
    """The total_physical value is not of type int."""
    NEGATIVE_TOTAL_PHYSICAL_VALUE = "NEGATIVE_TOTAL_PHYSICAL_VALUE"
    """The total_physical value is negative."""
    INVALID_TOTAL_SWAP_TYPE = "INVALID_TOTAL_SWAP_TYPE"
    """The total_swap value is not of type int."""
    NEGATIVE_TOTAL_SWAP_VALUE = "NEGATIVE_TOTAL_SWAP_VALUE"
    """The total_swap value is negative."""
