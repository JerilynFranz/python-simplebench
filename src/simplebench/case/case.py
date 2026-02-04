"""Benchmark case declaration and execution."""
import inspect
import itertools
from collections.abc import Callable, Mapping
from datetime import datetime
from pathlib import Path
from typing import TYPE_CHECKING, Any

import simplebench.defaults as defaults
import simplebench.vcs as vcs
from simplebench.benchmark_runner import BenchmarkRunner
from simplebench.display.progress_tracker import ProgressTracker
from simplebench.doc_utils import format_docstring
from simplebench.enums import Color
from simplebench.exceptions import (
    SimpleBenchAttributeError,
    SimpleBenchBenchmarkError,
    SimpleBenchRuntimeError,
    SimpleBenchTimeoutError,
)
from simplebench.options.reporter.options import ReporterOptions
from simplebench.report.versions import v1 as reports
from simplebench.reporters.protocols import ReporterCallback
from simplebench.reporters.validators import validate_reporter_callback
from simplebench.simplebench_types import ElementCollection, KWArgsVariations, VariationCols, VariationMarks
from simplebench.utils import timestamp_to_iso8601
from simplebench.validators import validate_bool

from . import validate
from ._error_tags import _CaseErrorTag
from .function_runner import FunctionRunner
from .results import Results
from .state import CaseState

