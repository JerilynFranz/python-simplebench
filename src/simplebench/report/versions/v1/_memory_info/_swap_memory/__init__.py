"""Swap memory validation and representation for version 1."""

from ._swap_memory import SwapMemoryObject
from ._typeddict_types import ImmutableSwapMemoryObjectDict, SwapMemoryObjectDict

__all__ = ['SwapMemoryObject', 'SwapMemoryObjectDict', 'ImmutableSwapMemoryObjectDict']
