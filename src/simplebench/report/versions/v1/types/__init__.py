"""Miscellaneous type definitions for V1 report version.

This module defines TypedDicts for various components of the V1 report
data structure, including CPUInfo, ExecutionEnvironment, MachineInfo,
MemoryInfo, MetricsObject, PythonInfo, Report, ResultsInfo, SystemInfo,
and ValueBlock.

These types ensure proper validation and serialization of report data
across different components and facilitate conversion to/from dictionary
representations.
"""

from .cpu_info_dict import CPUInfoData, CPUInfoDict, ImmutableCPUInfoData, ImmutableCPUInfoDict
from .execution_environment_dict import ExecutionEnvironmentData, ExecutionEnvironmentDict
from .machine_info_dict import MachineInfoData, MachineInfoDict
from .memory_info_dict import MemoryInfoData, MemoryInfoDict
from .metrics_object_dict import MetricDataTypes, MetricDictTypes, MetricsObjectData, MetricsObjectDict
from .python_info_dict import ImmutablePythonInfoDict, PythonInfoData, PythonInfoDict
from .raw_data_block_dict import RawDataBlockData, RawDataBlockDict
from .report_dict import ReportData, ReportDict
from .results_info_dict import ResultsInfoData, ResultsInfoDict
from .system_info_dict import SystemInfoData, SystemInfoDict
from .value_block_dict import ValueBlockData, ValueBlockDict

__all__ = [
    'CPUInfoData',
    'CPUInfoDict',
    "ImmutableCPUInfoData",
    'ImmutableCPUInfoDict',
    'ExecutionEnvironmentData',
    'ExecutionEnvironmentDict',
    'MachineInfoData',
    'MachineInfoDict',
    'MemoryInfoData',
    'MemoryInfoDict',
    'MetricsObjectData',
    'MetricsObjectDict',
    'MetricDataTypes',
    'MetricDictTypes',
    'PythonInfoData',
    'PythonInfoDict',
    'ImmutablePythonInfoDict',
    'RawDataBlockData',
    'RawDataBlockDict',
    'ReportData',
    'ReportDict',
    'ResultsInfoData',
    'ResultsInfoDict',
    'SystemInfoData',
    'SystemInfoDict',
    'ValueBlockData',
    'ValueBlockDict',
]
