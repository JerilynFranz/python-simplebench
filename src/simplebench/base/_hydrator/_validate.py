"""Validation functions for Hydrator parameters."""

import inspect
from collections.abc import Callable, Iterable, Mapping, Sequence, Set
from typing import Any, Union, get_args, get_origin, get_type_hints, is_typeddict

from simplebench.exceptions import SimpleBenchTypeError, SimpleBenchValueError
from simplebench.validators import validate_iterable_of_type, validate_type

from .._typed_dict_key_info import TypedDictKeyInfo
from ._error_tags import _HydratorErrorTag


def data(value: Mapping[str, Any]) -> dict[str, Any]:
    """Validate the data dictionary.

    :param data: The data dictionary to validate.
    :return: A validated, mutable `dict` copy of the data.
    :raises: SimpleBenchTypeError if the data dictionary is invalid.
    """
    validate_type(value, Mapping, 'data', _HydratorErrorTag.INVALID_DATA_TYPE)

    if not all(isinstance(key, str) for key in value.keys()):
        raise SimpleBenchTypeError(
            "All keys in the data dictionary must be of type 'str'", tag=_HydratorErrorTag.INVALID_DATA_KEY_TYPE
        )

    return dict(value)


def allowed(allowed_fields: Mapping[str, Any]) -> Mapping[str, Any]:
    """Validate the allowed parameters dictionary.

    A valid type annotation is a simple type (e.g., `int`) or a generic
    from the `typing` module (e.g., `list[str]`).

    :param allowed_fields: The allowed parameters dictionary to validate.
    :return: The validated allowed parameters dictionary.
    :raises: SimpleBenchTypeError if the allowed parameters dictionary is invalid.
    :raises: SimpleBenchValueError if the allowed parameters dictionary is empty.
    """
    validate_type(allowed_fields, Mapping, 'allowed', _HydratorErrorTag.INVALID_ALLOWED_TYPE)

    if len(allowed_fields) == 0:
        raise SimpleBenchValueError(
            'The `allowed` dictionary cannot be empty', tag=_HydratorErrorTag.INVALID_ALLOWED_EMPTY
        )

    for field in allowed_fields.values():
        # A valid type annotation is either a simple type (like `int`)
        # or a generic from the typing module (like `list[str]`, which has an __origin__).
        is_simple_type = isinstance(field, type)
        is_generic_type = hasattr(field, '__origin__')
        if not (is_simple_type or is_generic_type):
            raise SimpleBenchTypeError(
                f'All values in `allowed` must be a valid type annotation, but got {allowed_fields}',
                tag=_HydratorErrorTag.INVALID_ALLOWED_VALUE_TYPE,
            )

    return allowed_fields


def skip(skip_fields: Iterable[str], allowed_fields: Mapping[str, Any]) -> set[str]:
    """Validate the skip iterable.

    :param skip: The skip iterable to validate.
    :return: The validated skip set.
    :raises: SimpleBenchTypeError if the skip iterable is invalid.
    """
    skip_set = set(
        validate_iterable_of_type(
            skip_fields,
            str,
            'skip',
            _HydratorErrorTag.INVALID_SKIP_TYPE,
            _HydratorErrorTag.INVALID_SKIP_ITEM_TYPE,
            allow_empty=True,
            exact_type=False,
        )
    )
    if not all(field in allowed_fields for field in skip_set):
        raise SimpleBenchValueError(
            'All values in `skip` must match a key in `allowed`', tag=_HydratorErrorTag.INVALID_SKIP_VALUE
        )

    return skip_set


def optional(optional_fields: Iterable[str], allowed_fields: Mapping[str, Any]) -> set[str]:
    """Validate the optional iterable.

    :param optional_fields: The optional iterable to validate.
    :param allowed_fields: The allowed parameters dictionary to use for validation.
    :return: The validated optional set.
    :raises: SimpleBenchTypeError if the optional iterable is invalid.
    :raises: SimpleBenchValueError if the optional iterable contains invalid values.
    """
    optional_set = set(
        validate_iterable_of_type(
            optional_fields,
            str,
            'optional',
            _HydratorErrorTag.INVALID_OPTIONAL_TYPE,
            _HydratorErrorTag.INVALID_OPTIONAL_ITEM_TYPE,
            allow_empty=True,
            exact_type=False,
        )
    )
    if not all(field in allowed_fields for field in optional_set):
        raise SimpleBenchValueError(
            'All values in `optional` must match a key in `allowed`', tag=_HydratorErrorTag.INVALID_OPTIONAL_ITEM_VALUE
        )

    return optional_set


