"""Error tags for machine info utilities."""

from enum import auto
from simplebench.doc_utils import enum_docstrings
from simplebench.exceptions import ErrorTag


@enum_docstrings
class _MachineInfoErrorTag(ErrorTag):
    """Error tags for machine info utilities."""

    INVALID_EXECUTION_ENVIRONMENT_PARAM_TYPE = auto()
    """The `execution_environment` parameter is not an ExecutionEnvironment instance."""
    INVALID_FRESH_PARAM_TYPE = auto()
    """The `fresh` parameter is not a boolean value."""
    INVALID_CPU_INFO_PARAM_TYPE = auto()
    """The `cpu_info` parameter is not a CPUInfo instance."""
    INVALID_MEMORY_INFO_PARAM_TYPE = auto()
    """The `memory_info` parameter is not a MemoryInfo instance."""
    INVALID_PYTHON_INFO_PARAM_TYPE = auto()
    """The `python_info` parameter is not a PythonInfo instance."""
    INVALID_SYSTEM_INFO_PARAM_TYPE = auto()
    """The `system_info` parameter is not a SystemInfo instance."""
    INVALID_FRESH_CPU_INFO_PARAM_TYPE = auto()
    """The `fresh_cpu_info` parameter is not a boolean value."""
    INVALID_FRESH_MEMORY_INFO_PARAM_TYPE = auto()
    """The `fresh_memory_info` parameter is not a boolean value."""
    INVALID_CACHE_KEY_PARAM_TYPE = auto()
    """The 'cache_key' argument is not of type `str` or `None`."""
    INVALID_CACHE_KEY_PARAM_VALUE = auto()
    """The 'cache_key' argument is a string but neither an empty string nor an alphanumeric string."""
    INVALID_NODE_PARAM = auto()
    """Invalid 'node' parameter for MachineInfo initialization. Must be a string or `None`."""
