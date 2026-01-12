"""Standard Metrics defined by SimpleRunner benchmark runner.

Types for metrics in reporters and benchmarks.

This is used by reporters to specify what the metrics of benchmark results are.

Defined Metrics are:

- `STD_OPS_STATS`: Operations per second statistics.
- `STD_OPS_RAW`: Operations per second raw values.
- `STD_TIMING_STATS`: Time per measurement statistics.
- `STD_TIMING_RAW`: Time per measurement raw values.
- `STD_MEMORY_STATS`: Memory usage statistics.
- `STD_MEMORY_RAW`: Memory usage raw values.
- `STD_PEAK_MEMORY_STATS`: Peak memory usage statistics.
- `STD_PEAK_MEMORY_RAW`: Peak memory usage raw values.
- `STD_TOTAL_ELAPSED_TIME`: Total elapsed time metric.
- `STD_TOTAL_CPU_TIME`: Total CPU time metric.
- `STD_CPU_TIME_STATS`: CPU time per measurement statistics.
- `STD_CPU_TIME_RAW`: CPU time per measurement raw values.
- `STD_GC_GEN0_COLLECTIONS_STATS`: Generation 0 garbage collections statistics.
- `STD_GC_GEN0_COLLECTIONS_RAW`: Generation 0 garbage collections raw values.
- `STD_GC_GEN1_COLLECTIONS_STATS`: Generation 1 garbage collections statistics.
- `STD_GC_GEN1_COLLECTIONS_RAW`: Generation 1 garbage collections raw values.
- `STD_GC_GEN2_COLLECTIONS_STATS`: Generation 2 garbage collections statistics.
- `STD_GC_GEN2_COLLECTIONS_RAW`: Generation 2 garbage collections raw values.
- `STD_GC_GEN0_COLLECTED_STATS`: Generation 0 garbage collected objects statistics.
- `STD_GC_GEN0_COLLECTED_RAW`: Generation 0 garbage collected objects raw values.
- `STD_GC_GEN1_COLLECTED_STATS`: Generation 1 garbage collected objects statistics.
- `STD_GC_GEN1_COLLECTED_RAW`: Generation 1 garbage collected objects raw values.
- `STD_GC_GEN2_COLLECTED_STATS`: Generation 2 garbage collected objects statistics.
- `STD_GC_GEN2_COLLECTED_RAW`: Generation 2 garbage collected objects raw values.
- `STD_GC_GEN0_UNCOLLECTABLE_STATS`: Generation 0 uncollectable objects statistics.
- `STD_GC_GEN0_UNCOLLECTABLE_RAW`: Generation 0 uncollectable objects raw values.
- `STD_GC_GEN1_UNCOLLECTABLE_STATS`: Generation 1 uncollectable objects statistics.
- `STD_GC_GEN1_UNCOLLECTABLE_RAW`: Generation 1 uncollectable objects raw values.
- `STD_GC_GEN2_UNCOLLECTABLE_STATS`: Generation 2 uncollectable objects statistics.
- `STD_GC_GEN2_UNCOLLECTABLE_RAW`: Generation 2 uncollectable objects raw values.

The 'STD_' prefix is used to indicate that the metric is a standard metric
defined by the SimpleBench library. Custom metrics should use a different prefix.
Ideally, custom metrics should use a prefix that is unique to the benchmark or
benchmark suite that defines them to avoid conflicts with other metrics.
"""

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from simplebench.metrics.metric import Metric
    from simplebench.metrics.metric_types_registry import metric_types_registry
    from simplebench.metrics.metrics import Metrics

else:
    Metric = None  # pylint: disable=invalid-name
    metric_types_registry = None  # pylint: disable=invalid-name
    Metrics = None  # pylint: disable=invalid-name

_CACHED_METRICS = None


