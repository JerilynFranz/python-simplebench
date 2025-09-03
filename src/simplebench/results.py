# -*- coding: utf-8 -*-
"""Container for the results of a single benchmark test."""

from dataclasses import dataclass, field
from typing import Any

from .constants import DEFAULT_INTERVAL_SCALE, DEFAULT_INTERVAL_UNIT
from .iteration import Iteration
from .stats import OperationsPerInterval, OperationTimings


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
        ops_per_interval_unit (str): The unit of measurement for operations per interval (e.g. "ops/s").
        ops_per_interval_scale (float): The scale factor for operations per interval (e.g. 1.0 for ops/s).
        total_elapsed (int): The total elapsed time for the benchmark.
        extra_info (dict[str, Any]): Additional information about the benchmark run.
    '''
    group: str
    title: str
    description: str
    n: int
    variation_cols: dict[str, str] = field(default_factory=dict[str, str])
    interval_unit: str = DEFAULT_INTERVAL_UNIT
    interval_scale: float = DEFAULT_INTERVAL_SCALE
    ops_per_interval_unit: str = DEFAULT_INTERVAL_UNIT
    ops_per_interval_scale: float = DEFAULT_INTERVAL_SCALE
    iterations: list[Iteration] = field(default_factory=list[Iteration])
    ops_per_second: OperationsPerInterval = field(default_factory=OperationsPerInterval)
    per_round_timings: OperationTimings = field(default_factory=OperationTimings)
    total_elapsed: int = 0
    variation_marks: dict[str, Any] = field(default_factory=dict[str, Any])
    extra_info: dict[str, Any] = field(default_factory=dict[str, Any])

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
