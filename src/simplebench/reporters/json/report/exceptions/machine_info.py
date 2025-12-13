"""JSONMachineInfo reporter exception Error Tags."""
from simplebench.enums import enum_docstrings
from simplebench.exceptions import ErrorTag


@enum_docstrings
class _MachineInfoErrorTag(ErrorTag):
    """Error tags for JSONMachineInfo exceptions."""
    INVALID_VERSION_TYPE = 'INVALID_VERSION_TYPE'
    """Attempted to set the version property to something other than a type int."""
    UNSUPPORTED_VERSION = 'UNSUPPORTED_VERSION'
    """Attempted to set the version property to an unsupported value."""
    JSON_SCHEMA_VALIDATION_ERROR = 'JSON_SCHEMA_VALIDATION_ERROR'
    """JSON schema validation failed for the MachineInfo object."""
    INVALID_HASH_ID_PROPERTY_TYPE = 'INVALID_HASH_ID_PROPERTY_TYPE'
    """Attempted to set the hash_id property to something other than a type str."""
    INVALID_HASH_ID_PROPERTY_VALUE = 'INVALID_HASH_ID_PROPERTY_VALUE'
    """Attempted to set the hash_id property to a value that is not a valid SHA-256 hexadecimal string."""
    INVALID_DATA_ARG_TYPE = 'INVALID_DATA_ARG_TYPE'
    """The data argument passed to from_dict() was not a dictionary."""
    INVALID_DATA_ARG_EXTRA_KEYS = 'INVALID_DATA_ARG_EXTRA_KEYS'
    """The data argument passed to from_dict() contained extra unknown keys."""
    INVALID_DATA_ARG_MISSING_KEYS = 'INVALID_DATA_ARG_MISSING_KEYS'
    """The data argument passed to from_dict() was missing required keys."""
    INVALID_SYSTEM_PROPERTY_TYPE = 'INVALID_SYSTEM_PROPERTY_TYPE'
    """Attempted to set the system property to something other than a type str."""
    INVALID_SYSTEM_PROPERTY_VALUE = 'INVALID_SYSTEM_PROPERTY_VALUE'
    """Attempted to set the system property to an invalid value."""
    INVALID_RELEASE_PROPERTY_TYPE = 'INVALID_RELEASE_PROPERTY_TYPE'
    """Attempted to set the release property to something other than a type str."""
    INVALID_RELEASE_PROPERTY_VALUE = 'INVALID_RELEASE_PROPERTY_VALUE'
    """Attempted to set the release property to an invalid value."""
    INVALID_CPU_PROPERTY_TYPE = 'INVALID_CPU_PROPERTY_TYPE'
    """Attempted to set the cpu property to something other than a type JSONCPUInfo."""
    INVALID_EXECUTION_ENVIRONMENT_PROPERTY_TYPE = 'INVALID_EXECUTION_ENVIRONMENT_PROPERTY_TYPE'
    """Attempted to set the execution_environment property to something other than a type JSONExecutionEnvironment."""
    INVALID_NODE_PROPERTY_TYPE = 'INVALID_NODE_PROPERTY_TYPE'
    """Attempted to set the node property to something other than a type str."""
    EMPTY_NODE_PROPERTY_VALUE = 'EMPTY_NODE_PROPERTY_VALUE'
    """Attempted to set the node property to an invalid value."""
    INVALID_MACHINE_PROPERTY_TYPE = 'INVALID_MACHINE_PROPERTY_TYPE'
    """Attempted to set the machine property to something other than a type str."""
    EMPTY_MACHINE_PROPERTY_VALUE = 'EMPTY_MACHINE_PROPERTY_VALUE'
    """Attempted to set the machine property to an empty string."""
    INVALID_PROCESSOR_PROPERTY_TYPE = 'INVALID_PROCESSOR_PROPERTY_TYPE'
    """Attempted to set the processor property to something other than a type str."""
    EMPTY_PROCESSOR_PROPERTY_VALUE = 'EMPTY_PROCESSOR_PROPERTY_VALUE'
    """Attempted to set the processor property to an empty string."""
