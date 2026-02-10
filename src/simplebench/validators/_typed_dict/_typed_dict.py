"""Validation functions for TypedDicts

Follows spec at https://typing.python.org/en/latest/spec/typeddict.html
except it allows non-dict Mappings that conform to the structure of the
TypedDict subclass to be recognized as mimics.
"""

from collections.abc import Mapping, Sequence, Set
from types import UnionType
from typing import (
    Any,
    Optional,
    TypedDict,
    TypeGuard,
    TypeVar,
    Union,
    cast,
    get_args,
    get_origin,
    is_typeddict,
)

from simplebench._log import _log
from simplebench.base._typed_dict_key_info import TypedDictKeyInfo
from simplebench.defaults import DEFAULT_MAX_CORE_DATA_DEPTH
from simplebench.exceptions import SimpleBenchTypeError
from simplebench.simplebench_types import CoreDataMapping, Never
from simplebench.validators._cache import ValidationCache
from simplebench.validators.core_data_types import is_core_data_primitive, is_core_data_primitive_type

from . import _validate
from ._error_tags import _TypedDictErrorTag

_CACHE = ValidationCache(min_cache_size=100, max_cache_size=16384)

T = TypeVar('T', bound=TypedDict)  # type: ignore[invalidTypeForm,valid-type]


def is_typed_dict_mimic(data: Mapping[str, Any], td_cls: type[T]) -> TypeGuard[T]:
    """TypeGuard function. Check if a mapping conforms to a TypedDict subclass.

    It acts as a structural isinstance() check for mappings against the TypedDict subclass.

    It comprehensively checks that the mapping conforms to the structure defined
    by the TypedDict subclass and recursively checks nested TypedDicts.

    Static type checkers can use this to narrow types accordingly and will understand
    that after a successful check the mapping conforms to the TypedDict structure.

    A Mapping[str, Any] is checked against the structure defined by the TypedDict subclass.

    It validates that:
    - All required keys are present and of the correct type.
    - All optional keys, if present, are of the correct type.
    - No extra keys are present.

    It **DOES NOT** require an actual instance of TypedDict and performs
    a structural check against the TypedDict subclass definition for a
    generic Mapping[str, Any]. This allows validating arbitrary dictionaries
    against the TypedDict structure without needing to create TypedDict instances.

    For performance, it uses a size-limited cache to store previous validation results.

    Also, if subtrees of the mapping have already been validated and cached,
    it reuses those cached results to avoid redundant validation.

    If subtrees are newly encountered, they are validated and their results
    are added to the cache for future reuse. Only fully immutable core data type
    structures are cached positively (with validity of `True`) to ensure safety.

    Cyclic references are detected and raise an error to prevent infinite recursion.

    :param Mapping[str, Any] data: The dictionary to check.
    :param type[TypedDict] td_cls: The TypedDict subclass type to check against.
    :return bool: True if the dictionary conforms to the TypedDict subclass, False otherwise.
    """
    # fast path for clearly non-conforming types to avoid unnecessary validation overhead
    if not isinstance(data, Mapping) or not isinstance(td_cls, type) or not is_typeddict(td_cls):
        _log.debug(f'Fast path check failed for data: {data!r} and TypedDict: {td_cls!r}')
        return False

    try:
        valid, _ = _validate_and_check_immutability_of_mimic(data, td_cls)
        _log.debug(f'Validation result for data: {data!r} against TypedDict: {td_cls.__name__}: valid={valid}')
        return valid
    except SimpleBenchTypeError as e:
        _log.debug(f'Validation error during TypedDict mimic check for data: {data!r} '
                   f'against TypedDict: {td_cls.__name__}: {e} (tag={e.tag_code})')
        return False


