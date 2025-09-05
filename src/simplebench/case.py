# -*- coding: utf-8 -*-
"""Benchmark case declaration and execution."""
from dataclasses import dataclass, field
import itertools
from typing import Any, Callable, Literal, Optional

from rich.progress import TaskID

from .constants import DEFAULT_ITERATIONS
from .results import Results
from .runners import SimpleRunner
from .session import Session
from .tasks import RichTask


@dataclass(kw_only=True)
class Case:
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

    def __post_init__(self) -> None:
        self.results: list[Results] = []

    @property
    def expanded_kwargs_variations(self) -> list[dict[str, Any]]:
        '''All combinations of keyword arguments from the specified kwargs_variations.

        Returns:
            A list of dictionaries, each representing a unique combination of keyword arguments.
        '''
        keys = self.kwargs_variations.keys()
        values = [self.kwargs_variations[key] for key in keys]
        return [dict(zip(keys, v)) for v in itertools.product(*values)]

    def run(self, session: Optional[Session] = None) -> None:
        """Run the benchmark tests.

        This method will execute the benchmark for each combination of
        keyword arguments and collect the results. After running the
        benchmarks, the results will be stored in the `self.results` attribute.

        If passed, the session's tasks will be used to display progress,
        control verbosity, and pass CLI arguments to the benchmark runner.

        Args:
            session (Optional[Session]): The session to use for the benchmark case.
        """
        all_variations = self.expanded_kwargs_variations
        task_name: str = 'case_variations'
        task: RichTask | None = None
        if session and session.tasks:
            task = session.tasks.get(task_name)
            if not task:
                task = session.tasks.new_task(
                    name=task_name,
                    description=f'[cyan] Running case {self.title}',
                    completed=0,
                    total=len(all_variations))
        if task:
            task.reset()
        collected_results: list[Results] = []
        kwargs: dict[str, Any]
        for variations_counter, kwargs in enumerate(all_variations):
            benchmark: SimpleRunner = SimpleRunner(case=self, session=session, kwargs=kwargs)
            results: Results = self.action(benchmark)
            collected_results.append(results)
            if task:
                task.update(
                        description=(f'[cyan] Running case {self.title} '
                                     f'({variations_counter + 1}/{len(all_variations)})'),
                        completed=variations_counter + 1,
                        refresh=True)
        if task:
            task.stop()
        self.results = collected_results

    def as_dict(self, session: Optional[Session]) -> dict[str, Any]:
        """Returns the benchmark case and results as a JSON serializable dict.

        If passed, the session's args will be used to determine the level of detail
        to include in the results. Without a session or if session.args specifies
        json_data, full results and data will be included. Otherwise, only statistical
        summaries will be included.

        Args:
            session (Optional[Session]): The session to use for the benchmark case.

        Returns:
            dict[str, Any]: A JSON serializable dict representation of the benchmark case and results.
        """
        results = []
        for result in self.results:
            # full dump if no session or if session.args specifies json_data
            if session is None or (session.args is not None and session.args.json_data):
                results.append(result.results_and_data_as_dict)
            else:  # otherwise only stats
                results.append(result.results_as_dict)
        return {
            'type': self.__class__.__name__,
            'group': self.group,
            'title': self.title,
            'description': self.description,
            'variation_cols': self.variation_cols,
            'results': results
        }
