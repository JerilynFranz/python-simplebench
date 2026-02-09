"""report Metrics base class.

This class represents Metrics in a report.

It implements validation and serialization/deserialization methods to and from dictionaries
for a metrics property object in the following JSON Schema version:

https://raw.githubusercontent.com/JerilynFranz/python-simplebench/main/schemas/v1/json-report.json

It is not a standalone JSON schema object, but rather a component of the overall JSON report schema object

It is the base implemention of the JSON a metrics object representation.

This makes the implementations of Metrics backwards compatible with future versions
of the JSON report schema and the V1 implementation itself is essentially a frozen snapshot
of the results object representation at the time of the V1 schema release."""

import hashlib
from collections.abc import Iterable, Iterator, Mapping
from types import MappingProxyType
from typing import Any, TypeAlias, cast

from simplebench.exceptions import (
    SimpleBenchAttributeError,
    SimpleBenchKeyError,
    SimpleBenchTypeError,
    SimpleBenchValueError,
)
from simplebench.report._error_tags import _MetricsErrorTag
from simplebench.simplebench_types import Immutable
from simplebench.validators import validate_namespaced_identifier, validate_string

from ..raw_data_block import RawDataBlock
from ..stats_block import StatsBlock
from ..value_block import ValueBlock
from .typeddict_types import ImmutableMetricDictTypes, ImmutableMetricsObjectDict

MetricItem: TypeAlias = StatsBlock | ValueBlock | RawDataBlock
"""Type alias for the possible types of metric items in the metrics dictionary."""

MetricItemsDict: TypeAlias = MappingProxyType[str, MetricItem]
"""Type alias for the metrics dictionary type."""

METRIC_ITEM_TYPES: tuple[type, ...] = (StatsBlock, ValueBlock, RawDataBlock)
"""Tuple of the possible types of metric items in the metrics dictionary."""

__all__: list[str] = []


class MetricsObject(Mapping, Immutable):
    """Immutable base class representing the 'metrics' object in a report ResultsInfo object.

    This is a dictionary where the keys are metric names (strings) and the values
    are MetricItem objects (a StatsBlock, a ValueBlock, or a RawDataBlock).

    It is not a standalone JSON schema object, but rather a subcomponent
    of the results-info JSON schema object that represents the 'metrics' property.

    See :class:`~simplebench.report.versions.v1.ResultsInfo` for more details.

    The typing enforcement is done in the __setitem__ method at initialization time.

    Currently, the only possible types are
    - :class:`~simplebench.report.versions.v1.StatsBlock`
    - :class:`~simplebench.report.versions.v1.ValueBlock`
    - :class:`~simplebench.report.versions.v1.RawDataBlock`
    """

    __slots__ = ('_metric_items', '_hash', '_hash_id')

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
        """
        for metric_name, metric_object in metrics.items():
            validate_namespaced_identifier(metric_name)
            if not isinstance(metric_object, METRIC_ITEM_TYPES):
                raise SimpleBenchTypeError(
                    f'Metric item must be a StatsBlock, ValueBlock, RawDataBlock - got {type(metric_object)}',
                    tag=_MetricsErrorTag.INVALID_METRIC_ITEM_TYPE,
                )
        self._metric_items: MetricItemsDict = cast(MetricItemsDict, MappingProxyType(metrics))

        # Precompute the hash for immutability and fast comparisons
        metric_hashes: list[tuple[str, str]] = []
        for key, value in sorted(self._metric_items.items()):
            metric_hashes.append((key, value.hash_id))
        self._hash_id = hashlib.sha256(repr(metric_hashes).encode('utf-8')).hexdigest()
        self._hash = hash(self._hash_id)

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
            if not isinstance(metric_data, dict):
                raise SimpleBenchTypeError(
                    f'Metric item must be a dictionary, got {type(metric_data)}',
                    tag=_MetricsErrorTag.INVALID_METRIC_ITEM_TYPE,
                )
            discriminator_type = metric_data.get('type')
            if discriminator_type not in supported_metric_types:
                raise SimpleBenchValueError(
                    f'Invalid metric item type: {discriminator_type}', tag=_MetricsErrorTag.INVALID_METRIC_ITEM_TYPE
                )
            metrics[metric_name] = supported_metric_types[discriminator_type].from_dict(metric_data)

        return cls(metrics)

    def to_dict(self) -> ImmutableMetricsObjectDict:
        """Convert the Metrics object instance to a dictionary.

        The returned dictionary is immutable and suitable for JSON serialization.
        It matches the expected structure of the 'metrics' property in the JSON report schema
        as mirrored in the :class:`ImmutableMetricsObjectDict` typed dictionary.

        :return: Dictionary representation of the Metrics object.
        """
        result: dict[str, ImmutableMetricDictTypes] = {}
        for metric_name, metric_item in self._metric_items.items():
            result[metric_name] = metric_item.to_dict()
        return cast(ImmutableMetricsObjectDict, result)

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

        Disabled after initialization to make the MetricsObject immutable.

        The key must be a valid namespaced identifier and the value must be a MetricItem object
        (either a StatsBlock or a ValueBlock).

        The identifier must be in the format 'namespace::type_name' where both namespace
        and type_name start and end with an alphanumeric character and can contain
        underscores in between. The identifier cannot be blank and MUST
        have the same value as the `semantic_type` attribute of the metric item value.

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

        :param key: The metric name.
        :raises SimpleBenchAttributeError: Always, since the MetricsObject is immutable.
        """
        raise SimpleBenchAttributeError(
            f"Metric name '{key}' does not exist in metrics.",
            tag=_MetricsErrorTag.INVALID_METRIC_NAME_VALUE,
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
        """Get the hash of the MetricsObject based on its hash_id."""
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
        """Get the string representation of the MetricsObject instance.

        :return str: The string representation.
        """
        entries = dict(self._metric_items)
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
        return NotImplemented

    def __copy__(self) -> 'MetricsObject':
        inst = self.__class__.__new__(self.__class__)
        inst._metric_items = self._metric_items
        inst._hash = self._hash
        return inst

    def copy(self) -> 'MetricsObject':
        """Get a copy of the MetricsObject.

        :return MetricsObject: A copy of the MetricsObject instance.
        """
        cls = self.__class__
        return cls(self._metric_items)

    @classmethod
    def fromkeys(cls, iterable: Iterable, value: MetricItem | None = None) -> 'MetricsObject':
        return NotImplemented