def _validate_and_check_immutability_of_mimic(
    data: Mapping[str, Any],
    td_cls: type[TypedDict],  # type: ignore
    parents: set[int] | None = None,
    raise_on_error: bool = True,
) -> tuple[bool, bool]:
    """Validate a mapping against a TypedDict subclass
    and check if it consists only of fully immutable core data types.

    It recursively checks the structure and types of the mapping against the TypedDict subclass
    and returns whether it conforms to the TypedDict subclass and whether the structure
    is fully immutable core data types.

    Cyclic references are detected and raise an error to prevent infinite recursion.

    :param Mapping[str, Any] data: The dictionary to check.
    :param type[TypedDict] td_cls: The TypedDict subclass type to check against.
    :param set[type] | None parents: Set of parent data nodes in the recursion stack to detect cycles.
    :param bool raise_on_error: If True, raise an error on validation failure.
    :return tuple[bool, bool]: A tuple where the first element indicates if the dictionary
        conforms to the TypedDict subclass, and the second element indicates if the
        data consists only of fully immutable core data types.
    :raise SimpleBenchTypeError: If there is a validation error and raise_on_error is True.
    """
    _log.debug(f'Validating TypedDict mimic for data: {data} against TypedDict: {td_cls.__name__}')
    cached_state: bool | None = _CACHE.valid_in_cache(td_cls, data)
    if cached_state is not None:
        # Cached results are always immutable core data types and thus safe to reuse.
        # Mutable structures can be validated but they are not cached because their
        # state may change after validation.
        return (cached_state, cached_state)
    parents = parents or set()
    if id(data) in parents:
        raise SimpleBenchTypeError(
            'Cyclic reference detected in data structure during TypedDict validation',
            tag=_TypedDictErrorTag.CYCLIC_REFERENCE_DETECTED,
        )

    if len(parents) > DEFAULT_MAX_CORE_DATA_DEPTH:
        raise SimpleBenchTypeError(
            'Maximum core data depth exceeded during TypedDict validation',
            tag=_TypedDictErrorTag.MAX_CORE_DATA_DEPTH_EXCEEDED,
        )
    if not _validate.typed_dict_subclass(td_cls, raise_on_error):
        _log.debug(f'TypedDict subclass validation failed for {td_cls!r}')
        return (False, False)
    if not _validate.is_mapping_of_string_to_any(data, raise_on_error):
        _log.debug(f'Data is not a mapping of string to any: {data!r}')
        return (False, False)
    if not _validate.has_required_and_no_extra_keys(data, td_cls, raise_on_error):
        _log.debug(f'Data does not have required keys or has extra keys for TypedDict {td_cls.__name__}')
        return (False, False)

    keys_to_check: set[str] = set(data.keys())

    # Check value types for all keys in the data against the expected types defined in the TypedDict subclass.
    immutable_children: bool = True
    checked_keys: set[str] = set()
    required_keys = td_cls.__required_keys__ if hasattr(td_cls, '__required_keys__') else set()
    while keys_to_check:
        key = keys_to_check.pop()
        _log.debug(f'Validating key: {key!r} of TypedDict: {td_cls.__name__}')
        value = data[key]
        key_info = TypedDictKeyInfo(key, td_cls)
        expected_type_hint = key_info.value_type
        _log.debug(f'Expected type hint for key {key!r}: {expected_type_hint}')

        # Python primitive types and simple types that are considered core
        # data primitives are validated directly here.
        if is_core_data_primitive_type(expected_type_hint):
            if not is_core_data_primitive(value):
                if raise_on_error:
                    raise SimpleBenchTypeError(
                        f"Value for key '{key}' has invalid type {type(value)}, "
                        f'expected core data primitive type {expected_type_hint}',
                        tag=_TypedDictErrorTag.INVALID_TYPEDDICT_KEY_VALUE_TYPE,
                    )
                _log.debug(f'Value for key {key!r} is not a core data primitive as expected: {value!r}')
                return (False, False)  # Value type mismatch and we don't know immutability
            if not isinstance(value, expected_type_hint):
                if raise_on_error:
                    raise SimpleBenchTypeError(
                        f"Value for key '{key}' has invalid type {type(value)}, expected type {expected_type_hint}",
                        tag=_TypedDictErrorTag.INVALID_TYPEDDICT_KEY_VALUE_TYPE,
                    )
                _log.debug(f'Value for key {key!r} is not of expected type {expected_type_hint}: {value!r}')
                return (False, False)  # Value type mismatch and we don't know immutability
            checked_keys.add(key)
            continue  # Valid core data primitive, move to next key

        # Validate misc types (e.g., nested TypedDicts, generic containers) recursively using _validate_field_value
        parents.add(id(data))
        is_valid, is_immutable = _validate_field_value(value, expected_type_hint, parents)
        parents.remove(id(data))
        if not is_valid:
            if raise_on_error:
                raise SimpleBenchTypeError(
                    f"Value for key '{key}' has invalid type {type(value)}, expected type {expected_type_hint}",
                    tag=_TypedDictErrorTag.INVALID_TYPEDDICT_KEY_VALUE_TYPE,
                )
            _log.debug(f'Value for key {key!r} does not conform to expected type {expected_type_hint}: {value!r}')
            return (False, False)  # Value type mismatch and we cannot determine immutability
        if not is_immutable:
            immutable_children = False
        checked_keys.add(key)

    # Now check for required keys in the TypedDict that were missing from the data.
    skipped_keys = required_keys - checked_keys
    for key in skipped_keys:
        _log.debug(f'Validating skipped key: {key!r} of TypedDict: {td_cls.__name__}')
        key_info = TypedDictKeyInfo(key, td_cls)
        if not key_info.is_required:
            checked_keys.add(key)
            continue
        _log.debug(f'Missing required key {key!r} for TypedDict {td_cls.__name__}')
        return (False, False)  # Missing required key and we cannot determine immutability

    if immutable_children:  # All children are immutable core data types and so we can cache positively
        _CACHE.add_cache_entry(td_cls, data, True)
    _log.debug(f'TypedDict mimic validation successful for data: {data!r} against TypedDict: {td_cls.__name__}, '
                f'immutable_children={immutable_children}')
    return (True, immutable_children)  # All keys validated successfully, propagate immutability status


