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
from typing import Final

from simplebench.metric.metric import Metric
from simplebench.metric.metric_types_registry import metric_types_registry
from simplebench.metric.metrics import Metrics

STD_OPS_STATS: Final[Metric] = Metric(
    label='STD_OPS_STATS',
    title="Ops",
    description='Operations per second statistics',
    metric_type=metric_types_registry['STD_OPS_STATS'])
"""Operations per second metric.

The operations per second is the average number of operations performed per second.
This is the inverse of STD_TIMING_STATS."""

STD_OPS_RAW: Final[Metric] = Metric(
    label='STD_OPS_RAW',
    title="Ops Raw",
    description='Operations per second raw values',
    metric_type=metric_types_registry['STD_OPS_RAW'])
"""Operations per second raw values metric."""

STD_TIMING_STATS: Final[Metric] = Metric(
    label='STD_TIMING_STATS',
    title="Timing",
    description='Time per measurement statistics',
    metric_type=metric_types_registry['STD_TIMING_STATS'])
"""Time per measurement metric.

This is the inverse of STD_OPS_STATS and has the technical unit of 's/ops', but is usually
referred to as 's' for simplicity and common usage.

The time per measurement is the average of the per-round execution times for an iteration
(an iteration is considered a single measurement but may consist of multiple rounds).
"""

STD_TIMING_RAW: Final[Metric] = Metric(
    label='STD_TIMING_RAW',
    title="Timing Raw",
    description='Time per measurement raw values',
    metric_type=metric_types_registry['STD_TIMING_RAW'])
"""Time per measurement raw values metric."""

STD_MEMORY_STATS: Final[Metric] = Metric(
    label='STD_MEMORY_STATS',
    title="Memory",
    description='Memory usage statistics',
    metric_type=metric_types_registry['STD_MEMORY_STATS'])
"""Memory usage metric."""

STD_MEMORY_RAW: Final[Metric] = Metric(
    label='STD_MEMORY_RAW',
    title="Memory Raw",
    description='Memory usage raw values',
    metric_type=metric_types_registry['STD_MEMORY_RAW'])
"""Memory usage raw values metric."""

STD_PEAK_MEMORY_STATS: Final[Metric] = Metric(
    label='STD_PEAK_MEMORY_STATS',
    title="Peak Memory",
    description='Peak memory usage statistics',
    metric_type=metric_types_registry['STD_PEAK_MEMORY_STATS'])
"""Peak memory usage metric."""

STD_PEAK_MEMORY_RAW: Final[Metric] = Metric(
    label='STD_PEAK_MEMORY_RAW',
    title="Peak Memory Raw",
    description='Peak memory usage raw values',
    metric_type=metric_types_registry['STD_PEAK_MEMORY_RAW'])
"""Peak memory usage raw values metric."""

STD_TOTAL_ELAPSED_TIME: Final[Metric] = Metric(
    label='STD_TOTAL_ELAPSED_TIME',
    title="Total Elapsed Time",
    description='Total elapsed time',
    metric_type=metric_types_registry['STD_TOTAL_ELAPSED_TIME'])
"""Total elapsed time metric."""

STD_TOTAL_CPU_TIME: Final[Metric] = Metric(
    label='STD_TOTAL_CPU_TIME',
    title="Total CPU Time",
    description='Total CPU time',
    metric_type=metric_types_registry['STD_TOTAL_CPU_TIME'])
"""Total CPU time metric."""

STD_CPU_TIME_STATS: Final[Metric] = Metric(
    label='STD_CPU_TIME_STATS',
    title="CPU Time",
    description='CPU time per measurement statistics',
    metric_type=metric_types_registry['STD_CPU_TIME_STATS'])
"""CPU time per measurement metric."""

STD_CPU_TIME_RAW: Final[Metric] = Metric(
    label='STD_CPU_TIME_RAW',
    title="CPU Time Raw",
    description='CPU time per measurement raw values',
    metric_type=metric_types_registry['STD_CPU_TIME_RAW'])
"""CPU time per measurement raw values metric."""

STD_GC_GEN0_COLLECTIONS_STATS: Final[Metric] = Metric(
    label='STD_GC_GEN0_COLLECTIONS_STATS',
    title="GC Gen0 Collections",
    description='Generation 0 garbage collections statistics',
    metric_type=metric_types_registry['STD_GC_GEN0_COLLECTIONS_STATS'])
"""Generation 0 garbage collections metric."""

