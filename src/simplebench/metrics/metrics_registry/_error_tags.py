"""Error tags for metric registry operations."""
from simplebench.doc_utils import enum_docstrings
from simplebench.exceptions import ErrorTag


@enum_docstrings
class _MetricsRegistryErrorTag(ErrorTag):
    """Enumerates error tags for metric registry operations."""
    NOT_ITERABLE_OF_METRIC = "NOT_ITERABLE_OF_METRIC"
    """The provided input is not iterable or does not contain valid Metric objects."""
    DUPLICATE_METRIC_NAME = "DUPLICATE_METRIC_NAME"
    """A metric with the same name already exists in the registry."""
    NOT_METRIC_OR_ITERABLE_OF_METRICS = "NOT_METRIC_OR_ITERABLE_OF_METRICS"
    """The provided input is neither a Metric object nor an iterable of Metric objects."""
    NOT_STRING_OR_ITERABLE_OF_STRINGS = "NOT_STRING_OR_ITERABLE_OF_STRINGS"
    """The provided input is neither a string nor an iterable of strings."""
    INVALID_FILTER_TYPE = "INVALID_FILTER_TYPE"
    """The provided filter type is invalid."""
    INVALID_METRICS_ARGUMENT = "INVALID_METRICS_ARGUMENT"
    """The provided metrics argument is invalid."""
    INVALID_FILTER_CATEGORY = "INVALID_FILTER_CATEGORY"
    """The provided filter category is invalid."""
