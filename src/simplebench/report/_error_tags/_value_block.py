"""Error tags for JSON value block representation exceptions."""

from enum import auto
from simplebench.doc_utils import enum_docstrings
from simplebench.exceptions import ErrorTag

__all__: list[str] = []


@enum_docstrings
class _ValueBlockErrorTag(ErrorTag):
    """Error tags for JSON value block representation exceptions."""

    INVALID_HASH_ID_TYPE = auto()
    """The hash_id value is not a string."""
    INVALID_HASH_ID_VALUE = auto()
    """The hash_id value is invalid.

    Must be a 64-character hexadecimal string or an empty string.
    """
    INVALID_HASH_ID_STRUCTURE = auto()
    """The hash_id value is not a valid 64-character hexadecimal string."""
    INVALID_SEMANTIC_TYPE_TYPE = auto()
    """The semantic type value is not a string."""
    INVALID_SEMANTIC_TYPE_VALUE = auto()
    """The semantic type value is invalid."""
    INVALID_VERSION_TYPE = auto()
    """The version value is not an integer."""
    UNSUPPORTED_VERSION = auto()
    """The version value is not supported."""
    JSON_SCHEMA_VALIDATION_ERROR = auto()
    """The JSON value does not conform to the expected schema."""
    INVALID_DATA_ARG_EXTRA_KEYS = auto()
    """The data argument contains unexpected extra keys."""
    INVALID_DATA_ARG_MISSING_KEYS = auto()
    """The data argument is missing required keys."""
    INVALID_TIMER_TYPE = auto()
    """The timer value is not a string or None."""
    INVALID_TIMER_VALUE = auto()
    """The timer value is invalid."""
    INVALID_VALUE_TYPE = auto()
    """The type value is not a string."""
    INVALID_VALUE_VALUE = auto()
    """The type value is invalid."""
    INVALID_VALUE_PATTERN = auto()
    """The type value does not match the required pattern."""
    INVALID_SCALE_TYPE = auto()
    """The scale value is not a float or int."""
    INVALID_SCALE_VALUE = auto()
    """The scale value is invalid."""
    INVALID_UNIT_TYPE = auto()
    """The unit value is not a string."""
    INVALID_UNIT_VALUE = auto()
    """The unit value is invalid."""
