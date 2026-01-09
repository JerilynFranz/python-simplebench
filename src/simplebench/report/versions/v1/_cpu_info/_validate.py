"""Validation functions for CPUInfo report version v1"""
import re
from typing import Any, cast

from typechecked import is_immutable, isinstance_of_typehint

from simplebench.exceptions import SimpleBenchTypeError
from simplebench.report._error_tags import _CPUInfoErrorTag
from simplebench.validators import validate_core_data_mapping, validate_string, validate_string_with_regex

from ..types import CPUInfoData, ImmutableCPUInfoData

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


def data(value: Any) -> ImmutableCPUInfoData:
    """Validate the data property of CPUInfo.

    The data property must be a dictionary that contains the raw CPU information.

    .. note:: This is a composite validator, not a primitive.

       This function calls other, more basic, validators internally. To avoid
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
    
    :param Any value: The data dictionary to validate. Should conform to `CPUInfoData` TypedDict.
    :return ImmutableCPUInfoData: The validated data dictionary as an immutable mapping.
    :raises SimpleBenchValueError: If any key in the dictionary is not a non-blank,
        non-empty string, or if the structure contains unsupported types or cycles.
    :raises SimpleBenchTypeError: If the value is not a valid dictionary.
    """
    if not isinstance_of_typehint(value, CPUInfoData):
        raise SimpleBenchTypeError(
            "CPUInfo.data must be a 'CPUInfoData' TypedDict - validation failed.",
            tag=_CPUInfoErrorTag.INVALID_DATA_ARG_TYPE)
    if is_immutable(value):
        return cast(ImmutableCPUInfoData, value)

    immutable_value = validate_core_data_mapping(value, 'CPUInfo.data', max_depth=10)
    return cast(ImmutableCPUInfoData, immutable_value)
