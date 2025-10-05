# -*- coding: utf-8 -*-
"""Containers for benchmark statistics"""
from __future__ import annotations
from typing import Optional, Sequence, Any

from . import Stats
from ..exceptions import ErrorTag, SimpleBenchKeyError, SimpleBenchTypeError
from ..validators import (validate_non_blank_string, validate_float, validate_positive_float,
                          validate_non_negative_float, validate_sequence_of_numbers)


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
        self._unit = validate_non_empty_string(
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
    def from_dict(cls, data: dict[str, Any], unit: Optional[str] = None, scale: Optional[int | float] = None) -> Stats:
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
        if 'unit' not in data and unit is None:
            raise SimpleBenchKeyError(
                'The data dictionary must contain a "unit" key or a unit must be provided as an argument.',
                tag=ErrorTag.STATS_FROM_DICT_MISSING_UNIT)
        if 'scale' not in data and scale is None:
            raise SimpleBenchKeyError(
                'The data dictionary must contain a "scale" key or a scale must be provided as an argument.',
                tag=ErrorTag.STATS_FROM_DICT_MISSING_SCALE)
        if 'data' not in data:
            raise SimpleBenchKeyError(
                'The data dictionary must contain a non-empty "data" key with at least one data point.',
                tag=ErrorTag.STATS_INVALID_DATA_ARG_TYPE)
        raw_unit = data.get('unit') if 'unit' in data else unit
        final_unit: str = validate_non_empty_string(
                    raw_unit, 'unit',  # type: ignore[arg-type]
                    ErrorTag.STATS_INVALID_UNIT_ARG_TYPE,
                    ErrorTag.STATS_INVALID_UNIT_ARG_VALUE)
        raw_scale = data.get('scale') if scale is None else scale
        final_scale: float = validate_positive_float(
                    raw_scale, 'scale',  # type: ignore[arg-type]
                    ErrorTag.STATS_FROM_DICT_INVALID_SCALE_ARG_TYPE,
                    ErrorTag.STATS_FROM_DICT_INVALID_SCALE_ARG_VALUE)
        raw_data_points = data.get('data')
        float_data_points: Sequence[int | float] = validate_sequence_of_numbers(
                    value=raw_data_points,  # type: ignore[arg-type]
                    field_name='data',
                    allow_empty=False,
                    type_tag=ErrorTag.STATS_INVALID_DATA_ARG_TYPE,
                    value_tag=ErrorTag.STATS_INVALID_DATA_ARG_ITEM_TYPE)
        final_data_points: Sequence[int | float] = [value * final_scale for value in float_data_points]
        return cls(unit=final_unit, scale=final_scale, data=final_data_points)
