"""Registry for metric defintions and their corresponding functions.

The registry is a globally available :class:`simplebench.metrics.Metrics` object that
maps metric labels to their corresponding functions.

This allows for easy addition, removal, and lookup of metrics by their labels,
as well as filtering of metrics based on their types and categories.

Available Functions:

- :func:`register`: Register one or more new metrics in the registry.
- :func:`unregister`: Unregister one or more metrics from the registry.
- :func:`clear`: Clear all registered metrics from the registry.
- :func:`reset`: Clear all metrics and initialize with the default standard metrics.
- :func:`filtered_metrics`: Return a Metrics object created by filtering
        the metrics registry based on metric types and/or metric categories.

The registry is initialized with the default metrics defined in
:mod:`simplebench.metrics.standard_metrics`
and can be extended or modified using the provided functions.

The registry itself is store in the :obj:`simplebench.metrics.metrics_registry`
and is an instance of :class:`simplebench.metrics.Metrics`.
"""
import simplebench.metrics.standard_metrics as standard_metrics
from simplebench.exceptions import SimpleBenchTypeError
from simplebench.metrics.metric import Metric
from simplebench.metrics.metric_category import MetricCategory
from simplebench.metrics.metric_type import MetricType
from simplebench.metrics.metric_types import MetricTypes
from simplebench.metrics.metrics import Metrics
from simplebench.simplebench_types import ElementCollection, is_element_collection
from simplebench.validators import validate_iterable_of_type


from ._error_tags import _MetricsRegistryErrorTag

__all__: list[str] = []


def register_metrics(metrics: Metric | ElementCollection[Metric] | Metrics) -> None:
    """Register one or more new metrics in the registry.

    :param metrics: A single metric or an iterable of metrics to register.
        or a :class:`Metrics` instance to register all its metrics.
    :raises SimpleBenchTypeError: If `metrics` is not a Metric or an iterable of Metrics
        or a :class:`Metrics` instance.
    """
    if isinstance(metrics, Metrics):
        metrics_registry.extend(metrics)
        return

    if isinstance(metrics, Metric):
        metrics_registry[metrics.label] = metrics
        return

    validated_metrics = validate_iterable_of_type(
        metrics,
        Metric,
        'metrics',
        _MetricsRegistryErrorTag.NOT_ITERABLE_OF_METRIC,
        _MetricsRegistryErrorTag.NOT_ITERABLE_OF_METRIC,
    )
    metrics_registry.extend(validated_metrics)


def unregister_metrics(metrics: str | ElementCollection[str] | Metric | Metrics) -> None:
    """Unregister one or more metrics from the registry.

    :param metrics: A single metric label, a Metric, an iterable of metric labels,
        or a Metrics instance (to unregister all its metric labels).
    :raises SimpleBenchTypeError: If `metrics` is not one of the supported types.
    """
    if isinstance(metrics, str):
        del metrics_registry[metrics]

    elif isinstance(metrics, Metric):
        del metrics_registry[metrics.label]

    # This handles an iterable of strings or a Metrics object (which iterates its keys)
    elif isinstance(metrics, ElementCollection):
        for metric_label in metrics:
            del metrics_registry[metric_label]
    else:
        raise SimpleBenchTypeError(
            'metrics must be a string, Metric, an iterable of strings, or a Metrics instance',
            tag=_MetricsRegistryErrorTag.NOT_STRING_OR_ITERABLE_OF_STRINGS,
        )


def reset_metrics() -> None:
    """Clear all metrics and restore the default meta-metrics and standard metrics."""
    metrics_registry.clear()
    metrics_registry.extend(standard_metrics.metrics())


def clear_metrics() -> None:
    """Clear all registered metrics from the registry."""
    metrics_registry.clear()



