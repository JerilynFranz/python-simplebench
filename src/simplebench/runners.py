# -*- coding: utf-8 -*-
"""Test runners for benchmarking."""
from __future__ import annotations
import gc
import importlib.util
import sys
import tracemalloc
from typing import Any, Callable, Optional, TYPE_CHECKING
from types import ModuleType

from .defaults import DEFAULT_TIMER, DEFAULT_INTERVAL_SCALE, MIN_MEASURED_ITERATIONS
from .exceptions import ErrorTag, SimpleBenchImportError
from .iteration import Iteration
from .results import Results
from .validators import validate_positive_int


if TYPE_CHECKING:
    from .case import Case
    from .session import Session
    from .tasks import RichTask


def _create_timers_module() -> ModuleType:
    """Creates a module to hold dynamically created timer functions.

    The module is created using importlib and added to sys.modules
    under the name 'simplebench._timers'. If the module already exists
    in sys.modules, it is returned as is.

    Returns:
        ModuleType: The created or existing timers module.

    Raises:
        SimpleBenchImportError: If the module could not be created.
    """
    spec = importlib.util.spec_from_loader('simplebench._timers', loader=None)
    if spec is None:
        raise SimpleBenchImportError(
            'Could not create spec for simplebench._timers module',
            tag=ErrorTag.RUNNERS_CREATE_TIMERS_MODULE_SPEC_FAILED)
    if 'simplebench._timers' in sys.modules:
        return sys.modules['simplebench._timers']
    timers_module = importlib.util.module_from_spec(spec)
    sys.modules['simplebench._timers'] = timers_module
    return timers_module


_timers_module = _create_timers_module()  # Ensure the timers module exists
"""A dynamically created module to hold generated timer functions."""


def _mock_action(**kwargs) -> None:  # pylint: disable=unused-argument
    """A mock action that does nothing."""
    return None


class ProgressTracker:
    """Helper to manage benchmark progress updates."""

    def __init__(self, *,
                 runner: SimpleRunner,
                 task_name: str,
                 progress_max: int | float = 100,
                 description: str = 'Benchmarking') -> None:
        """Initialize the ProgressTracker.

        Args:
            runner (SimpleRunner): The SimpleRunner instance.
            task_name (str): The name of the progress task.
            progress_max (int | float, default=100): The maximum value for progress completion.
            description (str, default='Benchmarking'): The description for the progress task.
        """
        self._session: Session | None = runner.session
        self._task: RichTask | None = None
        if self._session and self._session.show_progress and self._session.tasks:
            self._task = self._session.tasks.get(task_name)
            if not self._task:
                self._task = self._session.tasks.new_task(
                    name=task_name,
                    description=f'  [green]{description}[/green]',
                    completed=0,
                    total=progress_max)
        if self._task:
            self._task.reset()
            self._task.update(
                completed=5,
                description=description)

    def update(self, completed: int | float, description: str, refresh: bool | None = None) -> None:
        """Update progress display."""
        if self._task:
            self._task.update(
                completed=completed,
                description=f'  [green]{description}[/green]',
                refresh=refresh)

    def stop(self) -> None:
        """Stop the progress tracking."""
        if self._task:
            self._task.stop()


