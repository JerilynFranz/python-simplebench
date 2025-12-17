"""SimpleRunner for benchmarking.

SimpleRunner is a basic class for running benchmarks for various actions.

It measures the time taken to execute a given action and the memory usage of the action.
It also provides a method to auto-calibrate the number of rounds for the benchmark
timing.

It provides 4 output Results Metrics for each benchmark run:

  - 'simplebench_std::timing_per_operation': The total time taken to execute each operation.
  - 'simplebench_std::operations_per_second': The number of operations performed per second.
  - 'simplebench_std::peak_memory': The peak memory usage of the action.
  - 'simplebench_std::memory': The memory usage of the action.

  The timing_per_operation and operations_per_second are based on the same
  timing measurement, and are therefore consistent with each other. Both are
  provided for convenience and to provide a more complete picture of the benchmark
  results.
"""
from __future__ import annotations

import gc
import importlib.util
import math
import sys
import tracemalloc
from types import ModuleType
from typing import TYPE_CHECKING, Any, Callable, Optional

from simplebench.benchmark_runner import BenchmarkRunner
from simplebench.case.results import Results
from simplebench.case.results.metrics import Iteration, Value
from simplebench.defaults import (
    DEFAULT_INTERVAL_SCALE,
    DEFAULT_SIGNIFICANT_FIGURES,
    DEFAULT_TIMER,
    MIN_MEASURED_ITERATIONS,
)
from simplebench.display.progress_tracker import ProgressTracker
from simplebench.enums import Color
from simplebench.exceptions import SimpleBenchImportError, SimpleBenchTimeoutError, SimpleBenchTypeError
from simplebench.metric import metrics_registry
from simplebench.timeout import Timeout
from simplebench.timers import is_valid_timer, timer_overhead_ns, timer_precision_ns
from simplebench.validators import validate_positive_int

from ._error_tags import _SimpleRunnerErrorTag

if TYPE_CHECKING:
    from simplebench.case import Case
    from simplebench.session import Session


def _create_timers_module() -> ModuleType:
    """Create a module to hold dynamically created timer functions.

    The module is created using :mod:`importlib` and added to :data:`sys.modules`
    under the name 'simplerunner._timers'. If the module already exists
    in :data:`sys.modules`, it is returned as is.

    :return: The created or existing timers module.
    :rtype: ModuleType
    :raises SimpleBenchImportError: If the module could not be created.
    """
    spec = importlib.util.spec_from_loader('simplerunner._timers', loader=None)
    if spec is None:
        raise SimpleBenchImportError(
            'Could not create spec for simplerunner._timers module',
            tag=_SimpleRunnerErrorTag.RUNNERS_CREATE_TIMERS_MODULE_SPEC_FAILED)
    if 'simplerunner._timers' in sys.modules:
        return sys.modules['simplerunner._timers']
    timers_module = importlib.util.module_from_spec(spec)
    sys.modules['simplerunner._timers'] = timers_module
    return timers_module


_timers_module = _create_timers_module()  # Ensure the timers module exists
"""A dynamically created module to hold generated timer functions."""


