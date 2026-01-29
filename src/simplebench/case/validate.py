"""Validators for the simplebench.case package"""
import inspect
from collections.abc import Callable, Mapping
from typing import Any, get_type_hints

import simplebench.defaults as defaults
from simplebench.benchmark_runner import BenchmarkRunner
from simplebench.exceptions import SimpleBenchTypeError, SimpleBenchValueError
from simplebench.reporters.reporter.options import ReporterOptions
from simplebench.simplebench_types import (
    ElementCollection,
    KWArgsVariations,
    Mark,
    VariationCols,
    is_element_collection,
)
from simplebench.validators import validate_positive_float, validate_positive_int, validate_string, validate_type
from simplebench.vcs import VCSInfo

from ._error_tags import _CaseErrorTag
from .function_runner import FunctionRunner


def node(node_value: str | None) -> str | None:
    """Validate the node name for a benchmark case.

    The node name must be a non-blank, non-empty string.

    :param node_value: The node name to validate.
    :return str: The validated node name.
    :raises SimpleBenchTypeError: If the node is not a string.
    :raises SimpleBenchValueError: If the node is blank or empty.
    """
    if node_value is None:
       return None

    return validate_string(
        node_value,
        'node',
        _CaseErrorTag.INVALID_NODE,
        _CaseErrorTag.INVALID_NODE,
        allow_blank=True,
        allow_empty=True,
        strip=True,
    )

def benchmark_id(benchmark_id_value: str) -> str:
    """Validate the benchmark_id for a benchmark case

    :param str benchmark_id_value: The benchmark ID to validate.
    :return str: The validated benchmark ID.
    :raises SimpleBenchTypeError: If the benchmark ID is not a string.
    :raises SimpleBenchValueError: If the benchmark ID is blank or empty.
    """
    return validate_string(
        benchmark_id_value,
        'benchmark_id',
        _CaseErrorTag.INVALID_BENCHMARK_ID_TYPE,
        _CaseErrorTag.INVALID_BENCHMARK_ID_VALUE,
        strip=True,
        allow_blank=False,
        allow_empty=False,
    )


def group(group_value: str) -> str:
    """Validate the group name for a benchmark case.

    The group name must be a non-blank, non-empty string.

    :param group_value: The group name to validate.
    :return str: The validated group name.
    :raises SimpleBenchTypeError: If the group is not a string.
    :raises SimpleBenchValueError: If the group is blank or empty.
    """
    return validate_string(
        group_value,
        'group',
        _CaseErrorTag.INVALID_GROUP_TYPE,
        _CaseErrorTag.INVALID_GROUP_VALUE,
        allow_blank=False,
        allow_empty=False,
        strip=True,
    )


def description(action_func: FunctionRunner, description_value: str | None = None) -> str:
    """Validate the description for a benchmark case.

    :param FunctionRunner action_func: The action function of the benchmark case.
    :param str | None description_value: The description of the benchmark case.
    :return str: The validated description.
    :raises SimpleBenchTypeError: If the value is not a string.
    :raises SimpleBenchValueError: If the va;ue is blank or empty.
    """
    if description_value is None:
        description_value = action_func.__doc__ if action_func.__doc__ else '(no description)'
    return validate_string(
        description_value,
        'description',
        _CaseErrorTag.INVALID_DESCRIPTION_TYPE,
        _CaseErrorTag.INVALID_DESCRIPTION_VALUE,
        strip=True,
        allow_blank=False,
        allow_empty=False,
    )


def min_time(min_time_value: float) -> float:
    """Validate min_time for a benchmark case

    :param float min_time_value: The minimum time for the benchmark case.
    :return float: The validated minimum time.
    :raises SimpleBenchTypeError: If value is not a float.
    :raises SimpleBenchValueError: If value is not positive.
    """
    return validate_positive_float(
        min_time_value, 'min_time', _CaseErrorTag.INVALID_MIN_TIME_TYPE, _CaseErrorTag.INVALID_MIN_TIME_VALUE
    )


def max_time(max_time_value: float) -> float:
    """Validate max_time for a benchmark case

    :param float max_time_value: The maximum time for the benchmark case.
    :return float: The validated maximum time.
    :raises SimpleBenchTypeError: If value is not a float.
    :raises SimpleBenchValueError: If value is not positive.
    """
    return validate_positive_float(
        max_time_value, 'max_time', _CaseErrorTag.INVALID_MAX_TIME_TYPE, _CaseErrorTag.INVALID_MAX_TIME_VALUE
    )


