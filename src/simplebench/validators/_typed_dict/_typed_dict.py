"""Validation functions for type hints and instances against those type hints."""

from collections.abc import Mapping, Sequence, Set
from typing import Annotated, Any, Literal, TypedDict, TypeGuard, TypeVar, cast, get_args, get_origin, get_type_hints

from typeguard import check_type

from simplebench.base._typed_dict_key_info import TypedDictKeyInfo
from simplebench.defaults import DEFAULT_MAX_CORE_DATA_DEPTH
from simplebench.exceptions import SimpleBenchTypeError
from simplebench.validators._cache import ValidationCache
from simplebench.validators.core_data_types import is_core_data_primitive, is_core_data_primitive_type

from ._error_tags import _TypedDictErrorTag

_CACHE = ValidationCache(min_cache_size=100, max_cache_size=16384)

T = TypeVar('T', bound=TypedDict)  # type: ignore[invalidTypeForm,valid-type]


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
    try:
        valid = check_type(data, td_cls)
    except SimpleBenchTypeError as exc:
        raise SimpleBenchTypeError(
            f'Data does not conform to TypedDict {td_cls.__name__}: {exc} {data}',
            tag=_TypedDictErrorTag.NOT_A_TYPED_DICT
        ) from exc

    if not valid:
        raise SimpleBenchTypeError(
            f'Data does not conform to TypedDict {td_cls.__name__} : {data}',
            tag=_TypedDictErrorTag.NOT_A_TYPED_DICT
        )

    return cast(T, data)


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
    try:
        valid, _ = _validate_and_check_immutability_of_mimic(data, td_cls)
        return valid
    except SimpleBenchTypeError:
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
    cached_state: bool | None = _CACHE.valid_in_cache(td_cls, data)
    if cached_state is not None:
        # Cached results are always immutable core data types and thus safe to reuse.
        # Mutable structures can be validated but they are not cached because their
        # state can change after validation.
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
    if not _validate_typed_dict_subclass(td_cls, raise_on_error):
        return (False, False)
    if not _validate_is_mapping_of_string_to_any(data, raise_on_error):
        return (False, False)
    if not _validate_has_required_and_no_extra_keys(data, td_cls, raise_on_error):
        return (False, False)

    keys_to_check: set[str] = set(data.keys())

    # Check value types
    immutable_children: bool = True
    while keys_to_check:
        key = keys_to_check.pop()
        value = data[key]
        key_info = TypedDictKeyInfo(key, td_cls)
        expected_type_hint = key_info.value_type

        if is_core_data_primitive_type(expected_type_hint):
            if not is_core_data_primitive(value):
                if raise_on_error:
                    raise SimpleBenchTypeError(
                        f"Value for key '{key}' has invalid type {type(value)}, "
                        f'expected core data primitive type {expected_type_hint}',
                        tag=_TypedDictErrorTag.INVALID_TYPEDDICT_KEY_VALUE_TYPE,
                    )
                return (False, False)  # Value type mismatch and we don't know immutability
            continue

        # Validate nested TypedDict or generic container types
        parents.add(id(data))
        is_valid, is_immutable = _validate_field_value(value, expected_type_hint, parents)
        parents.remove(id(data))
        if not is_valid:
            if raise_on_error:
                raise SimpleBenchTypeError(
                    f"Value for key '{key}' has invalid type {type(value)}, expected type {expected_type_hint}",
                    tag=_TypedDictErrorTag.INVALID_TYPEDDICT_KEY_VALUE_TYPE,
                )
            return (False, False)  # Value type mismatch and we cannot determine immutability
        if not is_immutable:
            immutable_children = False

    if immutable_children:  # All children are immutable core data types and so we can cache positively
        _CACHE.add_cache_entry(td_cls, data, True)
    return (True, immutable_children)  # All keys validated successfully, propagate immutability status


