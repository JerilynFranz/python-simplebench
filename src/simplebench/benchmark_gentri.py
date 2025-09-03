#!env python3
# -*- coding: utf-8 -*-
'''
Benchmark for the Generalized Trie implementation.
This script runs a series of tests to measure the performance of the Generalized Trie
against a set of predefined test cases.
'''
# pylint: disable=wrong-import-position, too-many-instance-attributes
# pylint: disable=too-many-positional-arguments, too-many-arguments, too-many-locals
# pyright: reportUnnecessaryIsInstance=false

from argparse import ArgumentParser, Namespace
import csv
from datetime import datetime
from functools import cache
from dataclasses import dataclass, field
import gc
import gzip
import itertools
import json
import math
from pathlib import Path
import re
import statistics
import time
from typing import Any, Callable, Literal, Optional, Sequence

import matplotlib as mpl
import matplotlib.pyplot as plt
import pandas as pd
from rich.progress import Progress, TaskID
from rich.table import Table
import seaborn as sns
from gentrie import GeneralizedTrie, GeneralizedKey, TrieId


PROGRESS = Progress(refresh_per_second=5)
"""Progress bar for benchmarking."""

TASKS: dict[str, TaskID] = {}
"""Task IDs for the progress bar."""

MIN_MEASURED_ITERATIONS: int = 3
"""Minimum number of iterations for statistical analysis."""

DEFAULT_ITERATIONS: int = 20
"""Default number of iterations for benchmarking."""

DEFAULT_TIMER = time.perf_counter_ns
"""Default timer function for benchmarking."""

DEFAULT_INTERVAL_SCALE: float = 1e-9
"""Default scaling factor for time intervals (nanoseconds -> seconds)."""

DEFAULT_INTERVAL_UNIT: str = 'ns'
"""Default unit for time intervals (nanoseconds)."""

BASE_INTERVAL_UNIT: str = 's'
"""Base unit for time intervals."""

DEFAULT_OPS_PER_INTERVAL_SCALE: float = 1.0
"""Default scaling factor for operations per interval (1.0 -> 1.0)."""

DEFAULT_OPS_PER_INTERVAL_UNIT: str = 'Ops/s'
"""Default unit for operations per interval (operations per second)."""

BASE_OPS_PER_INTERVAL_UNIT: str = 'Ops/s'
"""Base unit for operations per interval."""

DEFAULT_SIGNIFICANT_FIGURES: int = 3
"""Default number of significant figures for output values (3 significant figures)."""


def generate_test_data(depth: int, symbols: str, max_keys: int) -> list[str]:
    '''Generate test data for the Generalized Trie.

    Args:
        depth (int): The depth of the keys to generate.
        symbols (str): The symbols to use in the keys.
        max_keys (int): The maximum number of keys to generate.'''
    test_data: list[str] = []
    for key in itertools.product(symbols, repeat=depth):
        key_string = ''.join(key)
        test_data.append(key_string)
        if len(test_data) >= max_keys:
            break
    return test_data


def generate_test_trie(depth: int,
                       symbols: str,
                       max_keys: int,
                       value: Optional[Any] = None,
                       runtime_validation: bool = True) -> GeneralizedTrie:
    '''Generate a test Generalized Trie for the given depth and symbols.

    Args:
        depth (int): The depth of the trie.
        symbols (str): The symbols to use in the trie.
        max_keys (int): The maximum number of keys to generate.
        value (Optional[Any]): The value to assign to each key in the trie.
        runtime_validation (bool): Whether to enable runtime validation on the returned trie. (default: True)

    Returns:
        GeneralizedTrie: The generated trie with the specified keys and values.
    '''
    return generate_test_trie_from_data(
        data=generate_test_data(depth, symbols, max_keys),
        value=value,
        runtime_validation=runtime_validation)


def generate_test_trie_from_data(
        data: Sequence[GeneralizedKey],
        value: Optional[Any] = None,
        runtime_validation: bool = True) -> GeneralizedTrie:
    '''Generate a test Generalized Trie from the passed Sequence of GeneralizedKey.

    Args:
        data (Sequence[GeneralizedKey]): The sequence of keys to insert into the trie.
        value (Optional[Any]): The value to assign to each key in the trie.
        runtime_validation (bool): Whether to enable runtime validation on the returned trie. (default: True)

    Returns:
        GeneralizedTrie: The generated trie with the specified keys and values.
    '''
    trie = GeneralizedTrie(runtime_validation=False)
    for key in data:
        trie[key] = value
    trie.runtime_validation = runtime_validation
    return trie


def generate_trie_with_missing_key_from_data(
        test_data: Sequence[GeneralizedKey], value: Optional[Any] = None) -> tuple[GeneralizedTrie, Any]:
    """Generate a GeneralizedTrie and a key that is not in the trie.

    The generated trie will contain all keys from the test_data except for the last one.

    Args:
        test_data: The test data to populate the trie.
        value: The value to associate with the keys in the trie.
    """
    trie = generate_test_trie_from_data(data=test_data, value=value)
    missing_key = test_data[-1]  # Use the last key as the missing key
    trie.remove(missing_key)  # Ensure the key is not actually in the trie
    return trie, missing_key


def generate_fully_populated_trie(test_data: dict[int, list[str]],
                                  symbols: str,
                                  max_depth: int,
                                  value: Optional[Any] = None) -> GeneralizedTrie:
    '''Generate a fully populated Generalized Trie for the given max_depth.

    A fully populated trie contains all possible keys up to the specified depth.
    It uses the pregenerated test_data as the source of truth for the keys for each depth
    because it contains all the possible keys for the depth and symbol set.

    Args:
        max_depth (int): The maximum depth of the trie.
        value (Optional[Any], default=None): The value to assign to each key in the trie.
    '''
    trie = GeneralizedTrie(runtime_validation=False)
    # Use precomputed test_data if available for performance
    for depth, data in test_data.items():
        if depth <= max_depth:
            for key in data:
                trie[key] = value

    # Generate any requested depths NOT included in test_data
    for depth in range(1, max_depth + 1):
        if depth not in test_data:
            # Generate all possible keys for this depth
            for key in generate_test_data(depth, symbols, len(symbols) ** depth):
                trie[key] = value

    return trie


@cache
def load_english_words():
    """Imports English words from a gzipped text file.

    The file contains a bit over 278 thousand words in English
    (one per line).
    """
    words_file = Path(__file__).parent.joinpath("english_words.txt.gz")
    return list(map(str.rstrip, gzip.open(words_file, "rt")))


# TODO: Implement a formatting function to correctly format and decimal align significant figures

