"""ErrorTags for memory info report representation."""

from enum import auto
from simplebench.doc_utils import enum_docstrings
from simplebench.exceptions import ErrorTag


@enum_docstrings
class _MemoryInfoErrorTag(ErrorTag):
    """Error tags for memory info report representation validation errors."""

    INVALID_HASH_ID_TYPE = auto()
    """The hash_id value is not of type str."""
    INVALID_HASH_ID_VALUE = auto()
    """The hash_id value is not a valid 64-character hexadecimal string."""
    INVALID_SWAP_MEMORY_TYPE = auto()
    """The swap_memory value is not of type SwapMemoryObject."""
    INVALID_VIRTUAL_MEMORY_TYPE = auto()
    """The virtual_memory value is not of type VirtualMemoryObject."""
