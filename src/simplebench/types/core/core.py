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
from typing import Final, TypeAlias, TypeGuard

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

ImmutableCoreDataTypes: TypeAlias = str | int | float | bool | None | tuple['ImmutableCoreDataTypes', ...] | \
    frozenset['ImmutableCoreDataTypes'] | MappingProxyType[str, 'ImmutableCoreDataTypes']
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

_MAX_CACHE_SIZE = 1024
"""Maximum size for the immutable core data type cache."""

_IMMUTABLE_ITEMS_CACHE: OrderedDict[int, ImmutableCoreDataTypes] = OrderedDict()
"""Cache for immutable core data type references to optimize repeated checks."""

class _NotInCache:
    """Sentinel class representing a value not found in the cache."""


_NOT_IN_CACHE: Final[_NotInCache] = _NotInCache()

def is_core_data_type(
        value: CoreDataTypes, *,
        max_depth=DEFAULT_MAX_CORE_DATA_DEPTH) -> TypeGuard[CoreDataTypes]:
    """Check if a value is a valid CoreDataTypes instance.

    :param object value: The value to check.
    :param int max_depth: Maximum depth to check nested structures.
    :return bool: True if the value is a valid CoreDataTypes instance, False otherwise.
    """
    try:
        validators.validate_core_data(value, 'CoreData is checking', max_depth=max_depth)
        return True
    except (ValueError, TypeError):
        return False

def is_core_data_mapping_type(
        value: CoreDataMappingType, *,
        max_depth=DEFAULT_MAX_CORE_DATA_DEPTH) -> TypeGuard[CoreDataMappingType]:
    """Check if a value is a valid CoreDataMappingType instance.

    :param object value: The value to check.
    :param int max_depth: Maximum depth to check nested structures.
    :return bool: True if the value is a valid CoreDataMappingType instance, False otherwise.
    """
    try:
        validators.validate_core_data_mapping(value, 'CoreDataMapping is checking', max_depth=max_depth)
        return True
    except (ValueError, TypeError):
        return False

def is_core_data_sequence_type(
        value: CoreDataSequenceType, *,
        max_depth=DEFAULT_MAX_CORE_DATA_DEPTH) -> TypeGuard[CoreDataSequenceType]:
    """Check if a value is a valid CoreDataSequenceType instance.

    :param object value: The value to check.
    :param int max_depth: Maximum depth to check nested structures.
    :return bool: True if the value is a valid CoreDataSequenceType instance, False otherwise.
    """
    try:
        validators.validate_core_data_sequence(value, 'CoreDataSequence is checking', max_depth=max_depth)
        return True
    except (ValueError, TypeError):
        return False

def is_core_data_set_type(
        value: CoreDataSetType, *,
        max_depth=DEFAULT_MAX_CORE_DATA_DEPTH) -> TypeGuard[CoreDataSetType]:
    """Check if a value is a valid CoreDataSetType instance.

    :param object value: The value to check.
    :param int max_depth: Maximum depth to check nested structures.
    :return bool: True if the value is a valid CoreDataSetType instance, False otherwise.
    """
    try:
        validators.validate_core_data_set(value, 'CoreDataSet is checking', max_depth=max_depth)
        return True
    except (ValueError, TypeError):
        return False

def is_immutable_core_data_type(
        value: ImmutableCoreDataTypes, *,
        max_depth=DEFAULT_MAX_CORE_DATA_DEPTH) -> TypeGuard[ImmutableCoreDataTypes]:
    """Check if a value is a valid ImmutableCoreDataTypes instance.

    :param object value: The value to check.
    :param int max_depth: Maximum depth to check nested structures.
    :return bool: True if the value is a valid ImmutableCoreDataTypes instance, False otherwise.
    """
    if value is _in_immutables_cache(value):
        return True

    try:
        validators.validate_immutable_core_data(value, 'ImmutableCoreData is checking', max_depth=max_depth)
        return True
    except (ValueError, TypeError):
        return False

def is_immutable_core_data_mapping_type(
        value: ImmutableCoreDataMappingType, *,
        max_depth=DEFAULT_MAX_CORE_DATA_DEPTH) -> TypeGuard[ImmutableCoreDataMappingType]:
    """Check if a value is a valid ImmutableCoreDataMappingType instance.

    :param object value: The value to check.
    :param int max_depth: Maximum depth to check nested structures.
    :return bool: True if the value is a valid ImmutableCoreDataMappingType instance, False otherwise.
    """
    if value is _in_immutables_cache(value) and isinstance(value, MappingProxyType):
        return True
    try:
        validators.validate_immutable_core_data_mapping(
            value, 'ImmutableCoreDataMapping is checking', max_depth=max_depth)
        return True
    except (ValueError, TypeError):
        return False

