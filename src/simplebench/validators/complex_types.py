"""Validators for complex data types used in SimpleBench."""
import math
from collections.abc import Mapping
from types import MappingProxyType
from typing import Sequence, Set

from simplebench.exceptions import SimpleBenchTypeError, SimpleBenchValueError
from simplebench.types import CoreDataTypes, ImmutableCoreDataTypes
from simplebench.validators import _ValidatorsErrorTag

_DEFAULT_MAX_DEPTH: int = 10


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
        return f"_PendingItem(item={self.item}, depth={self.depth}), item id={id(self.item)})"



def _internal_validate_core_data_mapping(            *,
            item: Mapping[str, CoreDataTypes],
            name: str,
            max_depth: int,
            depth: int,
            previously_seen: set[int]) -> MappingProxyType[str, ImmutableCoreDataTypes]:
    """Internal helper to validate a CoreDataTypes mapping.

    :param Mapping[str, CoreDataTypes] value: The data mapping to validate.
    :param str name: The name of the mapping (used in error messages).
    :param int max_depth: The maximum allowed depth for nested structures. (optional, keyword-only, defaults to 10).
    :param int depth: The current depth in the data tree.
    :param set[int] previously_seen: Set of ids of previously seen items to detect cycles
    :return MappingProxyType[str, ImmutableCoreDataTypes]: An immutable validated data mapping.
    :raises SimpleBenchTypeError: If the tree structure contains invalid types.
    :raises SimpleBenchValueError: If any dictionary key is a blank or empty string or
        if a cyclic reference is detected.
    """
    # we don't need to validate that `item` type is Mapping, `name`, `max_depth`,
    # or `previously_seen` here as they are validated before this is called.
    if depth > max_depth:
        raise SimpleBenchValueError(
            f"The `{name}` mapping is too deeply nested (maximum depth is {max_depth}).",
            tag=_ValidatorsErrorTag.INVALID_CORE_MAPPING_PARAM_VALUE)

    item_id = id(item)
    if item_id in previously_seen:
        raise SimpleBenchValueError(
            f"Cyclic reference detected in `{name}`.",
            tag=_ValidatorsErrorTag.INVALID_CORE_MAPPING_PARAM_VALUE)
    previously_seen.add(item_id)

    validated_dict: dict[str, ImmutableCoreDataTypes] = {}
    for key, element in item.items():
        if not isinstance(key, str):
            raise SimpleBenchTypeError(
                f"All keys in the `{name}` mapping must be strings. "
                f"Invalid key: type {type(key).__name__}",
                tag=_ValidatorsErrorTag.INVALID_KEY_TYPE)
        if key.strip() == '':
            raise SimpleBenchValueError(
                f"All keys in the `{name}` mapping must be non-blank, non-empty strings. "
                f"Invalid key: '{key}'",
                tag=_ValidatorsErrorTag.INVALID_KEY_VALUE)
        validated_dict_element: ImmutableCoreDataTypes = _internal_validate_core_data(
            item=element,
            name=name,
            depth=depth + 1,
            max_depth=max_depth,
            previously_seen=previously_seen)
        validated_dict[key] = validated_dict_element
    return MappingProxyType(validated_dict)

