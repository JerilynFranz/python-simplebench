"""Data structures for logging."""
from __future__ import annotations

from abc import ABC, abstractmethod
from json import JSONEncoder
from pathlib import Path
from typing import TYPE_CHECKING, Any

from simplebench.exceptions import SimpleBenchNotImplementedError, SimpleBenchTypeError, SimpleBenchValueError
from simplebench.type_proxies import is_case, is_choice
from simplebench.utils import get_machine_info, timestamp_to_iso8601
from simplebench.validators import validate_type
from simplebench.vcs import GitInfo

from ..exceptions import _ReportLogEntryErrorTag

if TYPE_CHECKING:
    from simplebench.case import Case
    from simplebench.reporters.choice.choice import Choice


class ReportLogEntry(ABC):
    """Container for report log entry metadata.

    :ivar filepath: The path to the generated report file.
    :ivar timestamp: The timestamp of the report generation in ISO 8601 format.
    :ivar reports_log_path: The path to the reports log file.
    :ivar case: The Case instance containing benchmark results.
    :ivar choice: The Choice instance specifying the report configuration.
    """

    _JSON_SCHEMA_URI: str = "https://simplebench.dev/schemas/report_log_entry.json"
    """The JSON Schema URI for ReportLogEntry."""

    VERSION: int = 0
    """The version of the ReportLogEntry schema."""

    @classmethod
    @abstractmethod
    def from_dict(cls, data: dict) -> "ReportLogEntry":
        """Create a JSONReport instance from a dictionary.

        :param data: Dictionary containing the JSON report data.
        :return: JSONReport instance.
        """
        raise SimpleBenchNotImplementedError(
            "from_dict must be implemented in subclasses.",
            tag=_ReportLogEntryErrorTag.MISSING_FROM_DICT_IMPLEMENTATION)

    @classmethod
    def validate_schema_uri(cls, value: Any) -> str:
        """Validate the $schema URI.

        :param value: The $schema URI to validate.
        :return: The validated $schema URI string.
        :raise SimpleBenchTypeError: If the $schema URI is not a string.
        :raises SimpleBenchValueError: If the $schema URI is invalid.
        """
        if not isinstance(value, str):
            raise SimpleBenchValueError(
                f"$schema must be a string, got {type(value)}",
                tag=_ReportLogEntryErrorTag.INVALID_SCHEMA_URI_TYPE)
        if value != cls._JSON_SCHEMA_URI:
            raise SimpleBenchValueError(
                f"Incorrect JSONSchema $schema for JSONReport: {value} (expected {cls._JSON_SCHEMA_URI})",
                tag=_ReportLogEntryErrorTag.INVALID_SCHEMA_URI_VALUE)
        return value

    @classmethod
    def validate_version(cls, value: Any) -> int:
        """Validate the version.

        :param value: The version to validate.
        :return: The validated version integer.
        :raise SimpleBenchTypeError: If the version is not an integer.
        :raises SimpleBenchValueError: If the version is invalid.
        """
        if not isinstance(value, int):
            raise SimpleBenchValueError(
                f"version must be an integer, got {type(value)}",
                tag=_ReportLogEntryErrorTag.INVALID_VERSION_TYPE)
        if value != cls.VERSION:
            raise SimpleBenchValueError(
                f"Incorrect version for JSONReport: {value} (expected {cls.VERSION})",
                tag=_ReportLogEntryErrorTag.INVALID_VERSION_VALUE)

        return value

    @classmethod
    def validate_type(cls, found: Any, expected: str) -> str:
        """Validate the type.

        :param found: The type string to validate.
        :param expected: The expected type string.
        :return: The validated type string.
        :raise SimpleBenchTypeError: If the type is not a string.
        :raises SimpleBenchValueError: If the type is invalid.
        """
        if not isinstance(found, str):
            raise SimpleBenchValueError(
                f"type must be a string, got {type(found)}",
                tag=_ReportLogEntryErrorTag.INVALID_TYPE_TYPE)
        if found != expected:
            raise SimpleBenchValueError(
                f"Incorrect type for JSONReport: {found} (expected '{expected}')",
                tag=_ReportLogEntryErrorTag.INVALID_TYPE_VALUE)

        return found

    def __init__(
        self,
        *,
        reports_log_path: Path | None = None,
        filepath: Path | None = None,
        timestamp: float,
        case: Case,
        choice: Choice,
    ) -> None:
        """Initialize ReportLogMetadata.

        The timestamp is expected to be in epoch seconds (float) but will be stored
        as an ISO 8601 formatted string in UTC.

        The filepath is stored as a URI string in the :attr:`uri` property.

        :param filepath: The path to the generated report file. If None, no file path is set.
        :param timestamp: The timestamp of the report generation in epoch seconds.
        :param reports_log_path: The path to the reports log file.
        :param case: The Case instance containing benchmark results.
        :param choice: The Choice instance specifying the report configuration.
        :raises SimpleBenchTypeError: If any argument is of invalid type.
        """
        self.reports_log_path = reports_log_path
        self.filepath = filepath
        self.timestamp = timestamp
        self.case = case
        self.choice = choice

    @property
    def uri(self) -> str | None:
        """The path to the generated report as a URI string.

        The URI is relative to the directory of the reports log file if possible.

        Read only property returning the file URI string.
        """
        if self.filepath is None:
            return None
        if hasattr(self, '_reports_log_path') and self.reports_log_path is not None:
            try:
                root_path = self.reports_log_path.parent
                relative_path = self.filepath.relative_to(root_path)
                return relative_path.as_uri()
            except ValueError:
                pass  # filepath is not relative to reports_log_path parent
        return self.filepath.as_uri()

    @property
    def filepath(self) -> Path | None:
        """The path to the generated report file as a Path object."""
        return self._filepath

    @filepath.setter
    def filepath(self, value: Path | None) -> None:
        """Set the path to the generated report file.

        It is stored internally as both a URI string and a Path object.
        The URI string is available via the :attr:`uri_reference` property,
        and the Path object via the :attr:`filepath` property.

        :param value: The file Path.
        :type value: Path | None
        :raises SimpleBenchTypeError: If value is not a Path instance or None.
        """
        self._filepath: Path | None = None
        if value is not None:
            self._filepath = value

    @property
    def timestamp(self) -> str:
        """The timestamp of the report generation."""
        return self._timestamp

    @timestamp.setter
    def timestamp(self, value: float) -> None:
        """Set the timestamp of the report generation.

        :param value: The new timestamp.
        :type value: float
        :raises SimpleBenchTypeError: If value is not a float.
        """
        self._timestamp: str = timestamp_to_iso8601(value)

    @property
    def reports_log_path(self) -> Path | None:
        """The path to the reports log file."""
        return self._reports_log_path

    @reports_log_path.setter
    def reports_log_path(self, value: Path | None) -> None:
        """Set the path to the reports log file.

        :param value: The new reports log path.
        :type value: Path | None
        :raises SimpleBenchTypeError: If value is not a Path instance or None.
        """
        self._reports_log_path: Path | None = None
        if value is not None:
            self._reports_log_path = validate_type(
                value, Path, 'reports_log_path',
                _ReportLogEntryErrorTag.INVALID_REPORTS_LOG_PATH_ARG_TYPE)

    @property
    def case(self) -> Case:
        """The Case instance containing benchmark results."""
        return self._case

    @case.setter
    def case(self, value: Case) -> None:
        """Set the Case instance containing benchmark results.

        :param value: The new Case instance.
        :type value: Case
        :raises SimpleBenchTypeError: If value is not a Case instance.
        """
        if not is_case(value):
            raise SimpleBenchTypeError(
                f"Expected a Case instance for 'case', got: {type(value)}",
                tag=_ReportLogEntryErrorTag.INVALID_CASE_ARG_TYPE)
        self._case: Case = value

    @property
    def choice(self) -> Choice:
        """The Choice instance specifying the report configuration."""
        return self._choice

    @choice.setter
    def choice(self, value: Choice) -> None:
        """Set the Choice instance specifying the report configuration.

        :param value: The new Choice instance.
        :type value: Choice
        :raises SimpleBenchTypeError: If value is not a Choice instance.
        """
        if not is_choice(value):
            raise SimpleBenchTypeError(
                f"Expected a Choice instance for 'choice', got: {type(value)}",
                tag=_ReportLogEntryErrorTag.INVALID_CHOICE_ARG_TYPE)
        self._choice: Choice = value

    def save_to_log(self) -> None:
        """Append the metadata as a JSON entry to the reports log file."""
        if self.reports_log_path is None:
            raise SimpleBenchValueError(
                "Cannot save to log: 'reports_log_path' is not set.",
                tag=_ReportLogEntryErrorTag.REPORTS_LOG_PATH_NOT_SET)
        json_log_entry = self.to_json()
        reports_log_path = self.reports_log_path
        if not reports_log_path.parent.exists():
            reports_log_path.parent.mkdir(parents=True, exist_ok=True)
        with reports_log_path.open(mode='a', encoding='utf-8') as log_file:
            log_file.write(json_log_entry + '\n')

    def to_dict(self) -> dict[str, Any]:
        """Convert metadata to a dictionary for JSON serialization.

        :return: A dictionary representation of the metadata.
        :rtype: dict[str, Any]
        """
        git_info = self.case.git_info.to_dict() if isinstance(self.case.git_info, GitInfo) else None

        output = {
            "version": 1,
            "timestamp": self.timestamp,
            "benchmark_id": self.case.benchmark_id,
            "benchmark_group": self.case.group,
            "reporter_type": self.choice.reporter.__class__.__name__,
            "reporter_name": self.choice.reporter.name,
            "reporter_schema_version": self.choice.reporter.schema_version,
            "output_format": self.choice.output_format.name,
            "benchmark_title": self.case.title,
            "git": git_info,
            "machine_info": get_machine_info(),
        }
        if self.uri is not None:
            output["uri"] = self.uri
        return output

    def to_json(self) -> str:
        """Convert metadata to a one line JSON string.

        :return: A JSON string representation of the metadata.
        :rtype: str
        """
        return self._one_line_string(JSONEncoder(indent=None).encode(self.to_dict()))

    def _one_line_string(self, string: str) -> str:
        """Convert a multi-line string into a single line by replacing newlines with spaces.

        :param string: The input string.
        :type string: str
        :return: The single-line string.
        """
        return ' '.join(string.splitlines())