def _validate_typed_dict_subclass(td_cls: type[TypedDict], raise_on_error: bool = True) -> bool:  # type: ignore
    """Validate a TypedDict subclass schema.

    This is not a runtime instance validation, but a static schema validation.

    This function checks that the provided TypedDict subclass is declared correctly
    and consistently. It ensures that all keys in the TypedDict's annotations
    are accounted for in either the `__required_keys__` or `__optional_keys__` sets.
    It raises an error if there are any discrepancies.

    It ALWAYS raises an error if the TypedDict subclass is misconfigured
    as this is a structural code validation error and not dependent on instance data.

    Uses typing.get_type_hints to resolve forward references and type aliases.

    :param TypedDict td_cls: The TypedDict subclass to validate
    :param bool raise_on_error: If True, raise an error on validation failure.
    :return bool: True if the TypedDict subclass is valid, False otherwise.
    :raise SimpleBenchTypeError: If raise_on_error is True and the TypedDict subclass is misconfigured or
        type hints cannot be resolved
    """
    try:
        annotations = get_type_hints(td_cls)
    except Exception as exc:  # always raise because this is a code misconfiguration
        raise SimpleBenchTypeError(
            f'Failed to resolve type hints for {td_cls.__name__}: {exc}',
            tag=_TypedDictErrorTag.UNABLE_TO_RESOLVE_TYPE_HINT,
        ) from exc
    required: set[str] = getattr(td_cls, '__required_keys__', set(annotations))
    optional: set[str] = getattr(td_cls, '__optional_keys__', set())
    annotation_set = set(annotations.keys())

    if annotation_set != required.union(optional):
        missing_from_annotations = (required.union(optional)) - annotation_set
        extra_in_annotations = annotation_set - (required.union(optional))
        output = []
        if extra_in_annotations:
            output.append(
                f'Keys {extra_in_annotations} are in annotations but not marked as required/optional '
                f'for class {td_cls.__name__}'
            )
        if missing_from_annotations:
            output.append(
                f'Keys {missing_from_annotations} are marked as required/optional but '
                f'missing from annotations for class {td_cls.__name__}'
            )
        message = '; '.join(output)
        if raise_on_error:
            raise SimpleBenchTypeError(message, tag=_TypedDictErrorTag.MISCONFIGURED_TYPED_DICT)
        return False
    return True


def _validate_is_mapping_of_string_to_any(data: Mapping[str, Any], raise_on_error: bool = True) -> bool:
    """Validate that data is a Mapping[str, Any].

    :param Mapping[str, Any] data: The data to validate.
    :param bool raise_on_error: If True, raise an error on validation failure.
    :return bool: True if data is a Mapping[str, Any], False otherwise.
    :raise SimpleBenchTypeError: If data is not a Mapping[str, Any] and raise_on_error is True.
    """
    if not isinstance(data, Mapping):
        if raise_on_error:
            raise SimpleBenchTypeError(
                f'Data must be a Mapping, got {type(data)}', tag=_TypedDictErrorTag.NOT_A_MAPPING
            )
        return False

    for key in data.keys():
        if not isinstance(key, str):
            if raise_on_error:
                raise SimpleBenchTypeError(
                    f'All keys in data must be strings, found key of type {type(key)}',
                    tag=_TypedDictErrorTag.MAPPING_KEY_NOT_STRING,
                )
            return False
    return True