def defaults(default_values: Mapping[str, Any], optional_fields: set[str]) -> Mapping[str, Any]:
    """Validate the default mapping.

    :param Mapping[str, Any] default_values: The default mapping to validate.
    :param set[str] optional_fields: The optional set to use for validation.
    :return Mapping[str, Any]: The validated default mapping.
    :raises: SimpleBenchTypeError if the default mapping is invalid.
    :raises: SimpleBenchValueError if the default mapping contains invalid values.
    """
    if not isinstance(default_values, Mapping):
        raise SimpleBenchTypeError(
            'The `default` parameter must be of type `Mapping`', tag=_HydratorErrorTag.INVALID_DEFAULT_TYPE
        )

    if not all(field in optional_fields for field in default_values.keys()):
        raise SimpleBenchValueError(
            'All keys in `default` must match a key in `optional`', tag=_HydratorErrorTag.INVALID_DEFAULT_KEY
        )

    return default_values


def match_on(match_on_param: Mapping[str, Any], allowed_fields: Mapping[str, Any]) -> Mapping[str, Any]:
    """Validate the match_on dictionary.

    :param Mapping[str, Any] match_on_param: The match_on dictionary to validate.
    :param Mapping[str, Any] allowed_fields: The allowed parameters dictionary to use for validation.
    :return Mapping[str, Any]: The validated match_on dictionary.
    :raises: SimpleBenchTypeError if the match_on dictionary is invalid.
    :raises: SimpleBenchValueError if the match_on dictionary contains invalid values.
    """
    if not isinstance(match_on_param, Mapping):
        raise SimpleBenchTypeError(
            'The `match_on` parameter must be of type `Mapping`', tag=_HydratorErrorTag.INVALID_MATCH_ON_TYPE
        )

    if not all(field in allowed_fields for field in match_on_param.keys()):
        raise SimpleBenchValueError(
            'All keys in `match_on` must match a key in `allowed`', tag=_HydratorErrorTag.INVALID_MATCH_ON_KEY
        )

    return match_on_param


def process_as(
    process_as_handlers: Mapping[str, Callable[[Any], Any]], allowed_fields: Mapping[str, Any]
) -> Mapping[str, Callable[[Any], Any]]:
    """Validate the process_as mapping.

    :param Mapping[str, Callable[[Any], Any]] process_as_handlers: The process_as mapping to validate.
    :param Mapping[str, Any] allowed_fields: The allowed parameters mapping to use for validation.
    :return Mapping[str, Callable[[Any], Any]]: The validated process_as mapping.
    :raises: SimpleBenchTypeError if the process_as mapping is invalid.
    :raises: SimpleBenchValueError if the process_as mapping contains invalid values.
    """
    if not isinstance(process_as_handlers, Mapping):
        raise SimpleBenchTypeError(
            'The `process_as` parameter must be of type `Mapping`', tag=_HydratorErrorTag.INVALID_PROCESS_AS_TYPE
        )

    if not all(field in allowed_fields for field in process_as_handlers.keys()):
        raise SimpleBenchValueError(
            'All keys in `process_as` must match a key in `allowed`', tag=_HydratorErrorTag.INVALID_PROCESS_AS_KEY
        )

    for call in process_as_handlers.values():
        # must be callable with exactly one parameter and a return type annotation
        if not callable(call):
            raise SimpleBenchTypeError(
                'All values in `process_as` must be callable', tag=_HydratorErrorTag.INVALID_PROCESS_AS_NOT_CALLABLE
            )

        call_signature = inspect.signature(call)
        if len(call_signature.parameters) != 1:
            raise SimpleBenchTypeError(
                'All values in `process_as` must be callable with exactly one parameter',
                tag=_HydratorErrorTag.INVALID_PROCESS_AS_TOO_MANY_PARAMETERS,
            )
        param = list(call_signature.parameters.values())[0]
        if param.kind not in [inspect.Parameter.POSITIONAL_OR_KEYWORD, inspect.Parameter.POSITIONAL_ONLY]:
            raise SimpleBenchTypeError(
                'All values in `process_as` must be callable with a single positional parameter',
                tag=_HydratorErrorTag.INVALID_PROCESS_AS_NOT_POSITIONAL,
            )

        return_annotation = call_signature.return_annotation
        if return_annotation == inspect.Parameter.empty:
            raise SimpleBenchTypeError(
                'All values in `process_as` must be callable with a return type annotation',
                tag=_HydratorErrorTag.INVALID_PROCESS_AS_NO_RETURN_ANNOTATION,
            )

    return process_as_handlers