def options(options_value: ElementCollection[ReporterOptions] | None) -> tuple[ReporterOptions, ...]:
    """Validate the options list.

    :param ElementCollection[ReporterOptions] | None options_value: The options iterable to validate or None.
    :return: A shallow copy of the validated options as a list or an empty list if not provided.
    :rtype: tuple[ReporterOptions, ...]
    :raises SimpleBenchTypeError: If options is not an ElementCollection or if any entry is not a ReporterOption.
    """
    if options_value is None:
        return tuple([])
    if not is_element_collection(options_value):
        raise SimpleBenchTypeError(
            f'Invalid options: {options_value}. Must be an ElementCollection.',
            tag=_CaseErrorTag.INVALID_OPTIONS_NOT_ELEMENT_COLLECTION
        )
    options_list: list[ReporterOptions] = list(options_value)
    for option in options_list:
        if not isinstance(option, ReporterOptions):
            raise SimpleBenchTypeError(
                f'Invalid option: {option}. Must be of type ReporterOption or a sub-class.',
                tag=_CaseErrorTag.INVALID_OPTIONS_ENTRY_NOT_REPORTER_OPTION,
            )
    return tuple(options_list)


def rounds(rounds_value: int | None) -> int | None:
    """Validate the number of rounds for a benchmark case.

    :param rounds_value: The number of rounds to validate.
    :return int | None: The validated number of rounds, or None if not provided.
    :raises SimpleBenchTypeError: If rounds is not an integer.
    :raises SimpleBenchValueError: If rounds is not positive.
    """
    if rounds_value is None:
        return None
    return validate_positive_int(
        rounds_value, 'rounds', _CaseErrorTag.INVALID_ROUNDS_TYPE, _CaseErrorTag.INVALID_ROUNDS_VALUE
    )


def iterations(iterations_value: int) -> int:
    """Validate the number of iterations for a benchmark case.

    :param int value: The number of iterations to validate.
    :return int: The validated number of iterations.
    :raises SimpleBenchTypeError: If iterations is not an integer.
    :raises SimpleBenchValueError: If iterations is not positive.
    """
    return validate_positive_int(
        iterations_value, 'iterations', _CaseErrorTag.INVALID_ITERATIONS_TYPE, _CaseErrorTag.INVALID_ITERATIONS_VALUE
    )


def timeout(timeout_value: float | None, max_time_value: float) -> float:
    """Validate the timeout for a benchmark case.

    :param float | None timeout_value: The timeout to validate.
    :param float max_time_value: The maximum time for the benchmark case.
    :return float: The validated timeout.
    :raises SimpleBenchTypeError: If timeout is not a float.
    :raises SimpleBenchValueError: If timeout is not positive or less than max_time.
    """
    max_time(max_time_value)
    if timeout_value is None:
        return defaults.DEFAULT_TIMEOUT_GRACE_PERIOD

    timeout_value = validate_positive_float(
        timeout_value, 'timeout', _CaseErrorTag.INVALID_TIMEOUT_TYPE, _CaseErrorTag.INVALID_TIMEOUT_VALUE
    )
    if timeout_value <= max_time_value:
        raise SimpleBenchValueError(
            f'Invalid timeout: {timeout_value}. Must be greater than max_time {max_time_value}.',
            tag=_CaseErrorTag.INVALID_TIMEOUT_LESS_EQUAL_MAX_TIME,
        )
    return timeout_value


def timer(timer_func: Callable[[], int] | None = None, field_name: str = 'timer') -> Callable[[], int] | None:
    """Validate the timer for a benchmark case.

    :param timer_func: (default = :obj:`None`) The timer function to validate.
    :type timer_func: Callable[[], int] | None
    :param field_name: (default = 'timer') The name of the field being validated (for error messages).
    :type field_name: str
    :return: The validated timer function or :obj:`None` if not provided.
    :rtype: Callable[[], int] | None
    :raises SimpleBenchTypeError: If timer function is not a callable or does not return an int.
    """
    if not isinstance(field_name, str):
        raise SimpleBenchTypeError(
            f'Invalid field_name: {field_name}. Must be of type str.',
            tag=_CaseErrorTag.INVALID_TIMER_FIELD_NAME_TYPE
        )
    if timer_func is None:
        return None
    elif not callable(timer_func):
        raise SimpleBenchTypeError(
            f'Invalid {field_name} timer: {type(timer_func)}. Must be a callable.',
            tag=_CaseErrorTag.INVALID_TIMER_NOT_CALLABLE
        )

    test_value = timer_func()
    if not isinstance(test_value, int):
        raise SimpleBenchTypeError(
            (f'Invalid {field_name} timer: {type(timer_func)}. Timer callable must '
             f'return an int, got {type(test_value)}.'),
            tag=_CaseErrorTag.INVALID_TIMER_RETURN_TYPE,
        )

    return timer_func


