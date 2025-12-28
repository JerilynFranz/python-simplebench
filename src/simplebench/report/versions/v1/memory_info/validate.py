"""Validation functions for MachineInfo version 1."""
import re

from simplebench.report._error_tags import _MemoryInfoErrorTag
from simplebench.validators import validate_non_negative_int, validate_string, validate_string_with_regex

_HASH_RE: re.Pattern = re.compile(r'^[a-f0-9]{64}$')
"""Regular expression pattern for validating 64-character hexadecimal strings."""

def hash_id(value: str) -> str:
    """Validate hash_id property.

    It is validated to be a 64-character hexadecimal string or an empty string.

    :param str value: The hash_id string to validate.
    :return str: The validated hash_id string.
    :raises SimpleBenchTypeError: If value is not a string.
    :raises SimpleBenchValueError: If value is not a 64-character hexadecimal string
    """
    hash_string = validate_string(
        value, "hash_id",
        _MemoryInfoErrorTag.INVALID_HASH_ID_TYPE,
        _MemoryInfoErrorTag.INVALID_HASH_ID_VALUE,
        allow_empty=True, strip=True)
    if hash_string == '':
        return ''

    return validate_string_with_regex(
        hash_string, "hash_id", _HASH_RE,
        _MemoryInfoErrorTag.INVALID_HASH_ID_TYPE,
        _MemoryInfoErrorTag.INVALID_HASH_ID_VALUE,
        message="{name} must be 64-character hexadecimal string. Found: {value}"
    )

def total_physical(value: int) -> int:
    """Validate total_physical value.

    :param int value: The total_physical value to validate.
    :return int: The validated total_physical value.
    :raises SimpleBenchTypeError: If value is not an integer.
    :raises SimpleBenchValueError: If value is negative.
    """
    return validate_non_negative_int(
        value, "total_physical",
        _MemoryInfoErrorTag.INVALID_TOTAL_PHYSICAL_TYPE,
        _MemoryInfoErrorTag.NEGATIVE_TOTAL_PHYSICAL_VALUE
    )

def total_swap(value: int) -> int:
    """Validate total_swap value.

    :param int value: The total_swap value to validate.
    :return int: The validated total_swap value.
    :raises SimpleBenchTypeError: If value is not an integer.
    :raises SimpleBenchValueError: If value is negative.
    """
    return validate_non_negative_int(
        value, "total_swap",
        _MemoryInfoErrorTag.INVALID_TOTAL_SWAP_TYPE,
        _MemoryInfoErrorTag.NEGATIVE_TOTAL_SWAP_VALUE
    )
