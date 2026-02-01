"""Validation functions for SystemInfo version 1."""

import re

from simplebench.report._error_tags import _SystemInfoErrorTag
from simplebench.validators import validate_string, validate_string_with_regex

_HASH_RE: re.Pattern = re.compile(r'^[a-f0-9]{64}$')
"""Regular expression pattern for validating 64-character hexadecimal strings."""

__all__: list[str] = []


def hash_id(value: str) -> str:
    """Validate hash_id property.

    It is validated to be a 64-character hexadecimal string or an empty string.

    :param str value: The hash_id string to validate.
    :return str: The validated hash_id string.
    :raises SimpleBenchTypeError: If value is not a string.
    :raises SimpleBenchValueError: If value is not a 64-character hexadecimal string
    """
    hash_string = validate_string(
        value,
        'hash_id',
        _SystemInfoErrorTag.INVALID_HASH_ID_TYPE,
        _SystemInfoErrorTag.INVALID_HASH_ID_VALUE,
        allow_empty=True,
        strip=True,
    )
    if hash_string == '':
        return ''

    return validate_string_with_regex(
        hash_string,
        'hash_id',
        _HASH_RE,
        _SystemInfoErrorTag.INVALID_HASH_ID_TYPE,
        _SystemInfoErrorTag.INVALID_HASH_ID_VALUE,
        message='{name} must be 64-character hexadecimal string. Found: {value}',
    )


def system(value: str) -> str:
    """Validate system property.

    :param str value: The system string to validate.
    :return str: The validated system string.
    :raises SimpleBenchTypeError: If value is not a string.
    :raises SimpleBenchValueError: If value is empty.
    """
    return validate_string(
        value,
        'system',
        _SystemInfoErrorTag.INVALID_SYSTEM_TYPE,
        _SystemInfoErrorTag.EMPTY_SYSTEM_VALUE,
        allow_empty=False,
        strip=True,
    )


def system_version(value: str) -> str:
    """Validate system_version property.

    :param str value: The system_version string to validate.
    :return str: The validated system_version string.
    :raises SimpleBenchTypeError: If value is not a string.
    :raises SimpleBenchValueError: If value is empty.
    """
    return validate_string(
        value,
        'system_version',
        _SystemInfoErrorTag.INVALID_SYSTEM_VERSION_TYPE,
        _SystemInfoErrorTag.EMPTY_SYSTEM_VERSION_VALUE,
        allow_empty=False,
        strip=True,
    )


def release(value: str) -> str:
    """Validate release property.

    :param str value: The release string to validate.
    :return str: The validated release string.
    :raises SimpleBenchTypeError: If value is not a string.
    :raises SimpleBenchValueError: If value is empty.
    """
    return validate_string(
        value,
        'release',
        _SystemInfoErrorTag.INVALID_RELEASE_TYPE,
        _SystemInfoErrorTag.EMPTY_RELEASE_VALUE,
        allow_empty=False,
        strip=True,
    )


def machine(value: str) -> str:
    """Validate machine property.

    :param str value: The machine string to validate.
    :return str: The validated machine string.
    :raises SimpleBenchTypeError: If value is not a string.
    :raises SimpleBenchValueError: If value is empty.
    """
    return validate_string(
        value,
        'machine',
        _SystemInfoErrorTag.INVALID_MACHINE_TYPE,
        _SystemInfoErrorTag.EMPTY_MACHINE_VALUE,
        allow_empty=False,
        strip=True,
    )
