"""Validation functions for MachineInfo version 1."""

import re
from collections.abc import Mapping, Sequence
from types import MappingProxyType

from simplebench.exceptions import SimpleBenchTypeError, SimpleBenchValueError
from simplebench.report._error_tags import _PythonInfoErrorTag
from simplebench.validators import validate_bool, validate_string, validate_string_with_regex

_HASH_RE: re.Pattern = re.compile(r'^[a-f0-9]{64}$')
"""Regular expression pattern for validating 64-character hexadecimal strings."""

__all__ = []


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
        _PythonInfoErrorTag.INVALID_HASH_ID_TYPE,
        _PythonInfoErrorTag.INVALID_HASH_ID_VALUE,
        allow_empty=True,
        strip=True,
    )
    if hash_string == '':
        return ''

    return validate_string_with_regex(
        hash_string,
        'hash_id',
        _HASH_RE,
        _PythonInfoErrorTag.INVALID_HASH_ID_TYPE,
        _PythonInfoErrorTag.INVALID_HASH_ID_VALUE,
        message='{name} must be 64-character hexadecimal string. Found: {value}',
    )


def compiler(value: str) -> str:
    """Validate compiler property.

    The compiler property is allowed to be an empty string.

    :param str value: The compiler string to validate.
    :return str: The validated compiler string.
    :raises SimpleBenchTypeError: If value is not a string.
    :raises SimpleBenchValueError: If value is empty.
    """
    return validate_string(
        value,
        'compiler',
        _PythonInfoErrorTag.INVALID_COMPILER_TYPE,
        _PythonInfoErrorTag.EMPTY_COMPILER_VALUE,
        allow_empty=True,
        strip=True,
    )


def implementation(value: str) -> str:
    """Validate implementation property.

    The implementation property is not allowed to be an empty string.

    :param str value: The implementation string to validate.
    :return str: The validated implementation string.
    :raises SimpleBenchTypeError: If value is not a string.
    :raises SimpleBenchValueError: If value is empty.
    """
    return validate_string(
        value,
        'implementation',
        _PythonInfoErrorTag.INVALID_IMPLEMENTATION_TYPE,
        _PythonInfoErrorTag.EMPTY_IMPLEMENTATION_VALUE,
        allow_empty=False,
        strip=True,
    )


def implementation_version(value: str) -> str:
    """Validate implementation_version property.

    The implementation_version property is allowed to be an empty string.

    :param str value: The implementation_version string to validate.
    :return str: The validated implementation_version string.
    :raises SimpleBenchTypeError: If value is not a string.
    :raises SimpleBenchValueError: If value is empty.
    """
    return validate_string(
        value,
        'implementation_version',
        _PythonInfoErrorTag.INVALID_IMPLEMENTATION_VERSION_TYPE,
        _PythonInfoErrorTag.EMPTY_IMPLEMENTATION_VERSION_VALUE,
        allow_empty=True,
        strip=True,
    )


def python_version(value: str) -> str:
    """Validate python_version property.

    The python_version property is not allowed to be an empty string.

    :param str value: The python_version string to validate.
    :return str: The validated python_version string.
    :raises SimpleBenchTypeError: If value is not a string.
    :raises SimpleBenchValueError: If value is empty.
    """
    return validate_string(
        value,
        'python_version',
        _PythonInfoErrorTag.INVALID_PYTHON_VERSION_TYPE,
        _PythonInfoErrorTag.EMPTY_PYTHON_VERSION_VALUE,
        allow_empty=False,
        strip=True,
    )


def buildno(value: str) -> str:
    """Validate buildno property.

    The buildno property is allowed to be an empty string.

    :param str value: The buildno string to validate.
    :return str: The validated buildno string.
    :raises SimpleBenchTypeError: If value is not a string.
    :raises SimpleBenchValueError: If value is empty.
    """
    return validate_string(
        value,
        'buildno',
        _PythonInfoErrorTag.INVALID_BUILDNO_TYPE,
        _PythonInfoErrorTag.EMPTY_BUILDNO_VALUE,
        allow_empty=True,
        strip=True,
    )


def builddate(value: str) -> str:
    """Validate build property.

    The build property is allowed to be an empty string.

    :param str value: The build string to validate.
    :return str: The validated build string.
    :raises SimpleBenchTypeError: If value is not a string.
    :raises SimpleBenchValueError: If value is empty.
    """
    return validate_string(
        value,
        'build',
        _PythonInfoErrorTag.INVALID_BUILD_TYPE,
        _PythonInfoErrorTag.EMPTY_BUILD_VALUE,
        allow_empty=True,
        strip=True,
    )


def revision(value: str) -> str:
    """Validate revision property.

    It is allowed to be an empty string.

    :param str value: The revision string to validate.
    :return str: The validated revision string.
    :raises SimpleBenchTypeError: If value is not a string.
    """
    return validate_string(
        value,
        'revision',
        _PythonInfoErrorTag.INVALID_REVISION,
        _PythonInfoErrorTag.INVALID_REVISION,
        allow_empty=True,
        strip=True,
    )