def validate_core_data_mapping(
            item: Mapping[str, CoreDataTypes],
            name: str,
            *,
            max_depth: int = _DEFAULT_MAX_DEPTH) -> MappingProxyType[str, ImmutableCoreDataTypes]:
    """Validate a CoreDataTypes mapping.

    The `value` parameter must be a `Mapping[str, CoreDataTypes]` conformant mapping.

    It can have arbitrary keys and values but must conform with the :class:`CoreDataTypes` contract,
    and must use strings as keys. The entire mapping tree is validated recursively to ensure all
    elements conform to the :class:`CoreDataTypes` definition.

    It cannot contain cyclic references and must not exceed the specified maximum depth for nested structures.

    The validated mapping is returned as an immutable
    :class:`MappingProxyType[str, ImmutableCoreDataTypes]`.

    This has the result of ensuring that the returned mapping is both serializable and immutable
    and transforms all mutable structures (like lists and dicts) into their immutable counterparts
    (like tuples and MappingProxyType). This includes classes that are subclasses of the allowed
     mutable and immutable types.

    .. note:: This is a composable validator without dependencies on other public validators.
        This makes it safe to use in other validators without any risk of creating circular
        dependencies.

    :param Mapping[str, CoreDataTypes] value: The data mapping to validate.
    :param str name: The name of the mapping (used in error messages).
    :param int max_depth: The maximum allowed depth for nested structures. (optional, keyword-only, defaults to 10).
    :return MappingProxyType[str, ImmutableCoreDataTypes]: An immutable validated data mapping.
    :raises SimpleBenchTypeError: If the tree structure contains invalid types.
    :raises SimpleBenchValueError: If any dictionary key is a blank or empty string or
        if a cyclic reference is detected.
    """
    if not isinstance(name, str):
        raise SimpleBenchTypeError(
            f"The `name` parameter must be a string, got {type(name).__name__}.",
            tag=_ValidatorsErrorTag.INVALID_NAME_PARAM_TYPE)

    if name.strip() == '':
        raise SimpleBenchValueError(
            "The `name` parameter must be a non-blank, non-empty string.",
            tag=_ValidatorsErrorTag.INVALID_NAME_PARAM_VALUE)

    if not isinstance(item, Mapping):
        raise SimpleBenchTypeError(
            f"{name} parameter is not a Mapping. Got a {type(item).__name__} instead.",
            tag=_ValidatorsErrorTag.INVALID_CORE_MAPPING_PARAM_VALUE)

    if not isinstance(max_depth, int):
        raise SimpleBenchTypeError(
            f"The `max_depth` parameter must be an integer, got {type(max_depth).__name__}.",
            tag=_ValidatorsErrorTag.INVALID_NAME_PARAM_TYPE)

    if max_depth <= 0:
        raise SimpleBenchValueError(
            f"The `max_depth` parameter must be a positive integer, got {max_depth}.",
            tag=_ValidatorsErrorTag.INVALID_NAME_PARAM_VALUE)

    return _internal_validate_core_data_mapping(
        item=item,
        name=name,
        max_depth=max_depth,
        depth=0,
        previously_seen=set())

def _internal_validate_core_data_sequence(
            *,
            item: Sequence[CoreDataTypes],
            name: str,
            depth: int,
            max_depth: int,
            previously_seen: set[int]) -> tuple[ImmutableCoreDataTypes, ...]:
    """Recursively validate a CoreDataTypes sequence.

    Helper function for `validate_core_data_sequence` that performs the recursive
    validation of a sequence data structure and conversion to immutable types.

    :param Sequence[CoreDataTypes] item: The item to validate.
    :param str name: The name of the mapping (used in error messages).
    :param int depth: The current depth in the data tree.
    :param int max_depth: The maximum allowed depth for nested structures.
    :param set[int] previously_seen: Set of ids of previously seen items to detect cycles.
    :return ImmutableCoreDataTypes: The validated immutable item.
    :raises SimpleBenchTypeError: If the tree structure contains invalid types.
    :raises SimpleBenchValueError: If any dictionary key is a blank or empty string or if a
        cyclic reference is detected.
    """
    # we don't need to validate that `item` type is a Sequence, `name`, `max_depth`, or `previously_seen`
    # here as they are validated before this is called.
    if depth > max_depth:
        raise SimpleBenchValueError(
            f"The `{name}` mapping is too deeply nested (maximum depth is {max_depth}).",
            tag=_ValidatorsErrorTag.INVALID_CORE_MAPPING_PARAM_VALUE)

    item_id = id(item)
    previously_seen.add(item_id)

    validated_elements: tuple[ImmutableCoreDataTypes, ...] = tuple(
        _internal_validate_core_data(
            item=element,
            name=name,
            depth=depth + 1,
            max_depth=max_depth,
            previously_seen=previously_seen) for element in item)
    return validated_elements

