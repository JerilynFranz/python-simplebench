# -*- coding: utf-8 -*-
"""Decorators for simplifying benchmark case creation."""
from __future__ import annotations
from typing import Any, Callable, TYPE_CHECKING, TypeVar, ParamSpec

from .case import Case
from .defaults import (DEFAULT_WARMUP_ITERATIONS, DEFAULT_ROUNDS, DEFAULT_MIN_TIME,
                       DEFAULT_MAX_TIME, DEFAULT_ITERATIONS)
from .runners import SimpleRunner
from .exceptions import SimpleBenchTypeError, SimpleBenchValueError, DecoratorsErrorTag
from .validators import (validate_positive_int, validate_non_negative_int, validate_positive_float,
                         validate_non_blank_string)


if TYPE_CHECKING:
    from .reporters.reporter_option import ReporterOption

# A global registry to hold benchmark cases created by the decorator.
_DECORATOR_CASES: list[Case] = []
"""List to store benchmark cases registered via the @benchmark decorator."""

P = ParamSpec('P')
R = TypeVar('R')


def benchmark(
    group: str | Callable[..., Any] = 'default',  # group can be the function when used without params
    /, *,  # keyword-only parameters after this point
    title: str | None = None,
    description: str | None = None,
    iterations: int = DEFAULT_ITERATIONS,
    warmup_iterations: int = DEFAULT_WARMUP_ITERATIONS,
    rounds: int = DEFAULT_ROUNDS,
    min_time: float = DEFAULT_MIN_TIME,
    max_time: float = DEFAULT_MAX_TIME,
    variation_cols: dict[str, str] | None = None,
    kwargs_variations: dict[str, list[Any]] | None = None,
    options: list[ReporterOption] | None = None,
    n: int = 1,
    use_field_for_n: str | None = None
        ) -> Callable[[Callable[P, R]], Callable[P, R]]:
    """
    A decorator to register a function as a benchmark case.

    This module uses a global registry to store benchmark cases created via the
    @benchmark decorator. This enables a streamlined workflow where users simply
    decorate functions and call main().

    Note: Importing a module that uses @benchmark will register its cases globally.
    For testing, use clear_registered_cases() to reset state between tests.

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

    A minimal example:

    ```python
    from simplebench import benchmark, main


    @benchmark
    def addition_benchmark():
        '''A simple addition benchmark.'''
        sum(range(1000))


    if __name__ == '__main__':
        extra_args = None if len(sys.argv) > 1 else ['--progress', '--rich-table.console']
    main(extra_args=extra_args)
    ```

    Args:
        group (str, positional-only, default='default'): The benchmark reporting group to which the benchmark
            case belongs for selection and reporting purposes. It is used to categorize and filter benchmark cases.
            Cannot be blank. The group parameter is positional-only. All other parameters must be passed as keyword
            arguments. When the decorator is used without parameters, the group defaults to 'default'.

            This has special handling to allow the decorator to be used easily without any parameters.

        title (Optional[str], default=None): The title of the benchmark case. Uses the function
                name if None. Cannot be blank.
        description (Optional[str], default=None): A description for the case.
                Uses the function's docstring if None or '(no description)' if there is no docstring.
                Cannot be blank.
        iterations (int, default=`DEFAULT_WARMUP_ITERATIONS`): The minimum number of iterations to run for
                the benchmark.
        warmup_iterations (int, default=`DEFAULT_WARMUP_ITERATIONS`): The number of warmup iterations
                to run before the benchmark.
        rounds (int, default=`DEFAULT_ROUNDS`): The number of rounds to run the benchmark within each
                iteration.
        min_time (int | float, default=`DEFAULT_MIN_TIME`): The minimum time in seconds to run the benchmark.
                Must be a positive number.
        max_time (int | float, default=`DEFAULT_MAX_TIME`): The maximum time in seconds to run the benchmark.
                Must be a positive number greater than min_time.
        variation_cols (Optional[dict[str, str]], default=None): kwargs to be used for cols to denote kwarg
                variations. Each key is a keyword argument name, and the value is the column label to use for that
                argument. Only keywords that are also in `kwargs_variations` can be used here. These fields will be
                added to the output of reporters that support them as columns of data with the specified labels.

                If None, an empty dict is used.
        kwargs_variations (Optional[dict[str, list[Any]]], default=None): A mapping of keyword argument key names to
                a list of possible values for that argument. Default is {}. When tests are run, the benchmark
                will be executed for each combination of the specified keyword argument variations. The action
                function will be called with a `bench` parameter that is an instance of the runner and the
                keyword arguments for the current variation.

                If None, an empty dict is used.
        options (Optional[list[ReporterOption], default=None): A list of additional options for the benchmark case.
                Each option is an instance of ReporterOption or a subclass of ReporterOption.
                Reporter options can be used to customize the output of the benchmark reports for
                specific reporters. Reporters are responsible for extracting applicable ReporterOptions
                from the list of options themselves.
        n (int, default=1): The 'n' weighting of the benchmark case. Must be a positive integer.
        use_field_for_n (Optional[str], default=None): If provided, use the value of this field from kwargs_variations
            to set 'n' dynamically for each variation.

    Returns:
        A decorator that registers the function for benchmarking and returns it unmodified.

    Raises:
        SimpleBenchTypeError: If any argument is of an incorrect type.
        SimpleBenchValueError: If any argument has an invalid value.
    """
    func: Callable[..., Any] | None = None
    if callable(group):  # decorator used without parameters
        func = group
        group = 'default'

    group = validate_non_blank_string(group, 'group',
                                      DecoratorsErrorTag.BENCHMARK_GROUP_TYPE,
                                      DecoratorsErrorTag.BENCHMARK_GROUP_VALUE)

    # we can't fully validate title and description yet if they are None
    # because they will be inferred later from the function being decorated
    if title is not None:
        title = validate_non_blank_string(title, 'title',
                                          DecoratorsErrorTag.BENCHMARK_TITLE_TYPE,
                                          DecoratorsErrorTag.BENCHMARK_TITLE_VALUE)

    if description is not None:
        description = validate_non_blank_string(description, 'description',
                                                DecoratorsErrorTag.BENCHMARK_DESCRIPTION_TYPE,
                                                DecoratorsErrorTag.BENCHMARK_DESCRIPTION_VALUE)

    iterations = validate_positive_int(iterations, 'iterations',
                                       DecoratorsErrorTag.BENCHMARK_ITERATIONS_TYPE,
                                       DecoratorsErrorTag.BENCHMARK_ITERATIONS_VALUE)

    warmup_iterations = validate_non_negative_int(warmup_iterations, 'warmup_iterations',
                                                  DecoratorsErrorTag.BENCHMARK_WARMUP_ITERATIONS_TYPE,
                                                  DecoratorsErrorTag.BENCHMARK_WARMUP_ITERATIONS_VALUE)

    rounds = validate_positive_int(rounds, 'rounds',
                                   DecoratorsErrorTag.BENCHMARK_ROUNDS_TYPE,
                                   DecoratorsErrorTag.BENCHMARK_ROUNDS_VALUE)

    min_time = validate_positive_float(min_time, 'min_time',
                                       DecoratorsErrorTag.BENCHMARK_MIN_TIME_TYPE,
                                       DecoratorsErrorTag.BENCHMARK_MIN_TIME_VALUE)

    max_time = validate_positive_float(max_time, 'max_time',
                                       DecoratorsErrorTag.BENCHMARK_MAX_TIME_TYPE,
                                       DecoratorsErrorTag.BENCHMARK_MAX_TIME_VALUE)

    n = validate_positive_int(n, 'n',
                              DecoratorsErrorTag.BENCHMARK_N_TYPE,
                              DecoratorsErrorTag.BENCHMARK_N_VALUE)

    kwargs_variations = Case.validate_kwargs_variations(kwargs_variations)
    variation_cols = Case.validate_variation_cols(variation_cols=variation_cols,
                                                  kwargs_variations=kwargs_variations)
    options = Case.validate_options(options)

    if not isinstance(use_field_for_n, str) and use_field_for_n is not None:
        raise SimpleBenchTypeError("The 'use_field_for_n' parameter to the @benchmark decorator "
                                   "must be a string if passed.",
                                   tag=DecoratorsErrorTag.BENCHMARK_USE_FIELD_FOR_N_TYPE)

    if (isinstance(use_field_for_n, str) and isinstance(kwargs_variations, dict)):
        if use_field_for_n not in kwargs_variations:
            raise SimpleBenchValueError(
                "The 'use_field_for_n' parameter to the @benchmark decorator must "
                f"match one of the kwargs_variations keys: {list(kwargs_variations.keys())}",
                tag=DecoratorsErrorTag.BENCHMARK_USE_FIELD_FOR_N_KWARGS_VARIATIONS)
        if not all(isinstance(v, int) and v > 0 for v in kwargs_variations[use_field_for_n]):
            raise SimpleBenchValueError(
                f"The values for the '{use_field_for_n}' entry in 'kwargs_variations' "
                "must all be positive integers when used with 'use_field_for_n'.",
                tag=DecoratorsErrorTag.BENCHMARK_USE_FIELD_FOR_N_INVALID_VALUE)

    def decorator(func):
        """The actual decorator that wraps the user's function."""
        def case_action_wrapper(bench: SimpleRunner, **kwargs) -> Any:
            """
            This wrapper becomes the `action` for the `Case`.
            It calls the user's decorated function inside `runner.run()`.

            Args:
                bench (SimpleRunner): The benchmark runner executing the benchmark.
                **kwargs: Any keyword arguments from `kwargs_variations`.
            """
            # The designated use_field_for_n field will always be present
            # in kwargs if specified due to prior validation.
            n_for_run = n if use_field_for_n is None else kwargs.get(use_field_for_n)
            return bench.run(action=func, n=n_for_run, kwargs=kwargs)

        # Create the Case instance, using sensible defaults from the function.
        if title is None:
            inferred_title = func.__name__
        else:
            inferred_title = title
        if description is None:
            inferred_description = '(no description)'if func.__doc__ is None else func.__doc__
        else:
            inferred_description = description

        case = Case(
            group=group,
            title=inferred_title,
            action=case_action_wrapper,
            description=inferred_description,
            iterations=iterations,
            warmup_iterations=warmup_iterations,
            rounds=rounds,
            min_time=min_time,
            max_time=max_time,
            variation_cols=variation_cols,
            kwargs_variations=kwargs_variations,
            options=options,
        )

        # Add the created case to the global registry.
        _DECORATOR_CASES.append(case)

        # Return the original function so it remains callable.
        return func

    if func:  # @benchmark used without parameters
        return decorator(func)
    return decorator  # @benchmark(...) used with parameters


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
