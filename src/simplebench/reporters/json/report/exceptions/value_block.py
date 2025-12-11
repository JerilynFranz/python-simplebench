"""Error tags for JSON value block representation exceptions."""
from simplebench.enums import enum_docstrings
from simplebench.exceptions import ErrorTag


@enum_docstrings
class _ValueBlockErrorTag(ErrorTag):
    """Error tags for JSON value block representation exceptions."""
    INVALID_DATA_ARG_EXTRA_KEYS = "INVALID_DATA_ARG_EXTRA_KEYS"
    """The data argument contains unexpected extra keys."""
    INVALID_DATA_ARG_MISSING_KEYS = "INVALID_DATA_ARG_MISSING_KEYS"
    """The data argument is missing required keys."""
    INVALID_VALUE_TIMER_TYPE = "INVALID_VALUE_TIMER_TYPE"
    """The timer value is not a string or None."""
    INVALID_VALUE_TIMER_VALUE = "INVALID_VALUE_TIMER_VALUE"
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
