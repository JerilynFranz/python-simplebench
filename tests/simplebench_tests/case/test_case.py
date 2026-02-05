"""Tests for the case.py module."""

import inspect
import sys
from argparse import ArgumentParser
from functools import cache
from typing import Any, cast

import autopypath  # noqa: F401  # modifies sys.path to include project root
import pytest
from rich.console import Console
from testspec import Assert, PytestAction, PytestGet, PytestSet, TestAction, TestSpec, no_assigned_action

from simplebench.benchmark_runner import BenchmarkRunner, SimpleRunner
from simplebench.case import Case, Results
from simplebench.case._error_tags import _CaseErrorTag
from simplebench.enums import Format, Verbosity
from simplebench.exceptions import (
    SimpleBenchBenchmarkError,
    SimpleBenchRuntimeError,
    SimpleBenchTypeError,
    SimpleBenchValueError,
)
from simplebench.metrics import Metric
from simplebench.options.reporter.options import ReporterOptions
from simplebench.reporters.validators.exceptions import _ReportersValidatorsErrorTag
from simplebench.session import Session
from simplebench.simplebench_types import (
    Extras,
    Iterations,
    KWArgsVariations,
    Mark,
    MetricsTimers,
    Values,
    VariationCols,
    VariationMarks,
)
from simplebench_tests import factories
from simplebench_tests.kwargs import CaseKWArgs

_VALUES = Values([0.1, 0.2])
_DEFAULT_METRIC = factories.default_metric()
_DEFAULT_TIMER = 'time.perf_counter'
_DEFAULT_METRICS_TIMERS = MetricsTimers({ _DEFAULT_METRIC: _DEFAULT_TIMER })
_DEFAULT_ITERATIONS = Iterations({ _DEFAULT_METRIC: _VALUES })

class MockReporterOptions(ReporterOptions):
    """A mock ReporterOptions for testing purposes."""
    def __init__(self, name: str) -> None:
        self.name = name


def benchcase(bench: BenchmarkRunner, variation_marks: VariationMarks) -> Results:
    """A simple benchmark case function."""  # fixed docstring for testing purposes

    def action() -> None:
        """A simple benchmark case function."""
        sum(range(1000))  # Example operation to benchmark
    return bench.run(n=1000, action=action, variation_marks=variation_marks)


def benchcase_with_no_docstring(bench: BenchmarkRunner, variation_marks: VariationMarks) -> Results:  # pylint: disable=missing-function-docstring  # noqa: E501
    # No docstring benchcase for testing purposes
    def action() -> None:
        """A simple benchmark case function."""
        sum(range(1000))  # Example operation to benchmark
    return bench.run(n=1000, action=action, variation_marks=variation_marks)


def benchcase_with_size(bench: BenchmarkRunner, variation_marks: VariationMarks) -> Results:
    """A simple benchmark case function.

    :param bench: The benchmark runner.
    :param variation_marks: The variation marks.
    :return: The benchmark results.
    """
    def action(size: int) -> None:
        """A simple benchmark case function with a size parameter and weighted n."""
        _ = sum(range(size))
    if 'size' not in variation_marks:
        raise ValueError("Missing required 'size' parameter in variation_marks")
    return bench.run(n=variation_marks['size'].value, action=action, variation_marks=variation_marks)


def benchcase_with_size_and_factor(bench: BenchmarkRunner, variation_marks: VariationMarks) -> Results:
    """A simple benchmark case function.

    :param bench: The benchmark runner.
    :param variation_marks: The variation marks.
    :return: The benchmark results.
    """
    def action(size: int, factor: int) -> None:
        """A simple benchmark case function with size and factor parameters and weighted n."""
        _ = sum(range(size)) * factor
    if 'size' not in variation_marks or 'factor' not in variation_marks:
        raise ValueError("Missing required 'size' or 'factor' parameter in variation_marks")
    return bench.run(n=variation_marks['size'].value * variation_marks['factor'].value,
                      action=action, variation_marks=variation_marks)

def broken_benchcase_missing_bench(variation_marks: VariationMarks) -> Results:  # pragma: no cover
    """A broken benchmark case function that is missing the required 'bench' parameter.

    :param variation_marks: The variation marks.
    :return: The benchmark results.
    """
    bench = SimpleRunner(
        case=Case(
            group='example',
            title='benchcase',
            action_wrapper=benchcase,  # type: ignore[arg-type]  # expected to be broken
            description='Benchmark case'),
        variation_marks=VariationMarks({}))

    def action() -> None:
        """A simple benchmark case function."""
        sum(range(1000))  # Example operation to benchmark
    return bench.run(n=1000, action=action, variation_marks=variation_marks)


def broken_benchcase_missing_variation_marks(bench: BenchmarkRunner) -> Results:  # pragma: no cover
    """A broken benchmark case function that is missing the required 'variation_marks' parameter.

    :param bench: The benchmark runner.
    :return: The benchmark results.
    """
    variation_marks = VariationMarks({})

    def action() -> None:
        """A simple benchmark case function."""
        sum(range(1000))  # Example operation to benchmark
    return bench.run(n=1000, action=action, variation_marks=variation_marks)


def broken_benchcase_wrong_kwargs_kind(
        bench: BenchmarkRunner, variation_marks: dict[str, Any]) -> Results:  # pragma: no cover
    """A broken benchmark case function that has the wrong kind of variation_marks parameter (should be VariationMarks).

    :param bench: The benchmark runner.
    :param variation_marks: The variation marks.
    :return: The benchmark results.
    """

    def action() -> None:
        """A simple benchmark case function."""
        sum(range(1000))  # Example operation to benchmark
    return bench.run(n=1000, action=action, variation_marks=variation_marks)  # type: ignore[arg-type]  # expected to be broken


def broken_benchcase_extra_param(
        bench: BenchmarkRunner, extra_param: Any, variation_marks: VariationMarks) -> Results:  # pragma: no cover
    """A broken benchmark case function that has an extra parameter (should only have 'bench' and 'variation_marks').

    :param bench: The benchmark runner.
    :param extra_param: An extra parameter.
    :param variation_marks: The variation marks.
    :return: The benchmark results.
    """
    if extra_param is None:
        extra_param = 0

    def action() -> None:
        """A simple benchmark case function."""
        sum(range(1000))  # Example operation to benchmark
    return bench.run(n=1000, action=action, variation_marks=variation_marks)

def broken_benchcase_action_that_raises(
        bench: BenchmarkRunner, variation_marks: VariationMarks) -> Results:  # pragma: no cover
    """A broken benchmark case function whose action raises an exception.

    :param bench: The benchmark runner.
    :param variation_marks: The variation marks.
    :return: The benchmark results.
    """
    def action() -> None:
        """A simple benchmark case function that raises an exception."""
        raise RuntimeError("Intentional error in benchmark action")
    return bench.run(n=1000, action=action, variation_marks=variation_marks)


class BadRunner:  # pragma: no cover
    """A Class that is not a subclass of BenchmarkRunner, used to test invalid runner parameter."""


