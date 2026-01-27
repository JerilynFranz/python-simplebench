"""Validators for complex data types used in SimpleBench.

These validators ensure that data structures conform to the CoreDataTypes
contract defined in :module:`simplebench.types.core`.

They recursively validate mappings, sequences, and sets to ensure all
elements conform to the allowed primitive types.
"""

import math
import threading
from collections import OrderedDict
from collections.abc import Mapping, Sequence, Set
from types import MappingProxyType
from typing import Any, Final, TypeGuard

from simplebench.defaults import DEFAULT_MAX_CORE_DATA_DEPTH
from simplebench.exceptions import SimpleBenchTypeError, SimpleBenchValueError
from simplebench.simplebench_types import (
    CoreDataMappingType,
    CoreDataSequenceType,
    CoreDataSetType,
    CoreDataTypes,
    ImmutableCoreDataMappingType,
    ImmutableCoreDataSequenceType,
    ImmutableCoreDataSetType,
    ImmutableCoreDataTypes,
)
from simplebench.validators import _ValidatorsErrorTag

_CACHE_LOCK = threading.RLock()
"""Lock for thread-safe access to the immutables cache."""


class _PendingItem:
    """Helper class to represent an item pending validation in the data tree."""

    def __init__(self, item: CoreDataTypes, depth: int) -> None:
        """Initialize a `_PendingItem` instance.

        :param CoreDataTypes item: The item to be validated.
        :param int depth: The current depth of the item in the data tree.
        """
        self.item: CoreDataTypes = item
        self.depth: int = depth

    def __repr__(self) -> str:
        """Return a string representation of the PendingItem."""
        return f'_PendingItem(item={self.item}, depth={self.depth}), item id={id(self.item)})'


def _internal_validate_core_data_mapping(
    *, item: CoreDataMappingType, is_immutable: bool, name: str, max_depth: int, depth: int, parents: set[int]
) -> ImmutableCoreDataMappingType:
    """Internal helper to validate a CoreDataTypes mapping.

    It recursively validates the mapping and converts it to a deep immutable structure.

    :param Mapping[str, CoreDataTypes] value: The data mapping to validate.
    :param str name: The name of the mapping (used in error messages).
    :param bool is_immutable: Whether to check for immutability.
    :param int max_depth: The maximum allowed depth for nested structures. (optional, keyword-only, defaults to 10).
    :param int depth: The current depth in the data tree.
    :param set[int] parents: Set of ids of previously seen items to detect cycles
    :return MappingProxyType[str, ImmutableCoreDataTypes]: An immutable validated data mapping.
    :raises SimpleBenchTypeError: If the tree structure contains invalid types.
    :raises SimpleBenchValueError: If any dictionary key is a blank or empty string or
        if a cyclic reference is detected.
    """
    # we don't need to validate that `item` type is Mapping, `name`, `max_depth`,
    # or `parents` here as they are validated before this is called.
    if depth > max_depth:
        raise SimpleBenchValueError(
            f'The `{name}` mapping is too deeply nested (maximum depth is {max_depth}).',
            tag=_ValidatorsErrorTag.INVALID_CORE_MAPPING_PARAM_VALUE,
        )

    item_id = id(item)
    if item_id in parents:
        raise SimpleBenchValueError(
            f'Cyclic reference detected in `{name}`.', tag=_ValidatorsErrorTag.CYCLIC_REFERENCE_DETECTED
        )

    validated_dict: dict[str, ImmutableCoreDataTypes] = {}
    for key, element in item.items():
        if not isinstance(key, str):
            raise SimpleBenchTypeError(
                f'All keys in the `{name}` mapping must be strings. Invalid key: type {type(key).__name__}',
                tag=_ValidatorsErrorTag.INVALID_KEY_TYPE,
            )
        if key.strip() == '':
            raise SimpleBenchValueError(
                f"All keys in the `{name}` mapping must be non-blank, non-empty strings. Invalid key: '{key}'",
                tag=_ValidatorsErrorTag.INVALID_KEY_VALUE,
            )
        parents.add(item_id)
        validated_dict_element: ImmutableCoreDataTypes = _internal_validate_core_data(
            item=element, is_immutable=is_immutable, name=name, depth=depth + 1, max_depth=max_depth, parents=parents
        )
        parents.remove(item_id)
        validated_dict[key] = validated_dict_element
    return MappingProxyType(validated_dict)


