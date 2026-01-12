"""Error tags for machine info utilities."""

from simplebench.doc_utils import enum_docstrings
from simplebench.exceptions import ErrorTag


@enum_docstrings
class _MachineInfoErrorTag(ErrorTag):
    """Error tags for machine info utilities."""

    INVALID_EXECUTION_ENVIRONMENT_PARAM_TYPE = 'INVALID_EXECUTION_ENVIRONMENT_PARAM_TYPE'
    """The `execution_environment` parameter is not an ExecutionEnvironment instance."""
    INVALID_FRESH_PARAM_TYPE = 'INVALID_FRESH_PARAM_TYPE'
    """The `fresh` parameter is not a boolean value."""
    INVALID_CPU_INFO_PARAM_TYPE = 'INVALID_CPU_INFO_PARAM_TYPE'
    """The `cpu_info` parameter is not a CPUInfo instance."""
    INVALID_MEMORY_INFO_PARAM_TYPE = 'INVALID_MEMORY_INFO_PARAM_TYPE'
    """The `memory_info` parameter is not a MemoryInfo instance."""
    INVALID_PYTHON_INFO_PARAM_TYPE = 'INVALID_PYTHON_INFO_PARAM_TYPE'
    """The `python_info` parameter is not a PythonInfo instance."""
    INVALID_SYSTEM_INFO_PARAM_TYPE = 'INVALID_SYSTEM_INFO_PARAM_TYPE'
    """The `system_info` parameter is not a SystemInfo instance."""
    INVALID_FRESH_CPU_INFO_PARAM_TYPE = 'INVALID_FRESH_CPU_INFO_PARAM_TYPE'
    """The `fresh_cpu_info` parameter is not a boolean value."""
    INVALID_FRESH_MEMORY_INFO_PARAM_TYPE = 'INVALID_FRESH_MEMORY_INFO_PARAM_TYPE'
    """The `fresh_memory_info` parameter is not a boolean value."""
    INVALID_CACHE_KEY_PARAM_TYPE = 'INVALID_CACHE_KEY_PARAM_TYPE'
    """The 'cache_key' argument is not of type `str` or `None`."""
    INVALID_CACHE_KEY_PARAM_VALUE = 'INVALID_CACHE_KEY_PARAM_VALUE'
    """The 'cache_key' argument is a string but neither an empty string nor an alphanumeric string."""
    INVALID_NODE_PARAM = 'INVALID_NODE_PARAM'
    """Invalid 'node' parameter for MachineInfo initialization. Must be a string or `None`."""
