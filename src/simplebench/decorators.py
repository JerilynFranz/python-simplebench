# -*- coding: utf-8 -*-
"""Decorators for simplifying benchmark case creation."""
from __future__ import annotations
from functools import wraps
from typing import Any, Callable, TYPE_CHECKING

from .case import Case
from .constants import DEFAULT_WARMUP_ITERATIONS
from .runners import SimpleRunner
from .exceptions import SimpleBenchTypeError, SimpleBenchValueError, ErrorTag

if TYPE_CHECKING:
    from .reporters.reporter_option import ReporterOption

# A global registry to hold benchmark cases created by the decorator.
_DECORATOR_CASES: list[Case] = []
"""List to store benchmark cases registered via the @benchmark decorator."""


def benchmark(
    *,
    group: str,
    title: str | None = None,
    description: str | None = None,
    iterations: int | None = None,
    warmup_iterations: int = DEFAULT_WARMUP_ITERATIONS,
    min_time: float | None = None,
    max_time: float | None = None,
    variation_cols: dict[str, str] | None = None,
    kwargs_variations: dict[str, list[Any]] | None = None,
    options: list[ReporterOption] | None = None,
    n: int = 1,
    use_field_for_n: str | None = None
) -> Callable:
    """
    A decorator to register a function as a benchmark case.

    This simplifies creating a `Case` by wrapping the decorated function.
    The decorated function should contain the code to be benchmarked.

    It is important to note that the decorated function will be called
    within the context of a `SimpleRunner.run()` call, which means it
    should not handle its own timing or iterations.

    The args provided to the decorator are used to create a `Case` instance,
    which is then added to a global registry. The original function is returned
    unmodified, allowing it to be called directly if needed.

    The arguments to the decorator are largely the same as those for `Case`, with
    the exception of `action`, which is replaced by the decorated function.

    n is included to allow weighting of the benchmark case when using
    runners that support it.

    Args:
        group (str): The group name for the benchmark case.
        title (str | None): The title of the benchmark case. Defaults to the function name.
        description (str | None): A description for the case. Defaults to the function's docstring.
        iterations (int | None): The minimum number of iterations to run for the benchmark.
                If None, uses the Case default. See `Case.iterations`.
        warmup_iterations (int): The number of warmup iterations to run before the benchmark.
                See `Case.warmup_iterations`.
        min_time (float | None): The minimum time in seconds to run the benchmark.
                If None, uses the Case default. See `Case.min_time`.
        max_time (float | None): The maximum time in seconds to run the benchmark.
                If None, uses the Case default. See `Case.max_time`.
        variation_cols (dict[str, str] | None): See `Case.variation_cols`.
        kwargs_variations (dict[str, list[Any]] | None): See `Case.kwargs_variations`.
        options (list[ReporterOption] | None): See `Case.options`.
        n (int, default=1): The 'n' weighting of the benchmark case.
        use_field_for_n (str | None): If provided, use the value of this field from kwargs_variations
            to set 'n' dynamically for each variation.

    Returns:
        A decorator that registers the function and returns it unmodified.
    """
    if not isinstance(group, str):
        raise SimpleBenchTypeError("The 'group' parameter to the @benchmark decorator must be a string.",
                                   tag=ErrorTag.BENCHMARK_DECORATOR_GROUP_TYPE)

    if group.strip() == '':
        raise SimpleBenchValueError("The 'group' parameter to the @benchmark decorator must be a non-empty string.",
                                    tag=ErrorTag.BENCHMARK_DECORATOR_GROUP_VALUE)

    if title is not None and not isinstance(title, str):
        raise SimpleBenchTypeError("The 'title' parameter to the @benchmark decorator must be a string if passed.",
                                   tag=ErrorTag.BENCHMARK_DECORATOR_TITLE_TYPE)
    if title is not None and title.strip() == '':
        raise SimpleBenchValueError("The 'title' parameter to the @benchmark decorator must be "
                                    "a non-empty string if passed.",
                                    tag=ErrorTag.BENCHMARK_DECORATOR_TITLE_VALUE)

    if description is not None and not isinstance(description, str):
        raise SimpleBenchTypeError("The 'description' parameter to the @benchmark decorator must be "
                                   "a string if passed.",
                                   tag=ErrorTag.BENCHMARK_DECORATOR_DESCRIPTION_TYPE)
    if description is not None and description.strip() == '':
        raise SimpleBenchValueError("The 'description' parameter to the @benchmark decorator must be "
                                    "a non-empty string if passed.",
                                    tag=ErrorTag.BENCHMARK_DECORATOR_DESCRIPTION_VALUE)
    if not isinstance(iterations, int) and iterations is not None:
        raise SimpleBenchTypeError("The 'iterations' parameter to the @benchmark decorator must be an integer.",
                                   tag=ErrorTag.BENCHMARK_DECORATOR_ITERATIONS_TYPE)

    if iterations is not None and iterations <= 0:
        raise SimpleBenchValueError(
            "The 'iterations' parameter to the @benchmark decorator must be a positive integer.",
            tag=ErrorTag.BENCHMARK_DECORATOR_ITERATIONS_VALUE)

    if not isinstance(warmup_iterations, int):
        raise SimpleBenchTypeError("The 'warmup_iterations' parameter to the @benchmark decorator must be an integer.",
                                   tag=ErrorTag.BENCHMARK_DECORATOR_WARMUP_ITERATIONS_TYPE)

    if warmup_iterations < 0:
        raise SimpleBenchValueError(
            "The 'warmup_iterations' parameter to the @benchmark decorator must be a non-negative integer.",
            tag=ErrorTag.BENCHMARK_DECORATOR_WARMUP_ITERATIONS_VALUE)

    if not isinstance(min_time, (float, int)) and min_time is not None:
        raise SimpleBenchTypeError("The 'min_time' parameter to the @benchmark decorator must be a float or int.",
                                   tag=ErrorTag.BENCHMARK_DECORATOR_MIN_TIME_TYPE)

    if not isinstance(max_time, (float, int)) and max_time is not None:
        raise SimpleBenchTypeError("The 'max_time' parameter to the @benchmark decorator must be a float or int.",
                                   tag=ErrorTag.BENCHMARK_DECORATOR_MAX_TIME_TYPE)

    if not isinstance(variation_cols, dict) and variation_cols is not None:
        raise SimpleBenchTypeError("The 'variation_cols' parameter to the @benchmark decorator must be a dictionary.",
                                   tag=ErrorTag.BENCHMARK_DECORATOR_VARIATION_COLS_TYPE)

    if not isinstance(options, list) and options is not None:
        raise SimpleBenchTypeError("The 'options' parameter to the @benchmark decorator must be a list.",
                                   tag=ErrorTag.BENCHMARK_DECORATOR_OPTIONS_TYPE)

    if not isinstance(n, int):
        raise SimpleBenchTypeError("The 'n' parameter to the @benchmark decorator must be an integer.",
                                   tag=ErrorTag.BENCHMARK_DECORATOR_N_TYPE)

    if n <= 0:
        raise SimpleBenchValueError("The 'n' parameter to the @benchmark decorator must be a positive integer.",
                                    tag=ErrorTag.BENCHMARK_DECORATOR_N_VALUE)

    if not isinstance(use_field_for_n, str) and use_field_for_n is not None:
        raise SimpleBenchTypeError("The 'use_field_for_n' parameter to the @benchmark decorator "
                                   "must be a string if passed.",
                                   tag=ErrorTag.BENCHMARK_DECORATOR_USE_FIELD_FOR_N_TYPE)

    if use_field_for_n is not None and use_field_for_n.strip() == '':
        raise SimpleBenchValueError("The 'use_field_for_n' parameter to the @benchmark decorator "
                                    "must be a non-empty string if passed.",
                                    tag=ErrorTag.BENCHMARK_DECORATOR_USE_FIELD_FOR_N_VALUE)
    if use_field_for_n is not None and kwargs_variations is None:
        raise SimpleBenchTypeError("The 'use_field_for_n' parameter to the @benchmark decorator requires "
                                   "that 'kwargs_variations' also be provided.",
                                   tag=ErrorTag.BENCHMARK_DECORATOR_USE_FIELD_FOR_N_KWARGS_VARIATIONS)

    if kwargs_variations is not None:
        if not isinstance(kwargs_variations, dict):
            raise SimpleBenchTypeError("The 'kwargs_variations' parameter to the @benchmark decorator "
                                       "must be a dictionary.",
                                       tag=ErrorTag.BENCHMARK_DECORATOR_KWARGS_VARIATIONS_TYPE)
        for key, values in kwargs_variations.items():
            if not isinstance(key, str):
                raise SimpleBenchTypeError(
                    "The keys in the 'kwargs_variations' parameter to the @benchmark decorator must be strings.",
                    tag=ErrorTag.BENCHMARK_DECORATOR_KWARGS_VARIATIONS_KEY_TYPE)
            if not isinstance(values, list):
                raise SimpleBenchTypeError(
                    f"The values for the '{key}' entry in the 'kwargs_variations' parameter "
                    "to the @benchmark decorator must be in a list.",
                    tag=ErrorTag.BENCHMARK_DECORATOR_KWARGS_VARIATIONS_VALUE_TYPE)
            if len(values) == 0:
                raise SimpleBenchValueError(
                    f"The values list for the '{key}' entry in the 'kwargs_variations' parameter "
                    "to the @benchmark decorator cannot be an empty list.",
                    tag=ErrorTag.BENCHMARK_DECORATOR_KWARGS_VARIATIONS_VALUE_VALUE)

    if (isinstance(use_field_for_n, str) and isinstance(kwargs_variations, dict)):
        if use_field_for_n not in kwargs_variations:
            raise SimpleBenchTypeError("The 'use_field_for_n' parameter to the @benchmark decorator must "
                                       f"match one of the kwargs_variations keys: {list(kwargs_variations.keys())}",
                                       tag=ErrorTag.BENCHMARK_DECORATOR_USE_FIELD_FOR_N_KWARGS_VARIATIONS)
        if not all(isinstance(v, int) and v > 0 for v in kwargs_variations[use_field_for_n]):
            raise SimpleBenchValueError(f"The values for the '{use_field_for_n}' entry in 'kwargs_variations' "
                                        "must all be positive integers when used with 'use_field_for_n'.",
                                        tag=ErrorTag.BENCHMARK_DECORATOR_USE_FIELD_FOR_N_INVALID_VALUE)

    if isinstance(variation_cols, dict):
        for key, value in variation_cols.items():
            if not isinstance(key, str):
                raise SimpleBenchTypeError("The keys in the 'variation_cols' dictionary must be strings.",
                                           tag=ErrorTag.BENCHMARK_DECORATOR_VARIATION_COLS_KEY_TYPE)
            if not isinstance(value, str):
                raise SimpleBenchTypeError("The values in the 'variation_cols' dictionary must be strings.",
                                           tag=ErrorTag.BENCHMARK_DECORATOR_VARIATION_COLS_VALUE_TYPE)
            if key.strip() == '':
                raise SimpleBenchValueError("The keys in the 'variation_cols' dictionary must be non-empty strings.",
                                            tag=ErrorTag.BENCHMARK_DECORATOR_VARIATION_COLS_KEY_VALUE)
            if value.strip() == '':
                raise SimpleBenchValueError("The values in the 'variation_cols' dictionary must be non-empty strings.",
                                            tag=ErrorTag.BENCHMARK_DECORATOR_VARIATION_COLS_VALUE_VALUE)
            if kwargs_variations is None or key not in kwargs_variations:
                raise SimpleBenchTypeError(f"The key '{key}' in 'variation_cols' must also be present in "
                                           "'kwargs_variations'.",
                                           tag=ErrorTag.BENCHMARK_DECORATOR_VARIATION_COLS_KWARGS_VARIATIONS_MISMATCH)

    def decorator(func):
        """The actual decorator that wraps the user's function."""
        @wraps(func)
        def case_action_wrapper(_runner: SimpleRunner, /,  **kwargs) -> Any:
            """
            This wrapper becomes the `action` for the `Case`.
            It calls the user's decorated function inside `runner.run()`.

            Args:
                _runner (SimpleRunner): The runner executing the benchmark.
                **kwargs: Any keyword arguments from `kwargs_variations`.
            """
            # The designated use_field_for_n field will always be present
            # in kwargs if specified due to prior validation.
            n_for_run = n if use_field_for_n is None else kwargs.get(use_field_for_n)
            return _runner.run(action=func, n=n_for_run, kwargs=kwargs)

        # Create the Case instance, using sensible defaults from the function.
        case_kwargs = {
            'group': group,
            'title': title or func.__name__,
            'action': case_action_wrapper,
            'description': description or func.__doc__ or '(no description)',
            'variation_cols': variation_cols or {},
            'kwargs_variations': kwargs_variations or {},
            'options': options or [],
            '_decoration': True
        }
        if iterations is not None:
            case_kwargs['iterations'] = iterations
        if min_time is not None:
            case_kwargs['min_time'] = min_time
        if max_time is not None:
            case_kwargs['max_time'] = max_time

        case = Case(**case_kwargs)

        # Add the created case to the global registry.
        _DECORATOR_CASES.append(case)

        # Return the original function so it remains callable.
        return func

    return decorator


def get_registered_cases() -> list[Case]:
    """
    Retrieve all benchmark cases registered via the `@benchmark` decorator.

    Returns:
        A list of `Case` objects.
    """
    return _DECORATOR_CASES


def clear_registered_cases() -> None:
    """
    Clear all benchmark cases registered via the `@benchmark` decorator.

    This can be useful in testing scenarios to reset the state.
    """
    _DECORATOR_CASES.clear()
