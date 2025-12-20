"""V1 StatsBlock class

This class represents a stats block information in a JSON report.

It implements validation and serialization/deserialization methods to and from dictionaries
for the following JSON Schema version:

https://raw.githubusercontent.com/JerilynFranz/python-simplebench/main/schemas/v1/stats-block.json

It is the base implemention of the JSON report stats block representation.

This makes the implementations of StatsBlock backwards compatible with future versions
of the JSON report schema and the V1 implementation itself is essentially a frozen snapshot
of the base CPUInfo representation at the time of the V1 schema release.

The code has three basic paths for creating a stats block:

1. Creation by directly instantiating the `StatsBlock` class with the required statistical parameters.
2. Creation by instantiating the `StatsBlock` class with the raw data measurements and
   having the class calculate the statistical parameters.
3. Creation by using the `from_dict` class method to create a `StatsBlock` instance from a
   dictionary that matches the JSON schema.

The created instance and all values available via properties are immutable once created
and can be serialized back to a dictionary using the `to_dict` method.

The class also implements equality and hashing methods to allow comparison
and use in hash-based collections like sets and dictionaries. It also
implements size-optimized pickling support for serialization/deserialization.

The dictionary serialized representation matches the JSON schema for version 1 reports
and can be used for JSON serialization and deserialization.
"""
import statistics
from copy import copy
from math import sqrt
from typing import Any, Sequence, overload

from simplebench.decorators import immutable
from simplebench.exceptions import SimpleBenchValueError
from simplebench.report._error_tags import _StatsBlockErrorTag
from simplebench.report.base import JSONSchema
from simplebench.report.base import StatsBlock as BaseStatsBlock
from simplebench.types.values import Values

from . import validate
from .stats_block_schema import StatsBlockSchema


