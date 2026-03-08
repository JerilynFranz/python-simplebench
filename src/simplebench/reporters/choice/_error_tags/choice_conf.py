"""ErrorTags for ChoiceConf class"""

from enum import auto
from simplebench.doc_utils import enum_docstrings
from simplebench.exceptions import ErrorTag


@enum_docstrings
class _ChoiceConfErrorTag(ErrorTag):
    """ErrorTags for ChoiceConf class."""

    OPTIONS_INVALID_ARG_VALUE_NOT_IMMUTABLE = auto()
    """The extra argument is not immutable."""
    FLAG_TYPE_INVALID_ARG_TYPE = auto()
    """The flag_type argument is not a FlagType enum value."""
    FLAGS_INVALID_ARG_TYPE = auto()
    """The flags argument is not a Sequence of strings."""
    FLAGS_INVALID_ARGS_VALUE = auto()
    """One or more items in the flags argument is an empty string,
    blank string, or whitespace-only string."""
    NAME_INVALID_ARG_TYPE = auto()
    """The name argument is not a string."""
    NAME_INVALID_ARG_VALUE = auto()
    """The name argument is an empty string or blank string."""
    DESCRIPTION_INVALID_ARG_TYPE = auto()
    """The description argument is not a string."""
    DESCRIPTION_INVALID_ARG_VALUE = auto()
    """The description argument is an empty string or blank string."""
    METRICS_INVALID_ARG_TYPE = auto()
    """The metrics argument is not a MetricsSelection instance."""
    METRICS_INVALID_ARG_VALUE = auto()
    """Empty MetricsSelection instance provided for metrics argument."""
    TARGETS_INVALID_ARG_TYPE = auto()
    """The targets argument is not a Sequence of Target enum values."""
    TARGETS_INVALID_ARG_VALUE = auto()
    """One or more items in the targets argument is not a Target enum value,
    or the targets argument is an empty sequence."""
    DEFAULT_TARGETS_INVALID_ARG_TYPE = auto()
    """The default_targets argument is not a Sequence of Target enum values."""
    DEFAULT_TARGETS_INVALID_ARG_VALUE = auto()
    """One or more items in the default_targets argument is not a Target enum value."""
    SUBDIR_INVALID_ARG_TYPE = auto()
    """The subdir argument is not a string."""
    SUBDIR_INVALID_ARG_VALUE = auto()
    """The subdir argument is not alphanumeric or is a blank string."""
    SUBDIR_TOO_LONG = auto()
    """The subdir argument is longer than 64 characters."""
    FILE_SUFFIX_INVALID_ARG_TYPE = auto()
    """The file_suffix argument is not a string."""
    FILE_SUFFIX_INVALID_ARG_VALUE = auto()
    """The file_suffix argument is a blank string, contains non-alphanumeric characters,
    or is longer than 10 characters."""
    FILE_SUFFIX_TOO_LONG = auto()
    """The file_suffix argument is longer than 10 characters."""
    FILE_UNIQUE_INVALID_ARG_TYPE = auto()
    """The file_unique argument is not a boolean value or None."""
    FILE_APPEND_INVALID_ARG_TYPE = auto()
    """The file_append argument is not a boolean value or None."""
    FILE_UNIQUE_FILE_APPEND_MUTUALLY_EXCLUSIVE = auto()
    """The file_unique and file_append arguments cannot both be set to True or both be set to False."""
    OUTPUT_FORMAT_INVALID_ARG_TYPE = auto()
    """The output_format argument is not a Format enum value."""
    OPTIONS_INVALID_ARG_TYPE = auto()
    """The options argument is not a ReporterOptions instance."""
    OPTIONS_INVALID_ARG_VALUE = auto()
    """One or more items in the options argument is not a ReporterOptions instance."""
