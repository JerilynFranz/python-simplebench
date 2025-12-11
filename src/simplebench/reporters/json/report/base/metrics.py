"""report Metrics base class.

This class represents Metrics in a JSON report.

It implements validation and serialization/deserialization methods to and from dictionaries
for a metrics property object in the following JSON Schema version:

https://raw.githubusercontent.com/JerilynFranz/python-simplebench/main/schemas/v1/json-report.json

It is not a standalone JSON schema object, but rather a component of the overall JSON report schema object

It is the base implemention of the JSON a metrics object representation.

This makes the implementations of Metrics backwards compatible with future versions
of the JSON report schema and the V1 implementation itself is essentially a frozen snapshot
of the results object representation at the time of the V1 schema release."""
from collections import UserDict
from copy import copy
from typing import Any, TypeAlias

from simplebench.exceptions import SimpleBenchKeyError, SimpleBenchTypeError, SimpleBenchValueError
from simplebench.validators import validate_namespaced_identifier, validate_string

from ..exceptions import _MetricsErrorTag
from .stats_block import StatsBlock
from .value_block import ValueBlock

MetricItem: TypeAlias = StatsBlock | ValueBlock


class Metrics(UserDict):
    """Base class representing the 'metrics' object in a JSON report results object.

    This is a dictionary where the keys are metric names (strings) and the values
    are MetricItem objects (either a StatsBlock or a ValueBlock).

    The typing enforcement is done in the __setitem__ method.
    """

    VERSION: int = 0
    """The JSON metrics version number.

    :note: This should be overridden in sub-classes."""

    TYPE: str = "SimpleBenchMetrics::V0"
    """The JSON metrics type."""

    @classmethod
    def from_dict(cls, data: dict[str, dict[str, Any]]) -> "Metrics":
        """Create a Metrics object instance from a dictionary.

        :param data: Dictionary containing the JSON results object data.
        :return: JSON Metrics object instance.
        """

        cls.validate_type(data.get('type'), cls.TYPE)

        value_block: str = f"SimpleBenchValueBlock::V{cls.VERSION}"
        stats_block: str = f"SimpleBenchStatsBlock::V{cls.VERSION}"

        metrics: dict[str, MetricItem] = {}
        for metric_name, metric_data in data.get('metrics', {}).items():
            validated_metric_name: str = validate_string(
                metric_name, 'metric name',
                _MetricsErrorTag.INVALID_METRIC_NAME_TYPE,
                _MetricsErrorTag.INVALID_METRIC_NAME_VALUE,
                allow_blank=False, strip=True)
            validate_namespaced_identifier(validated_metric_name)
            if not isinstance(metric_data, dict):
                raise SimpleBenchTypeError(
                    f"Metric item must be a dictionary, got {type(metric_data)}",
                    tag=_MetricsErrorTag.INVALID_METRIC_ITEM_TYPE)
            discriminator_type = metric_data.get('type')
            if discriminator_type == value_block:
                metrics[metric_name] = ValueBlock.from_dict(metric_data)

            elif discriminator_type == stats_block:
                metrics[metric_name] = StatsBlock.from_dict(metric_data)

            else:
                raise SimpleBenchValueError(
                    f"Invalid metric item type: {discriminator_type}",
                    tag=_MetricsErrorTag.INVALID_METRIC_ITEM_TYPE)

        return cls(metrics=metrics)

    def __init__(self, metrics: dict[str, MetricItem]):
        """Initialize a Metrics v1 instance.
        :param metrics: The metrics dictionary. The keys are metric names
            and the values are MetricItem objects (either a StatsBlock or a ValueBlock).

            The keys must must be in the format 'namespace::type_name'
            where both namespace and type_name start and end with an alphanumeric character
            and can contain underscores in between."
        """
        for metric_name, metric_object in metrics.items():
            validate_namespaced_identifier(metric_name)
            if not isinstance(metric_object, MetricItem):
                raise SimpleBenchTypeError(
                    f"Metric item must be a StatsBlock or ValueBlock, got {type(metric_object)}",
                    tag=_MetricsErrorTag.INVALID_METRIC_ITEM_TYPE)
        super().__init__(copy(metrics))

    @classmethod
    def validate_type(cls, found: Any, expected: str) -> str:
        """Validate the type.

        :param found: The type string to validate.
        :param expected: The expected type string.
        :return: The validated type string.
        :raise SimpleBenchTypeError: If the type is not a string.
        :raises SimpleBenchValueError: If the type is invalid.
        """
        if not isinstance(found, str):
            raise SimpleBenchValueError(
                f"type must be a string, got {type(found)}",
                tag=_MetricsErrorTag.INVALID_TYPE_TYPE)
        if found != expected:
            raise SimpleBenchValueError(
                f"Incorrect type for JSONMetrics: {found} (expected '{expected}')",
                tag=_MetricsErrorTag.INVALID_TYPE_VALUE)
        return found

    def __setitem__(self, key: str, value: MetricItem) -> None:
        """Set a metric item in the metrics dictionary.

        :param key: The metric name.
        :param value: The MetricItem object (either a StatsBlock or a ValueBlock).
        :raises SimpleBenchKeyError: If the metric name is invalid.
        :raises SimpleBenchTypeError: If the metric item is not of the correct type.
        """
        try:
            validate_namespaced_identifier(key)
        except SimpleBenchValueError as e:
            raise SimpleBenchKeyError(
                f"Invalid metric name '{key}': {e}",
                tag=_MetricsErrorTag.INVALID_METRIC_NAME_VALUE) from e
        if not isinstance(value, MetricItem):
            raise SimpleBenchTypeError(
                f"Metric item must be a StatsBlock or ValueBlock, got {type(value)}",
                tag=_MetricsErrorTag.INVALID_METRIC_ITEM_TYPE)
        super().__setitem__(key, value)

    def __getitem__(self, key: str) -> MetricItem:
        """Get a metric item from the metrics dictionary.

        :param key: The metric name.
        :return: The MetricItem object (either a StatsBlock or a ValueBlock).
        :raises SimpleBenchKeyError: If the metric name does not exist.
        """
        try:
            return super().__getitem__(key)
        except KeyError as e:
            raise SimpleBenchKeyError(
                f"Metric name '{key}' does not exist in metrics.",
                tag=_MetricsErrorTag.INVALID_METRIC_NAME_VALUE) from e

    def __delitem__(self, key: str) -> None:
        """Delete a metric item from the metrics dictionary.

        :param key: The metric name.
        :raises SimpleBenchKeyError: If the metric name does not exist.
        """
        try:
            super().__delitem__(key)
        except KeyError as e:
            raise SimpleBenchKeyError(
                f"Metric name '{key}' does not exist in metrics.",
                tag=_MetricsErrorTag.INVALID_METRIC_NAME_VALUE) from e