def _validate_field_value(
    value: Any, expected_type: Any, parents: set[int], raise_on_error: bool = True
) -> tuple[bool, bool]:
    """Validate a single field value against its expected type.

    The field must be one of:
    - A TypedDict subclass
    - A generic container type (e.g., List, Dict, Sequence, Mapping, Set...)
      with core data primitive types or TypedDict subclasses as element types

    _validate_field_value is a helper function that recursively checks
    the value against the expected type, handling nested structures.

    If it reaches primitive types, it uses is_core_data_primitive()
    to validate core data primitive values.

    If it reaches a TypedDict subclass, it uses
    is_typed_dict_mimic() to validate the structure.

    If it reaches a generic container type (e.g., List, Dict), it recursively
    validates each element against the specified element type.

    :param Any value: The value to validate.
    :param type expected_type: The expected type to validate against.
    :param set[int] parents: Set of parent object IDs to detect cycles.
    :param bool raise_on_error: If True, raise an error on validation failure.
    :return tuple[bool, bool]: A tuple (is_valid, is_immutable) indicating validation results.
    :raise SimpleBenchTypeError: If there is a validation error and raise_on_error is True.
    """
    _log.debug(f'A: Validating field value: {value!r} against expected type: {expected_type}')
    parents = parents or set()
    if id(value) in parents:
        if raise_on_error:
            raise SimpleBenchTypeError(
                'Cyclic reference detected in data structure during TypedDict validation',
                tag=_TypedDictErrorTag.CYCLIC_REFERENCE_DETECTED,
            )
        return (False, False)

    if len(parents) > DEFAULT_MAX_CORE_DATA_DEPTH:
        if raise_on_error:
            raise SimpleBenchTypeError(
                'Maximum core data depth exceeded during TypedDict validation',
                tag=_TypedDictErrorTag.MAX_CORE_DATA_DEPTH_EXCEEDED,
            )
        return (False, False)

    origin = get_origin(expected_type)
    args = get_args(expected_type)

    # Handle nested TypedDicts
    # Has to be checked before other types because
    # TypedDicts can be used as field types directly or nested
    # within generic containers and cause isinstance checks
    # to raise an error if we try to check them as a normal type.
    if is_typeddict(expected_type):
        valid, immutable = _validate_and_check_immutability_of_mimic(value, expected_type, parents)
        return (valid, immutable)


    # Core data primitives. Here both for performance and to
    # prevent str/bytes from being treated as containers
    # in the generic container handling below.
    if is_core_data_primitive_type(expected_type):
        return (isinstance(value, expected_type), True)

    # Handle generic Sequences (e.g. list, tuple, Sequence, etc.)
    if origin and isinstance(origin, type) and issubclass(origin, Sequence):
        results = _validate_generic_sequence_field(origin, args, value, parents)
        return results

    # Handle generic Sets (e.g. set, frozenset, Set, etc.)
    if origin and isinstance(origin, type) and issubclass(origin, Set):
        results = _validate_generic_set_field(args, value, parents)
        return results

    # Handle generic Mappings (e.g., dict, Mapping, MappingProxyType, etc.)
    if origin and isinstance(origin, type) and issubclass(origin, Mapping):
        results = _validate_generic_mapping_field(args, value, parents)
        return results

    # Handle Union types (e.g., Union[X, Y], Optional[X], etc.)
    if origin in (Union, UnionType, Optional):
        results = _validate_union_type_field(origin, args, value, parents)
        return results

    # Never say Never.
    # If the expected type is Never, then no value can conform to it.
    if expected_type is Never or origin is Never:
        if raise_on_error:
            raise SimpleBenchTypeError(
                f'Expected type is Never, but got value: {value!r}', tag=_TypedDictErrorTag.INVALID_TYPEDDICT_KEY_VALUE_TYPE
            )
        _log.debug(f'Expected type is Never, but got value: {value!r}')
        return (False, False)

    # Direct type check (non-Generic, non-TypedDict, non-core data primitive)
    _log.debug(f'B: Validating field value: {value!r} against expected non-generic, non-TypedDict type: {expected_type}')
    if isinstance(expected_type, type):
        return (isinstance(value, expected_type), True)
    _log.debug(f'Expected type {expected_type!r} is not a recognized type for validation, treating as Any')
    return (True, True)  # If expected_type is Any or not a type


