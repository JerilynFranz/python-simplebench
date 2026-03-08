"""Validators for MetricTypes"""
import re
from collections.abc import Iterable
from typing import TYPE_CHECKING

from simplebench.exceptions import SimpleBenchTypeError
from simplebench.report._error_tags import _MetricTypesErrorTag

if TYPE_CHECKING:
    from ..metric_type import MetricType
    from .metric_types import MetricTypes


def metric_types(value: 'Iterable[MetricType] | MetricTypes') -> tuple['MetricType', ...]:
    """Validate that the value is an Mapping of :class:`MetricType` instances
    and returns a tuple of the MetricType instances.

    :param value: The value to validate and convert.
    :type value: object
    :returns: A tuple of MetricType instances.
    :rtype: tuple[MetricType, ...]
    :raises SimpleBenchTypeError: If the value is not an iterable of MetricType instances or a
        mapping with MetricType instances as values.
    """
    from ..metric_type import MetricType
    from .metric_types import MetricTypes
    if isinstance(value, MetricTypes):
        return tuple(value.values())
    seen_labels: set[str] = set()
    if isinstance(value, Iterable) and not isinstance(value, (str, bytes)):
        metrics_list = []
        for item in value:
            if not isinstance(item, MetricType):
                raise SimpleBenchTypeError(
                    f"Expected an iterable of MetricType instances, but found an item of type {type(item).__name__}",
                    tag=_MetricTypesErrorTag.INVALID_METRIC_TYPES_FIELD_TYPE,
                )
            label = item.label
            if label in seen_labels:
                raise SimpleBenchTypeError(
                    f"Duplicate metric label '{label}' found in metrics iterable",
                    tag=_MetricTypesErrorTag.DUPLICATE_METRIC_TYPE_LABEL,
                )
            seen_labels.add(item.label)
            metrics_list.append(item)
        return tuple(metrics_list)

    raise SimpleBenchTypeError(
        f"Expected an iterable of Metric instances or a Metrics instance, got {type(value).__name__}",
        tag=_MetricTypesErrorTag.INVALID_METRIC_TYPES_FIELD_TYPE,
    )
