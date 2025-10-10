# -*- coding: utf-8 -*-
"""Containers for benchmark statistics"""
from __future__ import annotations
from typing import Sequence

from . import Stats, StatsSummary
from ..defaults import DEFAULT_MEMORY_SCALE, DEFAULT_MEMORY_UNIT
from ..iteration import Iteration
from ..exceptions import SimpleBenchTypeError, ErrorTag
from ..validators import validate_sequence_of_numbers


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
                 data: Sequence[int | float] | None = None):
        """Construct MemoryUsage stats from sequence of Iteration or raw memory data.

        At least one of iterations or data must be provided.

        If provided, iterations must be a Sequence of Iteration objects and memory data will be extracted
        from each Iteration's memory attribute. If data is also provided, the memory data extracted from
        the iterations will be appended to the provided data.

        Args:
            iterations (Sequence[Iteration] | None): Optional list of Iteration objects to extract memory data from.
            unit (str): Optional unit of measurement for the memory usage (e.g., "MB"). (default = 'bytes')
            scale (float): Optional scale factor for the memory usage (e.g., "1e6" for megabytes). (default = 1.0)
            data (Sequence[int | float] | None): Optional list of memory usage data points. If not provided,
                memory data will be extracted from the iterations if available.
        Raises:
            SimpleBenchTypeError: If any of the arguments are of the wrong type.
            SimpleBenchValueError: If any of the arguments have invalid values.
        """
        if iterations is None and data is None:
            raise SimpleBenchTypeError(
                "either iterations or data must be provided",
                tag=ErrorTag.STATS_MEMORY_USAGE_NO_DATA_OR_ITERATIONS_PROVIDED)
        if data is None:
            data = []
        imported_data: list[int | float] = list(validate_sequence_of_numbers(
                data, 'data',
                type_tag=ErrorTag.STATS_MEMORY_USAGE_INVALID_DATA_ARG_TYPE,
                value_tag=ErrorTag.STATS_MEMORY_USAGE_INVALID_DATA_ARG_VALUE))

        if iterations is not None:
            if not isinstance(iterations, Sequence):
                raise SimpleBenchTypeError(
                    "passed iterations arg is not a Sequence",
                    tag=ErrorTag.STATS_MEMORY_USAGE_INVALID_ITERATIONS_ARG_TYPE)

            if not all(isinstance(iteration, Iteration) for iteration in iterations):
                raise SimpleBenchTypeError(
                    "There are items in the iterations arg sequence that are not Iteration objects",
                    tag=ErrorTag.STATS_MEMORY_USAGE_INVALID_ITERATIONS_ITEM_ARG_TYPE)
            imported_data.extend(iteration.memory for iteration in iterations)

        super().__init__(unit=unit, scale=scale, data=imported_data)


class MemoryUsageSummary(StatsSummary):
    '''Container for summary statistics of a MemoryUsage benchmark, exclusive of raw data points.

    Attributes:
        unit (str): The unit of measurement for the benchmark (e.g., "ops/s"). (read only)
        scale (float): The scale factor for the interval (e.g. 1 for seconds). (read only)
        data (tuple[int | float, ...]): Always an empty tuple as a StatsSummary object does not
            contain raw data points. (read only)
        mean (float): The mean operations per time interval. (read only)
        median (float): The median operations per time interval. (read only)
        minimum (float): The minimum operations per time interval. (read only)
        maximum (float): The maximum operations per time interval. (read only)
        standard_deviation (float): The standard deviation of operations per time interval. (read only)
        relative_standard_deviation (float): The relative standard deviation of ops per time interval. (read only)
        percentiles (tuple[float, ...]): Percentiles of operations per time interval. (read only)
    '''
