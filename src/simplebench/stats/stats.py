# -*- coding: utf-8 -*-
"""Base benchmark statistics class."""
from __future__ import annotations
from math import isclose, sqrt
import statistics
from typing import Any, Sequence

from .exceptions.stats import StatsErrorTag, StatsSummaryErrorTag
from ..exceptions import SimpleBenchKeyError, SimpleBenchTypeError
from ..si_units import si_unit_base, si_scale_to_unit
from ..validators import (validate_non_blank_string, validate_float, validate_non_negative_float,
                          validate_positive_float, validate_sequence_of_numbers,
                          validate_positive_int)


class Stats:
    '''Generic container for statistics on a benchmark.

    Attributes:
        unit (str): The unit of measurement for the benchmark (e.g., "ops/s"). (read only)
        scale (float): The scale factor for the interval (e.g. 1 for seconds). (read only)
        rounds (int): The number of rounds each data point represents. (read only)
        data: (tuple[float | int, ...]) = Tuple of data points. (read only)
        mean (float): The mean operations per time interval. (read only)
        median (float): The median operations per time interval. (read only)
        minimum (float): The minimum operations per time interval. (read only)
        maximum (float): The maximum operations per time interval. (read only)
        standard_deviation (float): The standard deviation of operations per time interval. (read only)
        adjusted_standard_deviation (float): The standard deviation adjusted for the number of rounds. (read only)
        relative_standard_deviation (float): The relative standard deviation of ops per time interval. (read only)
        adjusted_relative_standard_deviation (float): The adjusted relative standard deviation of ops per
            time interval. (read only)
        percentiles (tuple[float, ...]): Percentiles of operations per time interval. (read only)
    '''
    __slots__ = ('_unit', '_scale', '_rounds', '_data', '_percentiles', '_mean', '_median',
                 '_minimum', '_maximum', '_standard_deviation', '_adjusted_standard_deviation',
                 '_relative_standard_deviation', '_adjusted_relative_standard_deviation',
                 '_statistics_as_dict', '_statistics_and_data_as_dict')

    def __init__(self, *, unit: str, scale: float, data: Sequence[int | float], rounds: int = 1) -> None:
        """Initialize the Stats object.

        Args:
            unit (str): The unit of measurement for the benchmark (e.g., "ops/s").
            scale (float): The scale factor for the interval (e.g. 1 for seconds).
            data (Sequence[int | float]): Sequence of data points.
            rounds (int, default=1): The number of rounds each data point represents.
        Raises:
            SimpleBenchTypeError: If any of the arguments are of the wrong type.
            SimpleBenchValueError: If any of the arguments have invalid values.
        """
        self._unit: str = validate_non_blank_string(
                                unit, 'unit',
                                StatsErrorTag.INVALID_UNIT_ARG_TYPE,
                                StatsErrorTag.INVALID_UNIT_ARG_VALUE)
        self._scale: float = validate_positive_float(
                                scale, 'scale',
                                StatsErrorTag.INVALID_SCALE_ARG_TYPE,
                                StatsErrorTag.INVALID_SCALE_ARG_VALUE)
        self._rounds: int = validate_positive_int(
                                rounds, 'rounds',
                                StatsErrorTag.INVALID_ROUNDS_ARG_TYPE,
                                StatsErrorTag.INVALID_ROUNDS_ARG_VALUE)
        # data is left unsorted to allow for time series data to be preserved
        self._data: tuple[int | float, ...] = tuple(validate_sequence_of_numbers(
                                            value=data,
                                            field_name='data',
                                            allow_empty=False,
                                            type_tag=StatsErrorTag.INVALID_DATA_ARG_TYPE,
                                            value_tag=StatsErrorTag.INVALID_DATA_ARG_ITEM_TYPE))
        self._percentiles: tuple[float, ...] | None = None
        self._mean: float | None = None
        self._median: float | None = None
        self._minimum: float | None = None
        self._maximum: float | None = None
        self._standard_deviation: float | None = None
        self._adjusted_standard_deviation: float | None = None
        self._relative_standard_deviation: float | None = None
        self._adjusted_relative_standard_deviation: float | None = None
        self._statistics_as_dict: dict[str, str | float | dict[int, float] | list[int | float]] | None = None
        self._statistics_and_data_as_dict: dict[str, str | float | dict[int, float] | list[int | float]] | None = None

    @property
    def unit(self) -> str:
        '''The unit of the data.'''
        return self._unit

    @property
    def scale(self) -> float:
        '''The scale of the data.'''
        return self._scale

    @property
    def rounds(self) -> int:
        '''The number of rounds each data point represents.'''
        return self._rounds

    @property
    def data(self) -> tuple[int | float, ...]:
        '''The data points.'''
        return self._data

    @property
    def mean(self) -> float:
        '''The mean of the data.'''
        if self._mean is None:
            self._mean = statistics.mean(self.data) if self.data else 0.0
        return self._mean

    @property
    def median(self) -> float:
        '''The median of the data.'''
        if self._median is None:
            self._median = statistics.median(self.data) if self.data else 0.0
        return self._median

    @property
    def minimum(self) -> float:
        '''The minimum of the data.'''
        if self._minimum is None:
            self._minimum = float(min(self.data)) if self.data else 0.0
        return self._minimum

    @property
    def maximum(self) -> float:
        '''The maximum of the data.'''
        if self._maximum is None:
            self._maximum = float(max(self.data)) if self.data else 0.0
        return self._maximum

    @property
    def standard_deviation(self) -> float:
        '''The standard deviation of the data.'''
        if self._standard_deviation is None:
            self._standard_deviation = statistics.stdev(self.data) if len(self.data) > 1 else 0.0
        return self._standard_deviation

    @property
    def adjusted_standard_deviation(self) -> float:
        '''The standard deviation adjusted for the number of rounds.

        This metric "un-suppresses" the variability that is reduced by averaging
        across multiple rounds. It is calculated by multiplying the standard
        deviation by the square root of the number of rounds.
        '''
        if self._adjusted_standard_deviation is None:
            self._adjusted_standard_deviation = self.standard_deviation * sqrt(self.rounds)
        return self._adjusted_standard_deviation

    @property
    def relative_standard_deviation(self) -> float:
        '''The relative standard deviation of the data.'''
        if self._relative_standard_deviation is None:
            self._relative_standard_deviation = abs(self.standard_deviation / self.mean * 100) if self.mean else 0.0
        return self._relative_standard_deviation

    @property
    def adjusted_relative_standard_deviation(self) -> float:
        '''The adjusted relative standard deviation of the data.'''
        if self._adjusted_relative_standard_deviation is None:
            self._adjusted_relative_standard_deviation = abs(
                self.adjusted_standard_deviation / self.mean * 100) if self.mean else 0.0
        return self._adjusted_relative_standard_deviation

    @property
    def percentiles(self) -> tuple[float, ...]:
        '''Percentiles of the data.

        Returns the 0th through 100th percentiles of the data as an immutable tuple.
        '''
        if self._percentiles is None:
            self._percentiles = self._calculate_percentiles()
        return self._percentiles

    def _calculate_percentiles(self) -> tuple[float, ...]:
        """Helper to calculate percentiles.

        Note:

            statistics.quantiles with n=102 and method='inclusive' is used
            to calculate the percentiles from 0 to 100 inclusive (it generates 101
            cut points, which correspond to percentiles 0 through 100).

        Returns:
            A tuple of percentiles keyed positionally by percent from 0 to 100.
        """
        percentiles_n: list[int] = list(range(0, 101))
        if len(self.data) == 1:
            return tuple(float(self.data[0]) for _ in percentiles_n)
        quantile_values = statistics.quantiles(self.data, n=102, method='inclusive')
        return tuple(quantile_values)

    @property
    def as_dict(self) -> dict[str, str | float | dict[int, float] | tuple[int | float, ...]]:
        '''Returns the statistics and data as a JSON-serializable dictionary.

        This includes all the statistics as well as the raw data points.

        The data values are scaled according to the scale factor to provide
        human-readable values using the base unit rather than the scaled unit.

        The unit is normalized to its SI base unit representation. (e.g., "ms" becomes "s")

        The dictionary is mutability-safe as all data is either a primitive or a copy.

        Returns:
            A dictionary containing the statistics and the scaled data points.
        '''
        # Immutability is preserved because all values are primitives or copies already
        stats = self.stats_summary.as_dict
        stats['type'] = f'{self.__class__.__name__}:statistics'
        stats['data'] = tuple(value / self.scale for value in self.data)
        return stats

    @property
    def stats_summary(self) -> StatsSummary:
        '''Returns a StatsSummary object created from this Stats object.

        Returns:
            A StatsSummary object containing the same statistics as this Stats object.
        '''
        return StatsSummary.from_stats(self)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> Stats:
        """Construct a Stats object from a dictionary.

        Example:
            stats_dict = {
                "unit": "ops/s",
                "scale": 1,
                "data": [1000, 2000, 1500, 3000, 2500]
            }
            stats = Stats.from_dict(stats_dict)
            print(stats.mean)  # Output: 2000.0

        Args:
            data (dict): A dictionary containing the stats data. Must contain 'data' key with a non-empty
                sequence of data points consisting of integers or floats.

        Returns:
            Stats: A Stats object constructed from the provided dictionary.

        Raises:
            SimpleBenchTypeError: If the data, unit, or scale arguments are of the wrong type.
            SimpleBenchKeyError: If the data dictionary does not contain a 'unit' key and
                no unit argument is provided.
            SimpleBenchValueError: If the data dictionary does not contain a non-empty 'data' key
                with at least one data point, if the scale argument is not greater than zero,
                or if the unit argument is an empty string
        """
        if not isinstance(data, dict):
            raise SimpleBenchTypeError('The data argument must be a dictionary.',
                                       tag=StatsErrorTag.FROM_DICT_INVALID_DATA_ARG_TYPE)
        if 'unit' not in data:
            raise SimpleBenchKeyError('The data dictionary is missing the required "unit" key.',
                                      tag=StatsErrorTag.FROM_DICT_MISSING_UNIT_KEY)
        if 'scale' not in data:
            raise SimpleBenchKeyError('The data dictionary is missing the required "scale" key.',
                                      tag=StatsErrorTag.FROM_DICT_MISSING_SCALE_KEY)
        if 'rounds' not in data:
            raise SimpleBenchKeyError('The data dictionary is missing the required "rounds" key.',
                                      tag=StatsErrorTag.FROM_DICT_MISSING_ROUNDS_KEY)
        if 'data' not in data:
            raise SimpleBenchKeyError('The data dictionary is missing the required "data" key.',
                                      tag=StatsErrorTag.FROM_DICT_MISSING_DATA_KEY)

        return cls(unit=data['unit'],
                   scale=data['scale'],
                   rounds=data['rounds'],
                   data=data['data'])  # type: ignore[arg-type]

    def __eq__(self, other: object) -> bool:
        """Compare two Stats objects for equality.

        Equality is based on stats statistics and not on object identity.

        It handles scale differences between two Stats objects and compares
        the statistics accordingly using an appropriate tolerance for floating-point comparisons.

        It also verifies that the units are equivalent when converted to their SI base units.

        It does not consider the raw data points in the comparison as they will differ
        between a basic Stats object and a StatsSummary object derived from it.

        Args:
            other (object): The other object to compare against.

        Returns:
            bool: True if the objects are considered equal, False otherwise.

        Raises:
            SimpleBenchValueError: If either Stats object has a scale of zero.
        """
        if not isinstance(other, (Stats, StatsSummary)):
            return NotImplemented

        # this handles scale differences between two Stats objects
        self_base_unit: str = si_unit_base(self.unit)
        other_base_unit: str = si_unit_base(other.unit)
        if self_base_unit != other_base_unit:
            return False

        scale_by: float = si_scale_to_unit(base_unit=self_base_unit,
                                           current_unit=other.unit,
                                           target_unit=self.unit)
        relative_scale: float = self.scale / other.scale

        if self.rounds != other.rounds:
            return False

        if not isclose(scale_by, relative_scale):
            return False

        if not (isclose(self.mean, other.mean / relative_scale) and
                isclose(self.median,  other.median / relative_scale) and
                isclose(self.minimum, other.minimum / relative_scale) and
                isclose(self.maximum, other.maximum / relative_scale) and
                isclose(self.standard_deviation, other.standard_deviation / relative_scale) and
                isclose(self.relative_standard_deviation, other.relative_standard_deviation)):
            return False

        if len(self.percentiles) != len(other.percentiles):
            return False

        for self_pct, other_pct in zip(self.percentiles, other.percentiles):
            if not isclose(self_pct, other_pct / relative_scale):
                return False

        return si_unit_base(self.unit) == si_unit_base(other.unit)

    def __repr__(self) -> str:
        return (f"{self.__class__.__name__}(unit='{self.unit}', scale={self.scale}, rounds={self.rounds}, "
                f"data=[{', '.join(str(d) for d in self.data)}])")