def validate_core_data_mapping(
    item: Any, name: str, *, max_depth: int = DEFAULT_MAX_CORE_DATA_DEPTH
) -> ImmutableCoreDataMappingType:
    """Validate a CoreDataTypes mapping.

    The `value` parameter must be a `Mapping[str, CoreDataTypes]` conformant mapping.

    It can have arbitrary keys and values but must conform with the :class:`CoreDataTypes` contract,
    and must use strings as keys. The entire mapping tree is validated recursively to ensure all
    elements conform to the :class:`CoreDataTypes` definition.

    It cannot contain cyclic references and must not exceed the specified maximum depth for nested structures.

    The validated mapping is returned as an immutable
    :class:`ImmutableCoreDataMappingType`.

    This has the result of ensuring that the returned mapping is both serializable and immutable
    and transforms all mutable structures (like lists and dicts) into their immutable counterparts
    (like tuples and MappingProxyType). This includes classes that are subclasses of the allowed
     mutable and immutable types.

    .. note:: This is a composable validator without dependencies on other public validators.
        This makes it safe to use in other validators without any risk of creating circular
        dependencies.

    :param CoreDataMappingType value: The data mapping to validate.
    :param str name: The name of the mapping (used in error messages).
    :param int max_depth: The maximum allowed depth for nested structures. (optional, keyword-only, defaults to 10).
    :return ImmutableCoreDataMappingType: An immutable validated data mapping.
    :raises SimpleBenchTypeError: If the tree structure contains invalid types.
    :raises SimpleBenchValueError: If any dictionary key is a blank or empty string or
        if a cyclic reference is detected.
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

    if not isinstance(item, Mapping):
        raise SimpleBenchTypeError(
            f'{name} parameter is not a Mapping. Got a {type(item).__name__} instead.',
            tag=_ValidatorsErrorTag.INVALID_CORE_MAPPING_PARAM_VALUE,
        )

    if not isinstance(max_depth, int):
        raise SimpleBenchTypeError(
            f'The `max_depth` parameter must be an integer, got {type(max_depth).__name__}.',
            tag=_ValidatorsErrorTag.INVALID_NAME_PARAM_TYPE,
        )

    if max_depth <= 0:
        raise SimpleBenchValueError(
            f'The `max_depth` parameter must be a positive integer, got {max_depth}.',
            tag=_ValidatorsErrorTag.INVALID_NAME_PARAM_VALUE,
        )

    return _internal_validate_core_data_mapping(
        item=item, is_immutable=False, name=name, max_depth=max_depth, depth=0, parents=set()
    )


def _internal_validate_core_data_sequence(
    *, item: Sequence[CoreDataTypes], is_immutable: bool, name: str, depth: int, max_depth: int, parents: set[int]
) -> tuple[ImmutableCoreDataTypes, ...]:
    """Recursively validate a CoreDataTypes sequence.

    Helper function for `validate_core_data_sequence` that performs the recursive
    validation of a sequence data structure and conversion to immutable types.

    :param CoreDataSequenceType item: The item to validate.
    :param str name: The name of the mapping (used in error messages).
    :param bool is_immutable: Whether to check for immutability.
    :param int depth: The current depth in the data tree.
    :param int max_depth: The maximum allowed depth for nested structures.
    :param set[int] parents: Set of ids of previously seen items to detect cycles.
    :return ImmutableCoreDataSequenceType: The validated immutable sequence.
    :raises SimpleBenchTypeError: If the tree structure contains invalid types.
    :raises SimpleBenchValueError: If any dictionary key is a blank or empty string or if a
        cyclic reference is detected.
    """
    # we don't need to validate that `item` type is a Sequence, `name`, `max_depth`, or `parents`
    # here as they are validated before this is called.
    if depth > max_depth:
        raise SimpleBenchValueError(
            f'The `{name}` mapping is too deeply nested (maximum depth is {max_depth}).',
            tag=_ValidatorsErrorTag.INVALID_CORE_MAPPING_PARAM_VALUE,
        )

    item_id = id(item)
    if item_id in parents:
        raise SimpleBenchValueError(
            f'Cyclic reference detected in `{name}`.', tag=_ValidatorsErrorTag.CYCLIC_REFERENCE_DETECTED
        )

    parents.add(item_id)
    validated_elements: ImmutableCoreDataSequenceType = tuple(
        _internal_validate_core_data(
            item=element, is_immutable=is_immutable, name=name, depth=depth + 1, max_depth=max_depth, parents=parents
        )
        for element in item
    )
    parents.remove(item_id)
    return validated_elements


def validate_core_data_sequence(
    item: CoreDataSequenceType, name: str, *, max_depth: int = DEFAULT_MAX_CORE_DATA_DEPTH
) -> ImmutableCoreDataSequenceType:
    """Validate a CoreDataTypes sequence.
    The `value` parameter must be a `Sequence[CoreDataTypes]` conformant sequence.
    It can have arbitrary values but must conform with the :class:`CoreDataTypes` contract.
    The entire sequence tree is validated recursively to ensure all elements conform to the
    :class:`CoreDataTypes` definition.

    It cannot contain cyclic references and must not exceed the specified maximum depth for nested structures.
    The validated sequence is returned as an immutable `tuple[ImmutableCoreDataTypes, ...]`.
    This has the result of ensuring that the returned sequence is both serializable and immutable
    and transforms all mutable structures (like lists and dicts) into their immutable counterparts
    (like tuples and MappingProxyType). This includes classes that are subclasses of the allowed
     mutable and immutable types.
    .. note:: This is a composable validator without dependencies on other public validators.
        This makes it safe to use in other validators without any risk of creating circular
        dependencies.
    :param CoreDataSequenceType item: The data sequence to validate.
    :param str name: The name of the mapping (used in error messages).
    :param int max_depth: The maximum allowed depth for nested structures. (optional, keyword-only, defaults to 10).
    :return ImmutableCoreDataSequenceType: An immutable validated data sequence.
    :raises SimpleBenchTypeError: If the tree structure contains invalid types.
    :raises SimpleBenchValueError: If a cyclic reference is detected.
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
    if not isinstance(max_depth, int):
        raise SimpleBenchTypeError(
            f'The `max_depth` parameter must be an integer, got {type(max_depth).__name__}.',
            tag=_ValidatorsErrorTag.INVALID_NAME_PARAM_TYPE,
        )
    if max_depth <= 0:
        raise SimpleBenchValueError(
            f'The `max_depth` parameter must be a positive integer, got {max_depth}.',
            tag=_ValidatorsErrorTag.INVALID_NAME_PARAM_VALUE,
        )
    if not isinstance(item, Sequence) or isinstance(item, (str, bytes)):
        raise SimpleBenchTypeError(
            f'{name} parameter is not a Sequence. Got a {type(item).__name__} instead.',
            tag=_ValidatorsErrorTag.INVALID_CORE_MAPPING_PARAM_VALUE,
        )
    return _internal_validate_core_data_sequence(
        item=item, is_immutable=False, name=name, max_depth=max_depth, depth=0, parents=set()
    )


