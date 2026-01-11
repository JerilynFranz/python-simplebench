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
from ._cpu_info import CPUInfo, CPUInfoData, CPUInfoDict, CPUInfoSchema, ImmutableCPUInfoData, ImmutableCPUInfoDict
from ._execution_environment import (
    ExecutionEnvironment,
    ExecutionEnvironmentData,
    ExecutionEnvironmentDict,
    ImmutableExecutionEnvironmentData,
    ImmutableExecutionEnvironmentDict,
)

from._generic_environment import GenericEnvironment, GenericEnvironmentSchema
from ._machine_info import (
    ImmutableMachineInfoData,
    ImmutableMachineInfoDict,
    MachineInfo,
    MachineInfoData,
    MachineInfoDict,
    MachineInfoSchema,
)
from ._memory_info import (
    ImmutableMemoryInfoData,
    ImmutableMemoryInfoDict,
    ImmutableSwapMemoryObjectDict,
    ImmutableVirtualMemoryObjectDict,
    MemoryInfo,
    MemoryInfoData,
    MemoryInfoDict,
    MemoryInfoSchema,
    SwapMemoryObjectDict,
    VirtualMemoryObjectDict,
)
from ._python_info import (
    ImmutablePythonInfoData,
    ImmutablePythonInfoDict,
    PythonInfo,
    PythonInfoData,
    PythonInfoDict,
    PythonInfoSchema,
)
from ._raw_data_block import (
    ImmutableRawDataBlockData,
    ImmutableRawDataBlockDict,
    RawDataBlock,
    RawDataBlockData,
    RawDataBlockDict,
    RawDataBlockSchema,
)
from ._stats_block import StatsBlock, StatsBlockSchema
from ._system_info import (
    ImmutableSystemInfoData,
    ImmutableSystemInfoDict,
    SystemInfo,
    SystemInfoData,
    SystemInfoDict,
    SystemInfoSchema,
)
from ._value_block import (
    ImmutableValueBlockData,
    ImmutableValueBlockDict,
    ValueBlock,
    ValueBlockData,
    ValueBlockDict,
    ValueBlockSchema,
)
from ._vcs_info import ImmutableVCSInfoData, ImmutableVCSInfoDict, VCSInfo, VCSInfoData, VCSInfoDict, VCSInfoSchema
from .metrics_object import MetricsObject
from .report import Report, ReportSchema
from .results_info import ResultsInfo, ResultsInfoSchema

__all__ = [
    "CPUInfo",
    "CPUInfoData",
    "CPUInfoDict",
    "CPUInfoSchema",
    "ImmutableCPUInfoData",
    "ImmutableCPUInfoDict",
    "ExecutionEnvironment",
    "ExecutionEnvironmentData",
    "ExecutionEnvironmentDict",
    "GenericEnvironment",
    "GenericEnvironmentSchema",
    "ImmutableExecutionEnvironmentData",
    "ImmutableExecutionEnvironmentDict",
    "MachineInfo",
    "MachineInfoData",
    "MachineInfoDict",
    "ImmutableMachineInfoData",
    "ImmutableMachineInfoDict",
    "MachineInfoSchema",
    "MemoryInfo",
    "MemoryInfoData",
    "MemoryInfoDict",
    "MemoryInfoSchema",
    "ImmutableMemoryInfoData",
    "ImmutableMemoryInfoDict",
    "ImmutableSwapMemoryObjectDict",
    "ImmutableVirtualMemoryObjectDict",
    "SwapMemoryObjectDict",
    "VirtualMemoryObjectDict",
    "MetricsObject",
    "PythonInfo",
    "PythonInfoData",
    "PythonInfoDict",
    "ImmutablePythonInfoData",
    "ImmutablePythonInfoDict",
    "PythonInfoSchema",
    "RawDataBlock",
    "RawDataBlockSchema",
    "RawDataBlockData",
    "RawDataBlockDict",
    "ImmutableRawDataBlockData",
    "ImmutableRawDataBlockDict",
    "Report",
    "ReportSchema",
    "ResultsInfo",
    "ResultsInfoSchema",
    "StatsBlock",
    "StatsBlockSchema",
    "SystemInfo",
    "SystemInfoData",
    "SystemInfoDict",
    "SystemInfoSchema",
    "ImmutableSystemInfoData",
    "ImmutableSystemInfoDict",
    "ValueBlock",
    "ValueBlockSchema",
    "ValueBlockData",
    "ValueBlockDict",
    "ImmutableValueBlockData",
    "ImmutableValueBlockDict",
    "VCSInfo",
    "VCSInfoSchema",
    "VCSInfoData",
    "VCSInfoDict",
    "ImmutableVCSInfoData",
    "ImmutableVCSInfoDict",
]
