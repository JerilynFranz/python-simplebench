"""Validators for Metrics"""
import re
from collections.abc import Iterable
from typing import TYPE_CHECKING

from simplebench.exceptions import SimpleBenchTypeError
from simplebench.report._error_tags import _MetricsErrorTag

if TYPE_CHECKING:
    from ..metric import Metric
    from .metrics import Metrics


LABEL_REGEX = re.compile(r'^[A-Z](?:[A-Z0-9_]*[A-Z0-9])?$')
"""Regex pattern for validating the label of a metric"""

def metrics(value: 'Iterable[Metric] | Metrics') -> tuple['Metric', ...]:
    """Validate that the value is an Mapping of :class:`Metric` instances
    and returns a tuple of the Metric instances.

    :param value: The value to validate and convert.
    :type value: object
    :returns: A tuple of Metric instances.
    :rtype: tuple[Metric, ...]
    :raises SimpleBenchTypeError: If the value is not an iterable of Metric instances or a
        mapping with Metric instances as values.
    """
    from ..metric import Metric
    from .metrics import Metrics
    if isinstance(value, Metrics):
        return tuple(value.values())
    seen_labels: set[str] = set()
    if isinstance(value, Iterable) and not isinstance(value, (str, bytes)):
        metrics_list = []
        for item in value:
            if not isinstance(item, Metric):
                raise SimpleBenchTypeError(
                    f"Expected an iterable of Metric instances, but found an item of type {type(item).__name__}",
                    tag=_MetricsErrorTag.INVALID_METRICS_FIELD_TYPE,
                )
            label = item.label
            if label in seen_labels:
                raise SimpleBenchTypeError(
                    f"Duplicate metric label '{label}' found in metrics iterable",
                    tag=_MetricsErrorTag.DUPLICATE_METRIC_LABEL,
                )
            if not LABEL_REGEX.match(label):
                raise SimpleBenchTypeError(
                    f"Invalid metric label '{label}'. Metric labels must match the pattern: {LABEL_REGEX.pattern!r}",
                    tag=_MetricsErrorTag.INVALID_METRICS_FIELD_TYPE,
                )
            seen_labels.add(item.label)
            metrics_list.append(item)
        return tuple(metrics_list)

    raise SimpleBenchTypeError(
        f"Expected an iterable of Metric instances or a Metrics instance, got {type(value).__name__}",
        tag=_MetricsErrorTag.INVALID_METRICS_FIELD_TYPE,
    )
