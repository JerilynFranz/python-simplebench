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
from collections import UserDict
from collections.abc import Mapping
from copy import copy
from typing import Any, TypeAlias

from simplebench.exceptions import SimpleBenchKeyError, SimpleBenchTypeError, SimpleBenchValueError
from simplebench.report._error_tags import _MetricsErrorTag
from simplebench.validators import validate_namespaced_identifier, validate_string

from .._raw_data_block import RawDataBlock
from .._stats_block import StatsBlock
from .._value_block import ValueBlock

MetricItem: TypeAlias = StatsBlock | ValueBlock | RawDataBlock
"""Type alias for the possible types of metric items in the metrics dictionary."""

METRIC_ITEM_TYPES: tuple[type, ...] = (StatsBlock, ValueBlock, RawDataBlock)
"""Tuple of the possible types of metric items in the metrics dictionary."""


class MetricsObject(UserDict):
    """Immutable base class representing the 'metrics' object in a report ResultsInfo object.

    This is a dictionary (a UserDict) where the keys are metric names (strings) and the values
    are MetricItem objects (a StatsBlock, a ValueBlock, or a RawDataBlock).

    It is not a standalone JSON schema object, but rather a subcomponent
    of the results-info JSON schema object.

    See :class:`~simplebench.report.versions.v1.ResultsInfo` for more details.

    The typing enforcement is done in the __setitem__ method at initialization time.

    Currently, the only possible types are
    - :class:`~simplebench.report.versions.v1.StatsBlock`
    - :class:`~simplebench.report.versions.v1.ValueBlock`
    - :class:`~simplebench.report.versions.v1.RawDataBlock`
    """

    def __init__(self, metrics: Mapping[str, MetricItem]):
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
        super().__init__(copy(metrics))
        self._hash_id: str = ''
        self._frozen: bool = True

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
        for metric_name, metric_data in data.get('metrics', {}).items():
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
            if not discriminator_type in supported_metric_types:
                raise SimpleBenchValueError(
                    f'Invalid metric item type: {discriminator_type}', tag=_MetricsErrorTag.INVALID_METRIC_ITEM_TYPE
                )
            metrics[metric_name] = supported_metric_types[discriminator_type].from_dict(metric_data)

        return cls(metrics)

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
        :raises SimpleBenchKeyError: If the metric name is invalid.
        :raises SimpleBenchTypeError: If the metric item is not of the correct type.
        """
        if self._frozen:
            raise SimpleBenchTypeError(
                'MetricsObject is frozen and cannot be modified after initialization.',
                tag=_MetricsErrorTag.METRICS_OBJECT_FROZEN,
            )
        try:
            validate_namespaced_identifier(key)
        except SimpleBenchValueError as e:
            raise SimpleBenchKeyError(
                f"Invalid metric name '{key}': {e}", tag=_MetricsErrorTag.INVALID_METRIC_NAME_VALUE
            ) from e
        if not isinstance(value, MetricItem):
            raise SimpleBenchTypeError(
                f'Metric item must be a StatsBlock or ValueBlock, got {type(value)}',
                tag=_MetricsErrorTag.INVALID_METRIC_ITEM_TYPE,
            )
        if value.semantic_type != key:
            raise SimpleBenchValueError(
                f"Metric item semantic type '{value.semantic_type}' does not match metric name '{key}'",
                tag=_MetricsErrorTag.INVALID_METRIC_ITEM_SEMANTIC_TYPE,
            )
        super().__setitem__(key, value)

    def __getitem__(self, key: str) -> 'MetricItem':
        """Get a metric item from the metrics dictionary.

        :param key: The metric name.
        :return: The MetricItem object (either a StatsBlock or a ValueBlock).
        :raises SimpleBenchKeyError: If the metric name does not exist.
        """
        try:
            return super().__getitem__(key)
        except KeyError as e:
            raise SimpleBenchKeyError(
                f"Metric name '{key}' does not exist in metrics.", tag=_MetricsErrorTag.INVALID_METRIC_NAME_VALUE
            ) from e

    def __delitem__(self, key: str) -> None:
        """Delete a metric item from the metrics dictionary.

        :param key: The metric name.
        :raises SimpleBenchKeyError: If the metric name does not exist.
        """
        try:
            super().__delitem__(key)
        except KeyError as e:
            raise SimpleBenchKeyError(
                f"Metric name '{key}' does not exist in metrics.", tag=_MetricsErrorTag.INVALID_METRIC_NAME_VALUE
            ) from e

    def __eq__(self, other):
        """Check equality with another MetricsObject."""
        if not isinstance(other, MetricsObject):
            return False
        return self.hash_id == other.hash_id

    def __hash__(self) -> int:
        """Get the hash of the MetricsObject based on its hash_id."""
        return hash(self.hash_id)

    @property
    def hash_id(self) -> str:
        """Get the hash_id property.

        The hash_id is a SHA-256 hash of the concatenated hash_ids of all metric items
        in the metrics dictionary, sorted by metric name for consistency.

        :return: The hash_id string.
        """
        if self._hash_id == '':
            hash_keys = sorted(k for k in self.data.items())
            hashed_subelements: list[str] = []
            for key, value in hash_keys:
                if hasattr(value, 'hash_id'):
                    hashed_subelements.append(f'{key}:{value.hash_id}')
            hash_input = '\x00'.join(hashed_subelements).encode('utf-8')
            self._hash_id = hashlib.sha256(hash_input).hexdigest()
        return self._hash_id
