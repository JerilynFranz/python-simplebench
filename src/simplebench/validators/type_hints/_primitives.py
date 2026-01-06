"""Helper function to validate primitive types against type hints."""
from types import NoneType
from typing import Any, TypeAlias

from ._log import log


__all__ = (
    "ImmutablePrimitiveTypes",
    "ImmutablePrimitiveTypesTuple",
    "IMMUTABLE_PRIMITIVE_TYPES_SET",
    "_is_primitive_typehint",
    "_is_primitive",
)

ImmutablePrimitiveTypes: TypeAlias = int | str | bytes | bool | float | complex | NoneType
"""Type alias for primitive data types."""

ImmutablePrimitiveTypesTuple: tuple[type[int] | type[str] | type[bytes]  # pylint: disable=invalid-name
        | type[bool] | type[float] | type[complex] | type[NoneType], ...] = (
            int, str, bytes, bool, float, complex, NoneType)
"""Tuple of primitive data types for isinstance checks."""

IMMUTABLE_PRIMITIVE_TYPES_SET: set[Any] = set(ImmutablePrimitiveTypesTuple)
"""Set of primitive data types for quick membership checks.

`None` is included as a special case.
"""


def _is_primitive_typehint(type_hint: Any) -> bool:
    """
    Check if a type hint directly represents a primitive data type.

    Primitive data types include: int, str, bytes, bool, float, complex, type(None).

    The value of `None` is special cased to be treated as `type(None)`.

    :param Any type_hint: The type hint to check.
    :return bool: True if the type hint represents a primitive data type, False otherwise.
    """
    if type_hint is None:
        type_hint = NoneType
    return type_hint in IMMUTABLE_PRIMITIVE_TYPES_SET

def _is_primitive(obj: Any) -> bool:
    """
    Check if an object is a primitive data type according to ImmutablePrimitiveTypes.

    If the object is `None`, it is considered a primitive.

    :param Any obj: The object to check.
    :return bool: True if the object is a primitive data type, False otherwise.
    """
    log.debug("_is_primitive: Checking if object of type '%s' isinstance of  '%s'",
              type(obj).__name__, ImmutablePrimitiveTypesTuple)
    if obj is None:
        return True
    try:
        return isinstance(obj, ImmutablePrimitiveTypesTuple)
    except (TypeError, ValueError, AttributeError):
        return False
