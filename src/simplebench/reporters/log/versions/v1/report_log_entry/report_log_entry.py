"""JSON Report Log Entry Version 1"""
from simplebench.exceptions import SimpleBenchTypeError
from simplebench.reporters.log.base import ReportLogEntry as BaseReportLogEntry

from .exceptions import _ReportLogEntryErrorTag


class ReportLogEntry(BaseReportLogEntry):
    """JSON Report Log Entry Version 1."""

    JSON_SCHEMA_URI: str = "https://json-schema.org/draft/2020-12/schema"
    """The JSON Schema version for defining report log entry json data validation."""
    VERSION: int = 1
    """The JSON report log entry schema version number."""

    @classmethod
    def from_dict(cls, data: dict) -> "ReportLogEntry":
        """Create a ReportLogEntry instance from a dictionary.

        :param data: Dictionary containing the report log entry data.
        :return: ReportLogEntry instance.
        :raises SimpleBenchTypeError: If the input data is not a dictionary or keys are not strings.
        """
        if not isinstance(data, dict):
            raise SimpleBenchTypeError(
                "Input data must be a dictionary",
                tag=_ReportLogEntryErrorTag.INVALID_INPUT_DATA_TYPE)
        if not all(isinstance(key, str) for key in data.keys()):
            raise SimpleBenchTypeError(
                "All keys in input data must be strings",
                tag=_ReportLogEntryErrorTag.INVALID_INPUT_DATA_KEYS_TYPE)
        BaseReportLogEntry.validate_schema_uri(data.get('$schema'))
        BaseReportLogEntry.validate_version(data.get('version'))
        BaseReportLogEntry.validate_type(data.get('type'), 'ReportLogEntry')
        file_uri = data.get('uri')

        report = cls(
            filepath=data.get('filepath'),
            timestamp=data.get('timestamp'),
        )
        return report
