"""Error tags for metric registry operations."""

from enum import auto
from simplebench.doc_utils import enum_docstrings
from simplebench.exceptions import ErrorTag

__all__: list[str] = []


@enum_docstrings
class _MetricsRegistryErrorTag(ErrorTag):
    """Enumerates error tags for metric registry operations."""

    NOT_ITERABLE_OF_METRIC = auto()
    """The provided input is not iterable or does not contain valid Metric objects."""
    DUPLICATE_METRIC_NAME = auto()
    """A metric with the same name already exists in the registry."""
    NOT_METRIC_OR_ITERABLE_OF_METRICS = auto()
    """The provided input is neither a Metric object nor an iterable of Metric objects."""
    NOT_STRING_OR_ITERABLE_OF_STRINGS = auto()
    """The provided input is neither a string nor an iterable of strings."""
    INVALID_FILTER_TYPE = auto()
    """The provided filter type is invalid."""
    INVALID_METRICS_ARGUMENT = auto()
    """The provided metrics argument is invalid."""
    INVALID_FILTER_CATEGORY = auto()
    """The provided filter category is invalid."""
