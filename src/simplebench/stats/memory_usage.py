# -*- coding: utf-8 -*-
"""Containers for benchmark statistics"""
from __future__ import annotations

from typing import Sequence

from ..defaults import DEFAULT_MEMORY_SCALE, DEFAULT_MEMORY_UNIT
from ..exceptions import SimpleBenchTypeError
from ..iteration import Iteration
from ..validators import validate_sequence_of_numbers
from . import Stats, StatsSummary
from .exceptions.memory_usage import _MemoryUsageErrorTag


class MemoryUsage(Stats):
    """Container for the memory usage statistics of a benchmark.

    :ivar unit: The unit of measurement for the memory usage (e.g., "MB").
    :vartype unit: str
    :ivar scale: The scale factor for the memory usage (e.g., "1e6" for megabytes).
    :vartype scale: float
    :ivar rounds: The number of data points in the benchmark.
    :vartype rounds: int
    :ivar data: Tuple of memory usage data points.
    :vartype data: tuple[float | int, ...]
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
                 data: Sequence[int | float] | None = None):
        """Construct MemoryUsage stats from sequence of Iteration or raw memory data.

        At least one of ``iterations`` or ``data`` must be provided.

        If provided, ``iterations`` must be a sequence of
        :class:`~simplebench.iteration.Iteration` objects and memory data will be extracted
        from each :attr:`~simplebench.iteration.Iteration.memory` attribute. If ``data`` is
        also provided, the memory data extracted from the iterations will be appended to
        the provided data.

        :param iterations: Optional list of
            :class:`~simplebench.iteration.Iteration` objects to extract memory data from.
        :param unit: Optional unit of measurement for the memory usage (e.g., "MB").
            Defaults to 'bytes'.
        :param scale: Optional scale factor for the memory usage (e.g., "1e6" for
            megabytes). Defaults to 1.0.
        :param rounds: The number of data points in the benchmark. Defaults to 1.
        :param data: Optional list of memory usage data points. If not provided,
            memory data will be extracted from the iterations if available.
        :raises ~simplebench.exceptions.SimpleBenchTypeError: If any of the arguments are
            of the wrong type.
        :raises ~simplebench.exceptions.SimpleBenchValueError: If any of the arguments have
            invalid values.
        """
        if iterations is None and data is None:
            raise SimpleBenchTypeError(
                "either iterations or data must be provided",
                tag=_MemoryUsageErrorTag.NO_DATA_OR_ITERATIONS_PROVIDED)
        if data is None:
            data = []
        imported_data: list[int | float] = list(validate_sequence_of_numbers(
                data, 'data',
                type_tag=_MemoryUsageErrorTag.INVALID_DATA_ARG_TYPE,
                value_tag=_MemoryUsageErrorTag.INVALID_DATA_ARG_VALUE))

        if iterations is not None:
            if not isinstance(iterations, Sequence):
                raise SimpleBenchTypeError(
                    "passed iterations arg is not a Sequence",
                    tag=_MemoryUsageErrorTag.INVALID_ITERATIONS_ARG_TYPE)

            if not all(isinstance(iteration, Iteration) for iteration in iterations):
                raise SimpleBenchTypeError(
                    "There are items in the iterations arg sequence that are not Iteration objects",
                    tag=_MemoryUsageErrorTag.INVALID_ITERATIONS_ITEM_ARG_TYPE)
            imported_data.extend(iteration.memory for iteration in iterations)

        super().__init__(unit=unit, scale=scale, rounds=rounds, data=imported_data)


class MemoryUsageSummary(StatsSummary):
    """Container for summary statistics of a MemoryUsage benchmark.

    This class is exclusive of raw data points.

    :ivar unit: The unit of measurement for the benchmark (e.g., "ops/s").
    :vartype unit: str
    :ivar scale: The scale factor for the interval (e.g. 1 for seconds).
    :vartype scale: float
    :ivar rounds: The number of data points in the benchmark.
    :vartype rounds: int
    :ivar data: Always an empty tuple as a :class:`~.StatsSummary` object does not
        contain raw data points.
    :vartype data: tuple[int | float, ...]
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
    :vartype percentiles: tuple[float, ...]
    """
