"""Core types for SimpleBench

.. code-block:: mermaid

    classDiagram
        class CoreDataMapping
        class CoreDataSequence
        class CoreDataSet

        class CoreDataPrimitiveTypes
        class CoreDataTypes
        class ImmutableCoreDataTypes

        CoreDataMapping <|-- CoreDataTypes
        CoreDataSequence <|-- CoreDataTypes
        CoreDataSet <|-- CoreDataTypes
        CoreDataPrimitiveTypes <|-- CoreDataTypes
        ImmutableCoreDataTypes <|-- CoreDataTypes

        CoreDataMappingType <|-- CoreDataMapping
        CoreDataSequenceType <|-- CoreDataSequence
        CoreDataSetType <|-- CoreDataSet
"""
# ruff: noqa: F401

from ._core_data_mapping import CoreDataMapping
from ._core_data_sequence import CoreDataSequence
from ._core_data_set import CoreDataSet
from ._types import (
    CORE_DATA_PRIMITIVE_TYPES_TUPLE,
    CORE_DATA_TYPES_TUPLE,
    IMMUTABLE_CORE_DATA_TYPES_TUPLE,
    CoreDataMappingType,
    CoreDataPrimitiveTypes,
    CoreDataSequenceType,
    CoreDataSetType,
    CoreDataTypes,
    ImmutableCoreDataTypes,
)

# No * imports at this level
__all__: list[str] = []

