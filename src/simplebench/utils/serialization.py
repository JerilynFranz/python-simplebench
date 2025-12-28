"""Serialization utilities for simplebench."""
import json
from collections.abc import Mapping, Sequence, Set
from dataclasses import asdict, is_dataclass
from json import JSONEncoder
from types import NoneType
from typing import Any, Callable, TypeAlias

from simplebench.exceptions import SimpleBenchTypeError, SimpleBenchValueError
from simplebench.validators import validate_bool, validate_type

from ._error_tags import _UtilsErrorTag

JSONPrimitiveTypes: TypeAlias = str | int | float | bool | NoneType
JSONDictTypes: TypeAlias = dict[str, 'JSONSerializableType']
JSONListTypes: TypeAlias = list['JSONSerializableType']
JSONSerializableType: TypeAlias = JSONPrimitiveTypes | JSONDictTypes | JSONListTypes


def serialize_to_json(
        obj: object,
        *,
        skipkeys: bool = False,
        ensure_ascii: bool = True,
        check_circular: bool = True,
        allow_nan: bool = True,
        cls: type[JSONEncoder] | None = None,
        indent: int | str | None = None,
        separators: tuple[str, str] | None = None,
        default: Callable[[Any], Any] | None = None,
        sort_keys: bool = False,
        **kwargs: Any) -> str:
    """Serialize an object to a JSON string.

    It uses `serialize_to_dict_list_or_primitive` to convert the object to a JSON-compatible dictionary
    representation, then serializes that to a JSON string using the Python standard library
    library function :func:`json.dumps()`.

    It requires that all mappings have string keys and that there are no cyclic references
    in the object graph. It takes the same arguments as :func:`json.dumps()`.

    :param object obj: The object to serialize.
    :param bool skipkeys: If True, skip keys that are not basic types (str, int, float, bool).
    :param bool ensure_ascii: If True, the output is guaranteed to be ASCII-only.
    :param bool check_circular: If True, check for circular references during serialization.
    :param bool allow_nan: If True, allow NaN and Infinity values in the output.
    :param type[JSONEncoder] | None cls: Custom JSONEncoder subclass to use for serialization.
    :param int | str | None indent: If specified, pretty-print the JSON with this indent level.
    :param tuple[str, str] | None separators: If specified, use these separators for items and key-value pairs.
    :param Callable[[Any], Any] | None default: If specified, a function that converts non-serializable objects.
    :param bool sort_keys: If True, sort the keys in the output JSON.
    :param kwargs: Additional keyword arguments to pass to `json.dumps()`.
    :return str: JSON string representation of the object.
    """
    validate_bool(skipkeys, "skipkeys", _UtilsErrorTag.INVALID_SKIPKEYS_ARG_TYPE)
    validate_bool(ensure_ascii, "ensure_ascii", _UtilsErrorTag.INVALID_ENSURE_ASCII_ARG_TYPE)
    validate_bool(check_circular, "check_circular", _UtilsErrorTag.INVALID_CHECK_CIRCULAR_ARG_TYPE)
    validate_bool(allow_nan, "allow_nan", _UtilsErrorTag.INVALID_ALLOW_NAN_ARG_TYPE)
    if cls is not None:
        if not issubclass(cls, JSONEncoder):
            raise SimpleBenchTypeError(
                "The 'cls' argument must be a subclass of json.JSONEncoder",
                tag=_UtilsErrorTag.INVALID_JSON_ENCODER_CLASS_ARG_TYPE)
    if indent is not None:
        validate_type(indent, (int, str), "indent", _UtilsErrorTag.INVALID_INDENT_ARG_TYPE)
    if separators is not None:
        validate_type(separators, tuple, "separators", _UtilsErrorTag.INVALID_SEPARATORS_ARG_TYPE)
        if len(separators) != 2 or not all(isinstance(s, str) for s in separators):
            raise SimpleBenchTypeError(
                "The 'separators' argument must be a tuple of two strings",
                tag=_UtilsErrorTag.INVALID_SEPARATORS_ARG_VALUE)
    if default is not None and not callable(default):
        raise SimpleBenchTypeError(
            "The 'default' argument must be a callable",
            tag=_UtilsErrorTag.INVALID_DEFAULT_ARG_TYPE)
    validate_bool(sort_keys, "sort_keys", _UtilsErrorTag.INVALID_SORT_KEYS_ARG_TYPE)

    serializable = serialize_to_dict_list_or_primitive(obj)
    return json.dumps(
        serializable,
        skipkeys=skipkeys,
        ensure_ascii=ensure_ascii,
        check_circular=check_circular,
        allow_nan=allow_nan,
        cls=cls,
        indent=indent,
        separators=separators,
        default=default,
        sort_keys=sort_keys,
        **kwargs)

def serialize_to_dict_list_or_primitive(obj: object) -> JSONSerializableType:
    """Serialize an object to a `json.dumps()` compatible dictionary, list, or primitive type.
    
    It recursively converts the object and its nested structures into types that can be
    directly serialized to JSON (i.e., dicts, lists, strings, numbers, booleans, and None).

    It requires that all mappings have string keys and that there are no cyclic references
    in the object graph.

    If an object has a `to_dict()` method, it will be used to obtain a dictionary
    representation of the object. If the object is a dataclass, it will be converted
    to a dictionary using `dataclasses.asdict()`.

    If an object is present in the graph in more than one place it must be a
    primitive immutable (e.g., str, int, float, bool, None) to avoid false positives
    for cyclic references.

    :param object obj: The object to serialize.
    :return dict: JSON-serialization compatible representation of the object.
    """
    return _internal_serialize_to_dict_list_or_primitive(obj, set())

