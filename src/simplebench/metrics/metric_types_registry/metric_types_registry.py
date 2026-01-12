"""Registry for metric type definitions and their corresponding functions.

The registry is a global dictionary that maps metric type labels to their corresponding functions.
This allows for easy addition, removal, and lookup of metric types by their labels.

Functions:
- `register(metric_types)`: Register one or more new metric types in the registry.
- `unregister(metric_types)`: Unregister one or more metric types from the registry.
- `clear()`: Clear all registered metric types from the registry.

The registry is initialized with the default metric types defined in
`simplebench.metric.meta_metrics` and in `simplebench.metric.standard_metrics`
and can be extended or modified using the provided functions.

The registry itself is a global variable named `registry`
and is an instance of :class:`simplebench.metric.MetricTypes`.
"""

from typing import Iterable

from simplebench.exceptions import SimpleBenchTypeError
from simplebench.metrics import standard_metric_types
from simplebench.metrics.metric_type import MetricType
from simplebench.metrics.metric_types import MetricTypes
from simplebench.validators import validate_iterable_of_type

from ._error_tags import _MetricTypesRegistryErrorTag


def register_metric_types(metrics: MetricType | Iterable[MetricType] | MetricTypes) -> None:
    """Register one or more new metric types in the registry.

    :param metrics: A single metric type or an iterable of metric types to register.
        or a :class:`MetricTypes` instance to register all its metric types.
    :raises SimpleBenchTypeError: If `metric_types` is not a MetricType or an iterable of MetricTypes
        or a :class:`MetricTypes` instance.
    """
    if isinstance(metrics, MetricTypes):
        metric_types_registry.extend(metrics)
        return

    if isinstance(metrics, MetricType):
        metric_types_registry[metrics.label] = metrics
        return

    validated_metrics = validate_iterable_of_type(
        metrics,
        MetricType,
        'metrics',
        _MetricTypesRegistryErrorTag.NOT_ITERABLE_OF_METRIC_DEFINITIONS,
        _MetricTypesRegistryErrorTag.NOT_ITERABLE_OF_METRIC_DEFINITIONS,
    )
    metric_types_registry.extend(validated_metrics)


def unregister_metric_types(metric_types: str | Iterable[str] | MetricType | MetricTypes) -> None:
    """Unregister one or more metric types from the registry.

    :param metric_types: A single metric type label, a MetricType, an iterable of metric type labels,
        or a MetricTypes instance (to unregister all its metric type labels).
    :raises SimpleBenchTypeError: If `metric_types` is not one of the supported types.
    """
    if isinstance(metric_types, str):
        del metric_types_registry[metric_types]

    elif isinstance(metric_types, MetricType):
        del metric_types_registry[metric_types.label]

    # This handles an iterable of strings or a Metrics object (which iterates its keys)
    elif isinstance(metric_types, Iterable):
        for metric_label in metric_types:
            del metric_types_registry[metric_label]
    else:
        raise SimpleBenchTypeError(
            'metric_types must be a string, MetricType, an iterable of strings, or a MetricTypes instance',
            tag=_MetricTypesRegistryErrorTag.NOT_STRING_OR_ITERABLE_OF_STRINGS,
        )


def reset_metric_types() -> None:
    """Clear all metric types and restore the default meta-metric types and standard metric types."""
    metric_types_registry.clear()
    metric_types_registry.extend(standard_metric_types.metric_types())


def clear_metric_types() -> None:
    """Clear all registered metrics from the registry."""
    metric_types_registry.clear()


metric_types_registry: MetricTypes = MetricTypes()  # pylint: disable=invalid-name
"""Registry for metrics and their corresponding functions.

This is a global variable that maps metric labels to their corresponding functions."""
reset_metric_types()  # Initialize with default metrics
