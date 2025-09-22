# -*- coding: utf-8 -*-
"""Benchmark case declaration and execution."""
from __future__ import annotations
from dataclasses import dataclass, field
import itertools
from typing import Any, Callable, Optional, TYPE_CHECKING

from .constants import DEFAULT_ITERATIONS
from .exceptions import SimpleBenchValueError, SimpleBenchTypeError, ErrorTag
from .reporters.reporter_option import ReporterOption
from .runners import SimpleRunner
from .enums import Section

if TYPE_CHECKING:
    from .reporters.choices import Format
    from .results import Results
    from .session import Session
    from .tasks import RichTask


@dataclass(kw_only=True)
class Case:
    '''Declaration of a benchmark case.

    Args:
        group (str): The benchmark reporting group to which the benchmark case belongs.
        title (str): The name of the benchmark case.
        description (str): A brief description of the benchmark case.
        action (Callable[..., Any]): The action to perform for the benchmark.
        iterations (int): The number of iterations to run for the benchmark.
        min_time (float): The minimum time for the benchmark in seconds. (default: 5.0)
        max_time (float): The maximum time for the benchmark in seconds. (default: 20.0)
        variation_cols (dict[str, str]): kwargs to be used for cols to denote kwarg variations.
            Each key is a keyword argument name, and the value is the column label to use for that argument.

            .. code-block:: python
                # example of variation_cols
                variation_cols={
                    'search_depth': 'Search Depth',
                    'runtime_validation': 'Runtime Validation'
                }
        kwargs_variations (dict[str, list[Any]]):
            Variations of keyword arguments for the benchmark.
            Each key is a keyword argument name, and the value is a list of possible values.

            .. code-block:: python
                # example of kwargs_variations
                kwargs_variations={
                    'search_depth': [1, 2, 3],
                    'runtime_validation': [True, False]
                }
        runner (Optional[Callable[..., Any]]): A custom runner for the benchmark.
        callback (Optional[Callable[Case, Section, Format, Any], None]):
            A callback function for additional processing of the report. The function should accept
            four arguments: the Case instance, the Section, the Format, and the generated report data.
            Leave as None if no callback is needed. (default: None)

            The callback function is responsible for handling the returned report data appropriately.
            The actually returned type signature of the data will depend on the Format
            specified for the report:
                - Case: The Case instance processed for the report.
                - Section: The reporters.choices.Section of the report.
                - Format: The reporters.choices.Format of the report.
                - Any: The generated report data (actual type returned depends on the Format).
                    - Format.PLAIN_TEXT: str (the plain text report as a string)
                    - Format.RICH_TEXT: str (the rich text report as a string)
                    - Format.MARKDOWN: str (the markdown report as a string)
                    - Format.CSV: str (the CSV data as a string)
                    - Format.JSON: str (the JSON data as a string)
                    - Format.GRAPH: bytes (the graph image data as bytes)
        options (list[ReporterOption]): A list of additional options for the benchmark case.
        _decoration (bool): This field is used internally to indicate if the Case was created via
            a benchmark decorator. It should not be set manually. (default: False)
    Properties:
        results (list[Results]): The benchmark results for the case.
    '''
    group: str
    """The benchmark reporting group to which the benchmark case belongs."""
    title: str
    """The name of the benchmark case."""
    description: str
    """A brief description of the benchmark case."""
    action: Callable[..., Any]
    """The action to perform for the benchmark."""
    iterations: int = DEFAULT_ITERATIONS
    """The number of iterations to run for the benchmark."""
    min_time: float = 5.0  # seconds
    """The minimum time for the benchmark in seconds."""
    max_time: float = 20.0  # seconds
    """The maximum time for the benchmark in seconds."""
    variation_cols: dict[str, str] = field(default_factory=dict[str, str])
    """Keyword arguments to be used for columns to denote kwarg variations."""
    kwargs_variations: dict[str, list[Any]] = field(default_factory=dict[str, list[Any]])
    """Variations of keyword arguments for the benchmark."""
    runner: Optional[Callable[..., Any]] = None
    """A custom runner for the benchmark."""
    callback: Optional[Callable[[Case, Section, Format, Any], None]] = None
    """A callback function for additional processing of the report."""
    results: list[Results] = field(init=False)
    """The benchmark list of Results for the case."""
    options: list[ReporterOption] = field(default_factory=list[ReporterOption])
    """A list of additional options for the benchmark case."""
    _decoration: bool = field(default=False, repr=False, compare=False)
    """Indicates if the Case was created via the @benchmark decorator. (internal use only)"""

    def __post_init__(self) -> None:
        self.results: list[Results] = []
        self.validate()

    def validate(self) -> None:
        """Validate the benchmark case parameters.

        Raises:
            SimpleBenchValueError: If any of the parameters are invalid.
            SimpleBenchTypeError: If any of the parameters are of the wrong type.
        """
        if self.iterations <= 0:
            raise SimpleBenchValueError(
                f'Invalid iterations: {self.iterations}. Must be a positive integer.',
                tag=ErrorTag.CASE_INVALID_ITERATIONS
                )
        if self.min_time <= 0.0:
            raise SimpleBenchValueError(
                f'Invalid min_time: {self.min_time}. Must be a positive float.',
                tag=ErrorTag.CASE_INVALID_MIN_TIME
                )
        if self.max_time <= 0.0:
            raise SimpleBenchValueError(
                f'Invalid max_time: {self.max_time}. Must be a positive float.',
                tag=ErrorTag.CASE_INVALID_MAX_TIME
                )
        if self.min_time > self.max_time:
            raise SimpleBenchValueError(
                f'Invalid time range: min_time {self.min_time} > max_time {self.max_time}.',
                tag=ErrorTag.CASE_INVALID_TIME_RANGE
                )
        if not callable(self.action):
            raise SimpleBenchTypeError(
                f'Invalid action: {self.action}. Must be a callable.',
                tag=ErrorTag.CASE_INVALID_ACTION_NOT_CALLABLE
                )
        if self.runner is not None and not callable(self.runner):
            raise SimpleBenchTypeError(
                f'Invalid runner: {self.runner}. Must be a callable or None.',
                tag=ErrorTag.CASE_INVALID_RUNNER_NOT_CALLABLE_OR_NONE
                )
        if not isinstance(self.variation_cols, dict):
            raise SimpleBenchTypeError(
                f'Invalid variation_cols: {self.variation_cols}. Must be a dictionary.',
                tag=ErrorTag.CASE_INVALID_VARIATION_COLS_NOT_DICT
                )
        for key, value in self.variation_cols.items():
            if not isinstance(key, str) or not isinstance(value, str):
                raise SimpleBenchValueError(
                    f'Invalid variation_cols entry: {key}: {value}. Keys and values must be strings.',
                    tag=ErrorTag.CASE_INVALID_VARIATION_COLS_ENTRY_NOT_STRINGS
                    )
        if not isinstance(self.kwargs_variations, dict):
            raise SimpleBenchValueError(
                f'Invalid kwargs_variations: {self.kwargs_variations}. Must be a dictionary.',
                tag=ErrorTag.CASE_INVALID_KWARGS_VARIATIONS_NOT_DICT
                )
        if self.callback is not None and not callable(self.callback):
            raise SimpleBenchValueError(
                f'Invalid callback: {self.callback}. Must be a callable or None.',
                tag=ErrorTag.CASE_INVALID_CALLBACK_NOT_CALLABLE_OR_NONE
                )
        if not isinstance(self.options, list):
            raise SimpleBenchTypeError(
                f'Invalid options: {self.options}. Must be a list.',
                tag=ErrorTag.CASE_INVALID_OPTIONS_NOT_LIST
                )
        for option in self.options:
            if not isinstance(option, ReporterOption):
                raise SimpleBenchTypeError(
                    f'Invalid option: {option}. Must be of type ReporterOption.',
                    tag=ErrorTag.CASE_INVALID_OPTIONS_ENTRY_NOT_REPORTER_OPTION
                    )

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
        if session and session.show_progress and session.tasks:
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
            results: Results = self.action(benchmark, **kwargs)
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

    def as_dict(self, full_data: bool = False) -> dict[str, Any]:
        """Returns the benchmark case and results as a JSON serializable dict.

        Only the results statistics are included by default. To include full results data,
        set `full_data` to True.

        Args:
            full_data (bool): Whether to include full results data. Defaults to False.

        Returns:
            dict[str, Any]: A JSON serializable dict representation of the benchmark case and results.
        """
        results = []
        for result in self.results:
            if full_data:  # full data if requested
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

    def section_mean(self, section: Section) -> float:
        """Calculate the mean value for a specific section across all results.

        This method computes the mean value for the specified section
        (either OPS or TIMING) across all benchmark results associated with this case.

        This is a very 'hand-wavy' mean calculation that simply averages
        the means of each result. It does not take into account the number
        of iterations or other statistical factors. It is intended to provide
        a rough estimate of the overall performance for the specified section for
        use in comparisons between successive benchmark runs in tests looking for
        large performance regressions. As such, it should not be used for any rigorous
        statistical analysis.

        Args:
            section (Section): The section for which to calculate the mean.

        Returns:
            float: The mean value for the specified section.
        """
        if not isinstance(section, Section):
            raise SimpleBenchTypeError(
                f'Invalid section type: {type(section)}. Must be of type Section.',
                tag=ErrorTag.CASE_SECTION_MEAN_INVALID_SECTION_TYPE_ARGUMENT
                )
        if section not in (Section.OPS, Section.TIMING):
            raise SimpleBenchValueError(
                f'Invalid section: {section}. Must be Section.OPS or Section.TIMING.',
                tag=ErrorTag.CASE_SECTION_MEAN_INVALID_SECTION_ARGUMENT
                )

        if not self.results:
            return 0.0
        total = 0.0
        count = 0
        for result in self.results:
            if section == Section.OPS:
                total += result.ops_per_second.mean
                count += 1
            elif section == Section.TIMING:
                total += result.per_round_timings.mean
                count += 1
        return total / count if count > 0 else 0.0

    @property
    def decorated(self) -> bool:
        """Returns True if the Case was created via the @benchmark decorator."""
        return self._decoration
