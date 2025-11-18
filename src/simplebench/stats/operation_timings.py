# -*- coding: utf-8 -*-
"""Containers for benchmark statistics"""
from __future__ import annotations

from typing import Optional, Sequence

from ..defaults import DEFAULT_INTERVAL_SCALE, DEFAULT_INTERVAL_UNIT
from ..exceptions import SimpleBenchTypeError
from ..iteration import Iteration
from ..validators import validate_sequence_of_numbers
from . import Stats, StatsSummary
from .exceptions.operation_timings import OperationTimingsErrorTag


class OperationTimings(Stats):
    """Container for the operation timing statistics of a benchmark.

    :ivar unit: The unit of measurement for the timings (e.g., "ns").
    :vartype unit: str
    :ivar scale: The scale factor for the timings (e.g., "1e-9" for nanoseconds).
    :vartype scale: float
    :ivar rounds: The number of data points in the benchmark.
    :vartype rounds: int
    :ivar data: Tuple of timing data points.
    :vartype data: tuple[int | float, ...]
    :ivar mean: The mean time per operation.
    :vartype mean: float
    :ivar median: The median time per operation.
    :vartype median: float
    :ivar minimum: The minimum time per operation.
    :vartype minimum: float
    :ivar maximum: The maximum time per operation.
    :vartype maximum: float
    :ivar standard_deviation: The standard deviation of the time per operation.
    :vartype standard_deviation: float
    :ivar relative_standard_deviation: The relative standard deviation of the time per
        operation.
    :vartype relative_standard_deviation: float
    :ivar percentiles: Percentiles of time per operation.
    :vartype percentiles: dict[int, float]
    """
    def __init__(self,
                 *,
                 iterations: Sequence[Iteration] | None = None,
                 unit: str = DEFAULT_INTERVAL_UNIT,
                 scale: float = DEFAULT_INTERVAL_SCALE,
                 rounds: int = 1,
                 data: Optional[Sequence[int | float]] = None):
        """Construct OperationTimings stats from Iteration or raw timing data.

        :param iterations: Sequence of
            :class:`~simplebench.iteration.Iteration` objects to extract timing data from.
        :param unit: The unit of measurement for the timings (e.g., "ns").
        :param scale: The scale factor for the timings (e.g., "1e-9" for nanoseconds).
        :param rounds: The number of data points in the benchmark.
        :param data: Optional sequence of timing data points. If not provided,
            timing data will be extracted from the iterations if available.
        :raises ~simplebench.exceptions.SimpleBenchTypeError: If any of the arguments are
            of the wrong type.
        :raises ~simplebench.exceptions.SimpleBenchValueError: If any of the arguments have
            invalid values.
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
    """Container for summary of operation timing statistics of a benchmark.

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
