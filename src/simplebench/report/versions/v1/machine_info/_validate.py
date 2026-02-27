"""Validation functions for MachineInfo version 1."""
from collections.abc import Sequence
import re

from simplebench.exceptions import SimpleBenchTypeError
from simplebench.report._error_tags import _MachineInfoErrorTag
from simplebench.validators import validate_string, validate_string_with_regex, validate_type

from ..cpu_info import CPUInfo
from ..environment_info import EnvironmentInfo
from ..memory_info import MemoryInfo
from ..system_info import SystemInfo

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
        _MachineInfoErrorTag.INVALID_HASH_ID_PROPERTY_TYPE,
        _MachineInfoErrorTag.INVALID_HASH_ID_PROPERTY_VALUE,
        allow_empty=True,
        strip=True,
    )
    if hash_string == '':
        return ''

    return validate_string_with_regex(
        hash_string,
        'hash_id',
        _HASH_RE,
        _MachineInfoErrorTag.INVALID_HASH_ID_PROPERTY_TYPE,
        _MachineInfoErrorTag.INVALID_HASH_ID_PROPERTY_VALUE,
        message='{name} must be 64-character hexadecimal string. Found: {value}',
    )


def node(value: str) -> str:
    """Validate node property.

    :param str value: The node string to validate.
    :return str: The validated node string.
    :raises SimpleBenchTypeError: If value is not a string.
    """
    return validate_string(
        value,
        'node',
        _MachineInfoErrorTag.INVALID_NODE_PROPERTY_TYPE,
        _MachineInfoErrorTag.EMPTY_NODE_PROPERTY_VALUE,
        allow_empty=True,
        strip=True,
    )


def cpu(value: CPUInfo) -> CPUInfo:
    """Validate a CPUInfo instance.

    :param value: The CPUInfo instance to validate.
    :return: The validated CPUInfo instance.
    :raises SimpleBenchTypeError: If value is not of type CPUInfo.
    """
    return validate_type(value, CPUInfo, 'cpu_info', _MachineInfoErrorTag.INVALID_CPU_TYPE)


def memory(value: MemoryInfo) -> MemoryInfo:
    """Validate a MemoryInfo instance.

    :param value: The MemoryInfo instance to validate.
    :return: The validated MemoryInfo instance.
    :raises SimpleBenchTypeError: If value is not of type MemoryInfo.
    """
    return validate_type(value, MemoryInfo, 'memory_info', _MachineInfoErrorTag.INVALID_MEMORY_TYPE)


def system(value: SystemInfo) -> SystemInfo:
    """Validate a SystemInfo instance.

    :param value: The SystemInfo instance to validate.
    :return: The validated SystemInfo instance.
    :raises SimpleBenchTypeError: If value is not of type SystemInfo.
    """
    return validate_type(value, SystemInfo, 'system', _MachineInfoErrorTag.INVALID_SYSTEM_TYPE)


def environment(value: Sequence[EnvironmentInfo]) -> tuple[EnvironmentInfo, ...]:
    """Validate a sequence of EnvironmentInfo instances.

    :param value: The sequence of EnvironmentInfo instances to validate.
    :return: A tuple of the validated EnvironmentInfo instances.
    :raises SimpleBenchTypeError: If value is not a sequence of EnvironmentInfo instances.
    """
    if not isinstance(value, Sequence) or isinstance(value, (str, bytes)):
        raise SimpleBenchTypeError(
            f"The 'environment' property must be a Sequence of EnvironmentInfo instances, got {type(value).__name__}",
            tag=_MachineInfoErrorTag.INVALID_ENVIRONMENT_PROPERTY_TYPE,
        )
    if not all(isinstance(item, EnvironmentInfo) for item in value):
        raise SimpleBenchTypeError(
            "All items in the 'environment' property must be of type EnvironmentInfo",
            tag=_MachineInfoErrorTag.INVALID_ENVIRONMENT_PROPERTY_TYPE,
        )
    return value if isinstance(value, tuple) else tuple(value)