def _validate_union_type_field(
        origin: Any, args: tuple[Any, ...], value: Any, parents: set[int]) -> tuple[bool, bool]:
    """Validate a Union/UnionType/Optional type field value against its expected types.
    This is called by _validate_field_value to handle Union types specifically.

    :param Any origin: The origin type of the expected Union type.
    :param tuple[Any, ...] args: The type arguments of the expected Union type.
    :param Any value: The value to validate.
    :param set[int] parents: Set of parent object IDs to detect cycles.
    :return tuple[bool, bool]: A tuple (is_valid, is_immutable) indicating validation results.
    """
    _log.debug(f'Validating Union type field value: {value!r} against expected Union types: {args}')
    for arg in args:
        immutable = True
        valid, is_arg_immutable = _validate_field_value(value, arg, parents)
        if valid:
            if not is_arg_immutable:
                immutable = False
            return (True, immutable)
    return (False, False)  # Value does not conform to any of the Union types

def _validate_generic_sequence_field(origin: Any, args: tuple[Any, ...], value: Any, parents: set[int]) -> tuple[bool, bool]:
    """Validate a sequence field value against its expected type.

    This is called by _validate_field_value to handle sequence types specifically
    and does not handle strings

    :param Any origin: The origin type of the expected type.
    :param tuple[Any, ...] args: The type arguments of the expected type.
    :param Any value: The value to validate.
    :param type expected_type: The expected type to validate against.
    :param set[int] parents: Set of parent object IDs to detect cycles.
    :return tuple[bool, bool]: A tuple (is_valid, is_immutable) indicating validation results.
    """
    if id(value) in parents:
        raise SimpleBenchTypeError(
            'Cyclic reference detected in data structure during TypedDict validation',
            tag=_TypedDictErrorTag.CYCLIC_REFERENCE_DETECTED,
        )

    if len(parents) > DEFAULT_MAX_CORE_DATA_DEPTH:
        raise SimpleBenchTypeError(
            'Maximum core data depth exceeded during TypedDict validation',
            tag=_TypedDictErrorTag.MAX_CORE_DATA_DEPTH_EXCEEDED,
        )

    # Handle Sequences (str/bytes are excluded earlier)
    if not isinstance(value, Sequence):
        return (False, False)

    # Handle variable-length tuple: Tuple[X, ...]
    if origin is tuple and len(args) == 2 and args[1] is Ellipsis:
        elem_type = args[0]
        immutable = True
        for v in value:
            parents.add(id(value))
            v_valid, v_immutable = _validate_field_value(v, elem_type, parents)
            parents.remove(id(value))
            if not v_valid:
                return (False, False)
            if not v_immutable:
                immutable = False
        return (True, immutable)

    # Handle fixed-length tuple: Tuple[X, Y, Z]
    if origin is tuple and len(args) > 0 and not (len(args) == 2 and args[1] is Ellipsis):
        if len(value) != len(args):
            return (False, False)
        immutable = True
        for v, elem_type in zip(value, args, strict=True):
            parents.add(id(value))
            v_valid, v_immutable = _validate_field_value(v, elem_type, parents)
            parents.remove(id(value))
            if not v_valid:
                return (False, False)
            if not v_immutable:
                immutable = False
        return (True, immutable)

    # Handle other sequences
    elem_type = args[0] if args else object
    _log.debug(f'Validating sequence field value: {value!r} against expected element type: {elem_type}')
    immutable = True
    for v in value:
        parents.add(id(value))
        v_valid, v_immutable = _validate_field_value(v, elem_type, parents)
        parents.remove(id(value))
        if not v_valid:
            return (False, False)
        if not v_immutable:
            immutable = False
    return (True, immutable)