def _internal_validate_core_data_set(
    *, item: CoreDataSetType, is_immutable: bool, name: str, depth: int, max_depth: int, parents: set[int]
) -> ImmutableCoreDataSetType:
    """Recursively validate a CoreDataTypes set.

    Helper function for `validate_core_data_set` that performs the recursive
    validation of a set data structure and conversion to immutable types.

    :param CoreDataSetType item: The item to validate.
    :param str name: The name of the mapping (used in error messages).
    :param bool is_immutable: Whether to check for immutability.
    :param int depth: The current depth in the data tree.
    :param int max_depth: The maximum allowed depth for nested structures.
    :param set[int] parents: Set of ids of previously seen items to detect cycles.
    :return ImmutableCoreDataSetType: The validated immutable item.
    :raises SimpleBenchTypeError: If the tree structure contains invalid types.
    :raises SimpleBenchValueError: If any dictionary key is a blank or empty string or if a
        cyclic reference is detected.
    """
    # we don't need to validate that `item` type is a Set, `name`, `max_depth`, or `parents`
    # here as they are validated before this is called.
    if depth > max_depth:
        raise SimpleBenchValueError(
            f'The `{name}` mapping is too deeply nested (maximum depth is {max_depth}).',
            tag=_ValidatorsErrorTag.INVALID_CORE_MAPPING_PARAM_VALUE,
        )

    item_id = id(item)
    if item_id in parents:
        raise SimpleBenchValueError(
            f'Cyclic reference detected in `{name}`.', tag=_ValidatorsErrorTag.CYCLIC_REFERENCE_DETECTED
        )

    parents.add(item_id)
    validated_elements: ImmutableCoreDataSetType = frozenset(
        _internal_validate_core_data(
            item=element, is_immutable=is_immutable, name=name, depth=depth + 1, max_depth=max_depth, parents=parents
        )
        for element in item
    )
    parents.remove(item_id)
    return validated_elements


