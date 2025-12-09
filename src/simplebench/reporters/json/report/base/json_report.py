"""Abstract Base Class for JSON reports."""
from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Any, Sequence

from simplebench.exceptions import SimpleBenchNotImplementedError, SimpleBenchValueError
from simplebench.validators import validate_sequence_of_str, validate_sequence_of_type, validate_string

from .. import results
from ..exceptions import _JSONReportErrorTag

if TYPE_CHECKING:
    from .json_results import JSONResults

_JSON_SCHEMA_URI: str = "https://json-schema.org/draft/2020-12/schema"
_VERSION: int = 0


class JSONReport(ABC):
    """Abstract Base class representing a JSON report."""

    @classmethod
    @abstractmethod
    def from_dict(cls, data: dict) -> JSONReport:
        """Create a JSONReport instance from a dictionary.

        :param data: Dictionary containing the JSON report data.
        :return: JSONReport instance.
        """
        raise SimpleBenchNotImplementedError(
            "from_dict must be implemented in subclasses.",
            tag=_JSONReportErrorTag.MISSING_FROM_DICT_IMPLEMENTATION)

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
                tag=_JSONReportErrorTag.INVALID_SCHEMA_URI_TYPE)
        if value != _JSON_SCHEMA_URI:
            raise SimpleBenchValueError(
                f"Incorrect JSONSchema $schema for JSONReport: {value} (expected {_JSON_SCHEMA_URI})",
                tag=_JSONReportErrorTag.INVALID_SCHEMA_URI_VALUE)

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
                tag=_JSONReportErrorTag.INVALID_VERSION_TYPE)
        if value != _VERSION:
            raise SimpleBenchValueError(
                f"Incorrect version for JSONReport: {value} (expected {_VERSION})",
                tag=_JSONReportErrorTag.INVALID_VERSION_VALUE)

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
                tag=_JSONReportErrorTag.INVALID_TYPE_TYPE)
        if found != expected:
            raise SimpleBenchValueError(
                f"Incorrect type for JSONReport: {found} (expected '{expected}')",
                tag=_JSONReportErrorTag.INVALID_TYPE_VALUE)

        return found

    def __init__(self) -> None:
        """Initialize a JSONReport instance."""
        raise SimpleBenchNotImplementedError(
            "JSONReport cannot be instantiated directly. Subclasses must implement __init__.",
            tag=_JSONReportErrorTag.MISSING_INIT_IMPLEMENTATION)

    @property
    def group(self) -> str:
        """Get the group property."""
        return self._group

    @group.setter
    def group(self, value: str) -> None:
        """Set the group property.

        :param value: The group value to set.
        """
        self._group: str = validate_string(
            value, "group",
            _JSONReportErrorTag.INVALID_GROUP_PROPERTY_TYPE,
            _JSONReportErrorTag.EMPTY_GROUP_PROPERTY_VALUE,
            allow_empty=False)

    @property
    def title(self) -> str:
        """Get the title property."""
        return self._title

    @title.setter
    def title(self, value: str) -> None:
        """Set the title property.

        :param value: The title value to set.
        """
        self._title: str = validate_string(
            value, "title",
            _JSONReportErrorTag.INVALID_TITLE_PROPERTY_TYPE,
            _JSONReportErrorTag.EMPTY_TITLE_PROPERTY_VALUE,
            allow_empty=False)

    @property
    def description(self) -> str:
        """Get the description property."""
        return self._description

    @description.setter
    def description(self, value: str) -> None:
        """Set the description property.

        :param value: The description value to set.
        """
        self._description: str = validate_string(
            value, "description",
            _JSONReportErrorTag.INVALID_DESCRIPTION_PROPERTY_TYPE,
            _JSONReportErrorTag.EMPTY_DESCRIPTION_PROPERTY_VALUE,
            allow_empty=False)

    @property
    def variation_cols(self) -> dict[str, str]:
        """Get the variation_cols property."""
        return self._variation_cols

    @variation_cols.setter
    def variation_cols(self, value: dict[str, str]) -> None:
        """Set the variation_cols property.

        :param value: The variation_cols value to set.
        """
        if not isinstance(value, dict):
            raise SimpleBenchValueError(
                "variation_cols must be a dictionary",
                tag=_JSONReportErrorTag.INVALID_VARIATION_COLS_PROPERTY_TYPE)

        validate_sequence_of_str(
            value.keys(), "variation_cols keys",
            _JSONReportErrorTag.INVALID_VARIATION_COLS_KEYS_TYPE,
            _JSONReportErrorTag.INVALID_VARIATION_COLS_KEYS_VALUE,
            allow_empty=False)

        validate_sequence_of_str(
            value.values(), "variation_cols values",
            _JSONReportErrorTag.INVALID_VARIATION_COLS_VALUES_TYPE,
            _JSONReportErrorTag.INVALID_VARIATION_COLS_VALUES_VALUE,
            allow_empty=False)

        self._variation_cols: dict[str, str] = value

    @property
    def results(self) -> list[JSONResults]:
        """Get the results property."""
        return self._results

    @results.setter
    def results(self, value: Sequence[dict[str, Any]]) -> None:
        """Set the results property.

        :param value: The results value to set.
        """
        maybe_results: list[dict[str, Any]] = validate_sequence_of_type(
            value, dict, 'results',
            _JSONReportErrorTag.INVALID_RESULTS_PROPERTY_NOT_A_SEQUENCE,
            _JSONReportErrorTag.INVALID_RESULTS_PROPERTY_ELEMENT_NOT_A_DICT,
            allow_empty=False)

        list_of_results: list[JSONResults] = []
        for item in maybe_results:
            list_of_results.append(results.from_dict(data=item, version=_VERSION))
        self._results: list[JSONResults] = list_of_results