@cache
def base_casekwargs() -> CaseKWArgs:
    """Create a base CaseKWArgs instance for use in tests.

    :return: A base CaseKWArgs instance.
    :rtype: CaseKWArgs
    """
    return CaseKWArgs(
            group='example',
            title='benchcase',
            description='Benchmark case',
            action_wrapper=benchcase,
            iterations=100,
            warmup_iterations=10,
            min_time=0.01,
            max_time=0.1,
            variation_cols={'size': 'Size'},
            kwargs_variations={'size': [10, 100, 1000]},
            options=[])


@cache
def base_case() -> Case:
    """Create a base Case instance for use in tests.

    :return: A base Case instance.
    :rtype: Case
    """
    caseargs: CaseKWArgs = base_casekwargs()
    return Case(**caseargs)


@cache
def postrun_benchmark_case() -> Case:
    """Create and runs a benchmark Case, returning the Case instance.

    :return: The Case instance after running the benchmark.
    :rtype: Case
    """
    case = Case(
        group='example',
        title='benchcase',
        action_wrapper=benchcase,
        description='Benchmark case',
        variation_cols={},
        kwargs_variations={},
        options=[]
    )

    argparse = ArgumentParser()
    session = Session(args_parser=argparse, cases=[case], verbosity=Verbosity.QUIET, show_progress=False)
    session.parse_args([])  # Empty args to use defaults
    session.run()

    return case


def broken_callback_missing_case(  # pragma: no cover  # pylint: disable=unused-argument
        *, metric: Metric, output_format: Format, output: Any) -> None:
    """A broken callback function that is missing the required 'case' parameter."""


def broken_callback_missing_metric(  # pragma: no cover  # pylint: disable=unused-argument
        *, case: Case,  output_format: Format, output: Any) -> None:
    """A broken callback function that is missing the required 'metric' parameter."""


def broken_callback_missing_format(  # pragma: no cover  # pylint: disable=unused-argument
        *, metric: Metric, case: Case, output: Any) -> None:
    """A broken callback function that is missing the required 'output_format' parameter."""


def broken_callback_missing_output(  # pragma: no cover  # pylint: disable=unused-argument
        *, metric: Metric, output_format: Format, case: Case) -> None:
    """A broken callback function that is missing the required 'output' parameter."""


def broken_callback_wrong_case_type(  # pylint: disable=unused-argument  # pragma: no cover
        *, case: str, metric: Metric, output_format: Format, output: Any) -> None:
    """A broken callback function that has the wrong type of 'case' parameter (should be 'case: Case')."""


def broken_callback_wrong_metric_type(  # pylint: disable=unused-argument  # pragma: no cover
        *, case: Case, metric: str, output_format: Format, output: Any) -> None:
    """A broken callback function that has the wrong type of 'metric' parameter (should be 'metric: Metric')."""


def broken_callback_wrong_format_type(    # pylint: disable=unused-argument  # pragma: no cover
        *, case: Case, metric: Metric, output_format: str, output: Any) -> None:
    """A broken callback function that has the wrong type of 'output_format' parameter
    (should be 'output_format: Format')."""


def broken_callback_wrong_output_type(  # pylint: disable=unused-argument  # pragma: no cover
        *, case: Case, metric: Metric, output_format: Format, output: str) -> None:
    """A broken callback function that has the wrong type of 'output' parameter (should be 'output: Any')."""


def broken_callback_extra_param(  # pylint: disable=unused-argument  # pragma: no cover
        *, case: Case, metric: Metric, output_format: Format, output: Any, extra_param: Any) -> None:
    """A broken callback function that has an extra parameter
    (should only have 'case', 'metric', 'output_format', and 'output')."""


def broken_callback_no_type_hints(  # noqa: ANN201  # pragma: no cover
        case, metric, output_format, output):  # type: ignore[no-untyped-def]  # noqa: ANN001
    """A broken callback function that has no type hints."""


def broken_callback_case_allowed_to_be_positional(  # pylint: disable=unused-argument  # pragma: no cover
        case: Case, *, metric: Metric, output_format: Format, output: Any) -> None:
    """A broken callback function that allows case to be positional."""


def broken_callback_metric_allowed_to_be_positional(  # pylint: disable=unused-argument  # pragma: no cover
        metric: Metric, *, case: Case, output_format: Format, output: Any) -> None:
    """A broken callback function that allows metric to be positional."""


def broken_callback_output_format_allowed_to_be_positional(  # pylint: disable=unused-argument  # pragma: no cover
        output_format: Format, *, case: Case, metric: Metric, output: Any) -> None:
    """A broken callback function that allows output_format to be positional."""


def broken_callback_output_allowed_to_be_positional(  # pylint: disable=unused-argument  # pragma: no cover
        output: Any, *, case: Case, metric: Metric, output_format: Format) -> None:
    """A broken callback function that allows output to be positional."""


def broken_callback_not_keyword_only(  # pylint: disable=unused-argument  # pragma: no cover
        case: Case, metric: Metric, output_format: Format, output: Any) -> None:
    """A broken callback function that is not keyword-only."""


def broken_callback_invalid_case_type_hint(  # pylint: disable=unused-argument,undefined-variable  # pragma: no cover
        *,
        case: 'ThisClassDoesNotExist',  # type: ignore[name-defined]  # pyright: ignore[reportUndefinedVariable]  # pylint: disable=line-too-long  # noqa: F821,E501
        metric: str,
        output_format: float,
        output: list) -> None:
    """A broken callback function that has a type hint for case that points to a non-existent class."""


def broken_callback_invalid_metric_type_hint(  # pylint: disable=unused-argument,undefined-variable  # pragma: no cover
        *,
        case: Case,
        metric: 'ThisClassDoesNotExist',  # type: ignore[name-defined]  # pyright: ignore[reportUndefinedVariable]  # pylint: disable=line-too-long  # noqa: F821,E501
        output_format: float,
        output: list) -> None:
    """A broken callback function that has a type hint for metric that points to a non-existent class."""


def broken_callback_invalid_format_type_hint(  # pylint: disable=unused-argument,undefined-variable  # pragma: no cover
        *,
        case: Case,
        metric: Metric,
        output_format: 'ThisClassDoesNotExist',  # type: ignore[name-defined]  # pyright: ignore[reportUndefinedVariable]  # pylint: disable=line-too-long  # noqa: F821,E501
        output: list) -> None:
    """A broken callback function that has a type hint for output_format that points to a non-existent class."""


def broken_callback_invalid_output_type_hint(  # pylint: disable=unused-argument,undefined-variable  # pragma: no cover
        *,
        case: Case,
        metric: Metric,
        output_format: Format,
        output: 'ThisClassDoesNotExist'   # type: ignore[name-defined]  # pyright: ignore[reportUndefinedVariable]  # pylint: disable=line-too-long  # noqa: F821,E501
        ) -> None:
    """A broken callback function that has a type hint for output that points to a non-existent class."""


def good_callback(  # pylint: disable=unused-argument
        *, case: Case, metric: Metric, output_format: Format, output: Any) -> None:
    """A good callback function that has the correct parameters and types."""


@cache
def displayless_console() -> Console:
    """Create a displayless Console for testing purposes.

    :return: A displayless Console instance.
    :rtype: Console
    """
    return Console(quiet=True)