def validate_core_data_set(
    item: CoreDataSetType, name: str, *, max_depth: int = DEFAULT_MAX_CORE_DATA_DEPTH
) -> ImmutableCoreDataSetType:
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
    :return ImmutableCoreDataSetType: An immutable validated data set.
    :raises SimpleBenchTypeError: If the tree structure contains invalid types.
    :raises SimpleBenchValueError: If a cyclic reference is detected.
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

    if not isinstance(max_depth, int):
        raise SimpleBenchTypeError(
            f'The `max_depth` parameter must be an integer, got {type(max_depth).__name__}.',
            tag=_ValidatorsErrorTag.INVALID_NAME_PARAM_TYPE,
        )

    if max_depth <= 0:
        raise SimpleBenchValueError(
            f'The `max_depth` parameter must be a positive integer, got {max_depth}.',
            tag=_ValidatorsErrorTag.INVALID_NAME_PARAM_VALUE,
        )

    if not isinstance(item, Set):
        raise SimpleBenchTypeError(
            f'{name} parameter is not a Set. Got a {type(item).__name__} instead.',
            tag=_ValidatorsErrorTag.INVALID_CORE_MAPPING_PARAM_VALUE,
        )
    return _internal_validate_core_data_set(
        item=item, is_immutable=False, name=name, max_depth=max_depth, depth=0, parents=set()
    )


def _internal_validate_core_data(
    *,
    item: CoreDataTypes,
    is_immutable: bool,
    name: str,
    depth: int,
    max_depth: int = DEFAULT_MAX_CORE_DATA_DEPTH,
    parents: set[int],
) -> ImmutableCoreDataTypes:
    """Recursively validate a CoreDataTypes item.

    Helper function that performs a recursive validation of the data/structure
    and conversion to immutable types.

    :param CoreDataTypes item: The item to validate.
    :param str name: The name of the mapping (used in error messages).
    :param bool is_immutable: Whether to check for immutability.
    :param int depth: The current depth in the data tree.
    :param int max_depth: The maximum allowed depth for nested structures.
    :param set[int] parents: Set of ids of previously seen items to detect cycles.
    :return ImmutableCoreDataTypes: The validated immutable item.
    :raises SimpleBenchTypeError: If the tree structure contains invalid types.
    :raises SimpleBenchValueError: If any dictionary key is a blank or empty string or if a
        cyclic reference is detected.
    """
    item_id = id(item)
    if item_id in parents:
        raise SimpleBenchValueError(
            f'Cyclic reference detected in `{name}`.', tag=_ValidatorsErrorTag.CYCLIC_REFERENCE_DETECTED
        )

    # bytes are not allowed in CoreDataTypes even though they are Sequences
    if isinstance(item, bytes):
        raise SimpleBenchTypeError(
            f'Invalid data type for element in `{name}` mapping: bytes. '
            f'Allowed types are Mapping, Sequence, Set, str, int, float, complex, bool, and None.',
            tag=_ValidatorsErrorTag.INVALID_CORE_MAPPING_PARAM_VALUE,
        )

    if isinstance(item, (str, int, float, complex, bool)) or item is None:
        # No 'parents' addition for immutable primitive types
        # because they cannot form cyclic references and can share ids.
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

    # Sets before Sequences because Sets are also Sequences
    elif isinstance(item, Set):
        results = _internal_validate_core_data_set(
            item=item, is_immutable=is_immutable, name=name, depth=depth, max_depth=max_depth, parents=parents
        )
        return results

    elif isinstance(item, Mapping):
        results = _internal_validate_core_data_mapping(
            item=item, is_immutable=is_immutable, name=name, depth=depth, max_depth=max_depth, parents=parents
        )
        return results

    elif isinstance(item, Sequence) and not isinstance(item, (str, bytes)):
        results = _internal_validate_core_data_sequence(
            item=item, is_immutable=is_immutable, name=name, depth=depth, max_depth=max_depth, parents=parents
        )
        return results

    raise SimpleBenchTypeError(
        f'Invalid data type for element in `{name}` mapping: {type(item).__name__}. '
        f'Allowed types are Mapping, Sequence, Set, str, int, float, bool, and None.',
        tag=_ValidatorsErrorTag.INVALID_CORE_MAPPING_PARAM_VALUE,
    )


