"""Class for reading log files."""

from json import JSONDecoder, JSONDecodeError
from pathlib import Path
from typing import TYPE_CHECKING

from simplebench.exceptions import (
    SimpleBenchFileNotFoundError,
    SimpleBenchOSError,
    SimpleBenchPermissionError,
    SimpleBenchTypeError,
)

from .exceptions import _ReportLogMetadataErrorTag

if TYPE_CHECKING:
    from io import TextIOWrapper


class LogReader:
    """Class for reading log files."""

    def __init__(self, log_path: Path) -> None:
        """Initialize the LogReader with the path to the log file.

        :param log_path: The path to the log file.
        """
        self.log_path = log_path

    @property
    def log_path(self) -> Path:
        """Get the path to the log file."""
        return self._log_path

    @log_path.setter
    def log_path(self, value: Path) -> None:
        """Set the path to the log file.

        :param value: The Path pointing to the log file.
        :raises SimpleBenchTypeError: If the value is not a Path instance.
        """
        if not isinstance(value, Path):
            raise SimpleBenchTypeError(
                f"Expected log_path to be a Path instance, got {type(value)}",
                tag=_ReportLogMetadataErrorTag.INVALID_LOG_PATH_TYPE)
        self._log_path: Path = value

    def read(self) -> None:
        """Read the contents of the log file."""
        if not self.log_path.exists():
            raise SimpleBenchFileNotFoundError(
                f"Log file not found: {self.log_path}",
                tag=_ReportLogMetadataErrorTag.LOG_FILE_NOT_FOUND)
        if not self.log_path.is_file():
            raise SimpleBenchFileNotFoundError(
                f"Log path is not a file: {self.log_path}",
                tag=_ReportLogMetadataErrorTag.LOG_NOT_A_FILE)
        try:
            with self.log_path.open('r') as file:
                self._import_log_entries(file)
        except PermissionError as e:
            raise SimpleBenchPermissionError(
                f"Permission denied when trying to read log file: {self.log_path}",
                tag=_ReportLogMetadataErrorTag.LOG_PERMISSION_DENIED
            ) from e
        except OSError as e:
            raise SimpleBenchOSError(
                f"OS error occurred when trying to read log file: {self.log_path}",
                tag=_ReportLogMetadataErrorTag.LOG_OS_ERROR
            ) from e

    def _import_log_entries(self, file: TextIOWrapper) -> None:
        """Import log entries from the opened log file.

        :param file: The opened log file.
        """
        if not isinstance(file, TextIOWrapper):
            raise SimpleBenchTypeError(
                f"Expected file to be a TextIOWrapper instance, got {type(file)}",
                tag=_ReportLogMetadataErrorTag.INVALID_LOG_FILE_OBJ_TYPE)
        for line in file:
            try:
                log_entry = JSONDecoder().decode(line)
            except JSONDecodeError:
                # Handle JSON decode error if necessary
                continue
