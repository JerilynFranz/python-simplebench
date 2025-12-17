"""Standard Metrics defined by SimpleRunner benchmark runner.

Types for metrics in reporters and benchmarks.

    This is used by reporters to specify what the metrics of benchmark results are.

    Defined Metrics are:

      - STD_OPS: Operations per second metric.
      - STD_TIMING: Time per measurement metric.
      - STD_MEMORY: Memory usage metric.
      - STD_PEAK_MEMORY: Peak memory usage metric.
      - STD_TOTAL_ELAPSED_TIME: Total elapsed time for the benchmark.

    The 'STD_' prefix is used to indicate that the metric is a standard metric
    defined by the SimpleBench library. Custom metrics should use a different prefix.
    Ideally, custom metrics should use a prefix that is unique to the benchmark or
    benchmark suite that defines them to avoid conflicts with other metrics.
"""
from typing import Final

from simplebench.metric.metric import Metric
from simplebench.metric.metric_types_registry import metric_types_registry as metric_types_registry
from simplebench.metric.metrics import Metrics

STD_OPS: Final[Metric] = Metric(
    label='STD_OPS',
    title="Ops",
    description='Operations per second',
    metric_type=metric_types_registry['STD_OPS'])
"""Operations per second metric.

The operations per second is the average number of operations performed per second.
This is the inverse of STD_TIMING."""

STD_TIMING: Final[Metric] = Metric(
    label='STD_TIMING',
    title="Timing",
    description='Time per measurement',
    metric_type=metric_types_registry['STD_TIMING'])
"""Time per measurement metric.

This is the inverse of STD_OPS and has the technical unit of 's/ops', but is usually
referred to as 's' for simplicity and common usage.

The time per measurement is the average of the per-round execution times for an iteration
(an iteration is considered a single measurement but may consist of multiple rounds).
"""
STD_MEMORY: Final[Metric] = Metric(
    label='STD_MEMORY',
    title="Memory",
    description='Memory usage',
    metric_type=metric_types_registry['STD_MEMORY'])
"""Memory usage metric."""

STD_PEAK_MEMORY: Final[Metric] = Metric(
    label='STD_PEAK_MEMORY',
    title="Peak Memory",
    description='Peak memory usage',
    metric_type=metric_types_registry['STD_PEAK_MEMORY'])
"""Peak memory usage metric."""

STD_TOTAL_ELAPSED_TIME: Final[Metric] = Metric(
    label='STD_TOTAL_ELAPSED_TIME',
    title="Total Elapsed Time",
    description='Total elapsed time',
    metric_type=metric_types_registry['STD_TOTAL_ELAPSED_TIME'])
"""Total elapsed time metric."""

metrics: Final[Metrics] = Metrics([  # pylint: disable=invalid-name
    STD_OPS,
    STD_TIMING,
    STD_MEMORY,
    STD_PEAK_MEMORY,
    STD_TOTAL_ELAPSED_TIME
])
"""Standard metric types defined by the SimpleBench library.

- `STD_OPS`: Operations per second metrics.
- `STD_TIMING`: Time per measurement metrics.
- `STD_MEMORY`: Memory usage metrics.
- `STD_PEAK_MEMORY`: Peak memory usage metric.
- `STD_TOTAL_ELAPSED_TIME`: Total elapsed time metric.
"""
