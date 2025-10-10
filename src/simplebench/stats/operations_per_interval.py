# -*- coding: utf-8 -*-
"""Container for OperationsPerInterval benchmark statistics"""
from __future__ import annotations
from typing import Optional, Sequence

from . import Stats, StatsSummary
from ..defaults import DEFAULT_OPS_PER_INTERVAL_UNIT, DEFAULT_OPS_PER_INTERVAL_SCALE
from ..exceptions import SimpleBenchTypeError, ErrorTag
from ..iteration import Iteration
from ..validators import validate_sequence_of_numbers


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
        if iterations is None and data is None:
            raise SimpleBenchTypeError(
                "either iterations or data must be provided",
                tag=ErrorTag.STATS_OPS_NO_DATA_OR_ITERATIONS_PROVIDED)
        if data is None:
            data = []
        imported_data: list[int | float] = list(validate_sequence_of_numbers(
                data, 'data',
                type_tag=ErrorTag.STATS_OPS_INVALID_DATA_ARG_TYPE,
                value_tag=ErrorTag.STATS_OPS_INVALID_DATA_ARG_VALUE))

        if iterations is not None:
            if not isinstance(iterations, Sequence):
                raise SimpleBenchTypeError(
                    "passed iterations arg is not a Sequence",
                    tag=ErrorTag.STATS_OPS_INVALID_ITERATIONS_ARG_TYPE)

            if not all(isinstance(iteration, Iteration) for iteration in iterations):
                raise SimpleBenchTypeError(
                    "There are items in the iterations arg sequence that are not Iteration objects",
                    tag=ErrorTag.STATS_OPS_INVALID_ITERATIONS_ITEM_ARG_TYPE)
            imported_data.extend(iteration.ops_per_second for iteration in iterations)

        super().__init__(unit=unit, scale=scale, data=imported_data)


class OperationsPerIntervalSummary(StatsSummary):
    '''Summary of OperationsPerInterval statistics.

    Attributes:
        unit (str): The unit of measurement for the benchmark (e.g., "ops/s"). (read only)
        scale (float): The scale factor for the interval (e.g. 1 for seconds). (read only)
        mean (float): The mean operations per time interval. (read only)
        median (float): The median operations per time interval. (read only)
        minimum (float): The minimum operations per time interval. (read only)
        maximum (float): The maximum operations per time interval. (read only)
        standard_deviation (float): The standard deviation of operations per time interval. (read only)
        relative_standard_deviation (float): The relative standard deviation of ops per time interval. (read only)
        percentiles (dict[int, float]): Percentiles of operations per time interval. (read only)
    '''
