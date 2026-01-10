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
    INVALID_SWAP_MEMORY_TYPE = "INVALID_SWAP_MEMORY_TYPE"
    """The swap_memory value is not of type SwapMemoryObject."""
    INVALID_VIRTUAL_MEMORY_TYPE = "INVALID_VIRTUAL_MEMORY_TYPE"
    """The virtual_memory value is not of type VirtualMemoryObject."""
