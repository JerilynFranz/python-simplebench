"""ErrorTags for simplebench.validators in SimpleBench."""

from enum import auto
from simplebench.doc_utils import enum_docstrings
from simplebench.exceptions import ErrorTag


@enum_docstrings
class _ValidatorsErrorTag(ErrorTag):
    """ErrorTags for validator-related exceptions."""

    # validated_dirname() tags
    VALIDATE_DIRNAME_INVALID_DIRNAME_ARG_TYPE = auto()
    """The 'dirname' argument must be a str."""
    VALIDATE_DIRNAME_TOO_LONG = auto()
    """The 'dirname' argument cannot be longer than 255 characters."""
    VALIDATE_DIRNAME_EMPTY_NOT_ALLOWED = auto()
    """The 'dirname' argument cannot be an empty string."""
    VALIDATE_DIRNAME_INVALID_CHARACTERS = auto()
    """The 'dirname' argument contains invalid characters."""



    # general tags
    INVALID_NAME_PARAM_TYPE = auto()
    """The 'name' parameter is not of type str."""
    INVALID_NAME_PARAM_VALUE = auto()
    """The 'name' parameter is an empty or blank string."""
    INVALID_KEY_TYPE = auto()
    """A key in a mapping is not of type str."""
    INVALID_KEY_VALUE = auto()
    """A key in a mapping is an empty or blank string."""
    INVALID_PREVIOUSLY_SEEN_PARAM_TYPE = auto()
    """The 'previously_seen' parameter is not of type set."""

    # validate_core_mapping() tags
    INVALID_CORE_MAPPING_PARAM_TYPE = auto()
    """The 'value' parameter is not of type Mapping[str, CoreDataTypes]."""
    INVALID_CORE_MAPPING_PARAM_VALUE = auto()
    """The 'value' parameter contains invalid CoreDataTypes elements."""
    RECURSION_LIMIT_REACHED = auto()
    """Recursion limit reached during validation."""

    # validate_namespaced_identifier() tags
    INVALID_TYPE_ERROR_TAG_TYPE = auto()
    """The type_error_tag is not of type ErrorTag."""
    INVALID_VALUE_ERROR_TAG_TYPE = auto()
    """The value_error_tag is not of type ErrorTag."""
    INVALID_NAMESPACED_IDENTIFIER_TYPE = auto()
    """The namespaced identifier is not of type string."""
    INVALID_NAMESPACED_IDENTIFIER = auto()
    """The namespaced identifier is not valid."""

    # validate_dirpath() tags
    VALIDATE_DIRPATH_INVALID_FIELD_NAME_ARG_TYPE = auto()
    """The 'field_name' argument must be a str."""
    VALIDATE_DIRPATH_INVALID_DIRPATH_ARG_TYPE = auto()
    """The 'dirpath' argument must be a str."""
    VALIDATE_DIRPATH_INVALID_DIRPATH_ARG_VALUE = auto()
    """The 'dirpath' argument has an invalid value."""
    VALIDATE_DIRPATH_INVALID_ALLOW_EMPTY_ARG_TYPE = auto()
    """The 'allow_empty' argument must be a bool."""
    VALIDATE_DIRPATH_INVALID_CHARACTERS = auto()
    """The 'dirpath' argument contains invalid characters."""
    VALIDATE_DIRPATH_INVALID_START_END = auto()
    """The 'dirpath' argument cannot start or end with a slash or backslash."""
    VALIDATE_DIRPATH_ELEMENT_HAS_INVALID_CHARACTERS = auto()
    """An element of the 'dirpath' argument contains invalid characters."""
    VALIDATE_DIRPATH_ELEMENT_EMPTY = auto()
    """An element of the 'dirpath' argument is empty."""
    VALIDATE_DIRPATH_ELEMENT_TOO_LONG = auto()
    """An element of the 'dirpath' argument is too long (max 64 characters)."""
    VALIDATE_DIRPATH_TOO_LONG = auto()
    """The 'dirpath' argument is too long (max 255 characters)."""

    # validate_bool() tags
    VALIDATE_BOOL_INVALID_NAME_ARG_TYPE = auto()
    """The 'name' argument must be a str."""
    VALIDATE_BOOL_INVALID_ERROR_TAG_TYPE = auto()
    """The 'error_tag' argument must be an ErrorTag."""
    VALIDATE_BOOL_INVALID_ALLOW_NONE_ARG_TYPE = auto()
    """The 'allow_none' argument must be a bool."""

    INVALID_PATH_TYPE = auto()
    """A non-str, non-pathlib.Path type was passed as a path."""
    PATH_DOES_NOT_EXIST = auto()
    """The provided path does not exist."""
    PATH_NOT_A_FILE = auto()
    """The provided path is not a file."""
    PATH_NOT_A_DIRECTORY = auto()
    """The provided path is not a directory."""
    INVALID_FIELD_NAME_TYPE = auto()
    """The 'field_name' argument must be a str."""
    INVALID_MIN_VALUE_TYPE = auto()
    """The 'min_value' argument has an invalid type."""
    INVALID_MAX_VALUE_TYPE = auto()
    """The 'max_value' argument has an invalid type."""
    INVALID_RANGE = auto()
    """The 'min_value' cannot be greater than 'max_value'."""

    # validate_type() tags
    VALIDATE_TYPE_INVALID_EXPECTED_ARG_TYPE = auto()
    """The expected argument was not a type."""
    VALIDATE_TYPE_INVALID_EXPECTED_ARG_ITEM_TYPE = auto()
    """An item in the expected argument tuple was not a type."""
    VALIDATE_TYPE_INVALID_NAME_ARG_TYPE = auto()
    """The name argument was not a str."""
    VALIDATE_TYPE_INVALID_ERROR_TAG_TYPE = auto()
    """The error_tag argument was not an ErrorTag."""

    # validate_string() tags
    INVALID_STRIP_ARG_TYPE = auto()
    """The 'strip' argument must be a bool."""
    INVALID_ALLOW_EMPTY_ARG_TYPE = auto()
    """The 'allow_empty' argument must be a bool."""
    INVALID_ALLOW_BLANK_ARG_TYPE = auto()
    """The 'allow_blank' argument must be a bool."""
    INVALID_ALPHANUMERIC_ONLY_ARG_TYPE = auto()
    """The 'alphanumeric_only' argument must be a bool."""
    CONFLICTING_STRING_VALIDATION_OPTIONS_ALLOW_EMPTY = auto()
    """Cannot have strip=True, allow_blank=True, and allow_empty=False set together."""
    CONFLICTING_STRING_VALIDATION_OPTIONS_ALPHANUMERIC_ONLY = auto()
    """Cannot have strip=True, allow_blank=True, and alphanumeric_only=True set together."""
    INVALID_MESSAGE_ARG_TYPE = auto()
    """The 'message' argument must be a str."""

    # validate_filename() tags
    VALIDATE_FILENAME_INVALID_FILENAME_ARG_TYPE = auto()
    """Something other than a string was passed to validate_filename()as the filename argument"""
    VALIDATE_FILENAME_SUFFIX_TOO_LONG = auto()
    """The filename arg passed to validate_filename() has a suffix (the part after the dot) longer than 10 characters"""
    VALIDATE_FILENAME_INVALID_STEM = auto()
    """The filename argument passed to validate_filename() has an invalid stem (name without suffix)"""
    VALIDATE_FILENAME_SUFFIX_NOT_ALPHANUMERIC = auto()
    """The suffix (the part after the dot) of the filename argument passed to
    validate_filename() contains non-alphanumeric characters"""
    VALIDATE_FILENAME_TOO_LONG = auto()
    """The filename argument passed to validate_filename() is longer than 255 characters"""
    VALIDATE_FILENAME_STEM_NOT_ALPHANUMERIC = auto()
    """The stem (name without suffix) of the filename argument passed to validate_filename()
    contains non-alphanumeric characters"""

    # validate_iterable_of_type() tags
    VALIDATE_ITERABLE_OF_TYPE_INVALID_TYPES_ARG = auto()
    """The 'types' argument must be a type or a tuple of types."""
    VALIDATE_ITERABLE_OF_TYPE_INVALID_FIELD_NAME_ARG_TYPE = auto()
    """The 'field_name' argument must be a str."""
    VALIDATE_ITERABLE_OF_TYPE_INVALID_TYPE_TAG_TYPE = auto()
    """The 'type_tag' argument must be an ErrorTag."""
    VALIDATE_ITERABLE_OF_TYPE_INVALID_VALUE_TAG_TYPE = auto()
    """The 'value_tag' argument must be an ErrorTag."""
    VALIDATE_ITERABLE_OF_TYPE_INVALID_ALLOW_EMPTY_ARG_TYPE = auto()
    """The 'allow_empty' argument must be a bool."""
    VALIDATE_ITERABLE_OF_TYPE_INVALID_EXACT_TYPE_ARG_TYPE = auto()
    """The 'exact_type' argument must be a bool."""

    # validate_sequence_of_type() tags
    VALIDATE_SEQUENCE_OF_TYPE_INVALID_TYPES_ARG = auto()
    """The 'types' argument must be a type or a tuple of types."""
    VALIDATE_SEQUENCE_OF_TYPE_INVALID_FIELD_NAME_ARG_TYPE = auto()
    """The 'field_name' argument must be a str."""
    VALIDATE_SEQUENCE_OF_TYPE_INVALID_TYPE_TAG_TYPE = auto()
    """The 'type_tag' argument must be an ErrorTag."""
    VALIDATE_SEQUENCE_OF_TYPE_INVALID_VALUE_TAG_TYPE = auto()
    """The 'value_tag' argument must be an ErrorTag."""
    VALIDATE_SEQUENCE_OF_TYPE_INVALID_ALLOW_EMPTY_ARG_TYPE = auto()
    """The 'allow_empty' argument must be a bool."""
    VALIDATE_SEQUENCE_OF_TYPE_INVALID_EXACT_TYPE_ARG_TYPE = auto()
    """The 'exact_type' argument must be a bool."""

    # Core data types validation tags
    INVALID_CACHE_TYPE = auto()
    """The provided cache size is not an integer."""
    INVALID_CACHE_SIZE = auto()
    """The provided cache size is less than 1."""