def time_range(min_value: float, max_value: float) -> None:
    """Validate that min_time < max_time for the case.

    :param float min_value: The minimum time.
    :param float max_value: The maximum time.
    :raises SimpleBenchValueError: The min_value is greater than max_value.
    """
    if min_value > max_value:
        raise SimpleBenchValueError(
            f'Invalid time range: min_value {min_value} > max_value {max_value}.', tag=_CaseErrorTag.INVALID_TIME_RANGE
        )


def title(action_func: FunctionRunner, title_value: str | None = None) -> str:
    """Validate the title for a benchmark case.

    :param action: The action function of the benchmark case.
    :param value: The title of the benchmark case.
    :return str: The validated title.
    :raises SimpleBenchTypeError: If the title is not a string.
    :raises SimpleBenchValueError: If the title is blank or empty.
    """
    title_value = action_func.__name__ if title_value is None else title_value  # type: ignore[attr-defined]
    return validate_string(
        title_value,
        'title',
        _CaseErrorTag.INVALID_TITLE_TYPE,
        _CaseErrorTag.INVALID_TITLE_VALUE,
        allow_blank=False,
        allow_empty=False,
        strip=True,
    )


def runners(runner_types: ElementCollection[type[BenchmarkRunner]] | None) -> tuple[type[BenchmarkRunner], ...]:
    """Validate the runner class types.

    :param runner_types: The runner class types to validate or None.
    :type runner_types: ElementCollection[type[BenchmarkRunner]] | None
    :return: The validated runner class types as a tuple. If None, returns an empty tuple.
    :rtype: tuple[type[BenchmarkRunner], ...]
    :raises SimpleBenchTypeError: If `runners` is not either an :class:`ElementCollection`:
        of :class:`BenchmarkRunner` subclass types or `None`.
    """
    if runner_types is None:
        return ()

    if not is_element_collection(runner_types):
        raise SimpleBenchTypeError(
            f'Invalid runners: {runner_types}. Must be an ElementCollection.',
            tag=_CaseErrorTag.INVALID_RUNNERS_NOT_ELEMENT_COLLECTION,
        )

    validated_runners: list[type[BenchmarkRunner]] = []
    for runner in runner_types:
        if not issubclass(runner, BenchmarkRunner):
            raise SimpleBenchTypeError(
                f'Invalid runner: {runner}. Must be a subclass of BenchmarkRunner.',
                tag=_CaseErrorTag.INVALID_RUNNER_NOT_SUBCLASS_OF_RUNNER,
            )
        validated_runners.append(runner)
    return tuple(validated_runners)


def warmup_iterations(warmup_iterations_value: int) -> int:
    """Validate the number of warmup iterations for a benchmark case.

    :param int warmup_iterations_value: The number of warmup iterations to validate.
    :return int: The validated number of warmup iterations.
    :raises SimpleBenchTypeError: If warmup_iterations is not an integer.
    :raises SimpleBenchValueError: If warmup_iterations is not positive.
    """
    return validate_positive_int(
        warmup_iterations_value,
        'warmup_iterations',
        _CaseErrorTag.INVALID_WARMUP_ITERATIONS_TYPE,
        _CaseErrorTag.INVALID_WARMUP_ITERATIONS_VALUE,
    )


