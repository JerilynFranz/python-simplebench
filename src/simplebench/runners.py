# -*- coding: utf-8 -*-
"""Test runners for benchmarking."""
from __future__ import annotations
import gc
from typing import Any, Callable, Optional, TYPE_CHECKING

from .constants import DEFAULT_TIMER, DEFAULT_INTERVAL_SCALE, MIN_MEASURED_ITERATIONS
from .iteration import Iteration
from .results import Results


if TYPE_CHECKING:
    from .case import Case
    from .session import Session
    from .tasks import RichTask


class SimpleRunner():
    """A class to run benchmarks for various actions.

    Args:
        case (Case): The benchmark case to run.
        kwargs (dict[str, Any]): The keyword arguments for the benchmark case.
        session (Optional[Session]): The session in which the benchmark is run.
        runner (Optional[Callable[..., Any]]): The function to use to run the benchmark. If None, uses default_runner.

    Attributes:
        case (Case): The benchmark case to run.
        kwargs (dict[str, Any]): The keyword arguments for the benchmark case.
        session (Optional[Session]): The session in which the benchmark is run.
        run (Callable[..., Any]): The function to use to run the benchmark.
    """
    def __init__(self,
                 case: Case,
                 kwargs: dict[str, Any],
                 session: Optional[Session] = None,
                 runner: Optional[Callable[..., Any]] = None) -> None:
        self.case: Case = case
        self.kwargs: dict[str, Any] = kwargs
        self.run: Callable[..., Any] = runner if runner is not None else self.default_runner
        self.session: Session | None = session

    @property
    def variation_marks(self) -> dict[str, Any]:
        '''Return the variation marks for the benchmark.

        The variation marks identify the specific variations being tested in a run
        from the kwargs values.

        Returns: dict[str, Any]: The variation marks for the benchmark.
        '''
        return {key: self.kwargs.get(key, None) for key in self.case.variation_cols.keys()}

    def default_runner(
            self,
            n: int,
            action: Callable[..., Any],
            setup: Optional[Callable[..., Any]] = None,
            teardown: Optional[Callable[..., Any]] = None) -> Results:
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
        total_elapsed: int = 0
        iterations_list: list[Iteration] = []
        while ((iteration_pass <= iterations_min or wall_time < min_stop_at)
                and wall_time < max_stop_at):
            iteration_pass += 1
            iteration_result = Iteration()
            iteration_result.elapsed = 0

            if callable(setup):
                setup()

            # Timer for benchmarked code
            timer_start: int = DEFAULT_TIMER()
            action()
            timer_end: int = DEFAULT_TIMER()

            if callable(teardown):
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
