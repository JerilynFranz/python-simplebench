"""Validators for complex data types used in SimpleBench.

These validators ensure that data structures conform to the CoreDataTypes
contract defined in :module:`simplebench.types.core`.

They recursively validate mappings, sequences, and sets to ensure all
elements conform to the allowed primitive types.
"""

import math
from collections.abc import Mapping, Sequence, Set

from simplebench.exceptions import SimpleBenchRecursionError, SimpleBenchTypeError, SimpleBenchValueError
from simplebench.simplebench_types import (
    CoreDataMapping,
    CoreDataMappingType,
    CoreDataSequence,
    CoreDataSequenceType,
    CoreDataSet,
    CoreDataSetType,
    CoreDataTypes,
)
from simplebench.validators import _ValidatorsErrorTag


def validate_core_data_mapping(item: CoreDataMappingType, name: str) -> CoreDataMapping:
    """Validate a CoreDataTypes mapping.

    The `value` parameter must be a `Mapping[str, CoreDataTypes]` conformant mapping.

    It can have arbitrary keys and values but must conform with the :class:`CoreDataTypes` contract,
    and must use strings as keys. The entire mapping tree is validated recursively to ensure all
    elements conform to the :class:`CoreDataTypes` definition.

    It cannot contain cyclic references and must not exceed the recursion depth.

    The validated mapping is returned as an immutable :class:`CoreDataMapping`.

    This has the result of ensuring that the returned mapping is both serializable and immutable
    and transforms all mutable structures (like lists and dicts) into their immutable counterparts
    (like CoreDataMapping, CoreDataSet, and CoreDataSequence). This includes classes that are
    subclasses of the allowed  mutable and immutable types.

    .. note:: This is a composable validator without dependencies on other public validators.
        This makes it safe to use in other validators without any risk of creating circular
        dependencies.

    :param CoreDataMappingType value: The data mapping to validate.
    :param str name: The name of the mapping (used in error messages).
    :return CoreDataMappingType: An immutable validated data mapping.
    :raises SimpleBenchTypeError: If the tree structure contains invalid types.
    :raises SimpleBenchValueError: If any dictionary key is a blank or empty string.
    :raises SimpleBenchRecursionError: If the checking exceeds the recursion limit.
    """
    if not isinstance(name, str):
        raise SimpleBenchTypeError(
            f'The `name` parameter must be a string, got {type(name).__name__}.',
            tag=_ValidatorsErrorTag.INVALID_NAME_PARAM_TYPE,
        )

    if name.strip() == '':
        raise SimpleBenchValueError(
            'The `name` parameter must be a non-blank, non-empty string.',
            tag=_ValidatorsErrorTag.INVALID_NAME_PARAM_VALUE,
        )
    if isinstance(item, CoreDataMapping):
        return item
    try:
        return CoreDataMapping(item)
    except RecursionError as exc:
        raise SimpleBenchRecursionError(
            f"Recursion limit reached {exc}",
            tag=_ValidatorsErrorTag.RECURSION_LIMIT_REACHED) from exc


def validate_core_data_sequence(item: CoreDataSequenceType, name: str) -> CoreDataSequence:
    """Validate a CoreDataTypes sequence.
    The `value` parameter must be a `Sequence[CoreDataTypes]` conformant sequence.
    It can have arbitrary values but must conform with the :class:`CoreDataTypes` contract.
    The entire sequence tree is validated recursively to ensure all elements conform to the
    :class:`CoreDataTypes` definition.

    It cannot contain cyclic references and must not exceed the recursion depth for nested structures.

    This has the result of ensuring that the returned sequence is both serializable and immutable
    and transforms all mutable structures (like lists and dicts) into their immutable counterparts
    (like CoreDataSequence, CoreDataSet, and CoreDataMapping). This includes classes that are subclasses of the allowed
     mutable and immutable types.

    .. note:: This is a composable validator without dependencies on other public validators.
        This makes it safe to use in other validators without any risk of creating circular
        dependencies.
    :param CoreDataSequenceType item: The data sequence to validate.
    :param str name: The name of the mapping (used in error messages).
    :return CoreDataSequence: An immutable validated data sequence.
    :raises SimpleBenchTypeError: If the tree structure contains invalid types.
    :raises SimpleBenchRecursionError: If the checking exceeds the recursion limit.
    """
    if not isinstance(name, str):
        raise SimpleBenchTypeError(
            f'The `name` parameter must be a string, got {type(name).__name__}.',
            tag=_ValidatorsErrorTag.INVALID_NAME_PARAM_TYPE,
        )
    if name.strip() == '':
        raise SimpleBenchValueError(
            'The `name` parameter must be a non-blank, non-empty string.',
            tag=_ValidatorsErrorTag.INVALID_NAME_PARAM_VALUE,
        )

    if isinstance(item, CoreDataSequence):
        return item

    try:
        return CoreDataSequence(item)
    except RecursionError as exc:
        raise SimpleBenchRecursionError(
            f"Recursion limit reached {exc}",
            tag=_ValidatorsErrorTag.RECURSION_LIMIT_REACHED) from exc


