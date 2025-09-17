# -*- coding: utf-8 -*-
"""Container for the results of a single benchmark test."""

from dataclasses import dataclass, field
from typing import Any

from simplebench.exceptions import ErrorTag, SimpleBenchValueError, SimpleBenchTypeError

from .constants import DEFAULT_INTERVAL_SCALE, DEFAULT_INTERVAL_UNIT
from .enums import Section
from .iteration import Iteration
from .stats import OperationsPerInterval, OperationTimings, Stats


@dataclass(kw_only=True)
class Results:
    '''Container for the results of a single benchmark test.

    Properties:
        group (str): The reporting group to which the benchmark case belongs.
        title (str): The name of the benchmark case.
        description (str): A brief description of the benchmark case.
        n (int): The number of rounds the benchmark ran per iteration.
        variation_cols (dict[str, str]): The columns to use for labelling kwarg variations in the benchmark.
        interval_unit (str): The unit of measurement for the interval (e.g. "ns").
        interval_scale (float): The scale factor for the interval (e.g. 1e-9 for nanoseconds).
        iterations (list[Iteration]): The list of Iteration objects representing each iteration of the benchmark.
        ops_per_second (OperationsPerInterval): Statistics for operations per interval.
        per_round_timings (OperationTimings): Statistics for per-round timings.
        ops_per_interval_unit (str): The unit of measurement for operations per interval (e.g. "ops/s").
        ops_per_interval_scale (float): The scale factor for operations per interval (e.g. 1.0 for ops/s).
        total_elapsed (int): The total elapsed time for the benchmark.
        variation_marks (dict[str, Any]): A dictionary of variation marks used to identify the benchmark variation.
        extra_info (dict[str, Any]): Additional information about the benchmark run.
    '''
    group: str
    """The reporting group to which the benchmark case belongs."""
    title: str
    """The name of the benchmark case."""
    description: str
    """A brief description of the benchmark case."""
    n: int
    """The number of rounds the benchmark ran per iteration."""
    variation_cols: dict[str, str] = field(default_factory=dict[str, str])
    """The columns to use for labelling kwarg variations in the benchmark."""
    interval_unit: str = DEFAULT_INTERVAL_UNIT
    """The unit of measurement for the interval (e.g. "ns")."""
    interval_scale: float = DEFAULT_INTERVAL_SCALE
    """The scale factor for the interval (e.g. 1e-9 for nanoseconds)."""
    ops_per_interval_unit: str = DEFAULT_INTERVAL_UNIT
    """The unit of measurement for operations per interval (e.g. "ops/s")."""
    ops_per_interval_scale: float = DEFAULT_INTERVAL_SCALE
    """The scale factor for operations per interval (e.g. 1.0 for ops/s)."""
    iterations: list[Iteration] = field(default_factory=list[Iteration])
    """The list of Iteration objects representing each iteration of the benchmark."""
    ops_per_second: OperationsPerInterval = field(default_factory=OperationsPerInterval)
    """Statistics for operations per interval."""
    per_round_timings: OperationTimings = field(default_factory=OperationTimings)
    """Statistics for per-round timings."""
    total_elapsed: int = 0
    """The total elapsed time for the benchmark."""
    variation_marks: dict[str, Any] = field(default_factory=dict[str, Any])
    """A dictionary of variation marks used to identify the benchmark variation."""
    extra_info: dict[str, Any] = field(default_factory=dict[str, Any])
    """Additional information about the benchmark run."""

    def results_section(self, section: Section) -> Stats:
        """Returns the requested section of the benchmark results.

        Args:
            section (Section): The section of the results to return. Must be Section.OPS or Section.TIMING.

        Returns:
            Stats: The requested section of the benchmark results.
        """
        if not isinstance(section, Section):
            raise SimpleBenchTypeError(
                f'Invalid section type: {type(section)}. Must be of type Section.',
                tag=ErrorTag.RESULTS_RESULTS_SECTION_INVALID_SECTION_TYPE_ARGUMENT
            )
        match section:
            case Section.OPS:
                return self.ops_per_second
            case Section.TIMING:
                return self.per_round_timings
            case _:
                raise SimpleBenchValueError(
                    f'Invalid section: {section}. Must be Section.OPS or Section.TIMING.',
                    tag=ErrorTag.RESULTS_RESULTS_SECTION_UNSUPPORTED_SECTION_ARGUMENT
                )

    def __post_init__(self) -> None:
        if self.iterations:
            self.per_round_timings.data = list([iteration.per_round_elapsed for iteration in self.iterations])
            self.ops_per_second.data = list([iteration.ops_per_second for iteration in self.iterations])

    @property
    def results_as_dict(self) -> dict[str, str | float | dict[int, float] | dict[str, Any]]:
        '''Returns the benchmark results as a JSON-serializable dictionary.'''
        return {
            'type': self.__class__.__name__,
            'group': self.group,
            'title': self.title,
            'description': self.description,
            'n': self.n,
            'variation_cols': self.variation_cols,
            'interval_unit': self.interval_unit,
            'interval_scale': self.interval_scale,
            'ops_per_interval_unit': self.ops_per_interval_unit,
            'ops_per_interval_scale': self.ops_per_interval_scale,
            'total_elapsed': self.total_elapsed,
            'extra_info': self.extra_info,
            'per_round_timings': self.per_round_timings.statistics_as_dict,
            'ops_per_second': self.ops_per_second.statistics_as_dict,
        }

    @property
    def results_and_data_as_dict(self) -> dict[str, str | float | dict[int, float] | dict[str, Any]]:
        '''Returns the benchmark results and iterations as a JSON-serializable dictionary.'''
        results = self.results_as_dict
        results['per_round_timings'] = self.per_round_timings.statistics_and_data_as_dict
        results['ops_per_second'] = self.ops_per_second.statistics_and_data_as_dict
        return results
