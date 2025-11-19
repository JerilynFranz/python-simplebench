# -*- coding: utf-8 -*-
"""Containers for benchmark statistics"""
from __future__ import annotations

from typing import Optional, Sequence

from ..defaults import DEFAULT_MEMORY_SCALE, DEFAULT_MEMORY_UNIT
from ..exceptions import SimpleBenchTypeError
from ..iteration import Iteration
from ..validators import validate_sequence_of_numbers
from . import Stats, StatsSummary
from .exceptions.peak_memory_usage import _PeakMemoryUsageErrorTag


class PeakMemoryUsage(Stats):
    """Container for the peak memory usage statistics of a benchmark.

    :ivar unit: The unit of measurement for the memory usage (e.g., "MB").
    :vartype unit: str
    :ivar scale: The scale factor for the memory usage (e.g., "1e6" for megabytes).
    :vartype scale: float
    :ivar rounds: The number of data points in the benchmark.
    :vartype rounds: int
    :ivar data: Tuple of peak memory usage data points.
    :vartype data: tuple[int | float, ...]
    :ivar mean: The mean memory usage.
    :vartype mean: float
    :ivar median: The median memory usage.
    :vartype median: float
    :ivar minimum: The minimum memory usage.
    :vartype minimum: float
    :ivar maximum: The maximum memory usage.
    :vartype maximum: float
    :ivar standard_deviation: The standard deviation of the memory usage.
    :vartype standard_deviation: float
    :ivar relative_standard_deviation: The relative standard deviation of the memory usage.
    :vartype relative_standard_deviation: float
    :ivar percentiles: Percentiles of memory usage.
    :vartype percentiles: dict[int, float]
    """
    def __init__(self,
                 *,
                 iterations: Sequence[Iteration] | None = None,
                 unit: str = DEFAULT_MEMORY_UNIT,
                 scale: float = DEFAULT_MEMORY_SCALE,
                 rounds: int = 1,
                 data: Optional[Sequence[int | float]] = None):
        """Construct PeakMemoryUsage stats from Iteration or raw memory data.

        :param iterations: Sequence of
            :class:`~simplebench.iteration.Iteration` objects to extract peak memory data
            from.
        :param unit: The unit of measurement for the memory usage (e.g., "MB").
        :param scale: The scale factor for the memory usage (e.g., "1e6" for megabytes).
        :param rounds: The number of data points in the benchmark.
        :param data: Optional Sequence of peak memory usage data points. If not
            provided, peak memory data will be extracted from the iterations if
            available.
        :raises ~simplebench.exceptions.SimpleBenchTypeError: If any of the arguments are
            of the wrong type.
        :raises ~simplebench.exceptions.SimpleBenchValueError: If any of the arguments have
            invalid values.
        """
        if iterations is None and data is None:
            raise SimpleBenchTypeError(
                "either iterations or data must be provided",
                tag=_PeakMemoryUsageErrorTag.NO_DATA_OR_ITERATIONS_PROVIDED)
        if data is None:
            data = []
        imported_data: list[int | float] = list(validate_sequence_of_numbers(
                data, 'data',
                type_tag=_PeakMemoryUsageErrorTag.INVALID_DATA_ARG_TYPE,
                value_tag=_PeakMemoryUsageErrorTag.INVALID_DATA_ARG_VALUE))

        if iterations is not None:
            if not isinstance(iterations, Sequence):
                raise SimpleBenchTypeError(
                    "passed iterations arg is not a Sequence",
                    tag=_PeakMemoryUsageErrorTag.INVALID_ITERATIONS_ARG_TYPE)

            if not all(isinstance(iteration, Iteration) for iteration in iterations):
                raise SimpleBenchTypeError(
                    "There are items in the iterations arg sequence that are not Iteration objects",
                    tag=_PeakMemoryUsageErrorTag.INVALID_ITERATIONS_ITEM_ARG_TYPE)
            imported_data.extend(iteration.peak_memory for iteration in iterations)

        super().__init__(unit=unit, scale=scale, rounds=rounds, data=imported_data)


class PeakMemoryUsageSummary(StatsSummary):
    """Container for the summary of peak memory usage statistics of a benchmark.

    :ivar unit: The unit of measurement for the memory usage (e.g., "MB").
    :vartype unit: str
    :ivar scale: The scale factor for the memory usage (e.g., "1e6" for megabytes).
    :vartype scale: float
    :ivar rounds: The number of data points in the benchmark.
    :vartype rounds: int
    :ivar mean: The mean memory usage.
    :vartype mean: float
    :ivar median: The median memory usage.
    :vartype median: float
    :ivar minimum: The minimum memory usage.
    :vartype minimum: float
    :ivar maximum: The maximum memory usage.
    :vartype maximum: float
    :ivar standard_deviation: The standard deviation of the memory usage.
    :vartype standard_deviation: float
    :ivar relative_standard_deviation: The relative standard deviation of the memory
        usage.
    :vartype relative_standard_deviation: float
    :ivar percentiles: Percentiles of memory usage.
    :vartype percentiles: dict[int, float]
    """
