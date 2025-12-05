"""Reads JSON reporter output files."""
import json
from pathlib import Path
from typing import Any

from simplebench.exceptions import (
    SimpleBenchFileNotFoundError,
    SimpleBenchJSONDecodeError,
    SimpleBenchNotAFileError,
    SimpleBenchTypeError,
    SimpleBenchValueError,
)

from .exceptions import _JSONReaderErrorTag


class JSONReportReader:
    """Reader for JSON reporter output files."""

    def __init__(self, filepath: Path) -> None:
        if not isinstance(filepath, Path):
            raise SimpleBenchTypeError(
                f'filepath must be a Path object, got {type(filepath)}',
                tag=_JSONReaderErrorTag.INVALID_FILEPATH_PROPERTY_TYPE)
        self.filepath = filepath
        self._dictionary: dict[str, Any]
        self._report: JSONReport

    @property
    def filepath(self) -> Path:
        """Path to the JSON reporter output file."""
        return self._filepath

    @filepath.setter
    def filepath(self, value: Path) -> None:
        if not isinstance(value, Path):
            raise SimpleBenchTypeError(
                f'filepath must be a Path object, got {type(value)}',
                tag=_JSONReaderErrorTag.INVALID_FILEPATH_PROPERTY_TYPE)
        self._filepath = value

    @property
    def dictionary(self) -> dict[str, Any]:
        """Contents of the JSON reporter output file as a dictionary.

        It is lazily loaded from the file on first access.
        """
        if not hasattr(self, '_dictionary'):
            self._dictionary = self._import_as_dict()
        return self._dictionary

    @property
    def report(self) -> JSONReport:
        """Contents of the JSON reporter output file as a JSONReport object."""
        if not hasattr(self, '_report'):
            self._report = self._import_as_report()
        return self._report

    def _import_as_dict(self) -> dict[str, Any]:
        """Read a JSON reporter output file and return its contents as a dictionary.

        :return: Contents of the JSON reporter output file as a dictionary.
        """
        filepath = self.filepath
        if not filepath.exists():
            raise SimpleBenchFileNotFoundError(
                f'File not found: {filepath}',
                tag=_JSONReaderErrorTag.FILE_NOT_FOUND)
        if not filepath.is_file():
            raise SimpleBenchNotAFileError(
                f'Path is not a file: {filepath}',
                tag=_JSONReaderErrorTag.NOT_A_FILE)

        output: dict[str, Any] = {}
        try:
            with filepath.open("r", encoding="utf-8") as file:
                output = json.load(file)
        except json.JSONDecodeError as exc:
            raise SimpleBenchJSONDecodeError(
                f'Error decoding JSON from file {filepath}: {exc}',
                tag=_JSONReaderErrorTag.JSON_DECODE_ERROR) from exc

        return output

    def _import_as_report(self) -> JSONReport:
        """Read a JSON reporter output file and return its contents as a Report object.

        :return: Contents of the JSON reporter output file as a Report object.
        """
        dictionary = self.dictionary
        try:
            report = JSONReport.from_dict(dictionary)
        except SimpleBenchValueError as exc:
            raise SimpleBenchValueError(
                f'Error creating JSONReport from dictionary: {exc}',
                tag=_JSONReaderErrorTag.SCHEMA_VALIDATION_ERROR) from exc
        return report
