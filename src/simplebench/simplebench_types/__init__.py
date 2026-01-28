"""Types used by SimpleBench."""

from ._compatibility_types import (
    Never,
    NotRequired,
    ReadOnly,
    Required,
    Self,
)
from ._core import (
    CORE_DATA_PRIMITIVE_TYPES_TUPLE,
    IMMUTABLE_CORE_DATA_TYPES_TUPLE,
    CoreDataMapping,
    CoreDataMappingType,
    CoreDataSequence,
    CoreDataSequenceType,
    CoreDataSet,
    CoreDataSetType,
    CoreDataTypes,
    ImmutableCoreDataMappingType,
    ImmutableCoreDataSequenceType,
    ImmutableCoreDataSetType,
    ImmutableCoreDataTypes,
)
from ._element_collection import ElementCollection, is_element_collection
from ._extras import Extras
from ._iterations import Iterations
from ._mark import Mark
from ._metrics_timers import MetricsTimers
from ._values import Values
from ._variations import (
    KWArgsVariations,
    VariationCols,
    VariationMarks,
)

__all__ = [
    'MetricsTimers',
    'Extras',
    'ElementCollection',
    'is_element_collection',
    'NotRequired',
    'Self',
    'ReadOnly',
    'Required',
    'Never',
    'CoreDataMapping',
    'CoreDataSequence',
    'CoreDataSet',
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
    'Iterations',
    'Mark',
    'VariationCols',
    'VariationMarks',
    'KWArgsVariations',
    'IMMUTABLE_CORE_DATA_TYPES_TUPLE',
]
