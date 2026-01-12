"""Collection of metrics selected from the registered metrics."""

from typing import Iterable

from simplebench.exceptions import SimpleBenchTypeError, SimpleBenchValueError
from simplebench.metrics import Metric
from simplebench.metrics.metrics import Metrics
from simplebench.metrics.metrics_registry import metrics_registry

from ._error_tags import _MetricSelectionErrorTag
from .metrics_selection import MetricsSelection
from .metrics_selection_type import MetricsSelectionType

__all__ = []


class MetricsCollection(MetricsSelection):
    """Represents a resolved, immutable set of metrics selected from the registered metrics

    This class is used to represent a resolved set of metrics that have been
    selected from a given universe. The set of metrics is immutable, meaning that
    once the set of metrics is created, it cannot be modified.

    :param metrics: A set of metrics to be selected from the given universe.

    :raises SimpleBenchTypeError: If the provided metrics are not an Iterable[Metrics] or a Metrics instance.
    :raises SimpleBenchValueError: If the provided metrics are an empty Iterable.
    """

    def __init__(self, *args: Metric, metrics: Iterable[Metric] | Metrics | Metric | None = None):
        """Constructor for MetricsCollection.

        Only one of the two ways to provide metrics should be used: either positional arguments
        or the `metrics` keyword argument.

        :param args: Positional arguments representing Metric instances.
        :param metrics: A keyword argument that can be an Iterable of Metric instances,
            a Metrics instance, or a single Metric instance.
        :raises SimpleBenchTypeError: If the provided metrics are not an Iterable[Metrics] or a Metrics instance.
        :raises SimpleBenchValueError: If the provided metrics are an empty Iterable.
        """
        all_metrics: list[Metric] = []

        if args and metrics:
            raise SimpleBenchTypeError(
                "Cannot provide both positional arguments and the 'metrics' keyword argument.",
                tag=_MetricSelectionErrorTag.METRICS_ARGS_AND_METRICS,
            )

        source = args or metrics
        if source is None:
            # No metrics provided, let validation handle it.
            pass

        elif isinstance(source, Metrics):
            # Handle a single Metrics instance passed via keyword
            all_metrics.extend(source.values())

        elif isinstance(source, Metric):
            # Handle a single metric passed via keyword
            all_metrics.append(source)

        elif isinstance(source, Iterable) and not isinstance(source, (str, bytes)):
            # Handle an iterable (from either args or the metrics keyword)
            all_metrics.extend(source)

        else:
            # This case handles if a non-iterable or string is passed to `metrics`
            raise SimpleBenchTypeError(
                'Input must be an iterable of Metric instances.', tag=_MetricSelectionErrorTag.METRICS_NOT_ITERABLE
            )

        self._metrics: Metrics = self._validate_metrics(all_metrics)
        super().__init__(selector_type=MetricsSelectionType.COLLECTION)

    def _validate_metrics(self, metrics: Iterable[Metric]) -> Metrics:
        """Validate the provided metrics.

        :param metrics: An iterable of Metric instances to validate.
        :return: A new Metrics instance containing the validated metrics.
        """
        if isinstance(metrics, (str, bytes)):
            raise SimpleBenchTypeError(
                'metrics must be an Iterable[Metric] or a Metrics instance',
                tag=_MetricSelectionErrorTag.METRICS_STRING_OR_BYTES,
            )
        if not metrics:
            raise SimpleBenchValueError('metrics cannot be empty', tag=_MetricSelectionErrorTag.METRICS_EMPTY)
        metrics_set = set(metrics)
        for metric in metrics_set:
            if not isinstance(metric, Metric):
                raise SimpleBenchTypeError(
                    'Some metrics are not of type Metric', tag=_MetricSelectionErrorTag.METRICS_NOT_METRIC
                )
            if metric not in metrics_registry:
                raise SimpleBenchValueError(
                    'metrics must be registered with the metrics registry', tag=_MetricSelectionErrorTag.NOT_REGISTERED
                )
        return Metrics(metrics_set)

    @property
    def metrics(self) -> Metrics:
        """Returns the set of metrics selected from the given universe."""
        return self._metrics
