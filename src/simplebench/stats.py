# -*- coding: utf-8 -*-
"""Containers for benchmark statistics"""

from copy import copy
import statistics
from typing import Optional

from .constants import (DEFAULT_INTERVAL_SCALE, DEFAULT_INTERVAL_UNIT,
                        DEFAULT_OPS_PER_INTERVAL_UNIT,
                        DEFAULT_OPS_PER_INTERVAL_SCALE,
                        DEFAULT_MEMORY_SCALE, DEFAULT_MEMORY_UNIT,
                        DEFAULT_CUSTOM_METRICS_UNIT, DEFAULT_CUSTOM_METRICS_SCALE)
from .iteration import Iteration
from .exceptions import SimpleBenchTypeError, SimpleBenchValueError, ErrorTag
from .si_units import si_unit_base


class Stats:
    '''Generic container for statistics on a benchmark.

    Attributes:
        unit (str): The unit of measurement for the benchmark (e.g., "ops/s").
        scale (float): The scale factor for the interval (e.g. 1 for seconds).
        data: list[int | float] = List of data points.
        mean (float): The mean operations per time interval. (read only)
        median (float): The median operations per time interval. (read only)
        minimum (float): The minimum operations per time interval. (read only)
        maximum (float): The maximum operations per time interval. (read only)
        standard_deviation (float): The standard deviation of operations per time interval. (read only)
        relative_standard_deviation (float): The relative standard deviation of ops per time interval. (read only)
        percentiles (dict[int, float]): Percentiles of operations per time interval. (read only)
    '''
    def __init__(self, *, unit: str, scale: float, data: Optional[list[int | float]] = None) -> None:
        self.unit = unit
        self.scale = scale
        self.data = data if data is not None else []

    @property
    def unit(self) -> str:
        '''The unit of the data.'''
        return self._unit

    @unit.setter
    def unit(self, unit: str) -> None:
        """Set the unit of the data.

        The unit should be a string representing the unit of measurement,
        such as "ops/s" for operations per second and "ns" for nanoseconds.

        It cannot be an empty string.

        Args:
            unit: The unit of measurement for the benchmark (e.g., "ops/s").

        Raises:
            SimpleBenchTypeError: If unit is not a str.
            SimpleBenchValueError: If unit is an empty string.
        """
        if not isinstance(unit, str):
            raise SimpleBenchTypeError(
                "unit must be a str",
                tag=ErrorTag.STATS_INVALID_UNIT_ARG_TYPE)
        if unit == '':
            raise SimpleBenchValueError(
                "unit must not be an empty string",
                tag=ErrorTag.STATS_INVALID_UNIT_ARG_VALUE)
        self._unit = unit

    @property
    def scale(self) -> float:
        '''The scale of the data.'''
        return self._scale

    @scale.setter
    def scale(self, scale: float) -> None:
        """Set the scale of the data.

        The scale should be a float or int greater than 0.

        Args:
            scale: The scale factor for the data.

        Raises:
            SimpleBenchTypeError: If scale is not a float or int.
            SimpleBenchValueError: If scale is not greater than 0.
        """
        if not isinstance(scale, (float, int)):
            raise SimpleBenchTypeError(
                "scale must be a float or int",
                tag=ErrorTag.STATS_INVALID_SCALE_ARG_TYPE)
        if scale <= 0:
            raise SimpleBenchValueError(
                "scale must be greater than 0",
                tag=ErrorTag.STATS_INVALID_SCALE_ARG_VALUE)
        self._scale = float(scale)

    @property
    def data(self) -> list[int | float]:
        '''The data points.'''
        return self._data

    @data.setter
    def data(self, data: Optional[list[int | float]]) -> None:
        """Set the data points.

        Args:
            data: A list of int or float data points, or None to clear the data.

        Raises:
            SimpleBenchTypeError: If data is not a list of int or float, or None.
        """
        if data is not None and not isinstance(data, list):
            raise SimpleBenchTypeError(
                "data must be a list of numbers (int or float) or None",
                tag=ErrorTag.STATS_INVALID_DATA_ARG_TYPE)
        if data is not None:
            for value in data:
                if not isinstance(value, (int, float)):
                    raise SimpleBenchTypeError(
                        "data values must be a list of int or float not " + str(type(value)),
                        tag=ErrorTag.STATS_INVALID_DATA_ARG_ITEM_TYPE)
        else:
            data = []
        self._data = data

    @property
    def mean(self) -> float:
        '''The mean of the data.'''
        return statistics.mean(self.data) if self.data else 0.0

    @property
    def median(self) -> float:
        '''The median of the data.'''
        return statistics.median(self.data) if self.data else 0.0

    @property
    def minimum(self) -> float:
        '''The minimum of the data.'''
        return float(min(self.data)) if self.data else 0.0

    @property
    def maximum(self) -> float:
        '''The maximum of the data.'''
        return float(max(self.data)) if self.data else 0.0

    @property
    def standard_deviation(self) -> float:
        '''The standard deviation of the data.'''
        return statistics.stdev(self.data) if len(self.data) > 1 else 0.0

    @property
    def relative_standard_deviation(self) -> float:
        '''The relative standard deviation of the data.'''
        return self.standard_deviation / self.mean * 100 if self.mean else 0.0

    @property
    def percentiles(self) -> dict[int, float]:
        '''Percentiles of the data.

        Computes the 5th, 10th, 25th, 50th, 75th, 90th, and 95th percentiles
        and returns them as a dictionary keyed by percent.
        '''
        # Calculate percentiles if we have enough data points
        if not self.data:
            return {p: 0.0 for p in [5, 10, 25, 50, 75, 90, 95]}
        if len(self.data) == 1:
            return {p: float(self.data[0]) for p in [5, 10, 25, 50, 75, 90, 95]}
        percentiles: dict[int, float] = {}
        for percent in [5, 10, 25, 50, 75, 90, 95]:
            percentiles[percent] = statistics.quantiles(self.data, n=100)[percent - 1]
        return percentiles

    @property
    def statistics_as_dict(self) -> dict[str, str | float | dict[int, float] | list[int | float]]:
        '''Returns the statistics as a JSON-serializable dictionary.

        The data values are scaled according to the scale factor to provide
        human-readable values using the base unit rather than the scaled unit.

        The unit is converted to its SI base unit representation. (e.g., "ms" becomes "s")

        This does not include the raw data points, only the statistics.

        Returns:
            A dictionary containing the statistics.
        '''
        return {
            'type': f'{self.__class__.__name__}:statistics',
            'unit': si_unit_base(self.unit),
            'mean': self.mean / self.scale if self.scale else self.mean,
            'median': self.median / self.scale if self.scale else self.median,
            'minimum': self.minimum / self.scale if self.scale else self.minimum,
            'maximum': self.maximum / self.scale if self.scale else self.maximum,
            'standard_deviation': self.standard_deviation / self.scale if self.scale else self.standard_deviation,
            'relative_standard_deviation': self.relative_standard_deviation,
            'percentiles': {key: value / self.scale for key, value in self.percentiles.items()
                            } if self.scale else copy(self.percentiles),
        }

    @property
    def statistics_and_data_as_dict(self) -> dict[
            str, str | float | dict[int, float] | list[int | float]]:
        '''Returns the statistics and data as a JSON-serializable dictionary.

        This includes all the statistics as well as the raw data points.

        The data values are scaled according to the scale factor to provide
        human-readable values using the base unit rather than the scaled unit.

        The unit is converted to its SI base unit representation. (e.g., "ms" becomes "s")

        Returns:
            A dictionary containing the statistics and the scaled data points.
        '''
        stats: dict[str, str | float | dict[int, float] | list[int | float]] = self.statistics_as_dict
        stats['data'] = [value / self.scale for value in self.data]
        return stats


