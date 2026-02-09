"""Module for immutable validation functions."""
from dataclasses import is_dataclass
from enum import Enum
from types import MappingProxyType, NoneType
from typing import Annotated, Any, TypeGuard, get_args, get_origin, is_typeddict

from simplebench._log import _log
from simplebench.exceptions import SimpleBenchRecursionError, SimpleBenchTypeError, SimpleBenchValueError

from ._error_tags import _ImmutableErrorTag
from ._protocol import Immutable, ImmutableTypedDict

__all__ = (
    "validate_immutable",
    "is_immutable",
    "is_immutable_typeddict_typehint",
    "is_immutable_data_typehint",
    "Immutable",
    "ImmutableTypedDict",
)


class _NoAttrSentinel:
    """Sentinel class to represent absence of an attribute."""


_NO_ATTR = _NoAttrSentinel()

IMMUTABLE_PRIMITIVE_TYPES_TUPLE: tuple[type, ...] = (int, float, complex, bool, str, bytes, NoneType, Enum, range)
IMMUTABLE_CONTAINER_TYPES_TUPLE: tuple[type, ...] = (tuple, frozenset, MappingProxyType)
IMMUTABLE_PRIMITIVE_TYPES_SET: set[type] = set(IMMUTABLE_PRIMITIVE_TYPES_TUPLE)


def validate_immutable(obj: Any, name: str, message: str | None = None, depth: int = 200) -> bool:
    """Validate that the given object is immutable.

    It recursively checks container types to ensure all contained elements are also immutable.

    The 'name' parameter is used in the error message to identify the object being validated.

    :param Any obj: The object to check.
    :param str name: The name of the object being validated.
    :param str | None message: Custom error message to use if validation fails. If None, a default message is used.
    :param int depth: Maximum recursion depth to prevent infinite loops on cyclic references.
    :return bool: True if the object is immutable.

    :raises SimpleBenchTypeError: If the object is not immutable
    :raises SimpleBenchTypeError: If the calling parameters are of incorrect types.
    :raises SimpleBenchValueError: If the calling parameters have invalid values.
    """
    if not isinstance(name, str):
        raise SimpleBenchTypeError(
            "The 'name' parameter must be a string.",
            tag=_ImmutableErrorTag.NAME_NOT_STRING)
    if name.strip() == "":
        raise SimpleBenchValueError(
            "The 'name' parameter must be a non-blank string.",
            tag=_ImmutableErrorTag.NAME_IS_EMPTY_OR_BLANK_STRING)
    if not isinstance(depth, int):
        raise SimpleBenchTypeError(
            "The 'depth' parameter must be an integer.",
            tag=_ImmutableErrorTag.DEPTH_NOT_INTEGER)
    if depth <= 0:
        raise SimpleBenchValueError(
            "The 'depth' parameter must be a positive integer.",
            tag=_ImmutableErrorTag.DEPTH_NOT_POSITIVE_INTEGER)
    if message is not None and not isinstance(message, str):
        raise SimpleBenchTypeError(
            "The 'message' parameter must be a string if provided.",
            tag=_ImmutableErrorTag.MESSAGE_NOT_STRING)
    message = message or "'{name}' must be immutable."
    formatted_message = message.format(name=name)
    if not _is_immutable(obj, parents=set(), depth=depth):
        raise SimpleBenchTypeError(
            formatted_message,
            tag=_ImmutableErrorTag.OBJECT_NOT_IMMUTABLE)
    return True


def is_immutable(obj: Any, depth: int = 200) -> bool:
    """Check if the given object is immutable.

    It recursively checks container types to ensure all contained elements are also immutable.

    :param Any obj: The object to check.
    :param int depth: Maximum recursion depth to prevent infinite loops on cyclic references.
    :return bool: True if the object is immutable, False otherwise.
    :raises TypeError: If the 'depth' parameter is not an integer.
    :raises ValueError: If the 'depth' parameter is not a positive integer.
    :raises RecursionError: If the maximum recursion depth is exceeded.
    """
    return _is_immutable(obj, parents=set(), depth=depth)


def _is_immutable(obj: Any, parents: set[int], depth: int) -> bool:
    """Helper function to check if the given object is immutable.

    It recursively checks container types to ensure all contained elements are also immutable.

    :param Any obj: The object to check.
    :param set[int] parents: Set of object IDs to detect cycles.
    :param int depth: Maximum recursion depth to prevent infinite loops on cyclic references.
    :return bool: True if the object is immutable, False otherwise.
    :raises TypeError: If the 'depth' parameter is not an integer.
    :raises RecursionError: If the maximum recursion depth is exceeded.
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
    if isinstance(obj, Immutable) or isinstance(obj, IMMUTABLE_PRIMITIVE_TYPES_TUPLE):
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
    elif is_dataclass(obj) and getattr(
            obj.__dataclass_params__, 'frozen', False):  # type: ignore[attr-defined, union-attr]
        immutable = True
        for field in obj.__dataclass_fields__.values():
            value = getattr(obj, field.name, _NO_ATTR)
            if value is _NO_ATTR:
                continue
            if not _is_immutable(value, parents, depth):
                immutable = False
                break

    parents.remove(new_id)
    return immutable


def is_immutable_typeddict_typehint(type_hint: Any) -> TypeGuard[type[ImmutableTypedDict]]:
    """
    Safely check if a type hint inherits from :class:`~simplebench.simplebench_types.ImmutableTypedDict`.

    This function is a TypeGuard, which allows static type checkers to understand
    that if this function returns True, the given `type_hint` is a class
    that inherits from ImmutableTypedDict.

    :param Any type_hint: The type hint to check.
    :return bool: True if the type hint inherits from ImmutableTypedDict, False otherwise.
    """
    if not is_typeddict(type_hint):
        return False
    try:
        # Check the MRO directly to see if it inherits from ImmutableTypedDict.
        # This avoids the static checker issue with issubclass and TypedDict.
        return ImmutableTypedDict in type_hint.__mro__
    except (TypeError, AttributeError):
        # issubclass would raise TypeError; __mro__ might raise AttributeError
        # if type_hint is not a class.
        return False


def is_immutable_data_typehint(type_hint: Any) -> bool:
    """
    Check if a type hint represents an immutable data type.

    :param Any type_hint: The type hint to check.
    :return bool: True if the type hint represents an immutable data type, False otherwise.
    """
    _log.debug("_is_immutable_data_typehint: Checking if type hint '%s' is immutable", type_hint)
    origin = get_origin(type_hint)
    args = get_args(type_hint)

    if origin is Annotated:
        return is_immutable_data_typehint(args[0])

    if type_hint in IMMUTABLE_PRIMITIVE_TYPES_SET:
        return True

    if origin is frozenset:
        if args:
            item_type = args[0]
            return is_immutable_data_typehint(item_type)
        return True  # frozenset with no args is immutable

    if origin is tuple:
        if args and args[-1] is Ellipsis:
            item_type = args[0]
            return is_immutable_data_typehint(item_type)
        for item_type in args:
            if not is_immutable_data_typehint(item_type):
                return False
        return True

    if origin is MappingProxyType:
        if len(args) == 2:
            key_type, value_type = args
            return (is_immutable_data_typehint(key_type)
                    and is_immutable_data_typehint(value_type))
        return True  # MappingProxyType with no args is immutable

    return False
