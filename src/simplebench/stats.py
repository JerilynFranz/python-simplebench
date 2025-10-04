# -*- coding: utf-8 -*-
"""Containers for benchmark statistics"""

import statistics
from typing import Optional, Sequence

from .constants import (DEFAULT_INTERVAL_SCALE, DEFAULT_INTERVAL_UNIT,
                        DEFAULT_OPS_PER_INTERVAL_UNIT,
                        DEFAULT_OPS_PER_INTERVAL_SCALE,
                        DEFAULT_MEMORY_SCALE, DEFAULT_MEMORY_UNIT)
from .iteration import Iteration
from .exceptions import ErrorTag
from .si_units import si_unit_base
from .validators import (validate_non_empty_string, validate_positive_float, validate_sequence_of_numbers)


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
        self._unit: str = validate_non_empty_string(
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
        if not self.data:  # edge case of no data, forbidden by constructor but just in case
            return tuple(0.0 for _ in percentiles_n)
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

        The unit is converted to its SI base unit representation. (e.g., "ms" becomes "s")

        The dictionary is mutability-safe as all data is either a primitive or a copy.

        Returns:
            A dictionary containing the statistics and the scaled data points.
        '''
        # Immutability is preserved because all values are primitives or copies already
        stats: dict[str, str | float | dict[int, float] | tuple[int | float, ...]] = self.statistics_as_dict
        stats['data'] = tuple(value / self.scale for value in self.data)
        return stats

    def __repr__(self) -> str:
        return (f"{self.__class__.__name__}(unit='{self.unit}', scale={self.scale}, "
                f"data=[{', '.join(str(d) for d in self.data)}])")


class OperationsPerInterval(Stats):
    '''Container for the operations per time interval statistics of a benchmark.

    Attributes:
        unit (str): The unit of measurement for the benchmark (e.g., "ops/s"). (read only)
        scale (float): The scale factor for the interval (e.g. 1 for seconds). (read only)
        data: Sequence[int | float] = List of data points. (read only)
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
                 iterations: Sequence[Iteration] | None = None,
                 unit: str = DEFAULT_OPS_PER_INTERVAL_UNIT,
                 scale: float = DEFAULT_OPS_PER_INTERVAL_SCALE,
                 data: Optional[Sequence[int | float]] = None) -> None:
        """Construct OperationsPerInterval stats from Iteration or raw ops data.

        Args:
            iterations (list[Iteration] | None): List of Iteration objects to extract ops data from.
            unit (str): The unit of measurement for the benchmark (e.g., "ops/s").
            scale (float): The scale factor for the interval (e.g. 1 for seconds).
            data (Optional[list[int | float]]): Optional list of ops data points. If not provided,
                ops data will be extracted from the iterations if available.
        Raises:
            SimpleBenchTypeError: If any of the arguments are of the wrong type.
            SimpleBenchValueError: If any of the arguments have invalid values.
        """
        if not data:
            data = []
        if not data and iterations is not None:
            data = [iteration.ops_per_second for iteration in iterations]
        super().__init__(unit=unit, scale=scale, data=data)


class OperationTimings(Stats):
    '''Container for the operation timing statistics of a benchmark.

    Attributes:
        unit (str): The unit of measurement for the timings (e.g., "ns"). (read only)
        scale (float): The scale factor for the timings (e.g., "1e-9" for nanoseconds). (read only)
        data: (tuple[int | float, ...]) = Tuple of timing data points. (read only)
        mean (float): The mean time per operation. (read only)
        median (float): The median time per operation. (read only)
        minimum (float): The minimum time per operation. (read only)
        maximum (float): The maximum time per operation. (read only)
        standard_deviation (float): The standard deviation of the time per operation. (read only)
        relative_standard_deviation (float): The relative standard deviation of the time per operation. (read only)
        percentiles (dict[int, float]): Percentiles of time per operation. (read only)
    '''
    def __init__(self,
                 *,
                 iterations: Sequence[Iteration] | None = None,
                 unit: str = DEFAULT_INTERVAL_UNIT,
                 scale: float = DEFAULT_INTERVAL_SCALE,
                 data: Optional[Sequence[int | float]] = None):
        """Construct OperationTimings stats from Iteration or raw timing data.

        Args:
            iterations (Sequence[Iteration] | None): Sequence of Iteration objects to extract timing data from.
            unit (str): The unit of measurement for the timings (e.g., "ns").
            scale (float): The scale factor for the timings (e.g., "1e-9" for nanoseconds).
            data (Optional[Sequence[int | float]]): Optional Sequence of timing data points. If not provided,
                timing data will be extracted from the iterations if available.
        Raises:
            SimpleBenchTypeError: If any of the arguments are of the wrong type.
            SimpleBenchValueError: If any of the arguments have invalid values.
        """
        if not data:
            data = []
        if not data and iterations is not None:
            data = [iteration.per_round_elapsed for iteration in iterations]
        super().__init__(unit=unit, scale=scale, data=data)


