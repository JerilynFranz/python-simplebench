"""ErrorTags for simplebench.utils in SimpleBench."""

from enum import auto
from simplebench.doc_utils import enum_docstrings
from simplebench.exceptions import ErrorTag


@enum_docstrings
class _UtilsErrorTag(ErrorTag):
    """ErrorTags for simplebench.utils in SimpleBench."""

    # utils.serialize_to_json() tags
    INVALID_SKIPKEYS_ARG_TYPE = auto()
    """The skipkeys argument was not a bool"""
    INVALID_ENSURE_ASCII_ARG_TYPE = auto()
    """The ensure_ascii argument was not a bool"""
    INVALID_CHECK_CIRCULAR_ARG_TYPE = auto()
    """The check_circular argument was not a bool"""
    INVALID_ALLOW_NAN_ARG_TYPE = auto()
    """The allow_nan argument was not a bool"""
    INVALID_JSON_ENCODER_CLASS_ARG_TYPE = auto()
    """The cls argument was not a subclass of json.JSONEncoder"""
    INVALID_INDENT_ARG_TYPE = auto()
    """The indent argument was not an int or str"""
    INVALID_SEPARATORS_ARG_TYPE = auto()
    """The separators argument was not a tuple"""
    INVALID_SEPARATORS_ARG_VALUE = auto()
    """The separators argument was not a tuple of two strings"""
    INVALID_DEFAULT_ARG_TYPE = auto()
    """The default argument was not a callable"""
    INVALID_SORT_KEYS_ARG_TYPE = auto()
    """The sort_keys argument was not a bool"""
    # utils.serialize_to_dict() tags
    SERIALIZATION_INVALID_OBJ_TYPE = auto()
    """The object to serialize was not a mapping type"""
    SERIALIZATION_CYCLIC_REFERENCE_DETECTED = auto()
    """A cyclic reference was detected during serialization"""

    # utils.timestamp_to_iso8601() tags
    TIMESTAMP_TO_ISO8601_INVALID_TIMESTAMP_ARG_TYPE = auto()
    """The timestamp argument was not a float"""

    # utils.iso8601_to_timestamp() tags
    TIMESTAMP_TO_ISO8601_INVALID_ISO8601_STR_ARG_TYPE = auto()
    """The iso8601_str argument was not a str"""
    TIMESTAMP_TO_ISO8601_EMPTY_ISO8601_STR_ARG_VALUE = auto()
    """The iso8601_str argument was an empty str"""

    # utils.sanitize_filename() tags
    SANITIZE_FILENAME_INVALID_NAME_ARG_TYPE = auto()
    """The filename argument was not a str"""
    SANITIZE_FILENAME_EMPTY_NAME_ARG = auto()
    """The filename argument was an empty str"""

    # utils.kwargs_variations() tags
    KWARGS_VARIATIONS_INVALID_KWARGS_ARG_TYPE = auto()
    """The kwargs argument was not a dictionary"""
    KWARGS_VARIATIONS_INVALID_KWARGS_VALUE_TYPE = auto()
    """A kwargs argument value was not a Sequence (e.g., list, tuple, set) or was a str or bytes instance"""

    # utils.sigfigs() tags
    SIGFIGS_INVALID_NUMBER_ARG_TYPE = auto()
    """The number argument was not an int or float"""
    SIGFIGS_INVALID_FIGURES_ARG_TYPE = auto()
    """The figures argument was not an int"""
    SIGFIGS_INVALID_FIGURES_ARG_VALUE = auto()
    """The figures argument was less than 1"""
    FLAG_TO_ARG_INVALID_FLAG_ARG_TYPE = auto()
    """The flag argument was not a str"""
    FLAG_TO_ARG_EMPTY_FLAG_ARG = auto()
    """The flag argument was an empty str"""
    FLAG_TO_ARG_INVALID_FLAG_ARG_VALUE = auto()
    """The flag argument did not start with '--'"""
    ARG_TO_FLAG_INVALID_FLAG_ARG_TYPE = auto()
    """The arg argument was not a str"""
    ARG_TO_FLAG_EMPTY_FLAG_ARG = auto()
    """The arg argument was an empty str"""
    COLLECT_ARG_LIST_INVALID_ARG_VALUE_ITEM_TYPE = auto()
    """An item in the arg_value list of lists was not a str"""
    COLLECT_ARG_LIST_INVALID_ARG_VALUE_TYPE = auto()
    """The arg_value argument was not a list of lists"""

    # utils.collect_arg_list() tags
    COLLECT_ARG_LIST_INVALID_ARGS_ARG_TYPE = auto()
    """The args argument was not a Namespace instance"""
    COLLECT_ARG_LIST_INVALID_FLAG_ARG_TYPE = auto()
    """The flag argument was not a str"""
    COLLECT_ARG_LIST_INVALID_INCLUDE_COMMA_SEPARATED_ARG_TYPE = (
        'COLLECT_ARG_LIST_INVALID_INCLUDE_COMMA_SEPARATED_ARG_TYPE'
    )
    """The include_comma_separated argument was not a bool"""
    COLLECT_ARG_LIST_INVALID_FLAG_ARG_VALUE = auto()
    """The flag argument contained invalid characters for a command-line flag"""


@enum_docstrings
class _MathErrorTag(ErrorTag):
    """ErrorTags for simplebench.utils.math in SimpleBench."""

    EMPTY_SEQUENCE = auto()
    """The input sequence was empty"""