def test_casekwargs_matches_case_signature() -> None:
    """Verify CaseKWArgs signature matches Case.__init__.

    This test ensures that the CaseKWArgs class has the same parameters as
    the Case class's __init__ method. This prevents discrepancies between
    the two classes that could lead to errors in tests or misunderstandings
    about the parameters required to initialize a Case instance.
    """
    case_sig = inspect.signature(Case.__init__)
    casekwargs_sig = inspect.signature(CaseKWArgs.__init__)

    # Get parameter names (excluding 'self')
    case_params = set(case_sig.parameters.keys()) - {'self'}
    casekwargs_params = set(casekwargs_sig.parameters.keys()) - {'self'}

    assert case_params == casekwargs_params, \
        f"Mismatch: Case has {case_params - casekwargs_params}, " \
        f"CaseKWArgs has {casekwargs_params - case_params}"


def validate_description(actual: str | None, expected: str | None) -> bool:
    """Helper function to validate description strings, accounting for None values.

    :param actual: The actual description.
    :type actual: str | None
    :param expected: The expected description.
    :type expected: str | None
    :return: True if the descriptions match, otherwise raises an AssertionError.
    :rtype: bool
    """
    assert actual == expected, f"Expected description '{expected}', got '{actual}'"
    return True


@pytest.mark.parametrize("testspec", [
    PytestAction("INIT_001",
        name="Minimal good path initialization",
        action=Case,
        kwargs=CaseKWArgs(
            group='example',
            title='benchcase',
            description='Benchmark case',
            action_wrapper=benchcase),
        assertion=Assert.ISINSTANCE,
        expected=Case,
    ),
    PytestAction("INIT_002",
        name="Maximal good path initialization",
        action=Case,
        kwargs=CaseKWArgs(
            group='example',
            title='benchcase',
            description='Benchmark case',
            action_wrapper=benchcase,
            iterations=100,
            warmup_iterations=10,
            min_time=0.1,
            max_time=10.0,
            variation_cols={},
            kwargs_variations={},
            options=[]),
        assertion=Assert.ISINSTANCE,
        expected=Case),
    PytestAction("INIT_003",
        name="Missing group parameter - default to 'default'",
        action=Case,
        kwargs=CaseKWArgs(title='benchcase', description='A simple benchmark case', action_wrapper=benchcase),
        validate_result=lambda case: case.group == 'default',
        assertion=Assert.ISINSTANCE,
        expected=Case),
    PytestAction("INIT_004",
        name="Missing title parameter - default to action function name",
        action=Case,
        kwargs=CaseKWArgs(group='example', description='Benchmark case', action_wrapper=benchcase),
        validate_result=lambda case: validate_description(case.title, benchcase.__name__),
        assertion=Assert.ISINSTANCE,
        expected=Case),
    PytestAction("INIT_005",
        name="Missing description parameter - default to docstring of action function",
        action=Case,
        kwargs=CaseKWArgs(group='example', title='benchcase', action_wrapper=benchcase),
        validate_result=lambda case: validate_description(case.description, benchcase.__doc__),
        assertion=Assert.ISINSTANCE,
        expected=Case),
    PytestAction("INIT_006",
        name="Missing action parameter",
        action=Case,
        kwargs=CaseKWArgs(group='example', title='benchcase', description='Benchmark case'),
        exception=TypeError),
    PytestAction("INIT_007",
        name="Wrong type for group parameter",
        action=Case,
        kwargs=CaseKWArgs(title='benchcase', description='Benchmark case', action_wrapper=benchcase,
                          group=123),  # type: ignore[arg-type]
        exception=SimpleBenchTypeError,
        exception_tag=_CaseErrorTag.INVALID_GROUP_TYPE),
    PytestAction("INIT_008",
        name="Invalid (blank) value for group parameter",
        action=Case,
        kwargs=CaseKWArgs(title='benchcase', description='Benchmark case', action_wrapper=benchcase,
                          group=' '),  # Invalid blank string

        exception=SimpleBenchValueError,
        exception_tag=_CaseErrorTag.INVALID_GROUP_VALUE),
    PytestAction("INIT_009",
        name="Wrong type for title parameter",
        action=Case,
        kwargs=CaseKWArgs(group='example', description='Benchmark case', action_wrapper=benchcase,
                          title=123),  # type: ignore[arg-type]
        exception=SimpleBenchTypeError,
        exception_tag=_CaseErrorTag.INVALID_TITLE_TYPE),
    PytestAction("INIT_010",
        name="Invalid (blank) value for title parameter",
        action=Case,
        kwargs=CaseKWArgs(group='example', description='Benchmark case', action_wrapper=benchcase,
                          title=' '),  # Invalid blank string
        exception=SimpleBenchValueError,
        exception_tag=_CaseErrorTag.INVALID_TITLE_VALUE),
    PytestAction("INIT_011",
        name="Wrong type for description parameter",
        action=Case,
        kwargs=CaseKWArgs(group='example', title='benchcase', action_wrapper=benchcase,
                          description=123),  # type: ignore[arg-type]
        exception=SimpleBenchTypeError,
        exception_tag=_CaseErrorTag.INVALID_DESCRIPTION_TYPE),
    PytestAction("INIT_012",
        name="Invalid (blank) value for description parameter",
        action=Case,
        kwargs=CaseKWArgs(group='example', title='benchcase', action_wrapper=benchcase,
                          description=' '),  # Invalid blank string
        exception=SimpleBenchValueError,
        exception_tag=_CaseErrorTag.INVALID_DESCRIPTION_VALUE),
    PytestAction("INIT_013",
        name="Wrong type for 'action' parameter",
        action=Case,
        kwargs=CaseKWArgs(group='example', title='benchcase', description='Benchmark case',
                          action_wrapper='not_a_function'),  # type: ignore[arg-type]
        exception=SimpleBenchTypeError,
        exception_tag=_CaseErrorTag.INVALID_ACTION_NOT_CALLABLE),
    PytestAction("INIT_014",
        name="'action' function does not accept required argument 'bench'",
        action=Case,
        kwargs=CaseKWArgs(group='example', title='benchcase', description='Benchmark case',
                          action_wrapper=broken_benchcase_missing_bench),  # type: ignore[arg-type]
        exception=SimpleBenchTypeError,
        exception_tag=_CaseErrorTag.INVALID_ACTION_MISSING_BENCH_PARAMETER),
    # PytestAction("INIT_015",
    #    name="'action' function does not accept required argument '**kwargs'",
    #    action=Case,
    #    kwargs=CaseKWArgs(group='example', title='benchcase', description='Benchmark case',
    #                      action_wrapper=broken_benchcase_missing_kwargs),  # type: ignore[arg-type]
    #    exception=SimpleBenchTypeError,
    #    exception_tag=_CaseErrorTag.INVALID_ACTION_MISSING_KWARGS_PARAMETER),
    # PytestAction("INIT_016",
    #    name="'action' function is using wrong form for kwargs: Should specifically be '**kwargs'",
    #    action=Case,
    #    kwargs=CaseKWArgs(group='example', title='benchcase', description='Benchmark case',
    #                      action_wrapper=broken_benchcase_wrong_kwargs_kind),  # type: ignore[arg-type]
    #    exception=SimpleBenchTypeError,
    #    exception_tag=_CaseErrorTag.INVALID_ACTION_MISSING_KWARGS_PARAMETER),
    PytestAction("INIT_017",
        name="Wrong type for iterations parameter",
        action=Case,
        kwargs=CaseKWArgs(group='example', title='benchcase', description='Benchmark case', action_wrapper=benchcase,
                          iterations='not_an_int'),  # type: ignore[arg-type]
        exception=SimpleBenchTypeError,
        exception_tag=_CaseErrorTag.INVALID_ITERATIONS_TYPE),
    PytestAction("INIT_018",
        name="Invalid (non-positive) value for iterations parameter",
        action=Case,
        kwargs=CaseKWArgs(group='example', title='benchcase', description='Benchmark case', action_wrapper=benchcase,
                          iterations=0),  # Invalid non-positive value
        exception=SimpleBenchValueError,
        exception_tag=_CaseErrorTag.INVALID_ITERATIONS_VALUE),
    PytestAction("INIT_019",
        name="Wrong type for warmup_iterations parameter",
        action=Case,
        kwargs=CaseKWArgs(group='example', title='benchcase', description='Benchmark case', action_wrapper=benchcase,
                          warmup_iterations='not_an_int'),  # type: ignore[arg-type]
        exception=SimpleBenchTypeError,
        exception_tag=_CaseErrorTag.INVALID_WARMUP_ITERATIONS_TYPE),
    PytestAction("INIT_020",
        name="Invalid (negative) value for warmup_iterations parameter",
        action=Case,
        kwargs=CaseKWArgs(group='example', title='benchcase', description='Benchmark case', action_wrapper=benchcase,
                          warmup_iterations=-1),  # Invalid negative value
        exception=SimpleBenchValueError,
        exception_tag=_CaseErrorTag.INVALID_WARMUP_ITERATIONS_VALUE),
    PytestAction("INIT_021",
        name="Wrong type for min_time parameter",
        action=Case,
        kwargs=CaseKWArgs(group='example', title='benchcase', description='Benchmark case', action_wrapper=benchcase,
                          min_time='not_a_float'),  # type: ignore[arg-type]
        exception=SimpleBenchTypeError,
        exception_tag=_CaseErrorTag.INVALID_MIN_TIME_TYPE),
    PytestAction("INIT_022",
        name="Invalid (non-positive) value for min_time parameter",
        action=Case,
        kwargs=CaseKWArgs(group='example', title='benchcase', description='Benchmark case', action_wrapper=benchcase,
                          min_time=0.0),  # Invalid non-positive value
        exception=SimpleBenchValueError,
        exception_tag=_CaseErrorTag.INVALID_MIN_TIME_VALUE),
    PytestAction("INIT_023",
        name="Wrong type for max_time parameter",
        action=Case,
        kwargs=CaseKWArgs(group='example', title='benchcase', description='Benchmark case', action_wrapper=benchcase,
                          max_time='not_a_float'),  # type: ignore[arg-type]
        exception=SimpleBenchTypeError,
        exception_tag=_CaseErrorTag.INVALID_MAX_TIME_TYPE),
    PytestAction("INIT_024",
        name="Invalid (non-positive) value for max_time parameter",
        action=Case,
        kwargs=CaseKWArgs(group='example', title='benchcase', description='Benchmark case', action_wrapper=benchcase,
                          max_time=0.0),  # Invalid non-positive value
        exception=SimpleBenchValueError,
        exception_tag=_CaseErrorTag.INVALID_MAX_TIME_VALUE),
    PytestAction("INIT_025",
        name="Invalid (max_time < min_time) values for time parameters",
        action=Case,
        kwargs=CaseKWArgs(group='example', title='benchcase', description='Benchmark case', action_wrapper=benchcase,
                          min_time=5.0,
                          max_time=1.0),  # Invalid: max_time < min_time
        exception=SimpleBenchValueError,
        exception_tag=_CaseErrorTag.INVALID_TIME_RANGE),
    PytestAction("INIT_026",
        name="Invalid (not a BenchmarkRunner subclass) type for runner option",
        action=Case,
        kwargs=CaseKWArgs(group='example', title='benchcase', description='Benchmark case', action_wrapper=benchcase,
                          runners=[BadRunner]),  # type: ignore[arg-type]  # Invalid: Not a BenchmarkRunner subclass
        exception=SimpleBenchTypeError,
        exception_tag=_CaseErrorTag.INVALID_RUNNER_NOT_BENCHMARK_RUNNER_SUBCLASS),
    PytestAction("INIT_027",
        name="Invalid (not a dict) type for variation_cols parameter",
        action=Case,
        kwargs=CaseKWArgs(group='example', title='benchcase', description='Benchmark case', action_wrapper=benchcase,
                          variation_cols='not_a_VariationCols'),  # type: ignore[arg-type]
        exception=SimpleBenchTypeError,
        exception_tag=_CaseErrorTag.INVALID_VARIATION_COLS_NOT_MAPPING),
    PytestAction("INIT_028",
        name="Invalid (contains key that is not type str) type for variation_cols parameter",
        action=Case,
        kwargs=CaseKWArgs(group='example', title='benchcase', description='Benchmark case', action_wrapper=benchcase,
                          variation_cols={123: 'value'}),  # type: ignore[dict-item]  # Invalid key type
        exception=SimpleBenchValueError,
        exception_tag=_CaseErrorTag.INVALID_VARIATION_COLS_ENTRY_KEY_NOT_IN_KWARGS),
    PytestAction("INIT_029",
        name="Invalid (contains key not in kwargs_variations) value for variation_cols parameter",
        action=Case,
        kwargs=CaseKWArgs(group='example', title='benchcase', description='Benchmark case', action_wrapper=benchcase,
                          variation_cols={'param1': 'value'},  # Key not in kwargs_variations
                          kwargs_variations={'param2': [1, 2, 3]}),
        exception=SimpleBenchValueError,
        exception_tag=_CaseErrorTag.INVALID_VARIATION_COLS_ENTRY_KEY_NOT_IN_KWARGS),
    PytestAction("INIT_030",
        name="Invalid (contains value that is not type str) type for variation_cols parameter",
        action=Case,
        kwargs=CaseKWArgs(group='example', title='benchcase', description='Benchmark case', action_wrapper=benchcase,
                          variation_cols={'param1': 123},  # type: ignore[dict-item]  # Invalid value type (not str)
                          kwargs_variations={'param1': [1, 2, 3]}),
        exception=SimpleBenchTypeError,
        exception_tag=_CaseErrorTag.INVALID_VARIATION_COLS_ENTRY_VALUE_NOT_STRING),
    PytestAction("INIT_031",
        name="Invalid (contains a blank string) value for variation_cols parameter",
        action=Case,
        kwargs=CaseKWArgs(group='example', title='benchcase', description='Benchmark case', action_wrapper=benchcase,
                          variation_cols={'param1': ' '},  # Invalid blank string value
                          kwargs_variations={'param1': [1, 2, 3]}),
        exception=SimpleBenchValueError,
        exception_tag=_CaseErrorTag.INVALID_VARIATION_COLS_ENTRY_VALUE_BLANK),
    PytestAction("INIT_032",
        name="Invalid (not a dict) type for kwargs_variations parameter",
        action=Case,
        kwargs=CaseKWArgs(group='example', title='benchcase', description='Benchmark case', action_wrapper=benchcase,
                          kwargs_variations='not_a_dict'),  # type: ignore[arg-type]
        exception=SimpleBenchTypeError,
        exception_tag=_CaseErrorTag.INVALID_KWARGS_VARIATIONS_NOT_MAPPING),
    PytestAction("INIT_033",
        name="Invalid (contains key that is not type str) type for kwargs_variations parameter",
        action=Case,
        kwargs=CaseKWArgs(group='example', title='benchcase', description='Benchmark case', action_wrapper=benchcase,
                          kwargs_variations={123: [1, 2, 3]}),  # type: ignore[dict-item]  # Invalid key type (not str)
        exception=SimpleBenchTypeError,
        exception_tag=_CaseErrorTag.INVALID_KWARGS_VARIATIONS_ENTRY_KEY_TYPE),
    PytestAction("INIT_034",
        name="Invalid (contains key that is not a valid Python identifier) key for kwargs_variations parameter",
        action=Case,
        kwargs=CaseKWArgs(group='example', title='benchcase', description='Benchmark case', action_wrapper=benchcase,
                          kwargs_variations={'invalid-key': [1, 2, 3]}),  # Invalid key format
        exception=SimpleBenchValueError,
        exception_tag=_CaseErrorTag.INVALID_KWARGS_VARIATIONS_ENTRY_KEY_NOT_IDENTIFIER),
    # PytestAction("INIT_035",
    #    name="'action' function has an extra parameter (should only have 'bench' and '**kwargs')",
    #    action=Case,
    #    kwargs=CaseKWArgs(group='example', title='benchcase', description='Benchmark case',
    #                      action_wrapper=broken_benchcase_extra_param),  # type: ignore[arg-type]
    #    exception=SimpleBenchValueError,
    #    exception_tag=_CaseErrorTag.INVALID_ACTION_PARAMETER_COUNT),
    PytestAction("INIT_036",
        name="Invalid (not an ElementCollection) type for options parameter",
        action=Case,
        kwargs=CaseKWArgs(group='example', title='benchcase', description='Benchmark case', action_wrapper=benchcase,
                          options='not_a_list'),  # type: ignore[arg-type]
        exception=SimpleBenchTypeError,
        exception_tag=_CaseErrorTag.INVALID_OPTIONS_NOT_ELEMENT_COLLECTION),
    PytestAction("INIT_037",
        name="Invalid (contains item that is not a ReporterOptions) type for options parameter",
        action=Case,
        kwargs=CaseKWArgs(group='example', title='benchcase', description='Benchmark case', action_wrapper=benchcase,
                          options=[
                              MockReporterOptions('valid_option'),
                              'not_a_reporter_option']),  # type: ignore[list-item]  # Invalid item type
        exception=SimpleBenchTypeError,
        exception_tag=_CaseErrorTag.INVALID_OPTIONS_ENTRY_NOT_REPORTER_OPTION),
    PytestAction("INIT_038",
        name="Valid (empty) list for options parameter",
        action=Case,
        kwargs=CaseKWArgs(group='example', title='benchcase', description='Benchmark case', action_wrapper=benchcase,
                          options=[]),  # Valid empty list
        assertion=Assert.ISINSTANCE,
        expected=Case),
    PytestAction("INIT_039",
        name="Valid (non-empty) list for options parameter",
        action=Case,
        kwargs=CaseKWArgs(group='example', title='benchcase', description='Benchmark case', action_wrapper=benchcase,
                          options=[MockReporterOptions('option1')]),  # Valid non-empty list
        assertion=Assert.ISINSTANCE,
        expected=Case),
    PytestAction("INIT_040",
        name="Empty list for kwargs_variations parameter (no variations defined for a parameter)",
        action=Case,
        kwargs=CaseKWArgs(group='example', title='benchcase', description='Benchmark case', action_wrapper=benchcase,
                          kwargs_variations={'size': []}),  # Invalid empty list for a parameter
        exception=SimpleBenchValueError,
        exception_tag=_CaseErrorTag.INVALID_KWARGS_VARIATIONS_ENTRY_VALUE_EMPTY_LIST),
    PytestAction("INIT_041",
        name="Invalid (contains item that is not a list) type for kwargs_variations parameter",
        action=Case,
        kwargs=CaseKWArgs(group='example', title='benchcase', description='Benchmark case', action_wrapper=benchcase,
                          kwargs_variations={'size': 'not_an_element_collection'}),  # type: ignore[dict-item]  # Invalid item type
        exception=SimpleBenchTypeError,
        exception_tag=_CaseErrorTag.INVALID_KWARGS_VARIATIONS_ENTRY_VALUE_NOT_ELEMENT_COLLECTION),
    PytestAction("INIT_042",
        name="Invalid type for callback parameter(str instead of callable)",
        action=Case,
        kwargs=CaseKWArgs(group='example', title='benchcase', description='Benchmark case', action_wrapper=benchcase,
                          callback='not_a_function'),  # type: ignore[arg-type]
        exception=SimpleBenchTypeError,
        exception_tag=_ReportersValidatorsErrorTag.REPORTER_CALLBACK_NOT_CALLABLE_OR_NONE),
    PytestAction("INIT_043",
        name="Good callback function for callback parameter",
        action=Case,
        kwargs=CaseKWArgs(group='example', title='benchcase', description='Benchmark case', action_wrapper=benchcase,
                          callback=good_callback),  # Valid callback function
        assertion=Assert.ISINSTANCE,
        expected=Case),
    PytestAction("INIT_044",
        name="Callback function missing required 'case' parameter",
        action=Case,
        kwargs=CaseKWArgs(group='example', title='benchcase', description='Benchmark case', action_wrapper=benchcase,
                          callback=broken_callback_missing_case),  # type: ignore[arg-type]
        exception=SimpleBenchTypeError,
        exception_tag=_ReportersValidatorsErrorTag.INVALID_CALL_INCORRECT_SIGNATURE_MISSING_PARAMETER),
    PytestAction("INIT_045",
        name="Callback function missing required 'metric' parameter",
        action=Case,
        kwargs=CaseKWArgs(group='example', title='benchcase', description='Benchmark case', action_wrapper=benchcase,
                          callback=broken_callback_missing_metric),  # type: ignore[arg-type]
        exception=SimpleBenchTypeError,
        exception_tag=_ReportersValidatorsErrorTag.INVALID_CALL_INCORRECT_SIGNATURE_MISSING_PARAMETER),
    PytestAction("INIT_046",
        name="Callback function missing required 'output_format' parameter",
        action=Case,
        kwargs=CaseKWArgs(group='example', title='benchcase', description='Benchmark case', action_wrapper=benchcase,
                          callback=broken_callback_missing_format),  # type: ignore[arg-type]
        exception=SimpleBenchTypeError,
        exception_tag=_ReportersValidatorsErrorTag.INVALID_CALL_INCORRECT_SIGNATURE_MISSING_PARAMETER),
    PytestAction("INIT_047",
        name="Callback function missing required 'output' parameter",
        action=Case,
        kwargs=CaseKWArgs(group='example', title='benchcase', description='Benchmark case', action_wrapper=benchcase,
                          callback=broken_callback_missing_output),  # type: ignore[arg-type]
        exception=SimpleBenchTypeError,
        exception_tag=_ReportersValidatorsErrorTag.INVALID_CALL_INCORRECT_SIGNATURE_MISSING_PARAMETER),
    PytestAction("INIT_048",
        name="Callback function has wrong type for 'case' parameter",
        action=Case,
        kwargs=CaseKWArgs(group='example', title='benchcase', description='Benchmark case', action_wrapper=benchcase,
                          callback=broken_callback_wrong_case_type),  # type: ignore[arg-type]
        exception=SimpleBenchTypeError,
        exception_tag=_ReportersValidatorsErrorTag.INVALID_CALL_INCORRECT_SIGNATURE_PARAMETER_TYPE),
    PytestAction("INIT_049",
        name="Callback function has wrong type for 'metric' parameter",
        action=Case,
        kwargs=CaseKWArgs(group='example', title='benchcase', description='Benchmark case', action_wrapper=benchcase,
                          callback=broken_callback_wrong_metric_type),  # type: ignore[arg-type]
        exception=SimpleBenchTypeError,
        exception_tag=_ReportersValidatorsErrorTag.INVALID_CALL_INCORRECT_SIGNATURE_PARAMETER_TYPE),
    PytestAction("INIT_050",
        name="Callback function has wrong type for 'output_format' parameter",
        action=Case,
        kwargs=CaseKWArgs(group='example', title='benchcase', description='Benchmark case', action_wrapper=benchcase,
                          callback=broken_callback_wrong_format_type),  # type: ignore[arg-type]
        exception=SimpleBenchTypeError,
        exception_tag=_ReportersValidatorsErrorTag.INVALID_CALL_INCORRECT_SIGNATURE_PARAMETER_TYPE),
    PytestAction("INIT_051",
        name="Callback function has wrong type for 'output' parameter",
        action=Case,
        kwargs=CaseKWArgs(group='example', title='benchcase', description='Benchmark case', action_wrapper=benchcase,
                          callback=broken_callback_wrong_output_type),  # type: ignore[arg-type]
        exception=SimpleBenchTypeError,
        exception_tag=_ReportersValidatorsErrorTag.INVALID_CALL_INCORRECT_SIGNATURE_PARAMETER_TYPE),
    PytestAction("INIT_052",
        name="Callback function has an extra parameter",
        action=Case,
        kwargs=CaseKWArgs(group='example', title='benchcase', description='Benchmark case', action_wrapper=benchcase,
                          callback=broken_callback_extra_param),  # type: ignore[arg-type]
        exception=SimpleBenchTypeError,
        exception_tag=_ReportersValidatorsErrorTag.REPORTER_CALLBACK_INCORRECT_NUMBER_OF_PARAMETERS),
    PytestAction("INIT_053",
        name="Callback function has unresolvable type hint for a parameter",
        action=Case,
        kwargs=CaseKWArgs(group='example', title='benchcase', description='Benchmark case', action_wrapper=benchcase,
                          callback=broken_callback_invalid_case_type_hint),  # type: ignore[arg-type]
        exception=SimpleBenchTypeError,
        exception_tag=_ReportersValidatorsErrorTag.INVALID_CALLBACK_UNRESOLVABLE_HINTS),
    PytestAction("INIT_054",
        name="Callback function has unresolvable type hint for metric parameter",
        action=Case,
        kwargs=CaseKWArgs(group='example', title='benchcase', description='Benchmark case', action_wrapper=benchcase,
                          callback=broken_callback_invalid_metric_type_hint),  # type: ignore[arg-type]
        exception=SimpleBenchTypeError,
        exception_tag=_ReportersValidatorsErrorTag.INVALID_CALLBACK_UNRESOLVABLE_HINTS),
    PytestAction("INIT_055",
        name="Callback function has unresolvable type hint for output_format parameter",
        action=Case,
        kwargs=CaseKWArgs(group='example', title='benchcase', description='Benchmark case', action_wrapper=benchcase,
                          callback=broken_callback_invalid_format_type_hint),  # type: ignore[arg-type]
        exception=SimpleBenchTypeError,
        exception_tag=_ReportersValidatorsErrorTag.INVALID_CALLBACK_UNRESOLVABLE_HINTS),
    PytestAction("INIT_056",
        name="Callback function has unresolvable type hint for output parameter",
        action=Case,
        kwargs=CaseKWArgs(group='example', title='benchcase', description='Benchmark case', action_wrapper=benchcase,
                          callback=broken_callback_invalid_output_type_hint),  # type: ignore[arg-type]
        exception=SimpleBenchTypeError,
        exception_tag=_ReportersValidatorsErrorTag.INVALID_CALLBACK_UNRESOLVABLE_HINTS),
    PytestAction("INIT_057",
        name="Callback function has no type hint for case parameter",
        action=Case,
        kwargs=CaseKWArgs(group='example', title='benchcase', description='Benchmark case', action_wrapper=benchcase,
                          callback=broken_callback_no_type_hints),  # type: ignore[arg-type]
        exception=SimpleBenchTypeError,
        exception_tag=_ReportersValidatorsErrorTag.INVALID_CALL_INCORRECT_SIGNATURE_MISSING_PARAMETER_TYPE_HINT),
    PytestAction("INIT_058",
        name="Callback function allows case parameter to be positional (should be keyword-only)",
        action=Case,
        kwargs=CaseKWArgs(group='example', title='benchcase', description='Benchmark case', action_wrapper=benchcase,
                          callback=broken_callback_case_allowed_to_be_positional),  # type: ignore[arg-type]
        exception=SimpleBenchTypeError,
        exception_tag=_ReportersValidatorsErrorTag.INVALID_CALL_INCORRECT_SIGNATURE_PARAMETER_NOT_KEYWORD_ONLY),
    PytestAction("INIT_059",
        name="Callback function allows metric parameter to be positional (should be keyword-only)",
        action=Case,
        kwargs=CaseKWArgs(group='example', title='benchcase', description='Benchmark case', action_wrapper=benchcase,
                          callback=broken_callback_metric_allowed_to_be_positional),  # type: ignore[arg-type]
        exception=SimpleBenchTypeError,
        exception_tag=_ReportersValidatorsErrorTag.INVALID_CALL_INCORRECT_SIGNATURE_PARAMETER_NOT_KEYWORD_ONLY),
    PytestAction("INIT_060",
        name="Callback function allows output_format parameter to be positional (should be keyword-only)",
        action=Case,
        kwargs=CaseKWArgs(group='example', title='benchcase', description='Benchmark case', action_wrapper=benchcase,
                          callback=broken_callback_output_format_allowed_to_be_positional),  # type: ignore[arg-type]
        exception=SimpleBenchTypeError,
        exception_tag=_ReportersValidatorsErrorTag.INVALID_CALL_INCORRECT_SIGNATURE_PARAMETER_NOT_KEYWORD_ONLY),
    PytestAction("INIT_061",
        name="Callback function allows output parameter to be positional (should be keyword-only)",
        action=Case,
        kwargs=CaseKWArgs(group='example', title='benchcase', description='Benchmark case', action_wrapper=benchcase,
                          callback=broken_callback_output_allowed_to_be_positional),  # type: ignore[arg-type]
        exception=SimpleBenchTypeError,
        exception_tag=_ReportersValidatorsErrorTag.INVALID_CALL_INCORRECT_SIGNATURE_PARAMETER_NOT_KEYWORD_ONLY),
    PytestAction("INIT_062",
        name="Accessing results before run triggers exception",
        action=Case,
        kwargs=CaseKWArgs(group='example', title='benchcase', description='Benchmark case', action_wrapper=benchcase),
        validate_attr='results',
        exception=SimpleBenchRuntimeError,
        exception_tag=_CaseErrorTag.HAVE_NOT_RUN_CASE_YET),
    PytestAction("INIT_063",
        name="runners attribute is initialized to () when not provided",
        action=Case,
        kwargs=CaseKWArgs(group='example', title='benchcase', description='Benchmark case', action_wrapper=benchcase),
        validate_attr='runners',
        expected=tuple()),
    PytestAction("INIT_064",
        name="runners attribute is initialized to [SimpleRunner]  when provided",
        action=Case,
        kwargs=CaseKWArgs(
            group='example', title='benchcase', description='Benchmark case', action_wrapper=benchcase,
            runners=[SimpleRunner]),
        validate_result=lambda obj: issubclass(obj.runners[0], SimpleRunner)),
    PytestAction("INIT_065",
        name="Missing description parameter and docstring - default to '(no description)'",
        action=Case,
        kwargs=CaseKWArgs(group='example', title='benchcase', action_wrapper=benchcase_with_no_docstring),
        validate_result=lambda case: validate_description(case.description, '(no description)'),
        assertion=Assert.ISINSTANCE,
        expected=Case),
    PytestAction("INIT_066",
        name="Invalid rounds parameter (not an int)",
        action=Case,
        kwargs=CaseKWArgs(rounds='not_an_int', action_wrapper=benchcase),  # type: ignore[arg-type]
        exception=SimpleBenchTypeError,
        exception_tag=_CaseErrorTag.INVALID_ROUNDS_TYPE),
    PytestAction("INIT_067",
        name="Invalid rounds parameter (zero value)",
        action=Case,
        kwargs=CaseKWArgs(rounds=0, action_wrapper=benchcase),
        exception=SimpleBenchValueError,
        exception_tag=_CaseErrorTag.INVALID_ROUNDS_VALUE),
])
def test_case_init(testspec: TestSpec) -> None:
    """Test the initialization of the Case class.

    :param testspec: The test specification to run.
    :type testspec: TestSpec
    """
    testspec.run()


