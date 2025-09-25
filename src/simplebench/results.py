# -*- coding: utf-8 -*-
"""Container for the results of a single benchmark test."""
from __future__ import annotations
from typing import Any

from simplebench.exceptions import ErrorTag, SimpleBenchValueError, SimpleBenchTypeError

from .constants import DEFAULT_INTERVAL_SCALE, DEFAULT_INTERVAL_UNIT, DEFAULT_MEMORY_SCALE, DEFAULT_MEMORY_UNIT
from .enums import Section
from .iteration import Iteration
from .stats import OperationsPerInterval, OperationTimings, MemoryUsage, PeakMemoryUsage, CustomMetrics, Stats


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
        memory_usage_unit (str): The unit of measurement for memory usage (e.g. "bytes").
        memory_usage_scale (float): The scale factor for memory usage (e.g. 1.0 for bytes).
        iterations (list[Iteration]): The list of Iteration objects representing each iteration of the benchmark.
        ops_per_second (OperationsPerInterval): Statistics for operations per interval.
        per_round_timings (OperationTimings): Statistics for per-round timings.
        memory_usage (MemoryUsage): Statistics for memory usage.
        peak_memory_usage (PeakMemoryUsage): Statistics for peak memory usage.
        custom_metrics (CustomMetrics): Statistics for custom metrics.
        custom_metrics_unit (str): The unit of measurement for custom metrics (e.g. "ops/s").
        custom_metrics_scale (float): The scale factor for custom metrics (e.g. 1.0 for ops/s).
        total_elapsed (float): The total elapsed time for the benchmark.
        variation_marks (dict[str, Any]): A dictionary of variation marks used to identify the benchmark variation.
        extra_info (dict[str, Any]): Additional information about the benchmark run.
    '''
    def __init__(self,
                 *,
                 group: str,
                 title: str,
                 description: str,
                 n: int,
                 variation_cols: dict[str, str] | None = None,
                 interval_unit: str = DEFAULT_INTERVAL_UNIT,
                 interval_scale: float = DEFAULT_INTERVAL_SCALE,
                 ops_per_interval_unit: str = DEFAULT_INTERVAL_UNIT,
                 ops_per_interval_scale: float = DEFAULT_INTERVAL_SCALE,
                 memory_usage_unit: str = DEFAULT_MEMORY_UNIT,
                 memory_usage_scale: float = DEFAULT_MEMORY_SCALE,
                 iterations: list[Iteration] | None = None,
                 ops_per_second: OperationsPerInterval | None = None,
                 per_round_timings: OperationTimings | None = None,
                 memory_usage: MemoryUsage | None = None,
                 peak_memory_usage: PeakMemoryUsage | None = None,
                 custom_metrics: CustomMetrics | None = None,
                 custom_metrics_unit: str = DEFAULT_INTERVAL_UNIT,
                 custom_metrics_scale: float = DEFAULT_INTERVAL_SCALE,
                 total_elapsed: float = 0.0,
                 variation_marks: dict[str, Any] | None = None,
                 extra_info: dict[str, Any] | None = None) -> None:
        self.group = group
        self.title = title
        self.description = description
        self.n = n
        self.iterations = iterations if iterations is not None else []
        self.variation_cols = variation_cols if variation_cols is not None else {}
        self.interval_unit = interval_unit
        self.interval_scale = interval_scale
        self.ops_per_interval_unit = ops_per_interval_unit
        self.ops_per_interval_scale = ops_per_interval_scale
        self.memory_usage_unit = memory_usage_unit
        self.memory_usage_scale = memory_usage_scale
        self.peak_memory_usage_unit = memory_usage_unit
        self.peak_memory_usage_scale = memory_usage_scale
        self.custom_metrics_unit = custom_metrics_unit
        self.custom_metrics_scale = custom_metrics_scale
        self.ops_per_second = ops_per_second if ops_per_second is not None else OperationsPerInterval(
                                                                                    iterations=iterations)
        self.per_round_timings = per_round_timings if per_round_timings is not None else OperationTimings(
                                                                                            iterations=iterations)
        self.memory_usage = memory_usage if memory_usage is not None else MemoryUsage(
                                                                            iterations=iterations)
        self.peak_memory_usage = peak_memory_usage if peak_memory_usage is not None else PeakMemoryUsage(
                                                                                            iterations=iterations)
        self.custom_metrics = custom_metrics if custom_metrics is not None else CustomMetrics(
                                                                                            iterations=iterations)
        self.total_elapsed = total_elapsed
        self.variation_marks = variation_marks if variation_marks is not None else {}
        self.extra_info = extra_info if extra_info is not None else {}

    @property
    def group(self) -> str:
        """The reporting group to which the benchmark case belongs."""
        return self._group

    @group.setter
    def group(self, value: str) -> None:
        if not isinstance(value, str):
            raise SimpleBenchTypeError(
                f'Invalid group type: {type(value)}. Must be of type str.',
                tag=ErrorTag.RESULTS_GROUP_INVALID_ARG_TYPE
            )
        if value == '':
            raise SimpleBenchValueError(
                'Invalid group value: empty string. Group must be a non-empty string.',
                tag=ErrorTag.RESULTS_GROUP_INVALID_ARG_VALUE
            )
        self._group = value

    @property
    def title(self) -> str:
        """The name of the benchmark case."""
        return self._title

    @title.setter
    def title(self, value: str) -> None:
        if not isinstance(value, str):
            raise SimpleBenchTypeError(
                f'Invalid title type: {type(value)}. Must be of type str.',
                tag=ErrorTag.RESULTS_TITLE_INVALID_ARG_TYPE
            )
        if value == '':
            raise SimpleBenchValueError(
                'Invalid title value: empty string. Title must be a non-empty string.',
                tag=ErrorTag.RESULTS_TITLE_INVALID_ARG_VALUE
            )
        self._title = value

    @property
    def description(self) -> str:
        """A brief description of the benchmark case."""
        return self._description

    @description.setter
    def description(self, value: str) -> None:
        if not isinstance(value, str):
            raise SimpleBenchTypeError(
                f'Invalid description type: {type(value)}. Must be of type str.',
                tag=ErrorTag.RESULTS_DESCRIPTION_INVALID_ARG_TYPE
            )
        self._description = value

    @property
    def n(self) -> int:
        """The number of rounds the benchmark ran per iteration."""
        return self._n

    @n.setter
    def n(self, value: int) -> None:
        if not isinstance(value, int):
            raise SimpleBenchTypeError(
                f'Invalid n type: {type(value)}. Must be of type int.',
                tag=ErrorTag.RESULTS_N_INVALID_ARG_TYPE
            )
        if value <= 0:
            raise SimpleBenchValueError(
                f'Invalid n value: {value}. Must be a positive integer.',
                tag=ErrorTag.RESULTS_N_INVALID_ARG_VALUE
            )
        self._n = value

    @property
    def variation_cols(self) -> dict[str, str]:
        """The columns to use for labelling kwarg variations in the benchmark."""
        return self._variation_cols

    @variation_cols.setter
    def variation_cols(self, value: dict[str, str]) -> None:
        if not isinstance(value, dict):
            raise SimpleBenchTypeError(
                f'Invalid variation_cols type: {type(value)}. Must be of type dict.',
                tag=ErrorTag.RESULTS_VARIATION_COLS_INVALID_ARG_TYPE
            )
        for key, val in value.items():
            if not isinstance(key, str):
                raise SimpleBenchTypeError(
                    f'Invalid variation_cols key type: {type(key)}. Must be of type str.',
                    tag=ErrorTag.RESULTS_VARIATION_COLS_INVALID_ARG_KEY_TYPE
                )
            if key == '':
                raise SimpleBenchValueError(
                    'Invalid variation_cols key value: empty string. Keys must be non-empty strings.',
                    tag=ErrorTag.RESULTS_VARIATION_COLS_INVALID_ARG_KEY_VALUE
                )
            if not isinstance(val, str):
                raise SimpleBenchTypeError(
                    f'Invalid variation_cols value type: {type(val)}. Must be of type str.',
                    tag=ErrorTag.RESULTS_VARIATION_COLS_INVALID_ARG_VALUE_TYPE
                )
        self._variation_cols = value

    @property
    def interval_unit(self) -> str:
        """The unit of measurement for the interval (e.g. "ns")."""
        return self._interval_unit

    @interval_unit.setter
    def interval_unit(self, value: str) -> None:
        if not isinstance(value, str):
            raise SimpleBenchTypeError(
                f'Invalid interval_unit type: {type(value)}. Must be of type str.',
                tag=ErrorTag.RESULTS_INTERVAL_UNIT_INVALID_ARG_TYPE
            )
        if value == '':
            raise SimpleBenchValueError(
                'Invalid interval_unit value: empty string. Interval unit must be a non-empty string.',
                tag=ErrorTag.RESULTS_INTERVAL_UNIT_INVALID_ARG_VALUE
            )
        self._interval_unit = value

    @property
    def interval_scale(self) -> float:
        """The scale factor for the interval (e.g. 1e-9 for nanoseconds)."""
        return self._interval_scale

    @interval_scale.setter
    def interval_scale(self, value: float) -> None:
        if not isinstance(value, (float)):
            raise SimpleBenchTypeError(
                f'Invalid interval_scale type: {type(value)}. Must be of type float.',
                tag=ErrorTag.RESULTS_INTERVAL_SCALE_INVALID_ARG_TYPE
            )
        if value <= 0:
            raise SimpleBenchValueError(
                f'Invalid interval_scale value: {value}. Must be a positive number.',
                tag=ErrorTag.RESULTS_INTERVAL_SCALE_INVALID_ARG_VALUE
            )
        self._interval_scale = value

    @property
    def ops_per_interval_unit(self) -> str:
        """The unit of measurement for operations per interval (e.g. "ops/s")."""
        return self._ops_per_interval_unit

    @ops_per_interval_unit.setter
    def ops_per_interval_unit(self, value: str) -> None:
        if not isinstance(value, str):
            raise SimpleBenchTypeError(
                f'Invalid ops_per_interval_unit type: {type(value)}. Must be of type str.',
                tag=ErrorTag.RESULTS_OPS_PER_INTERVAL_UNIT_INVALID_ARG_TYPE
            )
        if value == '':
            raise SimpleBenchValueError(
                'Invalid ops_per_interval_unit value: empty string. Ops per interval unit must be a non-empty string.',
                tag=ErrorTag.RESULTS_OPS_PER_INTERVAL_UNIT_INVALID_ARG_VALUE
            )
        self._ops_per_interval_unit = value

    @property
    def ops_per_interval_scale(self) -> float:
        """The scale factor for operations per interval (e.g. 1.0 for ops/s)."""
        return self._ops_per_interval_scale

    @ops_per_interval_scale.setter
    def ops_per_interval_scale(self, value: float) -> None:
        if not isinstance(value, (int, float)):
            raise SimpleBenchTypeError(
                f'Invalid ops_per_interval_scale type: {type(value)}. Must be of type float.',
                tag=ErrorTag.RESULTS_OPS_PER_INTERVAL_SCALE_INVALID_ARG_TYPE
            )
        if value <= 0:
            raise SimpleBenchValueError(
                f'Invalid ops_per_interval_scale value: {value}. Must be a positive number.',
                tag=ErrorTag.RESULTS_OPS_PER_INTERVAL_SCALE_INVALID_ARG_VALUE
            )
        self._ops_per_interval_scale = float(value)

    @property
    def custom_metrics_unit(self) -> str:
        """The unit of measurement for custom metrics (e.g. "units")."""
        return self._custom_metrics_unit

    @custom_metrics_unit.setter
    def custom_metrics_unit(self, value: str) -> None:
        if not isinstance(value, str):
            raise SimpleBenchTypeError(
                f'Invalid custom_metrics_unit type: {type(value)}. Must be of type str.',
                tag=ErrorTag.RESULTS_CUSTOM_METRICS_UNIT_INVALID_ARG_TYPE
            )
        if value == '':
            raise SimpleBenchValueError(
                'Invalid custom_metrics_unit value: empty string. Custom metric unit must be a non-empty string.',
                tag=ErrorTag.RESULTS_CUSTOM_METRICS_UNIT_INVALID_ARG_VALUE
            )
        self._custom_metrics_unit = value

    @property
    def custom_metrics_scale(self) -> float:
        """The scale factor for custom metrics (e.g. 1.0 for units)."""
        return self._custom_metrics_scale

    @custom_metrics_scale.setter
    def custom_metrics_scale(self, value: float) -> None:
        if not isinstance(value, (int, float)):
            raise SimpleBenchTypeError(
                f'Invalid custom_metrics_scale type: {type(value)}. Must be of type float.',
                tag=ErrorTag.RESULTS_CUSTOM_METRICS_SCALE_INVALID_ARG_TYPE
            )
        self._custom_metrics_scale = float(value)

    @property
    def iterations(self) -> list[Iteration]:
        """The list of Iteration objects representing each iteration of the benchmark."""
        return self._iterations

    @iterations.setter
    def iterations(self, value: list[Iteration]) -> None:
        if not isinstance(value, list):
            raise SimpleBenchTypeError(
                f'Invalid iterations type: {type(value)}. Must be of type list.',
                tag=ErrorTag.RESULTS_ITERATIONS_INVALID_ARG_TYPE
            )
        for iteration in value:
            if not isinstance(iteration, Iteration):
                raise SimpleBenchTypeError(
                    f'Invalid iteration element type: {type(iteration)}. Must be of type Iteration.',
                    tag=ErrorTag.RESULTS_ITERATIONS_INVALID_ARG_IN_SEQUENCE
                )
        self._iterations = value

    @property
    def ops_per_second(self) -> OperationsPerInterval:
        """Statistics for operations per interval."""
        return self._ops_per_second

    @ops_per_second.setter
    def ops_per_second(self, value: OperationsPerInterval) -> None:
        if not isinstance(value, OperationsPerInterval):
            raise SimpleBenchTypeError(
                f'Invalid ops_per_second type: {type(value)}. Must be of type OperationsPerInterval.',
                tag=ErrorTag.RESULTS_OPS_PER_SECOND_INVALID_ARG_TYPE
            )
        self._ops_per_second = value

    @property
    def per_round_timings(self) -> OperationTimings:
        """Statistics for per-round timings."""
        return self._per_round_timings

    @per_round_timings.setter
    def per_round_timings(self, value: OperationTimings) -> None:
        if not isinstance(value, OperationTimings):
            raise SimpleBenchTypeError(
                f'Invalid per_round_timings type: {type(value)}. Must be of type OperationTimings.',
                tag=ErrorTag.RESULTS_PER_ROUND_TIMINGS_INVALID_ARG_TYPE
            )
        self._per_round_timings = value

    @property
    def memory_usage(self) -> MemoryUsage:
        """Statistics for memory usage."""
        return self._memory_usage

    @memory_usage.setter
    def memory_usage(self, value: MemoryUsage) -> None:
        if not isinstance(value, MemoryUsage):
            raise SimpleBenchTypeError(
                f'Invalid memory_usage type: {type(value)}. Must be of type MemoryUsage.',
                tag=ErrorTag.RESULTS_MEMORY_USAGE_INVALID_ARG_TYPE
            )
        self._memory_usage = value

    @property
    def peak_memory_usage(self) -> PeakMemoryUsage:
        """Statistics for peak memory usage."""
        return self._peak_memory_usage

    @peak_memory_usage.setter
    def peak_memory_usage(self, value: PeakMemoryUsage) -> None:
        if not isinstance(value, PeakMemoryUsage):
            raise SimpleBenchTypeError(
                f'Invalid peak_memory_usage type: {type(value)}. Must be of type PeakMemoryUsage.',
                tag=ErrorTag.RESULTS_PEAK_MEMORY_USAGE_INVALID_ARG_TYPE
            )
        self._peak_memory_usage = value

    @property
    def custom_metrics(self) -> CustomMetrics:
        """Statistics for custom metrics."""
        return self._custom_metrics

    @custom_metrics.setter
    def custom_metrics(self, value: CustomMetrics) -> None:
        if not isinstance(value, CustomMetrics):
            raise SimpleBenchTypeError(
                f'Invalid custom_metrics type: {type(value)}. Must be of type CustomMetrics.',
                tag=ErrorTag.RESULTS_CUSTOM_METRICS_INVALID_ARG_TYPE
            )
        self._custom_metrics = value

    @property
    def total_elapsed(self) -> float:
        """The total elapsed time for the benchmark."""
        return self._total_elapsed

    @total_elapsed.setter
    def total_elapsed(self, value: float) -> None:
        if not isinstance(value, float):
            raise SimpleBenchTypeError(
                f'Invalid total_elapsed type: {type(value)}. Must be of type float or int.',
                tag=ErrorTag.RESULTS_TOTAL_ELAPSED_INVALID_ARG_TYPE
            )
        if value < 0:
            raise SimpleBenchValueError(
                f'Invalid total_elapsed value: {value}. Must be a non-negative number.',
                tag=ErrorTag.RESULTS_TOTAL_ELAPSED_INVALID_ARG_VALUE
            )
        self._total_elapsed = value

    @property
    def variation_marks(self) -> dict[str, Any]:
        """A dictionary of variation marks used to identify the benchmark variation."""
        return self._variation_marks

    @variation_marks.setter
    def variation_marks(self, value: dict[str, Any]) -> None:
        if not isinstance(value, dict):
            raise SimpleBenchTypeError(
                f'Invalid variation_marks type: {type(value)}. Must be of type dict.',
                tag=ErrorTag.RESULTS_VARIATION_MARKS_INVALID_ARG_TYPE
            )
        for key in value.keys():
            if not isinstance(key, str):
                raise SimpleBenchTypeError(
                    f'Invalid variation_marks key type: {type(key)}. Must be of type str.',
                    tag=ErrorTag.RESULTS_VARIATION_MARKS_INVALID_ARG_KEY_TYPE
                )
        self._variation_marks = value

    @property
    def extra_info(self) -> dict[str, Any]:
        """Additional information about the benchmark run."""
        return self._extra_info

    @extra_info.setter
    def extra_info(self, value: dict[str, Any]) -> None:
        if not isinstance(value, dict):
            raise SimpleBenchTypeError(
                f'Invalid extra_info type: {type(value)}. Must be of type dict.',
                tag=ErrorTag.RESULTS_EXTRA_INFO_INVALID_ARG_TYPE
            )
        self._extra_info = value

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
                tag=ErrorTag.RESULTS_RESULTS_SECTION_INVALID_SECTION_ARG_TYPE
            )
        match section:
            case Section.OPS:
                return self.ops_per_second
            case Section.TIMING:
                return self.per_round_timings
            case Section.MEMORY:
                return self.memory_usage
            case Section.PEAK_MEMORY:
                return self.peak_memory_usage
            case Section.CUSTOM:
                return self.custom_metrics
            case _:
                raise SimpleBenchValueError(
                    f'Invalid section: {section}. Must be Section.OPS or Section.TIMING.',
                    tag=ErrorTag.RESULTS_RESULTS_SECTION_UNSUPPORTED_SECTION_ARG_VALUE
                )

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
            'memory_usage_unit': self.memory_usage_unit,
            'memory_usage_scale': self.memory_usage_scale,
            'peak_memory_usage_unit': self.peak_memory_usage_unit,
            'peak_memory_usage_scale': self.peak_memory_usage_scale,
            'total_elapsed': self.total_elapsed,
            'extra_info': self.extra_info,
            'per_round_timings': self.per_round_timings.statistics_as_dict,
            'ops_per_second': self.ops_per_second.statistics_as_dict,
            'memory_usage': self.memory_usage.statistics_as_dict,
            'peak_memory_usage': self.peak_memory_usage.statistics_as_dict,
            'custom_metrics': self.custom_metrics.statistics_as_dict,
        }

    @property
    def results_and_data_as_dict(self) -> dict[str, str | float | dict[int, float] | dict[str, Any]]:
        '''Returns the benchmark results and iterations as a JSON-serializable dictionary.'''
        results = self.results_as_dict
        results['per_round_timings'] = self.per_round_timings.statistics_and_data_as_dict
        results['ops_per_second'] = self.ops_per_second.statistics_and_data_as_dict
        results['memory_usage'] = self.memory_usage.statistics_and_data_as_dict
        results['peak_memory_usage'] = self.peak_memory_usage.statistics_and_data_as_dict
        results['custom_metrics'] = self.custom_metrics.statistics_and_data_as_dict
        return results