class MemoryUsage(Stats):
    '''Container for the memory usage statistics of a benchmark.

    Attributes:
        unit (str): The unit of measurement for the memory usage (e.g., "MB"). (read only)
        scale (float): The scale factor for the memory usage (e.g., "1e6" for megabytes). (read only)
        data: tuple[float | int, ...] = Tuple of memory usage data points. (read only)
        mean (float): The mean memory usage. (read only)
        median (float): The median memory usage. (read only)
        minimum (float): The minimum memory usage. (read only)
        maximum (float): The maximum memory usage. (read only)
        standard_deviation (float): The standard deviation of the memory usage. (read only)
        relative_standard_deviation (float): The relative standard deviation of the memory usage. (read only)
        percentiles (dict[int, float]): Percentiles of memory usage. (read only)
    '''
    def __init__(self,
                 *,
                 iterations: Sequence[Iteration] | None = None,
                 unit: str = DEFAULT_MEMORY_UNIT,
                 scale: float = DEFAULT_MEMORY_SCALE,
                 data: Optional[Sequence[int | float]] = None):
        """Construct MemoryUsage stats from Iteration or raw memory data.

        Args:
            iterations (Sequence[Iteration] | None): List of Iteration objects to extract memory data from.
            unit (str): The unit of measurement for the memory usage (e.g., "MB").
            scale (float): The scale factor for the memory usage (e.g., "1e6" for megabytes).
            data (Optional[list[int | float]]): Optional list of memory usage data points. If not provided,
                memory data will be extracted from the iterations if available.
        Raises:
            SimpleBenchTypeError: If any of the arguments are of the wrong type.
            SimpleBenchValueError: If any of the arguments have invalid values.
        """
        if not data:
            data = []
        if not data and iterations is not None:
            data = [iteration.memory for iteration in iterations]
        super().__init__(unit=unit, scale=scale, data=data)


class PeakMemoryUsage(Stats):
    '''Container for the peak memory usage statistics of a benchmark.

    Attributes:
        unit (str): The unit of measurement for the memory usage (e.g., "MB"). (read only)
        scale (float): The scale factor for the memory usage (e.g., "1e6" for megabytes). (read only)
        data: tuple[int | float, ...] = Tuple of peak memory usage data points. (read only)
        mean (float): The mean memory usage. (read only)
        median (float): The median memory usage. (read only)
        minimum (float): The minimum memory usage. (read only)
        maximum (float): The maximum memory usage. (read only)
        standard_deviation (float): The standard deviation of the memory usage. (read only)
        relative_standard_deviation (float): The relative standard deviation of the memory usage. (read only)
        percentiles (dict[int, float]): Percentiles of memory usage. (read only)
    '''
    def __init__(self,
                 *,
                 iterations: Sequence[Iteration] | None = None,
                 unit: str = DEFAULT_MEMORY_UNIT,
                 scale: float = DEFAULT_MEMORY_SCALE,
                 data: Optional[Sequence[int | float]] = None):
        """Construct PeakMemoryUsage stats from Iteration or raw memory data.
        Args:
            iterations (Sequence[Iteration] | None): Sequence of Iteration objects to extract peak memory data from.
            unit (str): The unit of measurement for the memory usage (e.g., "MB").
            scale (float): The scale factor for the memory usage (e.g., "1e6" for megabytes).
            data (Optional[Sequence[int | float]]): Optional Sequence of peak memory usage data points. If not provided,
                peak memory data will be extracted from the iterations if available.
        Raises:
            SimpleBenchTypeError: If any of the arguments are of the wrong type.
            SimpleBenchValueError: If any of the arguments have invalid values.
        """
        if not data:
            data = []
        if not data and iterations is not None:
            data = [iteration.peak_memory for iteration in iterations]
        super().__init__(unit=unit, scale=scale, data=data)
