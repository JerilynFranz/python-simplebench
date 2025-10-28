"""ErrorTags for the simplebench.reporters.json module."""
from simplebench.exceptions import ErrorTag
from simplebench.enums import enum_docstrings


@enum_docstrings
class JSONReporterErrorTag(ErrorTag):
    """ErrorTags for the JSONReporter class."""
    RENDER_INVALID_CASE = "RENDER_INVALID_CASE"
    """An invalid Case instance was passed to the JSONReporter.render() method."""
    RENDER_INVALID_SECTION = "RENDER_INVALID_SECTION"
    """An invalid Section enum member was passed to the JSONReporter.render() method."""
    RENDER_INVALID_OPTIONS = "RENDER_INVALID_OPTIONS"
    """An invalid JSONOptions instance was passed to the JSONReporter.render() method."""
    RUN_REPORT_UNSUPPORTED_TARGET = "RUN_REPORT_UNSUPPORTED_TARGET"
    """An unsupported Target was passed to the reporter's run_report() method"""
    JSON_OUTPUT_ERROR = "JSON_OUTPUT_ERROR"
    """An error occurred while serializing the JSON output."""
    RUN_REPORT_INVALID_DEFAULT_TARGETS_TYPE = "RUN_REPORT_INVALID_DEFAULT_TARGETS_TYPE"
    """The DEFAULT_TARGETS class attribute is not of type frozenset[Target]."""
    RUN_REPORT_INVALID_DEFAULT_TARGETS_VALUE = "RUN_REPORT_INVALID_DEFAULT_TARGETS_VALUE"
    """The DEFAULT_TARGETS class attribute contains something other than Target values."""
    RUN_REPORT_INVALID_DEFAULT_SUBDIR_TYPE = "RUN_REPORT_INVALID_DEFAULT_SUBDIR_TYPE"
    """The DEFAULT_SUBDIR class attribute is not of type str."""
    RUN_REPORT_INVALID_DEFAULT_SUBDIR_VALUE = "RUN_REPORT_INVALID_DEFAULT_SUBDIR_VALUE"
    """The DEFAULT_SUBDIR class attribute must consist only of alphanumeric characters if not empty."""
    RENDER_INVALID_CASE_ARG_TYPE = "RENDER_INVALID_CASE_ARG_TYPE"
    """The case argument passed to the render() method was not of type Case."""
    RENDER_INVALID_OPTIONS_ARG = "RENDER_INVALID_OPTIONS_ARG"
    """The options argument passed to the render() method is not of the expected type (JSONOptions or None)."""
