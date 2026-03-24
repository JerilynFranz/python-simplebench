"""Validation functions for CPUInfo report version v1"""

import re
from typing import Any, cast

from typeguard import TypeCheckError, check_type

from simplebench.exceptions import SimpleBenchTypeError
from simplebench.report._error_tags import _CPUInfoErrorTag
from simplebench.simplebench_types import CoreDataMapping
from simplebench.validators import validate_core_data_mapping, validate_string, validate_string_with_regex

from .cpu_info_dict import CPUInfoData, ImmutableCPUInfoData

_HASH_RE = re.compile(r'^[a-f0-9]{64}$')


def hash_id(value: str) -> str:
    """Validate the hash_id property of CPUInfo.

    .. note:: This is a composible validator that is safe to use within other validators.

        It only depends on primitive validators and does not create circular dependencies.

    The hash_id must be a 64-character hexadecimal string or an empty string.

    :param value str: The hash_id string to validate.
    :return str: The validated hash_id string or an empty string.
    :raises SimpleBenchTypeError: If the value is not a valid hash_id, an empty string, or not a string at all.
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

    .. note:: This is a complex, high-level validator. It depends on other validators.

       This function calls multiple other validators internally. To avoid
       unintended behavior, such as circular dependencies,
       it should not be composed within other high-level validators without
       first inspecting its implementation to ensure it will avoid a case where
       two validators invoke each other recursively.

    It can have arbitrary keys and values but must be a dictionary consisting of
    - A tree composed of dictionaries, lists, strings, numbers, booleans, and nulls.
    - All keys in dictionaries must be non-blank, non-empty strings that are
        valid identifiers (matching regex `^[A-Za-z_][A-Za-z0-9_]*$`).
    - The tree structure must not contain cyclic references, unsupported types,
        or non-finite floats (NaN, Infinity).

    :param Any value: The data dictionary to validate. Should conform to `CPUInfoData` TypedDict.
    :return ImmutableCPUInfoData: The validated data dictionary as an immutable mapping.
    :raises SimpleBenchValueError: If any key in the dictionary is not a non-blank,
        non-empty string that is a valid identifier, or if the structure contains
        unsupported types or cycles.
    :raises SimpleBenchTypeError: If the value is not a valid dictionary.
    """
    from simplebench import environment
    if isinstance(value, environment.CPUInfo):
        dict_value = value.to_dict().thaw()  # type: ignore[attr-defined]
    elif isinstance(value, CoreDataMapping):
        dict_value = value.thaw()
    else:
        dict_value = value

    try:
        check_type(dict_value, CPUInfoData)

    except TypeCheckError as exc:
        raise SimpleBenchTypeError(
            f'CPUInfo.data must be a dictionary with string keys and values of valid types, got {value!r}.',
            tag=_CPUInfoErrorTag.INVALID_DATA_PROPERTY_TYPE,
        ) from exc

    # if was already ImmutableCPUInfoData, just return the original
    # immutable object now that its type checked against CPUInfoData
    if isinstance(value, environment.CPUInfo):
        return value.to_dict()

    return cast(ImmutableCPUInfoData, validate_core_data_mapping(dict_value, 'CPUInfo.data'))
