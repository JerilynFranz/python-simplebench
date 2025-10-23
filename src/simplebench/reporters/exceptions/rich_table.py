"""Exception ErrorTags for the rich_table reporter."""
from simplebench.exceptions.base import ErrorTag
from simplebench.enums import enum_docstrings


@enum_docstrings
class RichTableReporterErrorTag(ErrorTag):
    """ErrorTags for exceptions in the rich_table reporter."""
    INIT_INVALID_CASE_ARG = "INIT_INVALID_CASE_ARG"
    """Something other than a Case instance was passed to the RichTableReporter() constructor"""
    INIT_INVALID_SESSION_ARG = "INIT_INVALID_SESSION_ARG"
    """Something other than a Session instance was passed to the RichTableReporter() constructor"""
    REPORT_INVALID_CASE_ARG = "REPORT_INVALID_CASE_ARG"
    """Something other than a Case instance was passed to the RichTableReporter.report() method"""
    REPORT_INVALID_SESSION_ARG = "REPORT_INVALID_SESSION_ARG"
    """Something other than a Session instance was passed to the RichTableReporter.report() method"""
    REPORT_INVALID_CHOICE_ARG = "REPORT_INVALID_CHOICE_ARG"
    """Something other than a Choice instance was passed to the RichTableReporter.report() method"""
    REPORT_UNSUPPORTED_SECTION = "REPORT_UNSUPPORTED_SECTION"
    """An unsupported Section was passed to the RichTableReporter.report() method in the Choice.sections"""
    REPORT_UNSUPPORTED_TARGET = "REPORT_UNSUPPORTED_TARGET"
    """An unsupported Target was passed to the RichTableReporter.report() method in the Choice.targets"""
    REPORT_UNSUPPORTED_FORMAT = "REPORT_UNSUPPORTED_FORMAT"
    """An unsupported Format was passed to the RichTableReporter.report() method in the Choice.formats"""
    REPORT_MISSING_PATH_ARG = "REPORT_MISSING_PATH_ARG"
    """The required 'path' argument was not passed to the RichTableReporter.report() method"""
    REPORT_INVALID_PATH_ARG = "REPORT_INVALID_PATH_ARG"
    """Something other than a Path instance was passed to the RichTableReporter.report() method"""
    REPORT_INVALID_CALLBACK_ARG = "REPORT_INVALID_CALLBACK_ARG"
    """Something other than a callable was passed to the RichTableReporter.report() method as the callback argument"""
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
