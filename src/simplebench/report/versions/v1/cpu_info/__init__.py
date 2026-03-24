"""CPUInfo version 1 module for JSON report representation."""
# ruff: noqa: F401

from .cpu_info import CPUInfo
from .cpu_info_schema import CPUInfoSchema
from .cpu_info_dict import CPUInfoData, CPUInfoDict, ImmutableCPUInfoData, ImmutableCPUInfoDict

__all__: list[str] = []
