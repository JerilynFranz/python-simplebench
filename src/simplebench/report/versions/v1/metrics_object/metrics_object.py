"""report Metrics base class.

This class represents Metrics in a report.

It implements validation and serialization/deserialization methods to and from dictionaries
for a metrics property object in the following JSON Schema version:

https://raw.githubusercontent.com/JerilynFranz/python-simplebench/main/schemas/v1/results-info.json

It is not a standalone JSON schema object, but rather a component of the overall JSON report schema object

It is the base implemention of a metrics object representation.
"""

import hashlib
from collections.abc import Iterable, Iterator, Mapping
from typing import Any, TypeAlias

from simplebench.exceptions import (
    SimpleBenchAttributeError,
    SimpleBenchKeyError,
    SimpleBenchTypeError,
    SimpleBenchValueError,
)
from simplebench.report._error_tags import _MetricsErrorTag
from simplebench.simplebench_types import CoreDataMapping, Immutable
from simplebench.validators import validate_namespaced_identifier, validate_string

from ..raw_data_block import RawDataBlock
from ..stats_block import StatsBlock
from ..value_block import ValueBlock
from .metrics_object_dict import ImmutableMetricDictTypes

__all__: list[str] = []

MetricItem: TypeAlias = StatsBlock | ValueBlock | RawDataBlock
"""Type alias for the possible types of metric items in the metrics dictionary."""

METRIC_ITEM_TYPES: tuple[type, ...] = (StatsBlock, ValueBlock, RawDataBlock)
"""Tuple of the possible types of metric items in the metrics dictionary."""


