"""Exception ErrorTags for the rich_table reporter."""
from simplebench.exceptions.base import ErrorTag
from simplebench.enums import enum_docstrings


@enum_docstrings
class RichTableReporterErrorTag(ErrorTag):
    """ErrorTags for exceptions in the rich_table reporter."""
    CHOICE_OPTIONS_INVALID_DEFAULT_TARGETS_TYPE = (
        "CHOICE_OPTIONS_INVALID_DEFAULT_TARGETS_TYPE")
    """The default targets specified in the RichTableChoiceOptions are not valid Target enum members."""
    CHOICE_OPTIONS_INVALID_DEFAULT_TARGETS_VALUE = (
        "CHOICE_OPTIONS_INVALID_DEFAULT_TARGETS_VALUE")
    """The default targets specified in the RichTableChoiceOptions cannot be empty."""
    CHOICE_OPTIONS_INVALID_SUBDIR_TYPE = "CHOICE_OPTIONS_INVALID_SUBDIR_TYPE"
    """The subdir specified in the RichTableChoiceOptions must be a string."""
    CHOICE_OPTIONS_INVALID_SUBDIR_VALUE = "CHOICE_OPTIONS_INVALID_SUBDIR_VALUE"
    """The subdir specified in the RichTableChoiceOptions cannot be an empty string."""
    CHOICE_OPTIONS_INVALID_WIDTH_TYPE = "CHOICE_OPTIONS_INVALID_WIDTH_TYPE"
    """The width specified in the RichTableChoiceOptions must be an integer."""
    CHOICE_OPTIONS_INVALID_WIDTH_VALUE = "CHOICE_OPTIONS_INVALID_WIDTH_VALUE"
    """The width specified in the RichTableChoiceOptions must be greater than zero."""
    CHOICE_OPTIONS_DEFAULT_TARGETS_NOT_ITERABLE = (
        "CHOICE_OPTIONS_DEFAULT_TARGETS_NOT_ITERABLE")
    """The default targets specified in the RichTableChoiceOptions must be an iterable of Target enum members."""
    RUN_REPORT_UNSUPPORTED_TARGET = "RUN_REPORT_UNSUPPORTED_TARGET"
    """The rich table reporter does not support a target included in the targets."""
    RUN_REPORT_INVALID_CHOICE_OPTIONS_TYPE = "RUN_REPORT_INVALID_CHOICE_OPTIONS_TYPE"
    """The choice_options argument passed to RichTableReporter.report() is not a RichTableChoiceOptions instance."""
