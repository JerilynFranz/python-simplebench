"""SimpleRunner for benchmarking.

SimpleRunner is a basic class for running benchmarks for various actions.

It measures the time taken to execute a given action and the memory usage of the action.
It also provides a method to automatically calibrate the number of rounds for the benchmark
timing to achieve a desired level of precision and accuracy in the measurements.

It provides the following standard Metrics for each benchmark run:

- STD_TIMING_STATS: timing statistics for each operation
- STD_TIMING_RAW: timing raw values for each operation
- STD_CPU_TIME_STATS: CPU time statistics for each operation
- STD_CPU_TIME_RAW: CPU time raw values for each operation
- STD_OPS_STATS: operations per second statistics (computed from timing raw values)
- STD_OPS_RAW: operations per second raw values (computed from timing raw values)
- STD_MEMORY_STATS: memory usage statistics
- STD_MEMORY_RAW: memory usage raw values
- STD_PEAK_MEMORY_STATS: peak memory usage statistics
- STD_PEAK_MEMORY_RAW: peak memory usage raw values
- STD_TOTAL_ELAPSED_TIME: The sum of all timing raw values
- STD_TOTAL_CPU_TIME: The sum of all CPU time raw values
- STD_GC_GEN0_COLLECTIONS_STATS: Number of garbage collections for generation 0
- STD_GC_GEN0_COLLECTIONS_RAW: Number of garbage collections for generation 0 (raw values)
- STD_GC_GEN1_COLLECTIONS_STATS: Number of garbage collections for generation 1
- STD_GC_GEN1_COLLECTIONS_RAW: Number of garbage collections for generation 1 (raw values)
- STD_GC_GEN2_COLLECTIONS_STATS: Number of garbage collections for generation 2
- STD_GC_GEN2_COLLECTIONS_RAW: Number of garbage collections for generation 2 (raw values)
- STD_GC_GEN0_COLLECTED_STATS: Number of objects collected by garbage collection for generation 0
- STD_GC_GEN0_COLLECTED_RAW: Number of objects collected by garbage collection for generation 0 (raw values)
- STD_GC_GEN1_COLLECTED_STATS: Number of objects collected by garbage collection for generation 1
- STD_GC_GEN1_COLLECTED_RAW: Number of objects collected by garbage collection for generation 1 (raw values)
- STD_GC_GEN2_COLLECTED_STATS: Number of objects collected by garbage collection for generation 2
- STD_GC_GEN2_COLLECTED_RAW: Number of objects collected by garbage collection for generation 2 (raw values)
- STD_GC_GEN0_UNCOLLECTABLE_STATS: Number of uncollectable objects for generation 0
- STD_GC_GEN0_UNCOLLECTABLE_RAW: Number of uncollectable objects for generation 0 (raw values)
- STD_GC_GEN1_UNCOLLECTABLE_STATS: Number of uncollectable objects for generation 1
- STD_GC_GEN1_UNCOLLECTABLE_RAW: Number of uncollectable objects for generation 1 (raw values)
- STD_GC_GEN2_UNCOLLECTABLE_STATS: Number of uncollectable objects for generation 2
- STD_GC_GEN2_UNCOLLECTABLE_RAW: Number of uncollectable objects for generation 2 (raw values)

The timing per operation and operations per second measurements are based on the same
timing measurement, and are therefore consistent with each other. Both are
provided for convenience and to provide a more complete picture of the benchmark
results.
"""

import gc
import importlib.util
import math
import sys
import tracemalloc
from collections.abc import Callable
from functools import cache
from types import ModuleType
from typing import TYPE_CHECKING, Any, Final, NamedTuple

from simplebench import defaults
from simplebench.benchmark_runner.benchmark_runner import BenchmarkRunner
from simplebench.case.results import Results
from simplebench.display.progress_tracker import ProgressTracker
from simplebench.enums import Calibrate, Color
from simplebench.exceptions import (
    SimpleBenchImportError,
    SimpleBenchRuntimeError,
    SimpleBenchTimeoutError,
    SimpleBenchTypeError,
)
from simplebench.metrics import Metric, metrics_registry
from simplebench.simplebench_types import Extras, Iterations, MetricsTimers, Values, VariationCols, VariationMarks
from simplebench.timeout import Timeout
from simplebench.timers import is_valid_timer, timer_overhead_ns, timer_precision_ns
from simplebench.validators import validate_positive_int

from ._error_tags import _SimpleRunnerErrorTag

if TYPE_CHECKING:
    from simplebench.case import Case
    from simplebench.session import Session

_TIMERS_NAMESPACE: str = '_simplerunner_timers'
"""Namespace for dynamically created timer functions."""


def _create_timers_module(namespace: str) -> ModuleType:
    """Create a module to hold dynamically created timer functions.

    The module is created using :mod:`importlib` and added to :data:`sys.modules`
    under the name 'simplerunner._timers'. If the module already exists
    in :data:`sys.modules`, it is returned as is.

    :return: The created or existing timers module.
    :rtype: ModuleType
    :raises SimpleBenchImportError: If the module could not be created.
    """
    if not isinstance(namespace, str):
        raise SimpleBenchTypeError(
            f'Namespace must be a string, got {type(namespace).__name__}',
            tag=_SimpleRunnerErrorTag.RUNNERS_CREATE_TIMERS_MODULE_INVALID_NAMESPACE_TYPE,
        )
    if not namespace.isidentifier():
        raise SimpleBenchTypeError(
            f'Namespace must be a valid identifier, got {namespace}',
            tag=_SimpleRunnerErrorTag.RUNNERS_CREATE_TIMERS_MODULE_INVALID_NAMESPACE_VALUE,
        )
    spec = importlib.util.spec_from_loader(namespace, loader=None)
    if spec is None:
        raise SimpleBenchImportError(
            f'Could not create spec for {namespace} module',
            tag=_SimpleRunnerErrorTag.RUNNERS_CREATE_TIMERS_MODULE_SPEC_FAILED,
        )
    if namespace in sys.modules:
        return sys.modules[namespace]
    timers_module = importlib.util.module_from_spec(spec)
    sys.modules[namespace] = timers_module
    return timers_module


