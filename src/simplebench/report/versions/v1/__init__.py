"""V1 json report classes

This module exports all V1 report related classes including the main
report structure and all associated data blocks, such as CPUInfo, MemoryInfo,
MachineInfo, PythonInfo, SystemInfo, VCSInfo, StatsBlock, ValueBlock,
ExecutionEnvironment, and ResultsInfo as well as their corresponding schemas
for serialization and deserialization.

In essence, this module serves as the central access point for all V1 report
components, facilitating easy import and usage throughout the SimpleBench
codebase and the public API for report generation, processing, and import/export
of V1 report data.
"""
# ruff: noqa: F401

from .cpu_info import CPUInfo, CPUInfoData, CPUInfoDict, CPUInfoSchema, ImmutableCPUInfoData, ImmutableCPUInfoDict
from .environment_info import (
    EnvironmentInfo,
    EnvironmentInfoData,
    EnvironmentInfoDict,
    EnvironmentInfoSchema,
    ImmutableEnvironmentInfoData,
    ImmutableEnvironmentInfoDict,
)
from .extras_object import ExtrasObject
from .machine_info import (
    ImmutableMachineInfoData,
    ImmutableMachineInfoDict,
    MachineInfo,
    MachineInfoData,
    MachineInfoDict,
    MachineInfoSchema,
)
from .memory_info import (
    ImmutableMemoryInfoData,
    ImmutableMemoryInfoDict,
    ImmutableSwapMemoryObjectDict,
    ImmutableVirtualMemoryObjectDict,
    MemoryInfo,
    MemoryInfoData,
    MemoryInfoDict,
    MemoryInfoSchema,
    SwapMemoryObject,
    SwapMemoryObjectDict,
    VirtualMemoryObject,
    VirtualMemoryObjectDict,
)
from .metric_type import (
    AllowedCategoryValues,
    ImmutableMetricTypeData,
    ImmutableMetricTypeDict,
    MetricType,
    MetricTypeData,
    MetricTypeDict,
    MetricTypeSchema,
)
from .metrics_object import (
    METRIC_ITEM_TYPES,
    ImmutableMetricDataTypes,
    ImmutableMetricDictTypes,
    ImmutableMetricsObjectData,
    ImmutableMetricsObjectDict,
    MetricDataTypes,
    MetricDictTypes,
    MetricItem,
    MetricsObject,
    MetricsObjectData,
    MetricsObjectDict,
)
from .python_info import (
    ImmutablePythonInfoData,
    ImmutablePythonInfoDict,
    ImmutablePythonInfoEnv,
    PythonInfo,
    PythonInfoData,
    PythonInfoDict,
    PythonInfoEnv,
    PythonInfoSchema,
)
from .raw_data_block import (
    ImmutableRawDataBlockData,
    ImmutableRawDataBlockDict,
    RawDataBlock,
    RawDataBlockData,
    RawDataBlockDict,
    RawDataBlockSchema,
)
from .report import ImmutableReportData, ImmutableReportDict, Report, ReportData, ReportDict, ReportSchema
from .results_info import (
    ImmutableResultsInfoData,
    ImmutableResultsInfoDict,
    ResultsInfo,
    ResultsInfoData,
    ResultsInfoDict,
    ResultsInfoSchema,
)
from .stats_block import (
    ImmutableStatsBlockData,
    ImmutableStatsBlockDict,
    StatsBlock,
    StatsBlockData,
    StatsBlockDict,
    StatsBlockSchema,
)
from .system_info import (
    ImmutableSystemInfoData,
    ImmutableSystemInfoDict,
    SystemInfo,
    SystemInfoData,
    SystemInfoDict,
    SystemInfoSchema,
)
from .value_block import (
    ImmutableValueBlockData,
    ImmutableValueBlockDict,
    ValueBlock,
    ValueBlockData,
    ValueBlockDict,
    ValueBlockSchema,
)
from .vcs_info import ImmutableVCSInfoData, ImmutableVCSInfoDict, VCSInfo, VCSInfoData, VCSInfoDict, VCSInfoSchema

__all__: list[str] = []