def _validate_generic_set_field(args: tuple[Any, ...], value: Any, parents: set[int]) -> tuple[bool, bool]:
    """Validate a set field value against its expected type.
    This is called by _validate_field_value to handle set types specifically.

    :param tuple[Any, ...] args: The type arguments of the expected type.
    :param Any value: The value to validate.
    :param set[int] parents: Set of parent object IDs to detect cycles.
    :return tuple[bool, bool]: A tuple (is_valid, is_immutable) indicating validation results.
    """
    if id(value) in parents:
        raise SimpleBenchTypeError(
            'Cyclic reference detected in data structure during TypedDict validation',
            tag=_TypedDictErrorTag.CYCLIC_REFERENCE_DETECTED,
        )

    if len(parents) > DEFAULT_MAX_CORE_DATA_DEPTH:
        raise SimpleBenchTypeError(
            'Maximum core data depth exceeded during TypedDict validation',
            tag=_TypedDictErrorTag.MAX_CORE_DATA_DEPTH_EXCEEDED,
        )

    if not isinstance(value, Set):
        raise SimpleBenchTypeError(
            f'Expected a Set type for value, got {type(value)}', tag=_TypedDictErrorTag.NOT_A_SET
        )
    elem_type = args[0] if args else object
    immutable = True
    for v in value:
        parents.add(id(value))
        v_valid, v_immutable = _validate_field_value(v, elem_type, parents)
        parents.remove(id(value))
        if not v_valid:
            return (False, False)
        if not v_immutable:
            immutable = False
    return (True, immutable)