_timers_module = _create_timers_module(_TIMERS_NAMESPACE)  # Ensure the timers module exists
"""A dynamically created module to hold generated timer functions."""


class _Measurement(NamedTuple):
    """A named tuple to hold measurement data.

    :param timing: The time taken to execute the action.
    :type timing: float
    :param cpu_time: The CPU time taken to execute the action.
    :type cpu_time: float
    :param memory: The memory usage of the action.
    :type memory: int
    :param peak_memory: The peak memory usage of the action.
    :type peak_memory: int
    :param gc_gen0_collections: The number of generation 0 garbage collections.
    :type gc_gen0_collections: int
    :param gc_gen0_collected: The number of objects collected in generation 0.
    :type gc_gen0_collected: int
    :param gc_gen0_uncollectable: The number of uncollectable objects in generation 0.
    :type gc_gen0_uncollectable: int
    :param gc_gen1_collections: The number of generation 1 garbage collections.
    :type gc_gen1_collections: int
    :param gc_gen1_collected: The number of objects collected in generation 1.
    :type gc_gen1_collected: int
    :param gc_gen1_uncollectable: The number of uncollectable objects in generation 1.
    :type gc_gen1_uncollectable: int
    :param gc_gen2_collections: The number of generation 2 garbage collections.
    :type gc_gen2_collections: int
    :param gc_gen2_collected: The number of objects collected in generation 2.
    :type gc_gen2_collected: int
    :param gc_gen2_uncollectable: The number of uncollectable objects in generation 2.
    :type gc_gen2_uncollectable: int
    """

    timing: float
    cpu_time: float
    memory: int
    peak_memory: int
    gc_gen0_collections: int
    gc_gen0_collected: int
    gc_gen0_uncollectable: int
    gc_gen1_collections: int
    gc_gen1_collected: int
    gc_gen1_uncollectable: int
    gc_gen2_collections: int
    gc_gen2_collected: int
    gc_gen2_uncollectable: int


_MEASUREMENT_INDEXES: Final[dict[str, int]] = {name: idx for idx, name in enumerate(_Measurement._fields)}
"""A mapping of measurement field names to their corresponding indexes in the _Measurement tuple."""

# Index constants for measurement tuple elements
# This is a performance/code readability optimization to avoid using magic numbers
# Each constant represents the index of a specific element in the measurement tuple
# This is faster than using NamedTuple field access and provides a good way
# to process measurement tuples efficiently and clearly
#
_TIMING: Final[int] = _MEASUREMENT_INDEXES['timing']
"""A constant representing the index of the timing element in a measurement tuple."""
_CPU_TIME: Final[int] = _MEASUREMENT_INDEXES['cpu_time']
"""A constant representing the index of the CPU timing element in a measurement tuple."""
_MEMORY: Final[int] = _MEASUREMENT_INDEXES['memory']
"""A constant representing the index of the memory element in a measurement tuple."""
_PEAK_MEMORY: Final[int] = _MEASUREMENT_INDEXES['peak_memory']
"""A constant representing the index of the peak memory element in a measurement tuple."""
_GC_GEN0_COLLECTIONS: Final[int] = _MEASUREMENT_INDEXES['gc_gen0_collections']
"""A constant representing the index of the generation 0 garbage collections element in a measurement tuple."""
_GC_GEN0_COLLECTED: Final[int] = _MEASUREMENT_INDEXES['gc_gen0_collected']
"""A constant representing the index of the generation 0 collected garbage element in a measurement tuple."""
_GC_GEN0_UNCOLLECTABLE: Final[int] = _MEASUREMENT_INDEXES['gc_gen0_uncollectable']
"""A constant representing the index of the generation 0 uncollectable garbage element in a measurement tuple."""
_GC_GEN1_COLLECTIONS: Final[int] = _MEASUREMENT_INDEXES['gc_gen1_collections']
"""A constant representing the index of the generation 1 garbage collections element in a measurement tuple."""
_GC_GEN1_COLLECTED: Final[int] = _MEASUREMENT_INDEXES['gc_gen1_collected']
"""A constant representing the index of the generation 1 collected garbage element in a measurement tuple."""
_GC_GEN1_UNCOLLECTABLE: Final[int] = _MEASUREMENT_INDEXES['gc_gen1_uncollectable']
"""A constant representing the index of the generation 1 uncollectable garbage element in a measurement tuple."""
_GC_GEN2_COLLECTIONS: Final[int] = _MEASUREMENT_INDEXES['gc_gen2_collections']
"""A constant representing the index of the generation 2 garbage collections element in a measurement tuple."""
_GC_GEN2_COLLECTED: Final[int] = _MEASUREMENT_INDEXES['gc_gen2_collected']
"""A constant representing the index of the generation 2 collected garbage element in a measurement tuple."""
_GC_GEN2_UNCOLLECTABLE: Final[int] = _MEASUREMENT_INDEXES['gc_gen2_uncollectable']
"""A constant representing the index of the generation 2 uncollectable garbage element in a measurement tuple."""

_RETAINED_METRICS: Final[list[int]] = list(sorted(_MEASUREMENT_INDEXES.values()))
"""A sorted list of all measurement indexes to be retained in the results.

This includes all indexes defined in the _Measurement named tuple which
means any measurement included in the tuple is automatically retained.
"""

_STD_OPS_STATS_METRIC: Final[Metric] = metrics_registry['STD_OPS_STATS']
"""The standard operations per second statistics metric.

This is computed from the timing measurements so that it is consistent with them.
"""
_STD_OPS_RAW_METRIC: Final[Metric] = metrics_registry['STD_OPS_RAW']
"""The standard operations per second raw metric.

This is computed from the timing measurements so that it is consistent with them.
"""

