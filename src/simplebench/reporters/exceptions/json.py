"""ErrorTags for the simplebench.reporters.json module."""
from simplebench.exceptions import ErrorTag
from simplebench.enums import enum_docstrings


@enum_docstrings
class JSONReporterErrorTag(ErrorTag):
    """ErrorTags for the JSONReporter class."""
    RUN_REPORT_UNSUPPORTED_TARGET = "RUN_REPORT_UNSUPPORTED_TARGET"
    """An unsupported Target was passed to the reporter's run_report() method"""
    JSON_OUTPUT_ERROR = "JSON_OUTPUT_ERROR"
    """An error occurred while serializing the JSON output."""
