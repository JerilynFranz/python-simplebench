"""Error tags for reporter config exceptions."""
from simplebench.enums import enum_docstrings
from simplebench.exceptions import ErrorTag


@enum_docstrings
class _ReporterConfigErrorTag(ErrorTag):
    """Error tags for reporter configurations."""
    INVALID_NAME_TYPE = "INVALID_NAME_TYPE"
    """The 'name' argument is not a string."""
    INVALID_NAME_VALUE = "INVALID_NAME_VALUE"
    """The 'name' argument is an empty string."""

    INVALID_DESCRIPTION_TYPE = "INVALID_DESCRIPTION_TYPE"
    """The 'description' argument is not a string."""
    INVALID_DESCRIPTION_VALUE = "INVALID_DESCRIPTION_VALUE"
    """The 'description' argument is an empty string."""

    INVALID_SECTIONS_TYPE = "INVALID_SECTIONS_TYPE"
    """The 'sections' argument is not an iterable of Section enums."""
    INVALID_SECTIONS_VALUE = "INVALID_SECTIONS_VALUE"
    """The 'sections' argument is an empty iterable when not allowed."""

    INVALID_TARGETS_TYPE = "INVALID_TARGETS_TYPE"
    """The 'targets' argument is not an iterable of Target enums."""
    INVALID_TARGETS_VALUE = "INVALID_TARGETS_VALUE"
    """The 'targets' argument is an empty iterable when not allowed."""

    INVALID_DEFAULT_TARGETS_TYPE = "INVALID_DEFAULT_TARGETS_TYPE"
    """The 'default_targets' argument is not an iterable of Target enums."""
    INVALID_DEFAULT_TARGETS_VALUE = "INVALID_DEFAULT_TARGETS_VALUE"
    """The 'default_targets' argument is an empty iterable when not allowed."""

    INVALID_FORMATS_TYPE = "INVALID_FORMATS_TYPE"
    """The 'formats' argument is not an iterable of Format enums."""
    INVALID_FORMATS_VALUE = "INVALID_FORMATS_VALUE"
    """The 'formats' argument is an empty iterable when not allowed."""

    INVALID_CHOICES_TYPE = "INVALID_CHOICES_TYPE"
    """The 'choices' argument is not a ChoicesConf instance."""

    INVALID_FILE_SUFFIX_TYPE = "INVALID_FILE_SUFFIX_TYPE"
    """The 'file_suffix' argument is not a string."""
    INVALID_FILE_SUFFIX_VALUE = "INVALID_FILE_SUFFIX_VALUE"
    """The 'file_suffix' argument is an empty string or contains non-alphanumeric characters."""
    INVALID_FILE_SUFFIX_VALUE_TOO_LONG = "INVALID_FILE_SUFFIX_VALUE_TOO_LONG"
    """The 'file_suffix' argument exceeds the maximum allowed length."""

    INVALID_FILE_UNIQUE_TYPE = "INVALID_FILE_UNIQUE_TYPE"
    """The 'file_unique' argument is not a boolean."""

    INVALID_FILE_APPEND_TYPE = "INVALID_FILE_APPEND_TYPE"
    """The 'file_append' argument is not a boolean."""

    INVALID_FILE_APPEND_FILE_UNIQUE_COMBINATION = "INVALID_FILE_APPEND_FILE_UNIQUE_COMBINATION"
    """The 'file_append' and 'file_unique' arguments cannot both be True."""

    INVALID_FILE_APPEND_FILE_UNIQUE_ONE_MUST_BE_TRUE = "INVALID_FILE_APPEND_FILE_UNIQUE_ONE_MUST_BE_TRUE"
    """One of the 'file_append' or 'file_unique' arguments must be True."""

    INVALID_SUBDIR_TYPE = "INVALID_SUBDIR_TYPE"
    """The 'subdir' argument is not a string."""
