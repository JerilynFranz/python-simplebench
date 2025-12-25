"""Type definitions for CPU information data."""
from typing import TypeAlias

CPUInfoDataTypes: TypeAlias = str | int | float | bool | None | list['CPUInfoDataTypes'] | dict[str, 'CPUInfoDataTypes']
"""Type alias for the CPU information data types."""

CPUInfoDictType: TypeAlias = dict[str, CPUInfoDataTypes]
"""Type alias for the CPU information dictionary structure."""
