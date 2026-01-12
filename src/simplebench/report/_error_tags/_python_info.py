"""ErrorTags for PythonInfo classes"""

from simplebench.doc_utils import enum_docstrings
from simplebench.exceptions import ErrorTag


@enum_docstrings
class _PythonInfoErrorTag(ErrorTag):
    """ErrorTags for PythonInfo classes"""

    JSON_SCHEMA_VALIDATION_ERROR = 'JSON_SCHEMA_VALIDATION_ERROR'
    """JSON schema validation error"""
    MISSING_PROPERTY = 'MISSING_PROPERTY'
    """Missing required property for PythonInfo"""
    INVALID_HASH_ID_TYPE = 'INVALID_HASH_ID_TYPE'
    """Invalid hash_id type - must be a string"""
    INVALID_HASH_ID_VALUE = 'INVALID_HASH_ID_VALUE'
    """Invalid hash_id value - must be a 64-character hexadecimal string"""
    INVALID_COMPILER_TYPE = 'INVALID_COMPILER_TYPE'
    """Invalid compiler type - must be a string"""
    EMPTY_COMPILER_VALUE = 'EMPTY_COMPILER_VALUE'
    """Empty compiler value - must be a non-empty string"""
    INVALID_IMPLEMENTATION_TYPE = 'INVALID_IMPLEMENTATION_TYPE'
    """Invalid implementation type - must be a string"""
    EMPTY_IMPLEMENTATION_VALUE = 'EMPTY_IMPLEMENTATION_VALUE'
    """Empty implementation value - must be a non-empty string"""
    INVALID_IMPLEMENTATION_VERSION_TYPE = 'INVALID_IMPLEMENTATION_VERSION_TYPE'
    """Invalid implementation_version type - must be a string"""
    EMPTY_IMPLEMENTATION_VERSION_VALUE = 'EMPTY_IMPLEMENTATION_VERSION_VALUE'
    """Empty implementation_version value - must be a non-empty string"""
    INVALID_PYTHON_VERSION_TYPE = 'INVALID_PYTHON_VERSION_TYPE'
    """Invalid python_version type - must be a string"""
    EMPTY_PYTHON_VERSION_VALUE = 'EMPTY_PYTHON_VERSION_VALUE'
    """Empty python_version value - must be a non-empty string"""
    INVALID_BUILDNO_TYPE = 'INVALID_BUILDNO_TYPE'
    """Invalid buildno type - must be a string"""
    EMPTY_BUILDNO_VALUE = 'EMPTY_BUILDNO_VALUE'
    """Empty buildno value - must be a non-empty string"""
    INVALID_BUILD_TYPE = 'INVALID_BUILD_TYPE'
    """Invalid build type - must be a string"""
    EMPTY_BUILD_VALUE = 'EMPTY_BUILD_VALUE'
    """Empty build value - must be a non-empty string"""
    INVALID_REVISION = 'INVALID_REVISION'
    """Invalid revision type - must be a string"""
    INVALID_COMMAND_LINE_FLAGS = 'INVALID_COMMAND_LINE_FLAGS'
    """Invalid command_line_flags type - must be a string"""
    INVALID_ENVIRONMENT_VARIABLES_TYPE = 'INVALID_ENVIRONMENT_VARIABLES_TYPE'
    """Invalid environment_variables type - must be a mapping of strings to strings"""
    INVALID_ENVIRONMENT_VARIABLES_ITEM_TYPE = 'INVALID_ENVIRONMENT_VARIABLES_ITEM_TYPE'
    """Invalid environment_variables item type - all keys and values must be strings"""
    INVALID_GC_IS_ENABLED_TYPE = 'INVALID_GC_IS_ENABLED_TYPE'
    """Invalid gc_is_enabled type - must be a boolean"""
    INVALID_GC_THRESHOLDS_TYPE = 'INVALID_GC_THRESHOLDS_TYPE'
    """Invalid gc_thresholds type - must be a sequence of three integers"""
    INVALID_NUMBER_OF_GC_THRESHOLDS = 'INVALID_NUMBER_OF_GC_THRESHOLDS'
    """Invalid number of gc_thresholds - must contain exactly three integers"""
    INVALID_GC_THRESHOLD_ITEM_TYPE = 'INVALID_GC_THRESHOLD_ITEM_TYPE'
    """Invalid gc_thresholds item type - all items must be integers"""
    INVALID_THREAD_SWITCH_INTERVAL_TYPE = 'INVALID_THREAD_SWITCH_INTERVAL_TYPE'
    """Invalid thread_switch_interval type - must be a float or integer"""
    INVALID_ARCHITECTURE_BITS = 'INVALID_ARCHITECTURE_BITS'
    """Invalid architecture_bits type"""
    INVALID_ARCHITECTURE_LINKAGE = 'INVALID_ARCHITECTURE_LINKAGE'
    """Invalid architecture_linkage type"""
    INVALID_VERSION_TYPE = 'INVALID_VERSION_TYPE'
    """Invalid version type"""
    UNSUPPORTED_VERSION = 'UNSUPPORTED_VERSION'
    """Unsupported version"""
    INVALID_TYPE_TYPE = 'INVALID_TYPE_TYPE'
    """Invalid type type"""
    INVALID_TYPE_VALUE = 'INVALID_TYPE_VALUE'
    """Invalid type value"""
    INVALID_DATA_ARG_EXTRA_KEYS = 'INVALID_DATA_ARG_EXTRA_KEYS'
    """Invalid data argument extra keys"""
    INVALID_DATA_ARG_MISSING_KEYS = 'INVALID_DATA_ARG_MISSING_KEYS'
    """Invalid data argument missing keys"""
