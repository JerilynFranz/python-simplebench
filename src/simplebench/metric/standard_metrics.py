"""Standard Metrics defined by SimpleRunner benchmark runner.

Categories for metrics in reporters and benchmarks.

    This is used by reporters to specify which metrics of benchmark results to include
    in their output and by benchmarks to specify which metric of the output to generate.

    Defined Metrics are:

      - STD_OPS: Operations per second metric.
      - STD_TIMING: Time per measurement metric.
      - STD_MEMORY: Memory usage metric.
      - STD_PEAK_MEMORY: Peak memory usage metric.

    The 'STD_' prefix is used to indicate that the metric is a standard metric
    defined by the SimpleBench library. Custom metrics should use a different prefix.
    Ideally, custom metrics should use a prefix that is unique to the benchmark or
    benchmark suite that defines them to avoid conflicts with other metrics.
"""
from typing import Final

from simplebench.metric.metric_definition import MetricDefinition
from simplebench.metric.metrics import Metrics

STD_OPS: Final[MetricDefinition] = MetricDefinition(
            semantic_type='simplebench_std::operations_per_second',
            label='STD_OPS',
            unit='ops/s',
            description='Operations per second',
            scale=1.0)
"""Operations per second metric.

The operations per second is the average number of operations performed per second.
This is the inverse of STD_TIMING."""

STD_TIMING: Final[MetricDefinition] = MetricDefinition(
    semantic_type='simplebench_std::time_per_operation',
    label='STD_TIMING',
    unit='s',
    description='Time per measurement',
    scale=1.0)
"""Time per measurement metric.

This is the inverse of STD_OPS and has the technical unit of 's/ops', but is usually
referred to as 's' for simplicity and common usage.

The time per measurement is the average of the per-round execution times for an iteration
(an iteration is considered a single measurement but may consist of multiple rounds).
"""

STD_MEMORY: Final[MetricDefinition] = MetricDefinition(
    semantic_type='simplebench_std::memory',
    label='STD_MEMORY',
    unit='bytes',
    description='Memory usage',
    scale=1.0)
"""Memory usage metric."""

STD_PEAK_MEMORY: Final[MetricDefinition] = MetricDefinition(
    semantic_type='simplebench_std::peak_memory',
    label='STD_PEAK_MEMORY',
    unit='bytes',
    description='Peak memory usage',
    scale=1.0)
"""Peak Memory usage metric."""

metrics: Final[Metrics] = Metrics([  # pylint: disable=invalid-name
    STD_OPS,
    STD_TIMING,
    STD_MEMORY,
    STD_PEAK_MEMORY])
"""Standard metrics defined by the SimpleBench library.

- `STD_OPS`: Operations per second metric.
- `STD_TIMING`: Time per measurement metric.
- `STD_MEMORY`: Memory usage metric.
- `STD_PEAK_MEMORY`: Peak memory usage metric.
"""
