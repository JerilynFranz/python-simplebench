# -*- coding: utf-8 -*-
"""Benchmark case declaration and execution."""
from __future__ import annotations
import inspect
import itertools
from typing import Any, Callable, Optional, TYPE_CHECKING, get_type_hints

from .constants import DEFAULT_ITERATIONS, DEFAULT_WARMUP_ITERATIONS, DEFAULT_MIN_TIME, DEFAULT_MAX_TIME
from .exceptions import (SimpleBenchValueError, SimpleBenchTypeError, SimpleBenchAttributeError,
                         SimpleBenchRuntimeError, ErrorTag)
from .metaclasses import ICase
from .protocols import ActionRunner, ReporterCallback
from .reporters.reporter_option import ReporterOption
from .results import Results
from .runners import SimpleRunner
from .enums import Section, Format


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
                 '_callback', '_results', '_options', '_readonly')

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
        self._readonly: bool = False  # Allow setting parameters during initialization
        self.group = group
        self.title = title
        self.description = description
        self.action = action
        self.iterations = iterations
        self.warmup_iterations = warmup_iterations
        self.min_time = min_time
        self.max_time = max_time
        self.kwargs_variations = kwargs_variations if kwargs_variations is not None else {}
        self.variation_cols = variation_cols if variation_cols is not None else {}
        self.runner = runner
        self.callback = callback
        self.options = options if options is not None else []
        self._results: list[Results] = []  # No setter validation needed here
        self._readonly = True
        self._validate_time_range()

    def _validate_non_empty_string(
            self, value: str, field_name: str, type_error_tag: ErrorTag, value_error_tag: ErrorTag) -> str:
        """Validate and normalize a non-empty string field.

        Args:
            value (str): The string value to validate.
            field_name (str): The name of the field being validated (for error messages).
            type_error_tag (ErrorTag): The error tag to use for type errors.
            value_error_tag (ErrorTag): The error tag to use for value errors.

        Returns:
            str: The stripped string value.

        Raises:
            SimpleBenchTypeError: If the value is not a string.
            SimpleBenchValueError: If the string is empty or only whitespace.
        """
        if not isinstance(value, str):
            raise SimpleBenchTypeError(
                f'Invalid {field_name} type: {type(value)}. Must be a string.',
                tag=type_error_tag
            )
        if not value.strip():
            raise SimpleBenchValueError(
                f'Invalid {field_name}: cannot be empty or whitespace.',
                tag=value_error_tag
            )
        return value.strip()

    def _validate_positive_int(
            self, value: int, field_name: str, type_tag: ErrorTag, value_tag: ErrorTag) -> int:
        """Validate that a value is a positive integer.

        Args:
            value (int): The value to validate.
            field_name (str): The name of the field being validated (for error messages).
            type_tag (ErrorTag): The error tag to use for type errors.
            value_tag (ErrorTag): The error tag to use for value errors.

        Returns:
            int: The validated positive integer.

        Raises:
            SimpleBenchTypeError: If the value is not an integer.
            SimpleBenchValueError: If the value is not positive.
        """
        if not isinstance(value, int):
            raise SimpleBenchTypeError(
                f'Invalid {field_name} type: {type(value)}. Must be an int.',
                tag=type_tag
            )
        if value <= 0:
            raise SimpleBenchValueError(
                f'Invalid {field_name}: must be a positive integer.',
                tag=value_tag
            )
        return value

    def _validate_non_negative_int(
            self, value: int, field_name: str, type_tag: ErrorTag, value_tag: ErrorTag) -> int:
        if not isinstance(value, int):
            raise SimpleBenchTypeError(
                f'Invalid {field_name} type: {type(value)}. Must be an int.',
                tag=type_tag
            )
        if value < 0:
            raise SimpleBenchValueError(
                f'Invalid {field_name}: must be a non-negative integer.',
                tag=value_tag
            )
        return value

    def _validate_positive_float(
            self, value: float | int, field_name: str, type_tag: ErrorTag, value_tag: ErrorTag) -> float:
        """Validate that a value is a positive float or integer.

        Converts integers to floats.

        Args:
            value (float | int): The value to validate.
            field_name (str): The name of the field being validated (for error messages).
            type_tag (ErrorTag): The error tag to use for type errors.
            value_tag (ErrorTag): The error tag to use for value errors.
        Returns:
            float: The validated positive float.
        Raises:
            SimpleBenchTypeError: If the value is not a float.
            SimpleBenchValueError: If the value is not positive.
        """
        if not isinstance(value, (float, int)):  # Allow ints as valid floats
            raise SimpleBenchTypeError(
                f'Invalid {field_name} type: {type(value)}. Must be a float or int.',
                tag=type_tag
            )
        if value <= 0.0:
            raise SimpleBenchValueError(
                f'Invalid {field_name}: must be a positive float or int.',
                tag=value_tag
            )
        return float(value)

    def _validate_time_range(self) -> None:
        """Validate that min_time < max_time for the case.

        Returns:
            None

        Raises:
            SimpleBenchValueError: If any of the parameters are invalid.
            SimpleBenchTypeError: If any of the parameters are of the wrong type.
        """
        if self.min_time > self.max_time:
            raise SimpleBenchValueError(
                f'Invalid time range: min_time {self.min_time} > max_time {self.max_time}.',
                tag=ErrorTag.CASE_INVALID_TIME_RANGE)

    def _validate_action_signature(self, action: ActionRunner) -> None:
        """Validate that action has correct signature.

        An action function must accept the following two parameters:
            - bench: SimpleRunner
            - **kwargs: Arbitrary keyword arguments

        This is equivalent to the `ActionRunner` protocol.

        Args:
            action (ActionRunner): The action function to validate.
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

    def _resolve_callback_type_hints(self, callback: Callable) -> dict[str, type]:
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

    def _validate_callback_parameter(self,
                                     callback: Callable,
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
        resolved_hints = self._resolve_callback_type_hints(callback)
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

    def _validate_callback(self, callback: Optional[ReporterCallback]) -> ReporterCallback | None:
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
            return
        if not callable(callback):
            raise SimpleBenchTypeError(
                f'Invalid callback: {callback}. Must be a callable or None.',
                tag=ErrorTag.CASE_INVALID_CALLBACK_NOT_CALLABLE_OR_NONE)
        callback_signature = inspect.signature(callback)
        self._validate_callback_parameter(callback, Case, 'case')
        self._validate_callback_parameter(callback, Section, 'section')
        self._validate_callback_parameter(callback, Format, 'output_format')
        self._validate_callback_parameter(callback, Any, 'output')
        params = list(callback_signature.parameters.values())
        if len(params) != 4:
            raise SimpleBenchTypeError(
                f'Invalid callback: {callback}. Must accept exactly four keyword-only parameters with the following '
                'names and types: case: Case, section: Section, output_format: Format, output: Any',
                tag=ErrorTag.CASE_INVALID_CALLBACK_INCORRECT_NUMBER_OF_PARAMETERS)
        return callback

    def _validate_kwargs_variations(self, value: dict[str, list[Any]]) -> None:
        """Validate the kwargs_variations dictionary.

        Args:
            value (Optional[dict[str, list[Any]]]): The kwargs_variations dictionary to validate.

        Returns:
            dict[str, list[Any]]: The validated kwargs_variations dictionary or None if not provided.

        Raises:
            SimpleBenchTypeError: If the kwargs_variations is not a dictionary or if any key is not a string
            that is a valid Python identifier.
            SimpleBenchValueError: If any value is not a list or is an empty list.
        """
        if not isinstance(value, dict):
            raise SimpleBenchTypeError(
                f'Invalid kwargs_variations: {value}. Must be a dictionary.',
                tag=ErrorTag.CASE_INVALID_KWARGS_VARIATIONS_NOT_DICT
                )
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

    def _validate_variation_cols(self, value: dict[str, str]) -> None:
        """Validate the variation_cols dictionary.

        Args:
            value (dict[str, str]): The variation_cols dictionary to validate.
        Returns:
            None
        Raises:
            SimpleBenchTypeError: If the variation_cols is not a dictionary or if any key or
                value is not a string.
            SimpleBenchValueError: If any key is not found in `kwargs_variations` or if any
                value is a blank string.
        """
        if not isinstance(value, dict):
            raise SimpleBenchTypeError(
                f'Invalid variation_cols: {value}. Must be a dictionary.',
                tag=ErrorTag.CASE_INVALID_VARIATION_COLS_NOT_DICT
                )
        for key, vc_value in value.items():
            if key not in self.kwargs_variations:
                raise SimpleBenchValueError(
                    f'Invalid variation_cols entry key: {key}. Key not found in kwargs_variations.',
                    tag=ErrorTag.CASE_INVALID_VARIATION_COLS_ENTRY_KEY_NOT_IN_KWARGS)
            if not isinstance(vc_value, str):
                raise SimpleBenchTypeError(
                    f'Invalid variation_cols entry value for entry "{key}": "{vc_value}". Values must be of type str.',
                    tag=ErrorTag.CASE_INVALID_VARIATION_COLS_ENTRY_VALUE_NOT_STRING
                    )
            if vc_value.strip() == '':
                raise SimpleBenchValueError(
                    f'Invalid variation_cols entry value: "{vc_value}". Values cannot be blank strings.',
                    tag=ErrorTag.CASE_INVALID_VARIATION_COLS_ENTRY_VALUE_BLANK
                    )

    def _validate_options(self, value: list[ReporterOption]) -> None:
        """Validate the options list.
        Args:
            value (list[ReporterOption]): The options list to validate.
        Returns:
            None
        Raises:
            SimpleBenchTypeError: If options is not a list or if any entry is not a ReporterOption.
        """
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

    @property
    def group(self) -> str:
        """The benchmark reporting group to which the benchmark case belongs."""
        return self._group

    @group.setter
    def group(self, value: str) -> None:
        if self._readonly:
            raise SimpleBenchAttributeError(
                'group attribute is read-only.',
                name='group', obj=self, tag=ErrorTag.CASE_MODIFY_READONLY_GROUP)
        self._group = self._validate_non_empty_string(
                        value=value,
                        field_name='group',
                        type_error_tag=ErrorTag.CASE_INVALID_GROUP_TYPE,
                        value_error_tag=ErrorTag.CASE_INVALID_GROUP_VALUE)

    @property
    def title(self) -> str:
        """The name of the benchmark case."""
        return self._title

    @title.setter
    def title(self, value: str) -> None:
        if self._readonly:
            raise SimpleBenchAttributeError(
                'title attribute is read-only.',
                name='title', obj=self, tag=ErrorTag.CASE_MODIFY_READONLY_TITLE)
        self._title = self._validate_non_empty_string(
                        value=value,
                        field_name='title',
                        type_error_tag=ErrorTag.CASE_INVALID_TITLE_TYPE,
                        value_error_tag=ErrorTag.CASE_INVALID_TITLE_VALUE)

    @property
    def description(self) -> str:
        """A brief description of the benchmark case."""
        return self._description

    @description.setter
    def description(self, value: str) -> None:
        if self._readonly:
            raise SimpleBenchAttributeError(
                'description attribute is read-only.',
                name='description', obj=self, tag=ErrorTag.CASE_MODIFY_READONLY_DESCRIPTION)
        self._description = self._validate_non_empty_string(
                        value=value,
                        field_name='description',
                        type_error_tag=ErrorTag.CASE_INVALID_DESCRIPTION_TYPE,
                        value_error_tag=ErrorTag.CASE_INVALID_DESCRIPTION_VALUE
                    )

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

        Args:
            action (ActionRunner): The benchmark action function.
            **kwargs: Arbitrary keyword arguments to be passed to the action function.

        Returns:
            A Results object containing the benchmark results.

        Raises:
            SimpleBenchTypeError: If the action is not callable.
            SimpleBenchValueError: If the action does not have the correct signature.

        """
        return self._action

    @action.setter
    def action(self, value: ActionRunner) -> None:
        if self._readonly:
            raise SimpleBenchAttributeError(
                'action attribute is read-only.',
                name='action', obj=self, tag=ErrorTag.CASE_MODIFY_READONLY_ACTION
            )
        self._validate_action_signature(value)
        self._action = value

    @property
    def iterations(self) -> int:
        '''The number of iterations to run for the benchmark.'''
        return self._iterations

    @iterations.setter
    def iterations(self, value: int) -> None:
        if self._readonly:
            raise SimpleBenchAttributeError(
                'iterations attribute is read-only.',
                name='iterations', obj=self, tag=ErrorTag.CASE_MODIFY_READONLY_ITERATIONS
            )
        self._iterations = self._validate_positive_int(
            value=value, field_name='iterations',
            type_tag=ErrorTag.CASE_INVALID_ITERATIONS_TYPE,
            value_tag=ErrorTag.CASE_INVALID_ITERATIONS_VALUE)

    @property
    def warmup_iterations(self) -> int:
        '''The number of warmup iterations to run before the benchmark.'''
        return self._warmup_iterations

    @warmup_iterations.setter
    def warmup_iterations(self, value: int) -> None:
        if self._readonly:
            raise SimpleBenchAttributeError(
                'warmup_iterations attribute is read-only.',
                name='warmup_iterations', obj=self,
                tag=ErrorTag.CASE_MODIFY_READONLY_WARMUP_ITERATIONS
            )
        self._warmup_iterations = self._validate_non_negative_int(
            value=value,
            field_name='warmup_iterations',
            type_tag=ErrorTag.CASE_INVALID_WARMUP_ITERATIONS_TYPE,
            value_tag=ErrorTag.CASE_INVALID_WARMUP_ITERATIONS_VALUE)

    @property
    def min_time(self) -> float:
        '''The minimum time for the benchmark in seconds.'''
        return self._min_time

    @min_time.setter
    def min_time(self, value: float | int) -> None:
        if self._readonly:
            raise SimpleBenchAttributeError(
                'min_time attribute is read-only.',
                name='min_time', obj=self, tag=ErrorTag.CASE_MODIFY_READONLY_MIN_TIME
            )
        self._min_time = self._validate_positive_float(
            value=value, field_name='min_time',
            type_tag=ErrorTag.CASE_INVALID_MIN_TIME_TYPE,
            value_tag=ErrorTag.CASE_INVALID_MIN_TIME_VALUE)

    @property
    def max_time(self) -> float:
        '''The maximum time for the benchmark in seconds.'''
        return self._max_time

    @max_time.setter
    def max_time(self, value: float | int) -> None:
        if self._readonly:
            raise SimpleBenchAttributeError(
                'max_time attribute is read-only.',
                name='max_time', obj=self, tag=ErrorTag.CASE_MODIFY_READONLY_MAX_TIME
            )
        self._max_time = self._validate_positive_float(
            value=value, field_name='max_time',
            type_tag=ErrorTag.CASE_INVALID_MAX_TIME_TYPE,
            value_tag=ErrorTag.CASE_INVALID_MAX_TIME_VALUE)

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
        return self._variation_cols if self._variation_cols is not None else {}

    @variation_cols.setter
    def variation_cols(self, value: dict[str, str]) -> None:
        if self._readonly:
            raise SimpleBenchAttributeError(
                'variation_cols attribute is read-only.',
                name='variation_cols', obj=self, tag=ErrorTag.CASE_MODIFY_READONLY_VARIATION_COLS
            )
        self._validate_variation_cols(value)
        self._variation_cols = value

    @property
    def kwargs_variations(self) -> dict[str, list[Any]]:
        '''Variations of keyword arguments for the benchmark.'''
        return self._kwargs_variations if self._kwargs_variations is not None else {}

    @kwargs_variations.setter
    def kwargs_variations(self, value: dict[str, list[Any]]) -> None:
        if self._readonly:
            raise SimpleBenchAttributeError(
                'kwargs_variations attribute is read-only.',
                name='kwargs_variations', obj=self, tag=ErrorTag.CASE_MODIFY_READONLY_KWARGS_VARIATIONS
            )
        self._validate_kwargs_variations(value)
        self._kwargs_variations = value

    @property
    def runner(self) -> Optional[type[SimpleRunner]]:
        '''A custom runner for the benchmark. If None, the default SimpleRunner is used.'''
        return self._runner

    @runner.setter
    def runner(self, value: Optional[type[SimpleRunner]]) -> None:
        if self._readonly:
            raise SimpleBenchAttributeError(
                'runner attribute is read-only.',
                name='runner', obj=self, tag=ErrorTag.CASE_MODIFY_READONLY_RUNNER
            )
        if value is not None and not issubclass(value, SimpleRunner):
            raise SimpleBenchTypeError(
                f'Invalid runner: {value}. Must be a subclass of SimpleRunner.',
                tag=ErrorTag.CASE_INVALID_RUNNER_NOT_SIMPLE_RUNNER_SUBCLASS
                )
        self._runner = value

    @property
    def callback(self) -> Optional[ReporterCallback]:
        '''A callback function for additional processing of a report.'''
        return self._callback

    @callback.setter
    def callback(self, value: Optional[ReporterCallback]) -> None:
        if self._readonly:
            raise SimpleBenchAttributeError(
                'callback attribute is read-only.',
                name='callback', obj=self, tag=ErrorTag.CASE_MODIFY_READONLY_CALLBACK
            )
        self._callback = self._validate_callback(value)

    @property
    def results(self) -> list[Results]:
        '''The benchmark list of Results for the case.'''
        return self._results

    @property
    def options(self) -> list[ReporterOption]:
        '''A list of additional options for the benchmark case.'''
        return self._options if self._options is not None else []

    @options.setter
    def options(self, value: list[ReporterOption]) -> None:
        if self._readonly:
            raise SimpleBenchAttributeError(
                'options attribute is read-only.',
                name='options', obj=self, tag=ErrorTag.CASE_MODIFY_READONLY_OPTIONS
            )
        self._validate_options(value)
        self._options = value

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
            if self.runner:
                bench = self.runner(case=self, session=session, kwargs=kwargs)
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
            self.results.append(results)
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
