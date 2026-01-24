"""Types used by SimpleBench."""

from ._element_collection import ElementCollection, is_element_collection
from ._values import Values
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
from .variations import ImmutableVariationColsType, ImmutableVariationMarksType, VariationColsType, VariationMarksType

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
    'VariationColsType',
    'ImmutableVariationColsType',
    'VariationMarksType',
    'ImmutableVariationMarksType',
    'IMMUTABLE_CORE_DATA_TYPES_TUPLE',
]
