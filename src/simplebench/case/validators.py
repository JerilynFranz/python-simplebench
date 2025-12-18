"""Validators for the simplebench.case package"""
import inspect
from copy import copy
from typing import Any, Callable, Iterable, Sequence, get_type_hints

import simplebench.defaults as defaults
from simplebench.benchmark_runner import BenchmarkRunner
from simplebench.exceptions import SimpleBenchTypeError, SimpleBenchValueError
from simplebench.reporters.reporter.options import ReporterOptions
from simplebench.validators import validate_positive_float, validate_positive_int, validate_string, validate_type
from simplebench.vcs import VCSInfo

from ._error_tags import _CaseErrorTag
from .function_runner import FunctionRunner


def validate_benchmark_id(benchmark_id: str) -> str:
    """Validate the benchmark_id for a benchmark case

    :param str benchmark_id: The benchmark ID to validate.
    :return str: The validated benchmark ID.
    :raises SimpleBenchTypeError: If the benchmark ID is not a string.
    :raises SimpleBenchValueError: If the benchmark ID is blank or empty.
    """
    return validate_string(
            benchmark_id, "benchmark_id",
            _CaseErrorTag.INVALID_BENCHMARK_ID_TYPE,
            _CaseErrorTag.INVALID_BENCHMARK_ID_VALUE,
            strip=True, allow_blank=False, allow_empty=False)


def validate_group(group: str) -> str:
    """Validate the group name for a benchmark case.

    The group name must be a non-blank, non-empty string.

    :param group: The group name to validate.
    :return str: The validated group name.
    :raises SimpleBenchTypeError: If the group is not a string.
    :raises SimpleBenchValueError: If the group is blank or empty.
    """
    return validate_string(
                group, "group",
                _CaseErrorTag.INVALID_GROUP_TYPE,
                _CaseErrorTag.INVALID_GROUP_VALUE,
                allow_blank=False, allow_empty=False, strip=True)


def validate_description(action: FunctionRunner, description: str | None = None) -> str:
    """Validate the description for a benchmark case.

    :param action: The action function of the benchmark case.
    :param description: The description of the benchmark case.
    :return str: The validated description.
    :raises SimpleBenchTypeError: If the description is not a string.
    :raises SimpleBenchValueError: If the description is blank or empty.
    """
    if description is None:
        description = action.__doc__ if action.__doc__ else '(no description)'
    return validate_string(
                    description, "description",
                    _CaseErrorTag.INVALID_DESCRIPTION_TYPE,
                    _CaseErrorTag.INVALID_DESCRIPTION_VALUE,
                    strip=True, allow_blank=False, allow_empty=False)


def validate_min_time(min_time: float) -> float:
    """Validate min_time for a benchmark case

    :param float min_time: The minimum time for the benchmark case.
    :return float: The validated minimum time.
    :raises SimpleBenchTypeError: If min_time is not a float.
    :raises SimpleBenchValueError: If min_time is not positive.
    """
    return validate_positive_float(
                min_time, "min_time",
                _CaseErrorTag.INVALID_MIN_TIME_TYPE,
                _CaseErrorTag.INVALID_MIN_TIME_VALUE)


def validate_max_time(max_time: float) -> float:
    """Validate max_time for a benchmark case

    :param float max_time: The maximum time for the benchmark case.
    :return float: The validated maximum time.
    :raises SimpleBenchTypeError: If max_time is not a float.
    :raises SimpleBenchValueError: If max_time is not positive.
    """
    return validate_positive_float(
                max_time, "max_time",
                _CaseErrorTag.INVALID_MAX_TIME_TYPE,
                _CaseErrorTag.INVALID_MAX_TIME_VALUE)