def _validate_has_required_and_no_extra_keys(
    data: Mapping[str, Any],
    td_cls: type[TypedDict],  # type: ignore[invalidTypeForm]
    raise_on_error: bool = True,
) -> bool:
    """Validate that data has all required keys and no extra keys.

    :param Mapping[str, Any] data: The data to validate.
    :param type[TypedDict] td_cls: The TypedDict subclass to validate against.
    :param bool raise_on_error: If True, raise an error on validation failure.
    :return bool: True if data has all required keys and no extra keys, False otherwise.
    :raise SimpleBenchTypeError: If raise_on_error is True and required keys are missing or extra keys are present.
    """
    annotations = td_cls.__annotations__
    required: set[str] = getattr(td_cls, '__required_keys__', set(annotations))

    missing = required - data.keys()
    if missing:
        if raise_on_error:
            raise SimpleBenchTypeError(
                f'Missing required keys: {missing}', tag=_TypedDictErrorTag.MISSING_REQUIRED_KEYS
            )
        return False

    extra = data.keys() - annotations.keys()
    if extra:
        if raise_on_error:
            raise SimpleBenchTypeError(f'Extra keys not allowed: {extra}', tag=_TypedDictErrorTag.EXTRA_KEYS_PRESENT)
        return False
    return True


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

    # Special case: do not treat str/bytes as containers
    if origin in {str, bytes}:
        if is_core_data_primitive_type(expected_type):
            if not is_core_data_primitive(value):
                if raise_on_error:
                    raise SimpleBenchTypeError(
                        f'Value has invalid type {type(value)}, expected core data primitive type {expected_type}',
                        tag=_TypedDictErrorTag.INVALID_TYPEDDICT_KEY_VALUE_TYPE,
                    )
                return (False, False)
            return (True, True)
        if isinstance(expected_type, type):
            if isinstance(value, expected_type):
                return (True, True)
            elif raise_on_error:
                raise SimpleBenchTypeError(
                    f'Value has invalid type {type(value)}, expected type {expected_type}',
                    tag=_TypedDictErrorTag.INVALID_TYPEDDICT_KEY_VALUE_TYPE,
                )
            return (False, False)
        if expected_type is Any:
            return (True, False)

    # Handle Sequences (excluding str/bytes)
    if origin in (list, tuple, Sequence):
        parents.add(id(value))
        results = _validate_sequence_field(origin, args, value, parents)
        parents.remove(id(value))
        return results

    # Handle Sets
    if origin in (set, frozenset, Set):
        parents.add(id(value))
        results = _validate_set_field(args, value, parents)
        parents.remove(id(value))
        return results

    # Handle Mappings
    if origin in (dict, Mapping):
        parents.add(id(value))
        results = _validate_mapping_field(args, value, parents)
        parents.remove(id(value))
        return results

    # Handle TypedDicts
    if isinstance(expected_type, type) and issubclass(expected_type, TypedDict):  # type: ignore[reportArgumentType]
        parents.add(id(value))
        valid, immutable = _validate_and_check_immutability_of_mimic(value, expected_type, parents)
        parents.remove(id(value))
        return (valid, immutable)

    # Core data primitive
    if is_core_data_primitive_type(expected_type):
        return (is_core_data_primitive(value), True)

    # Fallback: direct type check
    if isinstance(expected_type, type):
        return (isinstance(value, expected_type), True)
    return (True, True)  # If expected_type is Any or not a type


def _validate_sequence_field(origin: Any, args: tuple[Any, ...], value: Any, parents: set[int]) -> tuple[bool, bool]:
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
            parents.add(id(v))
            v_valid, v_immutable = _validate_field_value(v, elem_type, parents)
            parents.remove(id(v))
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
            parents.add(id(v))
            v_valid, v_immutable = _validate_field_value(v, elem_type, parents)
            parents.remove(id(v))
            if not v_valid:
                return (False, False)
            if not v_immutable:
                immutable = False
        return (True, immutable)

    # Handle other sequences
    elem_type = args[0] if args else object
    immutable = True
    for v in value:
        parents.add(id(v))
        v_valid, v_immutable = _validate_field_value(v, elem_type, parents)
        parents.remove(id(v))
        if not v_valid:
            return (False, False)
        if not v_immutable:
            immutable = False
    return (True, immutable)


def _validate_set_field(args: tuple[Any, ...], value: Any, parents: set[int]) -> tuple[bool, bool]:
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
        parents.add(id(v))
        v_valid, v_immutable = _validate_field_value(v, elem_type, parents)
        parents.remove(id(v))
        if not v_valid:
            return (False, False)
        if not v_immutable:
            immutable = False
    return (True, immutable)


def _validate_mapping_field(args: tuple[Any, ...], value: Any, parents: set[int]) -> tuple[bool, bool]:
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
    if not _is_string_key_type(key_type):
        raise SimpleBenchTypeError(
            'Mapping key type must be str, Literal of str, or Annotated[str, ...] for TypedDict validation',
            tag=_TypedDictErrorTag.MAPPING_KEY_NOT_STRING,
        )
    immutable = True
    parents.add(id(value))
    for k, v in value.items():
        if not isinstance(k, str):
            raise SimpleBenchTypeError(
                f'Mapping key must be str for TypedDict validation, got {type(k)}',
                tag=_TypedDictErrorTag.MAPPING_KEY_NOT_STRING,
            )
        valid, v_immutable = _validate_field_value(v, val_type, parents)
        if not valid:
            return (False, False)
        if not v_immutable:
            immutable = False
    parents.remove(id(value))
    return (True, immutable)


def _is_string_key_type(key_type: Any) -> bool:
    """Check if a type is a valid string key type for Mappings.

    :param Any key_type: The type to check.
    :return bool: True if the type is a valid string key type, False otherwise.
    """
    if key_type is str:
        return True
    origin = get_origin(key_type)
    if origin is Literal:
        return all(isinstance(arg, str) for arg in get_args(key_type))
    if origin is Annotated and get_args(key_type) and get_args(key_type)[0] is str:
        return True
    try:
        return issubclass(key_type, str)
    except TypeError:
        return False
