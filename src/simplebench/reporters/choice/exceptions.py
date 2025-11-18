"""ErrorTags for :class:`~.Choice` class related exceptions."""
from simplebench.enums import enum_docstrings
from simplebench.exceptions import ErrorTag


@enum_docstrings
class ChoiceErrorTag(ErrorTag):
    """ErrorTags for :class:`~.Choice` class related exceptions."""
    INVALID_REPORTER_ARG_TYPE = "INVALID_REPORTER_ARG_TYPE"
    """Something other than a :class:`~simplebench.reporters.reporter.Reporter` subclass was
    passed as the ``reporter`` arg"""
    INVALID_FLAGS_ARGS_VALUE = "EMPTY_FLAGS_ARGS_VALUE"
    """The ``flags`` arg cannot be an empty sequence or contain strings with whitespace"""
    INVALID_FLAGS_ARG_TYPE = "INVALID_FLAGS_ARG_TYPE"
    """Something other than a sequence of string was passed as the ``flags`` arg"""
    INVALID_NAME_ARG_TYPE = "INVALID_NAME_ARG_TYPE"
    """Something other than a string was passed as the ``name`` arg"""
    EMPTY_NAME_ARG_VALUE = "EMPTY_NAME_ARG_VALUE"
    """The ``name`` arg cannot be an empty string"""
    INVALID_DESCRIPTION_ARG_TYPE = "INVALID_DESCRIPTION_ARG_TYPE"
    """Something other than a string was passed as the ``description`` arg"""
    EMPTY_DESCRIPTION_ARG_VALUE = "EMPTY_DESCRIPTION_ARG_VALUE"
    """The ``description`` arg cannot be an empty string"""
    INVALID_SECTIONS_ARG_TYPE = "INVALID_SECTIONS_ARG_TYPE"
    """Something other than a sequence of :class:`~simplebench.enums.Section` enums was passed
    as the ``sections`` arg"""
    EMPTY_SECTIONS_ARG_VALUE = "EMPTY_SECTIONS_ARG_VALUE"
    """The ``sections`` arg cannot be an empty sequence"""
    INVALID_TARGETS_ARG_TYPE = "INVALID_TARGETS_ARG_TYPE"
    """Something other than a sequence of :class:`~simplebench.enums.Target` enums was passed
    as the ``targets`` arg"""
    EMPTY_TARGETS_ARG_VALUE = "EMPTY_TARGETS_ARG_VALUE"
    """The ``targets`` arg cannot be an empty sequence"""
    INVALID_SUBDIR_ARG_TYPE = "INVALID_SUBDIR_ARG_TYPE"
    """Something other than a string was passed as the ``subdir`` arg"""
    INVALID_SUBDIR_ARG_VALUE = "INVALID_SUBDIR_ARG_VALUE"
    """The ``subdir`` arg must be an alphanumeric string (a-z, A-Z, 0-9) or an empty string"""
    SUBDIR_TOO_LONG = "SUBDIR_TOO_LONG"
    """The ``subdir`` arg cannot be longer than 64 characters."""
    INVALID_OUTPUT_FORMAT_ARG_TYPE = "INVALID_OUTPUT_FORMAT_ARG_TYPE"
    """Something other than a :class:`~simplebench.enums.Format` instance was passed as the
    ``output_format`` arg"""
    INVALID_OPTIONS_ARG_TYPE = "INVALID_OPTIONS_ARG_TYPE"
    """Something other than a
    :class:`~simplebench.reporters.reporter.options.ReporterOptions` instance was passed as
    the ``options`` arg"""
    INVALID_OPTIONS_ARG_VALUE = "INVALID_OPTIONS_ARG_VALUE"
    """The ``options`` arg contained something other than a
    :class:`~simplebench.reporters.reporter.options.ReporterOptions` instance"""
    INVALID_FLAG_TYPE_ARG_TYPE = "INVALID_FLAG_TYPE_ARG_TYPE"
    """Something other than a :class:`~simplebench.enums.FlagType` enum was passed as the
    ``flag_type`` arg"""
    INVALID_FILE_SUFFIX_ARG_TYPE = "INVALID_FILE_SUFFIX_ARG_TYPE"
    """Something other than a string was passed as the ``file_suffix`` arg"""
    EMPTY_FILE_SUFFIX_ARG_VALUE = "EMPTY_FILE_SUFFIX_ARG_VALUE"
    """The ``file_suffix`` arg cannot be an blank string (consist only of whitespace),
    contain non-alphanumeric characters, or be longer than 10 characters."""
    FILE_SUFFIX_TOO_LONG = "FILE_SUFFIX_TOO_LONG"
    """The ``file_suffix`` arg cannot be longer than 10 characters."""
    INVALID_FILE_UNIQUE_ARG_TYPE = "INVALID_FILE_UNIQUE_ARG_TYPE"
    """Something other than a boolean or ``None`` was passed as the ``file_unique`` arg"""
    INVALID_FILE_APPEND_ARG_TYPE = "INVALID_FILE_APPEND_ARG_TYPE"
    """Something other than a boolean or ``None`` was passed as the ``file_append`` arg"""
