"""ErrorTags for simplebench.utils in SimpleBench."""
from ..enums import enum_docstrings
from .base import ErrorTag


@enum_docstrings
class _UtilsErrorTag(ErrorTag):
    """ErrorTags for simplebench.utils in SimpleBench."""
    # utils.sanitize_filename() tags
    SANITIZE_FILENAME_INVALID_NAME_ARG_TYPE = "SANITIZE_FILENAME_INVALID_NAME_ARG_TYPE"
    """The filename argument was not a str"""
    SANITIZE_FILENAME_EMPTY_NAME_ARG = "SANITIZE_FILENAME_EMPTY_NAME_ARG"
    """The filename argument was an empty str"""

    # utils.kwargs_variations() tags
    KWARGS_VARIATIONS_INVALID_KWARGS_ARG_TYPE = "KWARGS_VARIATIONS_INVALID_KWARGS_ARG_TYPE"
    """The kwargs argument was not a dictionary"""
    KWARGS_VARIATIONS_INVALID_KWARGS_VALUE_TYPE = "KWARGS_VARIATIONS_INVALID_KWARGS_VALUE_TYPE"
    """A kwargs argument value was not a Sequence (e.g., list, tuple, set) or was a str or bytes instance"""

    # utils.sigfigs() tags
    SIGFIGS_INVALID_NUMBER_ARG_TYPE = "SIGFIGS_INVALID_NUMBER_ARG_TYPE"
    """The number argument was not an int or float"""
    SIGFIGS_INVALID_FIGURES_ARG_TYPE = "SIGFIGS_INVALID_FIGURES_ARG_TYPE"
    """The figures argument was not an int"""
    SIGFIGS_INVALID_FIGURES_ARG_VALUE = "SIGFIGS_INVALID_FIGURES_ARG_VALUE"
    """The figures argument was less than 1"""
    FLAG_TO_ARG_INVALID_FLAG_ARG_TYPE = "FLAG_TO_ARG_INVALID_FLAG_ARG_TYPE"
    """The flag argument was not a str"""
    FLAG_TO_ARG_EMPTY_FLAG_ARG = "FLAG_TO_ARG_EMPTY_FLAG_ARG"
    """The flag argument was an empty str"""
    FLAG_TO_ARG_INVALID_FLAG_ARG_VALUE = "FLAG_TO_ARG_INVALID_FLAG_ARG_VALUE"
    """The flag argument did not start with '--'"""
    ARG_TO_FLAG_INVALID_FLAG_ARG_TYPE = "ARG_TO_FLAG_INVALID_FLAG_ARG_TYPE"
    """The arg argument was not a str"""
    ARG_TO_FLAG_EMPTY_FLAG_ARG = "ARG_TO_FLAG_EMPTY_FLAG_ARG"
    """The arg argument was an empty str"""
    COLLECT_ARG_LIST_INVALID_ARG_VALUE_ITEM_TYPE = "COLLECT_ARG_LIST_INVALID_ARG_VALUE_ITEM_TYPE"
    """An item in the arg_value list of lists was not a str"""
    COLLECT_ARG_LIST_INVALID_ARG_VALUE_TYPE = "COLLECT_ARG_LIST_INVALID_ARG_VALUE_TYPE"
    """The arg_value argument was not a list of lists"""

    # utils.collect_arg_list() tags
    COLLECT_ARG_LIST_INVALID_ARGS_ARG_TYPE = "COLLECT_ARG_LIST_INVALID_ARGS_ARG_TYPE"
    """The args argument was not a Namespace instance"""
    COLLECT_ARG_LIST_INVALID_FLAG_ARG_TYPE = "COLLECT_ARG_LIST_INVALID_FLAG_ARG_TYPE"
    """The flag argument was not a str"""
    COLLECT_ARG_LIST_INVALID_INCLUDE_COMMA_SEPARATED_ARG_TYPE = (
        "COLLECT_ARG_LIST_INVALID_INCLUDE_COMMA_SEPARATED_ARG_TYPE")
    """The include_comma_separated argument was not a bool"""
    COLLECT_ARG_LIST_INVALID_FLAG_ARG_VALUE = "COLLECT_ARG_LIST_INVALID_FLAG_ARG_VALUE"
    """The flag argument contained invalid characters for a command-line flag"""
