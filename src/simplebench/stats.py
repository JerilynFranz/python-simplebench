# -*- coding: utf-8 -*-
"""Containers for benchmark statistics"""

import statistics
from typing import Optional

from .constants import (DEFAULT_INTERVAL_SCALE, DEFAULT_INTERVAL_UNIT,
                        DEFAULT_OPS_PER_INTERVAL_UNIT,
                        DEFAULT_OPS_PER_INTERVAL_SCALE)


class Stats:
    '''Generic container for statistics on a benchmark.

    Attributes:
        unit (str): The unit of measurement for the benchmark (e.g., "ops/s").
        scale (float): The scale factor for the interval (e.g. 1 for seconds).
        data: list[int | float] = field(default_factory=list[int | float])
        mean (float): The mean operations per time interval. (read only)
        median (float): The median operations per time interval. (read only)
        minimum (float): The minimum operations per time interval. (read only)
        maximum (float): The maximum operations per time interval. (read only)
        standard_deviation (float): The standard deviation of operations per time interval. (read only)
        relative_standard_deviation (float): The relative standard deviation of ops per time interval. (read only)
        percentiles (dict[int, float]): Percentiles of operations per time interval. (read only)
    '''
    def __init__(self, unit: str = '', scale: float = 0.0, data: Optional[list[int | float]] = None) -> None:
        self.unit: str = unit
        self.scale: float = scale
        self.data: list[int | float] = data if data is not None else []

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
    def relative_standard_deviation(self):
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
            return {p: float('nan') for p in [5, 10, 25, 50, 75, 90, 95]}
        percentiles: dict[int, float] = {}
        for percent in [5, 10, 25, 50, 75, 90, 95]:
            percentiles[percent] = statistics.quantiles(self.data, n=100)[percent - 1]
        return percentiles

    @property
    def statistics_as_dict(self) -> dict[str, str | float | dict[int, float] | list[int | float]]:
        '''Returns the statistics as a JSON-serializable dictionary.'''
        return {
            'type': f'{self.__class__.__name__}:statistics',
            'unit': self.unit,
            'scale': self.scale,
            'mean': self.mean / self.scale if self.scale else self.mean,
            'median': self.median / self.scale if self.scale else self.median,
            'minimum': self.minimum / self.scale if self.scale else self.minimum,
            'maximum': self.maximum / self.scale if self.scale else self.maximum,
            'standard_deviation': self.standard_deviation / self.scale if self.scale else self.standard_deviation,
            'relative_standard_deviation': self.relative_standard_deviation,
            'percentiles': self.percentiles,
        }

    @property
    def statistics_and_data_as_dict(self) -> dict[
            str, str | float | dict[int, float] | list[int | float]]:
        '''Returns the statistics and data as a JSON-serializable dictionary.'''
        stats: dict[str, str | float | dict[int, float] | list[int | float]] = self.statistics_as_dict
        stats['data'] = [value / self.scale for value in self.data]
        return stats


class OperationsPerInterval(Stats):
    '''Container for the operations per time interval statistics of a benchmark.

    Attributes:
        unit (str): The unit of measurement for the benchmark (e.g., "ops/s").
        scale (float): The scale factor for the interval (e.g. 1 for seconds).
        data: list[int] = field(default_factory=list[int])
        mean (float): The mean operations per time interval. (read only)
        median (float): The median operations per time interval. (read only)
        minimum (float): The minimum operations per time interval. (read only)
        maximum (float): The maximum operations per time interval. (read only)
        standard_deviation (float): The standard deviation of operations per time interval. (read only)
        relative_standard_deviation (float): The relative standard deviation of ops per time interval. (read only)
        percentiles (dict[int, float]): Percentiles of operations per time interval. (read only)
    '''
    def __init__(self,
                 unit: str = DEFAULT_OPS_PER_INTERVAL_UNIT,
                 scale: float = DEFAULT_OPS_PER_INTERVAL_SCALE,
                 data: Optional[list[int | float]] = None):
        super().__init__(unit=unit, scale=scale, data=data)


class OperationTimings(Stats):
    '''Container for the operation timing statistics of a benchmark.

    Attributes:
        unit (str): The unit of measurement for the timings (e.g., "ns").
        scale (float): The scale factor for the timings (e.g., "1e-9" for nanoseconds).
        mean (float): The mean time per operation.
        median (float): The median time per operation.
        minimum (float): The minimum time per operation.
        maximum (float): The maximum time per operation.
        standard_deviation (float): The standard deviation of the time per operation.
        relative_standard_deviation (float): The relative standard deviation of the time per operation.
        percentiles (dict[int, float]): Percentiles of time per operation.
        data: list[float | int] = field(default_factory=list[float | int])
    '''
    def __init__(self,
                 unit: str = DEFAULT_INTERVAL_UNIT,
                 scale: float = DEFAULT_INTERVAL_SCALE,
                 data: Optional[list[int | float]] = None):
        super().__init__(unit=unit, scale=scale, data=data)
