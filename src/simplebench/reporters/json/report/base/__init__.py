"""Base class for JSON report representation."""

from .json_metadata import JSONMetadata
from .json_report import JSONReport
from .json_report_schema import JSONReportSchema
from .json_results import JSONResults
from .json_stats import JSONStats

__all__ = [
    "JSONMetadata",
    "JSONReport",
    "JSONReportSchema",
    "JSONResults",
    "JSONStats",
]
