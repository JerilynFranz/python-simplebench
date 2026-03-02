"""Error tags for JSON raw datablock representation exceptions."""

from simplebench.doc_utils import enum_docstrings
from simplebench.exceptions import ErrorTag

__all__: list[str] = []


@enum_docstrings
class _RawDataBlockErrorTag(ErrorTag):
    """Error tags for JSON raw data block representation exceptions."""

    INVALID_NAME_TYPE = 'INVALID_NAME_TYPE'
    """The name value is not a string."""
    INVALID_NAME_VALUE = 'INVALID_NAME_VALUE'
    """The name value is blank."""
    INVALID_DESCRIPTION_TYPE = 'INVALID_DESCRIPTION_TYPE'
    """The description value is not a string."""
    INVALID_DESCRIPTION_VALUE = 'INVALID_DESCRIPTION_VALUE'
    """The description value is invalid."""
    INVALID_HASH_ID_TYPE = 'INVALID_HASH_ID_TYPE'
    """The hash_id value is not a string."""
    INVALID_HASH_ID_VALUE = 'INVALID_HASH_ID_VALUE'
    """The hash_id value is not either an empty string or a 64-character hexadecimal string."""
    INVALID_SEMANTIC_TYPE_TYPE = 'INVALID_SEMANTIC_TYPE_TYPE'
    """The semantic type value is not a string."""
    INVALID_SEMANTIC_TYPE_VALUE = 'INVALID_SEMANTIC_TYPE_VALUE'
    """The semantic type value is invalid."""
    INVALID_SEMANTIC_TYPE_PATTERN = 'INVALID_SEMANTIC_TYPE_PATTERN'
    """The semantic type value does not match the required pattern."""
    INVALID_VERSION_TYPE = 'INVALID_VERSION_TYPE'
    """The version value is not an integer."""
    UNSUPPORTED_VERSION = 'UNSUPPORTED_VERSION'
    """The version value is not supported."""
    JSON_SCHEMA_VALIDATION_ERROR = 'JSON_SCHEMA_VALIDATION_ERROR'
    """The JSON value does not conform to the expected schema."""
    INVALID_DATA_ARG_EXTRA_KEYS = 'INVALID_DATA_ARG_EXTRA_KEYS'
    """The data argument contains unexpected extra keys."""
    INVALID_DATA_ARG_MISSING_KEYS = 'INVALID_DATA_ARG_MISSING_KEYS'
    """The data argument is missing required keys."""
    INVALID_TIMER_TYPE = 'INVALID_TIMER_TYPE'
    """The timer value is not a string or None."""
    INVALID_TIMER_VALUE = 'INVALID_TIMER_VALUE'
    """The timer value is invalid."""
    INVALID_DATA_TYPE = 'INVALID_DATA_TYPE'
    """The data value is not of type Values."""
    INVALID_SCALE_TYPE = 'INVALID_SCALE_TYPE'
    """The scale value is not a float or int."""
    INVALID_SCALE_VALUE = 'INVALID_SCALE_VALUE'
    """The scale value is invalid."""
    INVALID_UNIT_TYPE = 'INVALID_UNIT_TYPE'
    """The unit value is not a string."""
    INVALID_UNIT_VALUE = 'INVALID_UNIT_VALUE'
    """The unit value is invalid."""
    INVALID_ROUNDS_TYPE = 'INVALID_ROUNDS_TYPE'
    """The rounds value is not an integer."""
    INVALID_ROUNDS_VALUE = 'INVALID_ROUNDS_VALUE'
    """The rounds value is not a positive integer."""