def kwargs_variations(kwargs_variations_value: Mapping[str, ElementCollection[Any]] | None
                      ) -> KWArgsVariations:
    """Validate the kwargs_variations dictionary.

    Validates that the kwargs_variations is a Mapping where each key is a string
    that is a valid Python identifier, and each value is a non-empty ElementCollection of values.

    A shallow copy of the validated Mapping is performed and each :class:`ElementCollection` is
    converted to a tuple of :class:`Mark` instances. Existing :class:`Mark` instances are preserved.

    Values that are not :class:`Mark` instances are converted to :class:`Mark` instances
    with the name set to the string representation of the value and the value
    set to the original value. If the value's string representation is not stringifiable,
    an exception may be raised during this conversion. This is intentional to ensure
    that all values can be represented as strings for reporting purposes.

    It is the responsibility of the caller to ensure that the values in the ElementCollections
    are of types that can be meaningfully converted to strings - using :class:`Mark` instances
    directly is recommended for complex types.

    If a value cannot be converted to a string, a :class:`SimpleBenchTypeError` is raised.

    :param kwargs_variations_value: (default = {}) The kwargs_variations Mapping to validate.
    :type kwargs_variations_value: Mapping[str, ElementCollection[Any]] | None
    :return: A shallow copy of the validated kwargs_variations dictionary or {} if not provided.
        The keys are strings that are valid Python identifiers, and the values are non-empty tuples.
        The tuples may contain any type of values.
    :rtype: MappingProxyType[str, tuple[Mark, ...]]
    :raises SimpleBenchTypeError: If the kwargs_variations_value is not a Mapping.
    :raises SimpleBenchTypeError: If any key is not a string.
    :raises SimpleBenchValueError: If any key is not a valid `Python identifier <https://docs.python.org/3/library/stdtypes.html#str.isidentifier>`_.
    :raises SimpleBenchTypeError: If any value is not an ElementCollection.
    :raises SimpleBenchValueError: If the value is an empty ElementCollection.
    :raises SimpleBenchTypeError: If any value cannot be converted to a string for a Mark label.
    """
    if kwargs_variations_value is None:
        return KWArgsVariations({})

    if not isinstance(kwargs_variations_value, Mapping):
        raise SimpleBenchTypeError(
            f'Invalid kwargs_variations: {kwargs_variations_value}. Must be a Mapping.',
            tag=_CaseErrorTag.INVALID_KWARGS_VARIATIONS_NOT_MAPPING,
        )
    validated_dict = {}
    for key, kw_value in kwargs_variations_value.items():
        if not is_element_collection(kw_value):
            raise SimpleBenchTypeError(
                f'Invalid kwargs_variations entry value for entry "{key}": {kw_value}. '
                'Values must be an ElementCollection.',
                tag=_CaseErrorTag.INVALID_KWARGS_VARIATIONS_ENTRY_VALUE_NOT_ELEMENT_COLLECTION,
            )
        if not kw_value:
            raise SimpleBenchValueError(
                (f'Invalid kwargs_variations entry value for entry "{key}": {kw_value}. '
                 'Values cannot be empty ElementCollections.'),
                tag=_CaseErrorTag.INVALID_KWARGS_VARIATIONS_ENTRY_VALUE_EMPTY_LIST,
            )

        if not isinstance(key, str):
            raise SimpleBenchTypeError(
                f'Invalid kwargs_variations entry key: {key}. Keys must be of type str.',
                tag=_CaseErrorTag.INVALID_KWARGS_VARIATIONS_ENTRY_KEY_TYPE,
            )
        if not key.isidentifier():
            raise SimpleBenchValueError(
                f'Invalid kwargs_variations entry key: {key}. Keys must be valid Python identifiers.',
                tag=_CaseErrorTag.INVALID_KWARGS_VARIATIONS_ENTRY_KEY_NOT_IDENTIFIER,
            )

        try:
            # Convert each ElementCollection to a sorted tuple of Mark instances as needed
            # By sorting here, we ensure consistent ordering for reporting later
            marks_list: list[Mark] = []
            for item in kw_value:
                if isinstance(item, Mark):
                    marks_list.append(item)
                else:
                    marks_list.append(Mark(label=str(item), value=item))
            validated_dict[key] = tuple(sorted(marks_list))
        except Exception as exc:
            raise SimpleBenchTypeError(
                f'Invalid kwargs_variations entry value for entry "{key}": Unable to stringify values. '
                'All values must be stringifiable for Mark labels. If using complex types, consider '
                'using Mark instances directly to apply labels.',
                tag=_CaseErrorTag.INVALID_KWARGS_VARIATIONS_ENTRY_VALUE_CANNOT_CONVERT_TO_STRING,
            ) from exc
    return KWArgsVariations(validated_dict)


