"""V1 StatsBlock class

This class represents a stats block information in a JSON report.

It implements validation and serialization/deserialization methods to and from dictionaries
for the following JSON Schema version:

https://raw.githubusercontent.com/JerilynFranz/python-simplebench/main/schemas/v1/stats-block.json

It is the base implemention of the JSON report stats block representation.

This makes the implementations of StatsBlock backwards compatible with future versions
of the JSON report schema and the V1 implementation itself is essentially a frozen snapshot
of the base StatsBlock representation at the time of the V1 schema release.

The code has three basic paths for creating a stats block:

1. Creation by directly instantiating the `StatsBlock` class with the required statistical parameters.
2. Creation by instantiating the `StatsBlock` class with the raw data measurements and
   having the class calculate the statistical parameters.
3. Creation by using the `from_dict` class method to create a `StatsBlock` instance from a
   dictionary that matches the JSON schema. This does not allow raw measurements to be
   provided; the statistical parameters must be provided directly in the dictionary.

The created instance and all values available via properties are immutable once created
and can be serialized back to a dictionary using the `to_dict` method.

The class also implements equality and hashing methods to allow comparison
and use in hash-based collections like sets and dictionaries. It also
implements size-optimized pickling support for serialization/deserialization.

The dictionary serialized representation matches the JSON schema for version 1 reports
and can be used for JSON serialization and deserialization.

Some statistical properties cannot always be calculated from raw measurements (e.g.,
if there are too few measurements to calculate stdev) and so these properties (stdev, relative_stdev,
drift_index, autocorrelation, percentiles) may be NaN.

In the dictionary and JSON representations, NaN values are converted to None to
ensure compatibility with JSON, which does not support NaN as a value.

While the StatsBlock can be initialized using measurements, they are NOT
considered part of the StatsBlock's identity for equality or hashing, and they are not included in the
dictionary representation of the StatsBlock. They are only used optionally in calculating the statistical properties
when initializing the object and are not stored as part of the object's state for comparison or serialization.
"""

import statistics
from collections.abc import Mapping, Sequence
from math import isnan, sqrt
from types import MappingProxyType
from typing import Any, overload

from simplebench.exceptions import SimpleBenchTypeError, SimpleBenchValueError
from simplebench.report._error_tags import _StatsBlockErrorTag
from simplebench.report.base import BaseStatsBlock, JSONSchema
from simplebench.simplebench_types import CoreDataMapping, Values

from ..metric import Metric
from ..metrics import Metrics
from . import _validate
from .stats_block_dict import ImmutableStatsBlockDict, StatsBlockData
from .stats_block_schema import StatsBlockSchema

__all__: list[str] = []


