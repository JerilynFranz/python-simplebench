"""Validation functions for MachineInfo version 1."""

import re

from simplebench.report._error_tags import _MemoryInfoErrorTag
from simplebench.validators import validate_string, validate_string_with_regex, validate_type

from .swap_memory import SwapMemoryObject
from .virtual_memory import VirtualMemoryObject

_HASH_RE: re.Pattern[str] = re.compile(r'^[a-f0-9]{64}$')
"""Regular expression pattern for validating 64-character hexadecimal strings."""

__all__ = []


def hash_id(value: str) -> str:
    """Validate hash_id property.

    It is validated to be a 64-character hexadecimal string or an empty string.

    :param str value: The hash_id string to validate.
    :return str: The validated hash_id string.
    :raises SimpleBenchTypeError: If value is not a string.
    :raises SimpleBenchValueError: If value is not either empty or a 64-character hexadecimal string
    """
    hash_string = validate_string(
        value,
        'hash_id',
        _MemoryInfoErrorTag.INVALID_HASH_ID_TYPE,
        _MemoryInfoErrorTag.INVALID_HASH_ID_VALUE,
        allow_empty=True,
        strip=True,
    )
    if hash_string == '':
        return ''

    return validate_string_with_regex(
        hash_string,
        'hash_id',
        _HASH_RE,
        _MemoryInfoErrorTag.INVALID_HASH_ID_TYPE,
        _MemoryInfoErrorTag.INVALID_HASH_ID_VALUE,
        message='{name} must be 64-character hexadecimal string. Found: {value}',
    )


def swap_memory(value: SwapMemoryObject) -> SwapMemoryObject:
    """Validate swap_memory property.

    :param SwapMemoryObject value: The swap_memory value to validate.
    :return SwapMemoryObject: The validated swap_memory value.
    :raises SimpleBenchTypeError: If value is not a SwapMemoryObject.
    :raises SimpleBenchValueError: If value is invalid.
    """
    return validate_type(value, SwapMemoryObject, 'swap_memory', _MemoryInfoErrorTag.INVALID_SWAP_MEMORY_TYPE)


def virtual_memory(value: VirtualMemoryObject) -> VirtualMemoryObject:
    """Validate virtual_memory property.

    :param VirtualMemoryObject value: The virtual_memory value to validate.
    :return VirtualMemoryObject: The validated virtual_memory value.
    :raises SimpleBenchTypeError: If value is not a VirtualMemoryObject.
    :raises SimpleBenchValueError: If value is invalid.
    """
    return validate_type(value, VirtualMemoryObject, 'virtual_memory', _MemoryInfoErrorTag.INVALID_VIRTUAL_MEMORY_TYPE)
