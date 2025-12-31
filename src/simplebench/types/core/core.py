"""Defines primitive and recursively-defined data types for SimpleBench.

This module provides two key `TypeAlias` definitions:
- `CoreDataTypes`: A general-purpose alias for serializable data/structures.
- `ImmutableCoreDataTypes`: A stricter alias for immutable serializable data/structures.

There are also several related `TypeAlias` definitions for mappings, sequences, and sets
built upon these core types and is_* functions to validate instances of these types.
"""
from __future__ import annotations

import threading
from collections import OrderedDict
from collections.abc import Mapping, Sequence, Set
from types import MappingProxyType
from typing import Any, Final, TypeAlias, TypeGuard

from simplebench.defaults import DEFAULT_MAX_CORE_DATA_DEPTH
from simplebench.exceptions import SimpleBenchTypeError, SimpleBenchValueError
from simplebench.validators import core_data_types as validators

from ._error_tags import _CoreTypeErrorTags

CoreDataTypes: TypeAlias = str | int | float | bool | None | \
    Sequence['CoreDataTypes'] | Mapping[str, 'CoreDataTypes'] | Set['CoreDataTypes']
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


class ImmutableDict(Mapping[str, 'ImmutableCoreDataTypes']):
    """Immutable dictionary type for use in ImmutableCoreDataTypes.

    This class implements the Mapping interface to provide an immutable
    dictionary-like object that can be used as part of the ImmutableCoreDataTypes
    type alias.

    It is both serializable and immutable.
    """

    def __init__(self, data: 'CoreDataMappingType') -> None:
        """Initialize the ImmutableDict with the provided data.

        :param Mapping[str, ImmutableCoreDataTypes] data: The data to store in the immutable dictionary.
        """
        validated_data = validators.validate_core_data_mapping(
                            data, 'ImmutableDict initialization')
        self._data: 'ImmutableCoreDataMappingType' = validated_data

    def __getitem__(self, key: str) -> 'ImmutableCoreDataTypes':
        return self._data[key]

    def __iter__(self):
        return iter(self._data)

    def __len__(self) -> int:
        return len(self._data)

    def __contains__(self, key: object) -> bool:
        return key in self._data

    def keys(self):
        return self._data.keys()

    def values(self):
        return self._data.values()

    def get(self,
            key: str,
            default: Any = None) -> 'ImmutableCoreDataTypes':
        return self._data.get(key, default)

    def items(self):
        return self._data.items()

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Mapping):
            return False
        return dict(self._data) == dict(other)

    def __ne__(self, other: object) -> bool:
        return not self.__eq__(other)

class ImmutableTypedDict(Mapping[str, 'ImmutableCoreDataTypes']):
    """Immutable typed dictionary for use in ImmutableCoreDataTypes.

    This class extends both TypedDict and ImmutableDict to provide an immutable
    typed dictionary-like object that can be used as part of the ImmutableCoreDataTypes
    type alias.

    It is both serializable and immutable.
    """
    def __init__(self, data: 'CoreDataMappingType') -> None:
        """Initialize the ImmutableDict with the provided data.

        :param Mapping[str, ImmutableCoreDataTypes] data: The data to store in the immutable dictionary.
        """
        validated_data = validators.validate_core_data_mapping(
                            data, 'ImmutableDict initialization')
        self._data: 'ImmutableCoreDataMappingType' = validated_data

    def __getitem__(self, key: str) -> 'ImmutableCoreDataTypes':
        return self._data[key]

    def __iter__(self):
        return iter(self._data)

    def __len__(self) -> int:
        return len(self._data)

    def __contains__(self, key: object) -> bool:
        return key in self._data

    def keys(self):
        return self._data.keys()

    def values(self):
        return self._data.values()

    def get(self,
            key: str,
            default: Any = None) -> 'ImmutableCoreDataTypes':
        return self._data.get(key, default)

    def items(self):
        return self._data.items()

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Mapping):
            return False
        return dict(self._data) == dict(other)

    def __ne__(self, other: object) -> bool:
        return not self.__eq__(other)


ImmutableCoreDataTypes: TypeAlias = str | int | float | bool | None | \
    tuple['ImmutableCoreDataTypes', ...] | frozenset['ImmutableCoreDataTypes'] | \
    MappingProxyType[str, 'ImmutableCoreDataTypes'] | ImmutableDict
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

CoreDataMappingType: TypeAlias = Mapping[str, CoreDataTypes]
"""Type alias for a mapping from strings to core data types.

This type represents a mapping where the keys are non-empty, non-blank strings
and the values are core data types as defined by `CoreDataTypes`.

It is serializable.
"""


ImmutableCoreDataMappingType: TypeAlias = MappingProxyType[str, ImmutableCoreDataTypes] | ImmutableDict
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

CoreDataPrimitiveTypesTuple: tuple[type, ...] = (str, int, float, bool, type(None))
"""Tuple of types representing core data primitive types."""
