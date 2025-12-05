"""Data structures for logging."""
from __future__ import annotations

from json import JSONEncoder
from pathlib import Path
from typing import TYPE_CHECKING, Any

from simplebench.exceptions import SimpleBenchTypeError, SimpleBenchValueError
from simplebench.type_proxies import is_case, is_choice
from simplebench.utils import get_machine_info
from simplebench.validators import validate_float, validate_type
from simplebench.vcs import GitInfo

from .exceptions import _ReportLogMetadataErrorTag

if TYPE_CHECKING:
    from simplebench.case import Case
    from simplebench.reporters.choice.choice import Choice


class ReportLogMetadata:
    """Container for report log entry metadata.

    :ivar filepath: The path to the generated report file.
    :ivar timestamp: The timestamp of the report generation.
    :ivar reports_log_path: The path to the reports log file.
    :ivar case: The Case instance containing benchmark results.
    :ivar choice: The Choice instance specifying the report configuration.
    """
    def __init__(
        self,
        *,
        filepath: Path | None = None,
        timestamp: float,
        reports_log_path: Path | None = None,
        case: Case,
        choice: Choice,
    ) -> None:
        """Initialize ReportLogMetadata.

        :param filepath: The path to the generated report file. If None, no file path is set.
        :param timestamp: The timestamp of the report generation.
        :param reports_log_path: The path to the reports log file.
        :param case: The Case instance containing benchmark results.
        :param choice: The Choice instance specifying the report configuration.
        :raises SimpleBenchTypeError: If any argument is of invalid type.
        """
        self._filepath: Path | None = None
        self.filepath = filepath

        self._timestamp: float = None  # type: ignore[assignment]
        self.timestamp = timestamp

        self._reports_log_path: Path | None = None
        self.reports_log_path = reports_log_path

        self._case: Case = None  # type: ignore[assignment]
        self.case = case

        self._choice: Choice = None  # type: ignore[assignment]
        self.choice = choice

    @property
    def filepath(self) -> Path | None:
        """The path to the generated report file."""
        return self._filepath

    @filepath.setter
    def filepath(self, value: Path | None) -> None:
        """Set the path to the generated report file.

        :param value: The new filepath.
        :type value: Path | None
        :raises SimpleBenchTypeError: If value is not a Path instance or None.
        """
        if value is None:
            self._filepath = None
        else:
            self._filepath = validate_type(
                value, Path, 'filepath',
                _ReportLogMetadataErrorTag.INVALID_FILEPATH_ARG_TYPE,)

    @property
    def timestamp(self) -> float:
        """The timestamp of the report generation."""
        return self._timestamp

    @timestamp.setter
    def timestamp(self, value: float) -> None:
        """Set the timestamp of the report generation.

        :param value: The new timestamp.
        :type value: float
        :raises SimpleBenchTypeError: If value is not a float.
        """
        self._timestamp = validate_float(
            value, 'timestamp',
            _ReportLogMetadataErrorTag.INVALID_TIMESTAMP_ARG_TYPE)

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
        if value is None:
            self._reports_log_path = None
        else:
            self._reports_log_path = validate_type(
                value, Path, 'reports_log_path',
                _ReportLogMetadataErrorTag.INVALID_REPORTS_LOG_PATH_ARG_TYPE)

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
        if is_case(value):
            self._case = value
        else:
            raise SimpleBenchTypeError(
                f"Expected a Case instance for 'case', got: {type(value)}",
                tag=_ReportLogMetadataErrorTag.INVALID_CASE_ARG_TYPE)

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
        if is_choice(value):
            self._choice = value
        else:
            raise SimpleBenchTypeError(
                f"Expected a Choice instance for 'choice', got: {type(value)}",
                tag=_ReportLogMetadataErrorTag.INVALID_CHOICE_ARG_TYPE)

    def save_to_log(self) -> None:
        """Append the metadata as a JSON entry to the reports log file."""
        if self.reports_log_path is None:
            raise SimpleBenchValueError(
                "Cannot save to log: 'reports_log_path' is not set.",
                tag=_ReportLogMetadataErrorTag.REPORTS_LOG_PATH_NOT_SET)
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

        return {
            "version": 1,
            "timestamp": self.timestamp,
            "benchmark_id": self.case.benchmark_id,
            "benchmark_group": self.case.group,
            "reporter_type": self.choice.reporter.__class__.__name__,
            "reporter_name": self.choice.reporter.name,
            "reporter_schema_version": self.choice.reporter.schema_version,
            "output_format": self.choice.output_format.name,
            "benchmark_title": self.case.title,
            "filepath": self.filepath.as_posix() if self.filepath else None,
            "git": git_info,
            "machine_info": get_machine_info(),
        }

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