class StatsBlock(BaseStatsBlock):
    """Class representing a stats summary for V1 reports.

    This class represents a stats block information in a JSON report.
    It implements validation and serialization/deserialization methods to and from dictionaries
    for the following JSON Schema version:

    https://raw.githubusercontent.com/JerilynFranz/python-simplebench/main/schemas/v1/stats-block.json

    :hash_id str: The hash identifier for the stats block.

    Properties:

    :param Metric metric: The Metric instance associated with this stats block.
    :param int iterations: The number of iterations measured for the stats block.
    :param int rounds: The number of rounds in each iteration measured.
    :param float mean: The mean value of the stats block.
    :param float median: The median value of the stats block.
    :param float minimum: The minimum value of the stats block.
    :param float maximum: The maximum value of the stats block.
    :param float stdev: The standard deviation of the stats block.
    :param float relative_stdev: The relative standard deviation of the stats block.
    :param float drift_index: The drift index (Pearson correlation with sequential position indices) of the stats block.
    :param float autocorrelation: The lag-1 autocorrelation of the measurement sequence for the stats block.
    :param Values percentiles: The list of percentiles for the stats block as a `Values` instance.
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

    _init_params_cache: MappingProxyType[str, Any] = MappingProxyType({})
    """Cache for the constructor parameters of the StatsBlock class."""

    @classmethod
    def _data_params(cls) -> MappingProxyType[str, Any]:
        """Get the constructor parameters for the schema data class.

        The parameters are cached after the first call for performance.

        It is returned as a read-only mapping and includes 'type' and 'version'.

        :return MappingProxyType[str, Any]: A read-only mapping of constructor parameter names and types.
        """
        if not cls._init_params_cache:
            params = cls.init_params(StatsBlockData)
            cls._init_params_cache = MappingProxyType(params)
        return cls._init_params_cache

    _DERIVABLE_PROPERTIES = (
        'iterations',
        'mean',
        'median',
        'minimum',
        'maximum',
        'stdev',
        'relative_stdev',
        'drift_index',
        'autocorrelation',
        'percentiles',
    )

    __slots__ = (
        '_hash_id',
        '_iterations',
        '_rounds',
        '_mean',
        '_median',
        '_minimum',
        '_maximum',
        '_stdev',
        '_relative_stdev',
        '_drift_index',
        '_autocorrelation',
        '_percentiles',
        '_measurements',
        '_to_dict_cache',
    )

    @overload
    def __init__(
        self,
        *,
        hash_id: str = '',
        metric: Metric,
        rounds: int,
        measurements: Sequence[float] | Values,
    ) -> None:
        """Initialize a StatsBlock by calculating statistics from raw measurements.

        :param str hash_id: The hash identifier for the stats block.
        :param Metric metric: The Metric instance associated with this stats block.
        :param int rounds: The number of rounds in the stats block.
        :param Sequence[float] | Values | None measurements: The list of raw measurements for the stats block.
        """

    @overload
    def __init__(
        self,
        *,
        hash_id: str = '',
        metric: Metric,
        iterations: int,
        rounds: int,
        mean: float,
        median: float,
        minimum: float,
        maximum: float,
        stdev: float,
        relative_stdev: float,
        drift_index: float,
        autocorrelation: float,
        percentiles: Sequence[float],
    ) -> None:
        """Initialize a StatsBlock with pre-calculated statistical values.

        :param Metric metric: The Metric instance associated with this stats block.
        :param int | None iterations: The number of iterations in the stats block.
        :param int rounds: The number of rounds in the stats block.
        :param float | None mean: The mean value of the stats block.
        :param float | None median: The median value of the stats block.
        :param float | None minimum: The minimum value of the stats block.
        :param float | None maximum: The maximum value of the stats block.
        :param float | None stdev: The standard deviation of the stats block.
        :param float | None relative_stdev: The relative standard deviation of the stats block.
        :param float drift_index: The drift index (Pearson correlation with position).
        :param float autocorrelation: The lag-1 autocorrelation of the measurement sequence.
        :param Sequence[float] | None percentiles: The list of percentiles for the stats block.
        """

    def __init__(
        self,
        *,
        hash_id: str = '',
        metric: Metric,
        iterations: int | None = None,
        rounds: int,
        mean: float | None = None,
        median: float | None = None,
        minimum: float | None = None,
        maximum: float | None = None,
        stdev: float | None = None,
        relative_stdev: float | None = None,
        drift_index: float | None = None,
        autocorrelation: float | None = None,
        percentiles: Sequence[float] | None = None,
        measurements: Sequence[float] | Values | None = None,
    ) -> None:
        """Initialize a StatsBlock object with the given parameters.

        The parameters are validated to ensure they meet the required types and constraints
        and match the contract of the JSON schema for the version 1 report.

        .. note::

            The following parameters can be derived from the measurements and cannot be
            set directly if measurements are provided. If measurements are provided and
            any of these parameters are also provided a value other than `None`,
            a `SimpleBenchTypeError` will be raised.

            - iterations
            - mean
            - median
            - minimum
            - maximum
            - stdev
            - relative_stdev
            - drift_index
            - autocorrelation
            - percentiles

        :param str hash_id: The hash identifier for the stats block.
        :param int | None iterations: The number of iterations. (exclusive with `measurements`)
        :param int rounds: The number of rounds in the stats block.
        :param str timer: The timer used for measurements.
        :param float | None mean: The mean value of the data. (exclusive with `measurements`)
        :param float | None median: The median value of the data. (exclusive with `measurements`)
        :param float | None minimum: The minimum value of the data. (exclusive with `measurements`)
        :param float | None maximum: The maximum value of the data. (exclusive with `measurements`)
        :param float | None stdev: The standard deviation of the data. (exclusive with `measurements`)
        :param float | None relative_stdev: The relative standard deviation of the data. (exclusive with `measurements`)
        :param Sequence[float] | None percentiles: The list of percentiles for the data (exclusive with `measurements`).
        :param Sequence[float] | Values | None measurements: The list of raw measurements for the data.
        :raise SimpleBenchTypeError: If any parameter is of an invalid type.
        :raise SimpleBenchValueError: If any parameter has an invalid value.
        """
        # First so other properties that can be lazy computed from
        # measurements are blocked from being set directly as they can be inferred as needed.
        # This prevents setting properties that can be derived from measurements
        # and possibly causing inconsistencies.
        self._measurements: Values | None = _validate.measurements(measurements)
        """The raw measurements for the stats block as a Values instance or None.

        It is a private attribute and should not be accessed directly. It is not
        included in the exported dictionary representation of the StatsBlock or
        considered part of the object's identity for equality or hashing."""

        self._metric: Metric = _validate.metric(metric)
        """The Metric instance associated with this stats block."""
        self._rounds: int = _validate.rounds(rounds)
        """The number of rounds per iteration."""

        self._hash_id: str = _validate.hash_id(hash_id)
        """The hash identifier for the stats block."""

        # potentially derivable properties - only settable if measurements is None
        self._iterations: int | None = _validate.iterations(iterations, self._measurements)
        """The number of iterations."""
        self._mean: float | None = _validate.mean(mean, self._measurements)
        """The mean value."""
        self._median: float | None = _validate.median(median, self._measurements)
        """The median value."""
        self._minimum: float | None = _validate.minimum(minimum, self._measurements)
        """The minimum value."""
        self._maximum: float | None = _validate.maximum(maximum, self._measurements)
        """The maximum value."""
        self._stdev: float | None = _validate.stdev(stdev, self._measurements)
        """The standard deviation."""
        self._relative_stdev: float | None = _validate.relative_stdev(relative_stdev, self._measurements)
        """The relative standard deviation."""
        self._drift_index: float | None = _validate.drift_index(drift_index, self._measurements)
        """The drift index (Pearson correlation with sequential position indices)."""
        self._autocorrelation: float | None = _validate.autocorrelation(autocorrelation, self._measurements)
        """The lag-1 autocorrelation of the measurement sequence."""
        self._percentiles: Values | None = _validate.percentiles(percentiles, self._measurements)
        """The list of percentiles."""

        self._to_dict_cache: ImmutableStatsBlockDict | None = None
        """Cache for the dictionary representation of the object."""

        self._validate_stats_block_consistency()

    @classmethod
    def from_dict(cls, data: Mapping[str, Any], metrics_registry: 'Metrics') -> 'StatsBlock':
        """Create a StatsBlock object from a dictionary representation
        that conforms to the version 1 :class:`StatsBlockSchema`.

        This method validates the input dictionary to ensure it matches
        the expected schema and types before creating the StatsBlock instance.

        It cannot be instantiated using raw measurements via this method;
        the statistical parameters must be provided directly in the dictionary.

        :param Any data: A dictionary representation of a StatsBlock.
        :param Metrics metrics_registry: A Metrics object for validating metric references.
        :return StatsBlock: A StatsBlock object created from the dictionary.
        :raise SimpleBenchTypeError: If any parameter in the dictionary is of an invalid type.
        :raise SimpleBenchTypeError: If the metrics registry is not of type Metrics.
        :raise SimpleBenchTypeError: If the data parameter is not a mapping type.
        :raise SimpleBenchValueError: If any parameter in the dictionary has an invalid value.
        :raise SimpleBenchValueError: If the metric reference in the dictionary is missing, invalid,
            or not found in the metrics registry.
        :raise SimpleBenchValueError: If the input data does not conform to the expected schema.
        :raise SimpleBenchValueError: If the input data contains unexpected extra keys or is missing required keys.
        """
        if not isinstance(data, Mapping):
            raise SimpleBenchTypeError(
                f"Invalid data type for StatsBlock: expected Mapping, got {type(data).__name__}.",
                tag=_StatsBlockErrorTag.INVALID_DATA_TYPE,
            )
        if not isinstance(metrics_registry, Metrics):
            raise SimpleBenchTypeError(
                f"Invalid metrics registry type: expected Metrics, got {type(metrics_registry).__name__}.",
                tag=_StatsBlockErrorTag.INVALID_METRICS_REGISTRY_TYPE,
            )
        allowed_keys = cls._data_params()

        data = dict(data)  # Make a shallow copy to avoid mutating the input

        # Lookup the metric in the metrics registry using the hash_id from the input data
        # as a foreign key. This allows us to convert the metric hash_id string from the input data
        # into the corresponding Metric instance from the metrics registry, which is required for
        # constructing the StatsBlock instance.
        if 'metric' not in data:
            raise SimpleBenchValueError(
                "Missing required field 'metric' in data for StatsBlock.",
                tag=_StatsBlockErrorTag.MISSING_METRIC_FIELD
            )
        metric_hash_id: str = data['metric']
        if not isinstance(metric_hash_id, str):
            raise SimpleBenchTypeError(
                f"Invalid type for 'metric' field: expected str, got {type(metric_hash_id).__name__}.",
                tag=_StatsBlockErrorTag.INVALID_METRIC_HASH_ID,
            )
        if metric_hash_id not in metrics_registry:
            raise SimpleBenchValueError(
                f"Invalid 'metric' field value: '{metric_hash_id}' not found in metrics registry.",
                tag=_StatsBlockErrorTag.UNKNOWN_METRIC_HASH_ID,
            )
        data['metric'] = metrics_registry[metric_hash_id]

        kwargs = cls.import_data(
            data=data,
            allowed_fields=allowed_keys,
            skip_fields={'version', 'type'},
            optional_fields={'description', 'version', 'type', 'hash_id'},
            defaults={'description': '', 'version': cls.VERSION, 'type': cls.TYPE},
            match_on={'version': cls.VERSION, 'type': cls.TYPE},
            process_as={'percentiles': Values,
                        'stdev': cls.import_stdev,
                        'relative_stdev': cls.import_relative_stdev,
                        'drift_index': cls.import_drift_index,
                        'autocorrelation': cls.import_autocorrelation},
        )
        return cls(**kwargs)

    @classmethod
    def import_stdev(cls, value: Any) -> float:
        """Import and validate the stdev value from the input data.

        This method validates that the stdev value is a float, int, or None.
        If it is a float or int, it must be non-negative. If it is None, it is imported as NaN.

        :param Any value: The stdev value to validate.
        :return float: The validated stdev value as a float.
        :raise SimpleBenchTypeError: If the value is not a float, int or None.
        :raise SimpleBenchValueError: If the value is a negative float or int.
        """
        if value is None:
            return float('nan')
        if not isinstance(value, (float, int)):
            raise SimpleBenchTypeError(
                f'stdev must be a float, int, or None, got {type(value).__name__}',
                tag=_StatsBlockErrorTag.INVALID_STANDARD_DEVIATION_TYPE,
            )
        if value < 0.0:
            raise SimpleBenchValueError(
                f'stdev must be non-negative, got {value}',
                tag=_StatsBlockErrorTag.INVALID_STANDARD_DEVIATION_VALUE,
            )
        return float(value)

    @classmethod
    def import_relative_stdev(cls, value: Any) -> float:
        """Import and validate the relative_stdev value from the input data.

        This method validates that the relative_stdev value is a float, int, or None.
        If it is a float or int, it must be non-negative. If it is None, it is imported as NaN.

        :param Any value: The relative_stdev value to validate.
        :return float: The validated relative_stdev value as a float.
        :raise SimpleBenchTypeError: If the value is not a float, int or None.
        :raise SimpleBenchValueError: If the value is a negative float or int.
        """
        if value is None:
            return float('nan')
        if not isinstance(value, (float, int)):
            raise SimpleBenchTypeError(
                f'relative_stdev must be a float, int, or None, got {type(value).__name__}',
                tag=_StatsBlockErrorTag.INVALID_RELATIVE_STANDARD_DEVIATION_TYPE,
            )
        if value < 0.0:
            raise SimpleBenchValueError(
                f'relative_stdev must be non-negative, got {value}',
                tag=_StatsBlockErrorTag.INVALID_RELATIVE_STANDARD_DEVIATION_VALUE,
            )
        return float(value)

    @classmethod
    def import_drift_index(cls, value: Any) -> float:
        """Import and validate the drift_index value from the input data.

        This method validates that the drift_index value is a float, int, or None.
        If it is a float or int, it must be in the range [-1.0, 1.0]. If it is None, it is imported as NaN.

        :param Any value: The drift_index value to validate.
        :return float: The validated drift_index value as a float.
        :raise SimpleBenchTypeError: If the value is not a float, int or None.
        :raise SimpleBenchValueError: If the value is a float or int but not in the range [-1.0, 1.0].
        """
        if value is None:
            return float('nan')
        if not isinstance(value, (float, int)):
            raise SimpleBenchTypeError(
                f'drift_index must be a float, int, or None, got {type(value).__name__}',
                tag=_StatsBlockErrorTag.INVALID_DRIFT_INDEX_TYPE,
            )
        if value < -1.0 or value > 1.0:
            raise SimpleBenchValueError(
                f'drift_index must be in the range [-1.0, 1.0], got {value}',
                tag=_StatsBlockErrorTag.INVALID_DRIFT_INDEX_VALUE,
            )
        return float(value)

    @classmethod
    def import_autocorrelation(cls, value: Any) -> float:
        """Import and validate the autocorrelation value from the input data.

        This method validates that the autocorrelation value is a float, int, or None.
        If it is a float or int, it must be in the range [-1.0, 1.0]. If it is None, it is imported as NaN.

        :param Any value: The autocorrelation value to validate.
        :return float: The validated autocorrelation value as a float.
        :raise SimpleBenchTypeError: If the value is not a float, int or None.
        :raise SimpleBenchValueError: If the value is a float or int but not in the range [-1.0, 1.0].
        """
        if value is None:
            return float('nan')
        if not isinstance(value, (float, int)):
            raise SimpleBenchTypeError(
                f'autocorrelation must be a float, int, or None, got {type(value).__name__}',
                tag=_StatsBlockErrorTag.INVALID_AUTOCORRELATION_TYPE,
            )
        if value < -1.0 or value > 1.0:
            raise SimpleBenchValueError(
                f'autocorrelation must be in the range [-1.0, 1.0], got {value}',
                tag=_StatsBlockErrorTag.INVALID_AUTOCORRELATION_VALUE,
            )
        return float(value)

    def to_dict(self) -> ImmutableStatsBlockDict:
        """Convert the StatsBlock object to an immutable mapping conforming to the version 1
        :class:`ImmutableStatsBlockSchema`.

        The exported mapping includes all properties of the StatsBlock and
        expands any nested objects by calling their own `to_dict` methods if available.

        It is the canonical representation of the StatsBlock suitable for serialization to JSON
        and deserialization back into a StatsBlock object.

        It converts possible NaN values to None in the output dictionary to ensure JSON compatibility, as NaN is not a
        valid JSON value.

        :return ImmutableStatsBlockDict: A dictionary representation of the StatsBlock.
        """
        return CoreDataMapping({
            'type': self.TYPE,
            'version': self.VERSION,
            'hash_id': self.hash_id,
            'metric': self.metric.to_dict(),
            'iterations': self.iterations,
            'rounds': self.rounds,
            'mean': self.mean,
            'median': self.median,
            'minimum': self.minimum,
            'maximum': self.maximum,
            'stdev': None if isnan(self.stdev) else self.stdev,
            'relative_stdev': None if isnan(self.relative_stdev) else self.relative_stdev,
            'drift_index': None if isnan(self.drift_index) else self.drift_index,
            'autocorrelation': None if isnan(self.autocorrelation) else self.autocorrelation,
            'percentiles': self.percentiles
        })  # type: ignore[return-value]
    # The return type is actually a CoreDataMapping that conforms to the ImmutableStatsBlockDict
    # TypedDict protocol, but we use the protocol as the return type for better type checking and to avoid
    # exposing the internal CoreDataMapping class in the public API.

    def for_json(self) -> ImmutableStatsBlockDict:
        """Get the JSON-serializable dictionary representation of this StatsBlock.

        This method delegates to the for_json method of the dictionary returned by :meth:`to_dict`
        because the dictionary is actually an instance of :class:`CoreDataMapping`
        which has the for_json method to convert to a JSON-serializable dictionary.

        :return: The JSON-serializable dictionary representation of this StatsBlock.
        """
        return self.to_dict().for_json()  # type: ignore[return-value]

    def as_json(self) -> str:
        """Get the JSON string representation of this StatsBlock.

        This method delegates to the as_json method of the dictionary returned by :meth:`to_dict`
        because the dictionary is actually an instance of :class:`CoreDataMapping`
        which has the as_json method to convert to a JSON string.

        :return: The JSON string representation of this StatsBlock.
        """
        return self.to_dict().as_json()  # type: ignore

    @property
    def hash_id(self) -> str:
        """Get the hash identifier of the stats block.

        :return: The hash identifier of the stats block.
        """
        if self._hash_id == '':
            self._hash_id = self._hash_id_helper(StatsBlockData)
        return self._hash_id

    @property
    def title(self) -> str:
        """Get the title of the stats block.

        :return: The title of the stats block.
        """
        return self.metric.title

    @property
    def description(self) -> str:
        """Get the description of the stats block.

        :return: The description of the stats block.
        """
        return self.metric.description

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
        return self.metric.semantic_type

    @property
    def metric(self) -> Metric:
        """Get the Metric instance associated with this stats block.

        :return: The Metric instance associated with this stats block.
        """
        return self._metric

    @property
    def unit(self) -> str:
        """Get the unit of measurement.

        :return: The unit of measurement.
        """
        return self.metric.unit

    @property
    def scale(self) -> float:
        """Get the scale factor.

        :return: The scale factor.
        :raise SimpleBenchTypeError: If scale is not a float.
        """
        return self.metric.scale

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
        if self._iterations is None:  # We have measurements if iterations is None (validated in __init__)
            self._iterations = len(self._measurements)  # type: ignore
        return self._iterations

    @property
    def rounds(self) -> int:
        """Get the number of rounds.

        :return: The number of rounds.
        """
        return self._rounds

    @property
    def mean(self) -> float:
        """Get the statistical mean value.

        .. note::
            The value is either set directly or calculated from the `measurements` property.

        :return float: The mean value.
        """
        if self._mean is None:
            self._mean = float(statistics.mean(self._measurements))  # type: ignore  # validated in __init__
        return self._mean

    @property
    def median(self) -> float:
        """Get the statistical median value.

        .. note::
            The value is either set directly or calculated from the `measurements` property.

        :return float: The median value.
        """
        if self._median is None:
            self._median = float(statistics.median(self._measurements))  # type: ignore  # validated in __init__
        return self._median

    @property
    def minimum(self) -> float:
        """Get the minimum value.

        .. note::
            The value is either set directly or calculated from the `measurements` property.

        :return: The minimum value.
        """
        if self._minimum is None:
            self._minimum = float(min(self._measurements))  # type: ignore  # validated in __init__
        return self._minimum

    @property
    def maximum(self) -> float:
        """Get the maximum value.

        .. note::
            The value is either set directly or calculated from the `measurements` property.

        :return: The maximum value.
        """
        if self._maximum is None:
            self._maximum = float(max(self._measurements))  # type: ignore  # validated in __init__
        return self._maximum

    @property
    def stdev(self) -> float:
        """Get the standard deviation.

        This calculates the estimated per-round standard deviation.

        .. note::
            The standard deviation is scaled from the raw calculated standard deviation of the iterations
            by the square root of the number of rounds per iteration.

            This counters the effect of averaging multiple rounds to a single iteration measurement which
            would otherwise **reduce** the apparent variability by the square root of the number of rounds
            per iteration and conceal the true variability of a single round.

        .. note::
            The value is either set directly or calculated from the `measurements` parameter.

        :return: The standard deviation.
        """
        if self._stdev is None:
            if len(self._measurements) > 1:  # type: ignore  # validated in __init__
                self._stdev = float(
                    statistics.stdev(self._measurements)  # type: ignore  # validated in __init__
                        * sqrt(float(self.rounds))
                )
            else:
                self._stdev = float('nan')  # Standard deviation is NaN if only one measurement
        return self._stdev

    @property
    def relative_stdev(self) -> float:
        """Get the relative standard deviation.

        The relative standard deviation (RSD) is calculated as the standard deviation
        divided by the mean, expressed as a percentage.

        .. note::
            If the mean is zero, the relative standard deviation is defined as NaN.

        :return: The relative standard deviation.
        """
        if self._relative_stdev is None:
            if self.mean == 0.0:
                self._relative_stdev = float('nan')
            else:
                self._relative_stdev = 100 * abs(self.stdev / self.mean)
        return self._relative_stdev

    @property
    def drift_index(self) -> float:
        """Get the drift index.

        The drift index is the Pearson correlation coefficient between the measurement
        values and their sequential position indices (0, 1, 2, …, n−1).

        Range [-1.0, 1.0]. 0.0 indicates no monotonic trend. Positive values indicate
        measurements increasing over iterations (e.g., growing timing, heap pressure).
        Negative values indicate measurements settling over iterations. Does not detect
        periodic patterns; see :attr:`autocorrelation` for that.

        Degenerate case (all measurements identical): returns 0.0.

        .. note::
            The value is either set directly or calculated from the `measurements` property.

        :return float: The drift index.
        """
        if self._drift_index is None:
            data = self._measurements
            if data is None:
                raise SimpleBenchValueError(
                    'Cannot calculate drift index because measurements are not set',
                    tag=_StatsBlockErrorTag.INVALID_MEASUREMENTS_STATE,
                )
            try:
                self._drift_index = float(statistics.correlation(data, range(len(data))))
            except statistics.StatisticsError:
                self._drift_index = 0.0
        return self._drift_index

    @property
    def autocorrelation(self) -> float:
        """Get the lag-1 autocorrelation.

        The autocorrelation is the Pearson correlation coefficient between each
        measurement and the next (lag-1).

        Range [-1.0, 1.0]. Near 0.0 indicates statistically independent consecutive
        samples (ideal). Strong positive values indicate slow-moving environmental
        effects (thermal throttling, OS load). Strong negative values indicate an
        alternating fast/slow pattern (GC-induced oscillation, cache state cycling).

        Degenerate case (constant sequence): returns 0.0.

        .. note::
            The value is either set directly or calculated from the `measurements` property.

        :return float: The lag-1 autocorrelation.
        """
        if self._autocorrelation is None:
            data = self._measurements
            if data is None:
                raise SimpleBenchValueError(
                    'Cannot calculate autocorrelation because measurements are not set',
                    tag=_StatsBlockErrorTag.INVALID_MEASUREMENTS_STATE,
                )
            try:
                self._autocorrelation = float(statistics.correlation(data[:-1], data[1:]))
            except statistics.StatisticsError:
                self._autocorrelation = 0.0
        return self._autocorrelation

    @property
    def percentiles(self) -> Values:
        """Get the values for the percentiles.

        The percentiles are represented as a sorted Values instance containing 101 float values
        corresponding to the percentiles from 0 to 100.

        .. note::
            The value is either set directly or calculated from the `measurements` property.

        :return Values: The Values instance containing the percentiles.
        :raise SimpleBenchValueError: If percentiles cannot be calculated because measurements are not set
            and it was not set directly either.
        """
        if self._percentiles is None:
            self._percentiles = self._calculate_percentiles()
        return self._percentiles

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
                'Cannot calculate percentiles because measurements are not set',
                tag=_StatsBlockErrorTag.INVALID_MEASUREMENTS_STATE,
            )
        if len(data) == 1:
            data_value = float(data[0])  # type: ignore  # validated in __init__
            return Values([data_value] * 101)
        quantile_values = statistics.quantiles(data, n=102, method='inclusive')  # type: ignore
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
            backing_attr = f'_{attr}'
            if getattr(self, backing_attr, None) is None:
                unset_properties.append(attr)

        if unset_properties:
            raise SimpleBenchValueError(
                "Either the 'measurements' argument must be provided, or all of the following arguments must be set: "
                f'{", ".join(unset_properties)}',
                tag=_StatsBlockErrorTag.INVALID_STATS_BLOCK_ARGUMENTS,
            )

    def __getstate__(self) -> tuple[dict[str, Any] | None, tuple[Any, ...]]:
        """Prepare the object's state for pickling, prioritizing size.

        This method ensures that the pickled representation of the StatsBlock
        is compact. It achieves this by forcing the calculation of any lazy-evaluated
        statistical properties and then excluding any attributes that are not part of the
        public interface of the StatsBlock from the pickled state. Those excluded attributes
        can be recalculated upon unpickling on demand and do not need to be stored.

        This prioritizes a small pickled size and fast subsequent unpickling over
        preserving the lazy-evaluation state across serialization.

        :return: A state tuple for pickling.
        :rtype: tuple[dict[str, Any] | None, tuple[Any, ...]]
        """
        # Sweep all slot attributes to force calculation of any lazy properties.
        # and collect any public attribute values for pickling.
        # 'version' and 'type' are excluded as they are class constants not
        # instance attributes and can be inferred.
        public_attrs = dict(self._data_params())
        public_attrs.pop('type', None)
        public_attrs.pop('version', None)
        slot_values: list[Any] = []
        for slot in self.__slots__:
            attr_name = slot.lstrip('_')
            if attr_name in public_attrs:
                slot_values.append(getattr(self, attr_name))
            else:
                # For any attributes that are not part of the public interface, we append None to the slot values
                # to maintain the correct number of slot values for unpickling, but we do not actually need to
                # store their values.
                slot_values.append(None)
        # Build the state tuple for a __slots__ class. The first element is for
        # __dict__ (None in our case) and the second is a tuple of the slotted values.
        state = tuple(slot_values)
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
        for slot, value in zip(self.__slots__, slot_values, strict=True):
            # Use object.__setattr__ to bypass our immutable setters.
            object.__setattr__(self, slot, value)

    def __repr__(self) -> str:
        """Get the string representation of the StatsBlock instance.

        This is a custom implementation of __repr__ that constructs a string representation of the StatsBlock
        by including all of its properties in a key=value format. It accesses the properties via their getters,
        which will trigger any lazy calculations if they haven't been computed yet. This ensures that the
        string representation includes the actual values of all properties, even those that are lazily computed.

        It DOES NOT include the 'type' and 'version' properties in the string representation since they
        are fixed for this class and do not provide additional information about the instance.

        It also does not include 'measurements' in the string representation since they are only needed
        for calculating the statistical properties - which can be used to completely reconstruct the StatsBlock -
        and including them would make the string representation excessively long and less readable.

        :return: The string representation of the StatsBlock.
        """
        # Get the init parameters excluding 'type' and 'version' since they are fixed for this class
        init_params = dict(self._data_params())
        init_params.pop('type', None)
        init_params.pop('version', None)
        init_params.pop('measurements', None)

        # Build the key-value argument string. Accessing the properties via getattr
        # will trigger their lazy calculation if they haven't been computed yet.
        calling_args = ', '.join(f'{key}={getattr(self, key)!r}' for key in init_params)
        return f'{self.__class__.__name__}({calling_args})'

    def __hash__(self) -> int:
        """Get the hash of the StatsBlock instance.

        :return: The hash value.
        """
        return hash(self.hash_id)

    def __eq__(self, other: object) -> bool:
        """Check equality between two StatsBlock instances.

        :param other: The other object to compare.
        :return: True if equal, False otherwise.
        """
        if not isinstance(other, StatsBlock):
            return NotImplemented
        return self.hash_id == other.hash_id

    def __ne__(self, other: object) -> bool:
        """Check inequality between two StatsBlock instances.

        :param other: The other object to compare.
        :return: True if not equal, False otherwise.
        """
        if not isinstance(other, StatsBlock):
            return NotImplemented
        return self.hash_id != other.hash_id

    def __copy__(self) -> 'StatsBlock':
        """Return the same instance since StatsBlock is immutable."""
        return self

    def __deepcopy__(self, memo: dict[int, Any]) -> 'StatsBlock':
        """Return the same instance since StatsBlock is immutable."""
        return self