def validate_core_data_sequence(
        item: Sequence[CoreDataTypes],
        name: str,
        *,
        max_depth: int = _DEFAULT_MAX_DEPTH) -> tuple[ImmutableCoreDataTypes, ...]:
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
    :param Sequence[CoreDataTypes] value: The data sequence to validate.
    :param str name: The name of the mapping (used in error messages).
    :param int max_depth: The maximum allowed depth for nested structures. (optional, keyword-only, defaults to 10).
    :return tuple[ImmutableCoreDataTypes, ...]: An immutable validated data sequence.
    :raises SimpleBenchTypeError: If the tree structure contains invalid types.
    :raises SimpleBenchValueError: If a cyclic reference is detected.
    """
    if not isinstance(name, str):
        raise SimpleBenchTypeError(
            f"The `name` parameter must be a string, got {type(name).__name__}.",
            tag=_ValidatorsErrorTag.INVALID_NAME_PARAM_TYPE)
    if name.strip() == '':
        raise SimpleBenchValueError(
            "The `name` parameter must be a non-blank, non-empty string.",
            tag=_ValidatorsErrorTag.INVALID_NAME_PARAM_VALUE)
    if not isinstance(max_depth, int):
        raise SimpleBenchTypeError(
            f"The `max_depth` parameter must be an integer, got {type(max_depth).__name__}.",
            tag=_ValidatorsErrorTag.INVALID_NAME_PARAM_TYPE)
    if max_depth <= 0:
        raise SimpleBenchValueError(
            f"The `max_depth` parameter must be a positive integer, got {max_depth}.",
            tag=_ValidatorsErrorTag.INVALID_NAME_PARAM_VALUE)
    if not isinstance(item, Sequence) or isinstance(item, (str, bytes)):
        raise SimpleBenchTypeError(
            f"{name} parameter is not a Sequence. Got a {type(item).__name__} instead.",
            tag=_ValidatorsErrorTag.INVALID_CORE_MAPPING_PARAM_VALUE)
    return _internal_validate_core_data_sequence(
        item=item,
        name=name,
        max_depth=max_depth,
        depth=0,
        previously_seen=set())

def _internal_validate_core_data_set(
            *,
            item: Set[CoreDataTypes],
            name: str,
            depth: int,
            max_depth: int,
            previously_seen: set[int]) -> frozenset[ImmutableCoreDataTypes]:
    """Recursively validate a CoreDataTypes set.

    Helper function for `validate_core_data_set` that performs the recursive
    validation of a set data structure and conversion to immutable types.

    :param Set[CoreDataTypes] item: The item to validate.
    :param str name: The name of the mapping (used in error messages).
    :param int depth: The current depth in the data tree.
    :param int max_depth: The maximum allowed depth for nested structures.
    :param set[int] previously_seen: Set of ids of previously seen items to detect cycles.
    :return ImmutableCoreDataTypes: The validated immutable item.
    :raises SimpleBenchTypeError: If the tree structure contains invalid types.
    :raises SimpleBenchValueError: If any dictionary key is a blank or empty string or if a
        cyclic reference is detected.
    """
    # we don't need to validate that `item` type is a Set, `name`, `max_depth`, or `previously_seen`
    # here as they are validated before this is called.
    if depth > max_depth:
        raise SimpleBenchValueError(
            f"The `{name}` mapping is too deeply nested (maximum depth is {max_depth}).",
            tag=_ValidatorsErrorTag.INVALID_CORE_MAPPING_PARAM_VALUE)

    item_id = id(item)
    previously_seen.add(item_id)

    validated_elements: frozenset[ImmutableCoreDataTypes] = frozenset(
        _internal_validate_core_data(
            item=element,
            name=name,
            depth=depth + 1,
            max_depth=max_depth,
            previously_seen=previously_seen) for element in item)
    return validated_elements

def validate_core_data_set(
            item: Set[CoreDataTypes],
            name: str,
            *,
            max_depth: int = _DEFAULT_MAX_DEPTH) -> frozenset[ImmutableCoreDataTypes]:
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

    :param Set[CoreDataTypes] value: The data set to validate.
    :param str name: The name of the mapping (used in error messages).
    :param int max_depth: The maximum allowed depth for nested structures. (optional, keyword-only, defaults to 10).
    :return frozenset[ImmutableCoreDataTypes]: An immutable validated data set.
    :raises SimpleBenchTypeError: If the tree structure contains invalid types.
    :raises SimpleBenchValueError: If a cyclic reference is detected.
    """
    if not isinstance(name, str):
        raise SimpleBenchTypeError(
            f"The `name` parameter must be a string, got {type(name).__name__}.",
            tag=_ValidatorsErrorTag.INVALID_NAME_PARAM_TYPE)

    if name.strip() == '':
        raise SimpleBenchValueError(
            "The `name` parameter must be a non-blank, non-empty string.",
            tag=_ValidatorsErrorTag.INVALID_NAME_PARAM_VALUE)

    if not isinstance(max_depth, int):
        raise SimpleBenchTypeError(
            f"The `max_depth` parameter must be an integer, got {type(max_depth).__name__}.",
            tag=_ValidatorsErrorTag.INVALID_NAME_PARAM_TYPE)

    if max_depth <= 0:
        raise SimpleBenchValueError(
            f"The `max_depth` parameter must be a positive integer, got {max_depth}.",
            tag=_ValidatorsErrorTag.INVALID_NAME_PARAM_VALUE)

    if not isinstance(item, Set):
        raise SimpleBenchTypeError(
            f"{name} parameter is not a Set. Got a {type(item).__name__} instead.",
            tag=_ValidatorsErrorTag.INVALID_CORE_MAPPING_PARAM_VALUE)
    return _internal_validate_core_data_set(
        item=item,
        name=name,
        max_depth=max_depth,
        depth=0,
        previously_seen=set())

