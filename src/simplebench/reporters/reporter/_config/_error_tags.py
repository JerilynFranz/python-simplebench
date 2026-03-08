"""Error tags for reporter config exceptions."""

from enum import auto
from simplebench.doc_utils import enum_docstrings
from simplebench.exceptions import ErrorTag


@enum_docstrings
class _ReporterConfigErrorTag(ErrorTag):
    """Error tags for reporter configurations."""

    INVALID_NAME_TYPE = auto()
    """The 'name' argument is not a string."""
    INVALID_NAME_VALUE = auto()
    """The 'name' argument is an empty string."""

    INVALID_DESCRIPTION_TYPE = auto()
    """The 'description' argument is not a string."""
    INVALID_DESCRIPTION_VALUE = auto()
    """The 'description' argument is an empty string."""

    INVALID_METRICS_TYPE = auto()
    """The 'metrics' argument is not an iterable of Metric enums."""
    INVALID_METRICS_VALUE = auto()
    """The 'metrics' argument is an empty iterable when not allowed."""

    INVALID_TARGETS_TYPE = auto()
    """The 'targets' argument is not an ElementCollection of Target enums."""
    INVALID_TARGETS_VALUE = auto()
    """The 'targets' argument is an empty ElementCollection when not allowed."""
    INVALID_TARGETS_ELEMENT_TYPE = auto()
    """An element in the 'targets' argument is not a Target enum."""

    INVALID_DEFAULT_TARGETS_TYPE = auto()
    """The 'default_targets' argument is not an ElementCollection of Target enums."""
    INVALID_DEFAULT_TARGETS_ELEMENT_TYPE = auto()
    """An element in the 'default_targets' argument is not a Target enum."""

    INVALID_FORMATS_TYPE = auto()
    """The 'formats' argument is not an ElementCollection of Format enums."""
    INVALID_FORMATS_ELEMENT_TYPE = auto()
    """An element in the 'formats' argument is not a Format enum."""

    INVALID_CHOICES_TYPE = auto()
    """The 'choices' argument is not a ChoicesConf instance."""

    INVALID_FILE_SUFFIX_TYPE = auto()
    """The 'file_suffix' argument is not a string."""
    INVALID_FILE_SUFFIX_VALUE = auto()
    """The 'file_suffix' argument is an empty string or contains non-alphanumeric characters."""
    INVALID_FILE_SUFFIX_VALUE_TOO_LONG = auto()
    """The 'file_suffix' argument exceeds the maximum allowed length."""

    INVALID_FILE_UNIQUE_TYPE = auto()
    """The 'file_unique' argument is not a boolean."""

    INVALID_FILE_APPEND_TYPE = auto()
    """The 'file_append' argument is not a boolean."""

    INVALID_FILE_APPEND_FILE_UNIQUE_COMBINATION = auto()
    """The 'file_append' and 'file_unique' arguments cannot both be True."""

    INVALID_FILE_APPEND_FILE_UNIQUE_ONE_MUST_BE_TRUE = auto()
    """One of the 'file_append' or 'file_unique' arguments must be True."""

    INVALID_SUBDIR_TYPE = auto()
    """The 'subdir' argument is not a string."""
