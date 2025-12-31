"""Report version 1 class.

The Report class represents a version 1 report.

It provides methods to convert to and from dictionary representations
and includes schema validation specific to version 1 reports.

It's primarily used for handling benchmark reports in SimpleBench.

The to_dict and from_dict methods facilitate safe serialization and
deserialization of report data.

The version 1 report is the first stable version of the report format
and serves as a foundation for future versions.
"""
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, Sequence, cast

from simplebench.exceptions import SimpleBenchRuntimeError
from simplebench.report._error_tags import _ReportErrorTag
from simplebench.report._base import BaseReport, JSONSchema
from simplebench.types import ImmutableVariationColsType, VariationColsType
from simplebench.validators import validate_core_data_mapping, validate_sequence_of_type

from .. import MachineInfo, ResultsInfo
from ..types import ReportData, ReportDict, ResultsInfoData
from . import validate
from .report_schema import ReportSchema

if TYPE_CHECKING:
    from simplebench.case import Case


class Report(BaseReport):
    """Immutable class representing a version 1 report."""

    SCHEMA: type[JSONSchema] = ReportSchema
    """The JSON schema class for version 1 reports."""

    TYPE: str = SCHEMA.TYPE
    """The JSON report type property value for version 1 reports."""

    VERSION: int = SCHEMA.VERSION
    """The JSON report version number."""

    ID: str = SCHEMA.ID
    """The JSON report ID property value for version 1 reports."""

    def __init__(self, *,
                 timestamp: str,
                 group: str,
                 title: str,
                 description: str,
                 variation_cols: VariationColsType,
                 results: Sequence[ResultsInfo],
                 machine: MachineInfo) -> None:
        """Initialize a Report instance.
        
        :param str timestamp: ISO 8601 formatted timestamp string.
        :param str group: Group of the benchmark.
        :param str title: Title of the benchmark.
        :param str description: Description of the benchmark.
        :param VariationColsType variation_cols: Variation columns dictionary.
        :param Sequence[ResultsInfo] results: Sequence of ResultsInfo instances.
        :param MachineInfo machine: MachineInfo instance.
        :raises SimpleBenchTypeError: If any parameter is of incorrect type.
        :raises SimpleBenchValueError: If any parameter has an invalid value.
        """
        self._timestamp: str = validate.timestamp(timestamp)
        self._group: str = validate.group(group)
        self._title: str = validate.title(title)
        self._description: str = validate.description(description)
        self._variation_cols: ImmutableVariationColsType = validate.variation_cols(variation_cols)
        self._results: tuple[ResultsInfo, ...] = validate.results(results)
        self._machine: MachineInfo = validate.machine(machine)
        self._to_dict_cache: ReportDict | None = None  # Cache for to_dict output
        """Cached immutable dictionary representation of the Report instance.
        
        It is initialized to None and populated on the first call to to_dict().
        It is used to improve performance by avoiding redundant conversions 
        and it is type cast to :class:`ReportDict
        """

    @classmethod
    def from_dict(cls, data: Mapping[str, Any]) -> 'Report':
        """Create a Report instance from a dictionary.

        The input dictionary is validated against the rules for the version 1 report schema.

        :param Mapping[str, Any] data: Dictionary containing the JSON structured report data.
        :return Report: Report instance.
        :raises SimpleBenchValueError: If any field has an invalid value.
        :raises SimpleBenchTypeError: If any field is of an incorrect type.
        """
        allowed_keys = cls.init_params()

        def process_results(value: Any) -> list[ResultsInfo]:
            """Process the results-info objects in the input sequence"""
            validated_list = validate_sequence_of_type(
                value, dict, 'results',
                _ReportErrorTag.INVALID_RESULTS_PROPERTY_NOT_A_SEQUENCE,
                _ReportErrorTag.INVALID_RESULTS_PROPERTY_ELEMENT_NOT_DICT,
                allow_empty=False)
            return [ResultsInfo.from_dict(item) for item in validated_list]

        kwargs = cls.import_data(  # Hydrate instance arguments from dict
            data=data,
            allowed_fields=allowed_keys,
            skip_fields={'version', 'type'},
            optional_fields={'version', 'type'},
            defaults={'version': cls.VERSION, 'type': cls.TYPE},
            match_on={'version': cls.VERSION, 'type': cls.TYPE},
            process_as={
                'results': process_results,
                'machine': MachineInfo.from_dict
            })
        return cls(**kwargs)

    def to_dict(self) -> ReportDict:
        """Convert the JSONReport instance to a dictionary.

        The output dictionary conforms to the version 1 report schema
        and is suitable for serialization to JSON. It is immutable and cached
        for efficiency and is type cast to :class:`ReportDict`.

        :return ReportDict: Immutable dictionary containing the JSON report data.
        """
        if self._to_dict_cache is None:
            self._to_dict_cache = self._to_dict_helper(ReportDict)
        return self._to_dict_cache


    @property
    def timestamp(self) -> str:
        """Get the timestamp property.
        
        :return str: The ISO 8601 formatted timestamp string.
        """
        return self._timestamp

    @property
    def group(self) -> str:
        """Get the group property.
        
        :return str: The group string.
        """
        return self._group

    @property
    def title(self) -> str:
        """Get the title property.
        
        :return str: The title string.
        """
        return self._title

    @property
    def description(self) -> str:
        """Get the description property.
        
        :return str: The description string.
        """
        return self._description

    @property
    def variation_cols(self) -> ImmutableVariationColsType:
        """Return the variation_cols property.
        
        A copy of the variation_cols dictionary is returned to prevent
        external modification of the internal state.

        :return ImmutableVariationColsType: The variation_cols dictionary as an immutable mapping.
        """
        return self._variation_cols

    @property
    def results(self) -> tuple[ResultsInfo, ...]:
        """Get the results property.

        The results property is a tuple of ResultsInfo instances.

        :return tuple[ResultsInfo]: The results tuple.
        """
        return self._results

    @property
    def machine(self) -> MachineInfo:
        """Get the machine property."""
        return self._machine
