"""Exceptions for JSONReport classes."""

from enum import auto

from simplebench.doc_utils import enum_docstrings
from simplebench.exceptions import ErrorTag

__all__: list[str] = []


@enum_docstrings
class _ReportErrorTag(ErrorTag):
    """Error tags for JSON report exceptions."""

    INPUT_DATA_NOT_A_MAPPING = auto()
    """The input data for Report.from_dict is not a mapping type (e.g., dict)."""
    MISSING_METRICS = auto()
    """The metrics field is missing from the JSON report input."""
    INVALID_METRICS_TYPE = auto()
    """The metrics is not of type Metrics."""
    INVALID_HASH_ID_TYPE = auto()
    """The hash_id is not of type str."""
    INVALID_HASH_ID_VALUE = auto()
    """The hash_id is not a valid 64-character hexadecimal string."""
    INVALID_RESULTS_TYPE = auto()
    """The results is not of type Sequence[ResultsInfo]."""
    INVALID_RESULTS_VALUE = auto()
    """Content of results does not match specified restrictions such as number of items."""
    INVALID_CASE = auto()
    """The provided object is not a valid Case instance."""
    CASE_HAS_NOT_BEEN_RUN = auto()
    """The provided Case instance has not been run yet."""
    INVALID_TIMESTAMP_PROPERTY_TYPE = auto()
    """Attempted to set the timestamp property to something other than a type str."""
    INVALID_TIMESTAMP_PROPERTY_VALUE = auto()
    """Attempted to set the timestamp property to something other than an ISO 8601 datetime string."""
    INVALID_DATA_ARG_EXTRA_KEYS = auto()
    """The data argument has extra keys that are not allowed."""
    INVALID_DATA_ARG_MISSING_KEYS = auto()
    """The data argument is missing required keys."""
    INVALID_DATA_ARG_TYPE = auto()
    """The data argument is not of type dict."""
    INVALID_RESULTS_PROPERTY_ELEMENT_NOT_DICT = auto()
    """An element in the results object is not a dictionary."""
    INVALID_MACHINE_PROPERTY_TYPE = auto()
    """Attempted to set the machine property to something other than a JSONMachineInfo instance."""
    JSON_SCHEMA_VALIDATION_ERROR = auto()
    """The JSON report data failed schema validation."""
    MISSING_INIT_IMPLEMENTATION = auto()
    """The __init__ method is not implemented in a subclass."""
    INVALID_RESULTS_ELEMENT_MISSING_TYPE_KEY = auto()
    """An element in the results sequence is missing the 'type' key."""
    INVALID_RESULTS_ELEMENT_KEYS_NOT_STR = auto()
    """An element in the results sequence has a key that is not a string."""
    INVALID_RESULTS_ELEMENT_KEYS_EMPTY_STRING = auto()
    """An element in the results sequence has a key that is an empty string."""
    INVALID_RESULTS_PROPERTY_NOT_A_SEQUENCE = auto()
    """Attempt to set results property to something besides a Sequence."""
    INVALID_RESULTS_PROPERTY_ELEMENT_NOT_RESULTS_INSTANCE = auto()
    """An element in the passed results property Sequence is not a Results instance."""
    INVALID_VARIATION_COLS_KEYS_TYPE = auto()
    """The keys in variation_cols are not all strings."""
    INVALID_VARIATION_COLS_KEYS_VALUE = auto()
    """The keys in variation_cols have invalid values (must be non-empty strings)."""
    INVALID_VARIATION_COLS_VALUES_TYPE = auto()
    """The values in variation_cols are not all strings."""
    INVALID_VARIATION_COLS_VALUES_VALUE = auto()
    """The values in variation_cols have invalid values (must be non-empty strings)."""
    INVALID_GROUP_PROPERTY_TYPE = auto()
    """Attempted to set the group property to something other than a type str."""
    EMPTY_GROUP_PROPERTY_VALUE = auto()
    """Attempted to set the group property to an empty string."""
    INVALID_TITLE_PROPERTY_TYPE = auto()
    """Attempted to set the title property to something other than a type str."""
    EMPTY_TITLE_PROPERTY_VALUE = auto()
    """Attempted to set the title property to an empty string."""
    INVALID_DESCRIPTION_PROPERTY_TYPE = auto()
    """Attempted to set the description property to something other than a type str."""
    EMPTY_DESCRIPTION_PROPERTY_VALUE = auto()
    """Attempted to set the description property to an empty string."""
    INVALID_VARIATION_COLS_PROPERTY_TYPE = auto()
    """Attempted to set the variation_cols property to something other than a type dict."""
    MISSING_FROM_DICT_IMPLEMENTATION = auto()
    """The from_dict method is not implemented in a subclass."""
    INVALID_PROPERTIES_TYPE = auto()
    """The properties is not of type dict."""
    INVALID_PROPERTIES_KEYS_TYPE = auto()
    """The keys in properties are not all strings."""
    INVALID_TYPE_TYPE = auto()
    """The type is not of type str."""
    INVALID_TYPE_VALUE = auto()
    """The type has an incorrect value."""
    INVALID_VERSION_TYPE = auto()
    """The version is not of type int."""
    INVALID_VERSION_VALUE = auto()
    """The version has an incorrect value."""
    INVALID_SCHEMA_URI_TYPE = auto()
    """The JSONSchema $schema URI is not of type str."""
    INVALID_SCHEMA_URI_VALUE = auto()
    """The JSONSchema $schema URI has an incorrect value."""
    INVALID_INPUT_DATA_TYPE = auto()
    """The input data is not of type dict."""
    INVALID_INPUT_DATA_KEYS_TYPE = auto()
    """The keys in the input data are not all strings."""
    MISSING_SCHEMA = auto()
    """The $schema is missing from the JSON report."""
    MISSING_VERSION = auto()
    """The version is missing from the JSON report."""
    INCORRECT_VERSION = auto()
    """The version in the JSON report is incorrect."""
    UNSUPPORTED_VERSION = auto()
    """The specified version is not supported."""