def validate_options(value: Iterable[ReporterOptions] | None) -> list[ReporterOptions]:
    """Validate the options list.

    :param Iterable[ReporterOptions] | None value: The options iterable to validate or None.
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


def validate_rounds(rounds: int | None) -> int | None:
    """Validate the number of rounds for a benchmark case.

    :param rounds: The number of rounds to validate.
    :return int | None: The validated number of rounds, or None if not provided.
    :raises SimpleBenchTypeError: If rounds is not an integer.
    :raises SimpleBenchValueError: If rounds is not positive.
    """
    if rounds is None:
        return None
    return validate_positive_int(
                        rounds, "rounds",
                        _CaseErrorTag.INVALID_ROUNDS_TYPE,
                        _CaseErrorTag.INVALID_ROUNDS_VALUE)


def validate_iterations(iterations: int) -> int:
    """Validate the number of iterations for a benchmark case.

    :param iterations: The number of iterations to validate.
    :return int: The validated number of iterations.
    :raises SimpleBenchTypeError: If iterations is not an integer.
    :raises SimpleBenchValueError: If iterations is not positive.
    """
    return validate_positive_int(
                        iterations, "iterations",
                        _CaseErrorTag.INVALID_ITERATIONS_TYPE,
                        _CaseErrorTag.INVALID_ITERATIONS_VALUE)


def validate_timeout(timeout: float | None, max_time: float) -> float:
    """Validate the timeout for a benchmark case.

    :param float | None timeout: The timeout to validate.
    :param float max_time: The maximum time for the benchmark case.
    :return float: The validated timeout.
    :raises SimpleBenchTypeError: If timeout is not a float.
    :raises SimpleBenchValueError: If timeout is not positive or less than max_time.
    """
    validate_max_time(max_time)
    if timeout is None:
        return max_time + defaults.DEFAULT_TIMEOUT_GRACE_PERIOD

    timeout_value = validate_positive_float(
                    timeout, "timeout",
                    _CaseErrorTag.INVALID_TIMEOUT_TYPE,
                    _CaseErrorTag.INVALID_TIMEOUT_VALUE)
    if timeout_value <= max_time:
        raise SimpleBenchValueError(
            f'Invalid timeout: {timeout_value}. Must be greater than max_time {max_time}.',
            tag=_CaseErrorTag.INVALID_TIMEOUT_LESS_EQUAL_MAX_TIME)
    return timeout_value


def validate_timer(timer: Callable[[], int] | None = None) -> Callable[[], int] | None:
    """Validate the timer for a benchmark case.

    :param timer: The timer to validate.
    :return float: The validated timer.
    :raises SimpleBenchTypeError: If timer is not a callable or does not return an int.
    """
    if timer is None:
        return None
    elif not callable(timer):
        raise SimpleBenchTypeError(
            f'Invalid timer: {type(timer)}. Must be a callable.',
            tag=_CaseErrorTag.INVALID_TIMER_NOT_CALLABLE)

    test_value = timer()
    if not isinstance(test_value, int):
        raise SimpleBenchTypeError(
            (f'Invalid timer: {type(timer)}. Timer callable must return an int, '
                f'got {type(test_value)}.'),
            tag=_CaseErrorTag.INVALID_TIMER_RETURN_TYPE)

    return timer


def validate_time_range(min_time: float, max_time: float) -> None:
    """Validate that min_time < max_time for the case.

    :param float min_time: The minimum time.
    :param float max_time: The maximum time.
    :raises SimpleBenchValueError: The min_time is greater than max_time.
    """
    if min_time > max_time:
        raise SimpleBenchValueError(
            f'Invalid time range: min_time {min_time} > max_time {max_time}.',
            tag=_CaseErrorTag.INVALID_TIME_RANGE)


def validate_title(action: FunctionRunner, title: str | None = None) -> str:
    """Validate the title for a benchmark case.

    :param action: The action function of the benchmark case.
    :param title: The title of the benchmark case.
    :return str: The validated title.
    :raises SimpleBenchTypeError: If the title is not a string.
    :raises SimpleBenchValueError: If the title is blank or empty.
    """
    title = action.__name__ if title is None else title  # type: ignore[attr-defined]
    return validate_string(
                title, "title",
                _CaseErrorTag.INVALID_TITLE_TYPE,
                _CaseErrorTag.INVALID_TITLE_VALUE,
                allow_blank=False, allow_empty=False, strip=True)


def validate_runners(runners: Sequence[type[BenchmarkRunner]] | None) -> list[type[BenchmarkRunner]]:
    """Validate the runner class.

    :param (Sequence[type[BenchmarkRunner]] | None) runners: The runner class types to validate or None.
    :return: The validated runner classes as a list or an empty list if not provided.
    :rtype: list[type[BenchmarkRunner]]
    :raises SimpleBenchTypeError: If `runners` is not either a sequence of `Runner` subclasses or a `None` value.
    """
    if runners is None:
        return []
    validated_runners: list[type[BenchmarkRunner]] = []
    for runner in runners:
        if not issubclass(runner, BenchmarkRunner):
            raise SimpleBenchTypeError(
                f'Invalid runner: {runner}. Must be a subclass of BenchmarkRunner.',
                tag=_CaseErrorTag.INVALID_RUNNER_NOT_SUBCLASS_OF_RUNNER)
        validated_runners.append(runner)
    return validated_runners


def validate_warmup_iterations(warmup_iterations: int) -> int:
    """Validate the number of warmup iterations for a benchmark case.

    :param warmup_iterations: The number of warmup iterations to validate.
    :return int: The validated number of warmup iterations.
    :raises SimpleBenchTypeError: If warmup_iterations is not an integer.
    :raises SimpleBenchValueError: If warmup_iterations is not positive.
    """
    return validate_positive_int(
                        warmup_iterations, "warmup_iterations",
                        _CaseErrorTag.INVALID_WARMUP_ITERATIONS_TYPE,
                        _CaseErrorTag.INVALID_WARMUP_ITERATIONS_VALUE)


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


def validate_action_signature(  # pylint: disable=too-many-branches  # noqa: C901
        action: FunctionRunner,
        kwargs_variations: dict[str, Any]) -> FunctionRunner:
    """Validate that action has correct signature.

    An action function must accept one of the two following formats for its parameters:

    **Two Parameters**
        - _bench: BenchmarkRunner
        - **kwargs: Arbitrary keyword arguments

    **Explicit Parameters**
        - _bench: BenchmarkRunner
        - any number of explicit parameters

    This is equivalent to the `ActionRunner` protocol.

    :param action: The action function to validate.
    :param kwargs_variations: The kwargs variations for the case.
    :return: The validated action function.
    :raises SimpleBenchTypeError: If the action is not callable or has an invalid signature or
        if the kwargs_variations is not a dictionary with valid keys or if the action signature
        does not match the kwargs_variations keys.
    """
    if not callable(action):
        raise SimpleBenchTypeError(
            f'Invalid action: {action}. Must be a callable.',
            tag=_CaseErrorTag.INVALID_ACTION_NOT_CALLABLE
            )

    # Resolve type hints to handle string annotations (from __future__ import annotations)
    try:
        type_hints = get_type_hints(action)
    except Exception:  # pylint: disable=broad-exception-caught
        # Fallback for callables where get_type_hints might fail (e.g. partials without globals)
        type_hints = {}

    action_signature = inspect.signature(action)
    kwargs_variations = validate_kwargs_variations(kwargs_variations)

    bench_param = action_signature.parameters.get('_bench')
    if bench_param is None:
        raise SimpleBenchTypeError(
            f'Invalid action: {action}. Must accept a "_bench" parameter.',
            tag=_CaseErrorTag.INVALID_ACTION_MISSING_BENCH_PARAMETER
            )
    if bench_param.annotation is inspect.Parameter.empty:
        raise SimpleBenchTypeError(
            f'Invalid action: {action}. "_bench" parameter must be annotated with BenchmarkRunner.',
            tag=_CaseErrorTag.INVALID_ACTION_BENCH_PARAMETER_NOT_ANNOTATED
            )

    # Use the resolved type hint if available, otherwise use the annotation from signature
    actual_annotation = type_hints.get('_bench', bench_param.annotation)

    if actual_annotation != BenchmarkRunner:
        raise SimpleBenchTypeError(
            f'Invalid action: {action}. "_bench" parameter must be of type BenchmarkRunner.',
            tag=_CaseErrorTag.INVALID_ACTION_BENCH_PARAMETER_WRONG_TYPE
            )

    # No arguments other than _bench
    if len(action_signature.parameters) == 1:
        return action

    # Two arguments: _bench and **kwargs
    if len(action_signature.parameters) == 2:
        # Check for **kwargs parameter
        kwargs_param = action_signature.parameters.get('kwargs')
        if kwargs_param is not None and kwargs_param.kind == inspect.Parameter.VAR_KEYWORD:
            return action

    # 2 or more arguments, _bench and explicit keyword-only parameters
    for param_name in action_signature.parameters:
        if param_name == '_bench':
            continue
        if param_name not in kwargs_variations:
            raise SimpleBenchTypeError(
                (f'Invalid action: {action}. Parameter "{param_name}" '
                    'not found in kwargs_variations.'),
                tag=_CaseErrorTag.INVALID_ACTION_PARAMETER_NOT_IN_KWARGS_VARIATIONS
                )
    for param_name in kwargs_variations:
        if param_name not in action_signature.parameters:
            raise SimpleBenchTypeError(
                (f'Invalid action: {action}. kwargs_variations key "{param_name}" '
                    'not found in action parameters.'),
                tag=_CaseErrorTag.INVALID_ACTION_KWARGS_VARIATIONS_KEY_NOT_IN_PARAMETERS
                )

    # All checks passed
    return action


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


def validate_vcs_info(vcs_info: VCSInfo | None) -> VCSInfo | None:
    """Validate the vcs_info argument.

    :param VCSInfo | None vcs_info: The vcs_info to validate or None.
    :return VCSInfo | None: The validated vcs_info or `None` if not provided.
    :raises SimpleBenchTypeError: If vcs_info is not of type VCSInfo.
    """
    return None if vcs_info is None else validate_type(
            vcs_info, VCSInfo, 'vcs_info', _CaseErrorTag.INVALID_VCS_INFO_ARG_TYPE)