def validate_core_data_set(item: CoreDataSetType, name: str) -> CoreDataSet:
    """Validate a CoreDataTypes set.

    The `value` parameter must be a `Set[CoreDataTypes]` conformant set.

    It can have arbitrary values but must conform with the :class:`CoreDataTypes` contract.
    The entire set tree is validated recursively to ensure all elements conform to the
    :class:`CoreDataTypes` definition.

    It cannot contain cyclic references and must not exceed the specified maximum depth for nested structures.

    The validated set is returned as an immutable `frozenset[ImmutableCoreDataTypes]`.

    This has the result of ensuring that the returned set is both serializable and immutable
    and transforms all mutable structures (like lists and dicts) into their immutable counterparts
    (like tuples and MappingProxyType). This includes classes that are subclasses of the allowed
     mutable and immutable types.

    .. note:: This is a composable validator without dependencies on other public validators.
        This makes it safe to use in other validators without any risk of creating circular
        dependencies.

    :param CoreDataSetType item: The data set to validate.
    :param str name: The name of the mapping (used in error messages).
    :param int max_depth: The maximum allowed depth for nested structures. (optional, keyword-only, defaults to 10).
    :return CoreDataSet: An immutable validated data set.
    :raises SimpleBenchTypeError: If the tree structure contains invalid types.
    :raises SimpleBenchRecursionError: If the checking exceeds the recursion limit.
    """
    if not isinstance(name, str):
        raise SimpleBenchTypeError(
            f'The `name` parameter must be a string, got {type(name).__name__}.',
            tag=_ValidatorsErrorTag.INVALID_NAME_PARAM_TYPE,
        )

    if name.strip() == '':
        raise SimpleBenchValueError(
            'The `name` parameter must be a non-blank, non-empty string.',
            tag=_ValidatorsErrorTag.INVALID_NAME_PARAM_VALUE,
        )

    if isinstance(item, CoreDataSet):
        return item

    try:
        return CoreDataSet(item)
    except RecursionError as exc:
        raise SimpleBenchRecursionError(
            f"Recursion limit reached {exc}",
            tag=_ValidatorsErrorTag.RECURSION_LIMIT_REACHED) from exc


def _internal_validate_core_data(item: CoreDataTypes, name: str) -> CoreDataTypes:
    """Recursively validate a CoreDataTypes item.

    Helper function that performs a recursive validation of the data/structure
    and conversion to immutable types.

    :param CoreDataTypes item: The item to validate.
    :param str name: The name of the mapping (used in error messages).
    :return CoreDataTypes: The validated immutable item.
    :raises SimpleBenchTypeError: If the tree structure contains invalid types.
    :raises SimpleBenchValueError: If any dictionary key is not a valid python identifier.
    :raises SimpleBenchRecursionError: If the checking exceeds the recursion limit.
    """
    # bytes are not allowed in CoreDataTypes even though they are Sequences
    # This is because they are problematic when serialized to JSON.
    if isinstance(item, bytes):
        raise SimpleBenchTypeError(
            f'Invalid data type for element in `{name}` mapping: bytes. '
            f'Allowed types are Mapping, Sequence, Set, str, int, float, complex, bool, and None.',
            tag=_ValidatorsErrorTag.INVALID_CORE_MAPPING_PARAM_VALUE,
        )

    # Primitives
    if isinstance(item, (str, int, float, complex, bool)) or item is None:
        # Check for non-finite floats (NaN, Infinity)
        if isinstance(item, float):
            if math.isnan(item) or math.isinf(item):
                raise SimpleBenchValueError(
                    f'Float values in `{name}` cannot be NaN or Infinity.',
                    tag=_ValidatorsErrorTag.INVALID_CORE_MAPPING_PARAM_VALUE,
                )
        if isinstance(item, complex):
            if math.isnan(item.real) or math.isinf(item.real) or math.isnan(item.imag) or math.isinf(item.imag):
                raise SimpleBenchValueError(
                    f'Complex values in `{name}` cannot have NaN or Infinity components.',
                    tag=_ValidatorsErrorTag.INVALID_CORE_MAPPING_PARAM_VALUE,
                )
        return item

    elif isinstance(item, Set):
        return item if isinstance(item, CoreDataSet) else CoreDataSet(item)

    elif isinstance(item, Mapping):
        return item if isinstance(item, CoreDataMapping) else CoreDataMapping(item)

    elif isinstance(item, Sequence) and not isinstance(item, (str, bytes)):
        return item if isinstance(item, CoreDataSequence) else CoreDataSequence(item)

    raise SimpleBenchTypeError(
        f'Invalid data type for element in `{name}` mapping: {type(item).__name__}. '
        f'Allowed types are Mapping, Sequence, Set, str, int, float, bool, and None.',
        tag=_ValidatorsErrorTag.INVALID_CORE_MAPPING_PARAM_VALUE,
    )


def validate_core_data(item: CoreDataTypes, name: str) -> CoreDataTypes:
    """Validate a CoreDataTypes item.

    The `value` parameter must be a `CoreDataTypes` conformant data/structure.
    It can have arbitrary structure but must conform with the :class:`CoreDataTypes` contract.
    The entire data tree is validated recursively to ensure all elements conform to the
    :class:`CoreDataTypes` definition.

    This has the result of ensuring that the returned data/structure is both serializable and immutable
    and transforms all mutable structures (like lists and dicts) into their immutable counterparts
    (like CoreDataSet, CoreDataSequence, and CoreDataMapping). This includes classes that are
    subclasses of the allowed  mutable and immutable types.

    .. note:: This is a composable validator without dependencies on other public validators.
        This makes it safe to use in other validators without any risk of creating circular
        dependencies.

    :param CoreDataTypes value: The data/structure to validate.
    :param str name: The name of the mapping (used in error messages).
    :return CoreDataTypes: An immutable validated data/structure.
    :raises SimpleBenchTypeError: If the tree structure contains invalid types.
    :raises SimpleBenchValueError: If any dictionary key is not a valid python identifier
    :raises SimpleBenchRecursionError: If the checking exceeds the recursion limit.
    """
    try:
        return _internal_validate_core_data(item=item, name=name)

    except RecursionError as exc:
        raise SimpleBenchRecursionError(
            f"Recursion limit reached {exc}",
            tag=_ValidatorsErrorTag.RECURSION_LIMIT_REACHED) from exc

