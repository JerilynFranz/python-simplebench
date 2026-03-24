"""Defines primitive and recursively-defined data types for SimpleBench.

Provides type aliases for core data types used throughout SimpleBench
and their immutable counterparts. Also provides tuples of types for runtime
type checking.

Defined types and tuplesinclude:
- :class:`CoreDataPrimitiveTypes` - a type alias for primitive data types.
- :data:`CORE_DATA_PRIMITIVE_TYPES_TUPLE` - a tuple of primitive data types for isinstance() checks.
- :class:`CoreDataTypes` - a recursive type alias for all core data types used in SimpleBench.
- :class:`ImmutableCoreDataTypes` - a recursive type alias for all immutable core data types used in SimpleBench.
- :data:`IMMUTABLE_CORE_DATA_TYPES_TUPLE` - a tuple of immutable core data types for isinstance() checks.
- :class:`CoreDataMappingType` - a type alias for mappings from strings to core data types.
- :class:`CoreDataSequenceType` - a type alias for sequences of core data types.
- :class:`CoreDataSetType` - a type alias for sets of core data types.
"""

from collections.abc import Mapping, Sequence, Set
from types import NoneType
from typing import TypeAlias

from ._core_data_mapping import CoreDataMapping
from ._core_data_sequence import CoreDataSequence
from ._core_data_set import CoreDataSet

__all__: list[str] = []


CoreDataPrimitiveTypes: TypeAlias = (str | int | float | bool | None)
"""Type alias for core data primitive types.

These are all immutable and serializable.

Includes:

- str
- int
- float
- bool
- NoneType
"""

CORE_DATA_PRIMITIVE_TYPES_TUPLE: tuple[type, ...] = (str, int, float, bool, NoneType)
"""Tuple of types representing core data primitive types.

They are all immutable and serializable.

It is intended for use in runtime type checking via isinstance().

Includes:
    - str
    - int
    - float
    - bool
    - NoneType
"""

CoreDataTypes: TypeAlias = (
    str
    | int
    | float
    | bool
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
    - int
    - float
    - bool
    - None
    - `Sequence[CoreDataTypes]` (covers list, tuple, etc.)
    - `Mapping[str, CoreDataTypes]` (covers dict, MappingProxyType, etc.)
    - `Set[CoreDataTypes]` (covers set, frozenset)
"""

IMMUTABLE_CORE_DATA_TYPES_TUPLE = (
    str,
    int,
    float,
    bool,
    NoneType,
    CoreDataSequence,
    CoreDataMapping,
    CoreDataSet)
"""Tuple of types representing immutable core data types.

They are deep immutable and serializable.

It is intended for use in runtime type checking via isinstance().

Includes:
    - str
    - int
    - float
    - bool
    - NoneType
    - CoreDataSequence
    - CoreDataMapping
    - CoreDataSet
"""

def is_immutable_core_data_type(value: object) -> bool:
    """Check if a value is of an immutable core data type.

    It is intended for use in runtime type checking.

    It is necessary to avoid recursive type issues inside the
    CoreDataSet, CoreDataMapping, and CoreDataSequence classes.

    Includes:
        - str
        - int
        - float
        - bool
        - NoneType
        - CoreDataSequence
        - CoreDataMapping
        - CoreDataSet

    :param value: The value to check.
    :type value: object
    :return: True if the value is an instance of an immutable core data type, False otherwise.
    """
    from ._core_data_mapping import CoreDataMapping
    from ._core_data_sequence import CoreDataSequence
    from ._core_data_set import CoreDataSet

    return isinstance(
        value, CORE_DATA_PRIMITIVE_TYPES_TUPLE) or isinstance(
            value, (CoreDataMapping, CoreDataSequence, CoreDataSet))

CORE_DATA_TYPES_TUPLE = (
    str,
    int,
    float,
    bool,
    NoneType,
    Sequence,
    Mapping,
    Set)
"""Tuple of types representing core data types.
They are serializable, but not necessarily immutable.
It is intended for use in runtime type checking via isinstance().

Includes:
    - str
    - int
    - float
    - bool
    - NoneType
    - Sequence
    - Mapping
    - Set
"""

ImmutableCoreDataTypes: TypeAlias = (
    str
    | int
    | float
    | bool
    | None
    | CoreDataMapping
    | CoreDataSequence
    | CoreDataSet
)
"""Type alias for the immutable core data types used in SimpleBench.

These are the immutable data types that can be used in various
data structures within SimpleBench.

They are both serializable and deep immutable.

Allowed types are:
    - :class:`str`
    - :class:`int`
    - :class:`float`
    - :class:`bool`
    - :data:`None`
    - :class:`CoreDataMapping`
    - :class:`CoreDataSequence`
    - :class:`CoreDataSet`
"""

CoreDataMappingType: TypeAlias = Mapping[str, CoreDataTypes]
"""Type alias for a mapping from strings to core data types.

This type represents a mapping where the keys are non-empty, non-blank strings
and the values are core data types as defined by `CoreDataTypes`.

It is serializable but not necessarily immutable.
"""

CoreDataSequenceType: TypeAlias = Sequence[CoreDataTypes]
"""Type alias for a sequence of core data types.

This type represents a sequence (like a list or tuple) where each element
is a core data type as defined by `CoreDataTypes`.

It is serializable but not necessarily immutable.

All of its elements must be of valid CoreData types as defined by `CoreDataTypes`.
"""

CoreDataSetType: TypeAlias = Set[CoreDataTypes]
"""Type alias for a set of core data types.

This type represents a set where each element is a core data type
as defined by `CoreDataTypes`.

It is serializable but not necessarily immutable.
"""
