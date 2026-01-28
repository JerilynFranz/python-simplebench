"""Error tags for MetricsTimers validation."""

from simplebench.doc_utils import enum_docstrings
from simplebench.exceptions import ErrorTag


@enum_docstrings
class _MetricsTimersErrorTag(ErrorTag):
    """Error tags for metrics timers validation errors."""

    METRICS_TIMERS_INVALID_ARG_TYPE = "METRICS_TIMERS_INVALID_ARG_TYPE"
    """The  argument is not a mapping of Metrics to :class:`Values`."""
    METRICS_TIMERS_INVALID_ARG_KEY_TYPE = "METRICS_TIMERS_INVALID_ARG_KEY_TYPE"
    """One or more keys in the metrics argument are not Metrics."""
    METRICS_TIMERS_INVALID_ARG_KEY_VALUE = "METRICS_TIMERS_INVALID_ARG_KEY_VALUE"
    """One or more keys in the metrics_timers argument are not valid Metrics."""
    METRICS_TIMERS_INVALID_ARG_VALUE_TYPE = "METRICS_TIMERS_INVALID_ARG_VALUE_TYPE"
    """One or more values in the metrics_timers argument are not a :class:`str` or :obj:`None`."""
    METRICS_TIMERS_IMMUTABLE = "METRICS_TIMERS_IMMUTABLE"
    """Attempted to modify an immutable MetricsTimers instance."""
    METRICS_TIMERS_KEY_ERROR = "METRICS_TIMERS_KEY_ERROR"
    """The specified key was not found in the MetricsTimers instance."""