class SimpleRunner():
    """A class to run benchmarks for various actions.

    Args:
        case (Case): The benchmark case to run.
        kwargs (dict[str, Any]): The keyword arguments for the benchmark case.
        session (Optional[Session]): The session in which the benchmark is run.
        runner (Optional[Callable[..., Any]]): The function to use to run the benchmark. If None, uses default_runner
            from SimpleRunner.

    Attributes:
        case (Case): The benchmark case to run.
        kwargs (dict[str, Any]): The keyword arguments for the benchmark case.
        session (Optional[Session]): The session in which the benchmark is run.
        run (Callable[..., Any]): The function to use to run the benchmark.
    """
    def __init__(self,
                 *,
                 case: Case,
                 kwargs: dict[str, Any],
                 session: Optional[Session] = None,
                 runner: Optional[Callable[..., Any]] = None) -> None:
        self.case: Case = case
        """The benchmark Case to run."""
        self.kwargs: dict[str, Any] = kwargs
        """The keyword arguments for the benchmark function."""
        self.run: Callable[..., Any] = runner if runner is not None else self.default_runner
        """Benchmark runner function. Defaults to SimpleRunner.default_runner.

        The runner function must accept the following parameters:
            n (int): The number of test rounds that will be run by the action on each iteration.
            action (Callable[..., Any]): The function to benchmark.
            setup (Optional[Callable[..., Any]]): A setup function to run before each iteration.
            teardown (Optional[Callable[..., Any]]): A teardown function to run after each iteration.
            kwargs (Optional[dict[str, Any]]): Keyword arguments to pass to the function being benchmarked.
        """
        self.session: Session | None = session
        """The session in which the benchmark is run."""

    def _timer_function(self, rounds: int) -> Callable[
            [Callable[[], int | float], Callable[..., Any], dict[str, Any]], float]:
        """Returns a timer function for the benchmark.

        The generated function will call the action `rounds` times and return the average time taken.
        The function is generated as a string and then compiled to avoid the overhead of
        a loop in Python during the actual timing benchmark.

        The generated function will have the following signature:

            def _timer_function_{rounds}(
                    timer: Callable[[], float | int],
                    action: Callable[..., Any],
                    kwargs: dict[str, Any]) -> float:

        It is created in the module `simplebench._timers` to avoid polluting the global namespace.

        By creating a new dedicated function for each needed rounds value, we avoid the overhead
        of a loop in Python during the actual timing benchmark. This is particularly important
        for micro-benchmarks where the action being benchmarked is very fast.

        Args:
            rounds (int): The number of test rounds that will be run by the action on each iteration. Must be >= 1.

        Returns:
            Callable[[Callable[[], int | float], Callable[..., Any], dict[str, Any]], float]:
                A function that returns the elapsed time for the benchmark as a float.
        """
        rounds = validate_positive_int(
            rounds, 'rounds',
            ErrorTag.SIMPLERUNNER_TIMER_FUNCTION_INVALID_ROUNDS_TYPE,
            ErrorTag.SIMPLERUNNER_TIMER_FUNCTION_INVALID_ROUNDS_VALUE)

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
            time_function_lines.append(f'    return float((end - start) / {rounds})')
            time_function_code = '\n'.join(time_function_lines)
            exec(time_function_code, _timers_module.__dict__)  # pylint: disable=exec-used

        return getattr(_timers_module, timer_name)

    @property
    def variation_marks(self) -> dict[str, Any]:
        '''Returns the variation marks for the benchmark as defined by the `Case.variation_cols`
        and the current keyworded arguments to the function being benchmarked.

        The variation marks identify the specific variations being tested in a run
        from the kwargs values.

        Returns: dict[str, Any]: The variation marks for the benchmark.
        '''
        return {key: self.kwargs.get(key, None) for key in self.case.variation_cols.keys()}

    def default_runner(
            self,
            *,
            n: int,
            action: Callable[..., Any],
            setup: Optional[Callable[..., Any]] = None,
            teardown: Optional[Callable[..., Any]] = None,
            kwargs: Optional[dict[str, Any]] = None) -> Results:
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
            n (int): The O(n) 'n' weight of the benchmark. This is used to calculate
                a weight for the purpose of O(n) analysis. For example, if the action being benchmarked
                is a function that sorts a list of length n, then n should be the
                length of the list. If the action being benchmarked is a function
                that performs a constant-time operation, then n should be 1.
            rounds (int): The number of test rounds that will be run by the action on each iteration.
            action (Callable[..., Any]): The action to benchmark.
            setup (Optional[Callable[..., Any]]): A setup function to run before each iteration.
            teardown (Optional[Callable[..., Any]]): A teardown function to run after each iteration.
            kwargs (Optional[dict[str, Any]]): Keyword arguments to pass to the action.

        Returns:
            Results: The results of the benchmark.
        """
        if kwargs is None:
            kwargs = {}

        group: str = self.case.group
        title: str = self.case.title
        description: str = self.case.description
        min_time: float = self.case.min_time
        max_time: float = self.case.max_time
        iterations: int = self.case.iterations

        # We force a garbage collection before measuring memory usage to reduce noise
        # from uncollected garbage. It is run separately from the timing to avoid
        # it affecting the timing measurements.
        gc.collect()
        tracemalloc.start()
        start_memory_current, start_memory_peak = tracemalloc.get_traced_memory()
        _mock_action(**kwargs)
        end_memory_current, end_memory_peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()
        memory_overhead: int = end_memory_current - start_memory_current
        peak_memory_overhead: int = end_memory_peak - start_memory_peak

        # warmup iterations are not included in the final stats
        # We start the count from -warmup_iterations to ensure we do the correct number of warmup
        # iterations even if warmup_iterations is 0.
        iteration_pass: int = -self.case.warmup_iterations
        time_start: float = float(DEFAULT_TIMER())
        max_stop_at: float = float(max_time / DEFAULT_INTERVAL_SCALE) + time_start
        min_stop_at: float = float(min_time / DEFAULT_INTERVAL_SCALE) + time_start
        wall_time: float = float(DEFAULT_TIMER())
        iterations_min: int = max(MIN_MEASURED_ITERATIONS, iterations)

        gc.collect()

        progress_max: float = 100.0
        progress_tracker = ProgressTracker(
            runner=self,
            task_name='SimpleRunner:case_runner',
            progress_max=progress_max,
            description=f'Benchmarking {group} (iteration {0:<6d}; time {0.00:<3.2f}s)')

        timer_function = self._timer_function(self.case.rounds)
        total_elapsed: float = 0.0
        iterations_list: list[Iteration] = []
        kiloround_timer = self._timer_function(1000)

        while ((iteration_pass <= iterations_min or wall_time < min_stop_at)
                and wall_time < max_stop_at):
            iteration_pass += 1
            # Time the action
            if self.case.rounds < 1000:
                # for less than 1000 rounds, we can use the generated timer function directly
                if callable(setup):
                    setup()
                elapsed = timer_function(DEFAULT_TIMER, action, kwargs)
                if callable(teardown):
                    teardown()
            else:
                # for 1000 or more rounds, we break the timing into chunks of 1000 rounds (a "kiloround")
                # to reduce the footprint of the generated timer functions and avoid hitting
                # Python's function size limits. Breaking into chunks of 1000 also
                # reduces the overhead of the loop in the timing function to a negligible level.
                elapsed = 0.0
                kiloround_chunks, remaining_rounds = divmod(self.case.rounds, 1000)
                if callable(setup):
                    setup()
                while kiloround_chunks:
                    elapsed += kiloround_timer(DEFAULT_TIMER, action, kwargs)
                    kiloround_chunks -= 1
                if remaining_rounds:
                    partial_timer = self._timer_function(remaining_rounds)
                    elapsed += partial_timer(DEFAULT_TIMER, action, kwargs)
                if callable(teardown):
                    teardown()

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
                # Warmup iterations not included in final stats
                continue

            memory = end_memory_current - start_memory_current - memory_overhead
            peak_memory = end_memory_peak - start_memory_peak - peak_memory_overhead
            iteration_result = Iteration(n=n, elapsed=elapsed, memory=memory, peak_memory=peak_memory)
            iterations_list.append(iteration_result)
            total_elapsed += iteration_result.elapsed
            wall_time = float(DEFAULT_TIMER())

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
            variation_marks=self.variation_marks,
            n=n,
            iterations=iterations_list,
            total_elapsed=total_elapsed,
            extra_info={})
        progress_tracker.stop()

        return benchmark_results
