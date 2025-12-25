"""Validators for environment.cpu_info module."""
import math

from simplebench.exceptions import SimpleBenchTypeError, SimpleBenchValueError
from simplebench.validators import validate_bool, validate_string, validate_type

from ._error_tags import _CPUInfoErrorTag
from .types import CPUInfoDataTypes, CPUInfoDictType


def cache_key(value: str | None) -> str | None:
    """Validate the cache_key parameter.

    The cache_key must be a non-blank string containing only alphanumeric characters.

    :param str | None value: The cache_key string to validate.
    :return str | None: The validated cache_key string.
    :raises SimpleBenchTypeError: If the value is not a string or ``None``.
    :raises SimpleBenchValueError: If the value is not a non-blank alphanumeric string.
    """
    if value is None:
        return None
    return validate_string(
        value, "cache_key",
        _CPUInfoErrorTag.INVALID_CACHE_KEY_PARAM_TYPE,
        _CPUInfoErrorTag.INVALID_CACHE_KEY_PARAM_VALUE,
        strip=False, allow_empty=False, alphanumeric_only=True,
        message="cache_key must be a non-empty string containing only alphanumeric characters.")

class PendingItem:
    """Helper class to represent an item pending validation in the data tree."""

    def __init__(self, item: CPUInfoDataTypes, depth: int) -> None:
        """Initialize a PendingItem instance.

        :param CPUInfoDataTypes item: The item to be validated.
        :param int depth: The current depth of the item in the data tree.
        """
        self.item: CPUInfoDataTypes = item
        self.depth: int = depth

def cpu_info_dict(name: str, value: CPUInfoDictType) -> CPUInfoDictType:
    """Validate a CPUInfoDictType.

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
    
    :param CPUInfoDictType value: The data dictionary to validate.
    :return CPUInfoDictType: The validated data dictionary.
    :raises SimpleBenchTypeError: If the tree structure contains invalid types.
    :raises SimpleBenchValueError: If any dictionary key is a blank or empty string.
    """
    validate_string(
        name, "name",
        _CPUInfoErrorTag.INVALID_NAME_PARAM_TYPE,
        _CPUInfoErrorTag.INVALID_NAME_PARAM_VALUE,
        message="`name` parameter must be a non-blank string.")
    validate_type(
        value, dict, "data",
        _CPUInfoErrorTag.INVALID_DATA_PARAM_TYPE,
        message="`{name}` parameter must be a dictionary.")

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