def action_signature(action_func: FunctionRunner,
                     kwargs_variations_value: Mapping[str, Any]) -> FunctionRunner:
    """Validate that action has correct signature.

    An action function must accept one of the two following formats for its parameters:

    **Two Parameters**
        - _bench: BenchmarkRunner
        - **kwargs: Arbitrary keyword arguments

    **Explicit Parameters**
        - _bench: BenchmarkRunner
        - any number of explicit parameters

    This is equivalent to the `FunctionRunner` protocol.

    :param action_func: The action function to validate.
    :type action_func: FunctionRunner
    :param kwargs_variations_value: The kwargs variations for the case.
    :type kwargs_variations_value: Mapping[str, Any]
    :return FunctionRunner: The validated action function.
    :raises SimpleBenchTypeError: If the action is not callable or has an invalid signature or
        if the kwargs_variations is not a dictionary with valid keys or if the action signature
        does not match the kwargs_variations keys.
    """
    if not callable(action_func):
        raise SimpleBenchTypeError(
            f'Invalid action: {action_func}. Must be a callable.', tag=_CaseErrorTag.INVALID_ACTION_NOT_CALLABLE
        )

    # Resolve type hints to handle string annotations (from __future__ import annotations)
    try:
        type_hints = get_type_hints(action_func)
    except Exception:  # pylint: disable=broad-exception-caught
        # Fallback for callables where get_type_hints might fail (e.g. partials without globals)
        type_hints = {}

    action_sig = inspect.signature(action_func)
    kwargs_variations_value = kwargs_variations(kwargs_variations_value)

    bench_param = action_sig.parameters.get('_bench')
    if bench_param is None:
        raise SimpleBenchTypeError(
            f'Invalid action: {action_func}. Must accept a "_bench" parameter.',
            tag=_CaseErrorTag.INVALID_ACTION_MISSING_BENCH_PARAMETER,
        )
    if bench_param.annotation is inspect.Parameter.empty:
        raise SimpleBenchTypeError(
            f'Invalid action: {action_func}. "_bench" parameter must be annotated with BenchmarkRunner.',
            tag=_CaseErrorTag.INVALID_ACTION_BENCH_PARAMETER_NOT_ANNOTATED,
        )

    # Use the resolved type hint if available, otherwise use the annotation from signature
    actual_annotation = type_hints.get('_bench', bench_param.annotation)

    if actual_annotation != BenchmarkRunner:
        raise SimpleBenchTypeError(
            f'Invalid action: {action_func}. "_bench" parameter must be of type BenchmarkRunner.',
            tag=_CaseErrorTag.INVALID_ACTION_BENCH_PARAMETER_WRONG_TYPE,
        )

    # No arguments other than _bench
    if len(action_sig.parameters) == 1:
        return action_func

    # Two arguments: _bench and **kwargs
    # If **kwargs is present, no further checks are performed.
    if len(action_sig.parameters) == 2:
        # Check for **kwargs parameter
        kwargs_param = action_sig.parameters.get('kwargs')
        if kwargs_param is not None and kwargs_param.kind == inspect.Parameter.VAR_KEYWORD:
            return action_func

    # 2 or more arguments, _bench and explicit keyword parameters
    # It does not check parameter types for explicit parameters beyond _bench
    # and does not handle optional parameters. If optional parameters are needed,
    # the action should use the **kwargs format or pass default values explicitly.
    for param_name in action_sig.parameters:
        if param_name == '_bench':
            continue
        if param_name not in kwargs_variations_value:
            raise SimpleBenchTypeError(
                (f'Invalid action: {action_func}. Parameter "{param_name}" not '
                 f'found in kwargs_variations.: {kwargs_variations_value!r}'),
                tag=_CaseErrorTag.INVALID_ACTION_PARAMETER_NOT_IN_KWARGS_VARIATIONS,
            )
    for param_name in kwargs_variations_value:
        if param_name not in action_sig.parameters:
            raise SimpleBenchTypeError(
                (
                    f'Invalid action: {action_func}. kwargs_variations key "{param_name}" '
                    'not found in action parameters.'
                ),
                tag=_CaseErrorTag.INVALID_ACTION_KWARGS_VARIATIONS_KEY_NOT_IN_PARAMETERS,
            )

    # All checks passed
    return action_func


