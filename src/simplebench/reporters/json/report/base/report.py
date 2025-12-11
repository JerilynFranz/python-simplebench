"""Abstract Base Class for JSON reports."""
from __future__ import annotations

from abc import ABC
from typing import Any, Sequence

from simplebench.exceptions import SimpleBenchValueError
from simplebench.validators import validate_sequence_of_str, validate_sequence_of_type, validate_string

from .. import results as versioned_results
from ..exceptions import _ReportErrorTag
from .json_schema import JSONSchema
from .machine_info import MachineInfo
from .results import Results

_JSON_SCHEMA_URI: str = "https://json-schema.org/draft/2020-12/schema"


class Report(ABC):
    """Abstract Base class representing a JSON report."""

    VERSION: int = 0
    """The version of the JSON report schema this class implements."""

    TYPE: str = "SimpleBenchReport::V0"
    """The type of the JSON report schema this class implements."""

    schema: type[JSONSchema] = JSONSchema
    """The JSON schema class for this report version.

    Has to be overridden in subclasses.
    """
    @classmethod
    def from_dict(cls, data: dict) -> Report:
        """Create a JSONReport instance from a dictionary.

        :param data: Dictionary containing the JSON report data.
        :return: JSONReport instance.
        :raises SimpleBenchValueError: If the version is not 1.
        """
        if not isinstance(data, dict):
            raise SimpleBenchValueError(
                "Input data must be a dictionary",
                tag=_ReportErrorTag.INVALID_INPUT_DATA_TYPE)
        if not all(isinstance(key, str) for key in data.keys()):
            raise SimpleBenchValueError(
                "All keys in input data must be strings",
                tag=_ReportErrorTag.INVALID_INPUT_DATA_KEYS_TYPE)

        cls.validate_schema_uri(data.get('$schema'))
        cls.validate_version(data.get('version'))
        cls.validate_type(data.get('type'), cls.TYPE)

        maybe_results: list[dict[str, Any]] = validate_sequence_of_type(
            data.get('results'), dict, 'results',
            _ReportErrorTag.INVALID_RESULTS_PROPERTY_NOT_A_SEQUENCE,
            _ReportErrorTag.INVALID_RESULTS_PROPERTY_ELEMENT_NOT_DICT,
            allow_empty=False)

        list_of_results: list[Results] = []
        for item in maybe_results:
            results = versioned_results.from_dict(data=item, version=cls.VERSION)
            list_of_results.append(results)

        report = cls(
            group=data.get('group'),  # type: ignore[reportArgumentType]
            title=data.get('title'),  # type: ignore[reportArgumentType]
            description=data.get('description'),  # type: ignore[reportArgumentType]
            variation_cols=data.get('variation_cols'),  # type: ignore[reportArgumentType]
            results=list_of_results)  # type: ignore[reportArgumentType]

        return report

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
                tag=_ReportErrorTag.INVALID_SCHEMA_URI_TYPE)
        if value != _JSON_SCHEMA_URI:
            raise SimpleBenchValueError(
                f"Incorrect JSONSchema $schema for JSONReport: {value} (expected {_JSON_SCHEMA_URI})",
                tag=_ReportErrorTag.INVALID_SCHEMA_URI_VALUE)

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
                tag=_ReportErrorTag.INVALID_VERSION_TYPE)
        if value != cls.VERSION:
            raise SimpleBenchValueError(
                f"Incorrect version for JSONReport: {value} (expected {cls.VERSION})",
                tag=_ReportErrorTag.INVALID_VERSION_VALUE)

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
                tag=_ReportErrorTag.INVALID_TYPE_TYPE)
        if found != expected:
            raise SimpleBenchValueError(
                f"Incorrect type for JSONReport: {found} (expected '{expected}')",
                tag=_ReportErrorTag.INVALID_TYPE_VALUE)

        return found

    def __init__(self, *,  # pylint: disable=super-init-not-called
                 group: str,
                 title: str,
                 description: str,
                 variation_cols: dict[str, str],
                 results: list[Results]) -> None:
        """Initialize a Report base instance."""
        self.group = group
        self.title = title
        self.description = description
        self.variation_cols = variation_cols
        self.results = results

    @property
    def version(self) -> int:
        """Get the version property."""
        return self._version

    @version.setter
    def version(self, value: int) -> None:
        """Set the version property.

        :param value: The version value to set.
        """
        self._version: int = self.validate_version(value)

    @property
    def type(self) -> str:
        """Get the type property."""
        return f"SimpleBenchReport::V{self.version}"

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
            _ReportErrorTag.INVALID_GROUP_PROPERTY_TYPE,
            _ReportErrorTag.EMPTY_GROUP_PROPERTY_VALUE,
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
            _ReportErrorTag.INVALID_TITLE_PROPERTY_TYPE,
            _ReportErrorTag.EMPTY_TITLE_PROPERTY_VALUE,
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
            _ReportErrorTag.INVALID_DESCRIPTION_PROPERTY_TYPE,
            _ReportErrorTag.EMPTY_DESCRIPTION_PROPERTY_VALUE,
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
                tag=_ReportErrorTag.INVALID_VARIATION_COLS_PROPERTY_TYPE)

        validate_sequence_of_str(
            value.keys(), "variation_cols keys",
            _ReportErrorTag.INVALID_VARIATION_COLS_KEYS_TYPE,
            _ReportErrorTag.INVALID_VARIATION_COLS_KEYS_VALUE,
            allow_empty=False)

        validate_sequence_of_str(
            value.values(), "variation_cols values",
            _ReportErrorTag.INVALID_VARIATION_COLS_VALUES_TYPE,
            _ReportErrorTag.INVALID_VARIATION_COLS_VALUES_VALUE,
            allow_empty=False)

        self._variation_cols: dict[str, str] = value

    @property
    def results(self) -> list[Results]:
        """Get the results property.

        The results property is a list of Results instances.
        """
        return self._results

    @results.setter
    def results(self, value: Sequence[Results]) -> None:
        """Set the results property.

        :param value: A sequence of Results values to set.
        """
        validated_results: list[Results] = validate_sequence_of_type(
            value, Results, 'results',
            _ReportErrorTag.INVALID_RESULTS_PROPERTY_NOT_A_SEQUENCE,
            _ReportErrorTag.INVALID_RESULTS_PROPERTY_ELEMENT_NOT_RESULTS_INSTANCE,
            allow_empty=False)

        self._results: list[Results] = validated_results

    @property
    def machine(self) -> MachineInfo:
        """Get the machine property."""
        return self._machine

    @machine.setter
    def machine(self, value: MachineInfo) -> None:
        """Set the machine property.

        :param value: The machine value to set.
        """
        if not isinstance(value, MachineInfo):
            raise SimpleBenchValueError(
                "machine must be a JSONMachineInfo instance",
                tag=_ReportErrorTag.INVALID_MACHINE_PROPERTY_TYPE)

        self._machine: MachineInfo = value
