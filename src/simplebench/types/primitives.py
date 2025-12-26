"""Defines primitive and recursively-defined data types for SimpleBench.

This module provides two key `TypeAlias` definitions:
- `CoreDataTypes`: A general-purpose alias for serializable data/structures.
- `ImmutableCoreDataTypes`: A stricter alias for immutable serializable data/structures.
"""
# pylint: disable=line-too-long
from __future__ import annotations

from collections.abc import Mapping, Sequence, Set
from types import MappingProxyType
from typing import TypeAlias

CoreDataTypes: TypeAlias = str | int | float | bool | None | Sequence['CoreDataTypes'] | Mapping[str, 'CoreDataTypes'] | Set['CoreDataTypes']
"""Type alias for the core data type primitives used in SimpleBench.

These are the primitive data types that can be safely used in various
data structures within SimpleBench.

They are serializable, but not necessarily immutable.

Allowed types are:
    - str
    - int
    - float
    - bool
    - None
    - `Sequence[CoreDataTypes]` (covers list, tuple, etc.)
    - `Mapping[str, CoreDataTypes]` (covers dict, MappingProxyType, etc.)
    - `Set[CoreDataTypes]` (covers set, frozenset)
"""

ImmutableCoreDataTypes: TypeAlias = str | int | float | bool | None | tuple['ImmutableCoreDataTypes', ...] | frozenset['ImmutableCoreDataTypes'] | MappingProxyType[str, 'ImmutableCoreDataTypes']
"""Type alias for the immutable core data type primitives used in SimpleBench.

These are the immutable primitive data types that can be used in various
data structures within SimpleBench.

They are both serializable and immutable.

Allowed types are:
    - str
    - int
    - float
    - bool
    - None
    - `tuple[ImmutableCoreDataTypes, ...]`
    - `frozenset[ImmutableCoreDataTypes]`
    - `MappingProxyType[str, ImmutableCoreDataTypes]`
"""
