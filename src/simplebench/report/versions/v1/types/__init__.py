"""Miscellaneous type definitions for V1 report version.

This module defines TypedDicts for various components of the V1 report
data structure, including CPUInfo, ExecutionEnvironment, MachineInfo,
MemoryInfo, MetricsObject, PythonInfo, Report, ResultsInfo, SystemInfo,
and ValueBlock.

These types ensure proper validation and serialization of report data
across different components and facilitate conversion to/from dictionary
representations.
"""

from ._cpu_info_dict import CPUInfoData, CPUInfoDict, ImmutableCPUInfoData, ImmutableCPUInfoDict
from ._memory_info_dict import (
    ImmutableMemoryInfoData,
    ImmutableMemoryInfoDict,
    ImmutableSwapMemoryObjectDict,
    ImmutableVirtualMemoryObjectDict,
    MemoryInfoData,
    MemoryInfoDict,
    SwapMemoryObjectDict,
    VirtualMemoryObjectDict,
)
from ._python_info_dict import ImmutablePythonInfoData, ImmutablePythonInfoDict, PythonInfoData, PythonInfoDict
from ._system_info_dict import ImmutableSystemInfoData, ImmutableSystemInfoDict, SystemInfoData, SystemInfoDict
from .execution_environment_dict import (
    ExecutionEnvironmentData,
    ExecutionEnvironmentDict,
    ImmutableExecutionEnvironmentData,
    ImmutableExecutionEnvironmentDict,
)
from .machine_info_dict import ImmutableMachineInfoData, ImmutableMachineInfoDict, MachineInfoData, MachineInfoDict
from .metrics_object_dict import MetricDataTypes, MetricDictTypes, MetricsObjectData, MetricsObjectDict
from .raw_data_block_dict import RawDataBlockData, RawDataBlockDict
from .report_dict import ReportData, ReportDict
from .results_info_dict import ResultsInfoData, ResultsInfoDict
from .value_block_dict import ValueBlockData, ValueBlockDict

__all__ = [
    'CPUInfoData',
    'CPUInfoDict',
    "ImmutableCPUInfoData",
    'ImmutableCPUInfoDict',
    'ExecutionEnvironmentData',
    'ExecutionEnvironmentDict',
    'ImmutableExecutionEnvironmentData',
    'ImmutableExecutionEnvironmentDict',
    'MachineInfoData',
    'MachineInfoDict',
    'ImmutableMachineInfoData',
    'ImmutableMachineInfoDict',
    'MemoryInfoData',
    'MemoryInfoDict',
    'SwapMemoryObjectDict',
    'ImmutableSwapMemoryObjectDict',
    'VirtualMemoryObjectDict',
    'ImmutableVirtualMemoryObjectDict',
    'ImmutableMemoryInfoData',
    'ImmutableMemoryInfoDict',
    'MetricsObjectData',
    'MetricsObjectDict',
    'MetricDataTypes',
    'MetricDictTypes',
    'PythonInfoData',
    'PythonInfoDict',
    'ImmutablePythonInfoData',
    'ImmutablePythonInfoDict',
    'RawDataBlockData',
    'RawDataBlockDict',
    'ReportData',
    'ReportDict',
    'ResultsInfoData',
    'ResultsInfoDict',
    'SystemInfoData',
    'ImmutableSystemInfoData',
    'SystemInfoDict',
    'ImmutableSystemInfoDict',
    'ValueBlockData',
    'ValueBlockDict',
]