def validate_core_data(
    item: CoreDataTypes, name: str, *, max_depth: int = DEFAULT_MAX_CORE_DATA_DEPTH
) -> ImmutableCoreDataTypes:
    """Validate a CoreDataTypes item.

    The `value` parameter must be a `CoreDataTypes` conformant data/structure.
    It can have arbitrary structure but must conform with the :class:`CoreDataTypes` contract.
    The entire data tree is validated recursively to ensure all elements conform to the
    :class:`CoreDataTypes` definition.
    It cannot contain cyclic references and must not exceed the specified maximum depth for nested structures.
    The validated data/structure is returned as an immutable `ImmutableCoreDataTypes`.

    This has the result of ensuring that the returned data/structure is both serializable and immutable
    and transforms all mutable structures (like lists and dicts) into their immutable counterparts
    (like tuples and MappingProxyType). This includes classes that are subclasses of the allowed
     mutable and immutable types.

    .. note:: This is a composable validator without dependencies on other public validators.
        This makes it safe to use in other validators without any risk of creating circular
        dependencies.

    :param CoreDataTypes value: The data/structure to validate.
    :param str name: The name of the mapping (used in error messages).
    :param int max_depth: The maximum allowed depth for nested structures. (optional, keyword-only, defaults to 10).
    :return ImmutableCoreDataTypes: An immutable validated data/structure.
    :raises SimpleBenchTypeError: If the tree structure contains invalid types.
    :raises SimpleBenchValueError: If any dictionary key is a blank or empty string or if a
        cyclic reference is detected.
    """
    return _internal_validate_core_data(
        item=item, is_immutable=False, name=name, depth=0, max_depth=max_depth, parents=set()
    )


def validate_immutable_core_data(
    item: ImmutableCoreDataTypes, name: str, *, max_depth: int = DEFAULT_MAX_CORE_DATA_DEPTH
) -> ImmutableCoreDataTypes:
    """Validate an ImmutableCoreDataTypes item.

    If it **IS** a valid ImmutableCoreDataTypes instance, returns the original object unchanged
    to conserve memory and equality.

    The `value` parameter must be an `ImmutableCoreDataTypes` conformant data/structure.
    It can have arbitrary structure but must conform with the :class:`ImmutableCoreDataTypes` contract.
    The entire data tree is validated recursively to ensure all elements conform to the
    :class:`ImmutableCoreDataTypes` definition.
    It cannot contain cyclic references and must not exceed the specified maximum depth for nested structures.
    The validated data/structure is returned as an immutable `ImmutableCoreDataTypes`.

    This has the result of ensuring that the returned data/structure is both serializable and immutable
    and transforms all mutable structures (like lists and dicts) into their immutable counterparts
    (like tuples and MappingProxyType). This includes classes that are subclasses of the allowed
     mutable and immutable types.

    .. note:: This is a composable validator without dependencies on other public validators.
        This makes it safe to use in other validators without any risk of creating circular
        dependencies.

    :param ImmutableCoreDataTypes value: The data/structure to validate.
    :param str name: The name of the mapping (used in error messages).
    :param int max_depth: The maximum allowed depth for nested structures. (optional, keyword-only, defaults to 10).
    :return ImmutableCoreDataTypes: An immutable validated data/structure.
    :raises SimpleBenchTypeError: If the tree structure contains invalid types.
    :raises SimpleBenchValueError: If any dictionary key is a blank or empty string or if a
        cyclic reference is detected.
    """
    _internal_validate_core_data(item=item, is_immutable=True, name=name, depth=0, max_depth=max_depth, parents=set())
    return item


