"""Exceptions for JSONReport classes."""
from simplebench.enums import enum_docstrings
from simplebench.exceptions import ErrorTag


@enum_docstrings
class _ReportErrorTag(ErrorTag):
    """Error tags for JSON report exceptions."""
    INVALID_RESULTS_PROPERTY_ELEMENT_NOT_DICT = 'INVALID_RESULTS_PROPERTY_ELEMENT_NOT_DICT'
    """An element in the results object is not a dictionary."""
    INVALID_MACHINE_PROPERTY_TYPE = 'INVALID_MACHINE_PROPERTY_TYPE'
    """Attempted to set the machine property to something other than a JSONMachineInfo instance."""
    JSON_SCHEMA_VALIDATION_ERROR = 'JSON_SCHEMA_VALIDATION_ERROR'
    """The JSON report data failed schema validation."""
    MISSING_INIT_IMPLEMENTATION = 'MISSING_INIT_IMPLEMENTATION'
    """The __init__ method is not implemented in a subclass."""
    INVALID_RESULTS_ELEMENT_MISSING_TYPE_KEY = 'INVALID_RESULTS_ELEMENT_MISSING_TYPE_KEY'
    """An element in the results sequence is missing the 'type' key."""
    INVALID_RESULTS_ELEMENT_KEYS_NOT_STR = 'INVALID_RESULTS_ELEMENT_KEYS_NOT_STR'
    """An element in the results sequence has a key that is not a string."""
    INVALID_RESULTS_ELEMENT_KEYS_EMPTY_STRING = 'INVALID_RESULTS_ELEMENT_KEYS_EMPTY_STRING'
    """An element in the results sequence has a key that is an empty string."""
    INVALID_RESULTS_PROPERTY_NOT_A_SEQUENCE = 'INVALID_RESULTS_PROPERTY_NOT_A_SEQUENCE'
    """Attempt to set results property to something besides a Sequence."""
    INVALID_RESULTS_PROPERTY_ELEMENT_NOT_RESULTS_INSTANCE = 'INVALID_RESULTS_PROPERTY_ELEMENT_NOT_RESULTS_INSTANCE'
    """An element in the passed results property Sequence is not a Results instance."""
    INVALID_VARIATION_COLS_KEYS_TYPE = 'INVALID_VARIATION_COLS_KEYS_TYPE'
    """The keys in variation_cols are not all strings."""
    INVALID_VARIATION_COLS_KEYS_VALUE = 'INVALID_VARIATION_COLS_KEYS_VALUE'
    """The keys in variation_cols have invalid values (must be non-empty strings)."""
    INVALID_VARIATION_COLS_VALUES_TYPE = 'INVALID_VARIATION_COLS_VALUES_TYPE'
    """The values in variation_cols are not all strings."""
    INVALID_VARIATION_COLS_VALUES_VALUE = 'INVALID_VARIATION_COLS_VALUES_VALUE'
    """The values in variation_cols have invalid values (must be non-empty strings)."""
    INVALID_GROUP_PROPERTY_TYPE = 'INVALID_GROUP_PROPERTY_TYPE'
    """Attempted to set the group property to something other than a type str."""
    EMPTY_GROUP_PROPERTY_VALUE = 'EMPTY_GROUP_PROPERTY_VALUE'
    """Attempted to set the group property to an empty string."""
    INVALID_TITLE_PROPERTY_TYPE = 'INVALID_TITLE_PROPERTY_TYPE'
    """Attempted to set the title property to something other than a type str."""
    EMPTY_TITLE_PROPERTY_VALUE = 'EMPTY_TITLE_PROPERTY_VALUE'
    """Attempted to set the title property to an empty string."""
    INVALID_DESCRIPTION_PROPERTY_TYPE = 'INVALID_DESCRIPTION_PROPERTY_TYPE'
    """Attempted to set the description property to something other than a type str."""
    EMPTY_DESCRIPTION_PROPERTY_VALUE = 'EMPTY_DESCRIPTION_PROPERTY_VALUE'
    """Attempted to set the description property to an empty string."""
    INVALID_VARIATION_COLS_PROPERTY_TYPE = 'INVALID_VARIATION_COLS_PROPERTY_TYPE'
    """Attempted to set the variation_cols property to something other than a type dict."""
    MISSING_FROM_DICT_IMPLEMENTATION = 'MISSING_FROM_DICT_IMPLEMENTATION'
    """The from_dict method is not implemented in a subclass."""
    INVALID_PROPERTIES_TYPE = 'INVALID_PROPERTIES_TYPE'
    """The properties is not of type dict."""
    INVALID_PROPERTIES_KEYS_TYPE = 'INVALID_PROPERTIES_KEYS_TYPE'
    """The keys in properties are not all strings."""
    INVALID_TYPE_TYPE = 'INVALID_TYPE_TYPE'
    """The type is not of type str."""
    INVALID_TYPE_VALUE = 'INVALID_TYPE_VALUE'
    """The type has an incorrect value."""
    INVALID_VERSION_TYPE = 'INVALID_VERSION_TYPE'
    """The version is not of type int."""
    INVALID_VERSION_VALUE = 'INVALID_VERSION_VALUE'
    """The version has an incorrect value."""
    INVALID_SCHEMA_URI_TYPE = 'INVALID_SCHEMA_URI_TYPE'
    """The JSONSchema $schema URI is not of type str."""
    INVALID_SCHEMA_URI_VALUE = 'INVALID_SCHEMA_URI_VALUE'
    """The JSONSchema $schema URI has an incorrect value."""
    INVALID_INPUT_DATA_TYPE = 'INVALID_INPUT_DATA_TYPE'
    """The input data is not of type dict."""
    INVALID_INPUT_DATA_KEYS_TYPE = 'INVALID_INPUT_DATA_KEYS_TYPE'
    """The keys in the input data are not all strings."""
    MISSING_SCHEMA = 'MISSING_SCHEMA'
    """The $schema is missing from the JSON report."""
    MISSING_VERSION = 'MISSING_VERSION'
    """The version is missing from the JSON report."""
    INCORRECT_VERSION = 'INCORRECT_VERSION'
    """The version in the JSON report is incorrect."""
    UNSUPPORTED_VERSION = 'UNSUPPORTED_VERSION'
    """The specified version is not supported."""
