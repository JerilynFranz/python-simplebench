"""Benchmark case declaration and execution."""
from __future__ import annotations

import datetime
import inspect
import itertools
from copy import copy
from pathlib import Path
from typing import TYPE_CHECKING, Any, Callable, Iterable, Optional, Sequence, TypeAlias

from simplebench import defaults, vcs
from simplebench.benchmark_runner import BenchmarkRunner
from simplebench.display.progress_tracker import ProgressTracker
from simplebench.doc_utils import format_docstring
from simplebench.enums import Color
from simplebench.environment import MachineInfo as EnvMachineInfo
from simplebench.exceptions import (
    SimpleBenchAttributeError,
    SimpleBenchBenchmarkError,
    SimpleBenchTimeoutError,
    SimpleBenchValueError,
)
from simplebench.report.versions import v1 as current_report_version
from simplebench.reporters.protocols import ReporterCallback
from simplebench.reporters.reporter.options import ReporterOptions
from simplebench.reporters.validators import validate_reporter_callback
from simplebench.utils import timestamp_to_iso8601
from simplebench.validators import validate_bool

from . import validate
from ._error_tags import _CaseErrorTag
from .function_runner import FunctionRunner
from .mark import Mark

MachineInfo: TypeAlias = current_report_version.MachineInfo

_DEFERRED_IMPORTS_DONE: bool = False

if TYPE_CHECKING:
    from simplebench.report.versions.v1 import Report
    from simplebench.session import Session

    from .results import Results
    _DEFERRED_IMPORTS_DONE = True


def _deferred_imports() -> None:
    """Perform deferred imports to avoid circular dependencies."""
    global _DEFERRED_IMPORTS_DONE, Report  # pylint: disable=global-statement
    if not _DEFERRED_IMPORTS_DONE:
        from simplebench.report.versions.v1 import Report  # pylint: disable=import-outside-toplevel
        _DEFERRED_IMPORTS_DONE = True


def generate_benchmark_id(obj: object | None, action: Callable[..., Any]) -> str:
    """Generate a stable benchmark ID based on action, group, and signature.

    This function attempts to create a stable benchmark ID based on the action
    function's name, its signature (parameter names and types), and the group.
    If this is not possible (e.g., if the action is a lambda or has no name),
    a transient ID based on the instance's id() will be used.

    :param obj: An object instance related to the benchmark case, used for transient ID generation if needed.
    :param action: The action function of the benchmark case.
    :return: A stable benchmark ID string or a transient ID if stability is not possible.
    :rtype: str
    :raises SimpleBenchAttributeError: If the action is a lambda function.
    """
    try:
        # Use __qualname__ to include class context.
        action_qualname = getattr(action, '__qualname__', '<unknown>')
        if action_qualname == '<lambda>':
            raise SimpleBenchAttributeError(
                'Lambda functions do not have stable names.',
                tag=_CaseErrorTag.INVALID_BENCHMARK_ID_VALUE,
                obj=obj,
                name='__qualname__')

        # Get the filename where the action is defined.
        module_file = Path(inspect.getfile(action)).name

        action_signature = inspect.signature(action)
        signature_parts = []
        for param in action_signature.parameters.values():
            param_type = 'Any'
            if param.annotation is not inspect.Parameter.empty:
                if isinstance(param.annotation, type):
                    param_type = param.annotation.__name__
                else:
                    param_type = str(param.annotation)
            signature_parts.append(f'{param.name}:{param_type}')
        signature_str = ','.join(signature_parts)

        # Combine filename, qualname, and signature for a more unique ID.
        benchmark_id = f'{module_file}::{action_qualname}({signature_str})'
        return benchmark_id
    except (AttributeError, TypeError):  # More specific exception handling
        # Fallback to transient ID for built-ins, interactively defined functions, etc.
        return f'transient-{id(obj)}'


