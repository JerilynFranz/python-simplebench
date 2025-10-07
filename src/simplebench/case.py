# -*- coding: utf-8 -*-
"""Benchmark case declaration and execution."""
from __future__ import annotations
from copy import copy
import inspect
import itertools
from typing import Any, Callable, Optional, TYPE_CHECKING, get_type_hints

from .constants import DEFAULT_ITERATIONS, DEFAULT_WARMUP_ITERATIONS, DEFAULT_MIN_TIME, DEFAULT_MAX_TIME
from .exceptions import (SimpleBenchValueError, SimpleBenchTypeError, SimpleBenchRuntimeError, ErrorTag)
from .metaclasses import ICase
from .protocols import ActionRunner, ReporterCallback
from .reporters.reporter_option import ReporterOption
from .results import Results
from .runners import SimpleRunner
from .enums import Section, Format
from .validators import (validate_non_blank_string, validate_positive_int,
                         validate_non_negative_int, validate_positive_float)


if TYPE_CHECKING:
    from .session import Session
    from .tasks import RichTask


class Case(ICase):
    '''Declaration of a benchmark case.

    A benchmark case defines the specific benchmark to be run, including the
    action to be performed, the parameters for the benchmark, and any variations
    of those parameters as well as the reporting group and title for the benchmark.

    It also defines the number of iterations, warmup iterations, minimum and maximum
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

    The Case class is designed to be immutable after creation. Once a Case instance
    is created, its properties cannot be directly changed. This immutability ensures that
    benchmark cases remain consistent throughout their lifecycle.

    The results of the benchmark runs are stored in the `results` property, which is a list
    of Results objects. Each Results object corresponds to a specific combination of
    keyword argument variations.

    Properties:
        group (str): The benchmark reporting group to which the benchmark case belongs.
        title (str): The name of the benchmark case.
        description (str): A brief description of the benchmark case.
        action (ActionRunner): The function to perform the benchmark. This function must
            accept a `bench` parameter of type SimpleRunner and arbitrary keyword arguments ('**kwargs').
            It must return a Results object.
        iterations (int): The minimum number of iterations to run for the benchmark.
        warmup_iterations (int): The number of warmup iterations to run before the benchmark.
        min_time (float): The minimum time for the benchmark in seconds.
        max_time (float): The maximum time for the benchmark in seconds.
        variation_cols (dict[str, str]): kwargs to be used for cols to denote kwarg variations in reports.
            Each key is a keyword argument name, and the value is the column label to use for that argument.
            Only keywords that are also in `kwargs_variations` can be used here. These fields will be
            added to the output of reporters that support them as columns of data with the specified labels.
        kwargs_variations (dict[str, list[Any]]): A mapping of keyword argument names to their variations.
            Each key is a keyword argument name, and the value is a list of possible values.

            When tests are run, the benchmark will be executed for each combination of the specified
            keyword argument variations. For example, if `kwargs_variations` is:
                {
                    'size': [10, 100],
                    'mode': ['fast', 'accurate']
                }
            The benchmark will be run 4 times with the following combinations of keyword arguments:
                1. size=10, mode='fast'
                2. size=10, mode='accurate'
                3. size=100, mode='fast'
                4. size=100, mode='accurate'
            The action function will be called with these keyword arguments accordingly and must
            accept them.
        expanded_kwargs_variations (list[dict[str, Any]]): A list of all combinations of keyword argument
            variations.
        runner (Optional[type[SimpleRunner]]): A custom runner class for the benchmark.
            If None, the default SimpleRunner is used.  (default: None)

            A custom runner class must be a subclass of SimpleRunner and must have a method
            named `run` that accepts the same parameters as SimpleRunner.run and returns a Results object.
            The action function will be called with a `bench` parameter that is an instance of the
            custom runner.

            It may also accept additional parameters to the run method as needed. If additional
            parameters are required, they must be specified in the `action` function signature.
        callback (Optional[ReporterCallback]): A callback function to be called with the benchmark
            results. This function should accept four arguments: the Case instance, the Section,
            the ReporterOption, and the output object. Leave as None if no callback is needed.
            (default: None)
        results (list[Results]): The benchmark results for the case. This is populated by the
            action function during the benchmark run.
    '''
    __slots__ = ('_group', '_title', '_description', '_action',
                 '_iterations', '_warmup_iterations', '_min_time', '_max_time',
                 '_variation_cols', '_kwargs_variations', '_runner',
                 '_callback', '_results', '_options')

    def __init__(self, *,
                 group: str,
                 title: str,
                 description: str,
                 action: ActionRunner,
                 iterations: int = DEFAULT_ITERATIONS,
                 warmup_iterations: int = DEFAULT_WARMUP_ITERATIONS,
                 min_time: float = DEFAULT_MIN_TIME,
                 max_time: float = DEFAULT_MAX_TIME,
                 variation_cols: Optional[dict[str, str]] = None,
                 kwargs_variations: Optional[dict[str, list[Any]]] = None,
                 runner: Optional[type[SimpleRunner]] = None,
                 callback: Optional[ReporterCallback] = None,
                 options: Optional[list[ReporterOption]] = None) -> None:
        """Constructor for Case.

        Args:
            group (str): The benchmark reporting group to which the benchmark case belongs.
            title (str): The name of the benchmark case.
            description (str): A brief description of the benchmark case.
            action (Callable[..., Results]): The function to perform the benchmark. This function must
                accept a `bench` parameter of type SimpleRunner and arbitrary keyword arguments ('**kwargs').
                It must return a Results object.
            iterations (int): The minimum number of iterations to run for the benchmark.
                (default: 20 - DEFAULT_ITERATIONS)
            warmup_iterations (int): The number of warmup iterations to run before the benchmark.
                (default: 10 - DEFAULT_WARMUP_ITERATIONS)
            min_time (float | int): The minimum time for the benchmark in seconds.
                (default: 5.0 seconds - DEFAULT_MIN_TIME)
            max_time (float | int): The maximum time for the benchmark in seconds.
                (default: 20.0 seconds - DEFAULT_MAX_TIME)
            variation_cols (dict[str, str]): kwargs to be used for cols to denote kwarg variations.
                Each key is a keyword argument name, and the value is the column label to use for that argument.
                (default: None)
            kwargs_variations (dict[str, list[Any]]):
                Variations of keyword arguments for the benchmark.
                Each key is a keyword argument name, and the value is a list of possible values.
                (default: None)
            runner (Optional[type[SimpleRunner]]): A custom runner class for the benchmark.
                If None, the default SimpleRunner is used. (default: None)
                The custom runner class must be a subclass of SimpleRunner and must have a method
                named `run` that accepts the same parameters as SimpleRunner.run and returns a Results object.
                The action function will be called with a `bench` parameter that is an instance of the
                custom runner.
                It may also accept additional parameters to the run method as needed. If additional
                parameters are needed for the custom runner, they will need to be passed to the run
                method as keyword arguments.
                No support is provided for passing additional parameters to a custom runner from the @benchmark
                decorator.
            callback (ReporterCallback):
                A callback function for additional processing of the report. The function should accept
                four arguments: the Case instance, the Section, the Format, and the generated report data.
                Leave as None if no callback is needed. (default: None)
                The callback function will be called with the following arguments:
                    case (Case): The `Case` instance processed for the report.
                    section (Section): The `Section` of the report.
                    output_format (Format): The `Format` of the report.
                    output (Any): The generated report data. Note that the actual type of this data will
                        depend on the Format specified for the report and the type generated by the
                        reporter for that Format
            options (list[ReporterOption]): A list of additional options for the benchmark case.
                Each option is an instance of ReporterOption or a subclass of ReporterOption.
                Reporter options can be used to customize the output of the benchmark reports for
                specific reporters. Reporters are responsible for extracting applicable ReporterOptions
                from the list of options themselves. (default: [])
        """
        self._group = validate_non_blank_string(
                        group, "group",
                        ErrorTag.CASE_INVALID_GROUP_TYPE,
                        ErrorTag.CASE_INVALID_GROUP_VALUE)
        self._title = validate_non_blank_string(
                        title, "title",
                        ErrorTag.CASE_INVALID_TITLE_TYPE,
                        ErrorTag.CASE_INVALID_TITLE_VALUE)
        self._description = validate_non_blank_string(
                        description, "description",
                        ErrorTag.CASE_INVALID_DESCRIPTION_TYPE,
                        ErrorTag.CASE_INVALID_DESCRIPTION_VALUE)
        self._action = Case.validate_action_signature(action)
        self._iterations = validate_positive_int(
                        iterations, "iterations",
                        ErrorTag.CASE_INVALID_ITERATIONS_TYPE,
                        ErrorTag.CASE_INVALID_ITERATIONS_VALUE)
        self._warmup_iterations = validate_non_negative_int(
                        warmup_iterations, "warmup_iterations",
                        ErrorTag.CASE_INVALID_WARMUP_ITERATIONS_TYPE,
                        ErrorTag.CASE_INVALID_WARMUP_ITERATIONS_VALUE)
        self._min_time = validate_positive_float(
                        min_time, "min_time",
                        ErrorTag.CASE_INVALID_MIN_TIME_TYPE,
                        ErrorTag.CASE_INVALID_MIN_TIME_VALUE)
        self._max_time = validate_positive_float(
                        max_time, "max_time",
                        ErrorTag.CASE_INVALID_MAX_TIME_TYPE,
                        ErrorTag.CASE_INVALID_MAX_TIME_VALUE)
        self._kwargs_variations = Case.validate_kwargs_variations(kwargs_variations)
        self._variation_cols = Case.validate_variation_cols(variation_cols, self._kwargs_variations)
        self._runner = Case.validate_runner(runner)
        self._callback = Case.validate_callback(callback)
        self._options = Case.validate_options(options)
        self._results: list[Results] = []  # No validation needed here
        self.validate_time_range(self._min_time, self._max_time)

    @staticmethod
    def validate_time_range(min_time: float, max_time: float) -> None:
        """Validate that min_time < max_time for the case.

        Args:
            min_time (float): The minimum time.
            max_time (float): The maximum time.

        Returns:
            None

        Raises:
            SimpleBenchValueError: The min_time is greater than max_time.
        """
        if min_time > max_time:
            raise SimpleBenchValueError(
                f'Invalid time range: min_time {min_time} > max_time {max_time}.',
                tag=ErrorTag.CASE_INVALID_TIME_RANGE)

    @staticmethod
    def validate_action_signature(action: ActionRunner) -> ActionRunner:
        """Validate that action has correct signature.

        An action function must accept the following two parameters:
            - bench: SimpleRunner
            - **kwargs: Arbitrary keyword arguments

        This is equivalent to the `ActionRunner` protocol.

        Args:
            action (ActionRunner): The action function to validate.

        Returns:
            ActionRunner: The validated action function.

        Raises:
            SimpleBenchTypeError: If the action is not callable or has an invalid signature.
        """
        if not callable(action):
            raise SimpleBenchTypeError(
                f'Invalid action: {action}. Must be a callable.',
                tag=ErrorTag.CASE_INVALID_ACTION_NOT_CALLABLE
                )
        action_signature = inspect.signature(action)
        if 'bench' not in action_signature.parameters:
            raise SimpleBenchTypeError(
                f'Invalid action: {action}. Must accept a "bench" parameter.',
                tag=ErrorTag.CASE_INVALID_ACTION_MISSING_BENCH_PARAMETER
                )
        kwargs_param = action_signature.parameters.get('kwargs')
        if kwargs_param is None or kwargs_param.kind not in (inspect.Parameter.VAR_KEYWORD,):
            raise SimpleBenchTypeError(
                f'Invalid action: {action}. Must accept "**kwargs" parameter.',
                tag=ErrorTag.CASE_INVALID_ACTION_MISSING_KWARGS_PARAMETER
                )
        if len(action_signature.parameters) != 2:
            raise SimpleBenchValueError(
                f'Invalid action: {action}. Must accept exactly 2 parameters: bench and **kwargs.',
                tag=ErrorTag.CASE_INVALID_ACTION_PARAMETER_COUNT
            )
        return action

    @staticmethod
    def resolve_callback_type_hints(callback: Callable) -> dict[str, type]:
        """Resolve the type hints for a callback function.

        Args:
            callback (Callable): The callback function to resolve type hints for.

        Returns:
            dict[str, type]: A dictionary mapping parameter names to their resolved types.

        Raises:
            SimpleBenchTypeError: If the type hints cannot be resolved.
        """
        try:
            resolved_hints = get_type_hints(
                callback, globalns=callback.__globals__)  # pyright: ignore[reportAttributeAccessIssue]
        except (NameError, TypeError) as e:
            # This can happen if an annotation refers to a type that doesn't exist.
            raise SimpleBenchTypeError(
                f"Invalid callback: {callback}. Could not resolve type hints. Original error: {e}",
                tag=ErrorTag.CASE_INVALID_CALLBACK_UNRESOLVABLE_HINTS
            ) from e
        return resolved_hints

    @staticmethod
    def validate_callback_parameter(callback: Callable,
                                    expected_type: type | Any,
                                    param_name: str) -> None:
        """Validate a parameter of the callback function.

        The parameter must exist, be of the expected type, and be a keyword-only parameter.

        Args:
            callback (Callable): The callback function to validate.
            expected_type (type | Any): The expected type of the parameter.
            param_name (str): The name of the parameter to validate.

        Raises:
            SimpleBenchTypeError: If the parameter is invalid.
        """
        resolved_hints = Case.resolve_callback_type_hints(callback)
        callback_signature = inspect.signature(callback)
        if param_name not in callback_signature.parameters:
            raise SimpleBenchTypeError(
                f'Invalid callback: {callback}. Must accept an "{param_name}" parameter.',
                tag=ErrorTag.CASE_INVALID_CALLBACK_INCORRECT_SIGNATURE_MISSING_PARAMETER)
        param_type = resolved_hints.get(param_name)
        if param_type is not expected_type:
            raise SimpleBenchTypeError(
                f"Invalid callback: {callback}. '{param_name}' parameter must be of type "
                f"'{expected_type}', not '{param_type}'.",
                tag=ErrorTag.CASE_INVALID_CALLBACK_INCORRECT_SIGNATURE_PARAMETER_TYPE)

        param = callback_signature.parameters[param_name]
        if param.kind is not inspect.Parameter.KEYWORD_ONLY:
            raise SimpleBenchTypeError(
                f'Invalid callback: {callback}. "{param_name}" parameter must be a keyword-only parameter.',
                tag=ErrorTag.CASE_INVALID_CALLBACK_INCORRECT_SIGNATURE_PARAMETER_NOT_KEYWORD_ONLY)

    @staticmethod
    def validate_callback(callback: Optional[ReporterCallback]) -> ReporterCallback | None:
        """Validate the callback function.

        It must be a callable or None. If callable, it must have the correct signature.

        A callback function must accept the following four keyword-only parameters:
            - case: Case
            - section: Section
            - output_format: Format
            - output: Any

        Args:
            callback (Optional[ReporterCallback]): The callback function to validate.

        Returns:
            ReporterCallback | None: The validated callback function or None.

        Raises:
            SimpleBenchTypeError: If the callback is invalid.
        """
        if callback is None:
            return None
        if not callable(callback):
            raise SimpleBenchTypeError(
                f'Invalid callback: {callback}. Must be a callable or None.',
                tag=ErrorTag.CASE_INVALID_CALLBACK_NOT_CALLABLE_OR_NONE)
        callback_signature = inspect.signature(callback)
        Case.validate_callback_parameter(callback, Case, 'case')
        Case.validate_callback_parameter(callback, Section, 'section')
        Case.validate_callback_parameter(callback, Format, 'output_format')
        Case.validate_callback_parameter(callback, Any, 'output')
        params = list(callback_signature.parameters.values())
        if len(params) != 4:
            raise SimpleBenchTypeError(
                f'Invalid callback: {callback}. Must accept exactly four keyword-only parameters with the following '
                'names and types: case: Case, section: Section, output_format: Format, output: Any',
                tag=ErrorTag.CASE_INVALID_CALLBACK_INCORRECT_NUMBER_OF_PARAMETERS)
        return callback

    @staticmethod
    def validate_kwargs_variations(value: dict[str, list[Any]] | None) -> dict[str, list[Any]]:
        """Validate the kwargs_variations dictionary.

        Validates that the kwargs_variations is a dictionary where each key is a string
        that is a valid Python identifier, and each value is a non-empty list.

        A shallow copy of the validated dictionary and the lists is performed before returning to prevent
        external modification.

        Args:
            value (dict[str, list[Any]] | None): The kwargs_variations dictionary to validate.

        Returns:
            dict[str, list[Any]]: A shallow copy of the validated kwargs_variations dictionary or {} if not provided.
                The keys are strings that are valid Python identifiers, and the values are non-empty lists.
                The lists may contain any type of values.

        Raises:
            SimpleBenchTypeError: If the kwargs_variations is not a dictionary or if any key is not a string
                that is a valid Python identifier.
            SimpleBenchValueError: If any value is not a list or is an empty list.
        """
        if value is None:
            return {}
        if not isinstance(value, dict):
            raise SimpleBenchTypeError(
                f'Invalid kwargs_variations: {value}. Must be a dictionary.',
                tag=ErrorTag.CASE_INVALID_KWARGS_VARIATIONS_NOT_DICT
                )
        validated_dict = {}
        for key, kw_value in value.items():
            if not isinstance(key, str):
                raise SimpleBenchTypeError(
                    f'Invalid kwargs_variations entry key: {key}. Keys must be of type str.',
                    tag=ErrorTag.CASE_INVALID_KWARGS_VARIATIONS_ENTRY_KEY_TYPE
                    )
            if not key.isidentifier():
                raise SimpleBenchValueError(
                    f'Invalid kwargs_variations entry key: {key}. Keys must be valid Python identifiers.',
                    tag=ErrorTag.CASE_INVALID_KWARGS_VARIATIONS_ENTRY_KEY_NOT_IDENTIFIER
                    )
            if not isinstance(kw_value, list):
                raise SimpleBenchTypeError(
                    f'Invalid kwargs_variations entry value for entry "{key}": {kw_value}. Values must be in a list.',
                    tag=ErrorTag.CASE_INVALID_KWARGS_VARIATIONS_ENTRY_VALUE_NOT_LIST
                    )
            if not kw_value:
                raise SimpleBenchValueError(
                    (f'Invalid kwargs_variations entry value for entry "{key}": {kw_value}. '
                     'Values cannot be empty lists.'),
                    tag=ErrorTag.CASE_INVALID_KWARGS_VARIATIONS_ENTRY_VALUE_EMPTY_LIST
                    )
            validated_dict[key] = copy(kw_value)
        return validated_dict

    @staticmethod
    def validate_variation_cols(variation_cols: dict[str, str] | None,
                                kwargs_variations: dict[str, list[Any]]) -> dict[str, str]:
        """Validate the variation_cols dictionary.

        Args:
            variation_cols (dict[str, str] | None): The variation_cols dictionary to validate.
            kwargs_variations (dict[str, list[Any]]): The kwargs_variations dictionary to validate against.

        Returns:
            dict[str, str]: A shallow copy of the validated variation_cols dictionary or {} if not provided.
                Each key is a keyword argument name from `kwargs_variations`, and each value is a
                non-blank string to be used as the column label for that argument in reports.
        Raises:
            SimpleBenchTypeError: If the variation_cols is not a dictionary or if any key or
                value is not a string.
            SimpleBenchValueError: If any key is not found in `kwargs_variations` or if any
                value is a blank string.
        """
        if variation_cols is None:
            return {}
        if not isinstance(variation_cols, dict):
            raise SimpleBenchTypeError(
                f'Invalid variation_cols: {variation_cols}. Must be a dictionary.',
                tag=ErrorTag.CASE_INVALID_VARIATION_COLS_NOT_DICT
                )
        validated_dict: dict[str, str] = {}
        for key, vc_value in variation_cols.items():
            if key not in kwargs_variations:
                raise SimpleBenchValueError(
                    f'Invalid variation_cols entry key: {key}. Key not found in kwargs_variations.',
                    tag=ErrorTag.CASE_INVALID_VARIATION_COLS_ENTRY_KEY_NOT_IN_KWARGS)
            if not isinstance(vc_value, str):
                raise SimpleBenchTypeError(
                    f'Invalid variation_cols entry value for entry "{key}": "{vc_value}". Values must be of type str.',
                    tag=ErrorTag.CASE_INVALID_VARIATION_COLS_ENTRY_VALUE_NOT_STRING
                    )
            stripped_value = vc_value.strip()
            if stripped_value == '':
                raise SimpleBenchValueError(
                    f'Invalid variation_cols entry value: "{vc_value}". Values cannot be blank strings.',
                    tag=ErrorTag.CASE_INVALID_VARIATION_COLS_ENTRY_VALUE_BLANK
                    )
            validated_dict[key] = stripped_value
        return validated_dict

    @staticmethod
    def validate_runner(value: type[SimpleRunner] | None) -> type[SimpleRunner] | None:
        """Validate the runner class.

        Args:
            value (Optional[type[SimpleRunner]]): The runner class to validate.
        Returns:
            Optional[type[SimpleRunner]]: The validated runner class or None.
        Raises:
            SimpleBenchTypeError: If the runner is not a subclass of SimpleRunner or None.
        """
        if value is None:
            return None
        if not (isinstance(value, type) and issubclass(value, SimpleRunner)):
            raise SimpleBenchTypeError(
                f'Invalid runner: {value}. Must be a subclass of SimpleRunner or None.',
                tag=ErrorTag.CASE_INVALID_RUNNER_NOT_SIMPLE_RUNNER_SUBCLASS
                )
        return value

    @staticmethod
    def validate_options(value: list[ReporterOption] | None) -> list[ReporterOption]:
        """Validate the options list.

        Args:
            value (list[ReporterOption] | None): The options list to validate or None.

        Returns:
            A shallow copy of the validated options list or an empty list if not provided.

        Raises:
            SimpleBenchTypeError: If options is not a list or if any entry is not a ReporterOption.
        """
        if value is None:
            return []
        if not isinstance(value, list):
            raise SimpleBenchTypeError(
                f'Invalid options: {value}. Must be a list.',
                tag=ErrorTag.CASE_INVALID_OPTIONS_NOT_LIST
                )
        for option in value:
            if not isinstance(option, ReporterOption):
                raise SimpleBenchTypeError(
                    f'Invalid option: {option}. Must be of type ReporterOption or a sub-class.',
                    tag=ErrorTag.CASE_INVALID_OPTIONS_ENTRY_NOT_REPORTER_OPTION
                    )
        return copy(value)

    @property
    def group(self) -> str:
        """The benchmark reporting group to which the benchmark case belongs."""
        return self._group

    @property
    def title(self) -> str:
        """The name of the benchmark case."""
        return self._title

    @property
    def description(self) -> str:
        """A brief description of the benchmark case."""
        return self._description

    @property
    def action(self) -> ActionRunner:
        """The function to perform the benchmark.

        The function must accept a `bench` parameter of type SimpleRunner and
        arbitrary keyword arguments ('**kwargs') and return a Results object.

        Example:
        .. code-block:: python

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
        '''The number of iterations to run for the benchmark.'''
        return self._iterations

    @property
    def warmup_iterations(self) -> int:
        '''The number of warmup iterations to run before the benchmark.'''
        return self._warmup_iterations

    @property
    def min_time(self) -> float:
        '''The minimum time for the benchmark in seconds.'''
        return self._min_time

    @property
    def max_time(self) -> float:
        '''The maximum time for the benchmark in seconds.'''
        return self._max_time

    @property
    def variation_cols(self) -> dict[str, str]:
        '''Keyword arguments to be used for columns to denote kwarg variations.

        Note that all keys in variation_cols must be present in kwargs_variations and
        updating it may require changes to both variation_cols and kwargs_variations_cols.

        Updating variation_cols does not automatically update kwargs_variations, and vice versa.

        Returns:
            A dictionary mapping keyword argument names to column labels.

        Each key is a keyword argument name, and the value is the column label to use for that argument.
        '''
        # shallow copy to prevent external modification of internal dict
        return copy(self._variation_cols) if self._variation_cols is not None else {}

    @property
    def kwargs_variations(self) -> dict[str, list[Any]]:
        """Variations of keyword arguments for the benchmark."""
        if self._kwargs_variations is None:
            return {}
        # shallow copy to prevent external modification of internal dict
        return {key: list(value) for key, value in self._kwargs_variations.items()}

    @property
    def runner(self) -> type[SimpleRunner] | None:
        '''A custom runner for the benchmark. If None, the default SimpleRunner is used.'''
        return self._runner

    @property
    def callback(self) -> ReporterCallback | None:
        '''A callback function for additional processing of a report.'''
        return self._callback

    @property
    def results(self) -> list[Results]:
        '''The benchmark list of Results for the case.

        This is a read-only attribute. To add results, use the `run` method.

        Returns:
            A list of Results objects for each variation run of the benchmark case.
        '''
        # shallow copy to prevent external modification of internal list
        return copy(self._results)

    @property
    def options(self) -> list[ReporterOption]:
        '''A list of additional options for the benchmark case.'''
        # shallow copy to prevent external modification of internal list
        return copy(self._options) if self._options is not None else []

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
        kwargs: dict[str, Any]
        for variations_counter, kwargs in enumerate(all_variations):
            bench: SimpleRunner
            if self.runner is not None and issubclass(self.runner, SimpleRunner):
                runner: type[SimpleRunner] = self.runner
                bench = runner(case=self, session=session, kwargs=kwargs)
            elif session and session.default_runner:
                bench = session.default_runner(case=self, session=session, kwargs=kwargs)
            else:
                bench = SimpleRunner(case=self, session=session, kwargs=kwargs)
            try:
                results: Results = self.action(bench, **kwargs)
            except Exception as e:
                raise SimpleBenchRuntimeError(
                    f'Error running benchmark action {str(self.action)} for case '
                    f'"{self.title}" with kwargs {kwargs}: {e}, {type(e)}',
                    tag=ErrorTag.CASE_BENCHMARK_ACTION_RAISED_EXCEPTION
                    ) from e
            self._results.append(results)
            if task:
                task.update(
                        description=(f'[cyan] Running case {self.title} '
                                     f'({variations_counter + 1}/{len(all_variations)})'),
                        completed=variations_counter + 1,
                        refresh=True)
        if task:
            task.stop()

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
                results.append(result.as_dict)
            else:  # otherwise only stats
                results.append(result.as_dict_with_data)
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