_METRIC_TO_MEASUREMENT_INDEX: Final[dict[Metric, int]] = {
    metrics_registry['STD_TIMING_STATS']: _TIMING,
    metrics_registry['STD_CPU_TIME_STATS']: _CPU_TIME,
    metrics_registry['STD_TIMING_RAW']: _TIMING,
    metrics_registry['STD_CPU_TIME_RAW']: _CPU_TIME,
    metrics_registry['STD_MEMORY_STATS']: _MEMORY,
    metrics_registry['STD_MEMORY_RAW']: _MEMORY,
    metrics_registry['STD_PEAK_MEMORY_STATS']: _PEAK_MEMORY,
    metrics_registry['STD_PEAK_MEMORY_RAW']: _PEAK_MEMORY,
    metrics_registry['STD_TOTAL_ELAPSED_TIME']: _TIMING,
    metrics_registry['STD_TOTAL_CPU_TIME']: _CPU_TIME,
    metrics_registry['STD_GC_GEN0_COLLECTIONS_STATS']: _GC_GEN0_COLLECTIONS,
    metrics_registry['STD_GC_GEN0_COLLECTED_STATS']: _GC_GEN0_COLLECTED,
    metrics_registry['STD_GC_GEN0_UNCOLLECTABLE_STATS']: _GC_GEN0_UNCOLLECTABLE,
    metrics_registry['STD_GC_GEN1_COLLECTIONS_STATS']: _GC_GEN1_COLLECTIONS,
    metrics_registry['STD_GC_GEN1_COLLECTED_STATS']: _GC_GEN1_COLLECTED,
    metrics_registry['STD_GC_GEN1_UNCOLLECTABLE_STATS']: _GC_GEN1_UNCOLLECTABLE,
    metrics_registry['STD_GC_GEN2_COLLECTIONS_STATS']: _GC_GEN2_COLLECTIONS,
    metrics_registry['STD_GC_GEN2_COLLECTED_STATS']: _GC_GEN2_COLLECTED,
    metrics_registry['STD_GC_GEN2_UNCOLLECTABLE_STATS']: _GC_GEN2_UNCOLLECTABLE,
    metrics_registry['STD_GC_GEN0_COLLECTIONS_RAW']: _GC_GEN0_COLLECTIONS,
    metrics_registry['STD_GC_GEN0_COLLECTED_RAW']: _GC_GEN0_COLLECTED,
    metrics_registry['STD_GC_GEN0_UNCOLLECTABLE_RAW']: _GC_GEN0_UNCOLLECTABLE,
    metrics_registry['STD_GC_GEN1_COLLECTIONS_RAW']: _GC_GEN1_COLLECTIONS,
    metrics_registry['STD_GC_GEN1_COLLECTED_RAW']: _GC_GEN1_COLLECTED,
    metrics_registry['STD_GC_GEN1_UNCOLLECTABLE_RAW']: _GC_GEN1_UNCOLLECTABLE,
    metrics_registry['STD_GC_GEN2_COLLECTIONS_RAW']: _GC_GEN2_COLLECTIONS,
    metrics_registry['STD_GC_GEN2_COLLECTED_RAW']: _GC_GEN2_COLLECTED,
    metrics_registry['STD_GC_GEN2_UNCOLLECTABLE_RAW']: _GC_GEN2_UNCOLLECTABLE,
}
"""A mapping of metrics to their corresponding measurement indexes.

This is used to extract the relevant measurement data for each metric from
the measurement tuples.

Any new metrics added to the SimpleBench metrics registry that correspond to
measurement data must be added here to be included in the benchmark results.
"""


@cache
def _metric_timers(
        wall_timer: Callable[[], int],
        cpu_timer: Callable[[], int]) -> dict[Metric, str | None]:
    """Return a mapping of metrics to their corresponding timer names or None.

    :param wall_timer: The wall-clock timer function used for the benchmark.
    :type wall_timer: Callable[[], int]
    :param cpu_timer: The CPU timer function used for the benchmark.
    :type cpu_timer: Callable[[], int]
    :return: A dictionary mapping metrics to their timer names.
    :rtype: dict[Metric, str | None]
    """
    wall_timer_name: str = wall_timer.__name__
    cpu_timer_name: str = cpu_timer.__name__
    return {
        metrics_registry['STD_TIMING_STATS']: wall_timer_name,
        metrics_registry['STD_CPU_TIME_STATS']: cpu_timer_name,
        metrics_registry['STD_TIMING_RAW']: wall_timer_name,
        metrics_registry['STD_CPU_TIME_RAW']: cpu_timer_name,
        metrics_registry['STD_OPS_STATS']: wall_timer_name,
        metrics_registry['STD_OPS_RAW']: wall_timer_name,
        metrics_registry['STD_MEMORY_STATS']: None,
        metrics_registry['STD_MEMORY_RAW']: None,
        metrics_registry['STD_PEAK_MEMORY_STATS']: None,
        metrics_registry['STD_PEAK_MEMORY_RAW']: None,
        metrics_registry['STD_TOTAL_ELAPSED_TIME']: wall_timer_name,
        metrics_registry['STD_TOTAL_CPU_TIME']: cpu_timer_name,
        metrics_registry['STD_GC_GEN0_COLLECTIONS_STATS']: None,
        metrics_registry['STD_GC_GEN0_COLLECTED_STATS']: None,
        metrics_registry['STD_GC_GEN0_UNCOLLECTABLE_STATS']: None,
        metrics_registry['STD_GC_GEN1_COLLECTIONS_STATS']: None,
        metrics_registry['STD_GC_GEN1_COLLECTED_STATS']: None,
        metrics_registry['STD_GC_GEN1_UNCOLLECTABLE_STATS']: None,
        metrics_registry['STD_GC_GEN2_COLLECTIONS_STATS']: None,
        metrics_registry['STD_GC_GEN2_COLLECTED_STATS']: None,
        metrics_registry['STD_GC_GEN2_UNCOLLECTABLE_STATS']: None,
        metrics_registry['STD_GC_GEN0_COLLECTIONS_RAW']: None,
        metrics_registry['STD_GC_GEN0_COLLECTED_RAW']: None,
        metrics_registry['STD_GC_GEN0_UNCOLLECTABLE_RAW']: None,
        metrics_registry['STD_GC_GEN1_COLLECTIONS_RAW']: None,
        metrics_registry['STD_GC_GEN1_COLLECTED_RAW']: None,
        metrics_registry['STD_GC_GEN1_UNCOLLECTABLE_RAW']: None,
        metrics_registry['STD_GC_GEN2_COLLECTIONS_RAW']: None,
        metrics_registry['STD_GC_GEN2_COLLECTED_RAW']: None,
        metrics_registry['STD_GC_GEN2_UNCOLLECTABLE_RAW']: None,
    }


