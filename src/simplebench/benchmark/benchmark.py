"""Decorators for simplifying benchmark case creation."""

from collections.abc import Mapping, Callable, Sequence
from typing import TYPE_CHECKING, Any, ParamSpec, TypeVar

from simplebench import defaults
from simplebench.benchmark_runner.benchmark_runner import BenchmarkRunner
from simplebench.case import validate as case_validate
from simplebench.doc_utils import format_docstring
from simplebench.exceptions import SimpleBenchValueError
from simplebench.options.reporter.options import ReporterOptions
from simplebench.simplebench_types import ElementCollection
from simplebench.validators import validate_non_blank_string
from simplebench.vcs import get_vcs_info

from . import _validate
from ._error_tags import _BenchmarkErrorTag

if TYPE_CHECKING:
    from simplebench.case import Case


# A global registry to hold benchmark cases created by the decorator.
_DECORATOR_CASES: list['Case'] = []
"""List to store benchmark cases registered via the @benchmark decorator."""

P = ParamSpec('P')
R = TypeVar('R')


@format_docstring(DEFAULT_TIMEOUT_GRACE_PERIOD=defaults.DEFAULT_TIMEOUT_GRACE_PERIOD)
def benchmark(  # noqa: C901
    group: str | Callable[..., Any] = 'default',  # group can be the function when used without params
    /,
    *,  # keyword-only parameters after this point
    title: str | None = None,
    benchmark_id: str | None = None,
    description: str | None = None,
    runners: Sequence[type[BenchmarkRunner]] | None = None,
    iterations: int = defaults.DEFAULT_ITERATIONS,
    warmup_iterations: int = defaults.DEFAULT_WARMUP_ITERATIONS,
    rounds: int | None = None,
    timer: Callable[[], int] | None = None,
    cpu_timer: Callable[[], int] | None = None,
    min_time: float = defaults.DEFAULT_MIN_TIME,
    max_time: float = defaults.DEFAULT_MAX_TIME,
    timeout: float | None = None,
    variation_cols: dict[str, str] | None = None,
    kwargs_variations: dict[str, ElementCollection[Any]] | None = None,
    options: list[ReporterOptions] | None = None,
    n: int | float = 1,
    use_field_for_n: str | None = None,
) -> Callable[[Callable[P, R]], Callable[P, R]]:
    """A decorator to register a function as a benchmark case.

    This module uses a global registry to store benchmark cases created via the
    @benchmark decorator. This enables a streamlined workflow where users simply
    decorate functions and call main().

    .. note::

        Importing a module that uses @benchmark will register its cases globally.
        For testing, use :func:`clear_registered_cases` to reset state between tests.

    This simplifies creating a :class:`Case` by wrapping the decorated function.
    The decorated function should contain the code to be benchmarked.

    It is important to note that the decorated function will be called
    within the context of a :meth:`SimpleRunner.run` call, which means it
    should not handle its own timing or iterations.

    The args provided to the decorator are used to create a :class:`Case` instance,
    which is then added to a global registry. The original function is returned
    unmodified, allowing it to be called directly if needed.

    The arguments to the decorator are largely the same as those for :class:`Case`, with
    the exception of `action`, which is replaced by the decorated function.

    n is included to allow n-weighting the complexity of the benchmark case when using
    runners that support it.

    A minimal example:

    .. code-block:: python

        from simplebench import benchmark, main


        @benchmark
        def addition_benchmark():
            '''A simple addition benchmark.'''
            sum(range(1000))


        if __name__ == '__main__':
            extra_args = None if len(sys.argv) > 1 : ['--progress', '--rich-table.console']
        main(extra_args=extra_args)

    You should read the documentation for :class:`Case` for full details on the parameters and their
    meanings.

    :param group: The benchmark reporting group to which the benchmark case belongs.

        Used to categorize and filter benchmark cases for selection and reporting.
        Cannot be blank (a string composed only of whitespace). The group parameter
        is positional-only. All other parameters must be passed as keyword
        arguments. When the decorator is used without parameters, the group defaults
        to 'default'. This has special handling to allow the decorator to be used
        easily without any parameters.
    :param title: The title of the benchmark case. Uses the function
        name if None. Cannot be blank.
    :param benchmark_id: An optional identifier for the benchmark case.
        If None, a benchmark ID is generated based on the function name and module.
    :param description: A description for the case.
        Uses the function's docstring if None or '(no description)' if there is no docstring.
        Cannot be blank.
    :param runners: A list of runner types to use for the benchmark.
        If None, the default list of runners is used. The default list includes
        all runners listed in `simplebench.defaults.DEFAULT_RUNNERS`
        unless overridden by this parameter or overridden in the Session configuration.

        Priority is given to runners specified here, followed by those specified in the Session,
        configuration and finally those specified in `simplebench.defaults.DEFAULT_RUNNERS`.
    :param iterations: The minimum number of iterations to run for the benchmark.
    :param warmup_iterations: The number of warmup iterations to run before the benchmark.
    :param rounds: The number of rounds to run for the benchmark.

            Rounds are multiple runs of calls to the action within an iteration to mitigate timer
            quantization, loop overhead, and other measurement effects for very fast actions. Setup and teardown
            functions are called only once per iteration (all rounds in the same iteration share the same
            setup/teardown context).

            If None, rounds will be auto-calibrated based on the precision and overhead of the
            timer function and the expected execution time of the action. If the action is very
            fast (e.g., under 10 microseconds), rounds will be set to a higher value to improve
            measurement accuracy with the goal of reducing timer quantization errors.
            If the action is slower, rounds will be set to a lower value.

            If specified, it must be a positive integer.
    :param timer: A callable that returns the current time. If None, the default timer is used.
        The timer function should return an int representing the current time.
    :param cpu_timer: A callable that returns the current CPU time. If None, the default CPU timer is used.
        The CPU timer function should return an int representing the current CPU time.
    :param min_time: The minimum time in seconds to run the benchmark.  Must be a positive number.
        Its reference depends on the timer used, but by default it is wall-clock time.
    :param max_time: The maximum time in seconds to run the benchmark.
        Must be a positive number greater than min_time. Its reference depends on the timer used,
        but by default it is wall-clock time.
    :param timeout: The maximum time in seconds to allow the benchmark
        to run before timing out. If None, a default timeout of
        `max_time` + {DEFAULT_TIMEOUT_GRACE_PERIOD} is used. Must be a positive number.
        Time for timeout is always referenced to wall-clock time.
    :param variation_cols: kwargs to be used for cols to denote kwarg
        variations. Each key is a keyword argument name, and the value is the column label to use for that
        argument. Only keywords that are also in `kwargs_variations` can be used here. These fields will be
        added to the output of reporters that support them as columns of data with the specified labels.
        If None, an empty dict is used.
    :param kwargs_variations: A mapping of keyword argument key names to
        a list of possible values for that argument. Default is {}. When tests are run, the benchmark
        will be executed for each combination of the specified keyword argument variations. The action
        function will be called with a `bench` parameter that is an instance of the runner and the
        keyword arguments for the current variation.
        If None, an empty dict is used.
    :param options: A list of additional options for the benchmark case.
        Each option is an instance of ReporterOptions or a subclass of ReporterOptions.
        Reporter options can be used to customize the output of the benchmark reports for
        specific reporters. Reporters are responsible for extracting applicable ReporterOptionss
        from the list of options themselves.
    :param n: The 'n' weighting of the benchmark case. Must be a positive integer or float.
    :param use_field_for_n: If provided, use the value of this field from kwargs_variations
        to set 'n' dynamically for each variation.
    :param timer: The timer function to use for the benchmark. If None, the default timer is used.
        The timer function should be a callable that returns a float or int representing the current
        time.
    :return: A decorator that registers the function for benchmarking and returns it unmodified.
    :rtype: Callable[[Callable[P, R]], Callable[P, R]]
    :raises SimpleBenchTypeError: If any argument is of an incorrect type.
    :raises SimpleBenchValueError: If any argument has an invalid value.
    """
    func: Callable[..., Any] | None = None
    if callable(group):  # decorator used without parameters
        func = group
        group = 'default'

    # we can't fully validate title and description yet if they are None
    # because they will be inferred later from the function being decorated
    title = _validate.title(title)
    description = _validate.description(description)

    group = case_validate.group(group)
    runners = case_validate.runners(runners)
    iterations = case_validate.iterations(iterations)
    warmup_iterations = case_validate.warmup_iterations(warmup_iterations)
    rounds = case_validate.rounds(rounds)
    timer = case_validate.timer(timer, 'timer')
    cpu_timer = case_validate.timer(cpu_timer, 'cpu_timer')
    min_time = case_validate.min_time(min_time)
    max_time = case_validate.max_time(max_time)
    case_validate.max_greater_than_min(min_time, max_time)
    timeout = case_validate.timeout(timeout, max_time)
    n = case_validate.n(n)
    validated_kwargs_variations = case_validate.kwargs_variations(kwargs_variations)
    validated_variation_cols = case_validate.variation_cols(
        variation_cols_value=variation_cols, kwargs_variations_value=validated_kwargs_variations)
    validated_options = case_validate.options(options)
    use_field_for_n = _validate.use_field_for_n(
        use_field_for_n, validated_kwargs_variations)
    vcs_info = get_vcs_info()

    def _decorator(func: Callable[..., Any]) -> Callable[..., Any]:
        """The actual decorator that wraps the user's function."""

        from simplebench.case import Case, generate_benchmark_id
        def case_action_wrapper(_bench: BenchmarkRunner, **kwargs: Mapping[str, Any]) -> Any:
            """This wrapper becomes the `action` for the `Case`.

            It calls the user's decorated function inside `runner.run()`.

            :param _bench: The benchmark runner executing the benchmark.
            :param kwargs: Any keyword arguments from `kwargs_variations`.
            """
            # The designated use_field_for_n field will always be present
            # in kwargs if specified due to prior validation.
            n_for_run = n if use_field_for_n is None else kwargs.get(use_field_for_n)
            if not isinstance(n_for_run, (int, float)) or n_for_run <= 0:
                raise SimpleBenchValueError(
                    "The 'n' value determined for the benchmark run must be a positive integer.",
                    tag=_BenchmarkErrorTag.BENCHMARK_N_FOR_RUN_INVALID_VALUE,
                )
            return _bench.run(action=func, n=n_for_run, kwargs=kwargs)

        final_benchmark_id = benchmark_id
        if final_benchmark_id is None:
            final_benchmark_id = generate_benchmark_id(obj=func, action=func)

        final_benchmark_id = validate_non_blank_string(
            final_benchmark_id,
            'benchmark_id',
            _BenchmarkErrorTag.BENCHMARK_ID_TYPE,
            _BenchmarkErrorTag.BENCHMARK_ID_VALUE,
        )

        # Create the Case instance, using sensible defaults from the function.
        if title is None:
            inferred_title = func.__name__
        else:
            inferred_title = title
        if description is None:
            inferred_description = '(no description)' if func.__doc__ is None else func.__doc__
        else:
            inferred_description = description

        case = Case(
            group=group,
            vcs_info=vcs_info,
            title=inferred_title,
            benchmark_id=final_benchmark_id,
            action=case_action_wrapper,
            description=inferred_description,
            runners=runners,
            iterations=iterations,
            warmup_iterations=warmup_iterations,
            rounds=rounds,
            timer=timer,
            min_time=min_time,
            max_time=max_time,
            timeout=timeout,
            variation_cols=validated_variation_cols,
            kwargs_variations=kwargs_variations,
            options=validated_options,
        )

        # Add the created case to the global registry.
        _DECORATOR_CASES.append(case)

        # Return the original function so it remains callable.
        return func

    if func:  # @benchmark used without parameters
        return _decorator(func)
    return _decorator  # @benchmark(...) used with parameters


def get_registered_cases() -> list['Case']:
    """Retrieve all benchmark cases registered via the `@benchmark` decorator.

    :return: A list of :class:`Case` objects.
    :rtype: list[Case]
    """
    return _DECORATOR_CASES


def clear_registered_cases() -> None:
    """Clear all benchmark cases registered via the `@benchmark` decorator.

    This can be useful in testing scenarios to reset the state.
    """
    _DECORATOR_CASES.clear()
