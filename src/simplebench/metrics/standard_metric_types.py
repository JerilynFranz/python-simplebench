"""Standard Metric Types defined by SimpleRunner benchmark runner.

Types for metrics in reporters and benchmarks.

This is used by reporters to specify what the metric types of benchmark results are.

Defined Metric Types are:

- `STD_OPS_STATS`: Operations per second metric statistics.
- `STD_OPS_RAW`: Raw list of operations per second data.
- `STD_TIMING_STATS`: Time per measurement metric statistics.
- `STD_TIMING_RAW`: Raw list of time per measurement data.
- `STD_MEMORY_STATS`: Memory usage metric statistics.
- `STD_MEMORY_RAW`: Raw list of memory usage data.
- `STD_PEAK_MEMORY_STATS`: Peak memory usage metric statistics.
- `STD_PEAK_MEMORY_RAW`: Raw list of peak memory usage data metric.
- `STD_TOTAL_ELAPSED_TIME`: Total elapsed time for the benchmark.
- `STD_TOTAL_CPU_TIME`: Total CPU time for the benchmark.
- `STD_CPU_TIME_STATS`: CPU time per measurement metric statistics.
- `STD_CPU_TIME_RAW`: Raw list of CPU time per measurement data.
- `STD_GC_GEN0_COLLECTIONS_STATS`: Number of garbage collections for generation 0
- `STD_GC_GEN0_COLLECTIONS_RAW`: Number of garbage collections for generation 0 (raw values)
- `STD_GC_GEN1_COLLECTIONS_STATS`: Number of garbage collections for generation 1
- `STD_GC_GEN1_COLLECTIONS_RAW`: Number of garbage collections for generation 1 (raw values)
- `STD_GC_GEN2_COLLECTIONS_STATS`: Number of garbage collections for generation 2
- `STD_GC_GEN2_COLLECTIONS_RAW`: Number of garbage collections for generation 2 (raw values)
- `STD_GC_GEN0_COLLECTED_STATS`: Number of objects collected by garbage collection for generation 0
- `STD_GC_GEN0_COLLECTED_RAW`: Number of objects collected by garbage collection for generation 0 (raw values)
- `STD_GC_GEN1_COLLECTED_STATS`: Number of objects collected by garbage collection for generation 1
- `STD_GC_GEN1_COLLECTED_RAW`: Number of objects collected by garbage collection for generation 1 (raw values)
- `STD_GC_GEN2_COLLECTED_STATS`: Number of objects collected by garbage collection for generation 2
- `STD_GC_GEN2_COLLECTED_RAW`: Number of objects collected by garbage collection for generation 2 (raw values)
- `STD_GC_GEN0_UNCOLLECTABLE_STATS`: Number of uncollectable objects for generation 0
- `STD_GC_GEN0_UNCOLLECTABLE_RAW`: Number of uncollectable objects for generation 0 (raw values)
- `STD_GC_GEN1_UNCOLLECTABLE_STATS`: Number of uncollectable objects for generation 1
- `STD_GC_GEN1_UNCOLLECTABLE_RAW`: Number of uncollectable objects for generation 1 (raw values)
- `STD_GC_GEN2_UNCOLLECTABLE_STATS`: Number of uncollectable objects for generation 2
- `STD_GC_GEN2_UNCOLLECTABLE_RAW`: Number of uncollectable objects for generation 2 (raw values)
The 'STD_' prefix is used to indicate that the metric is a standard metric type
defined by the SimpleBench library. Custom metric types should use a different prefix.
Ideally, custom metric types should use a prefix that is unique to the benchmark or
benchmark suite that defines them to avoid conflicts with other metric types.

Although metric types are primarily identified by their semantic type,
having standard labels and units helps with readability, selectability, and consistency
across different benchmarks and reporters and allows for specification of metrics
in a standardized way.

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

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from simplebench.metrics import MetricCategory, MetricType, MetricTypes

else:
    MetricCategory = None  # pylint: disable=invalid-name
    MetricType = None  # pylint: disable=invalid-name
    MetricTypes = None  # pylint: disable=invalid-name

__all__: list[str] = []


_CACHED_METRIC_TYPES = None


def metric_types() -> 'MetricTypes':
    """The standard metric types provided by SimpleBench.

    :return MetricTypes: A collection of standard metric types

    Standard metric types defined by the SimpleBench library.

    - `STD_OPS_STATS`: Operations per second metric statistics.
    - `STD_OPS_RAW`: Raw list of operations per second data.
    - `STD_TIMING_STATS`: Time per measurement metric statistics.
    - `STD_TIMING_RAW`: Raw list of time per measurement data.
    - `STD_MEMORY_STATS`: Memory usage metric statistics.
    - `STD_MEMORY_RAW`: Raw list of memory usage data.
    - `STD_PEAK_MEMORY_STATS`: Peak memory usage metric statistics.
    - `STD_PEAK_MEMORY_RAW`: Raw list of peak memory usage data metric.
    - `STD_TOTAL_ELAPSED_TIME`: Total elapsed time for the benchmark.
    - `STD_TOTAL_CPU_TIME`: Total CPU time for the benchmark.
    - `STD_CPU_TIME_STATS`: CPU time per measurement metric statistics.
    - `STD_CPU_TIME_RAW`: Raw list of CPU time per measurement data.
    - `STD_GC_GEN0_COLLECTIONS_STATS`: Number of garbage collections for generation 0
    - `STD_GC_GEN0_COLLECTIONS_RAW`: Number of garbage collections for generation 0 (raw values)
    - `STD_GC_GEN1_COLLECTIONS_STATS`: Number of garbage collections for generation 1
    - `STD_GC_GEN1_COLLECTIONS_RAW`: Number of garbage collections for generation 1 (raw values)
    - `STD_GC_GEN2_COLLECTIONS_STATS`: Number of garbage collections for generation 2
    - `STD_GC_GEN2_COLLECTIONS_RAW`: Number of garbage collections for generation 2 (raw values)
    - `STD_GC_GEN0_COLLECTED_STATS`: Number of objects collected by garbage collection for generation 0
    - `STD_GC_GEN0_COLLECTED_RAW`: Number of objects collected by garbage collection for generation 0 (raw values)
    - `STD_GC_GEN1_COLLECTED_STATS`: Number of objects collected by garbage collection for generation 1
    - `STD_GC_GEN1_COLLECTED_RAW`: Number of objects collected by garbage collection for generation 1 (raw values)
    - `STD_GC_GEN2_COLLECTED_STATS`: Number of objects collected by garbage collection for generation 2
    - `STD_GC_GEN2_COLLECTED_RAW`: Number of objects collected by garbage collection for generation 2 (raw values)
    - `STD_GC_GEN0_UNCOLLECTABLE_STATS`: Number of uncollectable objects for generation 0
    - `STD_GC_GEN0_UNCOLLECTABLE_RAW`: Number of uncollectable objects for generation 0 (raw values)
    - `STD_GC_GEN1_UNCOLLECTABLE_STATS`: Number of uncollectable objects for generation 1
    - `STD_GC_GEN1_UNCOLLECTABLE_RAW`: Number of uncollectable objects for generation 1 (raw values)
    - `STD_GC_GEN2_UNCOLLECTABLE_STATS`: Number of uncollectable objects for generation 2
    - `STD_GC_GEN2_UNCOLLECTABLE_RAW`: Number of uncollectable objects for generation 2 (raw values)
    """
    global _CACHED_METRIC_TYPES, MetricCategory, MetricType, MetricTypes  # pylint: disable=global-statement
    if _CACHED_METRIC_TYPES is not None:
        return _CACHED_METRIC_TYPES

    from simplebench.metrics.metric_category import MetricCategory  # pylint: disable=import-outside-toplevel
    from simplebench.metrics.metric_type import MetricType  # pylint: disable=import-outside-toplevel
    from simplebench.metrics.metric_types import MetricTypes  # pylint: disable=import-outside-toplevel

    _CACHED_METRIC_TYPES = MetricTypes(
        [
            MetricType(
                category=MetricCategory.STATISTICAL,
                semantic_type='simplebench_std::operations_per_second_stats',
                label='STD_OPS_STATS',
                unit='ops/s',
                description='Operations per second metric statistics',
                scale=1.0,
            ),
            MetricType(
                category=MetricCategory.RAW,
                semantic_type='simplebench_std::operations_per_second_raw',
                label='STD_OPS_RAW',
                unit='ops/s',
                description='Raw list of operations per second data',
                scale=1.0,
            ),
            MetricType(
                category=MetricCategory.STATISTICAL,
                semantic_type='simplebench_std::time_per_operation_stats',
                label='STD_TIMING_STATS',
                unit='s',
                description='Time per measurement metric statistics',
                scale=1.0,
            ),
            MetricType(
                category=MetricCategory.RAW,
                semantic_type='simplebench_std::time_per_operation_raw',
                label='STD_TIMING_RAW',
                unit='s',
                description='Raw list of time per measurement data',
                scale=1.0,
            ),
            MetricType(
                category=MetricCategory.STATISTICAL,
                semantic_type='simplebench_std::memory_stats',
                label='STD_MEMORY_STATS',
                unit='bytes',
                description='Memory usage statistics',
                scale=1.0,
            ),
            MetricType(
                category=MetricCategory.RAW,
                semantic_type='simplebench_std::memory_raw',
                label='STD_MEMORY_RAW',
                unit='bytes',
                description='Raw list of memory usage data',
                scale=1.0,
            ),
            MetricType(
                category=MetricCategory.STATISTICAL,
                semantic_type='simplebench_std::peak_memory_stats',
                label='STD_PEAK_MEMORY_STATS',
                unit='bytes',
                description='Peak memory usage statistics',
                scale=1.0,
            ),
            MetricType(
                category=MetricCategory.RAW,
                semantic_type='simplebench_std::peak_memory_raw',
                label='STD_PEAK_MEMORY_RAW',
                unit='bytes',
                description='Raw list of peak memory usage data',
                scale=1.0,
            ),
            MetricType(
                category=MetricCategory.CUMULATIVE,
                semantic_type='simplebench_std::total_elapsed_time',
                label='STD_TOTAL_ELAPSED_TIME',
                unit='s',
                description='Total elapsed time',
                scale=1.0,
            ),
            MetricType(
                category=MetricCategory.CUMULATIVE,
                semantic_type='simplebench_std::total_cpu_time',
                label='STD_TOTAL_CPU_TIME',
                unit='s',
                description='Total CPU time',
                scale=1.0,
            ),
            MetricType(
                category=MetricCategory.STATISTICAL,
                semantic_type='simplebench_std::cpu_time_stats',
                label='STD_CPU_TIME_STATS',
                unit='s',
                description='CPU time per measurement metric statistics',
                scale=1.0,
            ),
            MetricType(
                category=MetricCategory.RAW,
                semantic_type='simplebench_std::cpu_time_raw',
                label='STD_CPU_TIME_RAW',
                unit='s',
                description='Raw list of CPU time per measurement data',
                scale=1.0,
            ),
            MetricType(
                category=MetricCategory.STATISTICAL,
                semantic_type='simplebench_std::gc_gen0_collections_stats',
                label='STD_GC_GEN0_COLLECTIONS_STATS',
                unit='collections',
                description='Generation 0 garbage collections statistics',
                scale=1.0,
            ),
            MetricType(
                category=MetricCategory.RAW,
                semantic_type='simplebench_std::gc_gen0_collections_raw',
                label='STD_GC_GEN0_COLLECTIONS_RAW',
                unit='collections',
                description='Raw list of Generation 0 garbage collections data',
                scale=1.0,
            ),
            MetricType(
                category=MetricCategory.STATISTICAL,
                semantic_type='simplebench_std::gc_gen1_collections_stats',
                label='STD_GC_GEN1_COLLECTIONS_STATS',
                unit='collections',
                description='Generation 1 garbage collections statistics',
                scale=1.0,
            ),
            MetricType(
                category=MetricCategory.RAW,
                semantic_type='simplebench_std::gc_gen1_collections_raw',
                label='STD_GC_GEN1_COLLECTIONS_RAW',
                unit='collections',
                description='Raw list of Generation 1 garbage collections data',
                scale=1.0,
            ),
            MetricType(
                category=MetricCategory.STATISTICAL,
                semantic_type='simplebench_std::gc_gen2_collections_stats',
                label='STD_GC_GEN2_COLLECTIONS_STATS',
                unit='collections',
                description='Generation 2 garbage collections statistics',
                scale=1.0,
            ),
            MetricType(
                category=MetricCategory.RAW,
                semantic_type='simplebench_std::gc_gen2_collections_raw',
                label='STD_GC_GEN2_COLLECTIONS_RAW',
                unit='collections',
                description='Raw list of Generation 2 garbage collections data',
                scale=1.0,
            ),
            MetricType(
                category=MetricCategory.STATISTICAL,
                semantic_type='simplebench_std::gc_gen0_collected_stats',
                label='STD_GC_GEN0_COLLECTED_STATS',
                unit='objects',
                description='Generation 0 garbage collected objects statistics',
                scale=1.0,
            ),
            MetricType(
                category=MetricCategory.RAW,
                semantic_type='simplebench_std::gc_gen0_collected_raw',
                label='STD_GC_GEN0_COLLECTED_RAW',
                unit='objects',
                description='Raw list of Generation 0 garbage collected objects data',
                scale=1.0,
            ),
            MetricType(
                category=MetricCategory.STATISTICAL,
                semantic_type='simplebench_std::gc_gen1_collected_stats',
                label='STD_GC_GEN1_COLLECTED_STATS',
                unit='objects',
                description='Generation 1 garbage collected objects statistics',
                scale=1.0,
            ),
            MetricType(
                category=MetricCategory.RAW,
                semantic_type='simplebench_std::gc_gen1_collected_raw',
                label='STD_GC_GEN1_COLLECTED_RAW',
                unit='objects',
                description='Raw list of Generation 1 garbage collected objects data',
                scale=1.0,
            ),
            MetricType(
                category=MetricCategory.STATISTICAL,
                semantic_type='simplebench_std::gc_gen2_collected_stats',
                label='STD_GC_GEN2_COLLECTED_STATS',
                unit='objects',
                description='Generation 2 garbage collected objects statistics',
                scale=1.0,
            ),
            MetricType(
                category=MetricCategory.RAW,
                semantic_type='simplebench_std::gc_gen2_collected_raw',
                label='STD_GC_GEN2_COLLECTED_RAW',
                unit='objects',
                description='Raw list of Generation 2 garbage collected objects data',
                scale=1.0,
            ),
            MetricType(
                category=MetricCategory.STATISTICAL,
                semantic_type='simplebench_std::gc_gen0_uncollectable_stats',
                label='STD_GC_GEN0_UNCOLLECTABLE_STATS',
                unit='objects',
                description='Generation 0 uncollectable objects statistics',
                scale=1.0,
            ),
            MetricType(
                category=MetricCategory.RAW,
                semantic_type='simplebench_std::gc_gen0_uncollectable_raw',
                label='STD_GC_GEN0_UNCOLLECTABLE_RAW',
                unit='objects',
                description='Raw list of Generation 0 uncollectable objects data',
                scale=1.0,
            ),
            MetricType(
                category=MetricCategory.STATISTICAL,
                semantic_type='simplebench_std::gc_gen1_uncollectable_stats',
                label='STD_GC_GEN1_UNCOLLECTABLE_STATS',
                unit='objects',
                description='Generation 1 uncollectable objects statistics',
                scale=1.0,
            ),
            MetricType(
                category=MetricCategory.RAW,
                semantic_type='simplebench_std::gc_gen1_uncollectable_raw',
                label='STD_GC_GEN1_UNCOLLECTABLE_RAW',
                unit='objects',
                description='Raw list of Generation 1 uncollectable objects data',
                scale=1.0,
            ),
            MetricType(
                category=MetricCategory.STATISTICAL,
                semantic_type='simplebench_std::gc_gen2_uncollectable_stats',
                label='STD_GC_GEN2_UNCOLLECTABLE_STATS',
                unit='objects',
                description='Generation 2 uncollectable objects statistics',
                scale=1.0,
            ),
            MetricType(
                category=MetricCategory.RAW,
                semantic_type='simplebench_std::gc_gen2_uncollectable_raw',
                label='STD_GC_GEN2_UNCOLLECTABLE_RAW',
                unit='objects',
                description='Raw list of Generation 2 uncollectable objects data',
                scale=1.0,
            ),
        ]
    )
    return _CACHED_METRIC_TYPES
