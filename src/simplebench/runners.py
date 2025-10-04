# -*- coding: utf-8 -*-
"""Test runners for benchmarking."""
from __future__ import annotations
import gc
import tracemalloc
from typing import Any, Callable, Optional, TYPE_CHECKING


from .constants import DEFAULT_TIMER, DEFAULT_INTERVAL_SCALE, MIN_MEASURED_ITERATIONS
from .iteration import Iteration
from .results import Results


if TYPE_CHECKING:
    from .case import Case
    from .session import Session
    from .tasks import RichTask


def _mock_action(**kwargs) -> None:  # pylint: disable=unused-argument
    """A mock action that does nothing."""
    return None


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
            variation_cols (dict[str, str]): The variation columns to use for the benchmark.
            n (int): The number of test rounds that will be run by the action on each iteration.
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
        task_name: str = 'case_runner'
        task: RichTask | None = None
        if self.session and self.session.show_progress and self.session.tasks:
            task = self.session.tasks.get(task_name)
            if not task:
                task = self.session.tasks.new_task(
                    name=task_name,
                    description=f'[green] Benchmarking {group}',
                    completed=0,
                    total=progress_max)
        if task:
            task.reset()
            task.update(
                completed=5,
                description=(f'[green] Benchmarking {group} (iteration {iteration_pass:<6d}; '
                             f'time {0.00:<3.2f}s)'))
        total_elapsed: float = 0.0
        iterations_list: list[Iteration] = []
        while ((iteration_pass <= iterations_min or wall_time < min_stop_at)
                and wall_time < max_stop_at):
            iteration_pass += 1

            if callable(setup):
                setup()

            # Time the action. setup and teardown are not included in the timing.
            raw_timer_start = DEFAULT_TIMER()
            action(**kwargs)
            raw_timer_end = DEFAULT_TIMER()

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
            gc.collect()
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

            # We difference the raw timer readings to avoid floating point
            # precision issues with elapsed time. It effectively pushes the error to the
            # precision of the timer rather than the precision of floating point
            # with small differences between large values.
            elapsed = float(raw_timer_end - raw_timer_start)
            memory = end_memory_current - start_memory_current - memory_overhead
            peak_memory = end_memory_peak - start_memory_peak - peak_memory_overhead
            iteration_result = Iteration(n=n, elapsed=elapsed, memory=memory, peak_memory=peak_memory)
            iterations_list.append(iteration_result)
            total_elapsed += iteration_result.elapsed
            wall_time = float(DEFAULT_TIMER())

            # Update progress display if showing progress
            if task:
                iteration_completion: float = progress_max * iteration_pass / iterations_min
                wall_time_elapsed_seconds: float = (wall_time - time_start) * DEFAULT_INTERVAL_SCALE
                time_completion: float = progress_max * (wall_time - time_start) / (min_stop_at - time_start)
                progress_current = int(min(iteration_completion, time_completion))
                task.update(completed=progress_current,
                            description=(
                                f'[green] Benchmarking {group} (iteration {iteration_pass:6d}; '
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
        if task:
            task.stop()

        return benchmark_results