@pytest.mark.parametrize("testspec", [
    PytestSet("ATTR_001",
        name="Test setting read-only attribute 'group'",
        attribute='group', value='new_group', obj=base_case(),
        exception=AttributeError),
    PytestSet("ATTR_002",
        name="Test setting read-only attribute 'title'",
        attribute='title', value='new_title', obj=base_case(),
        exception=AttributeError),
    PytestSet("ATTR_003",
        name="Test setting read-only attribute 'description'",
        attribute='description', value='new_description', obj=base_case(),
        exception=AttributeError),
    PytestSet("ATTR_004",
        name="Test setting read-only attribute 'action'",
        attribute='action', value=benchcase, obj=base_case(),
        exception=AttributeError),
    PytestSet("ATTR_005",
        name="Test setting read-only attribute 'iterations'",
        attribute='iterations', value=50, obj=base_case(),
        exception=AttributeError),
    PytestSet("ATTR_006",
        name="Test read-only attribute 'warmup_iterations'",
        attribute='warmup_iterations', value=20, obj=base_case(),
        exception=AttributeError),
    PytestSet("ATTR_007",
        name="Test setting read-only attribute 'min_time'",
        attribute='min_time', value=1.0, obj=base_case(),
        exception=AttributeError),
    PytestSet("ATTR_008",
        name="Test setting read-only attribute 'max_time'",
        attribute='max_time', value=10.0, obj=base_case(),
        exception=AttributeError),
    PytestSet("ATTR_009",
        name="Test setting read-only attribute 'variation_cols'",
        attribute='variation_cols', value={'param1': 'Param 1'}, obj=base_case(),
        exception=AttributeError),
    PytestSet("ATTR_010",
        name="Test read-only attribute 'kwargs_variations'",
        attribute='kwargs_variations', value={'param1': [1, 2, 3]}, obj=base_case(),
        exception=AttributeError),
    PytestSet("ATTR_011",
        name="Test read-only attribute 'runners'",
        attribute='runners', value=SimpleRunner, obj=base_case(),
        exception=AttributeError),
    PytestSet("ATTR_012",
        name="Test setting read-only attribute 'callback'",
        obj=base_case(), attribute='callback', value=lambda case, metric, fmt, output: None,
        exception=AttributeError),
    PytestSet("ATTR_013",
        name="Test setting read-only attribute 'results'",
        attribute='results', value=[Results(
                                group='new_group',
                                title='new_title',
                                description='new_description',
                                n=1,
                                rounds=1,
                                metrics_timers=_DEFAULT_METRICS_TIMERS,
                                iterations=_DEFAULT_ITERATIONS,
                                extra_info=Extras())],
        obj=postrun_benchmark_case(),
        exception=AttributeError),
    PytestSet("ATTR_014",
        name="Test setting read-only attribute 'options'",
        attribute='options', value=[], obj=base_case(),
        exception=AttributeError),
])
def test_setting_read_only_attributes(testspec: TestSpec) -> None:
    """Test attempting to set read-only attributes on Case instances.

    :param testspec: The test specification to run.
    :type testspec: TestSpec
    """
    testspec.run()