def allowed_keys_against_data(data_values: dict[str, Any], allowed_fields_map: Mapping[str, Any]) -> None:
    """Validate that all keys in the data dictionary are allowed.

    This does not check types, only that the keys exist in the allowed fields.

    :param dict[str, Any] data_values: The data dictionary to validate.
    :param Mapping[str, Any] allowed_fields_map: The allowed fields map.
    :raises: SimpleBenchValueError if any key is not allowed.
    """
    for field in data_values.keys():
        if field not in allowed_fields_map:
            raise SimpleBenchValueError(f"The key '{field}' is not allowed", tag=_HydratorErrorTag.INVALID_DATA_KEY)


def required_keys_against_data(
    data_values: dict[str, Any], allowed_fields_map: Mapping[str, Any], optional_fields_set: set[str]
) -> None:
    """Validate that all required keys are present in the data dictionary.

    :param dict[str, Any] data_values: The data dictionary to validate.
    :param Mapping[str, Any] allowed_fields_map: The allowed fields map.
    :param set[str] optional_fields_set: The set of optional fields.
    :raises: SimpleBenchValueError if any required key is missing.
    """
    for field in allowed_fields_map:
        if field not in data_values and field not in optional_fields_set:
            raise SimpleBenchValueError(f"The key '{field}' is missing", tag=_HydratorErrorTag.INVALID_DATA_KEY)


def data_types(output: dict[str, Any], allowed_fields_map: Mapping[str, Any]) -> None:
    """Validate that all values in the data dictionary match the allowed types.

    :param dict[str, Any] output: The data dictionary to validate.
    :param Mapping[str, Any] allowed_fields_map: The allowed fields map.
    :raises: SimpleBenchTypeError if any value does not match the allowed type.
    """
    for field, value in output.items():
        if not is_instance_of_generic(value, allowed_fields_map[field]):
            raise SimpleBenchTypeError(
                f"The value of '{field}' does not match the expected type '{allowed_fields_map[field]}'",
                tag=_HydratorErrorTag.INVALID_DATA_VALUE_TYPE,
            )


def is_instance_of_generic(obj: Any, type_hint: Any) -> bool:
    """
    Check if an object is an instance of a generic type hint.
    Handles simple types, lists, sequences, and dictionaries.

    :param obj: The object to check.
    :param type_hint: The type hint to check against.
    :return: True if the object matches the type hint, False otherwise.
    """
    origin = get_origin(type_hint)
    args = get_args(type_hint)

    # Case 1: Simple type (e.g., int, str)
    if origin is None:
        if isinstance(type_hint, type):
            return isinstance(obj, type_hint)
        return False  # Should not happen with valid type hints

    # Case 2: Dictionary or Mapping
    if inspect.isclass(origin) and issubclass(origin, Mapping):
        if not isinstance(obj, Mapping):
            return False
        key_type, value_type = args
        return all(
            is_instance_of_generic(k, key_type) and is_instance_of_generic(v, value_type) for k, v in obj.items()
        )

    # Case 3: Iterable (but not a Mapping)
    if inspect.isclass(origin) and issubclass(origin, Iterable):
        # If the object is a string/bytes but the type hint is a different kind of iterable (e.g. list[str]),
        # it's a mismatch. We should not iterate over the string's characters.
        if isinstance(obj, (str, bytes)):
            return issubclass(origin, (str, bytes))

        if not isinstance(obj, Iterable):
            return False

        item_type = args[0]
        return all(is_instance_of_generic(item, item_type) for item in obj)

    # Fallback for other types (like Union, etc., which can be added here)
    return isinstance(obj, origin)


def match_on_values(data_values: dict[str, Any], match_on_fields: Mapping[str, Any]) -> None:
    """Validate match_on rules against the data dictionary.

    :param dict[str, Any] data_values: The data dictionary to validate.
    :param Mapping[str, Any] match_on_fields: The match_on rules to apply.
    :raises: SimpleBenchValueError for any mismatch.
    """
    for field, expected_value in match_on_fields.items():
        if data_values.get(field) != expected_value:
            raise SimpleBenchValueError(
                f"The value of '{field}' must be '{expected_value}'", tag=_HydratorErrorTag.INVALID_MATCH_ON_VALUE
            )


def _is_basetype(typeddict_cls: type) -> dict[str, Any]:
    """Return a dictionary of the parameters and their types for a TypedDict class.

    It takes a TypedDict class as input and returns a dictionary mapping
    parameter names to their types based on the TypedDict's annotations
    in a form suitable for isinstance checks.

    :param type typeddict_cls: The TypedDict class to inspect.
    :return dict[str, Any]: A dictionary mapping parameter names for the TypedDict to their types.
    """
    output: dict[str, Any] = {}
    annotations = get_type_hints(typeddict_cls)
    for key in annotations:
        value_info = TypedDictKeyInfo(key, typeddict_cls)
        value_type = value_info.value_type
        annotations[key] = _unwrap_typeddict_type(value_type)
    return output


