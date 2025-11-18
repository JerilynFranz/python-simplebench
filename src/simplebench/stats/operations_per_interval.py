# -*- coding: utf-8 -*-
"""Container for OperationsPerInterval benchmark statistics"""
from __future__ import annotations

from typing import Optional, Sequence

from ..defaults import DEFAULT_OPS_PER_INTERVAL_SCALE, DEFAULT_OPS_PER_INTERVAL_UNIT
from ..exceptions import SimpleBenchTypeError
from ..iteration import Iteration
from ..validators import validate_sequence_of_numbers
from . import Stats, StatsSummary
from .exceptions.operations_per_interval import OperationsPerIntervalErrorTag


class OperationsPerInterval(Stats):
    """Container for the operations per time interval statistics of a benchmark.

    :ivar unit: The unit of measurement for the benchmark (e.g., "ops/s").
    :vartype unit: str
    :ivar scale: The scale factor for the interval (e.g. 1 for seconds).
    :vartype scale: float
    :ivar rounds: The number of data points in the benchmark.
    :vartype rounds: int
    :ivar data: List of data points.
    :vartype data: ~typing.Sequence[int | float]
    :ivar mean: The mean operations per time interval.
    :vartype mean: float
    :ivar median: The median operations per time interval.
    :vartype median: float
    :ivar minimum: The minimum operations per time interval.
    :vartype minimum: float
    :ivar maximum: The maximum operations per time interval.
    :vartype maximum: float
    :ivar standard_deviation: The standard deviation of operations per time interval.
    :vartype standard_deviation: float
    :ivar relative_standard_deviation: The relative standard deviation of ops per time
        interval.
    :vartype relative_standard_deviation: float
    :ivar percentiles: Percentiles of operations per time interval.
    :vartype percentiles: dict[int, float]
    """
    def __init__(self,
                 *,
                 iterations: Sequence[Iteration] | None = None,
                 unit: str = DEFAULT_OPS_PER_INTERVAL_UNIT,
                 scale: float = DEFAULT_OPS_PER_INTERVAL_SCALE,
                 rounds: int = 1,
                 data: Optional[Sequence[int | float]] = None) -> None:
        """Construct OperationsPerInterval stats from Iteration or raw ops data.

        :param iterations: List of
            :class:`~simplebench.iteration.Iteration` objects to extract ops data from.
        :param unit: The unit of measurement for the benchmark (e.g., "ops/s").
        :param scale: The scale factor for the interval (e.g. 1 for seconds).
        :param rounds: The number of data points in the benchmark.
        :param data: Optional list of ops data points. If not provided,
            ops data will be extracted from the iterations if available.
        :raises ~simplebench.exceptions.SimpleBenchTypeError: If any of the arguments are
            of the wrong type.
        :raises ~simplebench.exceptions.SimpleBenchValueError: If any of the arguments have
            invalid values.
        """
        if iterations is None and data is None:
            raise SimpleBenchTypeError(
                "either iterations or data must be provided",
                tag=OperationsPerIntervalErrorTag.NO_DATA_OR_ITERATIONS_PROVIDED)
        if data is None:
            data = []
        imported_data: list[int | float] = list(validate_sequence_of_numbers(
                data, 'data',
                type_tag=OperationsPerIntervalErrorTag.INVALID_DATA_ARG_TYPE,
                value_tag=OperationsPerIntervalErrorTag.INVALID_DATA_ARG_VALUE))

        if iterations is not None:
            if not isinstance(iterations, Sequence):
                raise SimpleBenchTypeError(
                    "passed iterations arg is not a Sequence",
                    tag=OperationsPerIntervalErrorTag.INVALID_ITERATIONS_ARG_TYPE)

            if not all(isinstance(iteration, Iteration) for iteration in iterations):
                raise SimpleBenchTypeError(
                    "There are items in the iterations arg sequence that are not Iteration objects",
                    tag=OperationsPerIntervalErrorTag.INVALID_ITERATIONS_ITEM_ARG_TYPE)
            imported_data.extend(iteration.ops_per_second for iteration in iterations)

        super().__init__(unit=unit, scale=scale, rounds=rounds, data=imported_data)


class OperationsPerIntervalSummary(StatsSummary):
    """Summary of OperationsPerInterval statistics.

    :ivar unit: The unit of measurement for the benchmark (e.g., "ops/s").
    :vartype unit: str
    :ivar scale: The scale factor for the interval (e.g. 1 for seconds).
    :vartype scale: float
    :ivar rounds: The number of data points in the benchmark.
    :vartype rounds: int
    :ivar mean: The mean operations per time interval.
    :vartype mean: float
    :ivar median: The median operations per time interval.
    :vartype median: float
    :ivar minimum: The minimum operations per time interval.
    :vartype minimum: float
    :ivar maximum: The maximum operations per time interval.
    :vartype maximum: float
    :ivar standard_deviation: The standard deviation of operations per time interval.
    :vartype standard_deviation: float
    :ivar relative_standard_deviation: The relative standard deviation of ops per time
        interval.
    :vartype relative_standard_deviation: float
    :ivar percentiles: Percentiles of operations per time interval.
    :vartype percentiles: dict[int, float]
    """
