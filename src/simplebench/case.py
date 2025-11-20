"""Benchmark case declaration and execution."""
from __future__ import annotations

import inspect
import itertools
from copy import copy
from typing import TYPE_CHECKING, Any, Iterable, Optional

from .defaults import DEFAULT_ITERATIONS, DEFAULT_MAX_TIME, DEFAULT_MIN_TIME, DEFAULT_ROUNDS, DEFAULT_WARMUP_ITERATIONS
from .enums import Color, Section
from .exceptions import SimpleBenchRuntimeError, SimpleBenchTypeError, SimpleBenchValueError, _CaseErrorTag
from .protocols import ActionRunner
from .reporters.protocols import ReporterCallback
from .reporters.reporter.options import ReporterOptions
from .reporters.validators.validators import validate_reporter_callback
from .results import Results
from .runners import SimpleRunner
from .tasks import ProgressTracker
from .validators import (
    validate_non_blank_string,
    validate_non_negative_int,
    validate_positive_float,
    validate_positive_int,
)

if TYPE_CHECKING:
    from .session import Session


class Case:
    '''Declaration of a benchmark case.

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

    If your action is not extremely fast (~ 10 nanoseconds or faster), it is recommended to leave
    `rounds` at its default value of 1. If you do use it, you may want to run dual benchmarks
    with `rounds=1` and `rounds>1` to see how much the reported variability and other metrics change.

    The Case class is designed to be immutable after creation. Once a Case instance
    is created, its properties cannot be directly changed. This immutability ensures that
    benchmark cases remain consistent throughout their lifecycle.

    The results of the benchmark runs are stored in the `results` property, which is a list
    of Results objects. Each Results object corresponds to a specific combination of
    keyword argument variations.

    .. code-block:: python3
      :caption: Minimal Example

        from simplebench import (
            Case, SimpleRunner, Results, main)


        def my_benchmark_action(bench: SimpleRunner,
                                **kwargs) -> Results:
            # Perform benchmark action here
            def benchmark_operation():
                sum(range(1000))  # Example operation to benchmark

            return bench.run(benchmark_operation)


        if __name__ == '__main__':
            cases_list: list[Case] = [
                Case(action=my_benchmark_action)
            ]
            main(cases_list)
    '''
    __slots__ = ('_group', '_title', '_description', '_action',
                 '_iterations', '_warmup_iterations', '_min_time', '_max_time',
                 '_variation_cols', '_kwargs_variations', '_runner',
                 '_callback', '_results', '_options', '_rounds')

    def __init__(self, *,
                 action: ActionRunner,
                 group: str = 'default',
                 title: Optional[str] = None,
                 description: Optional[str] = None,
                 iterations: int = DEFAULT_ITERATIONS,
                 warmup_iterations: int = DEFAULT_WARMUP_ITERATIONS,
                 rounds: int = DEFAULT_ROUNDS,
                 min_time: float = DEFAULT_MIN_TIME,
                 max_time: float = DEFAULT_MAX_TIME,
                 variation_cols: Optional[dict[str, str]] = None,
                 kwargs_variations: Optional[dict[str, list[Any]]] = None,
                 runner: Optional[type[SimpleRunner]] = None,
                 callback: Optional[ReporterCallback] = None,
                 options: Optional[Iterable[ReporterOptions]] = None) -> None:
        """Constructor for Case. This defines a benchmark case.

        The only REQUIRED parameter is `action`.

        :param action: The function to perform the benchmark. This function must
            accept a `bench` instance of type SimpleRunner and arbitrary keyword arguments ('**kwargs').
            See the `ActionRunner` protocol for the exact signature required.
            It must return a `Results` object.
        :type action: ActionRunner
        :param group: The benchmark reporting group to which the benchmark case belongs.
        :type group: str
        :param title: The title of the benchmark case. If None, the name of the action
            function will be used. Cannot be blank.
        :type title: Optional[str]
        :param description: A brief description of the benchmark case. If None,
            the docstring of the action function will be used, or '(no description)' if no docstring
            is available. Cannot be blank.
        :type description: Optional[str]
        :param iterations: The minimum number of iterations to run for
            the benchmark.
        :type iterations: int
        :param warmup_iterations: The number of warmup iterations
            to run before the benchmark.
        :type warmup_iterations: int
        :param rounds: The number of rounds to run for the benchmark.
            Rounds are multiple runs of calls to the action within an iteration to mitigate timer
            quantization, loop overhead, and other measurement effects for very fast actions. Setup and teardown
            functions are called only once per iteration (all rounds in the same iteration share the same
            setup/teardown context).
        :type rounds: int
        :param min_time: The minimum time for the benchmark in seconds.
        :type min_time: float | int
        :param max_time: The maximum time for the benchmark in seconds.
        :type max_time: float | int
        :param variation_cols: kwargs to be used for cols to denote kwarg
            variations. Each key is a keyword argument name, and the value is the column label to use for that
            argument. Only keywords that are also in `kwargs_variations` can be used here. These fields will be
            added to the output of reporters that support them as columns of data with the specified labels.
            If None, an empty dict is used.
        :type variation_cols: Optional[dict[str, str]]
        :param kwargs_variations: A mapping of keyword argument key names to
            a list of possible values for that argument. Default is {}. When tests are run, the benchmark
            will be executed for each combination of the specified keyword argument variations. The action
            function will be called with a `bench` parameter that is an instance of the runner and the
            keyword arguments for the current variation.
            If None, an empty dict is used.
        :type kwargs_variations: Optional[dict[str, list[Any]]]
        :param runner: A custom runner class for the benchmark.
            Any custom runner classes must be a subclass of SimpleRunner and must have a method
            named `run` that accepts the same parameters as SimpleRunner.run and returns a Results object.
            The action function will be called with a `bench` parameter that is an instance of the
            custom runner.
            It may also accept additional parameters to the run method as needed. If additional
            parameters are needed for the custom runner, they will need to be passed to the run
            method as keyword arguments.
            No support is provided for passing additional parameters to a custom runner from the @benchmark
            decorator.
        :type runner: type[SimpleRunner]
        :param callback:
            A callback function for additional processing of the report. The function should accept
            four arguments: the Case instance, the Section, the Format, and the generated report data.
            The callback function will be called with the following arguments:
                - case (Case): The `Case` instance processed for the report.
                - section (Section): The `Section` of the report.
                - output_format (Format): The `Format` of the report.
                - output (Any): The generated report data. Note that the actual type of this data will
                  depend on the Format specified for the report and the type generated by the
                  reporter for that Format
            Omit if no callback is needed by a reporter.
        :type callback: Optional[ReporterCallback]
        :param options: A list of additional options for the benchmark case.
            Each option is an instance of ReporterOption or a subclass of ReporterOption.
            Reporter options can be used to customize the output of the benchmark reports for
            specific reporters. Reporters are responsible for extracting applicable ReporterOptions
            from the list of options themselves.
            If None, an empty list is used.
        :type options: Optional[list[ReporterOption]]
        """
        self._group = validate_non_blank_string(
                        group, "group",
                        _CaseErrorTag.INVALID_GROUP_TYPE,
                        _CaseErrorTag.INVALID_GROUP_VALUE)
        self._action = Case.validate_action_signature(action)
        title = action.__name__ if title is None else title  # type: ignore[attr-defined]
        self._title = validate_non_blank_string(
                        title, "title",
                        _CaseErrorTag.INVALID_TITLE_TYPE,
                        _CaseErrorTag.INVALID_TITLE_VALUE)
        if description is None:
            description = action.__doc__ if action.__doc__ else '(no description)'
        self._description = validate_non_blank_string(
                        description, "description",
                        _CaseErrorTag.INVALID_DESCRIPTION_TYPE,
                        _CaseErrorTag.INVALID_DESCRIPTION_VALUE)
        self._iterations = validate_positive_int(
                        iterations, "iterations",
                        _CaseErrorTag.INVALID_ITERATIONS_TYPE,
                        _CaseErrorTag.INVALID_ITERATIONS_VALUE)
        self._warmup_iterations = validate_non_negative_int(
                        warmup_iterations, "warmup_iterations",
                        _CaseErrorTag.INVALID_WARMUP_ITERATIONS_TYPE,
                        _CaseErrorTag.INVALID_WARMUP_ITERATIONS_VALUE)
        self._rounds = validate_positive_int(
                        rounds, "rounds",
                        _CaseErrorTag.INVALID_ROUNDS_TYPE,
                        _CaseErrorTag.INVALID_ROUNDS_VALUE)
        self._min_time = validate_positive_float(
                        min_time, "min_time",
                        _CaseErrorTag.INVALID_MIN_TIME_TYPE,
                        _CaseErrorTag.INVALID_MIN_TIME_VALUE)
        self._max_time = validate_positive_float(
                        max_time, "max_time",
                        _CaseErrorTag.INVALID_MAX_TIME_TYPE,
                        _CaseErrorTag.INVALID_MAX_TIME_VALUE)
        self._kwargs_variations = Case.validate_kwargs_variations(kwargs_variations)
        self._variation_cols = Case.validate_variation_cols(variation_cols, self._kwargs_variations)
        self._runner = Case.validate_runner(runner)
        self._callback = validate_reporter_callback(callback, allow_none=True)
        self._options = Case.validate_options(options)
        self._results: list[Results] = []  # No validation needed here
        self.validate_time_range(self._min_time, self._max_time)

    @staticmethod
    def validate_time_range(min_time: float, max_time: float) -> None:
        """Validate that min_time < max_time for the case.

        :param min_time: The minimum time.
        :type min_time: float
        :param max_time: The maximum time.
        :type max_time: float
        :raises SimpleBenchValueError: The min_time is greater than max_time.
        """
        if min_time > max_time:
            raise SimpleBenchValueError(
                f'Invalid time range: min_time {min_time} > max_time {max_time}.',
                tag=_CaseErrorTag.INVALID_TIME_RANGE)

    @staticmethod
    def validate_action_signature(action: ActionRunner) -> ActionRunner:
        """Validate that action has correct signature.

        An action function must accept the following two parameters:
            - bench: SimpleRunner
            - **kwargs: Arbitrary keyword arguments

        This is equivalent to the `ActionRunner` protocol.

        :param action: The action function to validate.
        :type action: ActionRunner
        :return: The validated action function.
        :rtype: ActionRunner
        :raises SimpleBenchTypeError: If the action is not callable or has an invalid signature.
        """
        if not callable(action):
            raise SimpleBenchTypeError(
                f'Invalid action: {action}. Must be a callable.',
                tag=_CaseErrorTag.INVALID_ACTION_NOT_CALLABLE
                )
        action_signature = inspect.signature(action)
        if 'bench' not in action_signature.parameters:
            raise SimpleBenchTypeError(
                f'Invalid action: {action}. Must accept a "bench" parameter.',
                tag=_CaseErrorTag.INVALID_ACTION_MISSING_BENCH_PARAMETER
                )
        kwargs_param = action_signature.parameters.get('kwargs')
        if kwargs_param is None or kwargs_param.kind not in (inspect.Parameter.VAR_KEYWORD,):
            raise SimpleBenchTypeError(
                f'Invalid action: {action}. Must accept "**kwargs" parameter.',
                tag=_CaseErrorTag.INVALID_ACTION_MISSING_KWARGS_PARAMETER
                )
        if len(action_signature.parameters) != 2:
            raise SimpleBenchValueError(
                f'Invalid action: {action}. Must accept exactly 2 parameters: bench and **kwargs.',
                tag=_CaseErrorTag.INVALID_ACTION_PARAMETER_COUNT
            )
        return action

    @staticmethod
    def validate_kwargs_variations(value: dict[str, list[Any]] | None) -> dict[str, list[Any]]:
        """Validate the kwargs_variations dictionary.

        Validates that the kwargs_variations is a dictionary where each key is a string
        that is a valid Python identifier, and each value is a non-empty list.

        A shallow copy of the validated dictionary and the lists is performed before returning to prevent
        external modification.

        :param value: The kwargs_variations dictionary to validate.
            Defaults to {} if None.
        :type value: dict[str, list[Any]] | None
        :return: A shallow copy of the validated kwargs_variations dictionary or {} if not provided.
            The keys are strings that are valid Python identifiers, and the values are non-empty lists.
            The lists may contain any type of values.
        :rtype: dict[str, list[Any]]
        :raises SimpleBenchTypeError: If the kwargs_variations is not a dictionary or if any key is not a string
            that is a valid Python identifier.
        :raises SimpleBenchValueError: If any value is not a list or is an empty list.
        """
        if value is None:
            return {}
        if not isinstance(value, dict):
            raise SimpleBenchTypeError(
                f'Invalid kwargs_variations: {value}. Must be a dictionary.',
                tag=_CaseErrorTag.INVALID_KWARGS_VARIATIONS_NOT_DICT
                )
        validated_dict = {}
        for key, kw_value in value.items():
            if not isinstance(key, str):
                raise SimpleBenchTypeError(
                    f'Invalid kwargs_variations entry key: {key}. Keys must be of type str.',
                    tag=_CaseErrorTag.INVALID_KWARGS_VARIATIONS_ENTRY_KEY_TYPE
                    )
            if not key.isidentifier():
                raise SimpleBenchValueError(
                    f'Invalid kwargs_variations entry key: {key}. Keys must be valid Python identifiers.',
                    tag=_CaseErrorTag.INVALID_KWARGS_VARIATIONS_ENTRY_KEY_NOT_IDENTIFIER
                    )
            if not isinstance(kw_value, list):
                raise SimpleBenchTypeError(
                    f'Invalid kwargs_variations entry value for entry "{key}": {kw_value}. Values must be in a list.',
                    tag=_CaseErrorTag.INVALID_KWARGS_VARIATIONS_ENTRY_VALUE_NOT_LIST
                    )
            if not kw_value:
                raise SimpleBenchValueError(
                    (f'Invalid kwargs_variations entry value for entry "{key}": {kw_value}. '
                     'Values cannot be empty lists.'),
                    tag=_CaseErrorTag.INVALID_KWARGS_VARIATIONS_ENTRY_VALUE_EMPTY_LIST
                    )
            validated_dict[key] = copy(kw_value)
        return validated_dict

    @staticmethod
    def validate_variation_cols(variation_cols: dict[str, str] | None,
                                kwargs_variations: dict[str, list[Any]]) -> dict[str, str]:
        """Validate the variation_cols dictionary.

        :param variation_cols: The variation_cols dictionary to validate or None.
        :type variation_cols: dict[str, str] | None
        :param kwargs_variations: The kwargs_variations dictionary to validate against.
        :type kwargs_variations: dict[str, list[Any]]
        :return: A shallow copy of the validated variation_cols dictionary or {} if not provided.
            Each key is a keyword argument name from `kwargs_variations`, and each value is a
            non-blank string to be used as the column label for that argument in reports.
        :rtype: dict[str, str]
        :raises SimpleBenchTypeError: If the variation_cols is not a dictionary or if any key or
            value is not a string.
        :raises SimpleBenchValueError: If any key is not found in `kwargs_variations` or if any
            value is a blank string.
        """
        if variation_cols is None:
            return {}
        if not isinstance(variation_cols, dict):
            raise SimpleBenchTypeError(
                f'Invalid variation_cols: {variation_cols}. Must be a dictionary.',
                tag=_CaseErrorTag.INVALID_VARIATION_COLS_NOT_DICT
                )
        validated_dict: dict[str, str] = {}
        for key, vc_value in variation_cols.items():
            if key not in kwargs_variations:
                raise SimpleBenchValueError(
                    f'Invalid variation_cols entry key: {key}. Key not found in kwargs_variations.',
                    tag=_CaseErrorTag.INVALID_VARIATION_COLS_ENTRY_KEY_NOT_IN_KWARGS)
            if not isinstance(vc_value, str):
                raise SimpleBenchTypeError(
                    f'Invalid variation_cols entry value for entry "{key}": "{vc_value}". Values must be of type str.',
                    tag=_CaseErrorTag.INVALID_VARIATION_COLS_ENTRY_VALUE_NOT_STRING
                    )
            stripped_value = vc_value.strip()
            if stripped_value == '':
                raise SimpleBenchValueError(
                    f'Invalid variation_cols entry value: "{vc_value}". Values cannot be blank strings.',
                    tag=_CaseErrorTag.INVALID_VARIATION_COLS_ENTRY_VALUE_BLANK
                    )
            validated_dict[key] = stripped_value
        return validated_dict

    @staticmethod
    def validate_runner(value: type[SimpleRunner] | None) -> type[SimpleRunner] | None:
        """Validate the runner class.

        :param value: The runner class to validate.
        :type value: Optional[type[SimpleRunner]]
        :return: The validated runner class or None.
        :rtype: Optional[type[SimpleRunner]]
        :raises SimpleBenchTypeError: If the runner is not a subclass of SimpleRunner or None.
        """
        if value is None:
            return None
        if not (isinstance(value, type) and issubclass(value, SimpleRunner)):
            raise SimpleBenchTypeError(
                f'Invalid runner: {value}. Must be a subclass of SimpleRunner or None.',
                tag=_CaseErrorTag.INVALID_RUNNER_NOT_SIMPLE_RUNNER_SUBCLASS
                )
        return value

    @staticmethod
    def validate_options(value: Iterable[ReporterOptions] | None) -> list[ReporterOptions]:
        """Validate the options list.

        :param value: The options iterable to validate or None.
        :type value: Iterable[ReporterOption] | None
        :return: A shallow copy of the validated options as a list or an empty list if not provided.
        :rtype: list[ReporterOptions]
        :raises SimpleBenchTypeError: If options is not a list or if any entry is not a ReporterOption.
        """
        if value is None:
            return []
        if not isinstance(value, Iterable):
            raise SimpleBenchTypeError(
                f'Invalid options: {value}. Must be an iterable.',
                tag=_CaseErrorTag.INVALID_OPTIONS_NOT_ITERABLE)
        options_list: list[ReporterOptions] = list(value)
        for option in options_list:
            if not isinstance(option, ReporterOptions):
                raise SimpleBenchTypeError(
                    f'Invalid option: {option}. Must be of type ReporterOption or a sub-class.',
                    tag=_CaseErrorTag.INVALID_OPTIONS_ENTRY_NOT_REPORTER_OPTION
                    )
        return options_list

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
    def action(self) -> ActionRunner:
        """The function to perform the benchmark.

        The function must accept a `bench` parameter of type SimpleRunner and
        arbitrary keyword arguments ('**kwargs') and return a Results object.

        Example:

        .. code-block:: python3

            def my_benchmark_action(*, bench: SimpleRunner, **kwargs) -> Results:
                def setup_function(size: int) -> None:
                    # Setup code goes here
                    pass

                def teardown_function(size: int) -> None:
                    # Teardown code goes here
                    pass

                def action_function(size: int) -> None:
                    # The code to benchmark goes here
                    lst = list(range(size))

                # Perform the benchmark using the provided SimpleRunner instance
                results: Results = bench.run(
                    n=kwargs.get('size', 1),
                    setup=setup_function, teardown=teardown_function,
                    action=action_function, **kwargs)
                return results
        """
        return self._action

    @property
    def iterations(self) -> int:
        """The number of iterations to run for the benchmark."""
        return self._iterations

    @property
    def warmup_iterations(self) -> int:
        """The number of warmup iterations to run before the benchmark."""
        return self._warmup_iterations

    @property
    def rounds(self) -> int:
        """The number of rounds to run for the benchmark for each iteration.

        Rounds are multiple runs of the entire benchmark to get a better average for an iteration.
        Each iteration will run the specified number of rounds after setup and before teardown. (default: 1)"""
        return self._rounds

    @property
    def min_time(self) -> float:
        """The minimum time for the benchmark in seconds."""
        return self._min_time

    @property
    def max_time(self) -> float:
        """The maximum time for the benchmark in seconds."""
        return self._max_time

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
    def runner(self) -> type[SimpleRunner] | None:
        """A custom runner class for the benchmark.

        If None, the default SimpleRunner is used.  (default: None)

        A custom runner class must be a subclass of SimpleRunner and must have a method
        named `run` that accepts the same parameters as SimpleRunner.run and returns a Results object.
        The action function will be called with a `bench` parameter that is an instance of the
        custom runner.

        It may also accept additional parameters to the run method as needed. If additional
        parameters are required, they must be specified in the `action` function signature.
        """
        return self._runner

    @property
    def callback(self) -> ReporterCallback | None:
        """A callback function for additional processing of a report.

        A callback function to be called with the benchmark results in a reporter.
        This function should accept four arguments: the Case instance, the Section,
        the ReporterOption, and the output object. Leave as None if no callback is needed.
        (default: None)
        """
        return self._callback

    @property
    def results(self) -> list[Results]:
        """The benchmark list of Results for the case.

        This is a read-only attribute. To add results, use the `run` method.

        :return: A list of Results objects for each variation run of the benchmark case.
        :rtype: list[Results]
        """
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

    def run(self, session: Optional[Session] = None) -> None:
        """Run the benchmark tests.

        This method will execute the benchmark for each combination of
        keyword arguments and collect the results. After running the
        benchmarks, the results will be stored in the `self.results` attribute.

        If passed, the session's tasks will be used to display progress,
        control verbosity, and pass CLI arguments to the benchmark runner.

        :param session: The session to use for the benchmark case.
        :type session: Optional[Session]
        """
        all_variations = self.expanded_kwargs_variations
        progress_tracker = ProgressTracker(
            session=session,
            task_name='Case:run',
            progress_max=len(all_variations),
            description=f'Running case {self.title}',
            color=Color.CYAN)
        progress_tracker.reset()

        kwargs: dict[str, Any]
        for variations_counter, kwargs in enumerate(all_variations):
            bench: SimpleRunner
            if self.runner is not None and issubclass(self.runner, SimpleRunner):
                runner: type[SimpleRunner] = self.runner
                bench = runner(case=self, session=session, kwargs=kwargs)
            elif session and session.default_runner is not None:
                bench = session.default_runner(case=self, session=session, kwargs=kwargs)
            else:
                bench = SimpleRunner(case=self, session=session, kwargs=kwargs)
            try:
                results: Results = self.action(bench, **kwargs)
            except Exception as e:
                raise SimpleBenchRuntimeError(
                    f'Error running benchmark action {str(self.action)} for case '
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

    def as_dict(self, full_data: bool = False) -> dict[str, Any]:
        """Returns the benchmark case and results as a JSON serializable dict.

        Only the results statistics are included by default. To include full results data,
        set `full_data` to True.

        :param full_data: Whether to include full results data. Defaults to False.
        :type full_data: bool
        :return: A JSON serializable dict representation of the benchmark case and results.
        :rtype: dict[str, Any]
        """
        results = []
        for result in self.results:
            results.append(result.as_dict(full_data=full_data))

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

        :param section: The section for which to calculate the mean.
        :type section: Section
        :return: The mean value for the specified section.
        :rtype: float
        """
        if not isinstance(section, Section):
            raise SimpleBenchTypeError(
                f'Invalid section type: {type(section)}. Must be of type Section.',
                tag=_CaseErrorTag.SECTION_MEAN_INVALID_SECTION_TYPE_ARGUMENT
                )
        if section not in (Section.OPS, Section.TIMING):
            raise SimpleBenchValueError(
                f'Invalid section: {section}. Must be Section.OPS or Section.TIMING.',
                tag=_CaseErrorTag.SECTION_MEAN_INVALID_SECTION_ARGUMENT
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
