"""JSONMachineInfo reporter exception Error Tags."""

from enum import auto
from simplebench.doc_utils import enum_docstrings
from simplebench.exceptions import ErrorTag

__all__: list[str] = []


@enum_docstrings
class _MachineInfoErrorTag(ErrorTag):
    """Error tags for JSONMachineInfo exceptions."""

    INVALID_HASH_ID_TYPE = auto()
    """Attempted to set the hash_id property to something other than a type str."""
    INVALID_HASH_ID_VALUE = auto()
    """Attempted to set the hash_id property to a value that is not a valid SHA-256 hexadecimal string."""
    INVALID_ENVIRONMENT_PROPERTY_TYPE = auto()
    """Attempted to set the environment property to something other than a type Sequence of EnvironmentInfo."""
    INVALID_SYSTEM_TYPE = auto()
    """Attempted to set the system property to something other than a v1 SystemInfo"""
    INVALID_EXECUTION_ENVIRONMENT_TYPE = auto()
    """Attempted to set the execution_environment property to something other than a v1 ExecutionEnvironment"""
    INVALID_MEMORY_TYPE = auto()
    """Attempted to set the memory property to something other than a v1 MemoryInfo"""
    INVALID_CPU_TYPE = auto()
    """Attempted to set the cpu property to something other than a v1 CPUInfo"""
    INVALID_VERSION_TYPE = auto()
    """Attempted to set the version property to something other than a type int."""
    UNSUPPORTED_VERSION = auto()
    """Attempted to set the version property to an unsupported value."""
    JSON_SCHEMA_VALIDATION_ERROR = auto()
    """JSON schema validation failed for the MachineInfo object."""
    INVALID_HASH_ID_PROPERTY_TYPE = auto()
    """Attempted to set the hash_id property to something other than a type str."""
    INVALID_HASH_ID_PROPERTY_VALUE = auto()
    """Attempted to set the hash_id property to a value that is not a valid SHA-256 hexadecimal string."""
    INVALID_DATA_ARG_TYPE = auto()
    """The data argument passed to from_dict() was not a dictionary."""
    INVALID_DATA_ARG_EXTRA_KEYS = auto()
    """The data argument passed to from_dict() contained extra unknown keys."""
    INVALID_DATA_ARG_MISSING_KEYS = auto()
    """The data argument passed to from_dict() was missing required keys."""
    INVALID_SYSTEM_PROPERTY_TYPE = auto()
    """Attempted to set the system property to something other than a type str."""
    INVALID_SYSTEM_PROPERTY_VALUE = auto()
    """Attempted to set the system property to an invalid value."""
    INVALID_RELEASE_PROPERTY_TYPE = auto()
    """Attempted to set the release property to something other than a type str."""
    INVALID_RELEASE_PROPERTY_VALUE = auto()
    """Attempted to set the release property to an invalid value."""
    INVALID_CPU_PROPERTY_TYPE = auto()
    """Attempted to set the cpu property to something other than a type JSONCPUInfo."""
    INVALID_EXECUTION_ENVIRONMENT_PROPERTY_TYPE = auto()
    """Attempted to set the execution_environment property to something other than a type JSONExecutionEnvironment."""
    INVALID_NODE_PROPERTY_TYPE = auto()
    """Attempted to set the node property to something other than a type str."""
    EMPTY_NODE_PROPERTY_VALUE = auto()
    """Attempted to set the node property to an invalid value."""
    INVALID_MACHINE_PROPERTY_TYPE = auto()
    """Attempted to set the machine property to something other than a type str."""
    EMPTY_MACHINE_PROPERTY_VALUE = auto()
    """Attempted to set the machine property to an empty string."""
    INVALID_PROCESSOR_PROPERTY_TYPE = auto()
    """Attempted to set the processor property to something other than a type str."""
    EMPTY_PROCESSOR_PROPERTY_VALUE = auto()
    """Attempted to set the processor property to an empty string."""
    INVALID_DICT_EXPORT_TYPE = auto()
    """The dictionary representation of MachineInfo does not conform to the ImmutableMachineInfoDict TypedDict
    definition."""
