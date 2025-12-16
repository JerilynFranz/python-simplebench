"""Registry for metrics and their corresponding functions.

The registry is a global dictionary that maps metric labels to their corresponding functions.
This allows for easy addition, removal, and lookup of metrics by their labels.

Functions:
- `register(metrics)`: Register one or more new metrics in the registry.
- `unregister(metrics)`: Unregister one or more metrics from the registry.
- `clear()`: Clear all registered metrics from the registry.

The registry is initialized with the default metrics defined in
`simplebench.metric.meta_metrics` and in `simplebench.metric.standard_metrics`
and can be extended or modified using the provided functions.

The registry itself is a global variable named `registry`
and is an instance of :class:`simplebench.metric.Metrics`.
"""
from typing import Final, Iterable

import simplebench.metric.meta_metrics as meta_metrics
import simplebench.metric.standard_metrics as standard_metrics
from simplebench.exceptions import SimpleBenchTypeError
from simplebench.metric.metric_definition import MetricDefinition
from simplebench.metric.metrics import Metrics
from simplebench.validators import validate_iterable_of_type

from ._error_tags import _MetricRegistryErrorTag


def register(metrics: MetricDefinition | Iterable[MetricDefinition] | Metrics) -> None:
    """Register one or more new metrics in the registry.

    :param metrics: A single metric definition or an iterable of metric definitions to register.
        or a :class:`Metrics` instance to register all its metrics.
    :raises SimpleBenchTypeError: If `metrics` is not a MetricDefinition or an iterable of MetricDefinitions
        or a :class:`Metrics` instance.
    """
    if isinstance(metrics, Metrics):
        registry.extend(metrics)
        return

    if isinstance(metrics, MetricDefinition):
        registry[metrics.label] = metrics
        return

    validated_metrics = validate_iterable_of_type(
        metrics, MetricDefinition, "metrics",
        _MetricRegistryErrorTag.NOT_ITERABLE_OF_METRIC_DEFINITIONS,
        _MetricRegistryErrorTag.NOT_ITERABLE_OF_METRIC_DEFINITIONS)
    registry.extend(validated_metrics)


def unregister(metrics: str | Iterable[str] | MetricDefinition | Metrics) -> None:
    """Unregister one or more metrics from the registry.

    :param metrics: A single metric label, a MetricDefinition, an iterable of metric labels,
        or a Metrics instance (to unregister all its metric labels).
    :raises SimpleBenchTypeError: If `metrics` is not one of the supported types.
    """
    if isinstance(metrics, str):
        del registry[metrics]

    elif isinstance(metrics, MetricDefinition):
        del registry[metrics.label]

    # This handles an iterable of strings or a Metrics object (which iterates its keys)
    elif isinstance(metrics, Iterable):
        for metric_label in metrics:
            del registry[metric_label]
    else:
        raise SimpleBenchTypeError(
            "metrics must be a string, MetricDefinition, an iterable of strings, or a Metrics instance",
            tag=_MetricRegistryErrorTag.NOT_STRING_OR_ITERABLE_OF_STRINGS)


def reset() -> None:
    """Clear all metrics and restore the default meta-metrics and standard metrics."""
    registry.clear()
    registry.extend(meta_metrics.metrics + standard_metrics.metrics)


def clear() -> None:
    """Clear all registered metrics from the registry."""
    registry.clear()


registry: Final[Metrics] = Metrics()  # pylint: disable=invalid-name
"""Registry for metrics and their corresponding functions.

This is a global variable that maps metric labels to their corresponding functions."""
reset()  # Initialize with default metrics