class OperationsPerInterval(Stats):
    '''Container for the operations per time interval statistics of a benchmark.

    Attributes:
        unit (str): The unit of measurement for the benchmark (e.g., "ops/s").
        scale (float): The scale factor for the interval (e.g. 1 for seconds).
        data: list[int] = List of data points.
        mean (float): The mean operations per time interval. (read only)
        median (float): The median operations per time interval. (read only)
        minimum (float): The minimum operations per time interval. (read only)
        maximum (float): The maximum operations per time interval. (read only)
        standard_deviation (float): The standard deviation of operations per time interval. (read only)
        relative_standard_deviation (float): The relative standard deviation of ops per time interval. (read only)
        percentiles (dict[int, float]): Percentiles of operations per time interval. (read only)
    '''
    def __init__(self,
                 *,
                 iterations: list[Iteration] | None = None,
                 unit: str = DEFAULT_OPS_PER_INTERVAL_UNIT,
                 scale: float = DEFAULT_OPS_PER_INTERVAL_SCALE,
                 data: Optional[list[int | float]] = None):
        if data is None and iterations is not None:
            data = []
            for iteration in iterations:
                data.append(iteration.ops_per_second)
        super().__init__(unit=unit, scale=scale, data=data)


class OperationTimings(Stats):
    '''Container for the operation timing statistics of a benchmark.

    Attributes:
        unit (str): The unit of measurement for the timings (e.g., "ns").
        scale (float): The scale factor for the timings (e.g., "1e-9" for nanoseconds).
        data: list[float | int] = List of timing data points.)
        mean (float): The mean time per operation.
        median (float): The median time per operation.
        minimum (float): The minimum time per operation.
        maximum (float): The maximum time per operation.
        standard_deviation (float): The standard deviation of the time per operation.
        relative_standard_deviation (float): The relative standard deviation of the time per operation.
        percentiles (dict[int, float]): Percentiles of time per operation.
    '''
    def __init__(self,
                 *,
                 iterations: list[Iteration] | None = None,
                 unit: str = DEFAULT_INTERVAL_UNIT,
                 scale: float = DEFAULT_INTERVAL_SCALE,
                 data: Optional[list[int | float]] = None):
        if data is None and iterations is not None:
            data = []
            for iteration in iterations:
                data.append(iteration.per_round_elapsed)
        super().__init__(unit=unit, scale=scale, data=data)


