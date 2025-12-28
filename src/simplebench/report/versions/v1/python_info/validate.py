"""Validation functions for MachineInfo version 1."""
import re

from simplebench.report._error_tags import _PythonInfoErrorTag
from simplebench.validators import validate_string, validate_string_with_regex

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
        _PythonInfoErrorTag.INVALID_HASH_ID_TYPE,
        _PythonInfoErrorTag.INVALID_HASH_ID_VALUE,
        allow_empty=True, strip=True)
    if hash_string == '':
        return ''

    return validate_string_with_regex(
        hash_string, "hash_id", _HASH_RE,
        _PythonInfoErrorTag.INVALID_HASH_ID_TYPE,
        _PythonInfoErrorTag.INVALID_HASH_ID_VALUE,
        message="{name} must be 64-character hexadecimal string. Found: {value}"
    )

def compiler(value: str) -> str:
    """Validate compiler property.

    :param str value: The compiler string to validate.
    :return str: The validated compiler string.
    :raises SimpleBenchTypeError: If value is not a string.
    :raises SimpleBenchValueError: If value is empty.
    """
    return validate_string(
        value, "compiler",
        _PythonInfoErrorTag.INVALID_COMPILER_TYPE,
        _PythonInfoErrorTag.EMPTY_COMPILER_VALUE,
        allow_empty=False, strip=True
    )

def implementation(value: str) -> str:
    """Validate implementation property.

    :param str value: The implementation string to validate.
    :return str: The validated implementation string.
    :raises SimpleBenchTypeError: If value is not a string.
    :raises SimpleBenchValueError: If value is empty.
    """
    return validate_string(
        value, "implementation",
        _PythonInfoErrorTag.INVALID_IMPLEMENTATION_TYPE,
        _PythonInfoErrorTag.EMPTY_IMPLEMENTATION_VALUE,
        allow_empty=False, strip=True
    )

def implementation_version(value: str) -> str:
    """Validate implementation_version property.

    :param str value: The implementation_version string to validate.
    :return str: The validated implementation_version string.
    :raises SimpleBenchTypeError: If value is not a string.
    :raises SimpleBenchValueError: If value is empty.
    """
    return validate_string(
        value, "implementation_version",
        _PythonInfoErrorTag.INVALID_IMPLEMENTATION_VERSION_TYPE,
        _PythonInfoErrorTag.EMPTY_IMPLEMENTATION_VERSION_VALUE,
        allow_empty=False, strip=True
    )

def python_version(value: str) -> str:
    """Validate python_version property.

    :param str value: The python_version string to validate.
    :return str: The validated python_version string.
    :raises SimpleBenchTypeError: If value is not a string.
    :raises SimpleBenchValueError: If value is empty.
    """
    return validate_string(
        value, "python_version",
        _PythonInfoErrorTag.INVALID_PYTHON_VERSION_TYPE,
        _PythonInfoErrorTag.EMPTY_PYTHON_VERSION_VALUE,
        allow_empty=False, strip=True
    )

def build(value: str) -> str:
    """Validate build property.

    :param str value: The build string to validate.
    :return str: The validated build string.
    :raises SimpleBenchTypeError: If value is not a string.
    :raises SimpleBenchValueError: If value is empty.
    """
    return validate_string(
        value, "build",
        _PythonInfoErrorTag.INVALID_BUILD_TYPE,
        _PythonInfoErrorTag.EMPTY_BUILD_VALUE,
        allow_empty=False, strip=True
    )

def release(value: str) -> str:
    """Validate release property.

    :param str value: The release string to validate.
    :return str: The validated release string.
    :raises SimpleBenchTypeError: If value is not a string.
    :raises SimpleBenchValueError: If value is empty.
    """
    return validate_string(
        value, "release",
        _PythonInfoErrorTag.INVALID_RELEASE_TYPE,
        _PythonInfoErrorTag.EMPTY_RELEASE_VALUE,
        allow_empty=False, strip=True
    )

def system(value: str) -> str:
    """Validate system property.

    :param str value: The system string to validate.
    :return str: The validated system string.
    :raises SimpleBenchTypeError: If value is not a string.
    :raises SimpleBenchValueError: If value is empty.
    """
    return validate_string(
        value, "system",
        _PythonInfoErrorTag.INVALID_SYSTEM_TYPE,
        _PythonInfoErrorTag.EMPTY_SYSTEM_VALUE,
        allow_empty=False, strip=True
    )
