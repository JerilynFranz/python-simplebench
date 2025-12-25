"""Validation functions for CPUInfo report version v1"""
import math
import re
from types import NoneType
from typing import NamedTuple, TypeAlias

from simplebench.exceptions import SimpleBenchTypeError, SimpleBenchValueError
from simplebench.report._error_tags import _CPUInfoErrorTag
from simplebench.validators import validate_string, validate_string_with_regex, validate_type

_HASH_RE = re.compile(r'^[a-f0-9]{64}$')

def hash_id(value: str | None,
            name: str = 'hash_id',
            *,
            allow_none: bool = False,
            allow_empty: bool = False) -> str | None:
    """Validate the hash_id property of CPUInfo.

    .. note:: This is a composite validator, not a primitive.

       This function calls other, more basic validators internally. To avoid
       unintended behavior, such as circular dependencies,
       it should not be composed within other high-level validators without
       first inspecting its implementation to ensure it will avoid a case where
       two validators invoke each other recursively.

    The hash_id must be a 64-character hexadecimal string 
    or an empty string or None if allowed.

    - If passed as None and allow_none is True, None is returned.
    - If passed as an empty string and allow_empty is True, None is returned.

    :param value str | None: The hash_id string to validate.
    :param str name: The name of the property being validated (for error messages).
    :param bool allow_none: Whether to allow None as a valid value.
    :param bool allow_empty: Whether to allow an empty string as a valid value.
    :return str | None: The validated hash_id string or ``None``.
    :raises SimpleBenchTypeError: If the value is not a valid hash_id or ``None``.
    """
    if allow_none and value is None:
        return None

    value = validate_string(
        value, name,
        _CPUInfoErrorTag.INVALID_HASH_ID_PROPERTY_TYPE,
        _CPUInfoErrorTag.INVALID_HASH_ID_PROPERTY_VALUE,
        strip=True,
        allow_empty=allow_empty,
        message=f"{name} must be a string.")
    if allow_empty and value == '':
        return None

    return validate_string_with_regex(
              value, name, _HASH_RE,
              _CPUInfoErrorTag.INVALID_HASH_ID_PROPERTY_TYPE,
              _CPUInfoErrorTag.INVALID_HASH_ID_PROPERTY_VALUE,
              message=f"{name} must be a 64-character hexadecimal string")

DataTypes: TypeAlias = dict[str, "DataTypes"] | list["DataTypes"] | str | int | float | bool | NoneType


class PendingItem(NamedTuple):
    """A pending item for data validation.
    
    :param DataTypes item: The data item to validate.
    :param int depth: The current depth of the item in the data structure.
    """
    item: DataTypes
    depth: int


def data(value: dict[str, DataTypes]) -> dict[str, DataTypes]:
    """Validate the data property of CPUInfo.

    The data property must be a dictionary that contains the raw CPU information.

    .. note:: This is a composite validator, not a primitive.

       This function calls other, more basic validators internally. To avoid
       unintended behavior, such as circular dependencies,
       it should not be composed within other high-level validators without
       first inspecting its implementation to ensure it will avoid a case where
       two validators invoke each other recursively.

    It can have arbitrary keys and values but must be a dictionary consisting of
    - A tree composed of dictionaries, lists, strings, numbers, booleans, and nulls.
    - All keys in dictionaries must be non-blank, non-empty strings.
    - The tree structure must not contain cyclic references, unsupported types,
        non-finite floats (NaN, Infinity) or be deeply nested beyond reasonable limits
        (10 levels deep).
    
    :param dict[str, DataTypes] value: The data dictionary to validate.
    :return dict[str, DataTypes]: The validated data dictionary.
    :raises SimpleBenchTypeError: If the tree structure contains invalid types.
    :raises SimpleBenchValueError: If any dictionary key is a blank or empty string.
    """
    validate_type(
        value, dict, "data",
        _CPUInfoErrorTag.INVALID_DATA_PARAM_TYPE,
        message="{name} must be a dictionary.")

    max_depth: int = 10  # Arbitrary limit to prevent excessively deep nesting

    # Walk the data structure to ensure all elements are of allowed types
    pending_items: list[PendingItem] = [PendingItem(value, 0)]
    previously_seen: set[int] = set()
    while pending_items:
        current_item = pending_items.pop()
        depth = current_item.depth
        if depth > max_depth:
            raise SimpleBenchValueError(
                f"The data dictionary is too deeply nested (maximum depth is {max_depth}).",
                tag=_CPUInfoErrorTag.INVALID_DATA_PARAM_NESTING_DEPTH)
        item = current_item.item
        item_type = type(item)
        item_id = id(item)
        # Detect cyclic references
        if item_id in previously_seen:
            raise SimpleBenchTypeError(
                "Cyclic references are not allowed in the data dictionary.",
                tag=_CPUInfoErrorTag.INVALID_DATA_PARAM_CYCLIC_REFERENCE)
        previously_seen.add(item_id)
        if isinstance(item, (str, int, float, bool)) or item is None:
            # Check for non-finite floats (NaN, Infinity)
            if isinstance(item, float):
                if math.isnan(item) or math.isinf(item):
                    raise SimpleBenchValueError(
                        "Float values in the data dictionary cannot be NaN or Infinity.",
                        tag=_CPUInfoErrorTag.INVALID_DATA_PARAM_NON_FINITE_FLOAT)
            continue

        elif isinstance(item, list):
            for element in item:
                pending_items.append(PendingItem(element, depth + 1))

        elif isinstance(item, dict):
            for key, element in item.items():
                if not isinstance(key, str):
                    raise SimpleBenchTypeError(
                        f"All keys in the data dictionary must be strings. "
                        f"Invalid key: {key} of type {type(key).__name__}",
                        tag=_CPUInfoErrorTag.INVALID_DATA_PARAM_KEYS_TYPE)
                if key.strip() == '':
                    raise SimpleBenchValueError(
                        f"All keys in the data dictionary must be non-blank strings. "
                        f"Invalid key: '{key}'",
                        tag=_CPUInfoErrorTag.INVALID_DATA_PARAM_KEYS_VALUE)
                pending_items.append(PendingItem(element, depth + 1))

        else:
            raise SimpleBenchTypeError(
                f"Invalid data type for element in data dictionary: {item_type.__name__}. "
                f"Allowed types are dict, list, str, int, float, bool, and None.",
                tag=_CPUInfoErrorTag.INVALID_DATA_PARAM_TYPE)

    return value
