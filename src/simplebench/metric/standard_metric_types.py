"""Standard Metric Types defined by SimpleRunner benchmark runner.

Types for metrics in reporters and benchmarks.

    This is used by reporters to specify what the metric types of benchmark results are.

    Defined Metric Types are:

      - STD_OPS: Operations per second metric.
      - STD_TIMING: Time per measurement metric.
      - STD_MEMORY: Memory usage metric.
      - STD_PEAK_MEMORY: Peak memory usage metric.
      - STD_TOTAL_ELAPSED_TIME: Total elapsed time for the benchmark.

    The 'STD_' prefix is used to indicate that the metric is a standard metric type
    defined by the SimpleBench library. Custom metric types should use a different prefix.
    Ideally, custom metric types should use a prefix that is unique to the benchmark or
    benchmark suite that defines them to avoid conflicts with other metric types.

    Although metric types are primarily identified by their semantic type,
    having standard labels and units helps with readability and consistency
    across different benchmarks and reporters.

    To promote reusability and consistency, it is advisable to use these standard metric types
    whenever applicable, especially for common metrics like operations per second and timing.

    If a metric type does not fit any of the standard types defined here,
    a custom metric type should be created with a unique semantic type
    to avoid conflicts with existing types.

    Metric types and actual metrics are split into two separate concepts:
    - Metric Types define the nature of the measurement (e.g., operations per second).
    - Metrics are instances that use these types to represent specific measurements
      in benchmarks (e.g., STD_OPS metric using STD_OPS metric type).

    Multiple metrics can share the same metric type if they represent similar measurements
    but differ in other attributes like labels or descriptions because they are used
    in different contexts.
"""
from typing import Final

from simplebench.metric.metric_type import MetricCategory, MetricType
from simplebench.metric.metric_types import MetricTypes

STD_OPS: Final[MetricType] = MetricType(
    category=MetricCategory.STATISTICAL,
    semantic_type='simplebench_std::operations_per_second',
    label='STD_OPS',
    unit='ops/s',
    description='Operations per second',
    scale=1.0)
"""Operations per second metric.

The operations per second is the average number of operations performed per second.
This is the inverse of STD_TIMING."""

STD_TIMING: Final[MetricType] = MetricType(
    category=MetricCategory.STATISTICAL,
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

STD_MEMORY: Final[MetricType] = MetricType(
    category=MetricCategory.STATISTICAL,
    semantic_type='simplebench_std::memory',
    label='STD_MEMORY',
    unit='bytes',
    description='Memory usage',
    scale=1.0)
"""Memory usage metric."""


STD_PEAK_MEMORY: Final[MetricType] = MetricType(
    category=MetricCategory.STATISTICAL,
    semantic_type='simplebench_std::peak_memory',
    label='STD_PEAK_MEMORY',
    unit='bytes',
    description='Peak memory usage',
    scale=1.0)
"""Peak memory usage metric."""

STD_TOTAL_ELAPSED_TIME: Final[MetricType] = MetricType(
    category=MetricCategory.CUMULATIVE,
    semantic_type='simplebench_std::total_elapsed_time',
    label='STD_TOTAL_ELAPSED_TIME',
    unit='s',
    description='Total elapsed time',
    scale=1.0)
"""Total elapsed time metric."""

metrics: Final[MetricTypes] = MetricTypes([  # pylint: disable=invalid-name
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
