"""Error tags for JSON value block representation exceptions."""
from simplebench.doc_utils import enum_docstrings
from simplebench.exceptions import ErrorTag

__all__ = []


@enum_docstrings
class _ValueBlockErrorTag(ErrorTag):
    """Error tags for JSON value block representation exceptions."""
    INVALID_HASH_ID_TYPE = "INVALID_HASH_ID_TYPE"
    """The hash_id value is not a string."""
    INVALID_HASH_ID_VALUE = "INVALID_HASH_ID_VALUE"
    """The hash_id value is invalid.
    
    Must be a 64-character hexadecimal string or an empty string.
    """
    INVALID_HASH_ID_STRUCTURE = "INVALID_HASH_ID_STRUCTURE"
    """The hash_id value is not a valid 64-character hexadecimal string."""
    INVALID_SEMANTIC_TYPE_TYPE = "INVALID_SEMANTIC_TYPE_TYPE"
    """The semantic type value is not a string."""
    INVALID_SEMANTIC_TYPE_VALUE = "INVALID_SEMANTIC_TYPE_VALUE"
    """The semantic type value is invalid."""
    INVALID_VERSION_TYPE = "INVALID_VERSION_TYPE"
    """The version value is not an integer."""
    UNSUPPORTED_VERSION = "UNSUPPORTED_VERSION"
    """The version value is not supported."""
    JSON_SCHEMA_VALIDATION_ERROR = "JSON_SCHEMA_VALIDATION_ERROR"
    """The JSON value does not conform to the expected schema."""
    INVALID_DATA_ARG_EXTRA_KEYS = "INVALID_DATA_ARG_EXTRA_KEYS"
    """The data argument contains unexpected extra keys."""
    INVALID_DATA_ARG_MISSING_KEYS = "INVALID_DATA_ARG_MISSING_KEYS"
    """The data argument is missing required keys."""
    INVALID_TIMER_TYPE = "INVALID_TIMER_TYPE"
    """The timer value is not a string or None."""
    INVALID_TIMER_VALUE = "INVALID_TIMER_VALUE"
    """The timer value is invalid."""
    INVALID_VALUE_TYPE = "INVALID_VALUE_TYPE"
    """The type value is not a string."""
    INVALID_VALUE_VALUE = "INVALID_VALUE_VALUE"
    """The type value is invalid."""
    INVALID_VALUE_PATTERN = "INVALID_VALUE_PATTERN"
    """The type value does not match the required pattern."""
    INVALID_SCALE_TYPE = "INVALID_SCALE_TYPE"
    """The scale value is not a float or int."""
    INVALID_SCALE_VALUE = "INVALID_SCALE_VALUE"
    """The scale value is invalid."""
    INVALID_UNIT_TYPE = "INVALID_UNIT_TYPE"
    """The unit value is not a string."""
    INVALID_UNIT_VALUE = "INVALID_UNIT_VALUE"
    """The unit value is invalid."""