@pytest.mark.parametrize("testspec", [
    PytestGet('GET_001',
        name="Test getting attribute 'group'",
        attribute='group', obj=base_case(),
        expected=base_casekwargs().get('group')),
    PytestGet('GET_002',
        name="Test getting attribute 'title'",
        attribute='title', obj=base_case(),
        expected=base_casekwargs().get('title')),
    PytestGet('GET_003',
        name="Test getting attribute 'description'",
        attribute='description', obj=base_case(),
        expected=base_casekwargs().get('description')),
    PytestGet('GET_004',
        name="Test getting attribute 'action'",
        attribute='action', obj=base_case(),
        expected=base_casekwargs().get('action_wrapper')),
    PytestGet('GET_005',
        name="Test getting attribute 'iterations'",
        attribute='iterations', obj=base_case(),
        expected=base_casekwargs().get('iterations')),
    PytestGet('GET_006',
        name="Test getting attribute 'warmup_iterations'",
        attribute='warmup_iterations', obj=base_case(),
        expected=base_casekwargs().get('warmup_iterations')),
    PytestGet('GET_007',
        name="Test getting attribute 'min_time'",
        attribute='min_time', obj=base_case(),
        expected=base_casekwargs().get('min_time')),
    PytestGet('GET_008',
        name="Test getting attribute 'max_time'",
        attribute='max_time', obj=base_case(),
        expected=base_casekwargs().get('max_time')),
    PytestGet('GET_009',
        name="Test getting attribute 'variation_cols'",
        attribute='variation_cols', obj=base_case(),
        expected=VariationCols(cast(dict[str, str], base_casekwargs().get('variation_cols')))),
    PytestGet('GET_010',
        name="Test getting attribute 'kwargs_variations'",
        attribute='kwargs_variations', obj=base_case(),
        expected=KWArgsVariations({'size': [Mark('10', 10), Mark('100', 100), Mark('1000', 1000)]})),
    PytestGet('GET_011',
        name="Test getting attribute 'runners'",
        attribute='runners', obj=base_case(),
        expected=tuple()),
    PytestGet('GET_012',
        name="Test getting attribute 'callback'",
        attribute='callback', obj=base_case(),
        expected=base_casekwargs().get('callback')),
    PytestGet('GET_013',
        name="Test getting attribute 'results'",
        attribute='results', obj=postrun_benchmark_case(),
        expected=postrun_benchmark_case().results),
    PytestGet('GET_014',
        name="Test getting attribute 'options'",
        attribute='options', obj=base_case(),
        expected=tuple(base_casekwargs().get('options'))),  # type: ignore[arg-type]
])
def test_getting_attributes(testspec: TestSpec) -> None:
    """Test getting attributes on Case instances.

    :param testspec: The test specification to run.
    :type testspec: TestSpec
    """
    testspec.run()


