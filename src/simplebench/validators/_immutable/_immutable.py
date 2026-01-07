"""Module for immutable validators."""
from dataclasses import is_dataclass
from enum import Enum
from types import MappingProxyType, NoneType
from typing import Any

from simplebench.exceptions import SimpleBenchRecursionError, SimpleBenchTypeError, SimpleBenchValueError
from simplebench.types import Immutable

from ._error_tags import _ImmutableErrorTag


class NoAttrSentinel:
    """Sentinel class to represent absence of an attribute."""


NO_ATTR = NoAttrSentinel()

IMMUTABLE_PRIMATIVE_TYPES_TUPLE: tuple[type, ...] = (int, float, complex, bool, str, bytes, NoneType, Enum, range)
IMMUTABLE_CONTAINER_TYPES_TUPLE: tuple[type, ...] = (tuple, frozenset, MappingProxyType)

def validate_immutable(obj: Any, name: str, message: str | None = None, depth: int = 200) -> bool:
    """Validate that the given object is immutable.

    It recursively checks container types to ensure all contained elements are also immutable.

    The 'name' parameter is used in the error message to identify the object being validated.

    :param Any obj: The object to check.
    :param str name: The name of the object being validated.
    :param str | None message: Custom error message to use if validation fails. If None, a default message is used.
    :param int depth: Maximum recursion depth to prevent infinite loops on cyclic references.
    :return bool: True if the object is immutable.

    :raises SimpleBenchRecursionError: If the maximum recursion depth is exceeded while checking immutability.
    :raises SimpleBenchTypeError: If the object is not immutable or if parameters are of incorrect types.
    :raises SimpleBenchValueError: If parameters have invalid values.
    """
    if not isinstance(name, str):
        raise SimpleBenchTypeError("The 'name' parameter must be a string.",
                                   tag=_ImmutableErrorTag.NAME_NOT_STRING)
    if name.strip() == "":
        raise SimpleBenchValueError("The 'name' parameter must be a non-blank string.",
                                   tag=_ImmutableErrorTag.NAME_IS_EMPTY_OR_BLANK_STRING)
    if not isinstance(depth, int):
        raise SimpleBenchTypeError("The 'depth' parameter must be an integer.",
                                   tag=_ImmutableErrorTag.DEPTH_NOT_INTEGER)
    if depth <= 0:
        raise SimpleBenchValueError("The 'depth' parameter must be a positive integer.",
                                   tag=_ImmutableErrorTag.DEPTH_NOT_POSITIVE_INTEGER)
    if message is not None and not isinstance(message, str):
        raise SimpleBenchTypeError("The 'message' parameter must be a string if provided.",
                                   tag=_ImmutableErrorTag.MESSAGE_NOT_STRING)
    message = message or "'{name}' must be immutable."
    formatted_message = message.format(name=name)
    if not _is_immutable(obj, parents=set(), depth=depth):
        raise SimpleBenchTypeError(formatted_message,
                                   tag=_ImmutableErrorTag.OBJECT_NOT_IMMUTABLE)
    return True

def is_immutable(obj: Any, depth: int = 200) -> bool:
    """Check if the given object is immutable.

    It recursively checks container types to ensure all contained elements are also immutable.

    :param Any obj: The object to check.
    :return bool: True if the object is immutable, False otherwise.
    """
    return _is_immutable(obj, parents=set(), depth=depth)

def _is_immutable(obj: Any, parents: set[int], depth: int) -> bool:
    """Helper function to check if the given object is immutable.

    It recursively checks container types to ensure all contained elements are also immutable.

    :param Any obj: The object to check.
    :return bool: True if the object is immutable, False otherwise.
    """
    new_id = id(obj)
    if new_id in parents:
        return True  # Prevent infinite recursion on cyclic references

    parents.add(new_id)

    if depth < len(parents):
        raise SimpleBenchRecursionError(
            f"Maximum recursion depth of {depth} reached while checking immutability.",
            tag=_ImmutableErrorTag.RECURSION_LIMIT_EXCEEDED)

    immutable: bool = False

    # Directly immutable types
    if isinstance(obj, Immutable) or isinstance(obj, IMMUTABLE_PRIMATIVE_TYPES_TUPLE):
        immutable = True

    # Immutable container types
    elif isinstance(obj, IMMUTABLE_CONTAINER_TYPES_TUPLE):
        if isinstance(obj, tuple):
            immutable = all(_is_immutable(item, parents, depth) for item in obj)
        elif isinstance(obj, frozenset):
            immutable = all(_is_immutable(item, parents, depth) for item in obj)
        elif isinstance(obj, MappingProxyType):
            immutable = all(
                _is_immutable(key, parents, depth)
                and _is_immutable(value, parents, depth) for key, value in obj.items())
        else:
            raise NotImplementedError(f"Unhandled immutable container type: {type(obj)}")

    # Frozen dataclasses
    elif is_dataclass(obj) and getattr(obj.__dataclass_params__, 'frozen', False):  # type: ignore[attr-defined]
        immutable = True
        for field in obj.__dataclass_fields__.values():
            value = getattr(obj, field.name, NO_ATTR)
            if value is NO_ATTR:
                continue
            if not _is_immutable(value, parents, depth):
                immutable = False
                break

    parents.remove(new_id)
    return immutable
