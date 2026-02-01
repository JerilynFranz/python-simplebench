"""Error tags for metric selectors."""

from simplebench.doc_utils import enum_docstrings
from simplebench.exceptions import ErrorTag

__all__: list[str] = []


@enum_docstrings
class _MetricSelectionErrorTag(ErrorTag):
    """Error tags for metric selectors.

    These tags are used to categorize and handle errors that may occur when working with metric selectors.
    """

    METRICS_ARGS_AND_METRICS = 'METRICS_ARGS_AND_METRICS'
    """Both *args and metrics are provided. Only one should be provided."""
    METRICS_NOT_ITERABLE = 'METRICS_NOT_ITERABLE'
    """The provided metrics are not a Metric, Metrics, or ElementCollection of Metric instances."""
    METRICS_STRING_OR_BYTES = 'METRICS_STRING_OR_BYTES'
    """The provided metrics are a string or bytes (not Metrics instances or Iterable[Metric])."""
    METRICS_NOT_METRIC = 'METRICS_NOT_METRIC'
    """The provided metrics are not instances of Metric."""
    NOT_REGISTERED = 'NOT_REGISTERED'
    """The provided metric is not registered in the metric registry."""
    METRICS_EMPTY = 'METRICS_EMPTY'
    """The provided metrics are empty."""
