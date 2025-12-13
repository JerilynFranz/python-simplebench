"""V1 StatsBlock class

This class represents a stats block information in a JSON report.

It implements validation and serialization/deserialization methods to and from dictionaries
for the following JSON Schema version:

https://raw.githubusercontent.com/JerilynFranz/python-simplebench/main/schemas/v1/stats-block.json

It is the base implemention of the JSON report stats block representation.

This makes the implementations of StatsBlock backwards compatible with future versions
of the JSON report schema and the V1 implementation itself is essentially a frozen snapshot
of the base CPUInfo representation at the time of the V1 schema release.

"""
from typing import Any, Sequence

from simplebench.exceptions import SimpleBenchValueError
from simplebench.reporters.json.report.base import JSONSchema
from simplebench.reporters.json.report.base import StatsBlock as BaseStatsBlock
from simplebench.reporters.json.report.exceptions.stats_block import _StatsBlockErrorTag
from simplebench.validators import (
    validate_float,
    validate_namespaced_identifier,
    validate_positive_float,
    validate_positive_int,
    validate_sequence_of_type,
    validate_string,
)

from .stats_block_schema import StatsBlockSchema


class StatsBlock(BaseStatsBlock):
    """Class representing JSON stats summary for V1 reports."""
    SCHEMA: type[JSONSchema] = StatsBlockSchema
    """The JSON schema class for the stats summary block in version 1 reports."""

    TYPE: str = SCHEMA.TYPE
    """The JSON report type property value for version 1 reports."""

    VERSION: int = SCHEMA.VERSION
    """The JSON report version number."""

    ID: str = SCHEMA.ID
    """The JSON report ID property value for version 1 reports."""

    def __init__(self, *,
                 name: str,
                 description: str,
                 semantic_type: str,
                 unit: str,
                 scale: float,
                 iterations: int,
                 rounds: int,
                 mean: float,
                 median: float,
                 minimum: float,
                 maximum: float,
                 standard_deviation: float,
                 relative_standard_deviation: float,
                 percentiles: Sequence[float]) -> None:
        """Initialize a StatsBlock object with the given parameters.

        The parameters are validated to ensure they meet the required types and constraints
        and match the contract of the JSON schema for the version 1 report.

        :param name: The name of the stats block.
        :param description: The description of the stats block.
        :param semantic_type: The semantic type of the stats block.
        :param unit: The unit of measurement for the stats block.
        :param scale: The scale factor for the stats block.
        :param iterations: The number of iterations in the stats block.
        :param rounds: The number of rounds in the stats block.
        :param mean: The mean value of the stats block.
        :param median: The median value of the stats block.
        :param minimum: The minimum value of the stats block.
        :param maximum: The maximum value of the stats block.
        :param standard_deviation: The standard deviation of the stats block.
        :param relative_standard_deviation: The relative standard deviation of the stats block.
        :param percentiles: The list of percentiles for the stats block.
        :raise SimpleBenchTypeError: If any parameter is of an invalid type.
        :raise SimpleBenchValueError: If any parameter has an invalid value.
        """
        self.name = name
        self.description = description
        self.semantic_type = semantic_type
        self.unit = unit
        self.scale = scale
        self.iterations = iterations
        self.rounds = rounds
        self.mean = mean
        self.median = median
        self.minimum = minimum
        self.maximum = maximum
        self.standard_deviation = standard_deviation
        self.relative_standard_deviation = relative_standard_deviation
        self.percentiles = percentiles

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "StatsBlock":
        """Create a StatsBlock object from a dictionary."""
        allowed_keys = cls.init_params()
        allowed_keys['version'] = int
        allowed_keys['type'] = str

        kwargs = cls.import_data(
            data=data,
            allowed=allowed_keys,
            skip={'version', 'type'},
            optional={'description', 'version', 'type'},
            default={'description': '', 'version': cls.VERSION, 'type': cls.TYPE},
            match_on={'version': cls.VERSION, 'type': cls.TYPE})
        return cls(**kwargs)

    def to_dict(self) -> dict[str, Any]:
        """Convert the StatsBlock object to a dictionary."""
        property_keys = self.init_params().keys()
        data = {key: getattr(self, key) for key in property_keys}
        data['type'] = self.TYPE
        data['version'] = self.VERSION

        return data

    @property
    def name(self) -> str:
        """Get the name of the stats block.

        :return: The name of the stats block.
        """
        return self._name

    @name.setter
    def name(self, value: str) -> None:
        """Set the name of the stats block.

        :param value: The name of the stats block.
        :raise SimpleBenchTypeError: If name is not a string.
        :raise SimpleBenchValueError: If name is an empty string.
        """
        self._name: str = validate_string(
            value, 'name',
            _StatsBlockErrorTag.INVALID_NAME_TYPE,
            _StatsBlockErrorTag.INVALID_NAME_VALUE,
            allow_blank=False)

    @property
    def description(self) -> str:
        """Get the description of the stats block.

        :return: The description of the stats block.
        """
        return self._description

    @description.setter
    def description(self, value: str) -> None:
        """Set the description of the stats block.

        :param value: The description of the stats block.
        :raise SimpleBenchTypeError: If description is not a string.
        """
        self._description: str = validate_string(
            value, 'description',
            _StatsBlockErrorTag.INVALID_DESCRIPTION_TYPE,
            _StatsBlockErrorTag.INVALID_DESCRIPTION_VALUE,
            allow_blank=True, strip=True)

    @property
    def semantic_type(self) -> str:
        """Get the semantic type of the stats block.

        The semantic type is a namespaced identifier that describes the type of
        the data being measured (e.g., "time/seconds", "memory/bytes").

        Example:

            simplebench_std::time_per_operation

        It must be a valid namespaced identifier, which means it must be a non-empty string
        that conforms to the namespaced identifier pattern:

            <namespace>::<identifier>

        where <namespace> and <identifier> are non-empty strings that match
        the following regular expression pattern:

            [A-Za-z0-9](?:[_A-Za-z0-9]*[A-Za-z0-9])?

        In this means that the namespace and identifier must be non-empty strings
        that start and end with a letter or digit, and may contain underscores and digits
        in between, but not start or end with an underscore.

        The namespace and identifier must be separated by a double colon ("::").

        :return: The semantic type of the stats block.
        """
        return self._semantic_type

    @semantic_type.setter
    def semantic_type(self, value: str) -> None:
        """Set the semantic type of the stats block.

        :param value: The semantic type of the stats block.
        :raise SimpleBenchTypeError: If semantic_type is not a string.
        :raise SimpleBenchValueError: If semantic_type is not a valid namespaced identifier.
        """
        self._semantic_type = validate_namespaced_identifier(value)

    @property
    def unit(self) -> str:
        """Get the unit of measurement.

        :return: The unit of measurement.
        """
        return self._unit

    @unit.setter
    def unit(self, value: str) -> None:
        """Set the unit of measurement.

        :param value: The unit of measurement.
        :raise SimpleBenchTypeError: If unit is not a string.
        :raise SimpleBenchValueError: If unit is an empty string.
        """
        self._unit: str = validate_string(
            value, 'unit',
            _StatsBlockErrorTag.INVALID_UNIT_TYPE,
            _StatsBlockErrorTag.INVALID_UNIT_VALUE,
            allow_blank=False)

    @property
    def scale(self) -> float:
        """Get the scale factor.

        :return: The scale factor.
        :raise SimpleBenchTypeError: If scale is not a float.
        """
        return self._scale

    @scale.setter
    def scale(self, value: float) -> None:
        """Set the scale factor.

        :param value: The scale factor.
        :raise SimpleBenchTypeError: If scale is not a float.
        :raise SimpleBenchValueError: If scale is not a positive number.
        """
        self._scale: float = validate_positive_float(
            value, 'scale',
            _StatsBlockErrorTag.INVALID_SCALE_TYPE,
            _StatsBlockErrorTag.INVALID_SCALE_VALUE)

    @property
    def iterations(self) -> int:
        """Get the number of iterations.

        :return: The number of iterations.
        """
        return self._iterations

    @iterations.setter
    def iterations(self, value: int) -> None:
        """Set the number of iterations.

        :param value: The number of iterations.
        :raise SimpleBenchTypeError: If iterations is not an integer.
        :raise SimpleBenchValueError: If iterations is not a positive integer.
        """
        self._iterations = validate_positive_int(
            value, "iterations",
            _StatsBlockErrorTag.INVALID_ITERATIONS_TYPE,
            _StatsBlockErrorTag.INVALID_ITERATIONS_VALUE)

    @property
    def rounds(self) -> int:
        """Get the number of rounds.

        :return: The number of rounds.
        """
        return self._rounds

    @rounds.setter
    def rounds(self, value: int) -> None:
        """Set the number of rounds.

        :param value: The number of rounds.
        :raise SimpleBenchTypeError: If rounds is not an integer.
        :raise SimpleBenchValueError: If rounds is not a positive integer.
        """
        self._rounds = validate_positive_int(
            value, "rounds",
            _StatsBlockErrorTag.INVALID_ROUNDS_TYPE,
            _StatsBlockErrorTag.INVALID_ROUNDS_VALUE)

    @property
    def mean(self) -> float:
        """Get the mean value.

        :return: The mean value.
        """
        return self._mean

    @mean.setter
    def mean(self, value: float) -> None:
        """Set the mean value.

        :param value: The mean value.
        :raise SimpleBenchTypeError: If mean is not a float.
        """
        self._mean: float = validate_float(
            value, 'mean',
            _StatsBlockErrorTag.INVALID_MEAN_TYPE)

    @property
    def median(self) -> float:
        """Get the median value.

        :return: The median value.
        """
        return self._median

    @median.setter
    def median(self, value: float) -> None:
        """Set the median value.

        :param value: The median value.
        :raise SimpleBenchTypeError: If median is not a float.
        """
        self._median: float = validate_float(
            value, 'median',
            _StatsBlockErrorTag.INVALID_MEDIAN_TYPE)

    @property
    def minimum(self) -> float:
        """Get the minimum value.

        :return: The minimum value.
        """
        return self._minimum

    @minimum.setter
    def minimum(self, value: float) -> None:
        """Set the minimum value.

        :param value: The minimum value.
        :raise SimpleBenchTypeError: If minimum is not a float.
        """
        self._minimum: float = validate_float(
            value, 'minimum',
            _StatsBlockErrorTag.INVALID_MINIMUM_TYPE)

    @property
    def maximum(self) -> float:
        """Get the maximum value.

        :return: The maximum value.
        """
        return self._maximum

    @maximum.setter
    def maximum(self, value: float) -> None:
        """Set the maximum value.

        :param value: The maximum value.
        :raise SimpleBenchTypeError: If maximum is not a float.
        """
        self._maximum: float = validate_float(
            value, 'maximum',
            _StatsBlockErrorTag.INVALID_MAXIMUM_TYPE)

    @property
    def standard_deviation(self) -> float:
        """Get the standard deviation.

        :return: The standard deviation.
        """
        return self._standard_deviation

    @standard_deviation.setter
    def standard_deviation(self, value: float) -> None:
        """Set the standard deviation.

        :param value: The standard deviation.
        :raise SimpleBenchTypeError: If standard_deviation is not a float.
        """
        self._standard_deviation: float = validate_float(
            value, 'standard_deviation',
            _StatsBlockErrorTag.INVALID_STANDARD_DEVIATION_TYPE)

    @property
    def relative_standard_deviation(self) -> float:
        """Get the relative standard deviation.

        :return: The relative standard deviation.
        """
        return self._relative_standard_deviation

    @relative_standard_deviation.setter
    def relative_standard_deviation(self, value: float) -> None:
        """Set the relative standard deviation.

        :param value: The relative standard deviation.
        :raise SimpleBenchTypeError: If relative_standard_deviation is not a float.
        """
        self._relative_standard_deviation: float = validate_float(
            value, 'relative_standard_deviation',
            _StatsBlockErrorTag.INVALID_RELATIVE_STANDARD_DEVIATION_TYPE)

    @property
    def percentiles(self) -> list[float]:
        """Get the list of percentiles.

        The list consists of 101 float values representing the percentiles
        from 0 to 100.

        :return: The list of percentiles.
        """
        return self._percentiles

    @percentiles.setter
    def percentiles(self, value: Sequence[float | int]) -> None:
        """Set the list of percentiles.

        :param value: The list of percentiles.
        :raise SimpleBenchTypeError: If percentiles is not a sequence of float or int.
        :raise SimpleBenchValueError: If the sequence does not contain exactly 101 numbers.
        """
        validated_sequence = validate_sequence_of_type(
            value, (float, int), "percentiles",
            _StatsBlockErrorTag.INVALID_PERCENTILES_TYPE,
            _StatsBlockErrorTag.INVALID_PERCENTILES_CONTENT_TYPE,
            allow_empty=False
        )

        if len(validated_sequence) != 101:
            raise SimpleBenchValueError(
                "percentiles must be a sequence of 101 numbers",
                tag=_StatsBlockErrorTag.INVALID_PERCENTILES_LENGTH)

        self._percentiles: list[float] = [float(v) for v in validated_sequence]
