# -*- coding: utf-8 -*-
"""Containers for benchmark statistics"""
from __future__ import annotations
from typing import Optional, Sequence

from . import Stats, StatsSummary
from .exceptions.peak_memory_usage import PeakMemoryUsageErrorTag
from ..defaults import DEFAULT_MEMORY_SCALE, DEFAULT_MEMORY_UNIT
from ..exceptions import SimpleBenchTypeError
from ..validators import validate_sequence_of_numbers
from ..iteration import Iteration


class PeakMemoryUsage(Stats):
    '''Container for the peak memory usage statistics of a benchmark.

    Attributes:
        unit (str): The unit of measurement for the memory usage (e.g., "MB"). (read only)
        scale (float): The scale factor for the memory usage (e.g., "1e6" for megabytes). (read only)
        rounds (int): The number of data points in the benchmark. (read only)
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
                 rounds: int = 1,
                 data: Optional[Sequence[int | float]] = None):
        """Construct PeakMemoryUsage stats from Iteration or raw memory data.
        Args:
            iterations (Sequence[Iteration] | None): Sequence of Iteration objects to extract peak memory data from.
            unit (str): The unit of measurement for the memory usage (e.g., "MB").
            scale (float): The scale factor for the memory usage (e.g., "1e6" for megabytes).
            rounds (int): The number of data points in the benchmark.
            data (Optional[Sequence[int | float]]): Optional Sequence of peak memory usage data points. If not provided,
                peak memory data will be extracted from the iterations if available.
        Raises:
            SimpleBenchTypeError: If any of the arguments are of the wrong type.
            SimpleBenchValueError: If any of the arguments have invalid values.
        """
        if iterations is None and data is None:
            raise SimpleBenchTypeError(
                "either iterations or data must be provided",
                tag=PeakMemoryUsageErrorTag.NO_DATA_OR_ITERATIONS_PROVIDED)
        if data is None:
            data = []
        imported_data: list[int | float] = list(validate_sequence_of_numbers(
                data, 'data',
                type_tag=PeakMemoryUsageErrorTag.INVALID_DATA_ARG_TYPE,
                value_tag=PeakMemoryUsageErrorTag.INVALID_DATA_ARG_VALUE))

        if iterations is not None:
            if not isinstance(iterations, Sequence):
                raise SimpleBenchTypeError(
                    "passed iterations arg is not a Sequence",
                    tag=PeakMemoryUsageErrorTag.INVALID_ITERATIONS_ARG_TYPE)

            if not all(isinstance(iteration, Iteration) for iteration in iterations):
                raise SimpleBenchTypeError(
                    "There are items in the iterations arg sequence that are not Iteration objects",
                    tag=PeakMemoryUsageErrorTag.INVALID_ITERATIONS_ITEM_ARG_TYPE)
            imported_data.extend(iteration.peak_memory for iteration in iterations)

        super().__init__(unit=unit, scale=scale, rounds=rounds, data=imported_data)


class PeakMemoryUsageSummary(StatsSummary):
    '''Container for the summary of peak memory usage statistics of a benchmark.

    Attributes:
        unit (str): The unit of measurement for the memory usage (e.g., "MB"). (read only)
        scale (float): The scale factor for the memory usage (e.g., "1e6" for megabytes). (read only)
        rounds (int): The number of data points in the benchmark. (read only)
        mean (float): The mean memory usage. (read only)
        median (float): The median memory usage. (read only)
        minimum (float): The minimum memory usage. (read only)
        maximum (float): The maximum memory usage. (read only)
        standard_deviation (float): The standard deviation of the memory usage. (read only)
        relative_standard_deviation (float): The relative standard deviation of the memory usage. (read only)
        percentiles (dict[int, float]): Percentiles of memory usage. (read only)
    '''
