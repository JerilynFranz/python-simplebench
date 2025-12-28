"""ErrorTags for SystemInfo validation errors."""
from simplebench.doc_utils import enum_docstrings
from simplebench.exceptions import ErrorTag


@enum_docstrings
class _SystemInfoErrorTag(ErrorTag):
    """Error tags for SystemInfo validation errors."""
    INVALID_HASH_ID_TYPE = "INVALID_HASH_ID_TYPE"
    """The hash_id value is not of type str."""
    INVALID_HASH_ID_VALUE = "INVALID_HASH_ID_VALUE"
    """The hash_id value is not a valid 64-character hexadecimal string."""
    INVALID_SYSTEM_TYPE = "INVALID_SYSTEM_TYPE"
    """The system value is not of type str."""
    EMPTY_SYSTEM_VALUE = "EMPTY_SYSTEM_VALUE"
    """The system value is an empty string."""
    INVALID_SYSTEM_VERSION_TYPE = "INVALID_VERSION_TYPE"
    """The version value is not of type str."""
    EMPTY_SYSTEM_VERSION_VALUE = "EMPTY_VERSION_VALUE"
    """The version value is an empty string."""
    INVALID_RELEASE_TYPE = "INVALID_RELEASE_TYPE"
    """The release value is not of type str."""
    EMPTY_RELEASE_VALUE = "EMPTY_RELEASE_VALUE"
    """The release value is an empty string."""
    INVALID_MACHINE_TYPE = "INVALID_MACHINE_TYPE"
    """The machine value is not of type str."""
    EMPTY_MACHINE_VALUE = "EMPTY_MACHINE_VALUE"
    """The machine value is an empty string."""