"""Meta Metrics for SimpleBench.

Meta metrics used by reporters and benchmarks.

This is used by reporters to specify which metrics of benchmark results to include
in their output and by benchmarks to specify which metric of the output to generate.

Defined meta Metrics are:

    - META_ALL: All metrics. This is used by reporters to indicate that all
        known/applicable metrics should be included in the output.
    - META_NULL: No metric. This is used when a reporter does not specify a metric.

The 'META_' prefix is used to indicate that the metric is a meta-metric, which
is not a specific metric but rather a way to specify a set of metrics. This is
useful for specifying a set of metrics in a concise way, such as when a reporter
wants to include all known metrics in the output. This is also a reserved prefix
and should not be used for custom metric definitions to prevent future conflicts.
"""
from typing import Final

from simplebench.metric.metric_definition import MetricDefinition
from simplebench.metric.metrics import Metrics

META_NULL: Final[MetricDefinition] = MetricDefinition(
    semantic_type='simplebench_std::null',
    label='META_NULL',
    unit='NULL',
    description='Meta-metric - No metric',
    scale=1.0,
    meta_metric=True)
"""No metric. This is used when a reporter does not specify a metric."""

META_ALL: Final[MetricDefinition] = MetricDefinition(
    semantic_type='simplebench_std::all',
    label='META_ALL',
    unit='N/A',
    description='Meta-metric indicating that all metrics should be included',
    scale=1.0,
    meta_metric=True)
"""Meta-metric indicating that all known/applicable metrics should be included."""

metrics: Final[Metrics] = Metrics([META_NULL, META_ALL])  # pylint: disable=invalid-name
"""All defined meta-metrics.

- `META_NULL`: No metric. This is used when a reporter does not specify a metric for consumption.
- `META_ALL`: All metrics. This is used by reporters to indicate that all known/applicable
    metrics should be included in the output.
"""