def command_line_flags(value: str) -> str:
    """Validate command_line_flags property.

    It is allowed to be an empty string.

    :param str value: The command_line_flags string to validate.
    :return str: The validated command_line_flags string.
    :raises SimpleBenchTypeError: If value is not a string.
    """
    return validate_string(
        value,
        'command_line_flags',
        _PythonInfoErrorTag.INVALID_COMMAND_LINE_FLAGS,
        _PythonInfoErrorTag.INVALID_COMMAND_LINE_FLAGS,
        allow_empty=True,
        strip=True,
    )


def environment_variables(value: Mapping[str, str]) -> MappingProxyType[str, str]:
    """Validate environment_variables property.

    May be an empty mapping.

    :param Mapping[str, str] value: The environment_variables mapping to validate.
    :return MappingProxyType[str, str]: The validated environment_variables mapping.
    :raises SimpleBenchTypeError: If value is not a mapping of strings to strings.
    """
    if not isinstance(value, Mapping):
        raise SimpleBenchTypeError(
            f'environment_variables must be a mapping of strings to strings. Found: {type(value).__name__}',
            tag=_PythonInfoErrorTag.INVALID_ENVIRONMENT_VARIABLES_TYPE,
        )

    if not all(isinstance(k, str) and isinstance(v, str) for k, v in value.items()):
        raise SimpleBenchTypeError(
            f'environment_variables must be a mapping of strings to strings. Found: {type(value).__name__}',
            tag=_PythonInfoErrorTag.INVALID_ENVIRONMENT_VARIABLES_ITEM_TYPE,
        )

    if isinstance(value, MappingProxyType):
        return value

    return MappingProxyType(value)


def gc_is_enabled(value: bool) -> bool:
    """Validate gc_is_enabled property.

    :param bool value: The gc_is_enabled value to validate.
    :return bool: The validated gc_is_enabled value.
    :raises SimpleBenchTypeError: If value is not a boolean.
    """
    return validate_bool(value, 'gc_is_enabled', _PythonInfoErrorTag.INVALID_GC_IS_ENABLED_TYPE)


def gc_thresholds(value: Sequence[int]) -> tuple[int, int, int]:
    """Validate gc_thresholds property.

    The value must be a sequence of three integers. It is converted to a tuple
    for storage in the PythonInfo instance.

    :param Sequence[int] value: The gc_thresholds value to validate.
    :return tuple[int, int, int]: The validated gc_thresholds value.
    :raises SimpleBenchTypeError: If value is not a tuple of three integers.
    """
    if not isinstance(value, Sequence):
        raise SimpleBenchTypeError(
            f'gc_thresholds must be a sequence of three integers. Found: {type(value).__name__}',
            tag=_PythonInfoErrorTag.INVALID_GC_THRESHOLDS_TYPE,
        )
    if len(value) != 3:
        raise SimpleBenchValueError(
            'gc_thresholds must be a sequence of three integers. found {len(value)} items.',
            tag=_PythonInfoErrorTag.INVALID_NUMBER_OF_GC_THRESHOLDS,
        )

    if not all(isinstance(i, int) for i in value):
        raise SimpleBenchTypeError(
            f'gc_thresholds must be a tuple of three integers. Found: {type(value).__name__}',
            tag=_PythonInfoErrorTag.INVALID_GC_THRESHOLD_ITEM_TYPE,
        )

    validated_value: tuple[int, int, int] = tuple(value)  # type: ignore[reportAssignmentType]
    return validated_value


def thread_switch_interval(value: float | int) -> float:
    """Validate thread_switch_interval property.

    It must be either a float or an integer. The returned value is always a float.

    :param float value | int: The thread_switch_interval value to validate.
    :return float: The validated thread_switch_interval value.
    :raises SimpleBenchTypeError: If value is not a float or an integer.
    """
    if not isinstance(value, (float, int)):
        raise SimpleBenchTypeError(
            f'thread_switch_interval must be a float or an int. Found: {type(value).__name__}',
            tag=_PythonInfoErrorTag.INVALID_THREAD_SWITCH_INTERVAL_TYPE,
        )

    return float(value)


def architecture_bits(value: str) -> str:
    """Validate architecture_bits property.

    The architecture_bits property is allowed to be an empty string.

    :param str value: The architecture_bits string to validate.
    :return str: The validated architecture_bits string.
    :raises SimpleBenchTypeError: If value is not a string.
    :raises SimpleBenchValueError: If value is empty.
    """
    return validate_string(
        value,
        'architecture_bits',
        _PythonInfoErrorTag.INVALID_ARCHITECTURE_BITS,
        _PythonInfoErrorTag.INVALID_ARCHITECTURE_BITS,
        allow_empty=True,
        strip=True,
    )


def architecture_linkage(value: str) -> str:
    """Validate architecture_linkage property.

    The architecture_linkage property is allowed to be an empty string.

    :param str value: The architecture_linkage string to validate.
    :return str: The validated architecture_linkage string.
    :raises SimpleBenchTypeError: If value is not a string.
    :raises SimpleBenchValueError: If value is empty.
    """
    return validate_string(
        value,
        'architecture_linkage',
        _PythonInfoErrorTag.INVALID_ARCHITECTURE_LINKAGE,
        _PythonInfoErrorTag.INVALID_ARCHITECTURE_LINKAGE,
        allow_empty=True,
        strip=True,
    )