class BenchmarkUtils:
    '''Benchmarking utility class.'''

    def sanitize_filename(self, name: str) -> str:
        """Sanitizes a filename by replacing invalid characters with _.

        Only 'a-z', 'A-Z', '0-9', '_', and '-' are allowed. All other characters
        are replaced with '_' and multiple sequential '_' characters are then collapsed to
        single '_' characters.

        Args:
            name (str): The filename to sanitize.

        Returns:
            str: The sanitized filename.
        """
        first_pass: str = re.sub(r'[^a-zA-Z0-9_-]+', '_', name)
        return re.sub(r'_+', '_', first_pass)

    def si_scale_for_smallest(self, numbers: list[float], base_unit: str) -> tuple[str, float]:
        """Scale factor and SI unit for the smallest in list of numbers.

        The scale factor is the factor that will be applied to the numbers to convert
        them to the desired unit. The SI unit is the unit that corresponds to the scale factor.

        If passed only one number, it effectively gives the scale for that single number.
        If passed a list, it gives the scale for the smallest absolute value in the list.

        Args:
            numbers: A list of numbers to scale.
            base_unit: The base unit to use for scaling.

        Returns:
            A tuple containing the scaled unit and the scaling factor.
        """
        # smallest absolute number in list
        min_n: float = min([abs(n) for n in numbers])
        unit: str = ''
        scale: float = 1.0
        if min_n >= 1e12:
            unit, scale = 'T' + base_unit, 1e-12
        elif min_n >= 1e9:
            unit, scale = 'G' + base_unit, 1e-9
        elif min_n >= 1e6:
            unit, scale = 'M' + base_unit, 1e-6
        elif min_n >= 1e3:
            unit, scale = 'K' + base_unit, 1e-3
        elif min_n >= 1e0:
            unit, scale = base_unit, 1.0
        elif min_n >= 1e-3:
            unit, scale = 'm' + base_unit, 1e3
        elif min_n >= 1e-6:
            unit, scale = 'μ' + base_unit, 1e6
        elif min_n >= 1e-9:
            unit, scale = 'n' + base_unit, 1e9
        elif min_n >= 1e-12:
            unit, scale = 'p' + base_unit, 1e12
        return unit, scale

    def si_scale(self, unit: str, base_unit: str) -> float:
        """Get the SI scale factor for a unit given the base unit.

        This method will return the scale factor for the given unit
        relative to the base unit for SI prefixes ranging from tera (T)
        to pico (p).

        Args:
            unit (str): The unit to get the scale factor for.
            base_unit (str): The base unit.

        Returns:
            The scale factor for the given unit.

        Raises:
            ValueError: If the SI unit is not recognized.
        """
        si_prefixes = {
            f'T{base_unit}': 1e12,
            f'G{base_unit}': 1e9,
            f'M{base_unit}': 1e6,
            f'K{base_unit}': 1e3,
            f'{base_unit}': 1.0,
            f'm{base_unit}': 1e-3,
            f'μ{base_unit}': 1e-6,
            f'n{base_unit}': 1e-9,
            f'p{base_unit}': 1e-12,
        }
        if unit in si_prefixes:
            return si_prefixes[unit]
        raise ValueError(f'Unknown SI unit: {unit}')

    def si_scale_to_unit(self, base_unit: str, current_unit: str, target_unit: str) -> float:
        """Scale factor to convert a current SI unit to a target SI unit based on their SI prefixes.

        Example:
        scale_by: float = self.si_scale_to_unit(base_unit='s', current_unit='s', target_unit='ns')

        Args:
            numbers: A list of numbers to scale.
            current_unit: The base unit to use for unscaling.

        Returns:
            The scaling factor to return the number to the base unit
        """
        current_scale = self.si_scale(current_unit, base_unit)
        target_scale = self.si_scale(target_unit, base_unit)
        return target_scale / current_scale

    def sigfigs(self, number: float, figures: int = DEFAULT_SIGNIFICANT_FIGURES) -> float:
        """Rounds a floating point number to the specified number of significant figures.

        If the number of significant figures is not specified, it defaults to
        DEFAULT_SIGNIFICANT_FIGURES.

        * 14.2 to 2 digits of significant figures becomes 14
        * 0.234 to 2 digits of significant figures becomes 0.23
        * 0.0234 to 2 digits of significant figures becomes 0.023
        * 14.5 to 2 digits of significant figures becomes 15
        * 0.235 to 2 digits of significant figures becomes 0.24

        Args:
            number (float): The number to round.
            figures (int): The number of significant figures to round to.

        Returns:
            The rounded number as a float.

        Raises:
            TypeError: If the number arg is not a float or the figures arg is not an int.
            ValueError: If the figures arg is not at least 1.
        """
        if not isinstance(number, float):
            raise TypeError("number arg must be a float")
        if not isinstance(figures, int):
            raise TypeError("figures arg must be an int")
        if figures < 1:
            raise ValueError("figures arg must be at least 1")

        if number == 0.0:
            return 0.0
        return round(number, figures - int(math.floor(math.log10(abs(number)))) - 1)


@dataclass(kw_only=True)
class BenchIteration:
    '''Container for the results of a single benchmark iteration.

    Properties:
        n (int): The number of rounds performed in the iteration.
        elapsed (float): The elapsed time for the operations.
        unit (str): The unit of measurement for the elapsed time.
        scale (float): The scale factor for the elapsed time.
        ops_per_second (float): The number of operations per second. (read only)
        per_round_elapsed (float): The mean time for a single round scaled to the base unit. (read only)
    '''
    n: int = 0
    elapsed: int = 0
    unit: str = DEFAULT_INTERVAL_UNIT
    scale: float = DEFAULT_INTERVAL_SCALE

    @property
    def per_round_elapsed(self) -> float:
        '''The mean time for a single round scaled to the base unit.
        If elapsed is 0, returns 0.0

        The per round computation is the elapsed time divided by n
        where n is the number of rounds.

        The scaling to the base unit is done using the scale factor.
        This has the effect of converting the elapsed time into the base unit.
        For example, if the scale factor is 1e-9 then elapsed time in nanoseconds
        will be converted to seconds.

        Returns:
            The mean time for a single round scaled to the base unit.
        '''
        return self.elapsed * self.scale / self.n if self.n else 0.0

    @property
    def ops_per_second(self) -> float:
        '''The number of operations per second.

        This is calculated as the inverse of the elapsed time.

        The edge cases of 0 elapsed time or n results in a returned value of 0.
        This would otherwise be an impossible value and so flags a measurement error.
        '''
        if not self.elapsed:
            return 0
        return self.n / (self.elapsed * self.scale)


class BenchStatistics:
    '''Generic container for statistics on a benchmark.

    Attributes:
        unit (str): The unit of measurement for the benchmark (e.g., "ops/s").
        scale (float): The scale factor for the interval (e.g. 1 for seconds).
        data: list[int | float] = field(default_factory=list[int | float])
        mean (float): The mean operations per time interval. (read only)
        median (float): The median operations per time interval. (read only)
        minimum (float): The minimum operations per time interval. (read only)
        maximum (float): The maximum operations per time interval. (read only)
        standard_deviation (float): The standard deviation of operations per time interval. (read only)
        relative_standard_deviation (float): The relative standard deviation of ops per time interval. (read only)
        percentiles (dict[int, float]): Percentiles of operations per time interval. (read only)
    '''
    def __init__(self, unit: str = '', scale: float = 0.0, data: Optional[list[int | float]] = None):
        self.unit: str = unit
        self.scale: float = scale
        self.data: list[int | float] = data if data is not None else []

    @property
    def mean(self) -> float:
        '''The mean of the data.'''
        return statistics.mean(self.data) if self.data else 0.0

    @property
    def median(self) -> float:
        '''The median of the data.'''
        return statistics.median(self.data) if self.data else 0.0

    @property
    def minimum(self) -> float:
        '''The minimum of the data.'''
        return float(min(self.data)) if self.data else 0.0

    @property
    def maximum(self) -> float:
        '''The maximum of the data.'''
        return float(max(self.data)) if self.data else 0.0

    @property
    def standard_deviation(self) -> float:
        '''The standard deviation of the data.'''
        return statistics.stdev(self.data) if len(self.data) > 1 else 0.0

    @property
    def relative_standard_deviation(self):
        '''The relative standard deviation of the data.'''
        return self.standard_deviation / self.mean * 100 if self.mean else 0.0

    @property
    def percentiles(self) -> dict[int, float]:
        '''Percentiles of the data.

        Computes the 5th, 10th, 25th, 50th, 75th, 90th, and 95th percentiles
        and returns them as a dictionary keyed by percent.
        '''
        # Calculate percentiles if we have enough data points
        if not self.data:
            return {p: float('nan') for p in [5, 10, 25, 50, 75, 90, 95]}
        percentiles: dict[int, float] = {}
        for percent in [5, 10, 25, 50, 75, 90, 95]:
            percentiles[percent] = statistics.quantiles(self.data, n=100)[percent - 1]
        return percentiles

    @property
    def statistics_as_dict(self) -> dict[str, str | float | dict[int, float] | list[int | float]]:
        '''Returns the statistics as a JSON-serializable dictionary.'''
        return {
            'type': f'{self.__class__.__name__}:statistics',
            'unit': self.unit,
            'scale': self.scale,
            'mean': self.mean / self.scale if self.scale else self.mean,
            'median': self.median / self.scale if self.scale else self.median,
            'minimum': self.minimum / self.scale if self.scale else self.minimum,
            'maximum': self.maximum / self.scale if self.scale else self.maximum,
            'standard_deviation': self.standard_deviation / self.scale if self.scale else self.standard_deviation,
            'relative_standard_deviation': self.relative_standard_deviation,
            'percentiles': self.percentiles,
        }

    @property
    def statistics_and_data_as_dict(self) -> dict[
            str, str | float | dict[int, float] | list[int | float]]:
        '''Returns the statistics and data as a JSON-serializable dictionary.'''
        stats: dict[str, str | float | dict[int, float] | list[int | float]] = self.statistics_as_dict
        stats['data'] = [value / self.scale for value in self.data]
        return stats


