"""ErrorTags for simplebench.validators in SimpleBench."""
from .base import ErrorTag
from ..enums import enum_docstrings


@enum_docstrings
class ValidatorsErrorTag(ErrorTag):
    """ErrorTags for validator-related exceptions."""
    INVALID_PATH_TYPE = "INVALID_PATH_TYPE"
    """A non-str, non-pathlib.Path type was passed as a path."""
    PATH_DOES_NOT_EXIST = "PATH_DOES_NOT_EXIST"
    """The provided path does not exist."""
    PATH_NOT_A_FILE = "PATH_NOT_A_FILE"
    """The provided path is not a file."""
    PATH_NOT_A_DIRECTORY = "PATH_NOT_A_DIRECTORY"
    """The provided path is not a directory."""
    INVALID_FIELD_NAME_TYPE = "INVALID_FIELD_NAME_TYPE"
    """The 'field_name' argument must be a str."""
    INVALID_MIN_VALUE_TYPE = "INVALID_MIN_VALUE_TYPE"
    """The 'min_value' argument has an invalid type."""
    INVALID_MAX_VALUE_TYPE = "INVALID_MAX_VALUE_TYPE"
    """The 'max_value' argument has an invalid type."""
    INVALID_RANGE = "INVALID_RANGE"
    """The 'min_value' cannot be greater than 'max_value'."""

    # validate_type() tags
    VALIDATE_TYPE_INVALID_EXPECTED_ARG_TYPE = "VALIDATE_TYPE_INVALID_EXPECTED_ARG_TYPE"
    """The expected argument was not a type."""
    VALIDATE_TYPE_INVALID_EXPECTED_ARG_ITEM_TYPE = "VALIDATE_TYPE_INVALID_EXPECTED_ARG_ITEM_TYPE"
    """An item in the expected argument tuple was not a type."""
    VALIDATE_TYPE_INVALID_NAME_ARG_TYPE = "VALIDATE_TYPE_INVALID_NAME_ARG_TYPE"
    """The name argument was not a str."""

    # validate.py - validate_reporter_callback() tags
    INVALID_REPORTER_CALLBACK_NOT_CALLABLE_OR_NONE = "INVALID_REPORTER_CALLBACK_NOT_CALLABLE_OR_NONE"
    """The reporter callback is neither a callable nor None"""
    INVALID_REPORTER_CALLBACK_INCORRECT_NUMBER_OF_PARAMETERS = (
        "INVALID_REPORTER_CALLBACK_INCORRECT_NUMBER_OF_PARAMETERS")
    """The reporter callback does not have the correct number of parameters"""

    # validate.py - validate_callback() tags
    INVALID_CALLBACK_UNRESOLVABLE_HINTS = "INVALID_CALLBACK_UNRESOLVABLE_HINTS"
    """The type hints for the callback function could not be resolved"""

    # validate.py - validate_callback_parameter() tags
    INVALID_CALLBACK_INCORRECT_SIGNATURE_MISSING_PARAMETER = (
        "INVALID_CALLBACK_INCORRECT_SIGNATURE_MISSING_PARAMETER")
    """The callback function is missing a required parameter"""
    INVALID_CALLBACK_INCORRECT_SIGNATURE_PARAMETER_TYPE = (
        "INVALID_CALLBACK_INCORRECT_SIGNATURE_PARAMETER_TYPE")
    """The callback function has a parameter with an incorrect type annotation"""
    INVALID_CALLBACK_INCORRECT_SIGNATURE_PARAMETER_NOT_KEYWORD_ONLY = (
        "INVALID_CALLBACK_INCORRECT_SIGNATURE_PARAMETER_NOT_KEYWORD_ONLY")
    """The callback function has a parameter that is not keyword-only"""

    # validate_string() tags
    INVALID_STRIP_ARG_TYPE = "INVALID_STRIP_ARG_TYPE"
    """The 'strip' argument must be a bool."""
    INVALID_ALLOW_EMPTY_ARG_TYPE = "INVALID_ALLOW_EMPTY_ARG_TYPE"
    """The 'allow_empty' argument must be a bool."""
    INVALID_ALLOW_BLANK_ARG_TYPE = "INVALID_ALLOW_BLANK_ARG_TYPE"
    """The 'allow_blank' argument must be a bool."""
    INVALID_ALPHANUMERIC_ONLY_ARG_TYPE = "INVALID_ALPHANUMERIC_ONLY_ARG_TYPE"
    """The 'alphanumeric_only' argument must be a bool."""
    CONFLICTING_STRING_VALIDATION_OPTIONS_ALLOW_EMPTY = (
        "CONFLICTING_STRING_VALIDATION_OPTIONS_ALLOW_EMPTY")
    """Cannot have strip=True, allow_blank=True, and allow_empty=False set together."""
    CONFLICTING_STRING_VALIDATION_OPTIONS_ALPHANUMERIC_ONLY = (
        "CONFLICTING_STRING_VALIDATION_OPTIONS_ALPHANUMERIC_ONLY")
    """Cannot have strip=True, allow_blank=True, and alphanumeric_only=True set together."""

    # validate_filename() tags
    VALIDATE_FILENAME_INVALID_FILENAME_ARG_TYPE = "VALIDATE_FILENAME_INVALID_FILENAME_ARG_TYPE"
    """Something other than a string was passed to validate_filename()as the filename argument"""
    VALIDATE_FILENAME_SUFFIX_TOO_LONG = "VALIDATE_FILENAME_SUFFIX_TOO_LONG"
    """The filename arg passed to validate_filename() has a suffix (the part after the dot) longer than 10 characters"""
    VALIDATE_FILENAME_INVALID_STEM = "VALIDATE_FILENAME_INVALID_STEM"
    """The filename argument passed to validate_filename() has an invalid stem (name without suffix)"""
    VALIDATE_FILENAME_SUFFIX_NOT_ALPHANUMERIC = "VALIDATE_FILENAME_SUFFIX_NOT_ALPHANUMERIC"
    """The suffix (the part after the dot) of the filename argument passed to
    validate_filename() contains non-alphanumeric characters"""
    VALIDATE_FILENAME_TOO_LONG = "VALIDATE_FILENAME_TOO_LONG"
    """The filename argument passed to validate_filename() is longer than 255 characters"""
    VALIDATE_FILENAME_STEM_NOT_ALPHANUMERIC = "VALIDATE_FILENAME_STEM_NOT_ALPHANUMERIC"
    """The stem (name without suffix) of the filename argument passed to validate_filename()
    contains non-alphanumeric characters"""