if TYPE_CHECKING:
    from simplebench.session import Session


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
                name='__qualname__',
            )

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
    """
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

    The Case class is designed to be immutable after creation and running. Once a Case instance
    is created, its properties cannot be directly changed. This immutability ensures that
    benchmark cases remain consistent throughout their lifecycle. The only operation
    that can change its state after creation is calling the :method:`run` method to
    run the benchmark. The benchmark will be run and the results of the run can
    be read from the :property:`report` property.

    .. code-block:: python
      :caption: Minimal Example

        from simplebench import Case, BenchmarkRunner, Results, main


        def my_benchmark_action(bench: BenchmarkRunner, variation_marks: VariationMarks) -> Results:
            # Perform benchmark action here
            def benchmark_operation():
                sum(range(1000))  # Example operation to benchmark

            return bench.run(benchmark_operation)


        if __name__ == '__main__':
            cases_list: list[Case] = [Case(action=my_benchmark_action)]
            main(cases_list)

    """

    __slots__ = (
        '_group',
        '_title',
        '_description',
        '_action',
        '_iterations',
        '_warmup_iterations',
        '_min_time',
        '_max_time',
        '_variation_cols',
        '_kwargs_variations',
        '_variation_marks',
        '_runners',
        '_callback',
        '_results',
        '_options',
        '_rounds',
        '_benchmark_id',
        '_vcs_info',
        '_timeout',
        '_timer',
        '_cpu_timer',
        '_report_cache',
        '_report_cache_raw_data',
        '_timestamp',
        '_epoch_timestamp',
        '_node',
        '_state',
    )

    @format_docstring(
        DEFAULT_TIMEOUT_GRACE_PERIOD=defaults.DEFAULT_TIMEOUT_GRACE_PERIOD,
        DEFAULT_TIMER=defaults.DEFAULT_TIMER.__name__,
        DEFAULT_CPU_TIMER=defaults.DEFAULT_CPU_TIMER.__name__,
    )
    def __init__(
        self,
        *,
        benchmark_id: str | None = None,
        vcs_info: vcs.VCSInfo | None = None,
        action_wrapper: FunctionRunner,
        group: str = 'default',
        title: str | None = None,
        description: str | None = None,
        iterations: int = defaults.DEFAULT_ITERATIONS,
        warmup_iterations: int = defaults.DEFAULT_WARMUP_ITERATIONS,
        rounds: int | None = None,
        timer: Callable[[], int] | None = None,
        cpu_timer: Callable[[], int] | None = None,
        min_time: float = defaults.DEFAULT_MIN_TIME,
        max_time: float = defaults.DEFAULT_MAX_TIME,
        timeout: float | int | None = None,
        variation_cols: Mapping[str, str] | None = None,
        kwargs_variations: Mapping[str, ElementCollection[Any]] | None = None,
        runners: ElementCollection[type[BenchmarkRunner]] | None = None,
        callback: ReporterCallback | None = None,
        options: ElementCollection[ReporterOptions] | None = None,
        node: str | None = '',
    ) -> None:
        """The only REQUIRED parameter is `action`.

        :param benchmark_id: (default = :obj:`None`) An optional unique identifier for the benchmark case.

            If None, a transient ID is assigned. This is meant to provide a stable identifier for the
            benchmark case across multiple runs for tracking purposes. If not provided,
            an attempt will be made to generate a stable ID based on the the action function
            name, signature, and group. If that is not possible, a transient ID based
            on the instance's id() will be used. If a transient ID is used, it will differ
            between runs and cannot be used to correlate results across multiple runs.

            Benchmark ids must be unique within a benchmarking session and stable across runs
            or they cannot be used for tracking benchmark results over time.
        :type benchmark_id: str | :obj:`None`

        :param vcs_info: (default = :obj:`None`) An optional vcs.VCSInfo
            instance representing the state of the VCS repository.

            If not provided, the vcs.VCSInfo will be automatically retrieved from the current
            context of the caller if the code is part of a VCS repository.
        :type vcs_info: :class:`vcs.VCSInfo` | :obj:`None`

        :param action: The function to perform the benchmark.

            This function must accept a `_bench` instance of type :class:`BenchmarkRunner` and
            arbitrary keyword arguments (``**kwargs``). See the :class:`FunctionRunner`
            protocol for the exact signature required. It must return a :class:`Results` object.
        :type action: :class:`FunctionRunner`

        :param group: (default = 'default')The benchmark reporting group to which the benchmark case belongs.

            Benchmarks with the same group can be selected for execution without running
            other benchmarks. If not specified, the default group 'default' is used.
        :type group: Optional[str]

        :param title: (default = :obj:`None`) The title of the benchmark case.
        :type title: str | :obj:`None`

            If None, the name of the action function will be used. Cannot be blank.

        :param description: (default = :obj:`None`) A brief description of the benchmark case.

            If None, the docstring of the action function will be used, or
            '(no description)' if no docstring is available. Cannot be blank.
        :type description: str | :obj:`None`

        :param iterations: (default = :data:`~simplebench.defaults.DEFAULT_ITERATIONS`) The
            minimum number of iterations to run for the benchmark.
        :type iterations: int

        :param warmup_iterations: (default = :data:`~simplebench.defaults.DEFAULT_WARMUP_ITERATIONS`) The
            number of warmup iterations to run before the benchmark.
        :type warmup_iterations: int

        :param rounds: (default = :obj:`None`) The number of rounds to run for the benchmark.

            Rounds are multiple runs of calls to the action within an iteration to mitigate timer
            quantization, loop overhead, and other measurement effects for very fast actions. Setup and teardown
            functions are called only once per iteration (all rounds in the same iteration share the same
            setup/teardown context).

            If :obj:`None`, rounds will be auto-calibrated based on the precision and overhead of the timer function
            and the expected execution time of the action. If the action is very fast (e.g., under
            10 microseconds), rounds will be set to a higher value to improve measurement accuracy
            with the goal of reducing timer quantization errors. If the action is slower, rounds
            will be set lower values.

            If specified, it must be a positive integer.
        :type rounds: int | :obj:`None`

        :param timer: (default = :obj:`None`) The timer function to use for the benchmark.

            If :obj:`None`, when tests are run, the timer from the :class:`Session` instance (if set) or
            from :data:`~simplebench.defaults.DEFAULT_TIMER` ({DEFAULT_TIMER})
            is used by benchmark runners that require a timer.

            The timer function should be a callable that returns an int representing the
            current wallclock time.
        :type timer: Callable[[], int] | :obj:`None`

        :param cpu_timer: (default = :obj:`None`)
            The CPU timer function to use for the benchmark.

            If :obj:`None`, where tests are run, the cpu_timer from the :class:`Session` instance (if set) or
            from :data:`~simplebench.defaults.DEFAULT_CPU_TIMER` ({DEFAULT_CPU_TIMER})
            is used by benchmark runners that require a CPU timer.

            The CPU timer function should be a callable that returns an int representing the
            current CPU time.
        :type cpu_timer: Callable[[], int] | :obj:`None`

        :param min_time: (default = :data:`defaults.DEFAULT_MIN_TIME`) ({DEFAULT_MIN_TIME}) The minimum time
            for the benchmark to run in seconds. Its reference depends on the timer used,
            but by default it is wall-clock time.
        :type min_time: float

        :param max_time: (default = :data:`defaults.DEFAULT_MAX_TIME`) ({DEFAULT_MAX_TIME}) The maximum time
            for the benchmark run in seconds. Its reference depends on the timer used,
            but by default it is wall-clock time.
        :type max_time: float

        :param timeout: (default = :obj:`None`) How long to wait before timing
            out a benchmark run (in seconds). It is measured as wall-clock time.

            If :obj:`None`, it waits the full duration of :attr:`~simplebench.case.Case.max_time` plus the default
            timeout grace period ({DEFAULT_TIMEOUT_GRACE_PERIOD} seconds). It must be a positive
            float or int that is greater than :attr:`~simplebench.case.Case.max_time` if provided.
            This is a safety mechanism to prevent runaway benchmarks.

            If the timeout is reached during a run, a :class:`~simplebench.exceptions.SimpleBenchTimeoutError``
            will be raised, and the benchmark case's state changed to TIMED_OUT.
        :type timeout: float | int | :obj:`None`

        :param variation_cols: (default = :obj:`None`) Keyword arguments to be used for column labels
            to denote kwarg variations.

            Each key is a keyword argument name, and the value is the column label to use for that
            argument. Only keywords that are also in :attr:`~simplebench.case.Case.kwargs_variations`
            can be used here. These fields will be added to the output of reporters that support
            them as columns of data with the specified labels.

            If not provided or passed as :obj:`None`, an empty dict is used internally.
        :type variation_cols: Mapping[str, str] | :obj:`None`

        :param Optional[dict[str, list[Any]]] kwargs_variations: (default = {}) A map
            of keyword argument names to a list of possible values for that argument.

            When tests are run, the benchmark will be executed for each combination
            of the specified keyword argument variations. The action function will be
            called with a `bench` parameter that is an instance of the runner and the
            keyword arguments for the current variation.

            kwargs_variation values can be of any type, including types that are not easily serializable.
            To handle this situation, the `Mark` class can be used to create standardized marks that
            can be used to represent these variations in results and reports.

            .. code-block:: python
                :caption: Using Marks for Variation Representation

                from simplebench.case import Case, Mark, Results
                from simplebench.benchmark_runner import SimpleRunner


                def my_benchmark_action(bench: SimpleRunner, mode: str) -> Results:
                    # Benchmark action implementation
                    pass


                case = Case(
                    action=my_benchmark_action, kwargs_variations={'mode': [Mark('ModeA', 1), Mark('ModeB', 2)]}
                )

        :param Optional[Sequence[type[SimpleRunner]]] runners: A list of runners for the benchmark.

            Any runner classes must be a subclass of BenchmarkRunner and must have a method
            named `run` that accepts the same parameters as BenchmarkRunner.run and returns a Results object.
            The action function will be called with a `bench` parameter that is an instance of the
            custom runner.

            It may also accept additional parameters to the run method as needed. If additional
            parameters are needed for the custom runner, they will need to be passed to the run
            method as keyword arguments.

            No support is provided for passing additional parameters to a custom runner from the @benchmark
            decorator.

            If not specified, the default :class:`~simplebench.benchmark_runner.SimpleRunner`
            will be used. If multiple runners are specified, the benchmark will be run for
            each specified runner, and the results will be combined.

        :param Optional[ReporterCallback] callback: A callback function for additional processing of the report.

            The function should must four arguments: the Case instance, the Metric,
            the Format, and the generated report data.

            - case (Case): The `Case` instance processed for the report.
            - metric (Metric): The `Metric` of the report.
            - output_format (Format): The `Format` of the report.
            - output (Any): The generated report data. Note that the actual type of this data will
                depend on the Format specified for the report and the type generated by the
                reporter for that Format

            Omit if no callback is needed by a reporter.
        :param Optional[Iterable[ReporterOptions]] options: A list of additional options for the benchmark case.

            Each option is an instance of ReporterOption or a subclass of ReporterOption.
            Reporter options can be used to customize the output of the benchmark reports for
            specific reporters. Reporters are responsible for extracting applicable ReporterOptions
            from the list of options themselves.
            If None, an empty list is used.
        :param Optional[str] node: (default = '') An optional identifier for the node where the benchmark is run.
            This can be used in distributed benchmarking scenarios to identify
            the source of the benchmark data. If not specified, the actual node name
            from the environment will be used. Default is '' for privacy and
            security reasons.
        :raises SimpleBenchTypeError: If any parameter is of incorrect type.
        :raises SimpleBenchValueError: If any parameter has an invalid value.
        """
        # kwargs_variations processed first so it can be used for cross-validation of action signature
        self._kwargs_variations: KWArgsVariations = validate.kwargs_variations(kwargs_variations)
        self._group: str = validate.group(group)
        self._action: FunctionRunner = validate.action_signature(action_wrapper)
        self._title: str = validate.title(self._action, title)
        self._description: str = validate.description(self._action, description)
        self._iterations: int = validate.iterations(iterations)
        self._warmup_iterations: int = validate.warmup_iterations(warmup_iterations)
        self._rounds: int | None = validate.rounds(rounds)
        self._timer: Callable[[], int] | None = validate.timer(timer, 'timer')
        self._cpu_timer: Callable[[], int] | None = validate.timer(cpu_timer, 'cpu_timer')
        self._min_time: float = validate.min_time(min_time)
        self._max_time: float = validate.max_time(max_time)
        validate.time_range(self.min_time, self.max_time)
        self._timeout: float = validate.timeout(timeout, self.max_time)
        self._benchmark_id = validate.benchmark_id(benchmark_id or generate_benchmark_id(self, action_wrapper))
        self._variation_cols: VariationCols = validate.variation_cols(
            variation_cols, self.kwargs_variations)
        self._runners: tuple[type[BenchmarkRunner], ...] = validate.runners(runners)
        self._callback: ReporterCallback | None = validate_reporter_callback(callback, allow_none=True)
        self._options: tuple[ReporterOptions, ...] = validate.options(options)
        self._vcs_info: vcs.VCSInfo | None = validate.vcs_info(vcs_info or vcs.get_vcs_info())
        self._node: str | None = validate.node(node)

        # internal state
        self._report_cache: reports.Report | None = None
        self._report_cache_raw_data: reports.Report | None = None
        self._timestamp: str = ''
        self._epoch_timestamp: float = 0.0
        self._state: CaseState = CaseState.PENDING
        self._results: tuple[Results, ...] = ()

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
        """A brief description of the benchmark case.

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
                    setup=setup_function,
                    teardown=teardown_function,
                    action=action_function,
                    **kwargs,
                )
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

        If :obj:`None`, the default timer from the Session() (if set) or from
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
    def variation_cols(self) -> VariationCols:
        """Keyword arguments to be used for columns to denote kwarg variations.

        Each key is a keyword argument name, and the value is the column label to use for that argument.
        Only keywords that are also in `kwargs_variations` can be used here. These fields will be
        added to the output of reporters that support them as columns of data with the specified labels.

        Note that all keys in variation_cols must be present in kwargs_variations and
        updating it may require changes to both variation_cols and kwargs_variations_cols.

        Updating variation_cols does not automatically update kwargs_variations, and vice versa.

        :return: A dictionary mapping keyword argument names to column labels.
        :rtype: VariationCols
        """
        return self._variation_cols

    @property
    def kwargs_variations(self) -> KWArgsVariations:
        """Variations of keyword arguments for the benchmark.

        Each key is a keyword argument name, and the value is the column label to use for that argument.
        Only keywords that are also in `kwargs_variations` can be used here. These fields will be
        added to the output of reporters that support them as columns of data with the specified labels.

        When tests are run, the benchmark will be executed for each combination of the specified
        keyword argument variations. For example, if `kwargs_variations` is

        .. code-block:: python3
          :caption: `kwargs_variations` argument example

            ...
            kwargs_variations = ({'size': [10, 100], 'mode': ['fast', 'accurate']},)
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

        :return: A dictionary mapping keyword argument names to lists of possible values.
        :rtype: KWArgsVariations
        """
        return self._kwargs_variations

    @property
    def runners(self) -> tuple[type[BenchmarkRunner], ...]:
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
    def results(self) -> tuple[Results, ...]:
        """The benchmark list of Results for the case.

        This is a read-only attribute. To add results, use the `run` method.

        :return list[Results]: A list of Results objects. One for each variation run in the benchmark case.
        :raises SimpleBenchValueError: If the benchmark case has not been run yet.
        """
        if self.state is not CaseState.COMPLETED:
            raise SimpleBenchRuntimeError(
                f'The results are not available because the benchmark case has not run to completion: {self.state}',
                tag=_CaseErrorTag.HAVE_NOT_RUN_CASE_YET
            )
        return self._results

    @property
    def options(self) -> tuple[ReporterOptions, ...]:
        """A list of additional options for the benchmark case."""
        # shallow copy to prevent external modification of internal list
        return self._options

    @property
    def expanded_kwargs_variations(self) -> tuple[VariationMarks, ...]:
        """All combinations of keyword arguments from the specified kwargs_variations.

        A mapping of keyword argument names to their variations.

        Each key is a keyword argument name, and the value is a list of possible values.

        When tests are run, the benchmark will be executed for each combination of the specified
        keyword argument variations. For example, if `kwargs_variations` is

        .. code-block:: python

            kwargs_variations = ({
                'size': [Mark(label=10, value=10), Mark(label=100, value=100)],
                'mode': [Mark(label='Fast', value='fast'), Mark(label='Accurate', value='accurate')]
            })

        The benchmark will be run 4 times with the following combinations of keyword arguments:

        .. code-block:: python

            {size=Mark(label=10, value=10), mode=Mark(label='Fast', value='fast')}
            {size=Mark(label=10, value=10), mode=Mark(label='Accurate', value='accurate')}
            {size=Mark(label=100, value=100), mode=Mark(label='Fast', value='fast')}
            {size=Mark(label=100, value=100), mode=Mark(label='Accurate', value='accurate')}

        The action function will be called with these keyword arguments accordingly and must
        accept them.

        :return: A tuple of :class:`VariationMarks` dictionaries, each representing a
            unique combination of keyword arguments.
        :rtype: tuple[VariationMarks, ...]
        """
        keys = sorted(self.kwargs_variations.keys())
        values_list = [self.kwargs_variations[key] for key in keys]
        combinations: list[VariationMarks] = []
        for v in itertools.product(*values_list):
            kwargs = VariationMarks(
                { key: value for key, value in zip(keys, v, strict=True) })
            combinations.append(kwargs)
        return tuple(combinations)

    @property
    def timestamp(self) -> str:
        """The ISO 8601 timestamp when the benchmark case was run.

        This is a read-only attribute that is set when the `run` method is called.
        If the benchmark case has not been run yet, it will be an empty string.

        :return: The ISO 8601 timestamp as a string.
        """
        if self.state is not CaseState.COMPLETED:
            raise SimpleBenchRuntimeError(
                f'The timestap is not available because the benchmark case has not run to completion: {self.state}',
                tag=_CaseErrorTag.HAVE_NOT_RUN_CASE_YET
            )
        return self._timestamp

    @property
    def epoch_timestamp(self) -> float:
        """The epoch timestamp when the benchmark case was run.

        This is a read-only attribute that is set when the `run` method is called.
        If the benchmark case has not been run yet, it will be 0.

        :return: The epoch timestamp.
        :rtype: float
        """
        return self._epoch_timestamp

    @property
    def node(self) -> str | None:
        """The identifier for the node where the benchmark was run.

        This can be used in distributed benchmarking scenarios to identify
        the source of the benchmark data.

        :return: The node identifier as a string, or None if not set.
        :rtype: str | None
        """
        return self._node

    def run(self, session: 'Session | None' = None) -> None:
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
        self._state = CaseState.RUNNING
        self._set_timestamp(session)

        all_variations = self.expanded_kwargs_variations
        progress_tracker = ProgressTracker(
            session=session,
            task_name='Case:run',
            progress_max=len(all_variations),
            description=f'Running case {self.title}',
            color=Color.CYAN,
        )
        progress_tracker.reset()

        # BenchmarkRunner prioritization is Case().runners -> Session().default_runners -> defaults.DEFAULT_RUNNERS
        runners_list: tuple[type[BenchmarkRunner], ...] = self.runners
        if not runners_list and session and session.default_runners:
            runners_list = session.default_runners
        if not runners_list:
            runners_list = defaults.default_runners()

        variation_marks: VariationMarks
        # We loop over variations in the outside loop so that progress is reported
        # grouped by each variation run, which is more user-friendly than reporting progress
        # grouped by each runner.
        pending_results: list[Results] = []
        for variations_counter, variation_marks in enumerate(all_variations):
            for runner in runners_list:
                bench: BenchmarkRunner = runner(case=self, session=session, variation_marks=variation_marks)

                try:
                    results: Results = self.action(bench, variation_marks)
                except SimpleBenchTimeoutError as e:
                    self._state = CaseState.TIMED_OUT
                    raise SimpleBenchTimeoutError(
                        f'Timeout occurred running benchmark action {str(self.action)} for case '
                        f'"{self.title}" with kwargs {variation_marks}: {e}',
                        tag=_CaseErrorTag.BENCHMARK_ACTION_TIMEOUT_OCCURRED,
                    ) from e
                except Exception as e:
                    self._state = CaseState.FAILED
                    raise SimpleBenchBenchmarkError(
                        f'Error occurred running benchmark action {self.action!r} for case '
                        f'"{self.title}" with variation {variation_marks!r}: {e}, {type(e)}',
                        tag=_CaseErrorTag.BENCHMARK_ACTION_RAISED_EXCEPTION,
                    ) from e
                pending_results.append(results)
            progress_tracker.update(
                description=(f'Running case {self.title} ({variations_counter + 1}/{len(all_variations)})'),
                completed=variations_counter + 1,
                refresh=True,
            )
        progress_tracker.stop()
        self._results = tuple(pending_results)
        self._state = CaseState.COMPLETED

    def _set_timestamp(self, session: 'Session | None') -> None:
        """Set the timestamp for the benchmark case.

        This method sets the timestamp for the benchmark case to the current time.
        If a session is provided, it uses the session's timestamp. Otherwise, it
        uses the current UTC time.

        :param session: The session in which the case is being run.
        """
        if session is not None:
            self._epoch_timestamp = session.epoch_timestamp
            self._timestamp = session.timestamp
        else:
            self._epoch_timestamp = datetime.now().timestamp()
            self._timestamp = timestamp_to_iso8601(self.epoch_timestamp)

    @property
    def state(self) -> CaseState:
        """The current state of the benchmark case.

        It returns the state of the benchmark case as a CaseState enum value.

        - :data:`CaseState.PENDING`: The benchmark case has not been run yet.
        - :data:`CaseState.RUNNING`: The benchmark case is currently being run.
        - :data:`CaseState.COMPLETED`: The benchmark case has been run successfully.
        - :data:`CaseState.FAILED`: The benchmark case encountered an error during execution.
        - :data:`CaseState.TIMED_OUT`: The benchmark case timed out during execution.

        :return: The CaseState enum value representing the current state of the benchmark case.
        :rtype: :class:`CaseState`
        """
        return self._state

    def report(self, include_raw_data: bool = False) -> reports.Report:
        """Returns the benchmark case and results as a Report object.

        The Report format is a JSON serializable object that includes all the necessary
        information about the benchmark case and its results. This format can be used to
        exchange data between different systems or to store the data in a structured way.

        It conforms to the JSON Schema defined at
        https://raw.githubusercontent.com/JerilynFranz/python-simplebench/main/schemas/v1/report-info.json

        :param include_raw_data: Whether to include raw data. Defaults to False.
        :return: A JSON serializable representation of the benchmark case and results.
        """
        if self.state is not CaseState.COMPLETED:
            raise SimpleBenchRuntimeError(
                f'The report is not available because the benchmark case has not run to completion: {self.state}',
                tag=_CaseErrorTag.HAVE_NOT_RUN_CASE_YET
            )
        validate_bool(include_raw_data, 'include_raw_data', _CaseErrorTag.INVALID_REPORT_INCLUDE_RAW_DATA_NOT_BOOL)

        if include_raw_data:
            return self._report_with_raw_data()
        else:
            return self._report()

    def _report(self) -> reports.Report:
        """Generate or retrieve the cached report without raw data.

        :return: The Report object without raw data.
        """
        if self._report_cache is not None:
            return self._report_cache

        # TODO: Implement report generation logic here
        return report