class BenchOperationsPerInterval(BenchStatistics):
    '''Container for the operations per time interval statistics of a benchmark.

    Attributes:
        unit (str): The unit of measurement for the benchmark (e.g., "ops/s").
        scale (float): The scale factor for the interval (e.g. 1 for seconds).
        data: list[int] = field(default_factory=list[int])
        mean (float): The mean operations per time interval. (read only)
        median (float): The median operations per time interval. (read only)
        minimum (float): The minimum operations per time interval. (read only)
        maximum (float): The maximum operations per time interval. (read only)
        standard_deviation (float): The standard deviation of operations per time interval. (read only)
        relative_standard_deviation (float): The relative standard deviation of ops per time interval. (read only)
        percentiles (dict[int, float]): Percentiles of operations per time interval. (read only)
    '''
    def __init__(self,
                 unit: str = DEFAULT_OPS_PER_INTERVAL_UNIT,
                 scale: float = DEFAULT_OPS_PER_INTERVAL_SCALE,
                 data: Optional[list[int | float]] = None):
        super().__init__(unit=unit, scale=scale, data=data)


class BenchOperationTimings(BenchStatistics):
    '''Container for the operation timing statistics of a benchmark.

    Attributes:
        unit (str): The unit of measurement for the timings (e.g., "ns").
        scale (float): The scale factor for the timings (e.g., "1e-9" for nanoseconds).
        mean (float): The mean time per operation.
        median (float): The median time per operation.
        minimum (float): The minimum time per operation.
        maximum (float): The maximum time per operation.
        standard_deviation (float): The standard deviation of the time per operation.
        relative_standard_deviation (float): The relative standard deviation of the time per operation.
        percentiles (dict[int, float]): Percentiles of time per operation.
        data: list[float | int] = field(default_factory=list[float | int])
    '''
    def __init__(self,
                 unit: str = DEFAULT_INTERVAL_UNIT,
                 scale: float = DEFAULT_INTERVAL_SCALE,
                 data: Optional[list[int | float]] = None):
        super().__init__(unit=unit, scale=scale, data=data)


@dataclass(kw_only=True)
class BenchResults:
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
    iterations: list[BenchIteration] = field(default_factory=list[BenchIteration])
    ops_per_second: BenchOperationsPerInterval = field(default_factory=BenchOperationsPerInterval)
    per_round_timings: BenchOperationTimings = field(default_factory=BenchOperationTimings)
    total_elapsed: int = 0
    variation_marks: dict[str, Any] = field(default_factory=dict[str, Any])
    extra_info: dict[str, Any] = field(default_factory=dict[str, Any])

    def __post_init__(self):
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


