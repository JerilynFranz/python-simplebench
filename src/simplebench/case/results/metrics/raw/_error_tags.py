"""ErrorTags for the simplebench raw module."""

from enum import auto
from simplebench.doc_utils import enum_docstrings
from simplebench.exceptions.error_tag import ErrorTag


@enum_docstrings
class _RawErrorTag(ErrorTag):
    """ErrorTags for the Raw class."""
    INVALID_TIMER_ARG_TYPE = auto()
    """The timer argument is of an invalid type (not str or None)."""
    INVALID_TIMER_ARG_VALUE = auto()
    """The timer argument is an invalid value (blank string)."""
    INVALID_DATA_ARG_TYPE = auto()
    """The data argument is of an invalid type (not Values)."""
    INVALID_ROUNDS_ARG_TYPE = auto()
    """The rounds argument is of an invalid type (not int)."""
    INVALID_ROUNDS_ARG_VALUE = auto()
    """The rounds argument is an invalid value (not > 0)."""
    INVALID_METRIC_CATEGORY = auto()
    """The metric category is invalid (not 'RAW')."""
