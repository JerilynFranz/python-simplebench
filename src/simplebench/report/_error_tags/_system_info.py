"""ErrorTags for SystemInfo validation errors."""

from enum import auto
from simplebench.doc_utils import enum_docstrings
from simplebench.exceptions import ErrorTag


@enum_docstrings
class _SystemInfoErrorTag(ErrorTag):
    """Error tags for SystemInfo validation errors."""

    INVALID_HASH_ID_TYPE = auto()
    """The hash_id value is not of type str."""
    INVALID_HASH_ID_VALUE = auto()
    """The hash_id value is not a valid 64-character hexadecimal string."""
    INVALID_SYSTEM_TYPE = auto()
    """The system value is not of type str."""
    EMPTY_SYSTEM_VALUE = auto()
    """The system value is an empty string."""
    INVALID_SYSTEM_VERSION_TYPE = auto()
    """The version value is not of type str."""
    EMPTY_SYSTEM_VERSION_VALUE = auto()
    """The version value is an empty string."""
    INVALID_RELEASE_TYPE = auto()
    """The release value is not of type str."""
    EMPTY_RELEASE_VALUE = auto()
    """The release value is an empty string."""
    INVALID_MACHINE_TYPE = auto()
    """The machine value is not of type str."""
    EMPTY_MACHINE_VALUE = auto()
    """The machine value is an empty string."""