class Case:
    '''
    A benchmark case defines the specific benchmark to be run, including the
    action to be performed, the parameters for the benchmark, and any variations
    of those parameters as well as the reporting group and title for the benchmark.

    It also defines the number of iterations, warmup iterations, rounds, minimum and maximum
    time for the benchmark, the benchmark runner to use, and any callbacks to be invoked
    to process the results of the benchmark for reporting purposes.

    The min_time, max_time, iterations, and warmup_iterations parameters control how
    the benchmark is executed and measured and interact with each other as follows when
    using the default SimpleRunner:
    - The benchmark will perform `warmup_iterations` iterations before starting the timing
        and measurement phase. This is done to allow for any setup or caching effects to stabilize.
        This is separate from the main benchmark iterations and does not count towards the
        `iterations` count or the `min_time`/`max_time` limits.
    - The benchmark will run for at least `min_time` wall clock seconds, but will stop on
        completing the first iteration that ends after `max_time` seconds during the timing phase.
    - If the benchmark completes `iterations` iterations after `min_time` but before
        reaching `max_time`, it will stop.

    This means that the benchmark will run for at least `min_time` seconds and
    for at least one iteration during the timing phase. If `min_time` is reached
    before `iterations` is completed, the benchmark will continue running until
    either `iterations` or `max_time` is completed (whichever happens first).

    `rounds` specifies the number of times the action will be executed per iteration to get a better average.
    Each iteration will run the specified number of rounds after setup and before teardown. The timing
    for the iteration will be the average time taken for the rounds in that iteration.

    This helps to reduce the impact of variability in execution time for a single run of the action
    for very fast actions. This suppresses the overhead of the loop and timer quantization in Python
    during the actual timing benchmark/measurement phase. Internally, the action is called `rounds` times
    in an unrolled loop for each iteration, and the average time per call is used for the iteration timing.

    This removes the overhead of the loop and timer quantization in Python during the actual timing
    benchmark/measurement phase by aggregating multiple calls to the action within a single iteration
    without the overhead of looping constructs. This allows for more accurate timing of very fast actions
    by reducing the relative impact of loop overhead and timer resolution limitations.

    The trade-off is that total number of action calls is now `iterations * rounds`, and
    the reported time per action call is an average over the rounds in each iteration. This can
    dramatically improve the accuracy of timing measurements for very fast actions, at the cost
    of increased total execution time for the benchmark due to the additional calls to the action.

    The unrolled loop means that setup and teardown functions (if any) are called only once per iteration,
    not once per round. All rounds in the same iteration share the same setup/teardown context.

    It is recommended to leave `rounds` to its default of ``None``. A setting of ``None`` enables
    auto-calibration of rounds based on the expected execution time of the action and the
    precision and overhead of the timer function. If you do use it, you may want to run dual benchmarks
    with `rounds=1` and `rounds >> 1` to see how much the reported variability and other metrics change.

    The Case class is designed to be immutable after creation. Once a Case instance
    is created, its properties cannot be directly changed. This immutability ensures that
    benchmark cases remain consistent throughout their lifecycle.

    The results of the benchmark runs are stored in the `results` property, which is a list
    of Results objects. Each Results object corresponds to a specific combination of
    keyword argument variations.

    .. code-block:: python3
      :caption: Minimal Example

        from simplebench import (
            Case, BenchmarkRunner, Results, main)


        def my_benchmark_action(_bench: BenchmarkRunner,
                                **kwargs) -> Results:
            # Perform benchmark action here
            def benchmark_operation():
                sum(range(1000))  # Example operation to benchmark

            return _bench.run(benchmark_operation)


        if __name__ == '__main__':
            cases_list: list[Case] = [
                Case(action=my_benchmark_action)
            ]
            main(cases_list)

    '''
    __slots__ = ('_group', '_title', '_description', '_action',
                 '_iterations', '_warmup_iterations', '_min_time', '_max_time',
                 '_variation_cols', '_kwargs_variations', '_variation_marks', '_runners',
                 '_callback', '_results', '_options', '_rounds',
                 '_benchmark_id', '_vcs_info', '_timeout', '_timer', '_cpu_timer',
                 '_report_cache', '_report_cache_raw_data', '_benchmarks_have_run',
                 '_timestamp', '_epoch_timestamp')

    @format_docstring(DEFAULT_TIMEOUT_GRACE_PERIOD=defaults.DEFAULT_TIMEOUT_GRACE_PERIOD,
                      DEFAULT_TIMER=defaults.DEFAULT_TIMER.__name__,
                      DEFAULT_CPU_TIMER=defaults.DEFAULT_CPU_TIMER.__name__,
                      )
    def __init__(self, *,
                 benchmark_id: Optional[str] = None,
                 vcs_info: Optional[vcs.VCSInfo] = None,
                 action: FunctionRunner,
                 group: str = 'default',
                 title: Optional[str] = None,
                 description: Optional[str] = None,
                 iterations: int = defaults.DEFAULT_ITERATIONS,
                 warmup_iterations: int = defaults.DEFAULT_WARMUP_ITERATIONS,
                 rounds: int | None = None,
                 timer: Callable[[], int] | None = None,
                 cpu_timer: Callable[[], int] | None = None,
                 min_time: float = defaults.DEFAULT_MIN_TIME,
                 max_time: float = defaults.DEFAULT_MAX_TIME,
                 timeout: float | int | None = None,
                 variation_cols: Optional[dict[str, str]] = None,
                 kwargs_variations: Optional[dict[str, list[Any]]] = None,
                 runners: Sequence[type[BenchmarkRunner]] | None = None,
                 callback: Optional[ReporterCallback] = None,
                 options: Optional[Iterable[ReporterOptions]] = None) -> None:
        """The only REQUIRED parameter is `action`.

        :param benchmark_id: An optional unique identifier for the benchmark case.

            If None, a transient ID is assigned. This is meant to provide a stable identifier for the
            benchmark case across multiple runs for tracking purposes. If not provided,
            an attempt will be made to generate a stable ID based on the the action function
            name, signature, and group. If that is not possible, a transient ID based
            on the instance's id() will be used. If a transient ID is used, it will differ
            between runs and cannot be used to correlate results across multiple runs.

            Benchmark ids must be unique within a benchmarking session and stable across runs
            or they cannot be used for tracking benchmark results over time.
        :param vcs_info: An optional vcs.VCSInfo instance representing the state of the VCS repository.

            If not provided, the vcs.VCSInfo will be automatically retrieved from the current
            context of the caller if the code is part of a VCS repository.
        :param action: The function to perform the benchmark.

            This function must accept a `bench` instance of type BenchmarkRunner and
            arbitrary keyword arguments ('**kwargs'). See the ``ActionRunner``
            protocol for the exact signature required. It must return a `Results` object.
        :param group: The benchmark reporting group to which the benchmark case belongs.

            Benchmarks with the same group can be selected for execution without running
            other benchmarks. If not specified, the default group 'default' is used.
        :param title: The title of the benchmark case.

            If None, the name of the action function will be used. Cannot be blank.
        :param description: A brief description of the benchmark case.

            If None, the docstring of the action function will be used, or
            '(no description)' if no docstring is available. Cannot be blank.
        :param iterations: The minimum number of iterations to run for the benchmark.
        :param warmup_iterations: The number of warmup iterations to run before the benchmark.
        :param rounds: The number of rounds to run for the benchmark.

            Rounds are multiple runs of calls to the action within an iteration to mitigate timer
            quantization, loop overhead, and other measurement effects for very fast actions. Setup and teardown
            functions are called only once per iteration (all rounds in the same iteration share the same
            setup/teardown context).

            If None, rounds will be auto-calibrated based on the precision and overhead of the timer function
            and the expected execution time of the action. If the action is very fast (e.g., under
            10 microseconds), rounds will be set to a higher value to improve measurement accuracy
            with the goal of reducing timer quantization errors. If the action is slower, rounds
            will be set lower values.

            If specified, it must be a positive integer.
        :param timer: The timer function to use for the benchmark. If None, the default timer
            from the Session() (if set) or from `simplebench.defaults.DEFAULT_TIMER` ({DEFAULT_TIMER})
            is used by benchmark runners that require a timer.

            The timer function should be a callable that returns a float or int representing the current time.
        :param cpu_timer: The CPU timer function to use for the benchmark. If None, the default CPU timer
            from the Session() (if set) or from `simplebench.defaults.DEFAULT_CPU_TIMER` ({DEFAULT_CPU_TIMER})
            is used by benchmark runners that require a CPU timer.

            The CPU timer function should be a callable that returns a float or int representing the current CPU time.
        :param min_time: The minimum time for the benchmark to run in seconds. Its reference depends on the timer used,
            but by default it is wall-clock time.
        :param max_time: The maximum time for the benchmark run in seconds. Its reference depends on the timer used,
            but by default it is wall-clock time.
        :param timeout: How long to wait before timing out a benchmark run (in seconds). It is
            measured as wall-clock time.

            If None, it waits the full duration of ``max_time`` plus the default timeout grace period
            ({DEFAULT_TIMEOUT_GRACE_PERIOD} seconds). It must be a positive float or int that is greater
            than ``max_time`` if provided. This is a safety mechanism to prevent runaway benchmarks.

            If the timeout is reached during a run, a :class:`~simplebench.exceptions.SimpleBenchTimeoutError``
            will be raised, and the benchmark case's state to TIMED_OUT.
        :param variation_cols: kwargs to be used for cols to denote kwarg variations.

            Each key is a keyword argument name, and the value is the column label to use for that
            argument. Only keywords that are also in `kwargs_variations` can be used here. These
            fields will be added to the output of reporters that support them as columns of data
            with the specified labels.

            If None, an empty dict is used.
        :param kwargs_variations: A map of keyword argument names to a list of possible values for that argument.

            Default is {}. When tests are run, the benchmark
            will be executed for each combination of the specified keyword argument variations. The action
            function will be called with a `bench` parameter that is an instance of the runner and the
            keyword arguments for the current variation.
            If None, an empty dict is used.

            kwargs_variation values can be of any type, including types that are not easily serializable.
            To handle this situation, the `Mark` class can be used to create standardized marks that
            can be used to represent these variations in results and reports.

            .. code-block:: python3
              :caption: Using Marks for Variation Representation

                from simplebench.case import Case, Mark, Results
                from simplebench.benchmark_runner import SimpleRunner

                def my_benchmark_action(_bench: SimpleRunner, mode: str) -> Results:
                    # Benchmark action implementation
                    pass

                case = Case(
                    action=my_benchmark_action,
                    kwargs_variations={
                        'mode': [Mark('ModeA', 1), Mark('ModeB', 2)]
                    }
                )

        :param runners: A list of runners for the benchmark.

            Any runner classes must be a subclass of BenchmarkRunner and must have a method
            named `run` that accepts the same parameters as BenchmarkRunner.run and returns a Results object.
            The action function will be called with a `bench` parameter that is an instance of the
            custom runner.

            It may also accept additional parameters to the run method as needed. If additional
            parameters are needed for the custom runner, they will need to be passed to the run
            method as keyword arguments.

            No support is provided for passing additional parameters to a custom runner from the @benchmark
            decorator.

            If None, the default SimpleRunner will be used. If multiple runners are specified,
            the benchmark will be run for each runner, and the results will be combined.

        :param callback: A callback function for additional processing of the report.

            The function should must four arguments: the Case instance, the Metric,
            the Format, and the generated report data.

            - case (Case): The `Case` instance processed for the report.
            - metric (Metric): The `Metric` of the report.
            - output_format (Format): The `Format` of the report.
            - output (Any): The generated report data. Note that the actual type of this data will
                depend on the Format specified for the report and the type generated by the
                reporter for that Format

            Omit if no callback is needed by a reporter.
        :param options: A list of additional options for the benchmark case.

            Each option is an instance of ReporterOption or a subclass of ReporterOption.
            Reporter options can be used to customize the output of the benchmark reports for
            specific reporters. Reporters are responsible for extracting applicable ReporterOptions
            from the list of options themselves.
            If None, an empty list is used.
        :raises SimpleBenchTypeError: If any parameter is of incorrect type.
        :raises SimpleBenchValueError: If any parameter has an invalid value.
        """
        _deferred_imports()

        # kwargs_variations processed first so it can be used for cross-validation of action signature
        self._kwargs_variations: dict[str, list[Any]] = validate.kwargs_variations(kwargs_variations)
        self._group: str = validate.group(group)
        self._action: FunctionRunner = validate.action_signature(action, self._kwargs_variations)
        self._title: str = validate.title(self._action, title)
        self._description: str = validate.description(self._action, description)
        self._iterations: int = validate.iterations(iterations)
        self._warmup_iterations: int = validate.warmup_iterations(warmup_iterations)
        self._rounds: int | None = validate.rounds(rounds)
        self._timer: Callable[[], int] | None = validate.timer(timer)
        self._cpu_timer: Callable[[], int] | None = validate.timer(cpu_timer)
        self._min_time: float = validate.min_time(min_time)
        self._max_time: float = validate.max_time(max_time)
        validate.time_range(self._min_time, self._max_time)
        self._timeout: float = validate.timeout(timeout, self._max_time)
        self._benchmark_id = validate.benchmark_id(benchmark_id or generate_benchmark_id(self, action))
        self._variation_cols: dict[str, str] = validate.variation_cols(variation_cols, self._kwargs_variations)
        self._variation_marks: dict[str, tuple[str, ...]] = self._generate_variation_marks()
        self._runners: list[type[BenchmarkRunner]] = validate.runners(runners)
        self._callback: ReporterCallback | None = validate_reporter_callback(callback, allow_none=True)
        self._options : list[ReporterOptions] = validate.options(options)
        self._results: list[Results] = []  # No validation needed here
        self._vcs_info: vcs.VCSInfo | None = validate.vcs_info(vcs_info or vcs.get_vcs_info())

        # internal state
        self._report_cache: Report | None = None
        self._report_cache_raw_data: Report | None = None
        self._benchmarks_have_run: bool = False
        self._timestamp: str = ''
        self._epoch_timestamp: int = 0

    def _generate_variation_marks(self) -> dict[str, tuple[str, ...]]:
        """Generate variation marks for the kwarg variations.

        Each variation value is converted to a string representation suitable for use as a mark value.
        The variation marks are sorted for consistent ordering in reports.

        :return: A dictionary mapping variation column names to mark representation tuples.
        """
        variation_marks: dict[str, tuple[str, ...]] = {}
        for key, values in self.kwargs_variations.items():
            # Defer sorting until after all values are converted to a consistent type.
            # This simplifies the logic and avoids type-hinting issues.
            if all(isinstance(value, (int, float)) for value in values):
                # For numeric types, sort them numerically before converting to strings
                # to ensure a natural sort order (e.g., 1, 2, 10 instead of 1, 10, 2).
                value_marks = [str(v) for v in sorted(values)]
            else:
                # For mixed or non-numeric types, convert all to strings first, then sort.
                processed_values: list[str] = []
                for value in values:
                    if isinstance(value, Mark):
                        processed_values.append(value.name)
                    else:
                        processed_values.append(str(value))
                processed_values.sort()
                value_marks = processed_values
            variation_marks[key] = tuple(value_marks)
        return variation_marks

    @property
    def group(self) -> str:
        """The benchmark reporting group to which the benchmark case belongs for selection
        and reporting purposes.

        Cannot be blank. It is used to categorize and filter benchmark cases."""
        return self._group

    @property
    def title(self) -> str:
        """The name of the benchmark case.

        If not specified, defaults to the name of the action function.
        Cannot be blank."""
        return self._title

    @property
    def description(self) -> str:
        """ A brief description of the benchmark case.

        If not specified, defaults to the docstring of the action function or
        '(no description)' if no docstring is available.

        Cannot be blank."""
        return self._description

    @property
    def action(self) -> FunctionRunner:
        """The function to perform the benchmark.

        The function must accept a `bench` parameter of type BenchmarkRunner and
        arbitrary keyword arguments ('**kwargs') and return a Results object.

        Example:

        .. code-block:: python3

            def my_benchmark_action(*, bench: BenchmarkRunner, **kwargs) -> Results:
                def setup_function(size: int) -> None:
                    # Setup code goes here
                    pass

                def teardown_function(size: int) -> None:
                    # Teardown code goes here
                    pass

                def action_function(size: int) -> None:
                    # The code to benchmark goes here
                    lst = list(range(size))

                # Perform the benchmark using the provided BenchmarkRunner instance
                results: Results = bench.run(
                    n=kwargs.get('size', 1),
                    setup=setup_function, teardown=teardown_function,
                    action=action_function, **kwargs)
                return results
        """
        return self._action

    @property
    def benchmark_id(self) -> str:
        """A unique identifier for the benchmark case.

        It is meant to provide a stable identifier for the benchmark case across
        multiple runs for tracking purposes.

        If not provided, an attempt will be made to generate a stable ID based on
        the the action function name, signature, and group. If that is not possible,
        a transient ID based on the instance's id() will be used.

        If a transient ID is used, it will differ between runs and cannot be used
        to correlate results across multiple runs.

        Benchmark ids must be unique within a benchmarking session.

        Passed ids are stripped of leading and trailing whitespace and validated
        to be non-blank.
        """
        return self._benchmark_id

    @property
    def vcs_info(self) -> vcs.VCSInfo | None:
        """VCS information for the benchmark case.

        This is a read-only attribute that provides VCS information
        such as the current commit hash, branch name, datetime, and
        dirty status of the local repository.

        If the benchmark is not in a file managed by a VCS repository,
        a None value is returned.

        :return: A vcs.VCSInfo object containing VCS information, or None if not in a VCS repository.
        """
        return self._vcs_info

    @property
    def iterations(self) -> int:
        """The number of iterations to run for the benchmark."""
        return self._iterations

    @property
    def warmup_iterations(self) -> int:
        """The number of warmup iterations to run before the benchmark."""
        return self._warmup_iterations

    @property
    def rounds(self) -> int | None:
        """The number of rounds to run for the benchmark for each iteration.

        Rounds are multiple runs of the entire benchmark to get a better average for an iteration.
        Each iteration will run the specified number of rounds after setup and before teardown. (default: 1)"""
        return self._rounds

    @property
    def timer(self) -> Callable[[], int] | None:
        """The timer function to use for the benchmark.

        If None, the default timer from the Session() (if set) or from
        `simplebench.defaults.DEFAULT_TIMER` is used by benchmark runners.

        The timer function should be a callable that returns an int representing the current time.
        """
        return self._timer

    @property
    def cpu_timer(self) -> Callable[[], int] | None:
        """The CPU timer function to use for the benchmark.

        If None, the default CPU timer from the Session() (if set) or from
        `simplebench.defaults.DEFAULT_CPU_TIMER` is used by benchmark runners that require a CPU timer.

        The CPU timer function should be a callable that returns an int representing the current CPU time.
        """
        return self._cpu_timer

    @property
    def min_time(self) -> float:
        """The minimum time for the benchmark in seconds."""
        return self._min_time

    @property
    def max_time(self) -> float:
        """The maximum time for the benchmark in seconds."""
        return self._max_time

    @property
    def timeout(self) -> float:
        """The timeout for the benchmark in seconds."""
        return self._timeout

    @property
    def variation_cols(self) -> dict[str, str]:
        """Keyword arguments to be used for columns to denote kwarg variations.

        Each key is a keyword argument name, and the value is the column label to use for that argument.
        Only keywords that are also in `kwargs_variations` can be used here. These fields will be
        added to the output of reporters that support them as columns of data with the specified labels.

        Note that all keys in variation_cols must be present in kwargs_variations and
        updating it may require changes to both variation_cols and kwargs_variations_cols.

        Updating variation_cols does not automatically update kwargs_variations, and vice versa.

        :return: A dictionary mapping keyword argument names to column labels.
        :rtype: dict[str, str]
        """
        # shallow copy to prevent external modification of internal dict
        return copy(self._variation_cols) if self._variation_cols is not None else {}

    @property
    def kwargs_variations(self) -> dict[str, list[Any]]:
        """Variations of keyword arguments for the benchmark.

        Each key is a keyword argument name, and the value is the column label to use for that argument.
        Only keywords that are also in `kwargs_variations` can be used here. These fields will be
        added to the output of reporters that support them as columns of data with the specified labels.

        When tests are run, the benchmark will be executed for each combination of the specified
        keyword argument variations. For example, if `kwargs_variations` is

        .. code-block:: python3
          :caption: `kwargs_variations` argument example

            ...
            kwargs_variations = {
                    'size': [10, 100],
                    'mode': ['fast', 'accurate']
                },
            ...

        The benchmark will be run 4 times with the following combinations of keyword arguments:

        .. code-block:: python3
          :linenos:
          :caption: Keyword (`**kwargs`) Argument Combinations

            {size=10, mode='fast'}
            {size=10, mode='accurate'}
            {size=100, mode='fast'}
            {size=100, mode='accurate'}

        The action function will be called with these keyword arguments accordingly and must
        accept them.
        """
        if self._kwargs_variations is None:
            return {}
        # shallow copy to prevent external modification of internal dict
        return {key: list(value) for key, value in self._kwargs_variations.items()}

    @property
    def variation_marks(self) -> dict[str, tuple[str, ...]]:
        """Return marks for the kwarg variations.

        :return: A dictionary mapping 'kwarg_name=kwarg_value' to Mark objects.
        """
        # shallow copy to prevent external modification of internal dict
        return copy(self._variation_marks) if self._variation_marks is not None else {}

    @property
    def runners(self) -> list[type[BenchmarkRunner]]:
        """A list of runners for the benchmark.

        If an empty list, the default SimpleRunner will be used. If multiple runners are specified,
        the benchmark will be run for each runner, and the results will be combined.

        A custom runner class must be a subclass of BenchmarkRunner and must have a method
        named `run` that accepts the same parameters as BenchmarkRunner.run and returns a Results object.
        The action function will be called with a `bench` parameter that is an instance of the
        custom runner.

        It may also accept additional parameters to the run method as needed. If additional
        parameters are required, they must be specified in the `action` function signature.
        """
        return self._runners

    @property
    def callback(self) -> ReporterCallback | None:
        """A callback function for additional processing of a report.

        A callback function to be called with the benchmark results in a reporter.
        This function should accept four arguments: the Case instance, the Metric,
        the ReporterOption, and the output object. Leave as None if no callback is needed.
        (default: None)

        :return ReporterCallback | None: The callback function or None if not set.
        """
        return self._callback

    @property
    def results(self) -> list[Results]:
        """The benchmark list of Results for the case.

        This is a read-only attribute. To add results, use the `run` method.

        :return list[Results]: A list of Results objects. One for each variation run in the benchmark case.
        :raises SimpleBenchValueError: If the benchmark case has not been run yet.
        """
        self.validate_has_run()
        # shallow copy to prevent external modification of internal list
        return copy(self._results)

    @property
    def options(self) -> list[ReporterOptions]:
        """A list of additional options for the benchmark case."""
        # shallow copy to prevent external modification of internal list
        return copy(self._options) if self._options is not None else []

    @property
    def expanded_kwargs_variations(self) -> list[dict[str, Any]]:
        """All combinations of keyword arguments from the specified kwargs_variations.

        A mapping of keyword argument names to their variations.

        Each key is a keyword argument name, and the value is a list of possible values.

        When tests are run, the benchmark will be executed for each combination of the specified
        keyword argument variations. For example, if `kwargs_variations` is

        .. code-block:: python3
          :caption: `kwargs_variations` argument example

            ...
            kwargs_variations = {
                    'size': [10, 100],
                    'mode': ['fast', 'accurate']
                },
            ...

        The benchmark will be run 4 times with the following combinations of keyword arguments:

        .. code-block:: python3
          :linenos:
          :caption: Keyword (`**kwargs`) Argument Combinations

            {size=10, mode='fast'}
            {size=10, mode='accurate'}
            {size=100, mode='fast'}
            {size=100, mode='accurate'}

        The action function will be called with these keyword arguments accordingly and must
        accept them.

        :return: A list of dictionaries, each representing a unique combination of keyword arguments.
        :rtype: list[dict[str, Any]]
        """
        keys = self.kwargs_variations.keys()
        values = [self.kwargs_variations[key] for key in keys]
        return [dict(zip(keys, v)) for v in itertools.product(*values)]

    @property
    def timestamp(self) -> str:
        """The ISO 8601 timestamp when the benchmark case was run.

        This is a read-only attribute that is set when the `run` method is called.
        If the benchmark case has not been run yet, it will be an empty string.

        :return: The ISO 8601 timestamp as a string.
        """
        self.validate_has_run('Cannot get timestamp: benchmark case has not been run yet.')
        return self._timestamp

    @property
    def epoch_timestamp(self) -> int:
        """The epoch timestamp when the benchmark case was run.

        This is a read-only attribute that is set when the `run` method is called.
        If the benchmark case has not been run yet, it will be 0.

        :return: The epoch timestamp as an integer.
        """
        return self._epoch_timestamp

    def run(self, session: Session | None = None) -> None:
        """Run the benchmark tests.

        This method will execute the benchmark for each combination of
        runner and keyword arguments and collect the results. After running the
        benchmarks, the results will be stored in the `self.results` attribute.

        If passed, the session's tasks will be used to display progress,
        control verbosity, and pass CLI arguments to the benchmark runner.

        :param session: The session to use for the benchmark case.
        :raises SimpleBenchTimeoutError: If a timeout occurs during the benchmark action.
        :raises SimpleBenchBenchmarkError: If an error occurs during the benchmark action.
        """
        self._set_timestamp(session)

        all_variations = self.expanded_kwargs_variations
        progress_tracker = ProgressTracker(
            session=session,
            task_name='Case:run',
            progress_max=len(all_variations),
            description=f'Running case {self.title}',
            color=Color.CYAN)
        progress_tracker.reset()

        # BenchmarkRunner prioritization is Case().runners -> Session().default_runners -> defaults.DEFAULT_RUNNERS
        runners_list: list[type[BenchmarkRunner]] = self.runners
        if not runners_list and session and session.default_runners:
            runners_list = session.default_runners
        if not runners_list:
            runners_list = defaults.default_runners()

        kwargs: dict[str, Any]
        # We loop over variations in the outside loop so that progress is reported
        # grouped by each variation run, which is more user-friendly than reporting progress
        # grouped by each runner.
        for variations_counter, kwargs in enumerate(all_variations):
            for runner in runners_list:
                bench: BenchmarkRunner = runner(case=self, session=session, kwargs=kwargs)

                try:
                    results: Results = self.action(bench, **kwargs)
                except SimpleBenchTimeoutError as e:
                    raise SimpleBenchTimeoutError(
                        f'Timeout occurred running benchmark action {str(self.action)} for case '
                        f'"{self.title}" with kwargs {kwargs}: {e}',
                        tag=_CaseErrorTag.BENCHMARK_ACTION_TIMEOUT_OCCURRED
                        ) from e
                except Exception as e:
                    raise SimpleBenchBenchmarkError(
                        f'Error occurred running benchmark action {str(self.action)} for case '
                        f'"{self.title}" with kwargs {kwargs}: {e}, {type(e)}',
                        tag=_CaseErrorTag.BENCHMARK_ACTION_RAISED_EXCEPTION
                        ) from e
                self._results.append(results)
            progress_tracker.update(
                description=(
                    f'Running case {self.title} ({variations_counter + 1}/{len(all_variations)})'),
                completed=variations_counter + 1,
                refresh=True)
        progress_tracker.stop()
        self._mark_case_as_run()

    def _set_timestamp(self, session: Session | None) -> None:
        """Set the timestamp for the benchmark case.

        This method sets the timestamp for the benchmark case to the current time.
        If a session is provided, it uses the session's timestamp. Otherwise, it
        uses the current UTC time.

        :param session: The session in which the case is being run.
        """
        if session is not None:
            self._timestamp = session.timestamp
            self._epoch_timestamp = session.epoch_timestamp
        else:
            self._timestamp = datetime.now().timestamp()
            self._epoch_timestamp = timestamp_to_iso8601(self.epoch_timestamp)

    def _mark_case_as_run(self) -> None:
        """Mark the case as having been run.

        This method sets the internal flag to indicate that the benchmarks
        for this case have been executed.

        It also clears any cached report data to ensure that subsequent report generation reflects the latest
        results.

        :param session: The session in which the case was run.
        """
        self._benchmarks_have_run = True
        self._report_cache = None
        self._report_cache_raw_data = None
        self._machine_info: MachineInfo | None = None  # Reset machine info cache

    @property
    def machine_info(self) -> MachineInfo:
        """Get the MachineInfo for the benchmark case.

        This property retrieves the MachineInfo associated with the benchmark case.
        If the MachineInfo has not been set yet, it will be created and cached
        for future access.

        :return: The MachineInfo instance for the benchmark case.
        """
        if self._machine_info is None:
            self._machine_info = MachineInfo.from_system()
        return self._machine_info
    @property
    def has_run(self) -> bool:
        """Returns whether the benchmarks for this case have been run.

        :return: True if the benchmarks have been run, False otherwise.
        """
        return self._benchmarks_have_run

    def report(self, include_raw_data: bool = False) -> Report:
        """Returns the benchmark case and results as a Report object.

        The Report format is a JSON serializable object that includes all the necessary
        information about the benchmark case and its results. This format can be used to
        exchange data between different systems or to store the data in a structured way.

        It conforms to the JSON Schema defined at
        https://raw.githubusercontent.com/JerilynFranz/python-simplebench/main/schemas/v1/report-info.json

        :param include_raw_data: Whether to include raw data. Defaults to False.
        :return: A JSON serializable representation of the benchmark case and results.
        """
        self.validate_has_run()
        validate_bool(
            include_raw_data, 'include_raw_data',
            _CaseErrorTag.INVALID_REPORT_INCLUDE_RAW_DATA_NOT_BOOL)

        if include_raw_data:
            if self._report_cache_raw_data is None:
                self._report_cache_raw_data = Report.from_case(case=self, include_raw_data=True)
            return self._report_cache_raw_data
        else:
            if self._report_cache is None:
                self._report_cache = Report.from_case(case=self, include_raw_data=False)
            return self._report_cache

    def validate_has_run(self, message: str = '') -> None:
        """Validate the has_run state of the benchmark case.

        If the :attr:`has_run` state is not True, raises a SimpleBenchValueError.

        :param message: Optional custom error message to use if the has_run state is not True.
        :raises SimpleBenchValueError: If :attr:`has_run` is not True.
        """
        if not self.has_run:
            raise SimpleBenchValueError(
                    message or f'Cannot generate report for case "{self.title}" because benchmarks have not been run yet. '
                    f'Please run the benchmarks using the `run()` method before generating a report.',
                    tag=_CaseErrorTag.HAVE_NOT_RUN_CASE)
