"""Error tags for JSON raw datablock representation exceptions."""

from enum import auto

from simplebench.doc_utils import enum_docstrings
from simplebench.exceptions import ErrorTag

__all__: list[str] = []


@enum_docstrings
class _RawDataBlockErrorTag(ErrorTag):
    """Error tags for JSON raw data block representation exceptions."""

    MISSING_METRIC_FIELD = auto()
    """The required 'metric' field is missing from the data."""
    INVALID_METRIC_HASH_ID = auto()
    """The 'metric' field value is not a string."""
    UNKNOWN_METRIC_HASH_ID = auto()
    """The 'metric' field value does not correspond to any known metric hash ID in the metrics registry."""
    INVALID_METRIC_TYPE = auto()
    """The metric value is not an instance of Metric."""
    INVALID_NAME_TYPE = auto()
    """The name value is not a string."""
    INVALID_NAME_VALUE = auto()
    """The name value is blank."""
    INVALID_DESCRIPTION_TYPE = auto()
    """The description value is not a string."""
    INVALID_DESCRIPTION_VALUE = auto()
    """The description value is invalid."""
    INVALID_HASH_ID_TYPE = auto()
    """The hash_id value is not a string."""
    INVALID_HASH_ID_VALUE = auto()
    """The hash_id value is not either an empty string or a 64-character hexadecimal string."""
    INVALID_SEMANTIC_TYPE_TYPE = auto()
    """The semantic type value is not a string."""
    INVALID_SEMANTIC_TYPE_VALUE = auto()
    """The semantic type value is invalid."""
    INVALID_SEMANTIC_TYPE_PATTERN = auto()
    """The semantic type value does not match the required pattern."""
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
    INVALID_DATA_TYPE = auto()
    """The data value is not of type Values."""
    INVALID_SCALE_TYPE = auto()
    """The scale value is not a float or int."""
    INVALID_SCALE_VALUE = auto()
    """The scale value is invalid."""
    INVALID_UNIT_TYPE = auto()
    """The unit value is not a string."""
    INVALID_UNIT_VALUE = auto()
    """The unit value is invalid."""
    INVALID_ROUNDS_TYPE = auto()
    """The rounds value is not an integer."""
    INVALID_ROUNDS_VALUE = auto()
    """The rounds value is not a positive integer."""