@pytest.mark.parametrize("testspec", [
    PytestAction("RUN_001",
        name="Minimal benchmark case with no variations successfully runs without exceptions",
        action=no_assigned_action,
        kwargs={},
        extra={
            'output_expected': False,
            'case_kwargs': CaseKWArgs(
                                group='example', title='benchcase', description='Benchmark case',
                                min_time=0.01, max_time=0.1,
                                action_wrapper=benchcase),
        }),
    PytestAction("RUN_002",
        name="Benchmark case with one variation axis successfully runs without exceptions",
        action=no_assigned_action,
        kwargs={},
        extra={
            'output_expected': False,
            'case_kwargs': CaseKWArgs(
                group='example', title='benchcase', description='Benchmark case',
                min_time=0.01, max_time=0.1,
                action_wrapper=benchcase_with_size,
                kwargs_variations={'size': [10, 100, 1000]})}),
    PytestAction("RUN_003",
        name="Benchmark case with two variation axes successfully runs without exceptions",
        action=no_assigned_action,
        kwargs={},
        extra={
            'output_expected': False,
            'case_kwargs': CaseKWArgs(
                group='example', title='benchcase', description='Benchmark case',
                min_time=0.01, max_time=0.1,
                action_wrapper=benchcase_with_size_and_factor,
                kwargs_variations={'size': [10, 100], 'factor': [1, 2, 3]})}),
    PytestAction("RUN_004",
        name="Benchmark case run with a displayless Session successfully runs without exceptions or output",
        action=no_assigned_action,
        kwargs={'session': Session(console=displayless_console())},
        extra={
            'output_expected': False,
            'case_kwargs': CaseKWArgs(
                group='example', title='benchcase', description='Benchmark case',
                min_time=0.01, max_time=0.1, action_wrapper=benchcase)}),
    PytestAction("RUN_005",
        name=("Benchmark case run with a displayless Session and progress=True "
              "successfully runs without exceptions or output"),
        action=no_assigned_action,
        kwargs={'session': Session(console=displayless_console(), show_progress=True)},
        extra={
            'output_expected': False,
            'case_kwargs': CaseKWArgs(
                group='example', title='benchcase', description='Benchmark case',
                min_time=0.01, max_time=0.1, action_wrapper=benchcase)}),
    PytestAction("RUN_006",
        name=("Benchmark case run with a normal Session at DEBUG verbosity "
              "successfully runs without exceptions and with output"),
        action=no_assigned_action,
        kwargs={'session': Session(verbosity=Verbosity.DEBUG, show_progress=True)},
        extra={
            'output_expected': True,
            'case_kwargs': CaseKWArgs(
                group='example', title='benchcase', description='Benchmark case',
                min_time=0.01, max_time=0.1, action_wrapper=benchcase)}),
    PytestAction("RUN_007",
        name="Benchmark case with SimpleRunner set directly runs without exceptions",
        action=no_assigned_action,
        kwargs={},
        extra={
            'output_expected': False,
            'case_kwargs': CaseKWArgs(
                group='example', title='benchcase', description='Benchmark case',
                min_time=0.01, max_time=0.1, action_wrapper=benchcase, runners=[SimpleRunner])}),
    PytestAction("RUN_008",
        name="Benchmark case with SimpleRunner set as session default_runner runs without exceptions",
        action=no_assigned_action,
        kwargs={'session': Session(default_runners=[SimpleRunner])},
        extra={
            'output_expected': False,
            'case_kwargs': CaseKWArgs(
                group='example', title='benchcase', description='Benchmark case',
                min_time=0.01, max_time=0.1, action_wrapper=benchcase)}),
    PytestAction("RUN_009",
        name="Benchmark case with broken action function raises exception",
        action=broken_benchcase_action_that_raises,
        kwargs={},
        exception=SimpleBenchBenchmarkError,
        exception_tag=_CaseErrorTag.BENCHMARK_ACTION_RAISED_EXCEPTION,
        extra={
            'output_expected': False,
            'case_kwargs': CaseKWArgs(
                group='example', title='benchcase', description='Benchmark case',
                min_time=0.01, max_time=0.1, action_wrapper=broken_benchcase_action_that_raises)}),
])
def test_run(capsys: pytest.CaptureFixture[str], testspec: TestAction) -> None:
    """Test the run method of the Case class.

    :param capsys: The pytest capsys fixture.
    :param testspec: The test specification to run.
    :type testspec: TestSpec
    """
    if isinstance(testspec, TestAction):
        if 'case_kwargs' not in testspec.extra or not isinstance(testspec.extra['case_kwargs'], CaseKWArgs):
            raise AssertionError("CaseKWArgs must be provided in the test spec extra['case_kwargs'] field")
        case_args = testspec.extra['case_kwargs']
        try:
            benchmark_case = Case(**case_args)
        except Exception as e:
            raise AssertionError(f"Failed to initialize Case: {e}") from e
        testspec.action = benchmark_case.run

    testspec.run()

    if isinstance(testspec, TestAction):
        output = capsys.readouterr().out
        if testspec.extra.get('output_expected', True):
            assert output != "", "Expected output to stdout/stderr during session run"
        else:
            assert output == "", "Expected no output to stdout/stderr during displayless session run"


if __name__ == "__main__":
    if "typeguard" in sys.modules:
        sys.modules.pop("typeguard")
    pytest.main([__file__])