def validate_immutable_core_data_mapping(
    item: ImmutableCoreDataMappingType, name: str, *, max_depth: int = DEFAULT_MAX_CORE_DATA_DEPTH
) -> ImmutableCoreDataMappingType:
    """Validate an ImmutableCoreDataTypes mapping.

    If it **IS** a valid ImmutableCoreDataMappingType instance, returns the original object unchanged
    to conserve memory and equality.

    The `value` parameter must be a `MappingProxyType[str, ImmutableCoreDataTypes]` conformant mapping.
    It can have arbitrary keys and values but must conform with the :class:`ImmutableCoreDataTypes` contract,
    and must use strings as keys. The entire mapping tree is validated recursively to ensure all
    elements conform to the :class:`ImmutableCoreDataTypes` definition.

    It cannot contain cyclic references and must not exceed the specified maximum depth for nested structures.

    .. note:: This is a composable validator without dependencies on other public validators.
        This makes it safe to use in other validators without any risk of creating circular
        dependencies.

    :param ImmutableCoreDataMappingType value: The data mapping to validate.
    :param str name: The name of the mapping (used in error messages).
    :param int max_depth: The maximum allowed depth for nested structures. (optional, keyword-only, defaults to 10).
    :return ImmutableCoreDataMappingType: The original data mapping object.
    :raises SimpleBenchTypeError: If the tree structure contains invalid types.
    :raises SimpleBenchValueError: If any dictionary key is a blank or empty string or
        if a cyclic reference is detected.
    """
    _internal_validate_core_data_mapping(
        item=item, is_immutable=True, name=name, max_depth=max_depth, depth=0, parents=set()
    )
    return item


def validate_immutable_core_data_sequence(
    item: ImmutableCoreDataSequenceType, name: str, *, max_depth: int = DEFAULT_MAX_CORE_DATA_DEPTH
) -> ImmutableCoreDataSequenceType:
    """Validate an ImmutableCoreDataTypes sequence.

    If it **IS** a valid ImmutableCoreDataSequenceType instance, returns the original object unchanged
    to conserve memory and equality.

    The `value` parameter must be a `tuple[ImmutableCoreDataTypes, ...]` conformant sequence.

    It can have arbitrary values but must conform with the :class:`ImmutableCoreDataTypes` contract.

    The entire sequence tree is validated recursively to ensure all elements conform to the
    :class:`ImmutableCoreDataTypes` definition.

    It cannot contain cyclic references and must not exceed the specified maximum depth for nested structures.

    .. note:: This is a composable validator without dependencies on other public validators.
        This makes it safe to use in other validators without any risk of creating circular
        dependencies.

    :param ImmutableCoreDataSequenceType value: The data sequence to validate.
    :param str name: The name of the mapping (used in error messages).
    :param int max_depth: The maximum allowed depth for nested structures. (optional, keyword-only, defaults to 10).
    :return ImmutableCoreDataSequenceType: The original data sequence object.
    :raises SimpleBenchTypeError: If the tree structure contains invalid types.
    :raises SimpleBenchValueError: If a cyclic reference is detected.
    """
    _internal_validate_core_data_sequence(
        item=item, is_immutable=True, name=name, max_depth=max_depth, depth=0, parents=set()
    )
    return item


