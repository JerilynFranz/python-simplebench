"""Keyword arguments for Results class."""
from __future__ import annotations

from typing import Any, Sequence

from simplebench.iteration import Iteration
from simplebench.results import Results
from simplebench.stats import MemoryUsage, OperationsPerInterval, OperationTimings, PeakMemoryUsage

from .kwargs import KWArgs, NoDefaultValue


class ResultsKWArgs(KWArgs):
    """A class to hold keyword arguments for initializing a Results instance."""

    def __init__(  # pylint: disable=unused-argument
            self,
            *,
            group: str | NoDefaultValue = NoDefaultValue(),
            title: str | NoDefaultValue = NoDefaultValue(),
            description: str | NoDefaultValue = NoDefaultValue(),
            n: int | NoDefaultValue = NoDefaultValue(),
            rounds: int | NoDefaultValue = NoDefaultValue(),
            total_elapsed: float | NoDefaultValue = NoDefaultValue(),
            iterations: Sequence[Iteration] | NoDefaultValue = NoDefaultValue(),
            variation_cols: dict[str, str] | NoDefaultValue = NoDefaultValue(),
            variation_marks: dict[str, Any] | NoDefaultValue = NoDefaultValue(),
            interval_unit: str | NoDefaultValue = NoDefaultValue(),
            interval_scale: float | NoDefaultValue = NoDefaultValue(),
            ops_per_interval_unit: str | NoDefaultValue = NoDefaultValue(),
            ops_per_interval_scale: float | NoDefaultValue = NoDefaultValue(),
            memory_unit: str | NoDefaultValue = NoDefaultValue(),
            memory_scale: float | NoDefaultValue = NoDefaultValue(),
            ops_per_second: OperationsPerInterval | NoDefaultValue = NoDefaultValue(),
            per_round_timings: OperationTimings | NoDefaultValue = NoDefaultValue(),
            memory: MemoryUsage | NoDefaultValue = NoDefaultValue(),
            peak_memory: PeakMemoryUsage | NoDefaultValue = NoDefaultValue(),
            extra_info: dict[str, Any] | NoDefaultValue = NoDefaultValue(),
            ) -> None:
        """Initialize ResultsKWArgs with optional keyword arguments.

        :param group: The group name for the results.
        :type group: str
        :param title: The title of the results.
        :type title: str
        :param description: A description of the results.
        :type description: str
        :param n: The number of iterations.
        :type n: int
        :param rounds: The number of rounds in the benchmark case.
        :type rounds: int
        :param total_elapsed: The total elapsed time.
        :type total_elapsed: float
        :param iterations: A sequence of Iteration instances.
        :type iterations: Sequence[Iteration]
        :param variation_cols: Variation columns as a dictionary.
        :type variation_cols: dict[str, str]
        :param variation_marks: Variation marks as a dictionary.
        :type variation_marks: dict[str, Any]
        :param interval_unit: The unit for intervals.
        :type interval_unit: str
        :param interval_scale: The scale for intervals.
        :type interval_scale: float
        :param ops_per_interval_unit: The unit for operations per interval.
        :type ops_per_interval_unit: str
        :param ops_per_interval_scale: The scale for operations per interval.
        :type ops_per_interval_scale: float
        :param memory_unit: The unit for memory usage.
        :type memory_unit: str
        :param memory_scale: The scale for memory usage.
        :type memory_scale: float
        :param ops_per_second: OperationsPerInterval instance.
        :type ops_per_second: OperationsPerInterval
        :param per_round_timings: OperationTimings instance.
        :type per_round_timings: OperationTimings
        :param memory: MemoryUsage instance.
        :type memory: MemoryUsage
        :param peak_memory: PeakMemoryUsage instance.
        :type peak_memory: PeakMemoryUsage
        :param extra_info: Additional information as a dictionary.
        :type extra_info: dict[str, Any]
        """
        super().__init__(call=Results.__init__, kwargs=locals())
