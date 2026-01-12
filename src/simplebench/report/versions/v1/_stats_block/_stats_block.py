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
   dictionary that matches the JSON schema. This does not allow raw measurements to be
   provided; the statistical parameters must be provided directly in the dictionary.

The created instance and all values available via properties are immutable once created
and can be serialized back to a dictionary using the `to_dict` method.

The class also implements equality and hashing methods to allow comparison
and use in hash-based collections like sets and dictionaries. It also
implements size-optimized pickling support for serialization/deserialization.

The dictionary serialized representation matches the JSON schema for version 1 reports
and can be used for JSON serialization and deserialization.
"""

import statistics
from collections.abc import Mapping, Sequence
from copy import copy
from math import sqrt
from typing import Any, overload

from simplebench.exceptions import SimpleBenchValueError
from simplebench.report._base import BaseStatsBlock, JSONSchema
from simplebench.report._error_tags import _StatsBlockErrorTag
from simplebench.types._values._values import Values

from . import _validate
from ._stats_block_dict import ImmutableStatsBlockDict, StatsBlockData
from ._stats_block_schema import StatsBlockSchema


class StatsBlock(BaseStatsBlock):
    """Class representing a stats summary for V1 reports.

    This class represents a stats block information in a JSON report.
    It implements validation and serialization/deserialization methods to and from dictionaries
    for the following JSON Schema version:

    https://raw.githubusercontent.com/JerilynFranz/python-simplebench/main/schemas/v1/stats-block.json

    :hash_id str: The hash identifier for the stats block.
    :param str name: The name of the stats block.
    :param str description: The description of the stats block.
    :param str semantic_type: The semantic type of the stats block.
    :param str unit: The unit of measurement for the stats block.
    :param float scale: The scale factor for the stats block.
    :param int iterations: The number of iterations measured for the stats block.
    :param int rounds: The number of rounds in each iteration measured.
    :param float mean: The mean value of the stats block.
    :param float median: The median value of the stats block.
    :param float minimum: The minimum value of the stats block.
    :param float maximum: The maximum value of the stats block.
    :param float stdev: The standard deviation of the stats block.
    :param float relative_stdev: The relative standard deviation of the stats block.
    :param Values percentiles: The list of percentiles for the stats block as a `Values` instance.
    :param Sequence[float] | Values measurements: A list of raw measurements for initializing the stats block.
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

    _init_params_cache: dict[str, Any] = {}
    """Cache for the constructor parameters of the StatsBlock class."""

    @classmethod
    def _stats_block_params(cls) -> dict[str, Any]:
        """Get the constructor parameters for the StatsBlock class.

        The parameters are cached after the first call for performance.

        :return dict[str, Any]: A dictionary of constructor parameter names and types.
        """
        if not cls._init_params_cache:
            params = cls.init_params(StatsBlockData)
            params.pop('type', None)
            params.pop('version', None)
            cls._init_params_cache = params

        return cls._init_params_cache

    _DERIVABLE_PROPERTIES = (
        'iterations',
        'mean',
        'median',
        'minimum',
        'maximum',
        'stdev',
        'relative_stdev',
        'percentiles',
    )

    __slots__ = (
        '_hash_id',
        '_name',
        '_description',
        '_semantic_type',
        '_unit',
        '_scale',
        '_iterations',
        '_rounds',
        '_timer',
        '_mean',
        '_median',
        '_minimum',
        '_maximum',
        '_stdev',
        '_relative_stdev',
        '_percentiles',
        '_measurements',
        '_to_dict_cache',
    )

    @overload
    def __init__(
        self,
        *,
        hash_id: str,
        name: str,
        semantic_type: str,
        description: str = '',
        unit: str,
        scale: float,
        rounds: int,
        timer: str,
        measurements: Sequence[float] | Values,
    ) -> None:
        """Initialize a StatsBlock by calculating statistics from raw measurements.

        :param str hash_id: The hash identifier for the stats block.
        :param str name: The name of the stats block.
        :param str description: The description of the stats block.
        :param str semantic_type: The semantic type of the stats block.
        :param str unit: The unit of measurement for the stats block.
        :param float scale: The scale factor for the stats block.
        :param int rounds: The number of rounds in the stats block.
        :param str timer: The timer used for measurements.
        :param Sequence[float] | Values | None measurements: The list of raw measurements for the stats block.
        """

    @overload
    def __init__(
        self,
        *,
        hash_id: str,
        name: str,
        description: str = '',
        semantic_type: str,
        unit: str,
        scale: float,
        iterations: int,
        rounds: int,
        timer: str,
        mean: float,
        median: float,
        minimum: float,
        maximum: float,
        stdev: float,
        relative_stdev: float,
        percentiles: Sequence[float],
    ) -> None:
        """Initialize a StatsBlock with pre-calculated statistical values.

        :param str name: The name of the stats block.
        :param str description: The description of the stats block.
        :param str semantic_type: The semantic type of the stats block.
        :param str unit: The unit of measurement for the stats block.
        :param float scale: The scale factor for the stats block.
        :param int | None iterations: The number of iterations in the stats block.
        :param int rounds: The number of rounds in the stats block.
        :param str timer: The timer used for measurements.
        :param float | None mean: The mean value of the stats block.
        :param float | None median: The median value of the stats block.
        :param float | None minimum: The minimum value of the stats block.
        :param float | None maximum: The maximum value of the stats block.
        :param float | None stdev: The standard deviation of the stats block.
        :param float | None relative_stdev: The relative standard deviation of the stats block.
        :param Sequence[float] | None percentiles: The list of percentiles for the stats block.
        """

    def __init__(
        self,
        *,
        hash_id: str,
        name: str,
        description: str = '',
        semantic_type: str,
        unit: str,
        scale: float,
        iterations: int | None = None,
        rounds: int,
        timer: str = '',
        mean: float | None = None,
        median: float | None = None,
        minimum: float | None = None,
        maximum: float | None = None,
        stdev: float | None = None,
        relative_stdev: float | None = None,
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
            - percentiles

        :param str hash_id: The hash identifier for the stats block.
        :param str name: The name of the stats block.
        :param str description: The description.
        :param str semantic_type: The semantic type of the stats block.
        :param str unit: The unit of measurement.
        :param float scale: The scale factor.
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

        self._name: str = _validate.name(name)
        """The name of the stats block."""
        self._description: str = _validate.description(description)
        """The description of the stats block."""
        self._semantic_type: str = _validate.semantic_type(semantic_type)
        """The semantic type of the stats block."""
        self._unit: str = _validate.unit(unit)
        """The unit of measurement."""
        self._scale: float = _validate.scale(scale)
        """The scale factor."""
        self._rounds: int = _validate.rounds(rounds)
        """The number of rounds per iteration."""
        self._timer: str | None = _validate.timer(timer)
        """The timer used for measurements."""
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
        self._percentiles: Values | None = _validate.percentiles(percentiles, self._measurements)
        """The list of percentiles."""

        self._to_dict_cache: ImmutableStatsBlockDict | None = None
        """Cache for the dictionary representation of the object."""

        self._validate_stats_block_consistency()

    @classmethod
    def from_dict(cls, data: Mapping[str, Any]) -> 'StatsBlock':
        """Create a StatsBlock object from a dictionary representation
        that conforms to the version 1 :class:`StatsBlockSchema`.

        This method validates the input dictionary to ensure it matches
        the expected schema and types before creating the StatsBlock instance.

        It cannot be instantiated using raw measurements via this method;
        the statistical parameters must be provided directly in the dictionary.

        :param Any data: A dictionary representation of a StatsBlock.
        :return StatsBlock: A StatsBlock object created from the dictionary.
        :raise SimpleBenchTypeError: If any parameter in the dictionary is of an invalid type.
        :raise SimpleBenchValueError: If any parameter in the dictionary has an invalid value.
        """
        allowed_keys = cls._stats_block_params()

        kwargs = cls.import_data(
            data=data,
            allowed_fields=allowed_keys,
            skip_fields={'version', 'type'},
            optional_fields={'description', 'version', 'type'},
            defaults={'description': '', 'version': cls.VERSION, 'type': cls.TYPE},
            match_on={'version': cls.VERSION, 'type': cls.TYPE},
            process_as={'percentiles': Values},
        )
        return cls(**kwargs)

    def to_dict(self) -> ImmutableStatsBlockDict:
        """Convert the StatsBlock object to an immutable mapping conforming to the version 1 :class:`StatsBlockSchema`.

        The exported mapping includes all properties of the StatsBlock and
        expands any nested objects by calling their own `to_dict` methods if available.

        It is the canonical representation of the StatsBlock suitable for serialization to JSON
        and deserialization back into a StatsBlock object.

        :return StatsBlockDict: A dictionary representation of the StatsBlock.
        """
        if self._to_dict_cache is None:
            self._to_dict_cache = self._to_dict_helper(ImmutableStatsBlockDict)
        return self._to_dict_cache

    @property
    def hash_id(self) -> str:
        """Get the hash identifier of the stats block.

        :return: The hash identifier of the stats block.
        """
        if self._hash_id is None:
            self._hash_id = self._hash_id_helper(StatsBlockData)
        return self._hash_id

    @property
    def name(self) -> str:
        """Get the name of the stats block.

        :return: The name of the stats block.
        """
        return self._name

    @property
    def description(self) -> str:
        """Get the description of the stats block.

        :return: The description of the stats block.
        """
        return self._description

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

    @property
    def unit(self) -> str:
        """Get the unit of measurement.

        :return: The unit of measurement.
        """
        return self._unit

    @property
    def scale(self) -> float:
        """Get the scale factor.

        :return: The scale factor.
        :raise SimpleBenchTypeError: If scale is not a float.
        """
        return self._scale

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
            self._iterations = len(self._measurements)  # type: ignore[reportArgumentType]  # validated in __init__
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
            self._mean = float(statistics.mean(self._measurements))  # type: ignore[reportArgumentType]  # validated in __init__
        return self._mean

    @property
    def median(self) -> float:
        """Get the statistical median value.

        .. note::
            The value is either set directly or calculated from the `measurements` property.

        :return float: The median value.
        """
        if self._median is None:
            self._median = float(statistics.median(self._measurements))  # type: ignore[reportArgumentType]  # validated in __init__
        return self._median

    @property
    def minimum(self) -> float:
        """Get the minimum value.

        .. note::
            The value is either set directly or calculated from the `measurements` property.

        :return: The minimum value.
        """
        if self._minimum is None:
            self._minimum = float(min(self._measurements))  # type: ignore[reportArgumentType]  # validated in __init__
        return self._minimum

    @property
    def maximum(self) -> float:
        """Get the maximum value.

        .. note::
            The value is either set directly or calculated from the `measurements` property.

        :return: The maximum value.
        """
        if self._maximum is None:
            self._maximum = float(max(self._measurements))  # type: ignore[reportArgumentType]  # validated in __init__
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
            if len(self._measurements) > 1:  # type: ignore[reportArgumentType]  # validated in __init__
                self._stdev = float(
                    statistics.stdev(self._measurements)  # type: ignore[reportArgumentType]  # validated in __init__
                    * sqrt(self.rounds)
                )
            else:
                self._stdev = 0.0  # Standard deviation is 0 if only one measurement
        return self._stdev

    @property
    def relative_stdev(self) -> float:
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
        if self._relative_stdev is None:
            if self.mean == 0.0:
                self._relative_stdev = 1e9 if self.stdev else 0.0
            else:
                self._relative_stdev = abs(self.stdev / self.mean * 100)
        return self._relative_stdev

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
            backing_attr = f'_{attr}'
            if getattr(self, backing_attr, None) is None:
                unset_properties.append(attr)

        if unset_properties:
            raise SimpleBenchValueError(
                "Either the 'measurements' argument must be provided, or all of the following arguments must be set: "
                f'{", ".join(unset_properties)}',
                tag=_StatsBlockErrorTag.INVALID_STATS_BLOCK_ARGUMENTS,
            )

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

        return hash(self) == hash(other)

    def __hash__(self) -> int:
        """Compute the hash of the StatsBlock instance.

        The hash is computed from the hash_id.

        .. note::
            Triggers the lazy eval properties to be evaluated if they have not been already.
            This ensures that the hash is based on the actual values of the properties.

            This can be expensive the first time it is called if many properties
            need to be calculated from many measurements. This is unavoidable
            since the hash must reflect the actual state of the object.

        :return int: The hash value of the StatsBlock instance.
        """
        return hash(self.hash_id)

    def __repr__(self) -> str:
        """Get the string representation of the StatsBlock instance.

        The representation is a string that can be used to recreate the object.
        It triggers the lazy evaluation of any properties that have not been calculated yet.

        :return str: The string representation of the StatsBlock.
        """
        # Get the init parameters excluding 'type' and 'version'
        init_params = self._stats_block_params()

        # Build the key-value argument string. Accessing the properties via getattr
        # will trigger their lazy calculation if they haven't been computed yet.
        calling_args = ', '.join(f'{key}={getattr(self, key)!r}' for key in init_params)
        return f'{self.__class__.__name__}({calling_args})'

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
        public_attrs = self._stats_block_params()
        slot_values: list[Any] = []
        for slot in self.__slots__:
            attr_name = slot.lstrip('_')
            if attr_name in public_attrs:
                slot_values.append(getattr(self, attr_name))
            else:
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

    def __deepcopy__(self, memo: dict[int, Any]) -> 'StatsBlock':
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
