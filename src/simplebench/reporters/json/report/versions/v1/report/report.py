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
from typing import Any, Sequence

from simplebench.exceptions import SimpleBenchValueError
from simplebench.reporters.json.report.base import JSONSchema, MachineInfo
from simplebench.reporters.json.report.base import Report as BaseReport
from simplebench.reporters.json.report.base import ResultsInfo
from simplebench.reporters.json.report.exceptions import _ReportErrorTag
from simplebench.validators import validate_sequence_of_str, validate_sequence_of_type, validate_string

from ..machine_info import MachineInfo as MachineInfoV1
from ..results_info import ResultsInfo as ResultsV1
from .report_schema import ReportSchema


class Report(BaseReport):
    """Class representing a JSON report version 1."""

    SCHEMA: type[JSONSchema] = ReportSchema
    """The JSON schema class for version 1 reports."""

    TYPE: str = SCHEMA.TYPE
    """The JSON report type property value for version 1 reports."""

    VERSION: int = SCHEMA.VERSION
    """The JSON report version number."""

    ID: str = SCHEMA.ID
    """The JSON report ID property value for version 1 reports."""

    def __init__(self, *,
                 group: str,
                 title: str,
                 description: str,
                 variation_cols: dict[str, str],
                 results: list[ResultsInfo],
                 machine: MachineInfo) -> None:
        """Initialize a Report base instance."""
        self.group = group
        self.title = title
        self.description = description
        self.variation_cols = variation_cols
        self.results = results
        self.machine = machine

    @classmethod
    def from_dict(cls, data: dict) -> 'Report':
        """Create a Report instance from a dictionary.

        :param data: Dictionary containing the JSON report data.
        :return: Report instance.
        :raises SimpleBenchValueError: If the version is not 1.
        """
        allowed_keys = cls.init_params()
        allowed_keys['version'] = int
        allowed_keys['type'] = str

        def process_results(value: Any) -> list[ResultsInfo]:
            validated_list = validate_sequence_of_type(
                value, dict, 'results',
                _ReportErrorTag.INVALID_RESULTS_PROPERTY_NOT_A_SEQUENCE,
                _ReportErrorTag.INVALID_RESULTS_PROPERTY_ELEMENT_NOT_DICT,
                allow_empty=False)
            return [ResultsV1.from_dict(item) for item in validated_list]

        kwargs = cls.import_data(
            data=data,
            allowed=allowed_keys,
            skip={'version', 'type'},
            optional={'version', 'type'},
            default={'version': cls.VERSION, 'type': cls.TYPE},
            match_on={'version': cls.VERSION, 'type': cls.TYPE},
            process_as={
                'results': process_results,
                'machine': MachineInfoV1.from_dict
            })
        return cls(**kwargs)

    def to_dict(self) -> dict[str, Any]:
        """Convert the JSONReport instance to a dictionary.

        :return: Dictionary containing the JSON report data.
        """
        data: dict[str, Any] = {}
        for key in self.init_params():
            value = getattr(self, key)
            if key == 'machine':
                data[key] = value.to_dict()
            elif key == 'results':
                data[key] = [result.to_dict() for result in value]
            else:
                data[key] = value

        data['type'] = self.TYPE
        data['version'] = self.VERSION
        return data

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
    def results(self) -> list[ResultsInfo]:
        """Get the results property.

        The results property is a list of Results instances.
        """
        return self._results

    @results.setter
    def results(self, value: Sequence[ResultsInfo]) -> None:
        """Set the results property.

        :param value: A sequence of Results values to set.
        """
        validated_results: list[ResultsInfo] = validate_sequence_of_type(
            value, ResultsInfo, 'results',
            _ReportErrorTag.INVALID_RESULTS_PROPERTY_NOT_A_SEQUENCE,
            _ReportErrorTag.INVALID_RESULTS_PROPERTY_ELEMENT_NOT_RESULTS_INSTANCE,
            allow_empty=False)

        self._results: list[ResultsInfo] = validated_results

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
