"""Collection of metrics selected from the registered metrics."""

from collections.abc import Iterator, Set
from typing import cast

from typechecked import Immutable

from simplebench.exceptions import SimpleBenchTypeError, SimpleBenchValueError
from simplebench.metrics import Metric
from simplebench.metrics.metrics import Metrics
from simplebench.metrics.metrics_registry import metrics_registry
from simplebench.simplebench_types import ElementCollection, is_element_collection

from ._error_tags import _MetricSelectionErrorTag
from .metrics_selection import MetricsSelection
from .metrics_selection_type import MetricsSelectionType

__all__ = []


class MetricsCollection(MetricsSelection, Set[Metric], Immutable):
    """Represents a resolved, immutable collection of metrics selected from the registered metrics

    This class is used to represent a resolved set of metrics that have been
    selected from a given universe. The set of metrics is immutable, meaning that
    once the set of metrics is created, it cannot be modified.

    The collection itself behaves like a set, supporting standard set operations such as
    union, intersection, difference, and symmetric difference.

    :param args: Positional arguments of Metric, Metrics, or ElementCollection of Metric instances.
    :type args: tuple[ElementCollection[Metric] | Metrics | Metric, ...]
    :return: A MetricsCollection instance containing the selected metrics.
    :rtype: MetricsCollection
    :raises SimpleBenchTypeError: If the provided metrics are not a Metric, Metrics, or
        ElementCollection of Metric instances.
    :raises SimpleBenchValueError: If the provided metrics are an empty collection.
    """

    def __init__(self, *args: ElementCollection[Metric] | Metrics | Metric) -> None:
        """Constructor for MetricsCollection.

        Only one of the two ways to provide metrics should be used: either positional arguments
        or the `metrics` keyword argument. Only one of these should be provided at a time.

        :param args: Positional arguments of Metric, Metrics, or ElementCollection of Metric instances.
        :type args: tuple[ElementCollection[Metric] | Metrics | Metric, ...]
        :raises SimpleBenchTypeError: If the provided metrics are not an ElementCollection[Metric], Metrics,
            or Metric instance.
        :raises SimpleBenchValueError: If no metrics are provided.
        """
        all_metrics: list[Metric] = []

        source = args
        if source is None or (isinstance(source, tuple) and len(source) == 0):
            self._metrics = Metrics()
            super().__init__(selector_type=MetricsSelectionType.COLLECTION)
            return

        elif isinstance(source, Metrics):
            # Handle a single Metrics instance passed via keyword
            all_metrics.extend(source.values())

        elif isinstance(source, Metric):
            # Handle a single metric passed via keyword
            all_metrics.append(source)

        elif is_element_collection(source):
            if all(isinstance(item, Metric) for item in source):
                # Handle an ElementCollection of Metric instances
                all_metrics.extend(cast(ElementCollection[Metric], source))
            else:
                raise SimpleBenchTypeError(
                    'All items in the ElementCollection must be of type Metric (some are not).',
                    tag=_MetricSelectionErrorTag.METRICS_NOT_METRIC,
                )
        else:
            raise SimpleBenchTypeError(
                f'Input must be Metric, Metrics, or ElementCollection of Metric instances. Found: {type(source)}',
                tag=_MetricSelectionErrorTag.METRICS_NOT_ITERABLE)

        self._metrics: Metrics = self._validate_metrics(all_metrics)
        super().__init__(selector_type=MetricsSelectionType.COLLECTION)

    def _validate_metrics(self, metrics: ElementCollection[Metric]) -> Metrics:
        """Validate the provided metrics.

        :param metrics: An iterable of Metric instances to validate.
        :type metrics: ElementCollection[Metric]
        :return: A new Metrics instance containing the validated metrics.
        :rtype: Metrics
        :raises SimpleBenchTypeError: If the provided metrics are not a ElementCollection[Metric].
        :raises SimpleBenchValueError: If the provided metrics are an empty collection.
        """
        if not is_element_collection(metrics):
            raise SimpleBenchTypeError(
                'metrics must be an ElementCollection[Metric]',
                tag=_MetricSelectionErrorTag.METRICS_NOT_ITERABLE
            )
        if len(metrics) == 0:
            return Metrics()

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
        """Returns a :class:`Metrics` instance of the metrics selected from the given universe."""
        return self._metrics

    def __contains__(self, item: object) -> bool:
        """Check if a metric is in the collection."""
        return item in self._metrics

    def __iter__(self) -> Iterator[Metric]:
        """Iterate over metrics in the collection."""
        return iter(self._metrics.values())

    def __len__(self) -> int:
        """Return the number of metrics in the collection."""
        return len(self._metrics)

    @property
    def metrics_keys(self) -> ElementCollection[str]:
        """Return the names of the metrics in the collection."""
        return self._metrics.keys()

    def __repr__(self) -> str:
        """Return a string representation of the MetricsCollection."""
        metrics_list = ', '.join(repr(metric) for metric in self._metrics.values())
        return f'MetricsCollection(metrics=[{metrics_list}])'

    def __le__(self, other: object) -> bool:
        """Return True if this set is a subset of another set."""
        if not isinstance(other, Set):
            return NotImplemented
        return set(self._metrics.values()) <= set(other)

    def __lt__(self, other: object) -> bool:
        """Return True if this set is a proper subset of another set."""
        if not isinstance(other, Set):
            return NotImplemented
        return set(self._metrics.values()) < set(other)

    def __ge__(self, other: object) -> bool:
        """Return True if this set is a superset of another set."""
        if not isinstance(other, Set):
            return NotImplemented
        return set(self._metrics.values()) >= set(other)

    def __gt__(self, other: object) -> bool:
        """Return True if this set is a proper superset of another set."""
        if not isinstance(other, Set):
            return NotImplemented
        return set(self._metrics.values()) > set(other)

    def __and__(self, other: object) -> 'MetricsCollection':
        """Return the intersection of two sets as a new MetricsCollection."""
        if not isinstance(other, Set):
            return NotImplemented
        metrics = set(self._metrics.values()) & set(other)
        return MetricsCollection(metrics)

    def __or__(self, other: object) -> 'MetricsCollection':
        """Return the union of two sets as a new MetricsCollection."""
        if not isinstance(other, Set):
            return NotImplemented
        metrics = set(self._metrics.values()) | set(other)
        return MetricsCollection(metrics)

    def __sub__(self, other: object) -> 'MetricsCollection':
        """Return the difference of two sets as a new MetricsCollection."""
        if not isinstance(other, Set):
            return NotImplemented
        metrics = set(self._metrics.values()) - set(other)
        return MetricsCollection(metrics)

    def __xor__(self, other: object) -> 'MetricsCollection':
        """Return the symmetric difference of two sets as a new MetricsCollection."""
        if not isinstance(other, Set):
            return NotImplemented
        metrics = set(self._metrics.values()) ^ set(other)
        return MetricsCollection(metrics)

    def isdisjoint(self, other: object) -> bool:
        """Return True if two sets have a null intersection."""
        if not isinstance(other, Set):
            return NotImplemented
        return set(self._metrics.values()).isdisjoint(other)

