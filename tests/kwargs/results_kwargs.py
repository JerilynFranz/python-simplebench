"""Keyword arguments for Results class."""
from __future__ import annotations
from typing import Any, Sequence

from simplebench.results import Results
from simplebench.iteration import Iteration
from simplebench.stats import OperationsPerInterval, OperationTimings, MemoryUsage, PeakMemoryUsage

from .kwargs import NoDefaultValue, KWArgs


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

        Args:
            group (str): The group name for the results.
            title (str): The title of the results.
            description (str): A description of the results.
            n (int): The number of iterations.
            rounds (int): The number of rounds in the benchmark case.
            total_elapsed (float): The total elapsed time.
            iterations (Sequence[Iteration]): A sequence of Iteration instances.
            variation_cols (dict[str, str]): Variation columns as a dictionary.
            variation_marks (dict[str, Any]): Variation marks as a dictionary.
            interval_unit (str): The unit for intervals.
            interval_scale (float): The scale for intervals.
            ops_per_interval_unit (str): The unit for operations per interval.
            ops_per_interval_scale (float): The scale for operations per interval.
            memory_unit (str): The unit for memory usage.
            memory_scale (float): The scale for memory usage.
            ops_per_second (OperationsPerInterval): OperationsPerInterval instance.
            per_round_timings (OperationTimings): OperationTimings instance.
            memory (MemoryUsage): MemoryUsage instance.
            peak_memory (PeakMemoryUsage): PeakMemoryUsage instance.
            extra_info (dict[str, Any]): Additional information as a dictionary.
        """
        super().__init__(call=Results.__init__, kwargs=locals())