class SimpleRunner(BenchmarkRunner):
    """A class to run benchmarks for various actions.

    :param case: The benchmark case to run.
    :type case: Case
    :param kwargs: The keyword arguments for the benchmark case.
    :type kwargs: dict[str, Any]
    :param session: The session in which the benchmark is run.
    :type session: Session, optional
    :param runners: The BenchmarkRunner classes to use to run the benchmark.
    :type runners: Callable[..., Any], optional

    :ivar case: The benchmark case to run.
    :vartype case: Case
    :ivar kwargs: The keyword arguments for the benchmark case.
    :vartype kwargs: dict[str, Any]
    :ivar session: The session in which the benchmark is run.
    :vartype session: Session, optional
    :ivar run: The function to use to run the benchmark.
    :vartype run: Callable[..., Any]
    """
    def __init__(self,
                 *,
                 case: Case,
                 kwargs: dict[str, Any],
                 session: Optional[Session] = None,
                 runner: Optional[Callable[..., Any]] = None) -> None:
        """
        :param case: The benchmark case to run.
        :param kwargs: The keyword arguments for the benchmark case.
        :param session: The session in which the benchmark is run.
        :type session: Session, optional
        :ivar runner: The function to use to run the benchmark. If None, uses :meth:`default_runner`
            from :class:`SimpleRunner`.
        :type runner: Callable[..., Any], optional

        :ivar case: The benchmark case to run.
        :vartype case: Case
        :ivar kwargs: The keyword arguments for the benchmark case.
        :vartype kwargs: dict[str, Any]
        :ivar session: The session in which the benchmark is run.
        :vartype session: Session, optional
        :ivar run: The function to use to run the benchmark.
        :vartype run: Callable[..., Any]
        """
        self.case = case
        self.kwargs = kwargs
        self._runner: Callable[..., Any] = self.default_runner
        """Benchmark runner function. Defaults to :meth:`SimpleRunner.default_runner`.

        The runner function must accept the following parameters:
            n (int | float): The **O()** 'n' weight of the benchmark.
            This is used to calculate a weight for the purpose of **O()** analysis.

            For example, if the action being benchmarked is a function that
            sorts a list of length n, then n should be the length of the list.
            If the action being benchmarked is a function that performs
            a constant-time operation, then n should be 1.
            action (Callable[..., Any]): The function to benchmark.
            setup (Optional[Callable[..., Any]]): A setup function to run before each iteration.
            teardown (Optional[Callable[..., Any]]): A teardown function to run after each iteration.
            kwargs (Optional[dict[str, Any]]): Keyword arguments to pass to the function being benchmarked.
        """
        self.session = session

    def run(self,
            *,
            n: int | float,
            action: Callable[..., Any],
            setup: Optional[Callable[..., Any]] = None,
            teardown: Optional[Callable[..., Any]] = None,
            kwargs: Optional[dict[str, Any]] = None) -> Results:
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
        :param kwargs: Keyword arguments to pass to the function being benchmarked.
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
        func_name = getattr(action, "__qualname__",
                            getattr(action, "__name__",
                                    repr(action)))
        benchmark_id = self.case.benchmark_id
        timeout_interval = self.case.timeout
        try:
            result = Timeout(timeout_interval).run(
                self._runner,
                n=n,
                action=action,
                setup=setup,
                teardown=teardown,
                kwargs=kwargs)
        except SimpleBenchTimeoutError as e:
            raise SimpleBenchTimeoutError(
                f'Benchmark "{benchmark_id}" timed out after {timeout_interval} seconds without a result',
                tag=_SimpleRunnerErrorTag.SIMPLERUNNER_BENCHMARK_TIMEOUT,
                func_name=func_name) from e
        return result

    def _timer_function(self, rounds: int) -> Callable[
            [Callable[[], int | float], Callable[..., Any], dict[str, Any]], float]:
        """Return a timer function for the benchmark.

        The generated function will call the action `rounds` times and return the total time taken.
        The function is generated as a string and then compiled to avoid the overhead of
        a loop in Python during the actual timing benchmark.

        The generated function will have the following signature:

        .. code-block:: python

            def _timer_function_{rounds}(
                    timer: Callable[[], float | int],
                    action: Callable[..., Any],
                    kwargs: dict[str, Any]) -> float:

        It is created in the module ``simplerunner._timers`` to avoid polluting the global namespace.

        By creating a new dedicated function for each needed rounds value, we avoid the overhead
        of a loop in Python during the actual timing benchmark. This is particularly important
        for micro-benchmarks where the action being benchmarked is very fast.

        :param rounds: The number of test rounds that will be run by the action on each iteration. Must be >= 1.
        :type rounds: int
        :return: A function that returns the elapsed time for the benchmark as a float.
        :rtype: Callable[[Callable[[], int | float], Callable[..., Any], dict[str, Any]], float]
        """
        rounds = validate_positive_int(
            rounds, 'rounds',
            _SimpleRunnerErrorTag.SIMPLERUNNER_TIMER_FUNCTION_INVALID_ROUNDS_TYPE,
            _SimpleRunnerErrorTag.SIMPLERUNNER_TIMER_FUNCTION_INVALID_ROUNDS_VALUE)

        # If the timer function for the specified rounds does not exist, create it.
        # We create a new function for each rounds value to avoid the overhead of a loop
        # in the timing function.
        # The function is created as a string and then compiled to avoid the overhead
        # of a loop in Python during the actual timing benchmark.
        timer_name = f'_simplerunner_timer_function_{rounds}'
        if not hasattr(_timers_module, timer_name):
            time_function_lines: list[str] = []
            time_function_lines.append(f'def {timer_name}(timer: Callable[[], float | int], action: Callable[..., Any], kwargs: dict[str, Any]) -> float:')  # pylint: disable=line-too-long  # noqa: E501
            time_function_lines.append('    start = timer()')
            time_function_lines.extend(['    action(**kwargs)'] * rounds)
            time_function_lines.append('    end = timer()')
            time_function_lines.append('    return float(end - start)')
            time_function_code = '\n'.join(time_function_lines)
            exec(time_function_code, _timers_module.__dict__)  # pylint: disable=exec-used

        return getattr(_timers_module, timer_name)

    def _run_timed_iteration(
            self,
            *,
            rounds: int,
            timer: Callable[[], int | float],
            action: Callable[..., Any],
            kwargs: dict[str, Any],
            setup: Optional[Callable[..., Any]],
            teardown: Optional[Callable[..., Any]]) -> float:
        """Run a single timed iteration of the benchmark action for a given number of rounds.
        This method uses an unrolled loop to call the action the specified number of rounds,
        minimizing the overhead of loop control in Python.

        :param rounds: The number of test rounds that will be run by the action for the iteration.
        :param timer: The timer function to use for timing.
        :param action: The action to benchmark.
        :param kwargs: Keyword arguments to pass to the action.
        :param setup: A setup function to run before the iteration.
        :param teardown: A teardown function to run after the iteration.
        :return: The elapsed time for the iteration in seconds.
        """
        kiloround_timer = self._timer_function(1000)
        timer_metrics: int
        if rounds < 1000:
            # for less than 1000 rounds, we can use the generated timer function directly
            timer_metrics = 1
            if callable(setup):
                setup()
            elapsed = self._timer_function(rounds)(timer, action, kwargs)
            if callable(teardown):
                teardown()
        else:
            # for 1000 or more rounds, we break the timing into chunks of 1000 rounds (a "kiloround")
            # to reduce the footprint of the generated timer functions and avoid hitting
            # Python's function size limits.
            elapsed = 0.0
            timer_metrics = 0
            kiloround_chunks, remaining_rounds = divmod(rounds, 1000)
            if callable(setup):
                setup()
            while kiloround_chunks:
                elapsed += kiloround_timer(timer, action, kwargs)
                kiloround_chunks -= 1
                timer_metrics += 1
            if remaining_rounds:
                partial_timer = self._timer_function(remaining_rounds)
                elapsed += partial_timer(timer, action, kwargs)
                timer_metrics += 1
            if callable(teardown):
                teardown()
        return elapsed - timer_overhead_ns(timer) * timer_metrics

    def default_runner(
            self,
            *,
            n: int | float,
            action: Callable[..., Any],
            setup: Optional[Callable[..., Any]] = None,
            teardown: Optional[Callable[..., Any]] = None,
            kwargs: Optional[dict[str, Any]] = None) -> Results:
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
        :param action: The action to benchmark.
        :param setup: A setup function to run before each iteration.
        :param teardown: A teardown function to run after each iteration.
        :param kwargs: Keyword arguments to pass to the action.
        :return: The results of the benchmark.
        :rtype: Results
        """
        if kwargs is None:
            kwargs = {}

        group: str = self.case.group
        title: str = self.case.title
        description: str = self.case.description
        min_time: float = self.case.min_time
        max_time: float = self.case.max_time
        iterations: int = self.case.iterations

        # Prioritize the timer from the case, then from the session, then use the default timer
        timer = DEFAULT_TIMER
        if self.case.timer is not None:
            timer = self.case.timer
        elif self.session is not None and self.session.timer is not None:
            timer = self.session.timer

        # warmup iterations are not included in the final stats
        # We start the count from -warmup_iterations to ensure we do the correct number of warmup
        # iterations even if warmup_iterations is 0.
        iteration_pass: int = -self.case.warmup_iterations
        time_start: float = float(timer())
        max_stop_at: float = float(max_time / DEFAULT_INTERVAL_SCALE) + time_start
        min_stop_at: float = float(min_time / DEFAULT_INTERVAL_SCALE) + time_start
        wall_time: float = float(timer())
        iterations_min: int = max(MIN_MEASURED_ITERATIONS, iterations)

        rounds: int
        if self.case.rounds is None:
            rounds = self._calibrate_rounds(
                timer=timer,
                kwargs=kwargs,
                setup=setup,
                teardown=teardown,
                action=action)
        else:
            rounds = self.case.rounds

        gc.collect()

        progress_max: float = 100.0
        progress_tracker = ProgressTracker(
            session=self.session,
            task_name='SimpleRunner:case_runner',
            progress_max=progress_max,
            description=f'Benchmarking {group} (iteration {0:<6d}; time {0.00:<3.2f}s)',
            color=Color.GREEN)

        iterations_list: list[Iteration] = []
        elapsed_metric = metrics_registry['STD_TIMING']
        memory_metric = metrics_registry['STD_MEMORY']
        peak_memory_metric = metrics_registry['STD_PEAK_MEMORY']

        while ((iteration_pass <= iterations_min or wall_time < min_stop_at)
                and wall_time < max_stop_at):
            iteration_pass += 1
            # Time the action
            elapsed = self._run_timed_iteration(
                rounds=rounds,
                timer=timer,
                action=action,
                kwargs=kwargs,
                setup=setup,
                teardown=teardown)

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
            start_memory_current, start_memory_peak = tracemalloc.get_traced_memory()
            action(**kwargs)
            end_memory_current, end_memory_peak = tracemalloc.get_traced_memory()
            tracemalloc.stop()
            if callable(teardown):
                teardown()

            if iteration_pass < 1:
                # Warmup iterations not included in results
                continue

            memory = end_memory_current - start_memory_current
            peak_memory = end_memory_peak - start_memory_peak

            iteration_result = Iteration((
                Value(elapsed_metric, float(elapsed)),
                Value(memory_metric, float(memory)),
                Value(peak_memory_metric, float(peak_memory))
            ))

            iterations_list.append(iteration_result)
            wall_time = float(timer())

            # Update progress display if showing progress
            iteration_completion: float = progress_max * iteration_pass / iterations_min
            wall_time_elapsed_seconds: float = (wall_time - time_start) * DEFAULT_INTERVAL_SCALE
            time_completion: float = progress_max * (wall_time - time_start) / (min_stop_at - time_start)
            progress_current = int(min(iteration_completion, time_completion))
            progress_tracker.update(
                completed=progress_current,
                description=(
                    f'Benchmarking {group} (iteration {iteration_pass:6d}; '
                    f'time {wall_time_elapsed_seconds:<3.2f}s)'))

        benchmark_results = Results(
            group=group,
            title=title,
            description=description,
            n=n,
            rounds=rounds,
            iterations=iterations_list,
            extra_info={})
        progress_tracker.stop()

        return benchmark_results

    def _calibrate_rounds(self, *,  # noqa: C901
                          timer: Callable[[], int],
                          kwargs: dict[str, Any],
                          setup: Optional[Callable[..., Any]] = None,
                          teardown: Optional[Callable[..., Any]] = None,
                          action: Callable[..., Any]) -> int:
        """Auto-calibrate the number of rounds for the benchmark.

        This method estimates an appropriate number of rounds to use for the benchmark
        based on the precision and overhead of the timer function and the expected
        execution time of the action being benchmarked.

        The goal is to choose a number of rounds such that the total time taken
        for the action is significantly larger than the timer precision and overhead,
        to reduce the impact of timer quantization errors on the measurement.

        :param timer: The timer function to use for the benchmark.
        :param kwargs: Keyword arguments to pass to the action.
        :param setup: A setup function to run before each iteration.
        :param teardown: A teardown function to run after each iteration.
        :param action: The action to benchmark.
        :return: The calibrated number of rounds for the benchmark.
        """
        if not is_valid_timer(timer):
            raise SimpleBenchTypeError(
                'Invalid timer function provided for rounds calibration',
                tag=_SimpleRunnerErrorTag.SIMPLERUNNER_CALIBRATE_ROUNDS_INVALID_TIMER_FUNCTION)
        if not isinstance(kwargs, dict):
            raise SimpleBenchTypeError(
                'Invalid kwargs provided for rounds calibration; must be a dict',
                tag=_SimpleRunnerErrorTag.SIMPLERUNNER_CALIBRATE_ROUNDS_INVALID_KWARGS_TYPE)
        if not all(isinstance(key, str) for key in kwargs.keys()):
            raise SimpleBenchTypeError(
                'Invalid kwargs provided for rounds calibration; all keys must be strings',
                tag=_SimpleRunnerErrorTag.SIMPLERUNNER_CALIBRATE_ROUNDS_INVALID_KWARGS_KEY_TYPE)
        if not callable(action):
            raise SimpleBenchTypeError(
                'Invalid action provided for rounds calibration; must be callable',
                tag=_SimpleRunnerErrorTag.SIMPLERUNNER_CALIBRATE_ROUNDS_INVALID_ACTION_TYPE)
        if setup is not None and not callable(setup):
            raise SimpleBenchTypeError(
                'Invalid setup function provided for rounds calibration; must be callable',
                tag=_SimpleRunnerErrorTag.SIMPLERUNNER_CALIBRATE_ROUNDS_INVALID_SETUP)
        if teardown is not None and not callable(teardown):
            raise SimpleBenchTypeError(
                'Invalid teardown function provided for rounds calibration; must be callable',
                tag=_SimpleRunnerErrorTag.SIMPLERUNNER_CALIBRATE_ROUNDS_INVALID_TEARDOWN)

        timer_overhead: float = timer_overhead_ns(timer)
        timer_precision: float = timer_precision_ns(timer)

        # Target significant figures for the measurement
        multiplier: float = math.pow(10, DEFAULT_SIGNIFICANT_FIGURES)
        noise_floor_ns = timer_precision + timer_overhead
        target_time_ns = multiplier * noise_floor_ns

        if callable(setup):
            setup()

        kiloround_timer = self._timer_function(1000)
        estimate_rounds: int = 1
        while True:  # Loop until we find an adequate rounds estimate
            # Use kiloround chunking to avoid generating excessively large timer functions
            total_action_time_ns: float
            timer_metrics: int
            if estimate_rounds < 1000:
                estimate_timer = self._timer_function(estimate_rounds)
                total_action_time_ns = estimate_timer(timer, action, kwargs)
                timer_metrics = 1
            else:
                total_action_time_ns = 0.0
                timer_metrics = 0
                kiloround_chunks, remaining_rounds = divmod(estimate_rounds, 1000)
                while kiloround_chunks:
                    total_action_time_ns += kiloround_timer(timer, action, kwargs)
                    kiloround_chunks -= 1
                    timer_metrics += 1
                if remaining_rounds:
                    partial_timer = self._timer_function(remaining_rounds)
                    total_action_time_ns += partial_timer(timer, action, kwargs)
                    timer_metrics += 1

            # Subtract the cumulative overhead from all timed metrics.
            total_measured_time_ns = total_action_time_ns - (timer_overhead * timer_metrics)

            # loop exit condition
            if total_measured_time_ns >= target_time_ns:
                break

            if total_measured_time_ns <= 0:
                estimate_rounds *= 10
                continue

            # Calculate the average time to estimate the next number of rounds.
            avg_action_time_ns = total_measured_time_ns / estimate_rounds
            required_rounds = target_time_ns / avg_action_time_ns
            estimate_rounds = int(max(required_rounds, estimate_rounds * 10))

        if callable(teardown):
            teardown()

        return estimate_rounds
