"""Defines primitive and recursively-defined data types for SimpleBench.

This module provides two key `TypeAlias` definitions:
- `CoreDataTypes`: A general-purpose alias for serializable data/structures.
- `ImmutableCoreDataTypes`: A stricter alias for immutable serializable data/structures.

There are also several related `TypeAlias` definitions for mappings, sequences, and sets
built upon these core types and is_* functions to validate instances of these types.
"""

from collections.abc import Mapping, Sequence, Set
from types import MappingProxyType, NoneType
from typing import TypeAlias

CoreDataTypes: TypeAlias = (
    str
    | bytes
    | int
    | float
    | bool
    | complex
    | None
    | Sequence['CoreDataTypes']
    | Mapping[str, 'CoreDataTypes']
    | Set['CoreDataTypes']
)
"""Type alias for the core data type primitives used in SimpleBench.

These are the primitive data types that can be safely used in various
data structures within SimpleBench.

They are serializable, but not necessarily immutable.

Allowed types are:
    - str
    - bytes
    - int
    - float
    - bool
    - complex
    - None
    - `Sequence[CoreDataTypes]` (covers list, tuple, etc.)
    - `Mapping[str, CoreDataTypes]` (covers dict, MappingProxyType, etc.)
    - `Set[CoreDataTypes]` (covers set, frozenset)
"""

IMMUTABLE_CORE_DATA_TYPES_TUPLE = (str, bytes, int, float, bool, complex, NoneType, tuple, frozenset, MappingProxyType)
"""Tuple of types representing immutable core data primitive types.

Includes:
    - str
    - bytes
    - int
    - float
    - bool
    - complex
    - NoneType
    - tuple
    - frozenset
    - MappingProxyType
"""

ImmutableCoreDataTypes: TypeAlias = (
    str
    | bytes
    | int
    | float
    | bool
    | complex
    | None
    | tuple['ImmutableCoreDataTypes', ...]
    | frozenset['ImmutableCoreDataTypes']
    | MappingProxyType[str, 'ImmutableCoreDataTypes']
)
"""Type alias for the immutable core data type primitives used in SimpleBench.

These are the immutable primitive data types that can be used in various
data structures within SimpleBench.

They are both serializable and immutable.

Allowed types are:
    - :class:`str`
    - :class:`bytes`
    - :class:`int`
    - :class:`float`
    - :class:`complex`
    - :class:`bool`
    - :obj:`None`
    - `tuple[ImmutableCoreDataTypes, ...]`
    - `frozenset[ImmutableCoreDataTypes]`
    - `MappingProxyType[str, ImmutableCoreDataTypes]`
"""

CoreDataMappingType: TypeAlias = Mapping[str, CoreDataTypes]
"""Type alias for a mapping from strings to core data types.

This type represents a mapping where the keys are non-empty, non-blank strings
and the values are core data types as defined by `CoreDataTypes`.

It is serializable.
"""


ImmutableCoreDataMappingType: TypeAlias = MappingProxyType[str, ImmutableCoreDataTypes]
"""Type alias for an immutable mapping from strings to immutable core data types.

This type represents a mapping where the keys are non-empty, non-blank strings
and the values are immutable core data types as defined by `ImmutableCoreDataTypes`.

It is both serializable and immutable.
"""

CoreDataSequenceType: TypeAlias = Sequence[CoreDataTypes]
"""Type alias for a sequence of core data types.

This type represents a sequence (like a list or tuple) where each element
is a core data type as defined by `CoreDataTypes`.
It is serializable.
"""

ImmutableCoreDataSequenceType: TypeAlias = tuple[ImmutableCoreDataTypes, ...]
"""Type alias for an immutable sequence of immutable core data types.

This type represents an immutable sequence (tuple) where each element
is an immutable core data type as defined by `ImmutableCoreDataTypes`.
It is both serializable and immutable.
"""

CoreDataSetType: TypeAlias = Set[CoreDataTypes]
"""Type alias for a set of core data types.

This type represents a set where each element is a core data type
as defined by `CoreDataTypes`.
It is serializable.
"""

ImmutableCoreDataSetType: TypeAlias = frozenset[ImmutableCoreDataTypes]
"""Type alias for an immutable set of immutable core data types.

This type represents an immutable set (frozenset) where each element
is an immutable core data type as defined by `ImmutableCoreDataTypes`.

It is both serializable and immutable.
"""

CORE_DATA_PRIMITIVE_TYPES_TUPLE: tuple[type, ...] = (str, bytes, int, float, bool, complex, NoneType)
"""Tuple of types representing core data primitive types.

They are all immutable and serializable.

Includes:
    - str
    - bytes
    - int
    - float
    - bool
    - complex
    - NoneType
"""
