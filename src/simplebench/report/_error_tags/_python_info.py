"""ErrorTags for PythonInfo classes"""

from enum import auto
from simplebench.doc_utils import enum_docstrings
from simplebench.exceptions import ErrorTag


@enum_docstrings
class _PythonInfoErrorTag(ErrorTag):
    """ErrorTags for PythonInfo classes"""

    JSON_SCHEMA_VALIDATION_ERROR = auto()
    """JSON schema validation error"""
    MISSING_PROPERTY = auto()
    """Missing required property for PythonInfo"""
    INVALID_HASH_ID_TYPE = auto()
    """Invalid hash_id type - must be a string"""
    INVALID_HASH_ID_VALUE = auto()
    """Invalid hash_id value - must be a 64-character hexadecimal string"""
    INVALID_COMPILER_TYPE = auto()
    """Invalid compiler type - must be a string"""
    EMPTY_COMPILER_VALUE = auto()
    """Empty compiler value - must be a non-empty string"""
    INVALID_IMPLEMENTATION_TYPE = auto()
    """Invalid implementation type - must be a string"""
    EMPTY_IMPLEMENTATION_VALUE = auto()
    """Empty implementation value - must be a non-empty string"""
    INVALID_IMPLEMENTATION_VERSION_TYPE = auto()
    """Invalid implementation_version type - must be a string"""
    EMPTY_IMPLEMENTATION_VERSION_VALUE = auto()
    """Empty implementation_version value - must be a non-empty string"""
    INVALID_PYTHON_VERSION_TYPE = auto()
    """Invalid python_version type - must be a string"""
    EMPTY_PYTHON_VERSION_VALUE = auto()
    """Empty python_version value - must be a non-empty string"""
    INVALID_BUILDNO_TYPE = auto()
    """Invalid buildno type - must be a string"""
    EMPTY_BUILDNO_VALUE = auto()
    """Empty buildno value - must be a non-empty string"""
    INVALID_BUILDDATE = auto()
    """Invalid build type - must be a string"""
    """Empty build value - must be a non-empty string"""
    INVALID_REVISION = auto()
    """Invalid revision type - must be a string"""
    INVALID_COMMAND_LINE_FLAGS = auto()
    """Invalid command_line_flags type - must be a string"""
    INVALID_ENVIRONMENT_VARIABLES_TYPE = auto()
    """Invalid environment_variables type - must be a mapping of strings to strings"""
    INVALID_ENVIRONMENT_VARIABLES_ITEM_TYPE = auto()
    """Invalid environment_variables item type - all keys and values must be strings"""
    INVALID_GC_IS_ENABLED_TYPE = auto()
    """Invalid gc_is_enabled type - must be a boolean"""
    INVALID_GC_THRESHOLDS_TYPE = auto()
    """Invalid gc_thresholds type - must be a sequence of three integers"""
    INVALID_NUMBER_OF_GC_THRESHOLDS = auto()
    """Invalid number of gc_thresholds - must contain exactly three integers"""
    INVALID_GC_THRESHOLD_ITEM_TYPE = auto()
    """Invalid gc_thresholds item type - all items must be integers"""
    INVALID_THREAD_SWITCH_INTERVAL_TYPE = auto()
    """Invalid thread_switch_interval type - must be a float or integer"""
    INVALID_ARCHITECTURE_BITS = auto()
    """Invalid architecture_bits type"""
    INVALID_ARCHITECTURE_LINKAGE = auto()
    """Invalid architecture_linkage type"""
    INVALID_VERSION_TYPE = auto()
    """Invalid version type"""
    UNSUPPORTED_VERSION = auto()
    """Unsupported version"""
    INVALID_TYPE_TYPE = auto()
    """Invalid type type"""
    INVALID_TYPE_VALUE = auto()
    """Invalid type value"""
    INVALID_DATA_ARG_EXTRA_KEYS = auto()
    """Invalid data argument extra keys"""
    INVALID_DATA_ARG_MISSING_KEYS = auto()
    """Invalid data argument missing keys"""
    INVALID_ENVIRONMENT_VARIABLES_KEY_FORMAT = auto()
    """Invalid environment variable key format - all keys must match the pattern ^PYTHON[A-Z0-9_]*$"""
