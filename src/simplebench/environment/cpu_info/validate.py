"""Validators for environment.cpu_info module."""
import math

from simplebench.exceptions import SimpleBenchTypeError, SimpleBenchValueError
from simplebench.validators import validate_bool, validate_string, validate_type

from ._error_tags import _CPUInfoErrorTag
from .types import CPUInfoDataTypes, CPUInfoDictType


class PendingItem:
    """Helper class to represent an item pending validation in the data tree."""

    def __init__(self, item: CPUInfoDataTypes, depth: int) -> None:
        """Initialize a PendingItem instance.

        :param CPUInfoDataTypes item: The item to be validated.
        :param int depth: The current depth of the item in the data tree.
        """
        self.item: CPUInfoDataTypes = item
        self.depth: int = depth

def use_cache(value: bool) -> bool:
    """Validate the use_cache parameter.

    This function checks if the `use_cache` parameter is a boolean value.
    
    :param bool value: Indicates whether to use cached CPU information.
    :return bool: The validated `use_cache` value.
    :raises SimpleBenchTypeError: If `use_cache` is not a boolean.
    """
    return validate_bool(
        value, "use_cache",
        _CPUInfoErrorTag.INVALID_USE_CACHE_TYPE)

def detached(value: bool) -> bool:
    """Validate the detached parameter.

    This function checks if the `detached` parameter is a boolean value.
    
    :param bool value: Indicates whether the CPU information should be detached from future changes.
    :return bool: The validated `detached` value.
    :raises SimpleBenchTypeError: If `detached` is not a boolean.
    """
    return validate_bool(
        value, "detached",
        _CPUInfoErrorTag.INVALID_DETACHED_TYPE)

def use_cache_and_detached(use_cache_value: bool, detached_value: bool) -> None:
    """Validate the use_cache and detached parameters for CPUInfo initialization.

    This function checks the types and the combination of `use_cache` and `detached`
    parameters to ensure they are valid according to the following rules:
    - `use_cache` and `detached` must both be boolean values.
    - If `use_cache` is `False` and `detached` is `False`, a `SimpleBenchValueError` is raised
      because this combination does not make sense.
    
    :param bool use_cache_value: Indicates whether to use cached CPU information.
    :param bool detached: Indicates whether the CPU information should be detached from future changes.
    :raises SimpleBenchValueError: If the combination of parameters is invalid.
    """
    use_cache(use_cache_value)
    detached(detached_value)

    if not use_cache and not detached:
        raise SimpleBenchValueError(
            "Invalid combination: 'use_cache' cannot be False when 'detached' is also False.",
            tag=_CPUInfoErrorTag.INVALID_USE_CACHE_AND_DETACHED_COMBINATION)


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
