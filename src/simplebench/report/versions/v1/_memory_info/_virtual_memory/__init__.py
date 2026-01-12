"""Virtual memory validation and representation for version 1."""

from ._typeddict_types import ImmutableVirtualMemoryObjectDict, VirtualMemoryObjectDict
from ._virtual_memory import VirtualMemoryObject

__all__ = ['VirtualMemoryObject', 'VirtualMemoryObjectDict', 'ImmutableVirtualMemoryObjectDict']
