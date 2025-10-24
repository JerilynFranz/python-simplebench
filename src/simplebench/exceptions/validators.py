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