def filtered_metrics(
    *,
    metric_types: ElementCollection[MetricType] | MetricTypes | MetricType | None = None,
    metric_categories: ElementCollection[MetricCategory] | MetricCategory | None = None) -> Metrics:
    """Create a Metrics object by filtering the metrics registry based on metric types and/or metric categories.

    If given both metric_types and metric_categories, the resulting Metrics object
    will include only metrics that match both criteria.

    :param metric_types: A single MetricType, an ElementCollection of MetricType, or a MetricTypes object to filter
        the metrics.
    :type metric_types: MetricType | ElementCollection[MetricType] | MetricTypes | None
    :param metric_categories: A single MetricCategory or an ElementCollection of MetricCategory to filter the metrics.
    :type metric_categories: MetricCategory | ElementCollection[MetricCategory] | None
    :return: A new Metrics object containing the filtered metrics.
    """
    filtered: Metrics = _filtered_metrics_by_category(metrics=metrics_registry, metric_categories=metric_categories)

    filtered = _filtered_metrics_by_type(metrics=filtered, metric_types=metric_types)

    return filtered


def _filtered_metrics_by_type(
    *, metrics: Metrics, metric_types: ElementCollection[MetricType] | MetricTypes | MetricType | None = None
) -> Metrics:
    """Create a Metrics object by filtering the metrics registry based on metric types.

    :param metric_types: A single MetricType or an iterable of MetricType to filter the metrics.
    :return: A new Metrics object containing the filtered metrics.
    """
    if not isinstance(metrics, Metrics):
        raise SimpleBenchTypeError(
            'metrics must be a Metrics instance.', tag=_MetricsRegistryErrorTag.INVALID_METRICS_ARGUMENT
        )

    if metric_types is None:
        return metrics

    filter_types: MetricTypes
    if isinstance(metric_types, MetricTypes):
        filter_types = metric_types
    elif isinstance(metric_types, MetricType):
        filter_types = MetricTypes([metric_types])
    elif is_element_collection(metric_types) and all(isinstance(mt, MetricType) for mt in metric_types):
        filter_types = MetricTypes(metric_types)
    else:
        raise SimpleBenchTypeError(
            'metric_types must be a MetricType, an ElementCollection of MetricType, or a MetricTypes instance.',
            tag=_MetricsRegistryErrorTag.INVALID_FILTER_TYPE,
        )

    filtered_items = [metric for metric in metrics.values() if metric.metric_type in filter_types]
    return Metrics(filtered_items)


def _filtered_metrics_by_category(
    *, metrics: Metrics, metric_categories: ElementCollection[MetricCategory] | MetricCategory | None
) -> Metrics:
    """Create a Metrics object by filtering the metrics registry based on metric categories.

    :param metric_categories: A single MetricCategory or an iterable of MetricCategory to filter the metrics.
    :return: A new Metrics object containing the filtered metrics.
    """
    if not isinstance(metrics, Metrics):
        raise SimpleBenchTypeError(
            'metrics must be a Metrics instance.', tag=_MetricsRegistryErrorTag.INVALID_METRICS_ARGUMENT
        )

    if metric_categories is None:
        return metrics

    filter_categories: set[MetricCategory]
    if isinstance(metric_categories, MetricCategory):
        filter_categories = {metric_categories}

    elif is_element_collection(metric_categories) and all(isinstance(mc, MetricCategory) for mc in metric_categories):
        filter_categories = set(metric_categories)
        if not all(isinstance(cat, MetricCategory) for cat in filter_categories):
            raise SimpleBenchTypeError(
                'All items in metric_categories iterable must be of type MetricCategory.',
                tag=_MetricsRegistryErrorTag.INVALID_FILTER_CATEGORY,
            )

    else:
        raise SimpleBenchTypeError(
            'metric_categories must be a MetricCategory or an iterable of MetricCategory.',
            tag=_MetricsRegistryErrorTag.INVALID_FILTER_CATEGORY,
        )

    filtered_items: Metrics = Metrics(
        [metric for metric in metrics.values() if metric.metric_type.category in filter_categories]
    )
    return filtered_items


metrics_registry: Metrics = Metrics()
"""Registry for metrics and their corresponding functions.

This is a global variable that maps metric labels to their corresponding functions."""
reset_metrics()  # Initialize with default metrics
