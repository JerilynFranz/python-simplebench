"""Validation functions for MachineInfo data"""

from simplebench.environment._cpu_info import CPUInfo
from simplebench.environment._memory_info import MemoryInfo
from simplebench.environment._python_info import PythonInfo
from simplebench.environment._system_info import SystemInfo
from simplebench.validators import validate_bool, validate_string, validate_type

from ._error_tags import _MachineInfoErrorTag


def node(value: str | None) -> str | None:
    """Validate the node parameter.

    The node must be a string or `None`.

    :param str | None value: The node string to validate.
    :return str | None: The validated node string.
    :raises SimpleBenchTypeError: If the value is not a string or ``None``.
    """
    if value is None:
        return None
    return validate_string(
        value,
        'node',
        _MachineInfoErrorTag.INVALID_NODE_PARAM,
        _MachineInfoErrorTag.INVALID_NODE_PARAM,
        allow_empty=True,
        allow_blank=True,
        strip=True,
    )


def cache_key(value: str | None) -> str | None:
    """Validate the cache_key parameter.

    The cache_key must be one of the following values:
    - An empty string.
    - A string containing only alphanumeric characters.
    - `None`.

    :param str | None value: The cache_key string to validate.
    :return str | None: The validated cache_key string.
    :raises SimpleBenchTypeError: If the value is not a string or ``None``.
    :raises SimpleBenchValueError: If the value is a string but not empty or an alphanumeric string.
    """
    if value is None:
        return None

    return validate_string(
        value,
        'cache_key',
        _MachineInfoErrorTag.INVALID_CACHE_KEY_PARAM_TYPE,
        _MachineInfoErrorTag.INVALID_CACHE_KEY_PARAM_VALUE,
        strip=False,
        allow_empty=True,
        alphanumeric_only=True,
        message='cache_key must be a non-empty string containing only alphanumeric characters.',
    )


def fresh(value: bool) -> bool:
    """Validate the fresh parameter.

    The fresh must be a boolean.

    :param bool value: The fresh value to validate.
    :return bool: The validated fresh value.
    :raises SimpleBenchTypeError: If the value is not a boolean.
    """
    return validate_bool(value, 'fresh', _MachineInfoErrorTag.INVALID_FRESH_PARAM_TYPE)


def cpu_info(value: CPUInfo) -> CPUInfo:
    """Validate the 'cpu_info' parameter.

    The value must be an instance of CPUInfo.

    :param CPUInfo value: The CPUInfo instance to validate.
    :return CPUInfo: The validated CPUInfo instance.
    :raises SimpleBenchTypeError: If the value is not a CPUInfo instance.
    """
    return validate_type(value, CPUInfo, 'cpu_info', _MachineInfoErrorTag.INVALID_CPU_INFO_PARAM_TYPE)


def memory_info(value: MemoryInfo) -> MemoryInfo:
    """Validate the 'memory_info' parameter.

    The value must be an instance of MemoryInfo.

    :param MemoryInfo value: The MemoryInfo instance to validate.
    :return MemoryInfo: The validated MemoryInfo instance.
    :raises SimpleBenchTypeError: If the value is not a MemoryInfo instance.
    """
    return validate_type(value, MemoryInfo, 'memory_info', _MachineInfoErrorTag.INVALID_MEMORY_INFO_PARAM_TYPE)


def python_info(value: PythonInfo) -> PythonInfo:
    """Validate the 'python_info' parameter.

    The value must be an instance of PythonInfo.

    :param PythonInfo value: The PythonInfo instance to validate.
    :return PythonInfo: The validated PythonInfo instance.
    :raises SimpleBenchTypeError: If the value is not a PythonInfo instance.
    """
    return validate_type(value, PythonInfo, 'python_info', _MachineInfoErrorTag.INVALID_PYTHON_INFO_PARAM_TYPE)


def system_info(value: SystemInfo) -> SystemInfo:
    """Validate the 'system_info' parameter.

    The value must be an instance of SystemInfo.

    :param SystemInfo value: The SystemInfo instance to validate.
    :return SystemInfo: The validated SystemInfo instance.
    :raises SimpleBenchTypeError: If the value is not a SystemInfo instance.
    """
    return validate_type(value, SystemInfo, 'system_info', _MachineInfoErrorTag.INVALID_SYSTEM_INFO_PARAM_TYPE)