def validate_immutable_core_data_set(
    item: ImmutableCoreDataSetType, name: str, *, max_depth: int = DEFAULT_MAX_CORE_DATA_DEPTH
) -> ImmutableCoreDataSetType:
    """Validate an ImmutableCoreDataTypes set.

    If it **IS** a valid ImmutableCoreDataSetType instance, returns the original object unchanged
    to conserve memory and equality.

    The `item` parameter must be a `frozenset[ImmutableCoreDataTypes]` conformant set.

    It can have arbitrary values but must conform with the :class:`ImmutableCoreDataTypes` contract.
    The entire set tree is validated recursively to ensure all elements conform to the
    :class:`ImmutableCoreDataTypes` definition.

    It cannot contain cyclic references and must not exceed the specified maximum depth for nested structures.

    .. note:: This is a composable validator without dependencies on other public validators.
        This makes it safe to use in other validators without any risk of creating circular
        dependencies.

    :param ImmutableCoreDataSetType value: The data set to validate.
    :param str name: The name of the mapping (used in error messages).
    :param int max_depth: The maximum allowed depth for nested structures. (optional, keyword-only, defaults to 10).
    :return ImmutableCoreDataSetType: The original data set object.
    :raises SimpleBenchTypeError: If the tree structure contains invalid types.
    :raises SimpleBenchValueError: If a cyclic reference is detected.
    """
    _internal_validate_core_data_set(
        item=item, is_immutable=True, name=name, max_depth=max_depth, depth=0, parents=set()
    )
    return item


_MAX_CACHE_SIZE = 1024
"""Maximum size for the immutable core data type cache."""

_IMMUTABLE_ITEMS_CACHE: OrderedDict[int, ImmutableCoreDataTypes] = OrderedDict()
"""Cache for immutable core data type references to optimize repeated checks."""


class _NotInCache:
    """Sentinel class representing a value not found in the cache."""


_NOT_IN_CACHE: Final[_NotInCache] = _NotInCache()

_CORE_PRIMITIVES_SET: Final[set[type]] = {str, int, float, bool, complex, type(None)}
"""Set of core data primitive types for quick membership testing."""


def is_core_data_primitive(value: Any) -> TypeGuard[str | int | float | bool | complex | None]:
    """Check if a value is a core data primitive type.

    The allowed primitive types are str, int, float, bool, complex, and None.

    All core primitive types are immutable and serializable.

    :param object value: The value to check.
    :return bool: True if the value is a core data primitive type, False otherwise.
    """
    return isinstance(value, (str, int, float, bool, complex)) or value is None


def is_core_data_primitive_type(value_type: Any) -> TypeGuard[type[str | int | float | bool | complex | None]]:
    """Check if a type is a core data primitive type.

    The allowed primitive types are str, int, float, bool, complex, and NoneType.

    All core primitive types are immutable and serializable.

    :param object value_type: The type to check.
    :return bool: True if the type is a core data primitive type, False otherwise.
    """
    return value_type in _CORE_PRIMITIVES_SET


def is_core_data(value: CoreDataTypes, *, max_depth=DEFAULT_MAX_CORE_DATA_DEPTH) -> TypeGuard[CoreDataTypes]:
    """Check if a value is a valid CoreDataTypes instance.

    :param object value: The value to check.
    :param int max_depth: Maximum depth to check nested structures.
    :return bool: True if the value is a valid CoreDataTypes instance, False otherwise.
    """
    try:
        validate_core_data(value, 'CoreData is checking', max_depth=max_depth)
        return True
    except (ValueError, TypeError):
        return False


def is_core_data_mapping(
    value: CoreDataMappingType, *, max_depth=DEFAULT_MAX_CORE_DATA_DEPTH
) -> TypeGuard[CoreDataMappingType]:
    """Check if a value is a valid CoreDataMappingType instance.

    :param object value: The value to check.
    :param int max_depth: Maximum depth to check nested structures.
    :return bool: True if the value is a valid CoreDataMappingType instance, False otherwise.
    """
    try:
        validate_core_data_mapping(value, 'CoreDataMapping is checking', max_depth=max_depth)
        return True
    except (ValueError, TypeError):
        return False


def is_core_data_sequence(
    value: CoreDataSequenceType, *, max_depth=DEFAULT_MAX_CORE_DATA_DEPTH
) -> TypeGuard[CoreDataSequenceType]:
    """Check if a value is a valid CoreDataSequenceType instance.

    :param object value: The value to check.
    :param int max_depth: Maximum depth to check nested structures.
    :return bool: True if the value is a valid CoreDataSequenceType instance, False otherwise.
    """
    try:
        validate_core_data_sequence(value, 'CoreDataSequence is checking', max_depth=max_depth)
        return True
    except (ValueError, TypeError):
        return False


