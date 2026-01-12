"""CPUInfo version 1 module for JSON report representation."""

from ._cpu_info import CPUInfo
from ._cpu_info_schema import CPUInfoSchema
from ._typeddict_types import CPUInfoData, CPUInfoDict, ImmutableCPUInfoData, ImmutableCPUInfoDict

__all__ = ['CPUInfo', 'CPUInfoData', 'CPUInfoDict', 'CPUInfoSchema', 'ImmutableCPUInfoData', 'ImmutableCPUInfoDict']
