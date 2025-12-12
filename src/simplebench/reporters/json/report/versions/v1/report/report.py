"""JSON Report version 1 class.

The Report class represents a version 1 JSON report.

It provides methods to convert to and from dictionary representations
and includes schema validation specific to version 1 reports.

The version 1 report is the first stable version of the JSON report format
and serves as a foundation for future versions.

As such, it largely is just a wrapper around the base Report class
with the version number set to 1, the type set to "SimpleBenchReport::V1",
and the schema set to the ReportSchema class for version 1 reports.
"""

from simplebench.reporters.json.report.base import JSONSchema
from simplebench.reporters.json.report.base import Report as BaseReport

from .report_schema import ReportSchema


class Report(BaseReport):
    """Class representing a JSON report version 1."""

    TYPE: str = "SimpleBenchReport::V1"
    """The JSON report type property value for version 1 reports."""

    VERSION: int = 1
    """The JSON report version number."""

    SCHEMA: type[JSONSchema] = ReportSchema
    """The JSON schema class for version 1 reports."""
