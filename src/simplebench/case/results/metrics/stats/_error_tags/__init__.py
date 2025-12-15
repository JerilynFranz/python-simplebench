"""ErrorTags for the simplebench.stats package."""

from .memory_usage import _MemoryUsageErrorTag
from .operation_timings import _OperationTimingsErrorTag
from .operations_per_interval import _OperationsPerIntervalErrorTag
from .peak_memory_usage import _PeakMemoryUsageErrorTag
from .stats import _StatsErrorTag, _StatsSummaryErrorTag

__all__ = [
    "_StatsErrorTag",
    "_StatsSummaryErrorTag",
    "_MemoryUsageErrorTag",
    "_OperationTimingsErrorTag",
    "_OperationsPerIntervalErrorTag",
    "_PeakMemoryUsageErrorTag",
]