def _validate_generic_mapping_field(args: tuple[Any, ...], value: Any, parents: set[int]) -> tuple[bool, bool]:
    """Validate a mapping field value against its expected type.
    This is called by _validate_field_value to handle mapping types specifically.

    :param tuple[Any, ...] args: The type arguments of the expected type.
    :param Any value: The value to validate.
    :param set[int] parents: Set of parent object IDs to detect cycles.
    :return tuple[bool, bool]: A tuple (is_valid, is_immutable) indicating validation results.
    """
    if id(value) in parents:
        raise SimpleBenchTypeError(
            'Cyclic reference detected in data structure during TypedDict validation',
            tag=_TypedDictErrorTag.CYCLIC_REFERENCE_DETECTED,
        )

    if len(parents) > DEFAULT_MAX_CORE_DATA_DEPTH:
        raise SimpleBenchTypeError(
            'Maximum core data depth exceeded during TypedDict validation',
            tag=_TypedDictErrorTag.MAX_CORE_DATA_DEPTH_EXCEEDED,
        )

    if not isinstance(value, Mapping):
        raise SimpleBenchTypeError(
            f'Expected a Mapping type for value, got {type(value)}', tag=_TypedDictErrorTag.NOT_A_MAPPING
        )
    key_type, val_type = Any, Any

    # CoreDataMapping is a special case that is treated as a
    # Mapping with str keys and a single value type argument.
    if isinstance(value, CoreDataMapping):
        key_type = str
        match len(args):
            case 0:
                pass
            case 1:
                val_type = args[0]
            case 2:
                val_type = args[1]
            case _:
                raise SimpleBenchTypeError(
                    f'CoreDataMapping type must have zero or one type argument for value type: Found args: {args!r}',
                    tag=_TypedDictErrorTag.INVALID_CORE_DATA_MAPPING_TYPE_ARGS)
    else:
        match len(args):
            case 0:
                pass
            case 1:
                key_type = args[0]
            case 2:
                key_type, val_type = args
            case _:
                raise SimpleBenchTypeError(
                    'Mapping type must have zero, one, or two type arguments',
                    tag=_TypedDictErrorTag.INVALID_MAPPING_TYPE_ARGS,
                )

    if not _validate.is_string_key_type(key_type):
        raise SimpleBenchTypeError(
            'Mapping key type must be str, Literal of str, or Annotated[str, ...] for '
            f'TypedDict validation: found ({key_type!r}, {val_type!r})',
            tag=_TypedDictErrorTag.MAPPING_KEY_NOT_STRING,
        )
    immutable = True
    for k, v in value.items():
        if not isinstance(k, str):
            raise SimpleBenchTypeError(
                f'Mapping key must be str for TypedDict validation, got {type(k)}',
                tag=_TypedDictErrorTag.MAPPING_KEY_NOT_STRING,
            )
        parents.add(id(value))
        valid, v_immutable = _validate_field_value(v, val_type, parents)
        parents.remove(id(value))
        if not valid:
            return (False, False)
        if not v_immutable:
            immutable = False
    return (True, immutable)


def typed_dict_mimic(data: Mapping[str, Any], td_cls: type[T]) -> T:
    """Validate a mapping against the TypedDict.

    Raises an error if validation fails.

    This is a mimic function that behaves like a type cast to TypedDict.

    Because it performs structural validation, the returned value is guaranteed to conform
    to the specified TypedDict structure if no error is raised.

    This is a structural check and does not require an actual instance of TypedDict.

    It validates that:
    - All required keys are present and of the correct type.
    - All optional keys, if present, are of the correct type.
    - No extra keys are present.

    Cyclic references are detected and raise an error to prevent infinite recursion.

    :param Mapping[str, Any] data: The dictionary to validate.
    :param type[TypedDict] td_cls: The TypedDict subclass type to validate against.
    :return TypedDict: The validated TypedDict.
    :raise SimpleBenchTypeError: If any value has an incorrect type.
    """
    if is_typed_dict_mimic(data, td_cls):
        # Cast is safe because is_typed_dict_mimic ensures the structure conforms to td_cls
        return cast(T, data)

    raise SimpleBenchTypeError(
        f'Data does not conform to the structure of {td_cls.__name__}',
        tag=_TypedDictErrorTag.DATA_DOES_NOT_CONFORM_TO_TYPEDDICT)