def _internal_validate_core_data(
            *,
            item: CoreDataTypes,
            name: str,
            depth: int,
            max_depth: int = _DEFAULT_MAX_DEPTH,
            previously_seen: set[int]) -> ImmutableCoreDataTypes:
    """Recursively validate a CoreDataTypes item.

    Helper function that performs a recursive validation of the data/structure
    and conversion to immutable types.

    :param CoreDataTypes item: The item to validate.
    :param str name: The name of the mapping (used in error messages).
    :param int depth: The current depth in the data tree.
    :param int max_depth: The maximum allowed depth for nested structures.
    :param set[int] previously_seen: Set of ids of previously seen items to detect cycles.
    :return ImmutableCoreDataTypes: The validated immutable item.
    :raises SimpleBenchTypeError: If the tree structure contains invalid types.
    :raises SimpleBenchValueError: If any dictionary key is a blank or empty string or if a
        cyclic reference is detected.
    """
    if isinstance(item, (str, int, float, bool)) or item is None:
        # No 'previously_seen' addition for immutable primitive types
        # because they cannot form cyclic references and can share ids.
        # Check for non-finite floats (NaN, Infinity)
        if isinstance(item, float):
            if math.isnan(item) or math.isinf(item):
                raise SimpleBenchValueError(
                    f"Float values in `{name}` cannot be NaN or Infinity.",
                    tag=_ValidatorsErrorTag.INVALID_CORE_MAPPING_PARAM_VALUE)
        return item

    elif isinstance(item, Sequence) and not isinstance(item, (str, bytes)):
        return _internal_validate_core_data_sequence(
            item=item,
            name=name,
            depth=depth,
            max_depth=max_depth,
            previously_seen=previously_seen)

    elif isinstance(item, Mapping):
        return _internal_validate_core_data_mapping(
            item=item,
            name=name,
            depth=depth,
            max_depth=max_depth,
            previously_seen=previously_seen)

    elif isinstance(item, Set):
        return _internal_validate_core_data_set(
            item=item,
            name=name,
            depth=depth,
            max_depth=max_depth,
            previously_seen=previously_seen)

    raise SimpleBenchTypeError(
        f"Invalid data type for element in `{name}` mapping: {type(item).__name__}. "
        f"Allowed types are Mapping, Sequence, Set, str, int, float, bool, and None.",
        tag=_ValidatorsErrorTag.INVALID_CORE_MAPPING_PARAM_VALUE)

def validate_core_data(
        item: CoreDataTypes,
        name: str,
        *,
        max_depth: int = _DEFAULT_MAX_DEPTH) -> ImmutableCoreDataTypes:
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
        item=item,
        name=name,
        depth=0,
        max_depth=max_depth,
        previously_seen=set())