def _unwrap_typeddict_type(tp: Any) -> Any:
    """Unwrap a type annotation to its base type for isinstance checks.

    - For generics (e.g., list[str]), returns the base type (list, dict, set, tuple, etc.).
    - For TypedDict, returns dict.
    - For primitives, returns the primitive type.
    - For unions, returns a tuple of the base types.
    - For Literal, returns a tuple of the literal values.
    - Otherwise, returns the type itself.

    :param Any tp: The type annotation to unwrap.
    :return Any: The base type suitable for isinstance checks.
    """
    if is_typeddict(tp):
        return dict

    origin = get_origin(tp)
    if origin is not None:
        # Handle Union types
        if (
            origin is getattr(__import__('typing'), 'Union', None)
            or origin is getattr(__import__('types'), 'UnionType', None)
            or origin is Union
        ):
            args = get_args(tp)
            return tuple(_unwrap_typeddict_type(arg) for arg in args)
        # Handle Literal types
        if origin is getattr(__import__('typing'), 'Literal', None):
            return get_args(tp)
        return origin

    return tp  # Fallback: return the type itself


def is_instance_of_typehint(obj: Any, type_hint: Any, recurse: bool = False) -> bool:
    """
    Enhanced wrapper for is_instance_of_generic that handles unions, literals,
    TypedDict, Mapping, Iterable, Set, Sequence, and other special cases.
    Returns True if obj matches any type in the union, any value in a Literal,
    or matches the type_hint directly.
    If recurse=True, performs deep validation of nested structures.
    """
    origin = get_origin(type_hint)
    args = get_args(type_hint)

    # Handle TypedDict as Mapping
    if is_typeddict(type_hint):
        if not isinstance(obj, dict):
            return False
        if not all(isinstance(k, str) for k in obj.keys()):
            return False
        if recurse:
            annotations = get_type_hints(type_hint)
            for key, value_type in annotations.items():
                if key in obj:
                    if not is_instance_of_typehint(obj[key], value_type, recurse=True):
                        return False
        return True

    # Handle Union types
    if (
        origin is getattr(__import__('typing'), 'Union', None)
        or origin is getattr(__import__('types'), 'UnionType', None)
        or origin is Union
    ):
        return any(is_instance_of_typehint(obj, arg, recurse=recurse) for arg in args)

    # Handle Literal types
    if origin is getattr(__import__('typing'), 'Literal', None):
        return obj in args

    # Handle Mapping types
    if origin and issubclass(origin, Mapping):
        if not isinstance(obj, Mapping):
            return False
        if recurse and len(args) == 2:
            key_type, value_type = args
            for k, v in obj.items():
                if not is_instance_of_typehint(k, key_type, recurse=True):
                    return False
                if not is_instance_of_typehint(v, value_type, recurse=True):
                    return False
            return True
        return True  # Shallow: just check Mapping

    # Handle Set types
    if origin and issubclass(origin, Set) and not issubclass(origin, (str, bytes)):
        if not isinstance(obj, Set) or isinstance(obj, (str, bytes)):
            return False
        if recurse and args:
            item_type = args[0]
            for item in obj:
                if not is_instance_of_typehint(item, item_type, recurse=True):
                    return False
            return True
        return True  # Shallow: just check Set

    # Handle Sequence types (excluding str/bytes)
    if origin and issubclass(origin, Sequence) and not issubclass(origin, (str, bytes)):
        if not isinstance(obj, Sequence) or isinstance(obj, (str, bytes)):
            return False
        if recurse and args:
            item_type = args[0]
            for item in obj:
                if not is_instance_of_typehint(item, item_type, recurse=True):
                    return False
            return True
        return True  # Shallow: just check Sequence

    # Handle Iterable types (excluding str/bytes)
    if origin and issubclass(origin, Iterable) and not issubclass(origin, (str, bytes)):
        if not isinstance(obj, Iterable) or isinstance(obj, (str, bytes)):
            return False
        if recurse and args:
            item_type = args[0]
            for item in obj:
                if not is_instance_of_typehint(item, item_type, recurse=True):
                    return False
            return True
        return True  # Shallow: just check Iterable

    # Fallback to original logic
    return is_instance_of_generic(obj, type_hint)
    return is_instance_of_generic(obj, type_hint)
