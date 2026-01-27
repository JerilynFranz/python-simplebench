"""Types used by SimpleBench."""

from ._element_collection import ElementCollection, is_element_collection
from ._mark import Mark
from ._values import Values
from ._variations import (
    KWArgsVariations,
    VariationCols,
    VariationMarks,
)
from .core import (
    CORE_DATA_PRIMITIVE_TYPES_TUPLE,
    IMMUTABLE_CORE_DATA_TYPES_TUPLE,
    CoreDataMappingType,
    CoreDataSequenceType,
    CoreDataSetType,
    CoreDataTypes,
    ImmutableCoreDataMappingType,
    ImmutableCoreDataSequenceType,
    ImmutableCoreDataSetType,
    ImmutableCoreDataTypes,
)
from .typeddict import Never, NotRequired, ReadOnly, Required

__all__ = [
    'ElementCollection',
    'is_element_collection',
    'NotRequired',
    'ReadOnly',
    'Required',
    'Never',
    'CoreDataTypes',
    'CoreDataMappingType',
    'CORE_DATA_PRIMITIVE_TYPES_TUPLE',
    'CoreDataSequenceType',
    'CoreDataSetType',
    'ImmutableCoreDataMappingType',
    'ImmutableCoreDataSequenceType',
    'ImmutableCoreDataSetType',
    'ImmutableCoreDataTypes',
    'Values',
    'Mark',
    'VariationCols',
    'VariationMarks',
    'KWArgsVariations',
    'IMMUTABLE_CORE_DATA_TYPES_TUPLE',
]