@dataclass(kw_only=True)
class BenchCase:
    '''Declaration of a benchmark case.

    kwargs_variations are used to describe the variations in keyword arguments for the benchmark.
    All combinations of these variations will be tested.

    kwargs_variations example:
        kwargs_variations={
            'search_depth': [1, 2, 3],
            'runtime_validation': [True, False]
        }

    Args:
        group (str): The benchmark reporting group to which the benchmark case belongs.
        title (str): The name of the benchmark case.
        description (str): A brief description of the benchmark case.
        action (Callable[..., Any]): The action to perform for the benchmark.
        iterations (int): The number of iterations to run for the benchmark.
        min_time (float): The minimum time for the benchmark in seconds. (default: 5.0)
        max_time (float): The maximum time for the benchmark in seconds. (default: 20.0)
        variation_cols (dict[str, str]): kwargs to be used for cols to denote kwarg variations.
        kwargs_variations (dict[str, list[Any]]): Variations of keyword arguments for the benchmark.
        runner (Optional[Callable[..., Any]]): A custom runner for the benchmark.
        verbose (bool): Enable verbose output.
        progress (bool): Enable progress output.
        graph_aspect_ratio (float): The aspect ratio of the graph (default: 1.0).
        graph_style (Literal['default', 'dark_background']): The style of the graph (default: 'default').
        graph_y_starts_at_zero (bool): Whether the y-axis of the graph starts at zero (default: True).
        graph_x_labels_rotation (float): The rotation angle of the x-axis tick labels (default: 0.0).

    Properties:
        results (list[BenchResults]): The benchmark results for the case.
    '''
    group: str
    title: str
    description: str
    action: Callable[..., Any]
    iterations: int = DEFAULT_ITERATIONS
    min_time: float = 5.0  # seconds
    max_time: float = 20.0  # seconds
    variation_cols: dict[str, str] = field(default_factory=dict[str, str])
    kwargs_variations: dict[str, list[Any]] = field(default_factory=dict[str, list[Any]])
    runner: Optional[Callable[..., Any]] = None
    verbose: bool = False
    progress: bool = False
    variations_task: Optional[TaskID] = None
    graph_aspect_ratio: float = 1.0
    graph_style: Literal['default', 'dark_background'] = 'default'
    graph_y_starts_at_zero: bool = True
    graph_x_labels_rotation: float = 0.0

    def __post_init__(self):
        self.results: list[BenchResults] = []

    @property
    def expanded_kwargs_variations(self) -> list[dict[str, Any]]:
        '''All combinations of keyword arguments from the specified kwargs_variations.

        Returns:
            A list of dictionaries, each representing a unique combination of keyword arguments.
        '''
        keys = self.kwargs_variations.keys()
        values = [self.kwargs_variations[key] for key in keys]
        return [dict(zip(keys, v)) for v in itertools.product(*values)]

    def run(self):
        """Run the benchmark tests.

        This method will execute the benchmark for each combination of
        keyword arguments and collect the results. After running the
        benchmarks, the results will be stored in the `self.results` attribute.
        """
        all_variations = self.expanded_kwargs_variations
        task_name: str = 'variations'
        if task_name not in TASKS and self.progress:
            TASKS[task_name] = PROGRESS.add_task(
                description=f'[cyan] Running case {self.title}',
                total=len(all_variations))
        if task_name in TASKS:
            PROGRESS.reset(TASKS[task_name])
            PROGRESS.update(task_id=TASKS[task_name],
                            description=f'[cyan] Running case {self.title}',
                            total=len(all_variations))
        if task_name in TASKS:
            PROGRESS.start_task(TASKS[task_name])
        collected_results: list[BenchResults] = []
        kwargs: dict[str, Any]
        for variations_counter, kwargs in enumerate(all_variations):
            benchmark: BenchmarkRunner = BenchmarkRunner(case=self, kwargs=kwargs)
            results: BenchResults = self.action(benchmark)
            collected_results.append(results)
            if task_name in TASKS:
                PROGRESS.update(task_id=TASKS[task_name],
                                description=(f'[cyan] Running case {self.title} '
                                             f'({variations_counter + 1}/{len(all_variations)})'),
                                completed=variations_counter + 1,
                                refresh=True)
        if task_name in TASKS:
            PROGRESS.stop_task(TASKS[task_name])
        self.results = collected_results

    def results_as_rich_table(self,
                              base_unit: str,
                              target: Literal['ops_per_second', 'per_round_timings']) -> None:
        """Prints the benchmark results in a rich table format if available.
        """
        utils = BenchmarkUtils()
        mean_unit, mean_scale = utils.si_scale_for_smallest(
            numbers=[getattr(result, target).mean for result in self.results],
            base_unit=base_unit)
        median_unit, median_scale = utils.si_scale_for_smallest(
            numbers=[getattr(result, target).median for result in self.results],
            base_unit=base_unit)
        min_unit, min_scale = utils.si_scale_for_smallest(
            numbers=[getattr(result, target).minimum for result in self.results],
            base_unit=base_unit)
        max_unit, max_scale = utils.si_scale_for_smallest(
            numbers=[getattr(result, target).maximum for result in self.results],
            base_unit=base_unit)
        p5_unit, p5_scale = utils.si_scale_for_smallest(
            numbers=[getattr(result, target).percentiles[5] for result in self.results],
            base_unit=base_unit)
        p95_unit, p95_scale = utils.si_scale_for_smallest(
            numbers=[getattr(result, target).percentiles[95] for result in self.results],
            base_unit=base_unit)
        stddev_unit, stddev_scale = utils.si_scale_for_smallest(
            numbers=[getattr(result, target).standard_deviation for result in self.results],
            base_unit=base_unit)

        table = Table(title=(self.title + '\n\n' + self.description),
                      show_header=True,
                      title_style='bold green1',
                      header_style='bold magenta')
        table.add_column('N', justify='center')
        table.add_column('Iterations', justify='center')
        table.add_column('Elapsed Seconds', justify='center', max_width=7)
        table.add_column(f'mean {mean_unit}', justify='center', vertical='bottom', overflow='fold')
        table.add_column(f'median {median_unit}', justify='center', vertical='bottom', overflow='fold')
        table.add_column(f'min {min_unit}', justify='center', vertical='bottom', overflow='fold')
        table.add_column(f'max {max_unit}', justify='center', vertical='bottom', overflow='fold')
        table.add_column(f'5th {p5_unit}', justify='center', vertical='bottom', overflow='fold')
        table.add_column(f'95th {p95_unit}', justify='center', vertical='bottom', overflow='fold')
        table.add_column(f'std dev {stddev_unit}', justify='center', vertical='bottom', overflow='fold')
        table.add_column('rsd%', justify='center', vertical='bottom', overflow='fold')
        for value in self.variation_cols.values():
            table.add_column(value, justify='center', vertical='bottom', overflow='fold')
        for result in self.results:
            stats_target = getattr(result, target)
            row: list[str] = [
                f'{result.n:>6d}',
                f'{len(result.iterations):>6d}',
                f'{result.total_elapsed * DEFAULT_INTERVAL_SCALE:>4.2f}',
                f'{utils.sigfigs(stats_target.mean * mean_scale):>8.2f}',
                f'{utils.sigfigs(stats_target.median * median_scale):>8.2f}',
                f'{utils.sigfigs(stats_target.minimum * min_scale):>8.2f}',
                f'{utils.sigfigs(stats_target.maximum * max_scale):>8.2f}',
                f'{utils.sigfigs(stats_target.percentiles[5] * p5_scale):>8.2f}',
                f'{utils.sigfigs(stats_target.percentiles[95] * p95_scale):>8.2f}',
                f'{utils.sigfigs(stats_target.standard_deviation * stddev_scale):>8.2f}',
                f'{utils.sigfigs(stats_target.relative_standard_deviation):>5.2f}%'
            ]
            for value in result.variation_marks.values():
                row.append(f'{value!s}')
            table.add_row(*row)
        PROGRESS.console.print(table)

    def ops_results_as_rich_table(self) -> None:
        """Prints the benchmark results in a rich table format if available.
        """
        return self.results_as_rich_table(
            base_unit=BASE_OPS_PER_INTERVAL_UNIT,
            target='ops_per_second'
        )

    def timing_results_as_rich_table(self) -> None:
        """Prints the benchmark results in a rich table format if available.
        """
        return self.results_as_rich_table(
            base_unit=BASE_INTERVAL_UNIT,
            target='per_round_timings'
        )

    def output_results_to_csv(self,
                              filepath: Path,
                              base_unit: str,
                              target: Literal['ops_per_second', 'per_round_timings']) -> None:
        """Output the benchmark results to a file as tagged CSV if available.

        Args:
            filepath: The path to the CSV file to write.
            results: The benchmark results to write.
            target: The target metric to write (either 'ops_per_second' or 'per_round_timings').
        """
        if not self.results:
            return

        utils = BenchmarkUtils()
        all_numbers: list[float] = []
        all_numbers.extend([getattr(result, target).mean for result in self.results])
        all_numbers.extend([getattr(result, target).median for result in self.results])
        all_numbers.extend([getattr(result, target).minimum for result in self.results])
        all_numbers.extend([getattr(result, target).maximum for result in self.results])
        all_numbers.extend([getattr(result, target).percentiles[5] for result in self.results])
        all_numbers.extend([getattr(result, target).percentiles[95] for result in self.results])
        all_numbers.extend([getattr(result, target).standard_deviation for result in self.results])
        common_unit, common_scale = utils.si_scale_for_smallest(numbers=all_numbers, base_unit=base_unit)

        with filepath.open(mode='w', encoding='utf-8', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow([f'# {self.title}'])
            writer.writerow([f'# {self.description}'])
            header: list[str] = [
                'N',
                'Iterations',
                'Elapsed Seconds',
                f'mean ({common_unit})',
                f'median ({common_unit})',
                f'min ({common_unit})',
                f'max ({common_unit})',
                f'5th ({common_unit})',
                f'95th ({common_unit})',
                f'std dev ({common_unit})',
                'rsd (%)'
            ]
            for value in self.variation_cols.values():
                header.append(value)
            writer.writerow(header)
            for result in self.results:
                stats_target = getattr(result, target)
                row: list[str | float | int] = [
                    result.n,
                    len(result.iterations),
                    result.total_elapsed * DEFAULT_INTERVAL_SCALE,
                    utils.sigfigs(stats_target.mean * common_scale),
                    utils.sigfigs(stats_target.median * common_scale),
                    utils.sigfigs(stats_target.minimum * common_scale),
                    utils.sigfigs(stats_target.maximum * common_scale),
                    utils.sigfigs(stats_target.percentiles[5] * common_scale),
                    utils.sigfigs(stats_target.percentiles[95] * common_scale),
                    utils.sigfigs(stats_target.standard_deviation * common_scale),
                    utils.sigfigs(stats_target.relative_standard_deviation)
                ]
                for value in result.variation_marks.values():
                    row.append(value)
                writer.writerow(row)

        return

    def output_ops_results_to_csv(self, filepath: Path) -> None:
        """Output the benchmark results to a file as tagged CSV if available.
        """
        return self.output_results_to_csv(filepath=filepath,
                                          base_unit=BASE_OPS_PER_INTERVAL_UNIT,
                                          target='ops_per_second')

    def output_timing_results_to_csv(self, filepath: Path) -> None:
        """Outputs the timing benchmark results to file as tagged CSV.
        """
        return self.output_results_to_csv(filepath=filepath,
                                          base_unit=BASE_INTERVAL_UNIT,
                                          target='per_round_timings')

    def plot_results(self,
                     filepath: Path,
                     target: Literal['ops_per_second', 'per_round_timings'],
                     base_unit: str = '',
                     target_name: str = ''
                     ) -> None:
        """Generates and saves a bar plot of the ops/sec results.

        Args:
            filepath (Path): The path to the output file.
            target (Literal['ops_per_second', 'per_round_timings']): The target metric to plot.
            base_unit (str): The base unit for the y-axis.
            target_name (str): The name of the target metric.
            scale (float): The scale factor for the y-axis.
        """
        if not self.results:
            return

        utils = BenchmarkUtils()
        all_numbers: list[float] = []
        all_numbers.extend([getattr(result, target).mean for result in self.results])
        common_unit, common_scale = utils.si_scale_for_smallest(numbers=all_numbers, base_unit=base_unit)
        target_name = f'{target_name} ({base_unit})'

        # Prepare data for plotting
        plot_data = []
        x_axis_legend = '\n'.join([f"{self.variation_cols.get(k, k)}"
                                   for k in self.variation_cols.keys()])
        for result in self.results:
            target_stats = getattr(result, target)
            variation_label = '\n'.join([f"{v}" for v in result.variation_marks.values()])
            plot_data.append({
                x_axis_legend: variation_label,
                target_name: target_stats.mean * common_scale,
            })

        if not plot_data:
            return

        # See https://matplotlib.org/stable/users/explain/customizing.html#the-matplotlibrc-file
        benchmarking_theme = {
            'axes.grid': True,
            'grid.linestyle': '-',
            'grid.color': '#444444',
            'legend.framealpha': 1,
            'legend.shadow': True,
            'legend.fontsize': 14,
            'legend.title_fontsize': 16,
            'xtick.labelsize': 12,
            'ytick.labelsize': 12,
            'axes.labelsize': 16,
            'axes.titlesize': 20,
            'figure.dpi': 100}
        mpl.rcParams.update(benchmarking_theme)
        df = pd.DataFrame(plot_data)

        # Create the plot
        plt.style.use(self.graph_style)
        g = sns.relplot(data=df, y=target_name, x=x_axis_legend)
        g.figure.suptitle(self.title, fontsize='large', weight='bold')
        g.figure.subplots_adjust(top=.9)
        g.figure.set_dpi(160)
        g.figure.set_figheight(10)
        g.figure.set_figwidth(10 * self.graph_aspect_ratio)
        g.tick_params("x", rotation=self.graph_x_labels_rotation)
        # format the labels with f-strings
        for ax in g.axes.flat:
            ax.yaxis.set_major_formatter('{x}' + f' {common_unit}')
        if self.graph_y_starts_at_zero:
            _, top = plt.ylim()
            plt.ylim(bottom=0, top=top * 1.10)  # Add 10% headroom
        plt.savefig(filepath)
        plt.close()  # Close the figure to free memory

    def plot_ops_results(self, filepath: Path) -> None:
        """Plots the operations per second results graph.

        Args:
            filepath (Path): The path to the output file.
        """
        if not self.results:
            return
        return self.plot_results(filepath=filepath,
                                 target='ops_per_second',
                                 base_unit=BASE_OPS_PER_INTERVAL_UNIT,
                                 target_name='Operations per Second')

    def plot_timing_results(self, filepath: Path) -> None:
        """Plots the timing results graph.

        Args:
            filepath (Path): The path to the output file.
        """
        return self.plot_results(filepath=filepath,
                                 target='per_round_timings',
                                 base_unit=BASE_INTERVAL_UNIT,
                                 target_name='Time Per Round')

    def as_dict(self, args: Namespace) -> dict[str, Any]:
        """Returns the benchmark case and results as a JSON serializable dict.

        Args:
            args (Namespace): The command line arguments.
        """
        results = []
        for result in self.results:
            if args.json_data:
                results.append(result.results_and_data_as_dict)
            else:
                results.append(result.results_as_dict)
        return {
            'type': self.__class__.__name__,
            'group': self.group,
            'title': self.title,
            'description': self.description,
            'variation_cols': self.variation_cols,
            'results': results
        }


class BenchmarkRunner():
    """A class to run benchmarks for various actions.
    """
    def __init__(self,
                 case: BenchCase,
                 kwargs: dict[str, Any],
                 runner: Optional[Callable[..., Any]] = None):
        self.case: BenchCase = case
        self.kwargs: dict[str, Any] = kwargs
        self.run: Callable[..., Any] = runner if runner is not None else self.default_runner

    @property
    def variation_marks(self) -> dict[str, Any]:
        '''Return the variation marks for the benchmark.

        The variation marks identify the specific variations being tested in a run
        from the kwargs values.
        '''
        return {key: self.kwargs.get(key, None) for key in self.case.variation_cols.keys()}

    def default_runner(
            self,
            n: int,
            action: Callable[..., Any],
            setup: Optional[Callable[..., Any]] = None,
            teardown: Optional[Callable[..., Any]] = None) -> BenchResults:
        """Run a generic benchmark using the specified action and test data for rounds.

        This function will execute the benchmark for the given action and
        collect the results. It is designed for macro-benchmarks (i.e., benchmarks
        that measure the performance of a function over multiple iterations) where
        the overhead of the function call is not significant compared with the work
        done inside the function.

        Micro-benchmarks (i.e., benchmarks that measure the performance of a fast function
        over a small number of iterations) require more complex handling to account
        for the overhead of the function call.

        Args:
            variation_cols (dict[str, str]): The variation columns to use for the benchmark.
            n (int): The number of test rounds that will be run by the action on each iteration.
            action (Callable[..., Any]): The action to benchmark.
            setup (Optional[Callable[..., Any]]): A setup function to run before each iteration.
            teardown (Optional[Callable[..., Any]]): A teardown function to run after each iteration.
        """
        group: str = self.case.group
        title: str = self.case.title
        description: str = self.case.description
        min_time: float = self.case.min_time
        max_time: float = self.case.max_time
        iterations: int = self.case.iterations

        iteration_pass: int = 0
        time_start: int = DEFAULT_TIMER()
        max_stop_at: int = int(max_time / DEFAULT_INTERVAL_SCALE) + time_start
        min_stop_at: int = int(min_time / DEFAULT_INTERVAL_SCALE) + time_start
        wall_time: int = DEFAULT_TIMER()
        iterations_min: int = max(MIN_MEASURED_ITERATIONS, iterations)

        gc.collect()

        tasks_name = 'runner'

        progress_max: float = 100.0
        if self.case.progress and tasks_name not in TASKS:
            TASKS[tasks_name] = PROGRESS.add_task(
                            description=f'[green] Benchmarking {group}',
                            total=progress_max)
        if tasks_name in TASKS:
            PROGRESS.reset(TASKS[tasks_name])
            PROGRESS.update(TASKS[tasks_name],
                            completed=5.0,
                            description=f'[green] Benchmarking {group} (iteration {iteration_pass:<6d}; '
                                        f'time {0.00:<3.2f}s)')
            PROGRESS.start_task(TASKS[tasks_name])
        total_elapsed: float = 0
        iterations_list: list[BenchIteration] = []
        while ((iteration_pass <= iterations_min or wall_time < min_stop_at)
                and wall_time < max_stop_at):
            iteration_pass += 1
            iteration_result = BenchIteration()
            iteration_result.elapsed = 0

            if isinstance(setup, Callable):
                setup()

            # Timer for benchmarked code
            timer_start: int = DEFAULT_TIMER()
            action()
            timer_end: int = DEFAULT_TIMER()

            if isinstance(teardown, Callable):
                teardown()

            if iteration_pass == 1:
                # Warmup iteration, not included in final stats
                continue
            iteration_result.elapsed += (timer_end - timer_start)
            iteration_result.n = n
            total_elapsed += iteration_result.elapsed
            iterations_list.append(iteration_result)
            wall_time = DEFAULT_TIMER()

            # Update progress display if showing progress
            if tasks_name in TASKS:
                iteration_completion: float = progress_max * iteration_pass / iterations_min
                wall_time_elapsed_seconds: float = (wall_time - time_start) * DEFAULT_INTERVAL_SCALE
                time_completion: float = progress_max * (wall_time - time_start) / (min_stop_at - time_start)
                progress_current = min(iteration_completion, time_completion)
                PROGRESS.update(TASKS[tasks_name],
                                completed=progress_current,
                                description=(
                                    f'[green] Benchmarking {group} (iteration {iteration_pass:6d}; '
                                    f'time {wall_time_elapsed_seconds:<3.2f}s)'))

        benchmark_results = BenchResults(
            group=group,
            title=title,
            description=description,
            variation_marks=self.variation_marks,
            n=n,
            iterations=iterations_list,
            total_elapsed=total_elapsed,
            extra_info={})

        if tasks_name in TASKS:
            PROGRESS.stop_task(TASKS[tasks_name])

        return benchmark_results


def benchmark_build_with_add(benchmark: BenchmarkRunner) -> BenchResults:
    '''Benchmark the addition of keys to the trie.

    Args:
        benchmark (BenchmarkRunner): The benchmark runner instance.

    Returns (BenchResults):
        The results of the benchmark.
    '''
    kwargs = benchmark.kwargs
    depth = kwargs['depth']
    test_keys = kwargs['test_data'][depth]
    runtime_validation = kwargs['runtime_validation']

    def action_to_benchmark():
        trie = GeneralizedTrie(runtime_validation=runtime_validation)
        for key in test_keys:
            trie.add(key, None)

    return benchmark.run(action=action_to_benchmark, n=len(test_keys))


def benchmark_build_with_assign(benchmark: BenchmarkRunner) -> BenchResults:
    '''Benchmark the assignment of keys to the trie.

    Args:
        benchmark (BenchmarkRunner): The benchmark runner instance.

    Returns (BenchResults):
        The results of the benchmark.
    '''
    kwargs: dict[str, Any] = benchmark.kwargs
    depth = kwargs['depth']
    test_keys = kwargs['test_data'][depth]
    runtime_validation = kwargs['runtime_validation']

    def action_to_benchmark():
        trie = GeneralizedTrie(runtime_validation=runtime_validation)
        for key in test_keys:
            trie[key] = None

    return benchmark.run(n=len(test_keys), action=action_to_benchmark)


def benchmark_build_with_update(benchmark: BenchmarkRunner) -> BenchResults:
    '''Benchmark the building of a trie using update().

    Args:
        benchmark (BenchmarkRunner): The benchmark runner instance.

    Returns (BenchResults):
        The results of the benchmark.
    '''
    kwargs: dict[str, Any] = benchmark.kwargs
    depth = kwargs['depth']
    test_keys = kwargs['test_data'][depth]
    runtime_validation = kwargs['runtime_validation']

    def action_to_benchmark():
        trie = GeneralizedTrie(runtime_validation=runtime_validation)
        for key in test_keys:
            trie.update(key, None)

    return benchmark.run(n=len(test_keys), action=action_to_benchmark)


def benchmark_updating_trie(benchmark: BenchmarkRunner) -> BenchResults:
    '''Benchmark update() operations on keys in an existing trie.

    This is effectively a benchmark of code like this where all test keys
    are already in the trie and updated to the same value.

    ```
    for key in test_keys:
        trie.update(key, 1)
    ```
    Args:
        benchmark (BenchmarkRunner): The benchmark runner instance.

    Returns:
        A list of BenchResults containing the benchmark results.
    '''
    # Build the prefix tree - built here because we are modifying it
    # and don't want to modify the pre-generated test tries
    kwargs = benchmark.kwargs
    depth = kwargs['depth']
    test_keys = kwargs['test_data'][depth]
    test_args_data: list[tuple[GeneralizedKey, int]] = list([(key, 1) for key in test_keys])
    if len(test_keys) != len(test_args_data):
        raise ValueError("Test keys and args data length mismatch")
    trie = generate_test_trie_from_data(data=test_keys, value=None)
    trie.runtime_validation = kwargs['runtime_validation']

    def action_to_benchmark():
        for key in test_keys:
            trie.update(key, None)

    return benchmark.run(n=len(test_keys), action=action_to_benchmark)


def benchmark_remove_key_from_trie(benchmark: BenchmarkRunner) -> BenchResults:
    '''Benchmark remove() operations on keys in an existing trie.

    This is effectively a benchmark of code like this where all test keys
    are already in the trie and updated to the same value.

    ```
    for key in test_keys:
        trie.remove(key)
    ```
    Args:
        benchmark (BenchmarkRunner): The benchmark runner instance.

    Returns:
        A list of BenchResults containing the benchmark results.
    '''
    kwargs = benchmark.kwargs
    depth = kwargs['depth']
    test_keys = kwargs['test_data'][depth]
    runtime_validation = kwargs['runtime_validation']
    trie: GeneralizedTrie = GeneralizedTrie(runtime_validation=runtime_validation)

    def setup():
        "Setup the trie with test keys."
        for key in test_keys:
            trie.update(key, None)

    def action_to_benchmark():
        "Remove all test keys from the trie."
        for key in test_keys:
            trie.remove(key)

    def teardown():
        "Reset the trie after the benchmark iteration."
        trie.clear()

    return benchmark.run(n=len(test_keys), action=action_to_benchmark, setup=setup, teardown=teardown)


def benchmark_del_key_from_trie(benchmark: BenchmarkRunner) -> BenchResults:
    '''Benchmark "del trie[<key>] operations on keys in an existing trie.

    This is effectively a benchmark of code like this where all test keys
    are already in the trie.

    ```
    for key in test_keys:
        del trie[key]
    ```
    Args:
        benchmark (BenchmarkRunner): The benchmark runner instance.

    Returns:
        A list of BenchResults containing the benchmark results.
    '''
    kwargs = benchmark.kwargs
    depth = kwargs['depth']
    test_keys = kwargs['test_data'][depth]
    runtime_validation = kwargs['runtime_validation']
    trie: GeneralizedTrie = GeneralizedTrie(runtime_validation=runtime_validation)

    def setup():
        "Setup the trie with test keys."
        for key in test_keys:
            trie.update(key, None)

    def action_to_benchmark():
        "Remove all test keys from the trie using del operator"
        for key in test_keys:
            del trie[key]

    def teardown():
        "Clear the trie after the benchmark iteration."
        trie.clear()

    return benchmark.run(n=len(test_keys), action=action_to_benchmark, setup=setup, teardown=teardown)


def benchmark_del_id_from_trie(benchmark: BenchmarkRunner) -> BenchResults:
    '''Benchmark "del trie[<key>] operations on keys in an existing trie.

    This is effectively a benchmark of code like this where all test keys
    are already in the trie.

    ```
    for key in test_keys:
        del trie[key]
    ```
    Args:
        benchmark (BenchmarkRunner): The benchmark runner instance.

    Returns:
        A list of BenchResults containing the benchmark results.
    '''
    kwargs = benchmark.kwargs
    depth = kwargs['depth']
    test_keys: Sequence[GeneralizedKey] = kwargs['test_data'][depth]
    runtime_validation = kwargs['runtime_validation']
    test_ids: list[TrieId] = []
    trie: GeneralizedTrie = GeneralizedTrie(runtime_validation=runtime_validation)

    def setup():
        "Setup the trie with test keys and get the TrieIds for deletion."
        for key in test_keys:
            trie.update(key, None)
        test_ids.extend(trie.keys())

    def action_to_benchmark():
        "Remove all test keys from the trie."
        for trie_id in test_ids:
            del trie[trie_id]

    def teardown():
        "Reset the trie and test ids after the benchmark iteration."
        test_ids.clear()
        trie.clear()

    return benchmark.run(n=len(test_keys), action=action_to_benchmark, setup=setup, teardown=teardown)


def benchmark_key_in_trie(benchmark: BenchmarkRunner) -> BenchResults:
    '''Benchmark '<key> in <trie>' operations.

    Args:
        benchmark (BenchmarkRunner): The benchmark runner instance.

    Returns:
        A list of BenchResults containing the benchmark results.
    '''
    kwargs = benchmark.kwargs
    dataset = kwargs['dataset']
    test_keys: list[GeneralizedKey] = kwargs['test_data'][dataset]
    trie: GeneralizedTrie = kwargs['test_tries'][dataset]
    trie.runtime_validation = kwargs['runtime_validation']

    def action_to_benchmark():
        "Check if all test keys are in the trie."
        for key in test_keys:
            _ = key in trie

    return benchmark.run(n=len(test_keys), action=action_to_benchmark)


def benchmark_id_in_trie(benchmark: BenchmarkRunner) -> BenchResults:
    '''Benchmark '<TrieId> in trie' operations.

    Args:
        benchmark (BenchmarkRunner): The benchmark runner instance.

    Returns:
        A list of BenchResults containing the benchmark results.
    '''
    kwargs: dict[str, Any] = benchmark.kwargs
    dataset = kwargs['dataset']
    trie: GeneralizedTrie = kwargs['test_tries'][dataset]
    trie.runtime_validation = kwargs['runtime_validation']
    test_ids: list[TrieId] = list(trie.keys())

    def action_to_benchmark():
        for key in test_ids:
            _ = key in trie

    return benchmark.run(n=len(test_ids), action=action_to_benchmark)


def benchmark_trie_prefixes_key(benchmark: BenchmarkRunner) -> BenchResults:
    '''Benchmark trie prefixes() method.

    This test checks the performance of the prefixes() method on fully populated tries.
    Because the potential number of matching keys in the trie increases linearly with depth
    and the full runtime of a prefix search is dominated by the number of keys found,
    this test aims to measure the impact of this growth on the performance of the
    prefixes() method.

    Because prefixes() returns a Generator, we need to exhaust it to measure its performance.
    This is done by converting the generator to a list.

    Interpreting performance here is tricky because the number of keys found per prefix can vary
    significantly and they can have a large impact on the overall measurement.
    ```
    for key in test_keys:
        _ = list(trie.prefixes(key))
    ```
    Args:
        benchmark (BenchmarkRunner): The benchmark runner instance.

    Returns:
        A list of BenchResults containing the benchmark results.
    '''
    kwargs: dict[str, Any] = benchmark.kwargs
    depth = kwargs['depth']
    test_keys: list[str] = kwargs['test_keys'][depth]
    trie: GeneralizedTrie = kwargs['test_tries'][depth]
    trie.runtime_validation = kwargs['runtime_validation']

    def action_to_benchmark():
        for key in test_keys:
            _ = list(trie.prefixes(key))

    return benchmark.run(n=len(test_keys), action=action_to_benchmark)


def benchmark_trie_prefixed_by_key(benchmark: BenchmarkRunner) -> BenchResults:
    '''Benchmark trie prefixes_by() method.

    This test checks the performance of the prefixed_by() method on fully populated tries
    at various search depths.

    Because the potential number of matching keys in the trie increases exponentially with depth
    and the full runtime of a prefix search is dominated by the sheer number of keys found,
    this test aims to measure the impact of this growth on the performance of the prefixes() method.

    Because prefixed_by() returns a Generator, we need to exhaust it to measure its performance.
    This is done by converting the generator to a list.

    Interpreting performance here is tricky because the number of keys found per prefix can vary
    significantly by depth and they can have a large impact on the overall measurement.
    ```
    for key in test_keys:
        _ = list(trie.prefixed_by(key, depth))
    ```
    Args:
        benchmark (BenchmarkRunner): The benchmark runner instance.

    Returns:
        A list of BenchResults containing the benchmark results.
    '''
    kwargs: dict[str, Any] = benchmark.kwargs
    search_depth = kwargs['search_depth']
    if not isinstance(search_depth, int):
        raise TypeError(f"Expected 'search_depth' to be int, got {type(search_depth).__name__}")
    trie: GeneralizedTrie = kwargs['test_trie']
    trie.runtime_validation = kwargs['runtime_validation']
    test_keys: list[GeneralizedKey] = kwargs['test_keys']

    def action_to_benchmark():
        for key in test_keys:
            _ = list(trie.prefixed_by(key, search_depth))

    return benchmark.run(n=len(test_keys), action=action_to_benchmark)


@cache
def get_benchmark_cases() -> list[BenchCase]:
    """
    Define the benchmark cases to be run.
    """

    symbols: str = '0123'  # Define the symbols for the trie

    test_data: dict[int, list[str]] = {}
    test_depths: list[int] = [3, 4, 5, 6, 7, 8, 9, 10]  # Depths to test - 1 and 2 are omitted due to low key counts
    for gen_depth in test_depths:
        max_keys_for_depth = len(symbols) ** gen_depth  # pylint: disable=invalid-name
        test_data[gen_depth] = generate_test_data(gen_depth, symbols, max_keys=max_keys_for_depth)

    # We generate the test_tries from the test_data for synchronization
    test_tries: dict[int, GeneralizedTrie] = {}
    for gen_depth in test_depths:
        test_tries[gen_depth] = generate_test_trie_from_data(test_data[gen_depth], None)

    # We generate the test_missing_key_tries from the test_data for synchronization
    test_missing_key_tries: dict[int, tuple[GeneralizedTrie, str]] = {}
    for gen_depth in test_depths:
        test_missing_key_tries[gen_depth] = generate_trie_with_missing_key_from_data(test_data[gen_depth], None)

    test_fully_populated_tries: dict[int, GeneralizedTrie] = {}
    for gen_depth in test_depths:
        test_fully_populated_tries[gen_depth] = generate_fully_populated_trie(
                                                    test_data=test_data,
                                                    symbols=symbols,
                                                    max_depth=gen_depth)

    english_words = load_english_words()
    test_organic_data: dict[str, list[str]] = {
        'english': english_words
    }
    test_organic_tries: dict[str, GeneralizedTrie] = {
        'english': generate_test_trie_from_data(english_words, None)
    }

    benchmark_cases_list: list[BenchCase] = [
        BenchCase(
            group='str-synthetic-id-in-trie',
            title='<TrieId> in trie (Synthetic)',
            description='Timing [yellow bold]<TrieId> in trie[/yellow bold] with synthetic data',
            action=benchmark_id_in_trie,
            iterations=DEFAULT_ITERATIONS,
            variation_cols={'dataset': 'Depth', 'runtime_validation': 'Runtime Validation'},
            kwargs_variations={
                'runtime_validation': [False, True],
                'test_tries': [test_tries],
                'test_data': [test_data],
                'dataset': test_depths,
            },
            graph_aspect_ratio=2.0
        ),
        BenchCase(
            group='str-synthetic-key-in-trie',
            title='<key> in trie (Synthetic)',
            description='Timing [yellow bold]<key> in trie[/yellow bold] with synthetic data',
            action=benchmark_key_in_trie,
            iterations=DEFAULT_ITERATIONS,
            variation_cols={'dataset': 'Depth', 'runtime_validation': 'Runtime Validation'},
            kwargs_variations={
                'runtime_validation': [False, True],
                'test_tries': [test_tries],
                'test_data': [test_data],
                'dataset': test_depths,
            },
            graph_aspect_ratio=2.0
        ),
        BenchCase(
            group='str-english-dictionary-id-in-trie',
            title='<TrieId> in trie (English)',
            description=(
                'Timing [yellow bold]<TrieId> in trie[/yellow bold] with words from the English dictionary'),
            action=benchmark_id_in_trie,
            iterations=DEFAULT_ITERATIONS,
            variation_cols={'dataset': 'Dataset', 'runtime_validation': 'Runtime Validation'},
            kwargs_variations={
                'runtime_validation': [False, True],
                'test_tries': [test_organic_tries],
                'dataset': ['english'],
            },
            graph_aspect_ratio=1.0
        ),
        BenchCase(
            group='str-english-dictionary-key-in-trie',
            title='<key> in trie (English)',
            description=('Timing [yellow bold]<key> in trie[/yellow bold] with words from the English dictionary'),
            action=benchmark_key_in_trie,
            iterations=DEFAULT_ITERATIONS,
            variation_cols={'dataset': 'Dataset', 'runtime_validation': 'Runtime Validation'},
            kwargs_variations={
                'runtime_validation': [False, True],
                'test_tries': [test_organic_tries],
                'test_data': [test_organic_data],
                'dataset': ['english'],
            },
            graph_aspect_ratio=1.0
        ),
        BenchCase(
            group='str-synthetic-building-trie-add',
            title='trie.add(<key>, <value>) (Synthetic)',
            description=('Timing [yellow bold]trie.add(<key>, <value>)[/yellow bold] '
                         'while building a new trie with synthetic data'),
            action=benchmark_build_with_add,
            iterations=DEFAULT_ITERATIONS,
            variation_cols={'depth': 'Depth', 'runtime_validation': 'Runtime Validation'},
            kwargs_variations={
                'runtime_validation': [False, True],
                'test_data': [test_data],
                'depth': test_depths,
            },
            graph_aspect_ratio=2.0
        ),
        BenchCase(
            group='str-synthetic-building-trie-update',
            title='trie.update(<key>, <value>) (Synthetic)',
            description=('Timing [yellow bold]trie.update(<key>, <value>)[/yellow bold] '
                         'while building a new trie with synthetic data'),
            action=benchmark_build_with_update,
            iterations=DEFAULT_ITERATIONS,
            variation_cols={'depth': 'Depth', 'runtime_validation': 'Runtime Validation'},
            kwargs_variations={
                'runtime_validation': [False, True],
                'test_data': [test_data],
                'depth': test_depths,
            },
            graph_aspect_ratio=2.0
        ),
        BenchCase(
            group='str-synthetic-building-trie-assign',
            title='trie[<key>] = <value> (Synthetic)',
            description=('Timing [yellow bold]trie[<key>] = <value>[/yellow bold] '
                         'while building a new trie with synthetic data'),
            action=benchmark_build_with_assign,
            iterations=DEFAULT_ITERATIONS,
            variation_cols={'depth': 'Depth', 'runtime_validation': 'Runtime Validation'},
            kwargs_variations={
                'runtime_validation': [False, True],
                'test_data': [test_data],
                'depth': test_depths,
            },
            graph_aspect_ratio=2.0
        ),
        BenchCase(
            group='str-synthetic-updating-trie-update',
            title='trie.update(<key>, <value>) (Synthetic)',
            description=('Timing [yellow bold]trie.update(<key>, <value>)[/yellow bold] '
                         'while updating values for existing keys with synthetic data'),
            action=benchmark_updating_trie,
            iterations=DEFAULT_ITERATIONS,
            variation_cols={'depth': 'Depth', 'runtime_validation': 'Runtime Validation'},
            kwargs_variations={
                'runtime_validation': [False, True],
                'test_data': [test_data],
                'depth': test_depths,
            },
            graph_aspect_ratio=2.0
        ),
        BenchCase(
            group='str-synthetic-updating-trie-remove',
            title='trie.remove(<key>) (Synthetic)',
            description=('Timing [yellow bold]trie.remove(<key>)[/yellow bold] '
                         'while removing keys from a trie with synthetic data'),
            action=benchmark_remove_key_from_trie,
            variation_cols={'depth': 'Depth', 'runtime_validation': 'Runtime Validation'},
            iterations=DEFAULT_ITERATIONS,
            kwargs_variations={
                'runtime_validation': [False, True],
                'test_data': [test_data],
                'depth': test_depths,
            },
            graph_aspect_ratio=2.0
        ),
        BenchCase(
            group='str-synthetic-updating-trie-del-key',
            title='del trie[<key>] (Synthetic)',
            description=('Timing [yellow bold]del trie[<key>][/yellow bold] '
                         'while deleting keys from a trie with synthetic data'),
            action=benchmark_del_key_from_trie,
            variation_cols={'depth': 'Depth', 'runtime_validation': 'Runtime Validation'},
            iterations=DEFAULT_ITERATIONS,
            kwargs_variations={
                'runtime_validation': [False, True],
                'test_data': [test_data],
                'depth': test_depths,
            },
            graph_aspect_ratio=2.0
        ),
        BenchCase(
            group='str-synthetic-updating-trie-del-id',
            title='del trie[<TrieId>] (Synthetic)',
            description=('Timing [yellow bold]del trie[<TrieId>][/yellow bold] '
                         'while deleting keys from a trie with synthetic data'),
            action=benchmark_del_id_from_trie,
            variation_cols={'depth': 'Depth', 'runtime_validation': 'Runtime Validation'},
            iterations=DEFAULT_ITERATIONS,
            kwargs_variations={
                'runtime_validation': [False, True],
                'test_data': [test_data],
                'depth': test_depths,
            },
            graph_aspect_ratio=2.0
        ),
        BenchCase(
            group='str-synthetic-trie-prefixes',
            title='trie.prefixes(<key>) (Synthetic)',
            description=('Timing [yellow bold]trie.prefixes(<key>)[/yellow bold] '
                         'while finding keys matching a specific prefix in a trie with synthetic data'),
            action=benchmark_trie_prefixes_key,
            variation_cols={'depth': 'Depth', 'runtime_validation': 'Runtime Validation'},
            iterations=DEFAULT_ITERATIONS,
            kwargs_variations={
                'runtime_validation': [False, True],
                'test_tries': [test_fully_populated_tries],
                'test_keys': [test_data],
                'depth': test_depths,
            },
            graph_aspect_ratio=2.0
        ),
        BenchCase(
            group='str-synthetic-trie-prefixed_by',
            title='trie.prefixed_by(<key>, <search_depth>) (Synthetic)',
            description=('Timing [yellow bold]trie.prefixed_by(<key>, <search_depth>)[/yellow bold] '
                         'in a fully populated trie'),
            action=benchmark_trie_prefixed_by_key,
            variation_cols={'search_depth': 'Search Depth', 'runtime_validation': 'Runtime Validation'},
            iterations=DEFAULT_ITERATIONS,
            kwargs_variations={
                'runtime_validation': [False, True],
                'test_trie': [test_fully_populated_tries[9]],
                'test_keys': [test_data[5]],
                'search_depth': [1, 2, 3],
            },
            graph_aspect_ratio=2.0
        ),
    ]
    return benchmark_cases_list


def run_benchmarks(args: Namespace):
    """Run the benchmark tests and print the results.
    """
    benchmark_cases: list[BenchCase] = get_benchmark_cases()
    for case in benchmark_cases:
        case.verbose = args.verbose
        case.progress = args.progress

    cases_to_run: list[BenchCase] = []
    for case in benchmark_cases:
        if 'all' in args.run or case.group in args.run:
            cases_to_run.append(case)

    if args.progress:
        PROGRESS.start()
    case_counter: int = 0
    data_export: list[dict[str, Any]] = []
    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
    output_dir: Path = Path(args.output_dir)
    benchmark_run_dir: Path = output_dir.joinpath(f'run_{timestamp}')
    if args.json or args.json_data or args.csv or args.graph:
        output_dir.mkdir(parents=True, exist_ok=True)
        benchmark_run_dir.mkdir(parents=True, exist_ok=True)

    utils = BenchmarkUtils()
    try:
        task_name: str = 'cases'
        if task_name not in TASKS and args.progress:
            TASKS[task_name] = PROGRESS.add_task(
                description='Running benchmark cases',
                total=len(cases_to_run))

        for case_counter, case in enumerate(cases_to_run):
            if task_name in TASKS:
                PROGRESS.reset(TASKS[task_name])
                PROGRESS.update(
                    task_id=TASKS[task_name],
                    completed=case_counter,
                    description=f'Running benchmark cases (case {case_counter + 1:2d}/{len(cases_to_run)})')
            case.run()
            if case.results:
                if args.json or args.json_data:
                    data_export.append(case.as_dict(args=args))

                if args.graph:
                    if args.ops:
                        graph_file: Path = benchmark_run_dir.joinpath(f'benchmark_graph_ops_{case.group[:60]}.svg')
                        case.plot_ops_results(graph_file)
                    if args.timing:
                        graph_file: Path = benchmark_run_dir.joinpath(f'benchmark_graph_timing_{case.group[:60]}.svg')
                        case.plot_timing_results(graph_file)

                if args.csv:
                    output_targets: list[str] = []
                    if args.ops:
                        output_targets.append('ops')
                    if args.timing:
                        output_targets.append('timing')
                    for target in output_targets:
                        partial_filename: str = utils.sanitize_filename(f'benchmark_{target}_{case.group[:60]}')
                        uniquifier: int = 1
                        csv_file: Path = benchmark_run_dir.joinpath(f'{uniquifier:0>4d}_{partial_filename}.csv')
                        while csv_file.exists():
                            uniquifier += 1
                            csv_file = benchmark_run_dir.joinpath(f'{uniquifier:0>4d}_{partial_filename}.csv')
                        if target == 'ops':
                            case.output_ops_results_to_csv(csv_file)
                        elif target == 'timing':
                            case.output_timing_results_to_csv(csv_file)

                if args.console:
                    if args.ops:
                        case.ops_results_as_rich_table()
                    if args.timing:
                        case.timing_results_as_rich_table()
            else:
                PROGRESS.console.print('No results available')
        if args.json or args.json_data:
            filename = 'benchmark_results.json'
            full_path: Path = benchmark_run_dir.joinpath(filename)
            with full_path.open('w', encoding='utf-8') as json_file:
                json.dump(data_export, json_file, indent=4)
            PROGRESS.console.print(f'Benchmark results exported as JSON to [green]{str(full_path)}[/green]')
        if task_name in TASKS:
            PROGRESS.update(
                task_id=TASKS[task_name],
                completed=len(cases_to_run),
                description=f'Running benchmark cases (case {case_counter + 1:2d}/{len(cases_to_run)})')
        TASKS.clear()
    except KeyboardInterrupt:
        PROGRESS.console.print('Benchmarking interrupted by keyboard interrupt')
    except Exception as exc:  # pylint: disable=broad-exception-caught
        PROGRESS.console.print(f'Error occurred while running benchmarks: {exc}')
    finally:
        if args.progress:
            TASKS.clear()
            PROGRESS.stop()
            for task in PROGRESS.task_ids:
                PROGRESS.remove_task(task)


def main():
    """Main entry point for running benchmarks."""
    parser = ArgumentParser(description='Run GeneralizedTrie benchmarks.')
    parser.add_argument('--verbose', action='store_true', help='Enable verbose output')
    parser.add_argument('--progress', action='store_true', help='Enable progress output')
    parser.add_argument('--list', action='store_true', help='List all available benchmarks')
    parser.add_argument('--run', nargs="+", default='all', metavar='<benchmark>', help='Run specific benchmarks')
    parser.add_argument('--console', action='store_true', help='Enable console output')
    parser.add_argument('--json', action='store_true', help='Enable JSON file statistics output to files')
    parser.add_argument('--json-data',
                        action='store_true',
                        help='Enable JSON file statistics and data output to files')
    parser.add_argument('--csv', action='store_true', help='Enable tagged CSV statistics output to files')
    parser.add_argument('--graph', action='store_true', help='Enable graphical output (e.g., plots)')
    parser.add_argument('--output_dir', default='.benchmarks',
                        help='Output destination directory (default: .benchmarks)')
    parser.add_argument('--ops',
                        action='store_true',
                        help='Enable operations per second output to console or csv')
    parser.add_argument('--timing', action='store_true', help='Enable operations timing output to console or csv')

    args: Namespace = parser.parse_args()
    if args.verbose:
        PROGRESS.console.print('Verbose output enabled')

    if args.list:
        PROGRESS.console.print('Available benchmarks:')
        for case in get_benchmark_cases():
            PROGRESS.console.print('  - ', f'[green]{case.group:<40s}[/green]', f'{case.title}')
        return

    if not (args.console or args.json or args.csv or args.json or args.json_data):
        PROGRESS.console.print('No output format(s) selected, using console output by default')
        args.console = True

    if args.json and args.json_data:
        PROGRESS.console.print('Both --json and --json-data are enabled, using --json-data')
        args.json = False
    if (args.graph or args.json or args.json_data or args.csv) and not args.output_dir:
        PROGRESS.console.print('No output directory specified, using default: .benchmarks')

    if args.console and not (args.ops or args.timing):
        PROGRESS.console.print(
            'No benchmark result type selected for --console: At least one of --ops or --timing must be enabled')
        parser.print_usage()
        return

    if args.csv and not (args.ops or args.timing):
        PROGRESS.console.print(
            'No benchmark result type selected for --csv: At least one of --ops or --timing must be enabled')
        parser.print_usage()
        return

    if args.graph and not (args.ops or args.timing):
        PROGRESS.console.print(
            'No benchmark result type selected for --graph: At least one of --ops or --timing must be enabled')
        parser.print_usage()
        return

    run_benchmarks(args=args)


if __name__ == '__main__':
    main()