class StatsSummary:
    '''Container for summary statistics of a benchmark, exclusive of raw data points.

    This is a lightweight, data-only version of the Stats class, suitable for
    serialization or reporting when raw data points are not needed.

    Attributes:
        unit (str): The unit of measurement for the benchmark (e.g., "ops/s"). (read only)
        scale (float): The scale factor for the interval (e.g. 1 for seconds). (read only)
        rounds (int): The number of rounds each data point represents. (read only)
        mean (float): The mean operations per time interval. (read only)
        median (float): The median operations per time interval. (read only)
        minimum (float): The minimum operations per time interval. (read only)
        maximum (float): The maximum operations per time interval. (read only)
        standard_deviation (float): The standard deviation of operations per time interval. (read only)
        relative_standard_deviation (float): The relative standard deviation of ops per time interval. (read only)
        percentiles (tuple[float, ...]): Percentiles of operations per time interval. (read only)
        data (tuple[int | float, ...]): Always an empty tuple as StatsSummary does not contain raw data points.
            (read only)
    '''
    __slots__ = ('_unit', '_scale', '_rounds', '_mean', '_median', '_minimum', '_maximum',
                 '_standard_deviation', '_relative_standard_deviation', '_percentiles',
                 '_adjusted_standard_deviation', '_adjusted_relative_standard_deviation',
                 '_statistics_as_dict')

    def __init__(self,  # pylint: disable=too-many-arguments
                 *,
                 unit: str,
                 scale: float,
                 rounds: int,
                 mean: float,
                 median: float,
                 minimum: float,
                 maximum: float,
                 standard_deviation: float,
                 relative_standard_deviation: float,
                 percentiles: tuple[float, ...]):
        """Initialize the StatsSummary object.

        Args:
            unit (str): The unit of measurement for the data (e.g., "ops/s").
            scale (float): The scale factor the data (e.g. 1.0 for seconds).
            rounds (int): The number of rounds each data point represents.
            mean (float): The mean data point.
            median (float): The median data point.
            minimum (float): The minimum data point.
            maximum (float): The maximum data point.
            standard_deviation (float): The standard deviation of data.
            relative_standard_deviation (float): The relative standard deviation of data.
            percentiles (tuple[float, ...]): Percentiles of data.
        Raises:
            SimpleBenchTypeError: If any of the arguments are of the wrong type.
            SimpleBenchValueError: If any of the arguments have invalid values.
        """
        self._unit = validate_non_blank_string(
                        unit, 'unit',
                        StatsSummaryErrorTag.INVALID_UNIT_ARG_TYPE,
                        StatsSummaryErrorTag.INVALID_UNIT_ARG_VALUE)
        self._scale = validate_positive_float(
                        scale, 'scale',
                        StatsSummaryErrorTag.INVALID_SCALE_ARG_TYPE,
                        StatsSummaryErrorTag.INVALID_SCALE_ARG_VALUE)
        self._rounds = validate_positive_int(
                        rounds, 'rounds',
                        StatsSummaryErrorTag.INVALID_ROUNDS_ARG_TYPE,
                        StatsSummaryErrorTag.INVALID_ROUNDS_ARG_VALUE)
        self._mean = validate_float(
                        mean, 'mean',
                        StatsSummaryErrorTag.INVALID_MEAN_ARG_TYPE)
        self._median = validate_float(
                        median, 'median',
                        StatsSummaryErrorTag.INVALID_MEDIAN_ARG_TYPE)
        self._minimum = validate_float(
                        minimum, 'minimum',
                        StatsSummaryErrorTag.INVALID_MINIMUM_ARG_TYPE)
        self._maximum = validate_float(
                        maximum, 'maximum',
                        StatsSummaryErrorTag.INVALID_MAXIMUM_ARG_TYPE)
        self._standard_deviation = validate_non_negative_float(
                        standard_deviation, 'standard_deviation',
                        StatsSummaryErrorTag.INVALID_STANDARD_DEVIATION_ARG_TYPE,
                        StatsSummaryErrorTag.INVALID_STANDARD_DEVIATION_ARG_VALUE)
        self._relative_standard_deviation = validate_non_negative_float(
                        relative_standard_deviation, 'relative_standard_deviation',
                        StatsSummaryErrorTag.INVALID_RELATIVE_STANDARD_DEVIATION_ARG_TYPE,
                        StatsSummaryErrorTag.INVALID_RELATIVE_STANDARD_DEVIATION_ARG_VALUE)
        self._percentiles = tuple(validate_sequence_of_numbers(
                        percentiles, 'percentiles',
                        allow_empty=False,
                        type_tag=StatsSummaryErrorTag.INVALID_PERCENTILES_ARG_TYPE,
                        value_tag=StatsSummaryErrorTag.INVALID_PERCENTILES_ARG_VALUE))
        self._adjusted_standard_deviation: float | None = None
        self._adjusted_relative_standard_deviation: float | None = None
        self._statistics_as_dict = None

    @property
    def unit(self) -> str:
        '''The unit of the data.'''
        return self._unit

    @property
    def scale(self) -> float:
        '''The scale of the data.'''
        return self._scale

    @property
    def rounds(self) -> int:
        '''The number of rounds each data point represents.'''
        return self._rounds

    @property
    def mean(self) -> float:
        '''The mean of the data.'''
        return self._mean

    @property
    def median(self) -> float:
        '''The median of the data.'''
        return self._median

    @property
    def minimum(self) -> float:
        '''The minimum of the data.'''
        return self._minimum

    @property
    def maximum(self) -> float:
        '''The maximum of the data.'''
        return self._maximum

    @property
    def standard_deviation(self) -> float:
        '''The standard deviation of the data.'''
        return self._standard_deviation

    @property
    def adjusted_standard_deviation(self) -> float:
        '''The standard deviation adjusted for the number of rounds.'''
        if self._adjusted_standard_deviation is None:
            self._adjusted_standard_deviation = self.standard_deviation * sqrt(self.rounds)
        return self._adjusted_standard_deviation

    @property
    def relative_standard_deviation(self) -> float:
        '''The relative standard deviation of the data.'''
        return self._relative_standard_deviation

    @property
    def adjusted_relative_standard_deviation(self) -> float:
        '''The adjusted relative standard deviation of the data.'''
        if self._adjusted_relative_standard_deviation is None:
            self._adjusted_relative_standard_deviation = abs(
                self.adjusted_standard_deviation / self.mean * 100) if self.mean else 0.0
        return self._adjusted_relative_standard_deviation

    @property
    def percentiles(self) -> tuple[float, ...]:
        '''Percentiles of the data.'''
        return self._percentiles

    @property
    def data(self) -> tuple[int | float, ...]:
        '''The data points.

        This is always an empty tuple as a StatsSummary does not contain raw data points.
        '''
        return tuple()

    def __eq__(self, other: object) -> bool:
        """Compare this StatsSummary to another Stats or StatsSummary object.

        Equality is based on stats statistics and not on object identity.

        It handles scale differences between two objects and compares
        the statistics accordingly using an appropriate tolerance for floating-point comparisons.

        It also verifies that the units are equivalent when converted to their SI base units.

        Args:
            other (object): The other object to compare against.

        Returns:
            bool: True if the objects are considered equal, False otherwise.
        """
        if not isinstance(other, (Stats, StatsSummary)):
            return NotImplemented

        # this handles scale differences between two Stats objects
        self_base_unit: str = si_unit_base(self.unit)
        other_base_unit: str = si_unit_base(other.unit)
        if self_base_unit != other_base_unit:
            return False

        scale_by: float = si_scale_to_unit(base_unit=self_base_unit,
                                           current_unit=other.unit,
                                           target_unit=self.unit)
        relative_scale: float = self.scale / other.scale

        if self.rounds != other.rounds:
            return False

        if not isclose(scale_by, relative_scale):
            return False

        if not (isclose(self.mean, other.mean / relative_scale) and
                isclose(self.median,  other.median / relative_scale) and
                isclose(self.minimum, other.minimum / relative_scale) and
                isclose(self.maximum, other.maximum / relative_scale) and
                isclose(self.standard_deviation, other.standard_deviation / relative_scale) and
                isclose(self.relative_standard_deviation, other.relative_standard_deviation)):
            return False

        if len(self.percentiles) != len(other.percentiles):
            return False

        for self_pct, other_pct in zip(self.percentiles, other.percentiles):
            if not isclose(self_pct, other_pct / relative_scale):
                return False

        return True

    @classmethod
    def from_stats(cls, stats: Stats) -> StatsSummary:
        """Construct a new StatsSummary object from a Stats object.

        Args:
            stats (Stats): The Stats object to derive the summary from.

        Returns:
            StatsSummary: A new StatsSummary object containing the same statistics as the provided Stats object.

        Raises:
            SimpleBenchTypeError: If the stats argument is not a Stats object.
        """
        if not isinstance(stats, Stats):
            raise SimpleBenchTypeError(
                "The stats argument must be a Stats object.",
                tag=StatsSummaryErrorTag.FROM_STATS_INVALID_STATS_ARG_TYPE)
        return cls(
            unit=stats.unit,
            scale=stats.scale,
            rounds=stats.rounds,
            mean=stats.mean,
            median=stats.median,
            minimum=stats.minimum,
            maximum=stats.maximum,
            standard_deviation=stats.standard_deviation,
            relative_standard_deviation=stats.relative_standard_deviation,
            percentiles=stats.percentiles
        )

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> StatsSummary:
        """Construct a StatsSummary object from a dictionary.

        Example:
            stats_summary_dict = {
                "unit": "ops/s",
                "scale": 1.0,
                "rounds": 1,
                "mean": 2000.0,
                "median": 2000.0,
                "minimum": 1000.0,
                "maximum": 3000.0,
                "standard_deviation": 790.5694150420949,
                "relative_standard_deviation": 39.52847075252201,
                "percentiles": [1000.0, 1300.0, 1600.0, 1900.0, 2200.0,
                                2500.0, 2800.0, 3000.0, 3000.0]
            }
            stats_summary = StatsSummary.from_dict(stats_summary_dict)
            print(stats_summary.mean)  # Output: 2000.0

        Args:
            data (dict): A dictionary containing the stats data. Must contain 'data' key with a non-empty
                sequence of data points consisting of integers or floats.

        Returns:
            StatsSummary: A StatsSummary object constructed from the provided dictionary.

        Raises:
            SimpleBenchTypeError: If the data, unit, or scale arguments are of the wrong type.
            SimpleBenchKeyError: If the data dictionary does not contain a 'unit' key and
                no unit argument is provided.
            SimpleBenchValueError: If the data dictionary does not contain a non-empty 'data' key
                with at least one data point, if the scale argument is not greater than zero,
                or if the unit argument is an empty string
        """
        if not isinstance(data, dict):
            raise SimpleBenchTypeError('The data argument must be a dictionary.',
                                       tag=StatsErrorTag.FROM_DICT_INVALID_DATA_ARG_TYPE)

        required_keys = [
            'unit', 'scale', 'rounds', 'mean', 'median', 'minimum', 'maximum',
            'standard_deviation', 'relative_standard_deviation', 'percentiles'
        ]
        keys_for_construction = {}
        for key in required_keys:
            if key not in data:
                raise SimpleBenchKeyError(f"The data dictionary is missing the required '{key}' key.",
                                          tag=StatsSummaryErrorTag.FROM_DICT_MISSING_KEY)
            keys_for_construction[key] = data[key]
        return cls(**keys_for_construction)  # type: ignore[arg-type]  # pylint: disable=missing-kwoa

    @property
    def as_dict(self) -> dict[str, str | float | dict[int, float] | tuple[int | float, ...]]:
        '''Returns the statistics as a JSON-serializable dictionary.

        The data values are scaled according to the scale factor to provide
        human-readable values using the base unit rather than the scaled unit.

        The unit is converted to its SI base unit representation. (e.g., "ms" becomes "s")

        This does not include raw data points, only the statistics.

        The dictionary is mutability-safe as all data is either a primitive or a copy.

        Returns:
            A dictionary containing the statistics.
        '''
        # Immutability is preserved because all values are primitives or copies already
        return {
            'type': f'{self.__class__.__name__}',
            'unit': si_unit_base(self.unit),
            'scale': 1.0,
            'rounds': self.rounds,
            'mean': self.mean / self.scale,
            'median': self.median / self.scale,
            'minimum': self.minimum / self.scale,
            'maximum': self.maximum / self.scale,
            'standard_deviation': self.standard_deviation / self.scale,
            'adjusted_standard_deviation': self.adjusted_standard_deviation / self.scale,
            'relative_standard_deviation': self.relative_standard_deviation,
            'percentiles': tuple(value / self.scale for value in self.percentiles)
        }

    def __repr__(self) -> str:
        return (f"{self.__class__.__name__}(unit='{self.unit}', scale={self.scale}, rounds={self.rounds}, "
                f"mean={self.mean}, median={self.median}, minimum={self.minimum}, maximum={self.maximum}, "
                f"standard_deviation={self.standard_deviation}, "
                f"relative_standard_deviation={self.relative_standard_deviation}, "
                f"percentiles=[{', '.join(str(p) for p in self.percentiles)}])")
