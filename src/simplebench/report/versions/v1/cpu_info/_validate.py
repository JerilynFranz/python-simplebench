"""Validation functions for CPUInfo report version v1"""

import re
from typing import Any, cast

from typechecked import is_immutable

from simplebench.exceptions import SimpleBenchTypeError
from simplebench.report._error_tags import _CPUInfoErrorTag
from simplebench.validators import validate_core_data_mapping, validate_string, validate_string_with_regex

from .typeddict_types import ImmutableCPUInfoData

_HASH_RE = re.compile(r'^[a-f0-9]{64}$')


def hash_id(value: str) -> str:
    """Validate the hash_id property of CPUInfo.

    .. note:: This is a composite validator, not a primitive.

       This function calls other, more basic validators internally. To avoid
       unintended behavior, such as circular dependencies,
       it should not be composed within other high-level validators without
       first inspecting its implementation to ensure it will avoid a case where
       two validators invoke each other recursively.

    The hash_id must be a 64-character hexadecimal string or an empty string.

    :param value str: The hash_id string to validate.
    :return str: The validated hash_id string or.
    :raises SimpleBenchTypeError: If the value is not a valid hash_id or an empty string or.
    """

    value = validate_string(
        value,
        'hash_id',
        _CPUInfoErrorTag.INVALID_HASH_ID_PROPERTY_TYPE,
        _CPUInfoErrorTag.INVALID_HASH_ID_PROPERTY_VALUE,
        strip=True,
        allow_empty=True,
        message='hash_id must be a string.',
    )
    if value == '':
        return ''

    return validate_string_with_regex(
        value,
        'hash_id',
        _HASH_RE,
        _CPUInfoErrorTag.INVALID_HASH_ID_PROPERTY_TYPE,
        _CPUInfoErrorTag.INVALID_HASH_ID_PROPERTY_VALUE,
        message='hash_id must be a 64-character hexadecimal string',
    )


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
    from simplebench.environment import CPUInfo as EnvCPUInfo

    if not isinstance(value, EnvCPUInfo):
        raise SimpleBenchTypeError(
            f'CPUInfo.data must be an instance of simplebench.environment.CPUInfo, got {type(value).__name__}.',
            tag=_CPUInfoErrorTag.INVALID_DATA_PROPERTY_TYPE,
        )

    unpacked_value = value.to_dict()
    if is_immutable(unpacked_value):
        return cast(ImmutableCPUInfoData, value)

    immutable_value = validate_core_data_mapping(unpacked_value, 'CPUInfo.data', max_depth=10)
    return cast(ImmutableCPUInfoData, immutable_value)
