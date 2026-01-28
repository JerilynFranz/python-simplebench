"""ErrorTags for the simplebench raw module."""

from simplebench.doc_utils import enum_docstrings
from simplebench.exceptions.error_tag import ErrorTag


@enum_docstrings
class _RawErrorTag(ErrorTag):
    """ErrorTags for the Raw class."""
    INVALID_TIMER_ARG_TYPE = 'INVALID_TIMER_ARG_TYPE'
    """The timer argument is of an invalid type (not str or None)."""
    INVALID_TIMER_ARG_VALUE = 'INVALID_TIMER_ARG_VALUE'
    """The timer argument is an invalid value (blank string)."""
    INVALID_DATA_ARG_TYPE = 'INVALID_DATA_ARG_TYPE'
    """The data argument is of an invalid type (not Values)."""
    INVALID_ROUNDS_ARG_TYPE = 'INVALID_ROUNDS_ARG_TYPE'
    """The rounds argument is of an invalid type (not int)."""
    INVALID_ROUNDS_ARG_VALUE = 'INVALID_ROUNDS_ARG_VALUE'
    """The rounds argument is an invalid value (not > 0)."""
    INVALID_METRIC_CATEGORY = 'INVALID_METRIC_CATEGORY'
    """The metric category is invalid (not 'RAW')."""
