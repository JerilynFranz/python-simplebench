"""Collection of metrics selected from the registered metrics."""

from collections.abc import Hashable, Iterator, Set

from simplebench.exceptions import SimpleBenchTypeError, SimpleBenchValueError
from simplebench.metrics import Metric, Metrics, metrics_registry
from simplebench.simplebench_types import ElementCollection, Immutable, is_element_collection

from ._error_tags import _MetricSelectionErrorTag
from ._metrics_selection import MetricsSelection
from ._metrics_selection_type import MetricsSelectionType

__all__: list[str] = []


class MetricsCollection(MetricsSelection, Set[Metric], Immutable, Hashable):
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

    def __init__(self, *args: Metrics | Metric | ElementCollection[Metric]) -> None:
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

        self._metrics: Metrics

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
            for item in source:
                if isinstance(item, Metrics):
                    all_metrics.extend(item.values())
                elif isinstance(item, Metric):
                    all_metrics.append(item)
                else:
                    raise SimpleBenchTypeError(
                        'All items in the ElementCollection must be of type Metric or Metrics '
                        f'(some are not): {source!r} : item = {item!r}',
                        tag=_MetricSelectionErrorTag.METRICS_NOT_METRIC,
                    )

        else:
            raise SimpleBenchTypeError(
                f'Input must be Metric, Metrics, or ElementCollection of Metric instances. Found: {type(source)}',
                tag=_MetricSelectionErrorTag.METRICS_NOT_ITERABLE)

        self._metrics = self._validate_metrics(all_metrics)
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
            if metric.label not in metrics_registry:
                raise SimpleBenchValueError(
                    f'metrics must be registered with the metrics registry: Not found {metric!r}',
                    tag=_MetricSelectionErrorTag.NOT_REGISTERED
                )
        return Metrics(metrics_set)

    @property
    def metrics(self) -> Metrics:
        """Returns a :class:`Metrics` instance of the metrics selected from the given universe.

        This is a copy of the internal metrics to ensure immutability.

        :return: A Metrics instance containing the selected metrics.
        :rtype: Metrics
        """
        return Metrics(self._metrics)

    def __contains__(self, item: object) -> bool:
        """Check if a metric is in the collection.

        It can be checked by Metric instance or by metric label.

        :param item: The metric to check for.
        :type item: Metric | str
        :return: True if the metric is in the collection, False otherwise.
        :rtype: bool
        """
        if isinstance(item, Metric):
            return item.label in self._metrics
        return item in self._metrics

    def __iter__(self) -> Iterator[Metric]:
        """Iterate over metrics in the collection."""
        return iter(self._metrics.values())

    def __len__(self) -> int:
        """Return the number of metrics in the collection.

        :return: The number of metrics.
        :rtype: int
        """
        return len(self._metrics)

    @property
    def metrics_keys(self) -> tuple[str, ...]:
        """Return the names of the metrics in the collection.

        :return: A tuple of metric names.
        :rtype: tuple[str, ...]
        """
        return tuple(self._metrics.keys())

    def __repr__(self) -> str:
        """Return a string representation of the MetricsCollection.

        :return: A string representation of the MetricsCollection.
        :rtype: str
        """
        metrics_list = ', '.join(repr(metric) for metric in self._metrics.values())
        return f'MetricsCollection(metrics=[{metrics_list}])'

    def __le__(self, other: object) -> bool:
        """Return True if this set is a subset of another set.

        :param other: The other set to compare against.
        :type other: object
        :return: True if this set is a subset of the other set, False otherwise.
        :rtype: bool
        """
        if not isinstance(other, Set):
            return NotImplemented
        return set(self._metrics.values()) <= set(other)

    def __lt__(self, other: object) -> bool:
        """Return True if this set is a proper subset of another set.

        :param other: The other set to compare against.
        :type other: object
        :return: True if this set is a proper subset of the other set, False otherwise.
        :rtype: bool
        """
        if not isinstance(other, Set):
            return NotImplemented
        return set(self._metrics.values()) < set(other)

    def __ge__(self, other: object) -> bool:
        """Return True if this set is a superset of another set.

        :param other: The other set to compare against.
        :type other: object
        :return: True if this set is a superset of the other set, False otherwise.
        :rtype: bool
        """
        if not isinstance(other, Set):
            return NotImplemented
        return set(self._metrics.values()) >= set(other)

    def __gt__(self, other: object) -> bool:
        """Return True if this set is a proper superset of another set.

        :param other: The other set to compare against.
        :type other: object
        :return: True if this set is a proper superset of the other set, False otherwise.
        :rtype: bool
        """
        if not isinstance(other, Set):
            return NotImplemented
        return set(self._metrics.values()) > set(other)

    def __and__(self, other: object) -> 'MetricsCollection':
        """Return the intersection of two sets as a new MetricsCollection.

        :param other: The other set to intersect with.
        :type other: object
        :return: A new MetricsCollection containing the intersection of the two sets.
        :rtype: MetricsCollection
        """
        if not isinstance(other, Set):
            return NotImplemented
        metrics = set(self._metrics.values()) & set(other)
        return MetricsCollection(metrics)

    def __or__(self, other: object) -> 'MetricsCollection':
        """Return the union of two sets as a new MetricsCollection.

        :param other: The other set to union with.
        :type other: object
        :return: A new MetricsCollection containing the union of the two sets.
        :rtype: MetricsCollection
        """
        if not isinstance(other, Set):
            return NotImplemented
        metrics = set(self._metrics.values()) | set(other)
        return MetricsCollection(metrics)

    def __sub__(self, other: object) -> 'MetricsCollection':
        """Return the difference of two sets as a new MetricsCollection.

        :param other: The other set to subtract.
        :type other: object
        :return: A new MetricsCollection containing the difference of the two sets.
        :rtype: MetricsCollection
        """
        if not isinstance(other, Set):
            return NotImplemented
        metrics = set(self._metrics.values()) - set(other)
        return MetricsCollection(metrics)

    def __xor__(self, other: object) -> 'MetricsCollection':
        """Return the symmetric difference of two sets as a new MetricsCollection.

        :param other: The other set to symmetric difference with.
        :type other: object
        :return: A new MetricsCollection containing the symmetric difference of the two sets.
        :rtype: MetricsCollection
        """
        if not isinstance(other, Set):
            return NotImplemented
        metrics = set(self._metrics.values()) ^ set(other)
        return MetricsCollection(metrics)

    def isdisjoint(self, other: object) -> bool:
        """Return True if two sets have a null intersection.

        :param other: The other set to compare against.
        :type other: object
        :return: True if the two sets have a null intersection, False otherwise.
        :rtype: bool
        """
        if not isinstance(other, Set):
            return NotImplemented
        return set(self._metrics.values()).isdisjoint(other)

    def __hash__(self) -> int:
        """Return the hash of the MetricsCollection."""
        return hash(frozenset(sorted(self._metrics.values())))

    def __eq__(self, other: object) -> bool:
        """Check equality between two MetricsCollection instances.

        :param other: The other MetricsCollection to compare against.
        :type other: object
        :return: True if both MetricsCollection instances are equal, False otherwise.
        :rtype: bool
        """
        if not isinstance(other, MetricsCollection):
            return NotImplemented
        return self._metrics == other._metrics
