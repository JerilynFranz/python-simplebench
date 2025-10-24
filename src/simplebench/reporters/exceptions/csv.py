"""ErrorTags for the simplebench.reporters.csv module."""
from simplebench.exceptions import ErrorTag
from simplebench.enums import enum_docstrings


@enum_docstrings
class CSVReporterErrorTag(ErrorTag):
    """Error tags for the CSV reporter module."""
    RUN_REPORT_UNSUPPORTED_TARGET = "RUN_REPORT_UNSUPPORTED_TARGET"
    """An unsupported Target was passed to the CSVReporter.run_report() method in the choice.targets"""
