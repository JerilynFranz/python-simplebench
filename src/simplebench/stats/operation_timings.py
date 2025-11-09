# -*- coding: utf-8 -*-
"""Containers for benchmark statistics"""
from __future__ import annotations
from typing import Optional, Sequence

from . import Stats, StatsSummary
from .exceptions.operation_timings import OperationTimingsErrorTag
from ..defaults import DEFAULT_INTERVAL_SCALE, DEFAULT_INTERVAL_UNIT
from ..exceptions import SimpleBenchTypeError
from ..validators import validate_sequence_of_numbers
from ..iteration import Iteration


class OperationTimings(Stats):
    '''Container for the operation timing statistics of a benchmark.

    Attributes:
        unit (str): The unit of measurement for the timings (e.g., "ns"). (read only)
        scale (float): The scale factor for the timings (e.g., "1e-9" for nanoseconds). (read only)
        rounds (int): The number of data points in the benchmark. (read only)
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
                 rounds: int = 1,
                 data: Optional[Sequence[int | float]] = None):
        """Construct OperationTimings stats from Iteration or raw timing data.

        Args:
            iterations (Sequence[Iteration] | None): Sequence of Iteration objects to extract timing data from.
            unit (str): The unit of measurement for the timings (e.g., "ns").
            scale (float): The scale factor for the timings (e.g., "1e-9" for nanoseconds).
            rounds (int): The number of data points in the benchmark.
            data (Optional[Sequence[int | float]]): Optional Sequence of timing data points. If not provided,
                timing data will be extracted from the iterations if available.
        Raises:
            SimpleBenchTypeError: If any of the arguments are of the wrong type.
            SimpleBenchValueError: If any of the arguments have invalid values.
        """
        if iterations is None and data is None:
            raise SimpleBenchTypeError(
                "either iterations or data must be provided",
                tag=OperationTimingsErrorTag.NO_DATA_OR_ITERATIONS_PROVIDED)
        if data is None:
            data = []
        imported_data: list[int | float] = list(validate_sequence_of_numbers(
                data, 'data',
                type_tag=OperationTimingsErrorTag.INVALID_DATA_ARG_TYPE,
                value_tag=OperationTimingsErrorTag.INVALID_DATA_ARG_VALUE))

        if iterations is not None:
            if not isinstance(iterations, Sequence):
                raise SimpleBenchTypeError(
                    "passed iterations arg is not a Sequence",
                    tag=OperationTimingsErrorTag.INVALID_ITERATIONS_ARG_TYPE)

            if not all(isinstance(iteration, Iteration) for iteration in iterations):
                raise SimpleBenchTypeError(
                    "There are items in the iterations arg sequence that are not Iteration objects",
                    tag=OperationTimingsErrorTag.INVALID_ITERATIONS_ITEM_ARG_TYPE)
            imported_data.extend(iteration.per_round_elapsed for iteration in iterations)

        super().__init__(unit=unit, scale=scale, rounds=rounds, data=imported_data)


class OperationTimingsSummary(StatsSummary):
    '''Container for summary of operation timing statistics of a benchmark.

    Attributes:
        unit (str): The unit of measurement for the benchmark (e.g., "ops/s"). (read only)
        scale (float): The scale factor for the interval (e.g. 1 for seconds). (read only)
        rounds (int): The number of data points in the benchmark. (read only)
        mean (float): The mean operations per time interval. (read only)
        median (float): The median operations per time interval. (read only)
        minimum (float): The minimum operations per time interval. (read only)
        maximum (float): The maximum operations per time interval. (read only)
        standard_deviation (float): The standard deviation of operations per time interval. (read only)
        relative_standard_deviation (float): The relative standard deviation of ops per time interval. (read only)
        percentiles (dict[int, float]): Percentiles of operations per time interval. (read only)
    '''