def _internal_serialize_to_dict_list_or_primitive(current: object, parents: set[int]) -> JSONSerializableType:
    """Serialize an object to a JSON-compatible dictionary, list, or primitive type."""

    current_id = id(current)
    if current_id in parents:
        raise SimpleBenchValueError(
            "Cyclic reference detected during serialization",
            tag=_UtilsErrorTag.SERIALIZATION_CYCLIC_REFERENCE_DETECTED)

    if isinstance(current, (str, int, float, bool)) or current is None:
        return current
    elif isinstance(current, Mapping):
        parents.add(current_id)
        result = _internal_serialize_to_dict(current, parents)
        parents.remove(current_id)
        return result
    elif isinstance(current, Sequence) and not isinstance(current, (str, bytes)):
        parents.add(current_id)
        result = _internal_serialize_to_list(current, parents)
        parents.remove(current_id)
        return result
    else:
        # See if we can get a Mapping representation of the current object
        temp_dict = None
        to_dict = getattr(current, "to_dict", None)
        if to_dict is not None and callable(to_dict):
            temp_dict = to_dict()
        elif is_dataclass(current) and not isinstance(current, type):
            temp_dict = asdict(current)

        if isinstance(temp_dict, Mapping):
            parents.add(current_id)
            results = _internal_serialize_to_dict(temp_dict, parents)
            parents.remove(current_id)
            return results

    raise SimpleBenchTypeError(
        f"Object of type {type(current).__name__} is not JSON-serializable",
        tag=_UtilsErrorTag.SERIALIZATION_INVALID_OBJ_TYPE)

def _internal_serialize_to_dict(current: object, parents: set[int]) -> JSONSerializableType:
    """Serialize an object to a JSON-compatible dictionary representation."""

    current_id = id(current)
    if current_id in parents:
        raise SimpleBenchValueError(
            "Cyclic reference detected during serialization",
            tag=_UtilsErrorTag.SERIALIZATION_CYCLIC_REFERENCE_DETECTED)
    parents.add(current_id)

    # See if we can get a Mapping representation of the current object
    temp_dict = None
    to_dict = getattr(current, "to_dict", None)
    if to_dict is not None and callable(to_dict):
        temp_dict = to_dict()
    elif is_dataclass(current) and not isinstance(current, type):
        temp_dict = asdict(current)
    elif isinstance(current, Mapping):
        temp_dict = current

    if not isinstance(temp_dict, Mapping):
        raise SimpleBenchTypeError(
            f"Object of type {type(current).__name__} is not JSON-serializable",
            tag=_UtilsErrorTag.SERIALIZATION_INVALID_OBJ_TYPE)

    # Now turn it into a serializable dictionary recursively
    dictionary: JSONDictTypes = {}
    for key, value in temp_dict.items():
        if not isinstance(key, str):
            raise SimpleBenchTypeError(
                f"Dictionary key of type {type(key).__name__} is not JSON-serializable; keys must be strings",
                tag=_UtilsErrorTag.SERIALIZATION_INVALID_OBJ_TYPE)
        if isinstance(value, (str, int, float, bool)) or value is None:
            dictionary[key] = value
        elif isinstance(value, Mapping):
            parents.add(current_id)
            dictionary[key] = _internal_serialize_to_dict_list_or_primitive(value, parents)
            parents.remove(current_id)
        elif isinstance(value, (Sequence, Set)) and not isinstance(value, (str, bytes)):
            parents.add(current_id)
            dictionary[key] = _internal_serialize_to_dict_list_or_primitive(value, parents)
            parents.remove(current_id)
        else:
            raise SimpleBenchTypeError(
                f"Value of type {type(value).__name__} for key '{key}' is not JSON-serializable",
                tag=_UtilsErrorTag.SERIALIZATION_INVALID_OBJ_TYPE)
    return dictionary

def _internal_serialize_to_list(current: Sequence | Set, parents: set[int]) -> JSONListTypes:
    """Serialize a sequence to a JSON-compatible list representation."""
    current_id = id(current)
    if current_id in parents:
        raise SimpleBenchValueError(
            "Cyclic reference detected during serialization",
            tag=_UtilsErrorTag.SERIALIZATION_CYCLIC_REFERENCE_DETECTED)
    parents.add(current_id)

    try:
        if isinstance(current, Set):  # Sort sets to ensure consistent ordering
            sorted_current = sorted(current, key=lambda x: str(x))  # pylint: disable=unnecessary-lambda
            current = sorted_current
    except Exception:  # pylint: disable=broad-exception-caught
        pass  # If sorting fails, just proceed without sorting

    lst: JSONListTypes = []
    for item in current:
        if isinstance(item, (str, int, float, bool)) or item is None:
            lst.append(item)
        elif isinstance(item, Mapping):
            parents.add(current_id)
            lst.append(_internal_serialize_to_dict(item, parents))
            parents.remove(current_id)
        elif isinstance(item, (Sequence, Set)) and not isinstance(item, (str, bytes)):
            parents.add(current_id)
            lst.append(_internal_serialize_to_list(item, parents))
            parents.remove(current_id)
        else:
            raise SimpleBenchTypeError(
                f"Item of type {type(item).__name__} in sequence is not JSON-serializable",
                tag=_UtilsErrorTag.SERIALIZATION_INVALID_OBJ_TYPE)
    return lst
