# -*- coding: utf-8 -*-
"""Base benchmark statistics class."""
from __future__ import annotations
from math import isclose
import statistics
from typing import Any, Sequence

from ..exceptions import ErrorTag, SimpleBenchKeyError, SimpleBenchTypeError, SimpleBenchValueError
from ..si_units import si_unit_base, si_scale_to_unit
from ..validators import (validate_non_blank_string, validate_float, validate_non_negative_float,
                          validate_positive_float, validate_sequence_of_numbers)


class Stats:
    '''Generic container for statistics on a benchmark.

    Attributes:
        unit (str): The unit of measurement for the benchmark (e.g., "ops/s"). (read only)
        scale (float): The scale factor for the interval (e.g. 1 for seconds). (read only)
        data: (tuple[float | int, ...]) = Tuple of data points. (read only)
        mean (float): The mean operations per time interval. (read only)
        median (float): The median operations per time interval. (read only)
        minimum (float): The minimum operations per time interval. (read only)
        maximum (float): The maximum operations per time interval. (read only)
        standard_deviation (float): The standard deviation of operations per time interval. (read only)
        relative_standard_deviation (float): The relative standard deviation of ops per time interval. (read only)
        percentiles (tuple[float, ...]): Percentiles of operations per time interval. (read only)
    '''
    __slots__ = ('_unit', '_scale', '_data', '_percentiles', '_mean', '_median',
                 '_minimum', '_maximum', '_standard_deviation', '_relative_standard_deviation',
                 '_statistics_as_dict', '_statistics_and_data_as_dict')

    def __init__(self, *, unit: str, scale: float, data: Sequence[int | float]) -> None:
        """Initialize the Stats object.

        Args:
            unit (str): The unit of measurement for the benchmark (e.g., "ops/s").
            scale (float): The scale factor for the interval (e.g. 1 for seconds).
            data (Sequence[int | float]): Sequence of data points.
        Raises:
            SimpleBenchTypeError: If any of the arguments are of the wrong type.
            SimpleBenchValueError: If any of the arguments have invalid values.
        """
        self._unit: str = validate_non_blank_string(
                                unit, 'unit',
                                ErrorTag.STATS_INVALID_UNIT_ARG_TYPE,
                                ErrorTag.STATS_INVALID_UNIT_ARG_VALUE)
        self._scale: float = validate_positive_float(
                                scale, 'scale',
                                ErrorTag.STATS_INVALID_SCALE_ARG_TYPE,
                                ErrorTag.STATS_INVALID_SCALE_ARG_VALUE)
        # data is left unsorted to allow for time series data to be preserved
        self._data: tuple[int | float, ...] = tuple(validate_sequence_of_numbers(
                                            value=data,
                                            field_name='data',
                                            allow_empty=False,
                                            type_tag=ErrorTag.STATS_INVALID_DATA_ARG_TYPE,
                                            value_tag=ErrorTag.STATS_INVALID_DATA_ARG_ITEM_TYPE))
        self._percentiles: tuple[float, ...] | None = None
        self._mean: float | None = None
        self._median: float | None = None
        self._minimum: float | None = None
        self._maximum: float | None = None
        self._standard_deviation: float | None = None
        self._relative_standard_deviation: float | None = None
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
    def relative_standard_deviation(self) -> float:
        '''The relative standard deviation of the data.'''
        if self._relative_standard_deviation is None:
            self._relative_standard_deviation = self.standard_deviation / self.mean * 100 if self.mean else 0.0
        return self._relative_standard_deviation

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

        Returns:
            A tuple of percentiles keyed positionally by percent from 0 to 100.
        """
        percentiles_n: list[int] = list(range(0, 101))
        if len(self.data) == 1:
            return tuple(float(self.data[0]) for _ in percentiles_n)
        quantile_values = statistics.quantiles(self.data, n=102, method='inclusive')
        return tuple(quantile_values)

    @property
    def statistics_as_dict(self) -> dict[str, str | float | dict[int, float] | tuple[int | float, ...]]:
        '''Returns the statistics as a JSON-serializable dictionary.

        The data values are scaled according to the scale factor to provide
        human-readable values using the base unit rather than the scaled unit.

        The unit is converted to its SI base unit representation. (e.g., "ms" becomes "s")

        This does not include the raw data points, only the statistics.

        The dictionary is mutability-safe as all data is either a primitive or a copy.

        Returns:
            A dictionary containing the statistics.
        '''
        # Immutability is preserved because all values are primitives or copies already
        return {
            'type': f'{self.__class__.__name__}:statistics',
            'unit': si_unit_base(self.unit),
            'scale': 1.0,
            'mean': self.mean / self.scale,
            'median': self.median / self.scale,
            'minimum': self.minimum / self.scale,
            'maximum': self.maximum / self.scale,
            'standard_deviation': self.standard_deviation / self.scale,
            'relative_standard_deviation': self.relative_standard_deviation,
            'percentiles': tuple(value / self.scale for value in self.percentiles)
        }

    @property
    def statistics_and_data_as_dict(self) -> dict[
            str, str | float | dict[int, float] | tuple[int | float, ...]]:
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
        stats: dict[str, str | float | dict[int, float] | tuple[int | float, ...]] = self.statistics_as_dict
        stats['data'] = tuple(value / self.scale for value in self.data)
        return stats

    def as_stats_summary(self) -> StatsSummary:
        '''Returns a StatsSummary derived from this Stats object.

        This effectively strips the raw data points from the Stats object, leaving only the summary statistics.

        Returns:
            A StatsSummary object containing the same statistics as this Stats object.
        '''
        return StatsSummary(
            unit=self.unit,
            scale=self.scale,
            mean=self.mean,
            median=self.median,
            minimum=self.minimum,
            maximum=self.maximum,
            standard_deviation=self.standard_deviation,
            relative_standard_deviation=self.relative_standard_deviation,
            percentiles=self.percentiles
        )

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
                                       tag=ErrorTag.STATS_FROM_DICT_INVALID_DATA_ARG_TYPE)
        if 'unit' not in data:
            raise SimpleBenchKeyError('The data dictionary is missing the required "unit" key.',
                                      tag=ErrorTag.STATS_FROM_DICT_MISSING_UNIT_KEY)
        if 'scale' not in data:
            raise SimpleBenchKeyError('The data dictionary is missing the required "scale" key.',
                                      tag=ErrorTag.STATS_FROM_DICT_MISSING_SCALE_KEY)
        if 'data' not in data:
            raise SimpleBenchKeyError('The data dictionary is missing the required "data" key.',
                                      tag=ErrorTag.STATS_FROM_DICT_MISSING_DATA_KEY)

        return cls(unit=data['unit'], scale=data['scale'], data=data['data'])  # type: ignore[arg-type]

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
        if not isinstance(other, Stats):
            return NotImplemented

        # this handles scale differences between two Stats objects
        self_base_unit: str = si_unit_base(self.unit)
        other_base_unit: str = si_unit_base(other.unit)
        if self_base_unit != other_base_unit:
            return False

        scale_by: float = si_scale_to_unit(base_unit=self_base_unit,
                                           current_unit=other.unit,
                                           target_unit=self.unit)
        if self.scale == 0:  # should never happen due to validation in constructors
            raise SimpleBenchValueError(
                "self.scale must not be zero when comparing two Stats objects",
                tag=ErrorTag.STATS_COMPARISON_INCOMPATIBLE_SCALES)
        if other.scale == 0:   # should never happen due to validation in constructors
            raise SimpleBenchValueError(
                "other.scale must not be zero when comparing two Stats objects",
                tag=ErrorTag.STATS_COMPARISON_INCOMPATIBLE_SCALES)
        relative_scale: float = self.scale / other.scale

        if not isclose(scale_by, relative_scale):
            return False

        if not (isclose(self.mean, other.mean / relative_scale) and
                isclose(self.median,  other.median / relative_scale) and
                isclose(self.minimum, other.minimum / relative_scale) and
                isclose(self.maximum, other.maximum / relative_scale) and
                isclose(self.standard_deviation, other.standard_deviation / relative_scale) and
                isclose(self.relative_standard_deviation, other.relative_standard_deviation)):
            return False

        # should never happen due to validation in constructors
        if len(self.percentiles) != len(other.percentiles):
            return False

        for self_pct, other_pct in zip(self.percentiles, other.percentiles):
            if not isclose(self_pct, other_pct / relative_scale):
                return False

        return si_unit_base(self.unit) == si_unit_base(other.unit)

    def __repr__(self) -> str:
        return (f"{self.__class__.__name__}(unit='{self.unit}', scale={self.scale}, "
                f"data=[{', '.join(str(d) for d in self.data)}])")


class StatsSummary(Stats):
    '''Container for summary statistics of a benchmark, exclusive of raw data points.

    Attributes:
        unit (str): The unit of measurement for the benchmark (e.g., "ops/s"). (read only)
        scale (float): The scale factor for the interval (e.g. 1 for seconds). (read only)
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
    def __init__(self,  # pylint: disable=super-init-not-called,too-many-arguments
                 *,
                 unit: str,
                 scale: float,
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
                        ErrorTag.STATS_SUMMARY_INVALID_UNIT_ARG_TYPE,
                        ErrorTag.STATS_SUMMARY_INVALID_UNIT_ARG_VALUE)
        self._scale = validate_positive_float(
                        scale, 'scale',
                        ErrorTag.STATS_SUMMARY_INVALID_SCALE_ARG_TYPE,
                        ErrorTag.STATS_SUMMARY_INVALID_SCALE_ARG_VALUE)
        self._mean = validate_float(
                        mean, 'mean',
                        ErrorTag.STATS_SUMMARY_INVALID_MEAN_ARG_TYPE)
        self._median = validate_float(
                        median, 'median',
                        ErrorTag.STATS_SUMMARY_INVALID_MEDIAN_ARG_TYPE)
        self._minimum = validate_float(
                        minimum, 'minimum',
                        ErrorTag.STATS_SUMMARY_INVALID_MINIMUM_ARG_TYPE)
        self._maximum = validate_float(
                        maximum, 'maximum',
                        ErrorTag.STATS_SUMMARY_INVALID_MAXIMUM_ARG_TYPE)
        self._standard_deviation = validate_non_negative_float(
                        standard_deviation, 'standard_deviation',
                        ErrorTag.STATS_SUMMARY_INVALID_STANDARD_DEVIATION_ARG_TYPE,
                        ErrorTag.STATS_SUMMARY_INVALID_STANDARD_DEVIATION_ARG_VALUE)
        self._relative_standard_deviation = validate_non_negative_float(
                        relative_standard_deviation, 'relative_standard_deviation',
                        ErrorTag.STATS_SUMMARY_INVALID_RELATIVE_STANDARD_DEVIATION_ARG_TYPE,
                        ErrorTag.STATS_SUMMARY_INVALID_RELATIVE_STANDARD_DEVIATION_ARG_VALUE)
        self._percentiles = tuple(validate_sequence_of_numbers(
                        percentiles, 'percentiles',
                        allow_empty=False,
                        type_tag=ErrorTag.STATS_SUMMARY_INVALID_PERCENTILES_ARG_TYPE,
                        value_tag=ErrorTag.STATS_SUMMARY_INVALID_PERCENTILES_ARG_VALUE))
        self._statistics_as_dict = None
        self._statistics_and_data_as_dict = None

    @property
    def data(self) -> tuple[int | float, ...]:
        '''The data points.

        This is always an empty tuple as a StatsSummary does not contain raw data points.
        '''
        return tuple()

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> Stats:
        """Construct a StatsSummary object from a dictionary.

        Example:
            stats_summary_dict = {
                "unit": "ops/s",
                "scale": 1.0,
                "data": [1000, 2000, 1500, 3000, 2500]
            }
            stats_summary = Stats.from_dict(stats_summary_dict)
            print(stats_summary.mean)  # Output: 2000.0

        Args:
            data (dict): A dictionary containing the stats data. Must contain 'data' key with a non-empty
                sequence of data points consisting of integers or floats.
            unit (Optional[str]): The unit of measurement for the benchmark (e.g., "ops/s").
                It will be taken from the 'unit' key in the data dictionary by priority and
                from the unit argument if not present in the data dictionary.
            scale (Optional[int | float]): The scale factor for the interval (e.g. 1 for seconds).
                It will be taken from the 'scale' key in the data dictionary by priority and
                from the scale argument if not present in the data dictionary.

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
                                       tag=ErrorTag.STATS_FROM_DICT_INVALID_DATA_ARG_TYPE)

        required_keys = [
            'unit', 'scale', 'mean', 'median', 'minimum', 'maximum',
            'standard_deviation', 'relative_standard_deviation', 'percentiles'
        ]
        keys_for_construction = {}
        for key in required_keys:
            if key not in data:
                raise SimpleBenchKeyError(f"The data dictionary is missing the required '{key}' key.",
                                          tag=ErrorTag.STATS_SUMMARY_FROM_DICT_MISSING_KEY)
            keys_for_construction[key] = data[key]
        return cls(**keys_for_construction)  # type: ignore[arg-type]  # pylint: disable=missing-kwoa
