"""Error tags for JSONCPUInfo reporter base class."""

from enum import auto
from simplebench.doc_utils import enum_docstrings
from simplebench.exceptions import ErrorTag


@enum_docstrings
class _CPUInfoErrorTag(ErrorTag):
    """Error tags for JSONCPUInfo reporter base class."""

    INVALID_DATA_PROPERTY_TYPE = auto()
    """The 'data' property is not of type 'simplebench.environment.CPUInfo'."""

    INVALID_DATA_PARAM_NON_FINITE_FLOAT = auto()
    """The 'data' argument contains non-finite float values (NaN, Infinity)."""
    INVALID_DATA_PARAM_KEYS_VALUE = auto()
    """One or more keys in the 'data' argument are blank strings."""
    INVALID_DATA_PARAM_CYCLIC_REFERENCE = auto()
    """The 'data' argument contains cyclic references."""
    INVALID_DATA_PARAM_NESTING_DEPTH = auto()
    """The 'data' argument is nested too deeply."""
    INVALID_DATA_PARAM_TYPE = auto()
    """The 'data' argument is not of type 'dict'."""
    INVALID_DATA_PARAM_KEYS_TYPE = auto()
    """One or more keys in the 'data' argument are not of type 'str'"""
    JSON_SCHEMA_VALIDATION_ERROR = auto()
    """The JSON data does not conform to the expected schema."""
    INVALID_VERSION_TYPE = auto()
    """The 'version' property is not of type 'int'."""
    UNSUPPORTED_VERSION = auto()
    """The 'version' property is an unsupported version number."""
    INVALID_BRAND_RAW_TYPE = auto()
    """The 'brand_raw' property is not of type 'str'."""
    INVALID_BRAND_RAW_VALUE_BLANK_STRING = auto()
    """The 'brand_raw' property is a blank string."""
    INVALID_ARCH_STRING_RAW_TYPE = auto()
    """The 'arch_string_raw' property is not of type 'str'."""
    INVALID_ARCH_STRING_RAW_VALUE_BLANK_STRING = auto()
    """The 'arch_string_raw' property is a blank string."""
    INVALID_COUNT_TYPE = auto()
    """The 'count' property is not of type 'int'."""
    INVALID_COUNT_VALUE = auto()
    """The 'count' property is less than one."""
    INVALID_ARCH_TYPE = auto()
    """The 'arch' property is not of type 'str'."""
    INVALID_ARCH_VALUE_EMPTY_OR_BLANK_STRING = auto()
    """The 'arch' property is an empty or blank string."""
    INVALID_BITS_TYPE = auto()
    """The 'bits' property is not of type 'int'."""
    INVALID_BITS_VALUE = auto()
    """The 'bits' property is less than 16."""
    INVALID_HASH_ID_PROPERTY_TYPE = auto()
    """The 'hash_id' property is not of type 'str'."""
    INVALID_HASH_ID_PROPERTY_VALUE = auto()
    """The 'hash_id' property is not a valid SHA-256 hexadecimal string or empty"""
    INVALID_DATA_ARG_TYPE = auto()
    """The 'data' argument is not of type 'dict'."""
    INVALID_DATA_ARG_EXTRA_KEYS = auto()
    """The 'data' argument contains unexpected extra keys."""
    INVALID_DATA_ARG_MISSING_KEYS = auto()
    """The 'data' argument is missing required keys."""
