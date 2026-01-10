"""MemoryInfo version 1 package."""
from ._memory_info import MemoryInfo
from ._memory_info_schema import MemoryInfoSchema
from ._swap_memory import ImmutableSwapMemoryObjectDict, SwapMemoryObject, SwapMemoryObjectDict
from ._typeddict_types import ImmutableMemoryInfoData, ImmutableMemoryInfoDict, MemoryInfoData, MemoryInfoDict
from ._virtual_memory import ImmutableVirtualMemoryObjectDict, VirtualMemoryObject, VirtualMemoryObjectDict

__all__ = [
    "MemoryInfoSchema",
    "MemoryInfo",
    "MemoryInfoData",
    "ImmutableMemoryInfoData",
    "MemoryInfoDict",
    "ImmutableMemoryInfoDict",
    "SwapMemoryObject",
    "SwapMemoryObjectDict",
    "ImmutableSwapMemoryObjectDict",
    "VirtualMemoryObject",
    "VirtualMemoryObjectDict",
    "ImmutableVirtualMemoryObjectDict",
]