def variation_cols(
    variation_cols_value: Mapping[str, str] | None,
    kwargs_variations_value: KWArgsVariations,
) -> VariationCols:
    """Validate the variation_cols dictionary.

    :param variation_cols_value: The variation_cols dictionary to validate or None.
    :type variation_cols_value: Mapping[str, str] | None
    :param kwargs_variations_value: The kwargs_variations dictionary to validate against.
    :type kwargs_variations_value: KWArgsVariations
    :return: A shallow copy of the validated variation_cols dictionary or {} if not provided.
        Each key is a keyword argument name from `kwargs_variations_value`, and each value is a
        non-blank string to be used as the column label for that argument in reports.
    :rtype: MappingProxyType[str, str]
    :raises SimpleBenchTypeError: If the variation_cols is not a Mapping or if any key or
        value is not a string.
    :raises SimpleBenchValueError: If any key is not found in `kwargs_variations_value` or if any
        value is a blank string.
    """
    if variation_cols_value is None:
        return VariationCols({})

    if not isinstance(variation_cols_value, Mapping):
        raise SimpleBenchTypeError(
            f'Invalid variation_cols: {variation_cols_value}. Must be a mapping.',
            tag=_CaseErrorTag.INVALID_VARIATION_COLS_NOT_MAPPING,
        )
    validated_dict: dict[str, str] = {}
    for key, vc_value in variation_cols_value.items():
        if key not in kwargs_variations_value:
            raise SimpleBenchValueError(
                f'Invalid variation_cols entry key: {key}. Key not found in kwargs_variations.',
                tag=_CaseErrorTag.INVALID_VARIATION_COLS_ENTRY_KEY_NOT_IN_KWARGS,
            )
        if not isinstance(vc_value, str):
            raise SimpleBenchTypeError(
                f'Invalid variation_cols entry value for entry "{key}": "{vc_value}". Values must be of type str.',
                tag=_CaseErrorTag.INVALID_VARIATION_COLS_ENTRY_VALUE_NOT_STRING,
            )
        stripped_value = vc_value.strip()
        if stripped_value == '':
            raise SimpleBenchValueError(
                f'Invalid variation_cols entry value: "{vc_value}". Values cannot be blank strings.',
                tag=_CaseErrorTag.INVALID_VARIATION_COLS_ENTRY_VALUE_BLANK,
            )
        validated_dict[key] = stripped_value
    return VariationCols(validated_dict)


def vcs_info(vcs_info_value: VCSInfo | None) -> VCSInfo | None:
    """Validate the vcs_info argument.

    :param VCSInfo | None vcs_info: The vcs_info to validate or None.
    :return VCSInfo | None: The validated vcs_info or `None` if not provided.
    :raises SimpleBenchTypeError: If vcs_info is not of type VCSInfo.
    """
    return (
        None
        if vcs_info_value is None
        else validate_type(vcs_info_value, VCSInfo, 'vcs_info', _CaseErrorTag.INVALID_VCS_INFO_ARG_TYPE)
    )

def max_greater_than_min(min_time: float, max_time: float) -> None:
    """Validate that max_time is greater than or equal to min_time.

    :param min_time: The minimum time.
    :param max_time: The maximum time.
    :raises SimpleBenchValueError: If max_time is not greater than or equal to min_time.
    """
    if max_time < min_time:
        raise SimpleBenchValueError(
            "The 'max_time' parameter to the @benchmark decorator must be greater than or equal to 'min_time'.",
            tag=_CaseErrorTag.BENCHMARK_MAX_TIME_LESS_THAN_MIN_TIME)



def n(value: int | float) -> float:
    """Validate benchmark 'n' parameter.

    :param value: The 'n' value to validate.
    :type value: int | float
    :returns: The validated 'n' value.
    :rtype: int | float
    :raises SimpleBenchTypeError: If the 'n' value is not an int or float.
    :raises SimpleBenchValueError: If the 'n' value is not positive.
    """
    if not isinstance(value, (int, float)):
        raise SimpleBenchTypeError(
            f"The 'n' parameter to the @benchmark decorator must be an int or float, got {type(value).__name__}.",
            tag=_CaseErrorTag.BENCHMARK_N_TYPE,
        )
    if value <= 0:
        raise SimpleBenchValueError(
            "The 'n' parameter to the @benchmark decorator must be a positive integer or float value.",
            tag=_CaseErrorTag.BENCHMARK_N_VALUE,
        )
    return float(value)
