"""ErrorTags for simplebench.utils in SimpleBench."""

from simplebench.doc_utils import enum_docstrings
from simplebench.exceptions import ErrorTag


@enum_docstrings
class _UtilsErrorTag(ErrorTag):
    """ErrorTags for simplebench.utils in SimpleBench."""

    # utils.serialize_to_json() tags
    INVALID_SKIPKEYS_ARG_TYPE = 'INVALID_SKIPKEYS_ARG_TYPE'
    """The skipkeys argument was not a bool"""
    INVALID_ENSURE_ASCII_ARG_TYPE = 'INVALID_ENSURE_ASCII_ARG_TYPE'
    """The ensure_ascii argument was not a bool"""
    INVALID_CHECK_CIRCULAR_ARG_TYPE = 'INVALID_CHECK_CIRCULAR_ARG_TYPE'
    """The check_circular argument was not a bool"""
    INVALID_ALLOW_NAN_ARG_TYPE = 'INVALID_ALLOW_NAN_ARG_TYPE'
    """The allow_nan argument was not a bool"""
    INVALID_JSON_ENCODER_CLASS_ARG_TYPE = 'INVALID_JSON_ENCODER_CLASS_ARG_TYPE'
    """The cls argument was not a subclass of json.JSONEncoder"""
    INVALID_INDENT_ARG_TYPE = 'INVALID_INDENT_ARG_TYPE'
    """The indent argument was not an int or str"""
    INVALID_SEPARATORS_ARG_TYPE = 'INVALID_SEPARATORS_ARG_TYPE'
    """The separators argument was not a tuple"""
    INVALID_SEPARATORS_ARG_VALUE = 'INVALID_SEPARATORS_ARG_VALUE'
    """The separators argument was not a tuple of two strings"""
    INVALID_DEFAULT_ARG_TYPE = 'INVALID_DEFAULT_ARG_TYPE'
    """The default argument was not a callable"""
    INVALID_SORT_KEYS_ARG_TYPE = 'INVALID_SORT_KEYS_ARG_TYPE'
    """The sort_keys argument was not a bool"""
    # utils.serialize_to_dict() tags
    SERIALIZATION_INVALID_OBJ_TYPE = 'SERIALIZATION_INVALID_OBJ_TYPE'
    """The object to serialize was not a mapping type"""
    SERIALIZATION_CYCLIC_REFERENCE_DETECTED = 'SERIALIZATION_CYCLIC_REFERENCE_DETECTED'
    """A cyclic reference was detected during serialization"""

    # utils.timestamp_to_iso8601() tags
    TIMESTAMP_TO_ISO8601_INVALID_TIMESTAMP_ARG_TYPE = 'TIMESTAMP_TO_ISO8601_INVALID_TIMESTAMP_ARG_TYPE'
    """The timestamp argument was not a float"""

    # utils.iso8601_to_timestamp() tags
    TIMESTAMP_TO_ISO8601_INVALID_ISO8601_STR_ARG_TYPE = 'TIMESTAMP_TO_ISO8601_INVALID_ISO8601_STR_ARG_TYPE'
    """The iso8601_str argument was not a str"""
    TIMESTAMP_TO_ISO8601_EMPTY_ISO8601_STR_ARG_VALUE = 'TIMESTAMP_TO_ISO8601_EMPTY_ISO8601_STR_ARG_VALUE'
    """The iso8601_str argument was an empty str"""

    # utils.sanitize_filename() tags
    SANITIZE_FILENAME_INVALID_NAME_ARG_TYPE = 'SANITIZE_FILENAME_INVALID_NAME_ARG_TYPE'
    """The filename argument was not a str"""
    SANITIZE_FILENAME_EMPTY_NAME_ARG = 'SANITIZE_FILENAME_EMPTY_NAME_ARG'
    """The filename argument was an empty str"""

    # utils.kwargs_variations() tags
    KWARGS_VARIATIONS_INVALID_KWARGS_ARG_TYPE = 'KWARGS_VARIATIONS_INVALID_KWARGS_ARG_TYPE'
    """The kwargs argument was not a dictionary"""
    KWARGS_VARIATIONS_INVALID_KWARGS_VALUE_TYPE = 'KWARGS_VARIATIONS_INVALID_KWARGS_VALUE_TYPE'
    """A kwargs argument value was not a Sequence (e.g., list, tuple, set) or was a str or bytes instance"""

    # utils.sigfigs() tags
    SIGFIGS_INVALID_NUMBER_ARG_TYPE = 'SIGFIGS_INVALID_NUMBER_ARG_TYPE'
    """The number argument was not an int or float"""
    SIGFIGS_INVALID_FIGURES_ARG_TYPE = 'SIGFIGS_INVALID_FIGURES_ARG_TYPE'
    """The figures argument was not an int"""
    SIGFIGS_INVALID_FIGURES_ARG_VALUE = 'SIGFIGS_INVALID_FIGURES_ARG_VALUE'
    """The figures argument was less than 1"""
    FLAG_TO_ARG_INVALID_FLAG_ARG_TYPE = 'FLAG_TO_ARG_INVALID_FLAG_ARG_TYPE'
    """The flag argument was not a str"""
    FLAG_TO_ARG_EMPTY_FLAG_ARG = 'FLAG_TO_ARG_EMPTY_FLAG_ARG'
    """The flag argument was an empty str"""
    FLAG_TO_ARG_INVALID_FLAG_ARG_VALUE = 'FLAG_TO_ARG_INVALID_FLAG_ARG_VALUE'
    """The flag argument did not start with '--'"""
    ARG_TO_FLAG_INVALID_FLAG_ARG_TYPE = 'ARG_TO_FLAG_INVALID_FLAG_ARG_TYPE'
    """The arg argument was not a str"""
    ARG_TO_FLAG_EMPTY_FLAG_ARG = 'ARG_TO_FLAG_EMPTY_FLAG_ARG'
    """The arg argument was an empty str"""
    COLLECT_ARG_LIST_INVALID_ARG_VALUE_ITEM_TYPE = 'COLLECT_ARG_LIST_INVALID_ARG_VALUE_ITEM_TYPE'
    """An item in the arg_value list of lists was not a str"""
    COLLECT_ARG_LIST_INVALID_ARG_VALUE_TYPE = 'COLLECT_ARG_LIST_INVALID_ARG_VALUE_TYPE'
    """The arg_value argument was not a list of lists"""

    # utils.collect_arg_list() tags
    COLLECT_ARG_LIST_INVALID_ARGS_ARG_TYPE = 'COLLECT_ARG_LIST_INVALID_ARGS_ARG_TYPE'
    """The args argument was not a Namespace instance"""
    COLLECT_ARG_LIST_INVALID_FLAG_ARG_TYPE = 'COLLECT_ARG_LIST_INVALID_FLAG_ARG_TYPE'
    """The flag argument was not a str"""
    COLLECT_ARG_LIST_INVALID_INCLUDE_COMMA_SEPARATED_ARG_TYPE = (
        'COLLECT_ARG_LIST_INVALID_INCLUDE_COMMA_SEPARATED_ARG_TYPE'
    )
    """The include_comma_separated argument was not a bool"""
    COLLECT_ARG_LIST_INVALID_FLAG_ARG_VALUE = 'COLLECT_ARG_LIST_INVALID_FLAG_ARG_VALUE'
    """The flag argument contained invalid characters for a command-line flag"""


@enum_docstrings
class _MathErrorTag(ErrorTag):
    """ErrorTags for simplebench.utils.math in SimpleBench."""

    EMPTY_SEQUENCE = 'EMPTY_SEQUENCE'
    """The input sequence was empty"""