STD_GC_GEN0_COLLECTIONS_RAW: Final[Metric] = Metric(
    label='STD_GC_GEN0_COLLECTIONS_RAW',
    title="GC Gen0 Collections Raw",
    description='Generation 0 garbage collections raw values',
    metric_type=metric_types_registry['STD_GC_GEN0_COLLECTIONS_RAW'])
"""Generation 0 garbage collections raw values metric."""

STD_GC_GEN1_COLLECTIONS_STATS: Final[Metric] = Metric(
    label='STD_GC_GEN1_COLLECTIONS_STATS',
    title="GC Gen1 Collections",
    description='Generation 1 garbage collections statistics',
    metric_type=metric_types_registry['STD_GC_GEN1_COLLECTIONS_STATS'])
"""Generation 1 garbage collections metric."""

STD_GC_GEN1_COLLECTIONS_RAW: Final[Metric] = Metric(
    label='STD_GC_GEN1_COLLECTIONS_RAW',
    title="GC Gen1 Collections Raw",
    description='Generation 1 garbage collections raw values',
    metric_type=metric_types_registry['STD_GC_GEN1_COLLECTIONS_RAW'])
"""Generation 1 garbage collections raw values metric."""

STD_GC_GEN2_COLLECTIONS_STATS: Final[Metric] = Metric(
    label='STD_GC_GEN2_COLLECTIONS_STATS',
    title="GC Gen2 Collections",
    description='Generation 2 garbage collections statistics',
    metric_type=metric_types_registry['STD_GC_GEN2_COLLECTIONS_STATS'])
"""Generation 2 garbage collections metric."""

STD_GC_GEN2_COLLECTIONS_RAW: Final[Metric] = Metric(
    label='STD_GC_GEN2_COLLECTIONS_RAW',
    title="GC Gen2 Collections Raw",
    description='Generation 2 garbage collections raw values',
    metric_type=metric_types_registry['STD_GC_GEN2_COLLECTIONS_RAW'])
"""Generation 2 garbage collections raw values metric."""

STD_GC_GEN0_COLLECTED_STATS: Final[Metric] = Metric(
    label='STD_GC_GEN0_COLLECTED_STATS',
    title="GC Gen0 Collected",
    description='Generation 0 garbage collected objects statistics',
    metric_type=metric_types_registry['STD_GC_GEN0_COLLECTED_STATS'])
"""Generation 0 garbage collected objects metric."""

STD_GC_GEN0_COLLECTED_RAW: Final[Metric] = Metric(
    label='STD_GC_GEN0_COLLECTED_RAW',
    title="GC Gen0 Collected Raw",
    description='Generation 0 garbage collected objects raw values',
    metric_type=metric_types_registry['STD_GC_GEN0_COLLECTED_RAW'])
"""Generation 0 garbage collected objects raw values metric."""

STD_GC_GEN1_COLLECTED_STATS: Final[Metric] = Metric(
    label='STD_GC_GEN1_COLLECTED_STATS',
    title="GC Gen1 Collected",
    description='Generation 1 garbage collected objects statistics',
    metric_type=metric_types_registry['STD_GC_GEN1_COLLECTED_STATS'])
"""Generation 1 garbage collected objects metric."""

STD_GC_GEN1_COLLECTED_RAW: Final[Metric] = Metric(
    label='STD_GC_GEN1_COLLECTED_RAW',
    title="GC Gen1 Collected Raw",
    description='Generation 1 garbage collected objects raw values',
    metric_type=metric_types_registry['STD_GC_GEN1_COLLECTED_RAW'])
"""Generation 1 garbage collected objects raw values metric."""

STD_GC_GEN2_COLLECTED_STATS: Final[Metric] = Metric(
    label='STD_GC_GEN2_COLLECTED_STATS',
    title="GC Gen2 Collected",
    description='Generation 2 garbage collected objects statistics',
    metric_type=metric_types_registry['STD_GC_GEN2_COLLECTED_STATS'])
"""Generation 2 garbage collected objects metric."""

STD_GC_GEN2_COLLECTED_RAW: Final[Metric] = Metric(
    label='STD_GC_GEN2_COLLECTED_RAW',
    title="GC Gen2 Collected Raw",
    description='Generation 2 garbage collected objects raw values',
    metric_type=metric_types_registry['STD_GC_GEN2_COLLECTED_RAW'])
"""Generation 2 garbage collected objects raw values metric."""

