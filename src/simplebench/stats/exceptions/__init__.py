"""ErrorTags for the simplebench.stats package."""

from .stats import StatsErrorTag, StatsSummaryErrorTag
from .memory_usage import MemoryUsageErrorTag
from .operation_timings import OperationTimingsErrorTag
from .operations_per_interval import OperationsPerIntervalErrorTag
from .peak_memory_usage import PeakMemoryUsageErrorTag

__all__ = [
    "StatsErrorTag",
    "StatsSummaryErrorTag",
    "MemoryUsageErrorTag",
    "OperationTimingsErrorTag",
    "OperationsPerIntervalErrorTag",
    "PeakMemoryUsageErrorTag",
]