def is_immutable_core_data_sequence_type(
        value: ImmutableCoreDataSequenceType, *,
        max_depth=DEFAULT_MAX_CORE_DATA_DEPTH) -> TypeGuard[ImmutableCoreDataSequenceType]:
    """Check if a value is a valid ImmutableCoreDataSequenceType instance.

    :param object value: The value to check.
    :param int max_depth: Maximum depth to check nested structures.
    :return bool: True if the value is a valid ImmutableCoreDataSequenceType instance, False otherwise.
    """
    if value is _in_immutables_cache(value) and isinstance(value, tuple):
        return True
    try:
        validators.validate_immutable_core_data_sequence(
            value, 'ImmutableCoreDataSequence is checking', max_depth=max_depth)
        return True
    except (ValueError, TypeError):
        return False

def is_immutable_core_data_set_type(
        value: ImmutableCoreDataSetType, *,
        max_depth=DEFAULT_MAX_CORE_DATA_DEPTH) -> TypeGuard[ImmutableCoreDataSetType]:
    """Check if a value is a valid ImmutableCoreDataSetType instance.

    :param object value: The value to check.
    :param int max_depth: Maximum depth to check nested structures.
    :return bool: True if the value is a valid ImmutableCoreDataSetType instance, False otherwise.
    """
    if value is _in_immutables_cache(value) and isinstance(value, frozenset):
        return True

    try:
        validators.validate_immutable_core_data_set(
            value, 'ImmutableCoreDataSet is checking', max_depth=max_depth)
        _cache_immutable_reference(value)
        return True
    except (ValueError, TypeError):
        return False

def _in_immutables_cache(value: ImmutableCoreDataTypes) -> ImmutableCoreDataTypes | _NotInCache:
    """
    Check if an immutable core data type reference is cached and return it
    if found. Otherwise, return the sentinel object `_NOT_IN_CACHE`.

    This function is robust against rare race conditions where the cache
    entry is deleted between the 'in' check and the dictionary access.

    :param ImmutableCoreDataTypes value: The immutable core data type to check.
    :return ImmutableCoreDataTypes | _NotInCache: The cached value if found, else `_NOT_IN_CACHE` object.
    """
    value_id = id(value)
    if value_id in _IMMUTABLE_ITEMS_CACHE:
        try:  # optimistic access for performance
            cached_value = _IMMUTABLE_ITEMS_CACHE[value_id]
            if cached_value is value:
                return cached_value
        except KeyError:
            # Item was removed between the 'in' check and access by another thread
            return _NOT_IN_CACHE
    return _NOT_IN_CACHE

_CACHE_LOCK = threading.Lock()

def _cache_immutable_reference(value: ImmutableCoreDataTypes) -> None:
    """Cache an immutable core data type reference.

    :param ImmutableCoreDataTypes value: The immutable core data type to cache.
    """
    with _CACHE_LOCK:
        _IMMUTABLE_ITEMS_CACHE.setdefault(id(value), value)
        _trim_immutables_cache(_MAX_CACHE_SIZE)

def _trim_immutables_cache(size: int) -> None:
    """Trim the immutable core data type cache to the specified size.

    If the cache exceeds the specified size, the oldest entries are removed
    until the cache size is at or below 75% of the specified size (rounding down).

    This helps maintain cache efficiency while preventing unbounded growth
    and minimizing performance impact from frequent trimming.

    The smallest allowed size is 10.

    Cache trimming is performed within a thread-safe lock.

    :param int size: The maximum size of the cache.
    :raises SimpleBenchTypeError: If size is not an integer.
    :raises SimpleBenchValueError: If size is less than 1.
    """
    if not isinstance(size, int):
        raise SimpleBenchTypeError(
            'Cache size must be an integer.',
            tag=_CoreTypeErrorTags.INVALID_CACHE_TYPE)

    if size < 10: # Minimum size to ensure effective caching
        raise SimpleBenchValueError(
            'Cache size must be at least 10',
            tag=_CoreTypeErrorTags.INVALID_CACHE_SIZE)

    with _CACHE_LOCK:
        target_size = int(size * 0.75)
        while len(_IMMUTABLE_ITEMS_CACHE) > target_size:
            _IMMUTABLE_ITEMS_CACHE.popitem(last=False)