STD_GC_GEN0_UNCOLLECTABLE_STATS: Final[Metric] = Metric(
    label='STD_GC_GEN0_UNCOLLECTABLE_STATS',
    title="GC Gen0 Uncollectable",
    description='Generation 0 uncollectable objects statistics',
    metric_type=metric_types_registry['STD_GC_GEN0_UNCOLLECTABLE_STATS'])
"""Generation 0 uncollectable objects metric."""

STD_GC_GEN0_UNCOLLECTABLE_RAW: Final[Metric] = Metric(
    label='STD_GC_GEN0_UNCOLLECTABLE_RAW',
    title="GC Gen0 Uncollectable Raw",
    description='Generation 0 uncollectable objects raw values',
    metric_type=metric_types_registry['STD_GC_GEN0_UNCOLLECTABLE_RAW'])
"""Generation 0 uncollectable objects raw values metric."""

STD_GC_GEN1_UNCOLLECTABLE_STATS: Final[Metric] = Metric(
    label='STD_GC_GEN1_UNCOLLECTABLE_STATS',
    title="GC Gen1 Uncollectable",
    description='Generation 1 uncollectable objects statistics',
    metric_type=metric_types_registry['STD_GC_GEN1_UNCOLLECTABLE_STATS'])
"""Generation 1 uncollectable objects metric."""

STD_GC_GEN1_UNCOLLECTABLE_RAW: Final[Metric] = Metric(
    label='STD_GC_GEN1_UNCOLLECTABLE_RAW',
    title="GC Gen1 Uncollectable Raw",
    description='Generation 1 uncollectable objects raw values',
    metric_type=metric_types_registry['STD_GC_GEN1_UNCOLLECTABLE_RAW'])
"""Generation 1 uncollectable objects raw values metric."""

STD_GC_GEN2_UNCOLLECTABLE_STATS: Final[Metric] = Metric(
    label='STD_GC_GEN2_UNCOLLECTABLE_STATS',
    title="GC Gen2 Uncollectable",
    description='Generation 2 uncollectable objects statistics',
    metric_type=metric_types_registry['STD_GC_GEN2_UNCOLLECTABLE_STATS'])
"""Generation 2 uncollectable objects metric."""

STD_GC_GEN2_UNCOLLECTABLE_RAW: Final[Metric] = Metric(
    label='STD_GC_GEN2_UNCOLLECTABLE_RAW',
    title="GC Gen2 Uncollectable Raw",
    description='Generation 2 uncollectable objects raw values',
    metric_type=metric_types_registry['STD_GC_GEN2_UNCOLLECTABLE_RAW'])
"""Generation 2 uncollectable objects raw values metric."""

metrics: Final[Metrics] = Metrics([  # pylint: disable=invalid-name
    STD_OPS_STATS,
    STD_OPS_RAW,
    STD_TIMING_STATS,
    STD_TIMING_RAW,
    STD_MEMORY_STATS,
    STD_MEMORY_RAW,
    STD_PEAK_MEMORY_STATS,
    STD_PEAK_MEMORY_RAW,
    STD_TOTAL_ELAPSED_TIME,
    STD_TOTAL_CPU_TIME,
    STD_CPU_TIME_STATS,
    STD_CPU_TIME_RAW,
    STD_GC_GEN0_COLLECTIONS_STATS,
    STD_GC_GEN0_COLLECTIONS_RAW,
    STD_GC_GEN1_COLLECTIONS_STATS,
    STD_GC_GEN1_COLLECTIONS_RAW,
    STD_GC_GEN2_COLLECTIONS_STATS,
    STD_GC_GEN2_COLLECTIONS_RAW,
    STD_GC_GEN0_COLLECTED_STATS,
    STD_GC_GEN0_COLLECTED_RAW,
    STD_GC_GEN1_COLLECTED_STATS,
    STD_GC_GEN1_COLLECTED_RAW,
    STD_GC_GEN2_COLLECTED_STATS,
    STD_GC_GEN2_COLLECTED_RAW,
    STD_GC_GEN0_UNCOLLECTABLE_STATS,
    STD_GC_GEN0_UNCOLLECTABLE_RAW,
    STD_GC_GEN1_UNCOLLECTABLE_STATS,
    STD_GC_GEN1_UNCOLLECTABLE_RAW,
    STD_GC_GEN2_UNCOLLECTABLE_STATS,
    STD_GC_GEN2_UNCOLLECTABLE_RAW,
])
"""Standard metric types defined by the SimpleBench library.

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
