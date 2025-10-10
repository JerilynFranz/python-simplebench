# -*- coding: utf-8 -*-
"""Decorators for simplifying benchmark case creation."""
from __future__ import annotations
from typing import Any, Callable, TYPE_CHECKING

from .case import Case
from .defaults import DEFAULT_WARMUP_ITERATIONS
from .runners import SimpleRunner
from .exceptions import SimpleBenchTypeError, SimpleBenchValueError, ErrorTag
from .validators import (validate_positive_int, validate_non_negative_int, validate_positive_float,
                         validate_non_blank_string)


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

    Raises:
        SimpleBenchTypeError: If any argument is of an incorrect type.
        SimpleBenchValueError: If any argument has an invalid value.
    """
    group = validate_non_blank_string(group, 'group',
                                      ErrorTag.BENCHMARK_DECORATOR_GROUP_TYPE,
                                      ErrorTag.BENCHMARK_DECORATOR_GROUP_VALUE)

    if title is not None:
        title = validate_non_blank_string(title, 'title',
                                          ErrorTag.BENCHMARK_DECORATOR_TITLE_TYPE,
                                          ErrorTag.BENCHMARK_DECORATOR_TITLE_VALUE)

    if description is not None:
        description = validate_non_blank_string(description, 'description',
                                                ErrorTag.BENCHMARK_DECORATOR_DESCRIPTION_TYPE,
                                                ErrorTag.BENCHMARK_DECORATOR_DESCRIPTION_VALUE)
    if iterations is not None:
        iterations = validate_positive_int(iterations, 'iterations',
                                           ErrorTag.BENCHMARK_DECORATOR_ITERATIONS_TYPE,
                                           ErrorTag.BENCHMARK_DECORATOR_ITERATIONS_VALUE)

    warmup_iterations = validate_non_negative_int(warmup_iterations, 'warmup_iterations',
                                                  ErrorTag.BENCHMARK_DECORATOR_WARMUP_ITERATIONS_TYPE,
                                                  ErrorTag.BENCHMARK_DECORATOR_WARMUP_ITERATIONS_VALUE)

    if min_time is not None:
        min_time = validate_positive_float(min_time, 'min_time',
                                           ErrorTag.BENCHMARK_DECORATOR_MIN_TIME_TYPE,
                                           ErrorTag.BENCHMARK_DECORATOR_MIN_TIME_VALUE)

    if max_time is not None:
        max_time = validate_positive_float(max_time, 'max_time',
                                           ErrorTag.BENCHMARK_DECORATOR_MAX_TIME_TYPE,
                                           ErrorTag.BENCHMARK_DECORATOR_MAX_TIME_VALUE)

    n = validate_positive_int(n, 'n',
                              ErrorTag.BENCHMARK_DECORATOR_N_TYPE,
                              ErrorTag.BENCHMARK_DECORATOR_N_VALUE)

    kwargs_variations = Case.validate_kwargs_variations(kwargs_variations)
    variation_cols = Case.validate_variation_cols(variation_cols=variation_cols,
                                                  kwargs_variations=kwargs_variations)
    options = Case.validate_options(options)

    if not isinstance(use_field_for_n, str) and use_field_for_n is not None:
        raise SimpleBenchTypeError("The 'use_field_for_n' parameter to the @benchmark decorator "
                                   "must be a string if passed.",
                                   tag=ErrorTag.BENCHMARK_DECORATOR_USE_FIELD_FOR_N_TYPE)

    if (isinstance(use_field_for_n, str) and isinstance(kwargs_variations, dict)):
        if use_field_for_n not in kwargs_variations:
            raise SimpleBenchTypeError("The 'use_field_for_n' parameter to the @benchmark decorator must "
                                       f"match one of the kwargs_variations keys: {list(kwargs_variations.keys())}",
                                       tag=ErrorTag.BENCHMARK_DECORATOR_USE_FIELD_FOR_N_KWARGS_VARIATIONS)
        if not all(isinstance(v, int) and v > 0 for v in kwargs_variations[use_field_for_n]):
            raise SimpleBenchValueError(f"The values for the '{use_field_for_n}' entry in 'kwargs_variations' "
                                        "must all be positive integers when used with 'use_field_for_n'.",
                                        tag=ErrorTag.BENCHMARK_DECORATOR_USE_FIELD_FOR_N_INVALID_VALUE)

    def decorator(func):
        """The actual decorator that wraps the user's function."""
        def case_action_wrapper(bench: SimpleRunner,  **kwargs) -> Any:
            """
            This wrapper becomes the `action` for the `Case`.
            It calls the user's decorated function inside `runner.run()`.

            Args:
                _runner (SimpleRunner): The runner executing the benchmark.
                **kwargs: Any keyworsd arguments from `kwargs_variations`.
            """
            # The designated use_field_for_n field will always be present
            # in kwargs if specified due to prior validation.
            n_for_run = n if use_field_for_n is None else kwargs.get(use_field_for_n)
            return bench.run(action=func, n=n_for_run, kwargs=kwargs)

        # Create the Case instance, using sensible defaults from the function.
        case_kwargs = {
            'group': group,
            'title': title or func.__name__,
            'action': case_action_wrapper,
            'description': description or func.__doc__ or '(no description)',
            'variation_cols': variation_cols or {},
            'kwargs_variations': kwargs_variations or {},
            'options': options or [],
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