class MemoryUsage(Stats):
    '''Container for the memory usage statistics of a benchmark.

    Attributes:
        unit (str): The unit of measurement for the memory usage (e.g., "MB").
        scale (float): The scale factor for the memory usage (e.g., "1e6" for megabytes).
        data: list[float | int] = List of memory usage data points.
        mean (float): The mean memory usage.
        median (float): The median memory usage.
        minimum (float): The minimum memory usage.
        maximum (float): The maximum memory usage.
        standard_deviation (float): The standard deviation of the memory usage.
        relative_standard_deviation (float): The relative standard deviation of the memory usage.
        percentiles (dict[int, float]): Percentiles of memory usage.
    '''
    def __init__(self,
                 *,
                 iterations: list[Iteration] | None = None,
                 unit: str = DEFAULT_MEMORY_UNIT,
                 scale: float = DEFAULT_MEMORY_SCALE,
                 data: Optional[list[int | float]] = None):
        if data is None and iterations is not None:
            data = []
            for iteration in iterations:
                data.append(iteration.memory_usage)
        super().__init__(unit=unit, scale=scale, data=data)


class PeakMemoryUsage(Stats):
    '''Container for the peak memory usage statistics of a benchmark.

    Attributes:
        unit (str): The unit of measurement for the memory usage (e.g., "MB").
        scale (float): The scale factor for the memory usage (e.g., "1e6" for megabytes).
        data: list[float | int] = List of peak memory usage data points.
        mean (float): The mean memory usage.
        median (float): The median memory usage.
        minimum (float): The minimum memory usage.
        maximum (float): The maximum memory usage.
        standard_deviation (float): The standard deviation of the memory usage.
        relative_standard_deviation (float): The relative standard deviation of the memory usage.
        percentiles (dict[int, float]): Percentiles of memory usage.
    '''
    def __init__(self,
                 *,
                 iterations: list[Iteration] | None = None,
                 unit: str = DEFAULT_MEMORY_UNIT,
                 scale: float = DEFAULT_MEMORY_SCALE,
                 data: Optional[list[int | float]] = None):
        if data is None and iterations is not None:
            data = []
            for iteration in iterations:
                data.append(iteration.peak_memory_usage)
        super().__init__(unit=unit, scale=scale, data=data)


class CustomMetrics(Stats):
    '''Container for custom metrics statistics of a benchmark.

    Attributes:
        unit (str): The unit of measurement for the custom metric (default = DEFAULT_CUSTOM_METRICS_UNIT).
        scale (float): The scale factor for the custom metric (default = DEFAULT_CUSTOM_METRICS_SCALE).
        data: list[float | int] = List of custom metric data points.
        mean (float): The mean of the custom metric.
        median (float): The median of the custom metric.
        minimum (float): The minimum of the custom metric.
        maximum (float): The maximum of the custom metric.
        standard_deviation (float): The standard deviation of the custom metric.
        relative_standard_deviation (float): The relative standard deviation of the custom metric.
        percentiles (dict[int, float]): Percentiles of the custom metric.
    '''
    def __init__(self,
                 *,
                 iterations: list[Iteration] | None = None,
                 unit: str = DEFAULT_CUSTOM_METRICS_UNIT,
                 scale: float = DEFAULT_CUSTOM_METRICS_SCALE,
                 data: Optional[list[int | float]] = None):
        if data is None and iterations is not None:
            data = []
            for iteration in iterations:
                if iteration.custom_metric is not None:
                    data.append(iteration.custom_metric)
        super().__init__(unit=unit, scale=scale, data=data)