class SimpleRunner(BenchmarkRunner):
    """A class to run benchmarks for various actions.

    :param case: The benchmark case to run.
    :type case: Case
    :param variation_marks: The variation marks for the benchmark case.
    :type variation_marks: VariationMarks
    :param session: The session in which the benchmark is run.
    :type session: Session, optional
    :param runner: The BenchmarkRunner callable to use to run the benchmark.
    :type runner: Callable[..., Any], optional
    """

    def __init__(
        self,
        *,
        case: 'Case',
        variation_marks: VariationMarks,
        session: 'Session | None' = None,
        runner: Callable[..., Any] | None = None,
    ) -> None:
        """
        :param case: The benchmark case to run.
        :type case: Case
        :param variation_marks: The variation marks for the benchmark case.
        :type variation_marks: VariationMarksType
        :param session: The session in which the benchmark is run.
        :type session: :class:`Session` | :obj:`None`, optional
        :ivar runner: (default = :meth:`default_runner`) The function to use to run the benchmark.
            If :obj:`None`, uses :meth:`default_runner`
        :type runner: Callable[..., Any] | :obj:`None`, optional
        """
        self.case = case
        self.variation_marks = variation_marks
        self._runner: Callable[..., Any] = self.default_runner
        """Benchmark runner function. Defaults to :meth:`default_runner`.

        The runner function must accept the following parameters:
            ``n`` (int | float): The **O()** 'n' weight of the benchmark.
                This is used to calculate a weight for the purpose of **O()** analysis.

                For example, if the action being benchmarked is a function that
                sorts a list of length n, then n should be the length of the list.
                If the action being benchmarked is a function that performs
                a constant-time operation, then n should be 1.
            ``action`` (Callable[..., Any]): The function to benchmark.
            ``setup`` (Optional[Callable[..., Any]]): A setup function to run before each iteration.
            ``teardown`` (Optional[Callable[..., Any]]): A teardown function to run after each iteration.
            ``kwargs`` (Optional[dict[str, Any]]): Keyword arguments to pass to the function being benchmarked.
        """
        self.session = session

    def run(
        self,
        *,
        n: int | float,
        action: Callable[..., Any],
        setup: Callable[..., Any] | None = None,
        teardown: Callable[..., Any] | None = None,
        variation_marks: VariationMarks | None = None,
    ) -> Results:
        """Enforce a timeout while running the benchmark with the specified runner.

        This method wraps the benchmark execution in a :class:`~.simplebench.timeout.Timeout`
        to enforce the timeout specified in the benchmark case.

        .. warning:: **Important Timeout Behavior Notice**
            If the benchmark exceeds the specified timeout set in the case,
            a :class:`~.simplebench.exceptions.SimpleBenchTimeoutError`
            will be raised, and no results will be returned.

            Because the worker thread may still be running in the background after a timeout,
            it is recommended to exit the program cleanly rather than continuing execution
            because this can (probably **WILL**) lead to undefined behavior.

        :param n: The **O()** 'n' weight of the benchmark.
            This is used to calculate a weight for the purpose of **O()** analysis.

            For example, if the action being benchmarked is a function that
            sorts a list of length n, then n should be the length of the list.
            If the action being benchmarked is a function that performs
            a constant-time operation, then n should be 1.
        :param action: The function to benchmark.
        :param setup: A setup function to run before each iteration.
        :param teardown: A teardown function to run after each iteration.
        :param variation_marks: Variation marks to apply to the benchmark.
        :return: The results of the benchmark.
        :rtype: Results
        :raises SimpleBenchTimeoutError: If the benchmark exceeds the specified timeout for the case.
        """
        # The Timeout class acts similarly to a context manager, but here we use it
        # to wrap the entire benchmark run to enforce a timeout on the whole operation.
        # This ensures that if the benchmark takes too long, it will be interrupted
        # and a timeout exception will be raised.
        # The run() method of the Timeout class is used to execute the benchmark
        # with the specified timeout and returns the returned value of the
        # called function, which in this case is a Results instance.
        func_name = getattr(action, '__qualname__', getattr(action, '__name__', repr(action)))
        benchmark_id = self.case.benchmark_id
        timeout_interval = self.case.timeout
        marks = VariationMarks() if variation_marks is None else variation_marks
        try:
            result = Timeout(timeout_interval).run(
                self._runner, n=n, action=action, setup=setup, teardown=teardown, variation_marks=marks
            )
        except SimpleBenchTimeoutError as e:
            raise SimpleBenchTimeoutError(
                f'Benchmark "{benchmark_id}" timed out after {timeout_interval} seconds without a result',
                tag=_SimpleRunnerErrorTag.SIMPLERUNNER_BENCHMARK_TIMEOUT,
                func_name=func_name,
            ) from e
        return result

    def _timer_function(
        self, rounds: int
    ) -> Callable[
        [Callable[[], int], Callable[[], int], Callable[..., Any], dict[str, Any]], tuple[float, float]
    ]:
        """Return a timer function for the benchmark.

        The generated function will call the action `rounds` times and return the total time
        taken as a float.

        The function is generated as a string and then compiled to avoid the overhead of
        a loop in Python during the actual timing benchmark.

        The generated function will have the following signature:

        .. code-block:: python

            def _timer_function_{rounds}(
                    timer: Callable[[], float | int],
                    cpu_timer: Callable[[], float | int],
                    action: Callable[..., Any],
                    kwargs: dict[str, Any]) -> tuple[float, float]:

        It is created in the module ``simplerunner._timers`` to avoid polluting the global namespace.

        By creating a new dedicated function for each needed rounds value, we avoid the overhead
        of a loop in Python during the actual timing benchmark. This is particularly important
        for micro-benchmarks where the action being benchmarked is very fast.

        :param rounds: The number of test rounds that will be run by the action on each iteration. Must be >= 1.
        :type rounds: int
        :return: A function that returns the elapsed time for the benchmark as a tuple of
            floats (elapsed time, CPU time).
        :rtype: Callable[[Callable[[], int | float], Callable[..., Any], dict[str, Any]], tuple[float, float]]
        """
        rounds = validate_positive_int(
            rounds,
            'rounds',
            _SimpleRunnerErrorTag.SIMPLERUNNER_TIMER_FUNCTION_INVALID_ROUNDS_TYPE,
            _SimpleRunnerErrorTag.SIMPLERUNNER_TIMER_FUNCTION_INVALID_ROUNDS_VALUE,
        )

        # If the timer function for the specified rounds does not exist, create it.
        # We create a new function for each rounds value to avoid the overhead of a loop
        # in the timing function.
        # The function is created as a string and then compiled to avoid the overhead
        # of a loop in Python during the actual timing benchmark.
        timer_name = f'_simplerunner_timer_function_{rounds}'
        if not hasattr(_timers_module, timer_name):
            time_function_lines: list[str] = []
            time_function_lines.extend([
                f'def {timer_name}(timer, cpu_timer, action, kwargs):',
                '    start = timer()',
                '    start_cpu = cpu_timer()',
            ])
            time_function_lines.extend(['    action(**kwargs)'] * rounds)
            time_function_lines.extend(['    end = timer()', '    end_cpu = cpu_timer()'])
            time_function_lines.append('    return float(end - start), float(end_cpu - start_cpu)')
            time_function_code = '\n'.join(time_function_lines)
            exec(time_function_code, _timers_module.__dict__)  # pylint: disable=exec-used

        return getattr(_timers_module, timer_name)

    def _execute_timed_rounds(
        self,
        *,
        rounds: int,
        timer: Callable[[], int],
        cpu_timer: Callable[[], int],
        action: Callable[..., Any],
        kwargs: dict[str, Any],
    ) -> tuple[float, float, int]:
        """Execute the action for the specified number of rounds and return raw timing totals.

        Uses kiloround chunking (1000-round slices) for large round counts to avoid generating
        excessively large timer functions and hitting Python's function size limits.

        :param rounds: The number of rounds to execute.
        :param timer: The wall-clock timer function.
        :param cpu_timer: The CPU timer function.
        :param action: The action to benchmark.
        :param kwargs: Keyword arguments to pass to the action.
        :return: A tuple of (total_elapsed_ns, total_elapsed_cpu_ns, timer_metrics_count).
        """
        if rounds < 1000:
            total_elapsed, total_elapsed_cpu = self._timer_function(rounds)(timer, cpu_timer, action, kwargs)
            return total_elapsed, total_elapsed_cpu, 1

        # for 1000 or more rounds, break into chunks of 1000 (a "kiloround") to reduce the
        # footprint of the generated timer functions and avoid hitting Python's function size limits.
        kiloround_timer = self._timer_function(1000)
        total_elapsed = 0.0
        total_elapsed_cpu = 0.0
        timer_metrics = 0
        kiloround_chunks, remaining_rounds = divmod(rounds, 1000)
        while kiloround_chunks:
            elapsed, elapsed_cpu = kiloround_timer(timer, cpu_timer, action, kwargs)
            total_elapsed += elapsed
            total_elapsed_cpu += elapsed_cpu
            kiloround_chunks -= 1
            timer_metrics += 1
        if remaining_rounds:
            elapsed, elapsed_cpu = self._timer_function(remaining_rounds)(timer, cpu_timer, action, kwargs)
            total_elapsed += elapsed
            total_elapsed_cpu += elapsed_cpu
            timer_metrics += 1
        return total_elapsed, total_elapsed_cpu, timer_metrics

    def _run_timed_iteration(
        self,
        *,
        rounds: int,
        timer: Callable[[], int],
        cpu_timer: Callable[[], int],
        action: Callable[..., Any],
        kwargs: dict[str, Any],
        setup: Callable[..., Any] | None,
        teardown: Callable[..., Any] | None,
    ) -> tuple[float, float]:
        """Run a single timed iteration of the benchmark action for a given number of rounds.
        This method uses an unrolled loop to call the action the specified number of rounds,
        minimizing the overhead of loop control in Python.

        :param int rounds: The number of test rounds that will be run by the action for the iteration.
        :param Callable[[], int | float] timer: The timer function to use for timing.
        :param Callable[..., Any] action: The action to benchmark.
        :param dict[str, Any] kwargs: Keyword arguments to pass to the action.
        :param Optional[Callable[..., Any]] setup: A setup function to run before the iteration.
        :param Optional[Callable[..., Any]] teardown: A teardown function to run after the iteration.
        :return float: The elapsed time for the iteration in seconds.
        """
        if callable(setup):
            setup()
        total_elapsed, total_elapsed_cpu, timer_metrics = self._execute_timed_rounds(
            rounds=rounds, timer=timer, cpu_timer=cpu_timer, action=action, kwargs=kwargs
        )
        if callable(teardown):
            teardown()
        elapsed_time = float((total_elapsed - timer_overhead_ns(timer) * timer_metrics) * defaults.DEFAULT_INTERVAL_SCALE)
        elapsed_cpu_time = float(
            (total_elapsed_cpu - timer_overhead_ns(cpu_timer) * timer_metrics) * defaults.DEFAULT_INTERVAL_SCALE
        )
        return elapsed_time, elapsed_cpu_time

    def default_runner(  # pylint: disable=too-many-arguments, too-many-locals, too-many-statements  # noqa: C901
        self,
        *,
        n: int | float,
        action: Callable[..., Any],
        setup: Callable[..., Any] | None = None,
        teardown: Callable[..., Any] | None = None,
        variation_marks: VariationMarks | None = None,
        variation_cols: VariationCols | None = None,
    ) -> Results:
        """Run a generic benchmark using the specified action and test case.

        It runs a complete benchmark for a specific combination of kwarg variations
        according to the parameters defined in the benchmark case, including the
        number of iterations, minimum and maximum time limits, and warmup iterations.

        All measurements are collected into :class:`~.simplebench.case.results.Results`
        which is returned at the end of the benchmark.

        The same number of rounds is used for every iteration in a single Results,
        which is either auto-calibrated or specified in the benchmark case.

        :param n: The **O()** 'n' weight of the benchmark. This is used to calculate
            a weight for the purpose of **O()** analysis.

            For example, if the action being benchmarked is a function that
            sorts a list of length n, then n should be the length of the list.
            If the action being benchmarked is a function that performs
            a constant-time operation, then n should be 1.
        :type n: int | float
        :param action: The action to benchmark.
        :type action: Callable[..., Any]
        :param setup: A setup function to run before each iteration.
        :type setup: Callable[..., Any] | None, optional
        :param teardown: A teardown function to run after each iteration.
        :type teardown: Callable[..., Any] | None, optional
        :param variation_marks: Keyword arguments to pass to the action.
        :type variation_marks: VariationMarksType | None, optional
        :return: The results of the benchmark.
        :rtype: Results
        """
        kwargs: dict[str, Any] = {}
        if variation_marks:
            kwargs = { k: v.value for k, v in variation_marks.items() }

        group: str = self.case.group
        title: str = self.case.title
        description: str = self.case.description
        min_time: float = self.case.min_time
        max_time: float = self.case.max_time
        iterations: int = self.case.iterations
        calibrate: Calibrate | None = self.case.calibrate
        if calibrate is None:
            if self.session and self.session.calibrate:
                calibrate = self.session.calibrate
            else:
                calibrate = Calibrate.CPU

        # Prioritize the timers from the case, then from the session, then use the default timer
        timer = defaults.DEFAULT_TIMER
        if self.case.timer is not None:
            timer = self.case.timer
        elif self.session is not None and self.session.timer is not None:
            timer = self.session.timer

        cpu_timer = defaults.DEFAULT_CPU_TIMER
        if self.case.cpu_timer is not None:
            cpu_timer = self.case.cpu_timer
        elif self.session is not None and self.session.cpu_timer is not None:
            cpu_timer = self.session.cpu_timer

        _timers_for_metrics: dict[Metric, str | None] = _metric_timers(wall_timer=timer,
                                                                       cpu_timer=cpu_timer)

        # warmup iterations are not included in the final stats
        # We start the count from -warmup_iterations to ensure we do the correct number of warmup
        # iterations even if warmup_iterations is 0.
        iteration_pass: int = -self.case.warmup_iterations
        time_start: float = float(timer())
        max_stop_at: float = float(max_time / defaults.DEFAULT_INTERVAL_SCALE) + time_start
        min_stop_at: float = float(min_time / defaults.DEFAULT_INTERVAL_SCALE) + time_start
        wall_time: float = float(timer())
        iterations_min: int = max(defaults.MIN_MEASURED_ITERATIONS, iterations)

        rounds: int
        if self.case.rounds is None:
            rounds = self._calibrate_rounds(
                calibrate=calibrate,
                timer=timer,
                cpu_timer=cpu_timer,
                kwargs=kwargs,
                setup=setup,
                teardown=teardown,
                action=action
            )
        else:
            rounds = self.case.rounds

        gc.collect()

        progress_max: float = 100.0
        progress_tracker = ProgressTracker(
            session=self.session,
            task_name='SimpleRunner:case_runner',
            progress_max=progress_max,
            description=f'Benchmarking {group} (iteration {0:<6d}; time {0.00:<3.2f}s)',
            color=Color.GREEN,
        )

        iterations_list: list[_Measurement] = []

        while (iteration_pass <= iterations_min or wall_time < min_stop_at) and wall_time < max_stop_at:
            iteration_pass += 1
            # Time the action
            elapsed, cpu_elapsed = self._run_timed_iteration(
                rounds=rounds,
                timer=timer,
                cpu_timer=cpu_timer,
                action=action,
                kwargs=kwargs,
                setup=setup,
                teardown=teardown,
            )

            # Measure memory usage of the action
            # We force a garbage collection before measuring memory usage to reduce noise
            # from uncollected garbage. It is run separately from the timing to avoid
            # it affecting the timing measurements.
            #
            # We use the tracemalloc module to measure memory allocations during the action.
            # We start and stop tracemalloc around the action to capture only the memory
            # allocations made during the action.
            if callable(setup):
                setup()

            if iteration_pass <= 1:
                gc.collect()  # Only collect garbage before the first measured iteration

            tracemalloc.start()
            tracemalloc.reset_peak()

            # Measure garbage collection counts baseline before the action
            gc_gen0_start = gc.get_stats()[0]
            gc_gen1_start = gc.get_stats()[1]
            gc_gen2_start = gc.get_stats()[2]

            start_memory_current, start_memory_peak = tracemalloc.get_traced_memory()
            action(**kwargs)
            end_memory_current, end_memory_peak = tracemalloc.get_traced_memory()
            tracemalloc.stop()

            # Measure garbage collection counts after the action
            gc_gen0_end = gc.get_stats()[0]
            gc_gen1_end = gc.get_stats()[1]
            gc_gen2_end = gc.get_stats()[2]

            if callable(teardown):
                teardown()

            if iteration_pass < 1:
                # Warmup iterations not included in results
                continue

            memory = end_memory_current - start_memory_current
            peak_memory = end_memory_peak - start_memory_peak



            iteration_result = _Measurement(
                timing=elapsed,
                cpu_time=cpu_elapsed,
                memory=memory,
                peak_memory=peak_memory,
                gc_gen0_collections=int(gc_gen0_end['collections'] - gc_gen0_start['collections']),
                gc_gen0_collected=int(gc_gen0_end['collected'] - gc_gen0_start['collected']),
                gc_gen0_uncollectable=int(gc_gen0_end['uncollectable'] - gc_gen0_start['uncollectable']),
                gc_gen1_collections=int(gc_gen1_end['collections'] - gc_gen1_start['collections']),
                gc_gen1_collected=int(gc_gen1_end['collected'] - gc_gen1_start['collected']),
                gc_gen1_uncollectable=int(gc_gen1_end['uncollectable'] - gc_gen1_start['uncollectable']),
                gc_gen2_collections=int(gc_gen2_end['collections'] - gc_gen2_start['collections']),
                gc_gen2_collected=int(gc_gen2_end['collected'] - gc_gen2_start['collected']),
                gc_gen2_uncollectable=int(gc_gen2_end['uncollectable'] - gc_gen2_start['uncollectable']),
            )
            iterations_list.append(iteration_result)
            wall_time = float(timer())

            # Update progress display if showing progress
            iteration_completion: float = progress_max * iteration_pass / iterations_min
            wall_time_elapsed_seconds: float = (wall_time - time_start) * defaults.DEFAULT_INTERVAL_SCALE
            time_completion: float = progress_max * (wall_time - time_start) / (min_stop_at - time_start)
            progress_current = int(min(iteration_completion, time_completion))
            progress_tracker.update(
                completed=progress_current,
                description=(
                    f'Benchmarking {group} (iteration {iteration_pass:6d}; time {wall_time_elapsed_seconds:<3.2f}s)'
                ),
            )

        # This takes the 'per-iteration' measurements of metrics and converts them into
        # Values objects for each metric with all iterations collected 'per-metric'
        # instead.
        empty_values = Values(())
        values: list[Values] = [empty_values] * len(_RETAINED_METRICS)
        for metric_index in _RETAINED_METRICS:
            values[metric_index] = Values(tuple(iteration[metric_index] for iteration in iterations_list))
        # Calculate operations per second values as a special case just for easier access
        timing_values: Values = values[_TIMING]
        ops_values: Values = Values(tuple(1 / timing if timing != 0 else 0.0 for timing in timing_values))
        iteration_results: dict[Metric, Values] = {
            _STD_OPS_STATS_METRIC: ops_values,
            _STD_OPS_RAW_METRIC: ops_values
        }
        for metric, metric_index in _METRIC_TO_MEASUREMENT_INDEX.items():
            if values[metric_index]:
                iteration_results[metric] = values[metric_index]

        benchmark_results = Results(
            group=group,
            title=title,
            description=description,
            n=n,
            rounds=rounds,
            iterations=Iterations(iteration_results),
            metrics_timers=MetricsTimers(_timers_for_metrics),
            variation_marks=variation_marks,
            extra_info=Extras()
        )
        progress_tracker.stop()

        return benchmark_results

    def _calibrate_rounds(
        self,
        *,
        calibrate: Calibrate,
        timer: Callable[[], int],
        cpu_timer: Callable[[], int],
        kwargs: dict[str, Any],
        setup: Callable[..., Any] | None = None,
        teardown: Callable[..., Any] | None = None,
        action: Callable[..., Any],
    ) -> int:
        """Auto-calibrate the number of rounds for the benchmark.

        This method estimates an appropriate number of rounds to use for the benchmark
        based on the precision and overhead of the timer functions and the expected
        execution time of the action being benchmarked.

        The goal is to choose a number of rounds such that the total time taken
        for the action is significantly larger than the timer functions' precision and overhead,
        to reduce the impact of timer quantization errors on the measurement.

        It targets a measurement time that provides a specified number of significant figures
        (specified by :data:`~simplebench.defaults.DEFAULT_SIGNIFICANT_FIGURES`) above
        the noise floor of the timer functions.

        :param calibrate: The type of timer to calibrate for (wall-clock or CPU).
        :type calibrate: Calibrate
        :param timer: The timer function to use for the benchmark.
        :type timer: Callable[[], int | float]
        :param cpu_timer: The CPU timer function to use for the benchmark.
        :type cpu_timer: Callable[[], int | float]
        :param kwargs: Keyword arguments to pass to the action.
        :type kwargs: dict[str, Any]
        :param setup: A setup function to run before each iteration.
        :type setup: Callable[..., Any] | None, optional
        :param teardown: A teardown function to run after each iteration.
        :type teardown: Callable[..., Any] | None, optional
        :param action: The action to benchmark.
        :type action: Callable[..., Any]
        :return: The calibrated number of rounds for the benchmark.
        :rtype: int
        """
        if calibrate not in (Calibrate.WALL, Calibrate.CPU):
            raise SimpleBenchTypeError(
                'Invalid calibrate value for rounds calibration; must be Calibrate.WALL or Calibrate.CPU',
                tag=_SimpleRunnerErrorTag.SIMPLERUNNER_CALIBRATE_ROUNDS_INVALID_CALIBRATE_VALUE,
            )
        if not is_valid_timer(timer):
            raise SimpleBenchTypeError(
                'Invalid timer function provided for rounds calibration',
                tag=_SimpleRunnerErrorTag.SIMPLERUNNER_CALIBRATE_ROUNDS_INVALID_TIMER_FUNCTION,
            )
        if not is_valid_timer(cpu_timer):
            raise SimpleBenchTypeError(
                'Invalid CPU timer function provided for rounds calibration',
                tag=_SimpleRunnerErrorTag.SIMPLERUNNER_CALIBRATE_ROUNDS_INVALID_CPU_TIMER_FUNCTION,
            )
        if not isinstance(kwargs, dict):
            raise SimpleBenchTypeError(
                'Invalid kwargs provided for rounds calibration; must be a dict',
                tag=_SimpleRunnerErrorTag.SIMPLERUNNER_CALIBRATE_ROUNDS_INVALID_KWARGS_TYPE,
            )
        if not all(isinstance(key, str) for key in kwargs.keys()):
            raise SimpleBenchTypeError(
                'Invalid kwargs provided for rounds calibration; all keys must be strings',
                tag=_SimpleRunnerErrorTag.SIMPLERUNNER_CALIBRATE_ROUNDS_INVALID_KWARGS_KEY_TYPE,
            )
        if not callable(action):
            raise SimpleBenchTypeError(
                'Invalid action provided for rounds calibration; must be callable',
                tag=_SimpleRunnerErrorTag.SIMPLERUNNER_CALIBRATE_ROUNDS_INVALID_ACTION_TYPE,
            )
        if setup is not None and not callable(setup):
            raise SimpleBenchTypeError(
                'Invalid setup function provided for rounds calibration; must be callable',
                tag=_SimpleRunnerErrorTag.SIMPLERUNNER_CALIBRATE_ROUNDS_INVALID_SETUP,
            )
        if teardown is not None and not callable(teardown):
            raise SimpleBenchTypeError(
                'Invalid teardown function provided for rounds calibration; must be callable',
                tag=_SimpleRunnerErrorTag.SIMPLERUNNER_CALIBRATE_ROUNDS_INVALID_TEARDOWN,
            )

        max_wallclock_calibration_time_ns: float = defaults.MAX_WALLCLOCK_CALIBRATION_TIME * 1_000_000_000
        max_cputime_calibration_time_ns: float = defaults.MAX_CPUTIME_CALIBRATION_TIME * 1_000_000_000

        timer_overhead: float = timer_overhead_ns(timer)
        cpu_timer_overhead: float = timer_overhead_ns(cpu_timer)
        timer_precision: float = timer_precision_ns(timer)
        cpu_timer_precision: float = timer_precision_ns(cpu_timer)

        # Target significant figures for the measurement
        multiplier: float = math.pow(10, defaults.DEFAULT_SIGNIFICANT_FIGURES)

        timer_noise_floor_ns = timer_precision + timer_overhead
        timer_target_time_ns = multiplier * timer_noise_floor_ns

        cpu_timer_noise_floor_ns = cpu_timer_precision + cpu_timer_overhead
        cpu_timer_target_time_ns = multiplier * cpu_timer_noise_floor_ns

        # We start with an initial estimate of rounds and then iteratively increase it until
        # we find a suitable number of rounds that meets our target measurement time above
        # the noise floor of the timer functions.
        noise_floor_scale_factor: int = 10
        estimation_scale_factor: int = 2
        need_teardown: bool = False

        try:
            estimate_rounds: int = 1
            total_action_time_ns: float = 0.0
            total_action_cpu_time_ns: float = 0.0
            timer_metrics: int

            while True:  # Loop until we find an adequate rounds estimate

                # Setup/teardown are inside the calibration loop to make them the same
                # as the actual benchmark iterations, but they are not included in the timed section to avoid
                # affecting the timing measurements.
                if callable(teardown):
                    if callable(setup):
                        setup()
                    need_teardown = True
                elif callable(setup):
                    setup()

                total_action_time_ns, total_action_cpu_time_ns, timer_metrics = self._execute_timed_rounds(
                    rounds=estimate_rounds, timer=timer, cpu_timer=cpu_timer, action=action, kwargs=kwargs
                )

                if need_teardown and callable(teardown):
                    teardown()
                    need_teardown = False

                # Subtract the cumulative overhead from all timed metrics.
                total_measured_time_ns = total_action_time_ns - (timer_overhead * timer_metrics)
                total_measured_cpu_time_ns = total_action_cpu_time_ns - (cpu_timer_overhead * timer_metrics)

                # loop exit conditions
                # We want to break the loop if we've reached the target time for the chosen timer,
                # or if we've hit the maximum number of calibration rounds,
                # or if the measured time has exceeded the maximum calibration time for either timer to
                # avoid excessively long calibration runs.
                if ((calibrate is Calibrate.WALL and  total_measured_time_ns >= timer_target_time_ns)
                        or (calibrate is Calibrate.CPU and total_measured_cpu_time_ns >= cpu_timer_target_time_ns)
                        or (estimate_rounds >= defaults.MAX_CALIBRATION_ROUNDS)
                        or (max_cputime_calibration_time_ns < total_measured_cpu_time_ns)
                        or (max_wallclock_calibration_time_ns < total_measured_time_ns)):
                    break

                # bootstrap quickly above the noise floor of the timer functions by increasing rounds aggressively
                if ((calibrate is Calibrate.WALL and total_measured_time_ns <= timer_noise_floor_ns)
                    or (calibrate is Calibrate.CPU and total_measured_cpu_time_ns <= cpu_timer_noise_floor_ns)):
                    estimate_rounds *= noise_floor_scale_factor
                    if estimate_rounds > defaults.MAX_CALIBRATION_ROUNDS:
                        estimate_rounds = defaults.MAX_CALIBRATION_ROUNDS
                    continue

                # Calculate the average time to estimate the next number of rounds.
                if calibrate is Calibrate.WALL:
                    avg_action_time_ns = total_measured_time_ns / estimate_rounds
                    required_rounds = timer_target_time_ns / avg_action_time_ns
                else:  # calibrate is Calibrate.CPU
                    avg_action_cpu_time_ns = total_measured_cpu_time_ns / estimate_rounds
                    required_rounds = cpu_timer_target_time_ns / avg_action_cpu_time_ns

                estimate_rounds = int(max(required_rounds, estimate_rounds * estimation_scale_factor))
                if estimate_rounds > defaults.MAX_CALIBRATION_ROUNDS:
                    estimate_rounds = defaults.MAX_CALIBRATION_ROUNDS

        except Exception as e:
            raise SimpleBenchRuntimeError(
                'An error occurred during rounds calibration',
                tag=_SimpleRunnerErrorTag.SIMPLERUNNER_CALIBRATE_ROUNDS_ERROR,
            ) from e
        finally:
            # Ensure that if we exited the loop with setup maybe having been called but not teardown,
            # we call teardown to clean up
            if need_teardown and callable(teardown):
                teardown()


        return estimate_rounds
