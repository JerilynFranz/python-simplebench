"""Validation functions for CPUInfo report version v1"""
import re
from types import NoneType
from typing import TypeAlias

from simplebench.exceptions import SimpleBenchTypeError, SimpleBenchValueError
from simplebench.report._error_tags import _CPUInfoErrorTag
from simplebench.validators import validate_string_with_regex, validate_type

_HASH_RE = re.compile(r'^[a-f0-9]{64}$')

def hash_id(value: str, name: str = '') -> str:
    """Validate the hash_id property of CPUInfo.

    :param value: The hash_id string to validate.
    :return: The validated hash_id string.
    :raises SimpleBenchTypeError: If the value is not a valid hash_id.
    """
    return validate_string_with_regex(
              value, name, _HASH_RE,
              _CPUInfoErrorTag.INVALID_HASH_ID_PROPERTY_TYPE,
              _CPUInfoErrorTag.INVALID_HASH_ID_PROPERTY_VALUE,
              message="hash_id must be a valid SHA-256 hexadecimal string")

DataTypes: TypeAlias = dict[str, "DataTypes"] | list["DataTypes"] | str | int | float | bool | NoneType

def data(value: dict[str, DataTypes]) -> dict[str, DataTypes]:
    """Validate the data property of CPUInfo.

    The data property must be a dictionary that contains the raw CPU information.

    It can have arbitrary keys and values but must be a dictionary consisting of
    - A tree composed of dictionaries, lists, strings, numbers, booleans, and nulls.
    - All keys in dictionaries must be non-blank, non-empty strings.
    
    :param dict[str, DataTypes] value: The data dictionary to validate.
    :return dict[str, DataTypes]: The validated data dictionary.
    :raises SimpleBenchTypeError: If the tree structure contains invalid types.
    :raises SimpleBenchValueError: If any dictionary key is a blank or empty string.
    """
    validate_type(
        value, dict, "data",
        _CPUInfoErrorTag.INVALID_DATA_PARAM_TYPE,
        message="{name} must be a dictionary.")

    # Walk the data structure to ensure all elements are of allowed types
    pending_items: list[DataTypes] = [value]
    while pending_items:
        current_item = pending_items.pop()
        item_type = type(current_item)
        if isinstance(current_item, (str, int, float, bool)) or current_item is None:
            continue

        elif isinstance(current_item, list):
            for element in current_item:
                pending_items.append(element)

        elif isinstance(current_item, dict):
            for key, element in current_item.items():
                if not isinstance(key, str):
                    raise SimpleBenchTypeError(
                        f"All keys in the data dictionary must be strings. "
                        f"Invalid key: {key} of type {type(key).__name__}",
                        tag=_CPUInfoErrorTag.INVALID_DATA_PARAM_KEYS_TYPE)
                if key.strip() == '':
                    raise SimpleBenchValueError(
                        f"All keys in the data dictionary must be non-blank strings. "
                        f"Invalid key: '{key}'",
                        tag=_CPUInfoErrorTag.INVALID_DATA_PARAM_KEYS_TYPE)
                pending_items.append(element)    

        else:
            raise SimpleBenchTypeError(
                f"Invalid data type for element in data dictionary: {item_type.__name__}. "
                f"Allowed types are dict, list, str, int, float, bool, and None.",
                tag=_CPUInfoErrorTag.INVALID_DATA_PARAM_TYPE)

    return value
