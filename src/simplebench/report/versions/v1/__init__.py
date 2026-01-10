"""V1 json report classes"""
from ._cpu_info import CPUInfo, CPUInfoSchema
from ._memory_info import MemoryInfo, MemoryInfoSchema
from ._python_info import PythonInfo, PythonInfoSchema
from ._system_info import SystemInfo, SystemInfoSchema
from .execution_environment import ExecutionEnvironment
from .machine_info import MachineInfo, MachineInfoSchema
from .metrics_object import MetricsObject
from .raw_data_block import RawDataBlock, RawDataBlockSchema
from .report import Report, ReportSchema
from .results_info import ResultsInfo, ResultsInfoSchema
from .stats_block import StatsBlock, StatsBlockSchema
from .types import (
    CPUInfoData,
    CPUInfoDict,
    ExecutionEnvironmentData,
    ExecutionEnvironmentDict,
    ImmutableCPUInfoData,
    ImmutableCPUInfoDict,
    ImmutableExecutionEnvironmentData,
    ImmutableExecutionEnvironmentDict,
    ImmutableMachineInfoData,
    ImmutableMachineInfoDict,
    ImmutableMemoryInfoData,
    ImmutableMemoryInfoDict,
    ImmutablePythonInfoData,
    ImmutablePythonInfoDict,
    ImmutableSwapMemoryObjectDict,
    ImmutableSystemInfoData,
    ImmutableSystemInfoDict,
    ImmutableVirtualMemoryObjectDict,
    MachineInfoData,
    MachineInfoDict,
    MemoryInfoData,
    MemoryInfoDict,
    PythonInfoData,
    PythonInfoDict,
    SwapMemoryObjectDict,
    SystemInfoData,
    SystemInfoDict,
    VirtualMemoryObjectDict,
)
from .value_block import ValueBlock, ValueBlockSchema
from .vcs_info import VCSInfo, VCSInfoSchema

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
    "VCSInfo",
    "VCSInfoSchema",
]