def metrics() -> 'Metrics':
    """Standard Metrics definitions

    - `STD_OPS_STATS`: Operations per second statistics.
    - `STD_OPS_RAW`: Operations per second raw values.
    - `STD_TIMING_STATS`: Time per measurement statistics.
    - `STD_TIMING_RAW`: Time per measurement raw values.
    - `STD_MEMORY_STATS`: Memory usage statistics.
    - `STD_MEMORY_RAW`: Memory usage raw values.
    - `STD_PEAK_MEMORY_STATS`: Peak memory usage statistics.
    - `STD_PEAK_MEMORY_RAW`: Peak memory usage raw values.
    - `STD_TOTAL_ELAPSED_TIME`: Total elapsed time metric.
    - `STD_TOTAL_CPU_TIME`: Total CPU time metric.
    - `STD_CPU_TIME_STATS`: CPU time per measurement statistics.
    - `STD_CPU_TIME_RAW`: CPU time per measurement raw values.
    - `STD_GC_GEN0_COLLECTIONS_STATS`: Generation 0 garbage collections statistics.
    - `STD_GC_GEN0_COLLECTIONS_RAW`: Generation 0 garbage collections raw values.
    - `STD_GC_GEN1_COLLECTIONS_STATS`: Generation 1 garbage collections statistics.
    - `STD_GC_GEN1_COLLECTIONS_RAW`: Generation 1 garbage collections raw values.
    - `STD_GC_GEN2_COLLECTIONS_STATS`: Generation 2 garbage collections statistics.
    - `STD_GC_GEN2_COLLECTIONS_RAW`: Generation 2 garbage collections raw values.
    - `STD_GC_GEN0_COLLECTED_STATS`: Generation 0 garbage collected objects statistics.
    - `STD_GC_GEN0_COLLECTED_RAW`: Generation 0 garbage collected objects raw values.
    - `STD_GC_GEN1_COLLECTED_STATS`: Generation 1 garbage collected objects statistics.
    - `STD_GC_GEN1_COLLECTED_RAW`: Generation 1 garbage collected objects raw values.
    - `STD_GC_GEN2_COLLECTED_STATS`: Generation 2 garbage collected objects statistics.
    - `STD_GC_GEN2_COLLECTED_RAW`: Generation 2 garbage collected objects raw values.
    - `STD_GC_GEN0_UNCOLLECTABLE_STATS`: Generation 0 uncollectable objects statistics.
    - `STD_GC_GEN0_UNCOLLECTABLE_RAW`: Generation 0 uncollectable objects raw values.
    - `STD_GC_GEN1_UNCOLLECTABLE_STATS`: Generation 1 uncollectable objects statistics.
    - `STD_GC_GEN1_UNCOLLECTABLE_RAW`: Generation 1 uncollectable objects raw values.
    - `STD_GC_GEN2_UNCOLLECTABLE_STATS`: Generation 2 uncollectable objects statistics.
    - `STD_GC_GEN2_UNCOLLECTABLE_RAW`: Generation 2 uncollectable objects raw values.
    """
    global _CACHED_METRICS, Metric, metric_types_registry, Metrics  # pylint: disable=global-statement
    if _CACHED_METRICS is not None:
        return _CACHED_METRICS

    from simplebench.metrics.metric import Metric  # pylint: disable=import-outside-toplevel
    from simplebench.metrics.metric_types_registry import metric_types_registry  # pylint: disable=import-outside-toplevel
    from simplebench.metrics.metrics import Metrics  # pylint: disable=import-outside-toplevel

    _CACHED_METRICS = Metrics(
        [
            Metric(
                label='STD_OPS_STATS',
                title='Ops',
                description='Operations per second statistics',
                metric_type=metric_types_registry['STD_OPS_STATS'],
            ),
            Metric(
                label='STD_OPS_RAW',
                title='Ops Raw',
                description='Operations per second raw values',
                metric_type=metric_types_registry['STD_OPS_RAW'],
            ),
            Metric(
                label='STD_TIMING_STATS',
                title='Timing',
                description='Time per measurement statistics',
                metric_type=metric_types_registry['STD_TIMING_STATS'],
            ),
            Metric(
                label='STD_TIMING_RAW',
                title='Timing Raw',
                description='Time per measurement raw values',
                metric_type=metric_types_registry['STD_TIMING_RAW'],
            ),
            Metric(
                label='STD_MEMORY_STATS',
                title='Memory',
                description='Memory usage statistics',
                metric_type=metric_types_registry['STD_MEMORY_STATS'],
            ),
            Metric(
                label='STD_MEMORY_RAW',
                title='Memory Raw',
                description='Memory usage raw values',
                metric_type=metric_types_registry['STD_MEMORY_RAW'],
            ),
            Metric(
                label='STD_PEAK_MEMORY_STATS',
                title='Peak Memory',
                description='Peak memory usage statistics',
                metric_type=metric_types_registry['STD_PEAK_MEMORY_STATS'],
            ),
            Metric(
                label='STD_PEAK_MEMORY_RAW',
                title='Peak Memory Raw',
                description='Peak memory usage raw values',
                metric_type=metric_types_registry['STD_PEAK_MEMORY_RAW'],
            ),
            Metric(
                label='STD_TOTAL_ELAPSED_TIME',
                title='Total Elapsed Time',
                description='Total elapsed time',
                metric_type=metric_types_registry['STD_TOTAL_ELAPSED_TIME'],
            ),
            Metric(
                label='STD_TOTAL_CPU_TIME',
                title='Total CPU Time',
                description='Total CPU time',
                metric_type=metric_types_registry['STD_TOTAL_CPU_TIME'],
            ),
            Metric(
                label='STD_CPU_TIME_STATS',
                title='CPU Time',
                description='CPU time per measurement statistics',
                metric_type=metric_types_registry['STD_CPU_TIME_STATS'],
            ),
            Metric(
                label='STD_CPU_TIME_RAW',
                title='CPU Time Raw',
                description='CPU time per measurement raw values',
                metric_type=metric_types_registry['STD_CPU_TIME_RAW'],
            ),
            Metric(
                label='STD_GC_GEN0_COLLECTIONS_STATS',
                title='GC Gen0 Collections',
                description='Generation 0 garbage collections statistics',
                metric_type=metric_types_registry['STD_GC_GEN0_COLLECTIONS_STATS'],
            ),
            Metric(
                label='STD_GC_GEN0_COLLECTIONS_RAW',
                title='GC Gen0 Collections Raw',
                description='Generation 0 garbage collections raw values',
                metric_type=metric_types_registry['STD_GC_GEN0_COLLECTIONS_RAW'],
            ),
            Metric(
                label='STD_GC_GEN1_COLLECTIONS_STATS',
                title='GC Gen1 Collections',
                description='Generation 1 garbage collections statistics',
                metric_type=metric_types_registry['STD_GC_GEN1_COLLECTIONS_STATS'],
            ),
            Metric(
                label='STD_GC_GEN1_COLLECTIONS_RAW',
                title='GC Gen1 Collections Raw',
                description='Generation 1 garbage collections raw values',
                metric_type=metric_types_registry['STD_GC_GEN1_COLLECTIONS_RAW'],
            ),
            Metric(
                label='STD_GC_GEN2_COLLECTIONS_STATS',
                title='GC Gen2 Collections',
                description='Generation 2 garbage collections statistics',
                metric_type=metric_types_registry['STD_GC_GEN2_COLLECTIONS_STATS'],
            ),
            Metric(
                label='STD_GC_GEN2_COLLECTIONS_RAW',
                title='GC Gen2 Collections Raw',
                description='Generation 2 garbage collections raw values',
                metric_type=metric_types_registry['STD_GC_GEN2_COLLECTIONS_RAW'],
            ),
            Metric(
                label='STD_GC_GEN0_COLLECTED_STATS',
                title='GC Gen0 Collected',
                description='Generation 0 garbage collected objects statistics',
                metric_type=metric_types_registry['STD_GC_GEN0_COLLECTED_STATS'],
            ),
            Metric(
                label='STD_GC_GEN0_COLLECTED_RAW',
                title='GC Gen0 Collected Raw',
                description='Generation 0 garbage collected objects raw values',
                metric_type=metric_types_registry['STD_GC_GEN0_COLLECTED_RAW'],
            ),
            Metric(
                label='STD_GC_GEN1_COLLECTED_STATS',
                title='GC Gen1 Collected',
                description='Generation 1 garbage collected objects statistics',
                metric_type=metric_types_registry['STD_GC_GEN1_COLLECTED_STATS'],
            ),
            Metric(
                label='STD_GC_GEN1_COLLECTED_RAW',
                title='GC Gen1 Collected Raw',
                description='Generation 1 garbage collected objects raw values',
                metric_type=metric_types_registry['STD_GC_GEN1_COLLECTED_RAW'],
            ),
            Metric(
                label='STD_GC_GEN2_COLLECTED_STATS',
                title='GC Gen2 Collected',
                description='Generation 2 garbage collected objects statistics',
                metric_type=metric_types_registry['STD_GC_GEN2_COLLECTED_STATS'],
            ),
            Metric(
                label='STD_GC_GEN2_COLLECTED_RAW',
                title='GC Gen2 Collected Raw',
                description='Generation 2 garbage collected objects raw values',
                metric_type=metric_types_registry['STD_GC_GEN2_COLLECTED_RAW'],
            ),
            Metric(
                label='STD_GC_GEN0_UNCOLLECTABLE_STATS',
                title='GC Gen0 Uncollectable',
                description='Generation 0 uncollectable objects statistics',
                metric_type=metric_types_registry['STD_GC_GEN0_UNCOLLECTABLE_STATS'],
            ),
            Metric(
                label='STD_GC_GEN0_UNCOLLECTABLE_RAW',
                title='GC Gen0 Uncollectable Raw',
                description='Generation 0 uncollectable objects raw values',
                metric_type=metric_types_registry['STD_GC_GEN0_UNCOLLECTABLE_RAW'],
            ),
            Metric(
                label='STD_GC_GEN1_UNCOLLECTABLE_STATS',
                title='GC Gen1 Uncollectable',
                description='Generation 1 uncollectable objects statistics',
                metric_type=metric_types_registry['STD_GC_GEN1_UNCOLLECTABLE_STATS'],
            ),
            Metric(
                label='STD_GC_GEN1_UNCOLLECTABLE_RAW',
                title='GC Gen1 Uncollectable Raw',
                description='Generation 1 uncollectable objects raw values',
                metric_type=metric_types_registry['STD_GC_GEN1_UNCOLLECTABLE_RAW'],
            ),
            Metric(
                label='STD_GC_GEN2_UNCOLLECTABLE_STATS',
                title='GC Gen2 Uncollectable',
                description='Generation 2 uncollectable objects statistics',
                metric_type=metric_types_registry['STD_GC_GEN2_UNCOLLECTABLE_STATS'],
            ),
            Metric(
                label='STD_GC_GEN2_UNCOLLECTABLE_RAW',
                title='GC Gen2 Uncollectable Raw',
                description='Generation 2 uncollectable objects raw values',
                metric_type=metric_types_registry['STD_GC_GEN2_UNCOLLECTABLE_RAW'],
            ),
        ]
    )
    return _CACHED_METRICS
