"""Tests for report.v1 package for SimpleBench tests."""
# ruff: noqa: F401

from .cpu_info import CPUInfoKWArgs
from .environment import EnvironmentKWArgs
from .memory_info import MemoryInfoKWArgs, SwapMemoryObjectKWArgs, VirtualMemoryObjectKWArgs
from .python_info import PythonInfoKWArgs
from .raw_data_block import RawDataBlockKWArgs
from .stats_block import StatsBlockKWArgs
from .system_info import SystemInfoKWArgs
from .value_block import ValueBlockKWArgs
from .vcs_info import VCSInfoKWArgs

__all__: list[str] = [
    'CPUInfoKWArgs',
    'EnvironmentKWArgs',
    'MemoryInfoKWArgs',
    'SwapMemoryObjectKWArgs',
    'VirtualMemoryObjectKWArgs',
    'PythonInfoKWArgs',
    'RawDataBlockKWArgs',
    'StatsBlockKWArgs',
    'SystemInfoKWArgs',
    'ValueBlockKWArgs',
    'VCSInfoKWArgs',
]