def is_core_data_set(value: CoreDataSetType, *, max_depth=DEFAULT_MAX_CORE_DATA_DEPTH) -> TypeGuard[CoreDataSetType]:
    """Check if a value is a valid CoreDataSetType instance.

    :param object value: The value to check.
    :param int max_depth: Maximum depth to check nested structures.
    :return bool: True if the value is a valid CoreDataSetType instance, False otherwise.
    """
    try:
        validate_core_data_set(value, 'CoreDataSet is checking', max_depth=max_depth)
        return True
    except (ValueError, TypeError):
        return False


def is_immutable_core_data(value: Any, *, max_depth=DEFAULT_MAX_CORE_DATA_DEPTH) -> TypeGuard[ImmutableCoreDataTypes]:
    """Check if a value is a valid ImmutableCoreDataTypes instance.

    :param object value: The value to check.
    :param int max_depth: Maximum depth to check nested structures.
    :return bool: True if the value is a valid ImmutableCoreDataTypes instance, False otherwise.
    """
    if value is _in_immutables_cache(value):
        return True

    try:
        validate_immutable_core_data(value, 'ImmutableCoreData is checking', max_depth=max_depth)
        return True
    except (ValueError, TypeError):
        return False


def is_immutable_core_data_mapping(
    value: ImmutableCoreDataMappingType, *, max_depth=DEFAULT_MAX_CORE_DATA_DEPTH
) -> TypeGuard[ImmutableCoreDataMappingType]:
    """Check if a value is a valid ImmutableCoreDataMappingType instance.

    :param object value: The value to check.
    :param int max_depth: Maximum depth to check nested structures.
    :return bool: True if the value is a valid ImmutableCoreDataMappingType instance, False otherwise.
    """
    if value is _in_immutables_cache(value) and isinstance(value, MappingProxyType):
        return True
    try:
        validate_immutable_core_data_mapping(value, 'ImmutableCoreDataMapping is checking', max_depth=max_depth)
        return True
    except (ValueError, TypeError):
        return False


def is_immutable_core_data_sequence(
    value: ImmutableCoreDataSequenceType, *, max_depth=DEFAULT_MAX_CORE_DATA_DEPTH
) -> TypeGuard[ImmutableCoreDataSequenceType]:
    """Check if a value is a valid ImmutableCoreDataSequenceType instance.

    :param object value: The value to check.
    :param int max_depth: Maximum depth to check nested structures.
    :return bool: True if the value is a valid ImmutableCoreDataSequenceType instance, False otherwise.
    """
    if value is _in_immutables_cache(value) and isinstance(value, tuple):
        return True
    try:
        validate_immutable_core_data_sequence(value, 'ImmutableCoreDataSequence is checking', max_depth=max_depth)
        return True
    except (ValueError, TypeError):
        return False


def is_immutable_core_data_set(
    value: ImmutableCoreDataSetType, *, max_depth=DEFAULT_MAX_CORE_DATA_DEPTH
) -> TypeGuard[ImmutableCoreDataSetType]:
    """Check if a value is a valid ImmutableCoreDataSetType instance.

    :param object value: The value to check.
    :param int max_depth: Maximum depth to check nested structures.
    :return bool: True if the value is a valid ImmutableCoreDataSetType instance, False otherwise.
    """
    if value is _in_immutables_cache(value) and isinstance(value, frozenset):
        return True

    try:
        validate_immutable_core_data_set(value, 'ImmutableCoreDataSet is checking', max_depth=max_depth)
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

    The smallest allowed size is 100.

    Cache trimming is performed within a thread-safe lock.

    :param int size: The maximum size of the cache.
    :raises SimpleBenchTypeError: If size is not an integer.
    :raises SimpleBenchValueError: If size is less than 100.
    """
    if not isinstance(size, int):
        raise SimpleBenchTypeError('Cache size must be an integer.', tag=_ValidatorsErrorTag.INVALID_CACHE_TYPE)

    if size < 100:  # Minimum size to ensure effective caching
        raise SimpleBenchValueError('Cache size must be at least 100', tag=_ValidatorsErrorTag.INVALID_CACHE_SIZE)

    with _CACHE_LOCK:
        target_size = int(size * 0.75)
        while len(_IMMUTABLE_ITEMS_CACHE) > target_size:
            _IMMUTABLE_ITEMS_CACHE.popitem(last=False)
