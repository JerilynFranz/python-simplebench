"""Provides validation for Immutable type hints."""
from typing import Any

from simplebench.types import Immutable

"""Validation functions for type hints and instances against those type hints."""
from types import MappingProxyType
from typing import Annotated, Any, get_args, get_origin

from simplebench.types import Immutable

from ._log import log
from ._options import Options
from ._primitives import ImmutablePrimitiveTypesTuple

__all__ = (
    "_is_immutable",
    "_is_immutable_data_typehint",
)

def _is_immutable(obj: Any) -> bool:
    """
    Check if an object is Immutable according to SimpleBench's definition.

    :param Any obj: The object to check.
    :return bool: True if the object is Immutable, False otherwise.
    """
    try:
        return isinstance(obj, Immutable)
    except (TypeError, ValueError, AttributeError):
        return False


def _is_immutable_data_typehint(type_hint: Any) -> bool:
    """
    Check if a type hint represents an immutable data type.

    :param Any type_hint: The type hint to check.
    :return bool: True if the type hint represents an immutable data type, False otherwise.
    """
    log.debug("_is_immutable_data_typehint: Checking if type hint '%s' is immutable", type_hint)
    origin = get_origin(type_hint)
    args = get_args(type_hint)

    if origin is Annotated:
        return _is_immutable_data_typehint(args[0])

    if type_hint in ImmutablePrimitiveTypesTuple:
        return True

    if origin is frozenset:
        if args:
            item_type = args[0]
            return _is_immutable_data_typehint(item_type)
        return True  # frozenset with no args is immutable

    if origin is tuple:
        if args and args[-1] is Ellipsis:
            item_type = args[0]
            return _is_immutable_data_typehint(item_type)
        for item_type in args:
            if not _is_immutable_data_typehint(item_type):
                return False
        return True

    if origin is MappingProxyType:
        if len(args) == 2:
            key_type, value_type = args
            return (_is_immutable_data_typehint(key_type)
                    and _is_immutable_data_typehint(value_type))
        return True  # MappingProxyType with no args is immutable

    return False