class MetricsObject(Mapping[str, MetricItem], Immutable):
    """Immutable base class representing the 'metrics' object in a report ResultsInfo object.

    This is a dictionary where the keys are metric names (strings) and the values
    are MetricItem objects (a StatsBlock, a ValueBlock, or a RawDataBlock).

    It is not a standalone JSON schema object, but rather a subcomponent
    of the results-info JSON schema object that represents the 'metrics' property.

    See :class:`~simplebench.report.versions.v1.ResultsInfo` for more details.

    Currently, the only possible types are
    - :class:`~simplebench.report.versions.v1.StatsBlock`
    - :class:`~simplebench.report.versions.v1.ValueBlock`
    - :class:`~simplebench.report.versions.v1.RawDataBlock`
    """

    __slots__ = ('_metric_items', '_hash', '_hash_id', "_dict_cache")

    def __init__(self, metrics: Mapping[str, MetricItem]) -> None:
        """Initialize a Metrics v1 instance.

        :param Mapping[str, MetricItem] metrics: The metrics dictionary. The keys are metric names
            and the values are :var:`MetricItem` objects (
            a :class:`~simplebench.report.versions.v1.StatsBlock`,
            :class:`~simplebench.report.versions.v1.ValueBlock`,
            or :class:`~simplebench.report.versions.v1.RawDataBlock` object).

            The keys must must be in the format 'namespace::type_name'
            where both namespace and type_name start and end with an alphanumeric character
            and can contain underscores in between. The identifier cannot be blank.

            They are used to identify the metric against the metrics
            defined in the report schema and to provide a unique identifier for the metric item
            which is used for hashing and comparisons.
        """
        for metric_name, metric_object in metrics.items():
            validate_namespaced_identifier(metric_name)
            if not isinstance(metric_object, METRIC_ITEM_TYPES):
                raise SimpleBenchTypeError(
                    f'Metric item must be a StatsBlock, ValueBlock, RawDataBlock - got {type(metric_object)}',
                    tag=_MetricsErrorTag.INVALID_METRIC_ITEM_TYPE,
                )
        # Shallow copy the input dictionary to ensure immutability and prevent external modifications.
        self._metric_items: dict[str, MetricItem] = dict(metrics)

        # Precompute the hash for immutability and fast comparisons
        metric_hashes: list[tuple[str, str]] = []
        for key, value in sorted(self._metric_items.items()):
            metric_hashes.append((key, value.hash_id))
        self._hash_id = hashlib.sha256(repr(metric_hashes).encode('utf-8')).hexdigest()
        self._hash = hash(self._hash_id)
        self._dict_cache: CoreDataMapping | None = None

    @classmethod
    def from_dict(cls, data: Mapping[str, Mapping[str, Any]]) -> 'MetricsObject':
        """Create a Metrics object instance from a dictionary.

        :param data: Dictionary containing the JSON results object data.
        :return: JSON Metrics object instance.
        """
        supported_metric_types: dict[str, type[MetricItem]] = {
            ValueBlock.TYPE: ValueBlock,
            StatsBlock.TYPE: StatsBlock,
            RawDataBlock.TYPE: RawDataBlock,
        }

        metrics: dict[str, MetricItem] = {}
        for metric_name, metric_data in data.items():
            validated_metric_name: str = validate_string(
                metric_name,
                'metric name',
                _MetricsErrorTag.INVALID_METRIC_NAME_TYPE,
                _MetricsErrorTag.INVALID_METRIC_NAME_VALUE,
                allow_blank=False,
                strip=True,
            )
            validate_namespaced_identifier(validated_metric_name)
            if not isinstance(metric_data, Mapping):
                raise SimpleBenchTypeError(
                    f'Metric item must be a Mapping, got {type(metric_data)}',
                    tag=_MetricsErrorTag.INVALID_METRIC_ITEM_TYPE,
                )
            discriminator_type = metric_data.get('type')
            if discriminator_type not in supported_metric_types:
                raise SimpleBenchValueError(
                    f'Invalid metric item type: {discriminator_type}', tag=_MetricsErrorTag.INVALID_METRIC_ITEM_TYPE
                )
            metrics[validated_metric_name] = supported_metric_types[discriminator_type].from_dict(metric_data)

        return cls(metrics)

    def to_dict(self) -> CoreDataMapping:
        """Convert the Metrics object instance to a dictionary.

        The returned dictionary is immutable and suitable for JSON serialization.
        It matches the expected structure of the 'metrics' property in the JSON report schema
        as mirrored in the :class:`CoreDataMapping` typed dictionary.

        :return: Dictionary representation of the Metrics object.
        """
        if self._dict_cache is None:
            result: dict[str, ImmutableMetricDictTypes] = {}
            for metric_name, metric_item in self._metric_items.items():
                result[metric_name] = metric_item.to_dict()
            self._dict_cache = CoreDataMapping(result)  # type: ignore
        return self._dict_cache

    def for_json(self) -> CoreDataMapping:
        """Get the JSON-serializable dictionary representation of this MetricsObject.

        This method delegates to the for_json method of the dictionary returned by :meth:`to_dict`
        because the dictionary is actually an instance of :class:`CoreDataMapping`
        which has the for_json method to convert to a JSON-serializable dictionary.

        :return: The JSON-serializable dictionary representation of this MetricsObject.
        """
        return self.to_dict().for_json()  # type: ignore

    def as_json(self) -> str:
        """Get the JSON string representation of this MetricsObject.

        This method delegates to the as_json method of the dictionary returned by :meth:`to_dict`
        because the dictionary is actually an instance of :class:`CoreDataMapping`
        which has the as_json method to convert to a JSON string.

        :return: The JSON string representation of this MetricsObject.
        """
        return self.to_dict().as_json()  # type: ignore

    @property
    def hash_id(self) -> str:
        """Get the hash ID of the MetricsObject.

        The hash ID is a SHA-256 hash of the metric names and their corresponding
        metric item hash IDs, ensuring immutability and consistent hashing.

        :return str: The hash ID string.
        """
        return self._hash_id

    def __setitem__(self, key: str, value: MetricItem) -> None:
        """Set a metric item in the metrics dictionary.

        Disabled because the MetricsObject is immutable. Attempting to set an item will raise an error.

        :param key: The metric name.
        :param value: The MetricItem object (either a StatsBlock or a ValueBlock).
        :raises SimpleBenchAttributeError: Always, since the MetricsObject is immutable.
        """
        raise SimpleBenchAttributeError(
            'MetricsObject is immutable and cannot be modified after initialization.',
            tag=_MetricsErrorTag.METRICS_OBJECT_IMMUTABLE,
            name=key,
            obj=self,
        )

    def __getitem__(self, key: str) -> 'MetricItem':
        """Get a metric item from the metrics dictionary.

        :param key: The metric name.
        :return: The MetricItem object (either a StatsBlock or a ValueBlock).
        :raises SimpleBenchKeyError: If the metric name does not exist.
        """
        try:
            return self._metric_items[key]
        except KeyError as e:
            raise SimpleBenchKeyError(
                f"Metric name '{key}' does not exist in metrics.",
                tag=_MetricsErrorTag.KEY_ERROR_INVALID_METRIC_NAME_VALUE,
            ) from e

    def __delitem__(self, key: str) -> None:
        """Delete a metric item from the metrics dictionary.

        Disabled because the MetricsObject is immutable. Attempting to delete an item will raise an error.

        :param key: The metric name.
        :raises SimpleBenchAttributeError: Always, since the MetricsObject is immutable.
        """
        raise SimpleBenchAttributeError(
            f"Metric '{key}' cannot be deleted because the MetricsObject is immutable.",
            tag=_MetricsErrorTag.METRICS_OBJECT_IMMUTABLE,
            name=key,
            obj=self,
        )

    def __eq__(self, other: object) -> bool:
        """Check equality with another MetricsObject.

        :param other: The other MetricsObject to compare with.
        :return bool: True if equal, False otherwise.
        """
        if not isinstance(other, MetricsObject):
            return False
        return self.hash_id == other.hash_id

    def __hash__(self) -> int:
        """Get the hash of the MetricsObject based on its hash_id.

        :return int: The hash value of the MetricsObject.
        """
        return self._hash

    def __len__(self) -> int:
        """Get the number of metric items in the metrics dictionary.

        :return int: The number of metric items.
        """
        return len(self._metric_items)

    def __iter__(self) -> Iterator[str]:
        """Get an iterator over the metric names in the metrics dictionary.

        :return Iterator[str]: An iterator over the metric names.
        """
        return iter(self._metric_items)

    def __repr__(self) -> str:
        """Get a string representation of the MetricsObject instance.

        :return str: The string representation.
        """
        keys = sorted(self._metric_items.keys())
        entries = {key: self._metric_items[key] for key in keys}
        return f'MetricsObject({entries!r})'

    def __or__(self, other: object) -> 'MetricsObject':
        """Return a new MetricsObject that is the union of this and another MetricsObject.

        .. code-block:: python
            new_metrics = this_metrics | other_metrics

        :param other: The other MetricsObject to union with.
        :return MetricsObject: A new MetricsObject that is the union of both.
        """
        if isinstance(other, MetricsObject):
            return self.__class__(dict(self._metric_items) | dict(other._metric_items))
        return NotImplemented

    def __ror__(self, other: object) -> 'MetricsObject':
        """Return a new MetricsObject that is the union of another MetricsObject and this one. (reversed)

        .. code-block:: python
            new_metrics = other_metrics | this_metrics

        :param other: The other MetricsObject to union with.
        :return MetricsObject: A new MetricsObject that is the union of both.
        """
        if isinstance(other, MetricsObject):
            return self.__class__(dict(other._metric_items) | dict(self._metric_items))
        return NotImplemented

    def __ior__(self, other: object) -> 'MetricsObject':
        """In-place union of this MetricsObject with another MetricsObject.

        Disabled because the MetricsObject is immutable. Attempting to perform an in-place union will raise an error.
        """
        return NotImplemented

    def __contains__(self, key: object) -> bool:
        """Check if a metric name is in the metrics dictionary.

        :param key: The metric name to check for.
        :return bool: True if the metric name exists, False otherwise.
        """
        return key in self._metric_items

    def __copy__(self) -> 'MetricsObject':
        """Return the same instance since MetricsObject is immutable.

        :return MetricsObject: The same instance of MetricsObject.
        """
        return self

    def __deepcopy__(self, memo: dict[int, Any]) -> 'MetricsObject':
        """Return a deep copy of the MetricsObject.

        Since MetricsObject is immutable, this method simply returns the same instance.

        :return MetricsObject: The same instance of MetricsObject.
        """
        return self

    def copy(self) -> 'MetricsObject':
        """Get a copy of the MetricsObject.

        It does not create a new instance since MetricsObject is immutable, but it provides
        a copy method for API consistency.

        :return MetricsObject: The same MetricsObject instance.
        """
        return self

    @classmethod
    def fromkeys(cls, iterable: Iterable, value: MetricItem | None = None) -> 'MetricsObject':
        return NotImplemented

    def __getstate__(self) -> tuple[dict[str, Any] | None, tuple[Any, ...]]:
        """Prepare the object's state for pickling, prioritizing size.

        This method ensures that the pickled representation of the MetricsObject
        is compact. It does this by excluding any cached or redundant attributes
        and only including the essential data needed to reconstruct the object.

        This prioritizes a small pickled size and fast subsequent unpickling over
        preserving the lazy-evaluation state across serialization.

        :return: A state tuple for pickling.
        :rtype: tuple[dict[str, Any] | None, tuple[Any, ...]]
        """
        excluded_attrs = {'_dict_cache'}
        slot_values: list[Any] = []
        for slot in self.__slots__:
            if slot in excluded_attrs:
                slot_values.append(None)
            else:
                slot_values.append(getattr(self, slot))

        # Build the state tuple for a __slots__ class. The first element is for
        # __dict__ (None in our case) and the second is a tuple of the slotted values.
        state = tuple(slot_values)
        return (None, state)

    def __setstate__(self, state: tuple[dict[str, Any] | None, tuple[Any, ...]]) -> None:
        """Restore the object's state from a pickled representation.

        This method is the counterpart to `__getstate__`. It takes the state
        tuple and repopulates the instance's `__slots__`.

        .. note::
            This method bypasses `__init__`, which is standard for unpickling.

        :param state: The state tuple from unpickling.
        :type state: tuple[dict[str, Any] | None, tuple[Any, ...]]
        """
        # The first element of the state tuple is for __dict__, which is None for this class.
        # The second element is a tuple of values for the __slots__.
        slot_values = state[1]
        for slot, value in zip(self.__slots__, slot_values, strict=True):
            self.__setattr__(slot, value)