class StatsBlock(BaseStatsBlock):
    """Class representing JSON stats summary for V1 reports.

    This class represents a stats block information in a JSON report.
    It implements validation and serialization/deserialization methods to and from dictionaries
    for the following JSON Schema version:

    https://raw.githubusercontent.com/JerilynFranz/python-simplebench/main/schemas/v1/stats-block.json

    :param name: The name of the stats block.
    :param description: The description of the stats block.
    :param semantic_type: The semantic type of the stats block.
    :param unit: The unit of measurement for the stats block.
    :param scale: The scale factor for the stats block.
    :param iterations: The number of iterations measured for the stats block.
    :param rounds: The number of rounds in each iteration measured.
    :param mean: The mean value of the stats block.
    :param median: The median value of the stats block.
    :param minimum: The minimum value of the stats block.
    :param maximum: The maximum value of the stats block.
    :param standard_deviation: The standard deviation of the stats block.
    :param relative_standard_deviation: The relative standard deviation of the stats block.
    :param percentiles: The list of percentiles for the stats block as a `Values` instance.
    :param measurements: A list of raw measurements for initializing the stats block.
    :raise SimpleBenchTypeError: If any parameter is of an invalid type.
    :raise SimpleBenchValueError: If any parameter has an invalid value.
    """
    SCHEMA: type[JSONSchema] = StatsBlockSchema
    """The JSON schema class for the stats summary block in version 1 reports."""

    TYPE: str = SCHEMA.TYPE
    """The JSON report type property value for version 1 reports."""

    VERSION: int = SCHEMA.VERSION
    """The JSON report version number."""

    ID: str = SCHEMA.ID
    """The JSON report ID property value for version 1 reports."""

    # These are the public properties that define the object's state for comparison and hashing.
    # This avoids comparing internal-only or cached attributes like _measurements or _hash_cache.
    _COMPARISON_ATTRIBUTES = (
        "name",
        "description",
        "semantic_type",
        "unit",
        "scale",
        "iterations",
        "rounds",
        "mean",
        "median",
        "minimum",
        "maximum",
        "standard_deviation",
        "relative_standard_deviation",
        "percentiles",
    )

    _DERIVABLE_PROPERTIES = (
        "iterations",
        "mean",
        "median",
        "minimum",
        "maximum",
        "standard_deviation",
        "relative_standard_deviation",
        "percentiles",
    )

    __slots__ = (
        "_name",
        "_description",
        "_semantic_type",
        "_unit",
        "_scale",
        "_iterations",
        "_rounds",
        "_mean",
        "_median",
        "_minimum",
        "_maximum",
        "_standard_deviation",
        "_relative_standard_deviation",
        "_percentiles",
        "_measurements",
        "_hash_cache",
    )

    @overload
    def __init__(self, *,
                 name: str,
                 description: str,
                 semantic_type: str,
                 unit: str,
                 scale: float,
                 rounds: int,
                 measurements: Sequence[float] | Values) -> None:
        """Initialize a StatsBlock by calculating statistics from raw measurements."""

    @overload
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
        """Initialize a StatsBlock with pre-calculated statistical values."""

    def __init__(self, *,
                 name: str,
                 description: str,
                 semantic_type: str,
                 unit: str,
                 scale: float,
                 iterations: int | None = None,
                 rounds: int,
                 mean: float | None = None,
                 median: float | None = None,
                 minimum: float | None = None,
                 maximum: float | None = None,
                 standard_deviation: float | None = None,
                 relative_standard_deviation: float | None = None,
                 percentiles: Sequence[float] | None = None,
                 measurements: Sequence[float] | Values | None = None) -> None:
        """Initialize a StatsBlock object with the given parameters.

        The parameters are validated to ensure they meet the required types and constraints
        and match the contract of the JSON schema for the version 1 report.

        .. note::

            The following parameters can be derived from the measurements and cannot be
            set directly if measurements are provided. If measurements are provided and
            any of these parameters are also provided a value other than `None`,
            a `SimpleBenchValueError` will be raised.

            - mean
            - median
            - minimum
            - maximum
            - standard_deviation
            - relative_standard_deviation
            - percentiles

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
        :param measurements: The list of raw measurements for the stats block.
        :raise SimpleBenchTypeError: If any parameter is of an invalid type.
        :raise SimpleBenchValueError: If any parameter has an invalid value.
        """
        # First so other properties that can be lazy computed from
        # measurements are blocked from being set directly as they can be inferred as needed.
        # This prevents setting properties that can be derived from measurements
        # and possibly causing inconsistencies.
        self._measurements: Values | None = validate.measurements(measurements)
        """The raw measurements for the stats block as a Values instance or None.

        It is a private attribute and should not be accessed directly. It is not
        included in the exported dictionary representation of the StatsBlock or
        considered part of the object's identity for equality or hashing."""

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
        self._hash_cache: int | None = None
        self._validate_stats_block_consistency()

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "StatsBlock":
        """Create a StatsBlock object from a dictionary representation
        that conforms to the version 1 :class:`StatsBlockSchema`.

        :param data: A dictionary representation of a StatsBlock.
        :return StatsBlock: A StatsBlock object created from the dictionary.
        :raise SimpleBenchTypeError: If any parameter in the dictionary is of an invalid type.
        :raise SimpleBenchValueError: If any parameter in the dictionary has an invalid value.
        """
        allowed_keys = cls.init_params()
        allowed_keys['version'] = int
        allowed_keys['type'] = str

        kwargs = cls.import_data(
            data=data,
            allowed=allowed_keys,
            skip={'version', 'type', 'measurements'},
            optional={'description', 'version', 'type'},
            default={'description': '', 'version': cls.VERSION, 'type': cls.TYPE},
            match_on={'version': cls.VERSION, 'type': cls.TYPE},
            process_as={'percentiles': Values})
        return cls(**kwargs)

    def to_dict(self) -> dict[str, Any]:
        """Convert the StatsBlock object to a dictionary.

        The exported dictionary representation includes all properties of the StatsBlock
        except for the `measurements` property, which is not included.

        It is the canonical representation of the StatsBlock suitable for serialization to JSON
        and deserialization back into a StatsBlock object.

        :return: A dictionary representation of the StatsBlock.
        """
        property_keys = self.init_params().keys()
        data = {key: getattr(self, key) for key in property_keys}
        if 'measurements' in data:  # not included in the exported dictionary representation
            del data['measurements']
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
    @immutable
    def name(self, value: str) -> None:
        """Set the name of the stats block.

        :param value: The name of the stats block.
        :raise SimpleBenchTypeError: If name is not a string.
        :raise SimpleBenchValueError: If name is an empty string.
        :raise SimpleBenchAttributeError: If name is already set.
        """
        self._name: str = validate.name(value)

    @property
    def description(self) -> str:
        """Get the description of the stats block.

        :return: The description of the stats block.
        """
        return self._description

    @description.setter
    @immutable
    def description(self, value: str) -> None:
        """Set the description of the stats block.

        :param value: The description of the stats block.
        :raise SimpleBenchTypeError: If description is not a string.
        :raise SimpleBenchAttributeError: If description is already set.
        """
        self._description: str = validate.description(value)

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
    @immutable
    def semantic_type(self, value: str) -> None:
        """Set the semantic type of the stats block.

        :param value: The semantic type of the stats block.
        :raise SimpleBenchTypeError: If semantic_type is not a string.
        :raise SimpleBenchValueError: If semantic_type is not a valid namespaced identifier.
        :raise SimpleBenchAttributeError: If semantic_type is already set.
        """
        self._semantic_type = validate.semantic_type(value)

    @property
    def unit(self) -> str:
        """Get the unit of measurement.

        :return: The unit of measurement.
        """
        return self._unit

    @unit.setter
    @immutable
    def unit(self, value: str) -> None:
        """Set the unit of measurement.

        :param value: The unit of measurement.
        :raise SimpleBenchTypeError: If unit is not a string.
        :raise SimpleBenchValueError: If unit is an empty string.
        :raise SimpleBenchAttributeError: If unit is already set.
        """
        self._unit: str = validate.unit(value)

    @property
    def scale(self) -> float:
        """Get the scale factor.

        :return: The scale factor.
        :raise SimpleBenchTypeError: If scale is not a float.
        """
        return self._scale

    @scale.setter
    @immutable
    def scale(self, value: float) -> None:
        """Set the scale factor.

        :param value: The scale factor.
        :raise SimpleBenchTypeError: If scale is not a float.
        :raise SimpleBenchValueError: If scale is not a positive number.
        :raise SimpleBenchAttributeError: If scale is already set.
        """
        self._scale: float = validate.scale(value)

    @property
    def iterations(self) -> int:
        """Get the number of iterations.

        .. note::
            The value is either set directly or calculated from the `measurements` property.

        :return int: The number of iterations.
        :raise SimpleBenchValueError: If iterations cannot be returned because
            its value was not set directly and cannot be calculated because
            `measurements` are not available either.
        """
        if self._iterations is None:
            if self._measurements is None:
                raise SimpleBenchValueError(
                    "Cannot calculate iterations without measurements",
                    tag=_StatsBlockErrorTag.INVALID_MEASUREMENTS_STATE)
            self._iterations = len(self._measurements)
        return self._iterations

    @iterations.setter
    @immutable
    def iterations(self, value: int | None) -> None:
        """Set the number of iterations.

        .. warning:: Cannot be set if `measurements` are already set
            This property is mutually exclusive with the `measurements` property
            because its value can be calculated from the `measurements` property.

        :param value: The number of iterations.
        :raise SimpleBenchTypeError: If iterations is not an integer.
        :raise SimpleBenchValueError: If iterations is not a positive integer.
        :raise SimpleBenchAttributeError: If iterations is already set.
        """
        self._validate_no_measurements('iterations')
        self._iterations: int | None = validate.iterations(value)

    @property
    def rounds(self) -> int:
        """Get the number of rounds.

        :return: The number of rounds.
        """
        return self._rounds

    @rounds.setter
    @immutable
    def rounds(self, value: int) -> None:
        """Set the number of rounds.

        :param value: The number of rounds.
        :raise SimpleBenchTypeError: If rounds is not an integer.
        :raise SimpleBenchValueError: If rounds is not a positive integer.
        :raise SimpleBenchAttributeError: If rounds is already set.
        """
        self._rounds: int = validate.rounds(value)

    @property
    def mean(self) -> float:
        """Get the statistical mean value.

        .. note::
            The value is either set directly or calculated from the `measurements` property.

        :return float: The mean value.
        """
        if self._mean is None:
            if self._measurements is None:
                raise SimpleBenchValueError(
                    "Cannot calculate mean without measurements",
                    tag=_StatsBlockErrorTag.INVALID_MEASUREMENTS_STATE)
            self._mean = statistics.mean(self._measurements)
        return self._mean

    @mean.setter
    @immutable
    def mean(self, value: float | None) -> None:
        """Set the mean value.

        .. warning:: Cannot be set if `measurements` are already set
            This property is mutually exclusive with the `measurements` property
            because its value can be calculated from the `measurements` property.

        :param value: The mean value.
        :raise SimpleBenchAttributeError: If measurements are already set.
        :raise SimpleBenchTypeError: If mean is not a float.
        """
        self._validate_no_measurements('mean')
        self._mean: float | None = validate.mean(value)

    @property
    def median(self) -> float:
        """Get the statistical median value.

        .. note::
            The value is either set directly or calculated from the `measurements` property.

        :return float: The median value.
        """
        if self._median is None:
            if self._measurements is None:
                raise SimpleBenchValueError(
                    "Cannot calculate median without measurements",
                    tag=_StatsBlockErrorTag.INVALID_MEASUREMENTS_STATE)
            self._median = statistics.median(self._measurements)
        return self._median

    @median.setter
    @immutable
    def median(self, value: float | None) -> None:
        """Set the median value.

        .. warning:: Cannot be set if `measurements` are already set
            This property is mutually exclusive with the `measurements` property
            because its value can be calculated from the `measurements` property.

        :param value: The median value.
        :raise SimpleBenchValueError: If measurements are already set.
        :raise SimpleBenchTypeError: If median is not a float.
        """
        self._validate_no_measurements('median')
        self._median: float | None = validate.median(value)

    @property
    def minimum(self) -> float:
        """Get the minimum value.

        .. note::
            The value is either set directly or calculated from the `measurements` property.

        :return: The minimum value.
        """
        if self._minimum is None:
            if self._measurements is None:
                raise SimpleBenchValueError(
                    "Cannot calculate minimum without measurements",
                    tag=_StatsBlockErrorTag.INVALID_MEASUREMENTS_STATE)
            self._minimum = float(min(self._measurements))
        return self._minimum

    @minimum.setter
    @immutable
    def minimum(self, value: float | None) -> None:
        """Set the minimum value.

        .. warning:: Cannot be set if `measurements` are already set
            This property is mutually exclusive with the `measurements` property
            because its value can be calculated from the `measurements` property.

        :param float | None value: The minimum value.
        :raise SimpleBenchTypeError: If minimum is not a float.
        :raise SimpleBenchAttributeError: If measurements are already set.
        """
        self._validate_no_measurements("minimum")
        self._minimum: float | None = validate.minimum(value)

    @property
    def maximum(self) -> float:
        """Get the maximum value.

        .. note::
            The value is either set directly or calculated from the `measurements` property.

        :return: The maximum value.
        """
        if self._maximum is None:
            if self._measurements is None:
                raise SimpleBenchValueError(
                    "Cannot calculate maximum without measurements",
                    tag=_StatsBlockErrorTag.INVALID_MEASUREMENTS_STATE)
            self._maximum = float(max(self._measurements))
        return self._maximum

    @maximum.setter
    @immutable
    def maximum(self, value: float | None) -> None:
        """Set the maximum value.

        .. warning:: Cannot be set if `measurements` are already set
            This property is mutually exclusive with the `measurements` property
            because its value can be calculated from the `measurements` property.

        :param float | None value: The maximum value.
        :raise SimpleBenchTypeError: If maximum is not a float.
        :raise SimpleBenchAttributeError: If maximum is already set.
        """
        self._validate_no_measurements("maximum")
        self._maximum: float | None = validate.maximum(value)

    @property
    def standard_deviation(self) -> float:
        """Get the standard deviation.

        .. note::
            The value is either set directly or calculated from the `measurements` property.

        :return: The standard deviation.
        """
        if self._standard_deviation is None:
            if self._measurements is None:
                raise SimpleBenchValueError(
                    "Cannot calculate standard deviation without measurements",
                    tag=_StatsBlockErrorTag.INVALID_MEASUREMENTS_STATE)
            if len(self._measurements) > 1:
                self._standard_deviation = float(
                    statistics.stdev(self._measurements) * sqrt(self.rounds))
            else:
                self._standard_deviation = 0.0

        return self._standard_deviation

    @standard_deviation.setter
    @immutable
    def standard_deviation(self, value: float | None) -> None:
        """Set the standard deviation.

        .. warning:: Cannot be set if `measurements` are already set
            This property is mutually exclusive with the `measurements` property
            because its value can be calculated from the `measurements` property.

        :param value: The standard deviation.
        :raise SimpleBenchTypeError: If standard_deviation is not a float.
        :raise SimpleBenchValueError: If standard_deviation is negative.
        :raise SimpleBenchValueError: If measurements are already set.
        :raise SimpleBenchAttributeError: If standard_deviation is already set.
        """
        self._validate_no_measurements("standard_deviation")
        self._standard_deviation: float | None = validate.standard_deviation(value)

    @property
    def relative_standard_deviation(self) -> float:
        """Get the relative standard deviation.

        The relative standard deviation (RSD) is calculated as the standard deviation
        divided by the mean, expressed as a percentage.

        .. note::
            If `mean` is exactly 0.0 but there is variation in the measurements,
            the relative standard deviation will be set to a very large number (1e9)
            to indicate an undefined relative standard deviation. This is because
            RSD is not mathematically defined when the mean is zero but there is
            variation in the measurements. If both the mean and standard deviation are zero,
            the relative standard deviation will be set to 0.0.

            The 1e9 value is used as a placeholder to indicate an undefined relative
            standard deviation without causing a division by zero error or needing
            to use NaN or inf values that cannot be easily represented in JSON.

        :return: The relative standard deviation.
        """
        if self._relative_standard_deviation is None:
            if self._measurements is None:
                raise SimpleBenchValueError(
                    "Cannot calculate relative standard deviation without measurements",
                    tag=_StatsBlockErrorTag.INVALID_MEASUREMENTS_STATE)
            if self.mean == 0.0:
                self._relative_standard_deviation = 1e9 if self.standard_deviation else 0.0
            else:
                self._relative_standard_deviation = abs(self.standard_deviation / self.mean * 100)
        return self._relative_standard_deviation

    @relative_standard_deviation.setter
    @immutable
    def relative_standard_deviation(self, value: float | None) -> None:
        """Set the relative standard deviation.

        :param value: The relative standard deviation.
        :raise SimpleBenchTypeError: If relative_standard_deviation is not a float.
        :raise SimpleBenchValueError: If relative_standard_deviation is negative.
        :raise SimpleBenchValueError: If measurements are already set.
        :raise SimpleBenchAttributeError: If relative_standard_deviation is already set.
        """
        self._validate_no_measurements("relative_standard_deviation")
        self._relative_standard_deviation: float | None = validate.relative_standard_deviation(value)

    @property
    def percentiles(self) -> Values:
        """Get the values for the percentiles.

        The percentiles are represented as a sorted Values instance containing 101 float values
        corresponding to the percentiles from 0 to 100.

        .. note::
            The value is either set directly or calculated from the `measurements` property.

        :return Values: The Values instance containing the percentiles.
        :raise SimpleBenchValueError: If percentiles cannot be calculated because measurements are not set.

        """
        if self._percentiles is None:
            if self._measurements is None:
                raise SimpleBenchValueError(
                    "Cannot calculate percentiles without measurements",
                    tag=_StatsBlockErrorTag.INVALID_MEASUREMENTS_STATE)
            self._percentiles = self._calculate_percentiles()
        return self._percentiles

    @percentiles.setter
    @immutable
    def percentiles(self, value: Sequence[float | int] | None) -> None:
        """Set the list of percentiles.

        The percentiles must be a sequence of 101 float or int values representing the percentiles
        from 0 to 100. The values must be sorted in ascending order.

        :param value: The list of percentiles.
        :raise SimpleBenchTypeError: If percentiles is not None or a sequence of float.
        :raise SimpleBenchValueError: If the sequence does not contain exactly 101 numbers
            or is not sorted in ascending order.
        :raise SimpleBenchValueError: If measurements are already set and the value is not None.
        :raise SimpleBenchAttributeError: If percentiles is already set.
        """
        self._validate_no_measurements("percentiles")
        self._percentiles: Values | None = validate.percentiles(value)

    def _validate_no_measurements(self, name: str) -> None:
        """Raises an exception if the measurements value is not None.

        :param name: The name of the value being set.
        :raises SimpleBenchValueError: If measurements are already set.
        """
        if self._measurements is not None:
            raise SimpleBenchValueError(
                f"Cannot set {name} when measurements are already set",
                tag=_StatsBlockErrorTag.INVALID_MEASUREMENTS_STATE)

    def _calculate_percentiles(self) -> Values:
        """Helper to calculate percentiles from the measurements.

        It returns a Values instance containing 101 floats representing the
        percentiles from 0 to 100.

        Note:

            statistics.quantiles with n=102 and method='inclusive' is used
            to calculate the percentiles from 0 to 100 inclusive (it generates 101
            cut points, which correspond to percentiles 0 through 100
            with 0 being the minimum value and 100 being the maximum value).

        Returns:
            A Values instance containing the percentiles from 0 to 100.
        """
        data = self._measurements
        if data is None:
            raise SimpleBenchValueError(
                "Cannot calculate percentiles because measurements are not set",
                tag=_StatsBlockErrorTag.INVALID_MEASUREMENTS_STATE)
        if len(data) == 1:
            data_value = float(data[0])
            return Values([data_value] * 101)
        quantile_values = statistics.quantiles(data, n=102, method='inclusive')
        return Values(quantile_values)

    def _validate_stats_block_consistency(self) -> None:
        """Validate the consistency of the StatsBlock instance.

        This method checks that if measurements are NOT provided,
        then all statistical properties that could otherwise be derived
        from them have been explicitly set.

        :raise SimpleBenchValueError: If measurements are NOT provided
            and any of the derivable statistical properties were not set.
        """
        if self._measurements is not None:
            return

        # If no measurements, all derivable properties must have been set.
        unset_properties: list[str] = []
        for attr in self._DERIVABLE_PROPERTIES:
            backing_attr = f"_{attr}"
            if getattr(self, backing_attr, None) is None:
                unset_properties.append(attr)

        if unset_properties:
            raise SimpleBenchValueError(
                "Either the 'measurements' argument must be provided, or all of the following arguments must be set: "
                f"{', '.join(unset_properties)}",
                tag=_StatsBlockErrorTag.INVALID_STATS_BLOCK_ARGUMENTS)

    def __eq__(self, other: object) -> bool:
        """Check equality between two StatsBlock instances.

        .. note::
            Triggers the lazy eval properties to be evaluated if they have not been already.
            This ensures that comparisons are made based on the actual values of the properties.

            This can be expensive the first time it is called if many properties
            need to be calculated from many measurements.

            This is unavoidable since equality must reflect the actual state of the object.

        :param other: The other StatsBlock instance to compare with.
        :return bool: True if the two StatsBlock instances are equal, False otherwise.
        """
        if not isinstance(other, StatsBlock):
            return NotImplemented

        # Use all() with a generator for an efficient, short-circuiting comparison
        # of the public properties that define the object's state.
        return all(getattr(self, attr) == getattr(other, attr) for attr in self._COMPARISON_ATTRIBUTES)

    def __hash__(self) -> int:
        """Compute the hash of the StatsBlock instance.

        The hash is computed from the public properties that define the object's state
        and is cached for performance.

        .. note::
            Triggers the lazy eval properties to be evaluated if they have not been already.
            This ensures that the hash is based on the actual values of the properties.

            This can be expensive the first time it is called if many properties
            need to be calculated from many measurements. This is unavoidable
            since the hash must reflect the actual state of the object.

        :return int: The hash value of the StatsBlock instance.
        """
        if self._hash_cache is None:
            # Build a tuple of all state-defining public properties and hash it.
            state = tuple(getattr(self, attr) for attr in self._COMPARISON_ATTRIBUTES)
            self._hash_cache = hash(state)   # pylint: disable=attribute-defined-outside-init
        return self._hash_cache

    def __repr__(self) -> str:
        """Get the string representation of the StatsBlock instance.

        The representation is a string that can be used to recreate the object.
        It triggers the lazy evaluation of any properties that have not been calculated yet.

        :return str: The string representation of the StatsBlock.
        """
        # Get the constructor parameters, excluding 'measurements' as this repr
        # should represent the object's state via its calculated statistical properties.
        init_params = self.__class__.init_params()
        if 'measurements' in init_params:
            del init_params['measurements']

        # Build the key-value argument string. Accessing the properties via getattr
        # will trigger their lazy calculation if they haven't been computed yet.
        calling_args = ', '.join(f"{key}={getattr(self, key)!r}" for key in init_params)
        return f"{self.__class__.__name__}({calling_args})"

    def __getstate__(self) -> tuple[dict[str, Any] | None, tuple[Any, ...]]:
        """Prepare the object's state for pickling, prioritizing size.

        This method ensures that the pickled representation of the StatsBlock
        is compact. It achieves this by forcing the calculation of any lazy-evaluated
        statistical properties and then excluding the potentially large `_measurements`
        list from the pickled state.

        This prioritizes a small pickled size and fast subsequent unpickling over
        preserving the lazy-evaluation state across serialization.

        :return: A state tuple for pickling.
        :rtype: tuple[dict[str, Any] | None, tuple[Any, ...]]
        """
        # Trigger all lazy calculations by accessing the public properties.
        # This ensures the internal state (_mean, _median, etc.) is populated.
        for attr in self._COMPARISON_ATTRIBUTES:
            getattr(self, attr)

        # Build the state tuple for a __slots__ class. The first element is for
        # __dict__ (None in our case) and the second is a tuple of the slotted values.
        state = tuple(
            None if slot == '_measurements' else getattr(self, slot)
            for slot in self.__slots__
        )
        return (None, state)

    def __setstate__(self, state: tuple[dict[str, Any] | None, tuple[Any, ...]]) -> None:
        """Restore the object's state from a pickled representation.

        This method is the counterpart to `__getstate__`. It takes the state
        tuple and repopulates the instance's `__slots__`.

        .. note::
            This method bypasses `__init__`, which is standard for unpickling.

        :param state: The state tuple from unpickling.
        :type state: tuple[dict[str, Any] | None, tuple[Any, ...]]
        """
        # The first element of the state tuple is for __dict__, which is None for this class.
        # The second element is a tuple of values for the __slots__.
        slot_values = state[1]
        for slot, value in zip(self.__slots__, slot_values):
            # Use object.__setattr__ to bypass our immutable setters.
            object.__setattr__(self, slot, value)

    def __deepcopy__(self, memo: dict[int, Any]) -> "StatsBlock":
        """Return a shallow copy of the instance as an optimized deep copy.

        Since the StatsBlock instance is immutable and composed of immutable components,
        a shallow copy is functionally identical to a deep copy. This method overrides
        the default `copy.deepcopy` behavior to perform a more efficient shallow copy instead.

        :param memo: The memoization dictionary used by `copy.deepcopy`.
                     It is not used in this optimized implementation.
        :return StatsBlock: A new, shallow-copied instance of the StatsBlock.
        """
        # because the StatsBlock is immutable, we can return a copy of self
        return copy(self)
