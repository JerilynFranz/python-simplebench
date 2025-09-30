"""Tests for the case.py module."""
from __future__ import annotations
from argparse import ArgumentParser
from functools import cache
from typing import Any

import pytest

from simplebench import Case, SimpleRunner, Results, Session, Verbosity
from simplebench.enums import Format, Section
from simplebench.exceptions import SimpleBenchTypeError, SimpleBenchValueError, SimpleBenchAttributeError, ErrorTag
from simplebench.protocols import ActionRunner, ReporterCallback
from simplebench.reporters.reporter_option import ReporterOption

from .testspec import TestAction, TestSet, idspec, Assert, TestGet, TestSpec


class MockReporterOption(ReporterOption):
    """A mock ReporterOption for testing purposes."""
    def __init__(self, name: str) -> None:
        self.name = name


class NoDefaultValue:
    """A class to mark parameters that have no default value."""


class CaseKWArgs(dict):
    """A class to hold keyword arguments for initializing a Case instance.

    This class is primarily used to facilitate testing of the Case class initialization
    with various combinations of parameters, including those that are optional and those
    that have no default value.

    It provides a convenient way to construct a dictionary of parameters to be passed
    to the Case class during initialization with linting tools guiding the types of each
    parameter without constraining the presence of or strictly enforcing the types of any parameter.
    """
    def __init__(  # pylint: disable=unused-argument
            self, *,
            group: str | NoDefaultValue = NoDefaultValue(),  # pylint: disable=unused-argument
            title: str | NoDefaultValue = NoDefaultValue(),  # pylint: disable=unused-argument
            description: str | NoDefaultValue = NoDefaultValue(),  # pylint: disable=unused-argument
            action: ActionRunner | NoDefaultValue = NoDefaultValue(),  # pylint: disable=unused-argument
            iterations: int | NoDefaultValue = NoDefaultValue(),  # pylint: disable=unused-argument
            warmup_iterations: int | NoDefaultValue = NoDefaultValue(),  # pylint: disable=unused-argument
            min_time: float | NoDefaultValue = NoDefaultValue(),  # pylint: disable=unused-argument
            max_time: float | NoDefaultValue = NoDefaultValue(),  # pylint: disable=unused-argument
            variation_cols: dict[str, str] | NoDefaultValue = NoDefaultValue(),  # pylint: disable=unused-argument
            kwargs_variations: dict[str, list[Any]] | NoDefaultValue = NoDefaultValue(),  # pylint: disable=unused-argument  # noqa: E501
            runner: SimpleRunner | NoDefaultValue = NoDefaultValue(),  # pylint: disable=unused-argument
            callback: ReporterCallback | NoDefaultValue = NoDefaultValue(),  # pylint: disable=unused-argument
            results: list[Results] | NoDefaultValue = NoDefaultValue(),  # pylint: disable=unused-argument
            options: list[ReporterOption] | NoDefaultValue = NoDefaultValue(),  # pylint: disable=unused-argument
            _decoration: bool | NoDefaultValue = NoDefaultValue()) -> None:  # pylint: disable=unused-argument
        """Constructs a CaseKWArgs instance. This class is used to hold keyword arguments for
        initializing a Case instance in tests.

        Args:
            group (str): The benchmark reporting group to which the benchmark case belongs.
            title (str): The name of the benchmark case.
            description (str): A brief description of the benchmark case.
            action (ActionRunner): The function to perform the benchmark. This function must
                accept a `bench` parameter of type SimpleRunner and arbitrary keyword arguments ('**kwargs').
                It must return a Results object.
            iterations (int): The minimum number of iterations to run for the benchmark. (default: 20)
            warmup_iterations (int): The number of warmup iterations to run before the benchmark. (default: 10)
            min_time (float): The minimum time for the benchmark in seconds. (default: 5.0)
            max_time (float): The maximum time for the benchmark in seconds. (default: 20.0)
            variation_cols (dict[str, str]): kwargs to be used for cols to denote kwarg variations.
                Each key is a keyword argument name, and the value is the column label to use for that argument.

                .. code-block:: python
                    # example of variation_cols
                    variation_cols={
                        'search_depth': 'Search Depth',
                        'runtime_validation': 'Runtime Validation'
                    }
            kwargs_variations (dict[str, list[Any]]):
                Variations of keyword arguments for the benchmark.
                Each key is a keyword argument name, and the value is a list of possible values.

                .. code-block:: python
                    # example of kwargs_variations
                    kwargs_variations={
                        'search_depth': [1, 2, 3],
                        'runtime_validation': [True, False]
                    }
            runner (Optional[SimpleRunner]): A custom runner for the benchmark.
                If None, the default SimpleRunner is used. (default: None)

                The custom runner must be a subclass of SimpleRunner and must have a method
                named `run` that accepts the same parameters as SimpleRunner.run and returns a Results object.

                The action function will be called with a `bench` parameter that is an instance of the
                custom runner.

                It may also accept additional parameters to the run method as needed. If additional
                parameters are needed for the custom runner, they will need to be passed to the run
                method from the action function when using a directly defined Case.

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
                from the list of options themselves.
            _decoration (bool): This field is used internally to indicate if a Case was created via
                a benchmark decorator.
        """
        kwargs = {}
        for key in (
                'group', 'title', 'description', 'action', 'iterations', 'warmup_iterations',
                'min_time', 'max_time', 'variation_cols', 'kwargs_variations', 'runner',
                'callback', 'results', 'options'):
            value = locals()[key]
            if not isinstance(value, NoDefaultValue):
                kwargs[key] = value
        super().__init__(**kwargs)


def benchcase(bench: SimpleRunner, **kwargs) -> Results:
    """A simple benchmark case function."""

    def action() -> None:
        """A simple benchmark case function."""
        sum(range(1000))  # Example operation to benchmark
    return bench.run(n=1000, action=action, **kwargs)


def broken_benchcase_missing_bench(**kwargs: Any) -> Results:  # pragma: no cover
    """A broken benchmark case function that is missing the required 'bench' parameter."""
    bench = SimpleRunner(
        case=Case(
            group='example',
            title='benchcase',
            action=benchcase,
            description='A simple benchmark case.'),
        kwargs={})

    def action() -> None:
        """A simple benchmark case function."""
        sum(range(1000))  # Example operation to benchmark
    return bench.run(n=1000, action=action, kwargs=kwargs)


def broken_benchcase_missing_kwargs(bench: SimpleRunner) -> Results:  # pragma: no cover
    """A broken benchmark case function that is missing the required '**kwargs' parameter."""
    kwargs: dict[str, Any] = {}

    def action() -> None:
        """A simple benchmark case function."""
        sum(range(1000))  # Example operation to benchmark
    return bench.run(n=1000, action=action, kwargs=kwargs)


def broken_benchcase_wrong_kwargs_kind(bench: SimpleRunner, kwargs: dict[str, Any]) -> Results:  # pragma: no cover
    """A broken benchmark case function that has the wrong kind of kwargs parameter (should be '**kwargs')."""

    def action() -> None:
        """A simple benchmark case function."""
        sum(range(1000))  # Example operation to benchmark
    return bench.run(n=1000, action=action, kwargs=kwargs)


def broken_benchcase_extra_param(bench: SimpleRunner, extra_param: Any, **kwargs: Any) -> Results:  # pragma: no cover
    """A broken benchmark case function that has an extra parameter (should only have 'bench' and '**kwargs')."""
    if extra_param is None:
        extra_param = 0

    def action() -> None:
        """A simple benchmark case function."""
        sum(range(1000))  # Example operation to benchmark
    return bench.run(n=1000, action=action, kwargs=kwargs)


class BadRunner:  # pragma: no cover
    """A Class that is not a subclass of SimpleRunner, used to test invalid runner parameter."""


@cache
def base_casekwargs() -> CaseKWArgs:
    """Creates a base CaseKWArgs instance for use in tests."""
    return CaseKWArgs(
            group='example',
            title='benchcase',
            description='A simple benchmark case.',
            action=benchcase,
            iterations=100,
            warmup_iterations=10,
            min_time=0.1,
            max_time=10.0,
            variation_cols={'size': 'Size'},
            kwargs_variations={'size': [10, 100, 1000]},
            options=[])


@cache
def base_case() -> Case:
    """Creates a base Case instance for use in tests."""
    caseargs: CaseKWArgs = base_casekwargs()
    return Case(**caseargs)


@cache
def postrun_benchmark_case() -> Case:
    """Creates and runs a benchmark Case, returning the Case instance."""
    case = Case(
        group='example',
        title='benchcase',
        action=benchcase,
        description='A simple benchmark case.',
        variation_cols={},
        kwargs_variations={},
        options=[]
    )

    argparse = ArgumentParser()
    session = Session(args_parser=argparse, cases=[case], verbosity=Verbosity.QUIET, progress=False)
    session.run()

    return case


def broken_callback_missing_case(  # pragma: no cover  # pylint: disable=unused-argument
        *, section: Section, output_format: Format, output: Any) -> None:
    """A broken callback function that is missing the required 'case' parameter."""


def broken_callback_missing_section(  # pragma: no cover  # pylint: disable=unused-argument
        *, case: Case,  output_format: Format, output: Any) -> None:
    """A broken callback function that is missing the required 'section' parameter."""


def broken_callback_missing_format(  # pragma: no cover  # pylint: disable=unused-argument
        *, section: Section, case: Case, output: Any) -> None:
    """A broken callback function that is missing the required 'output_format' parameter."""


def broken_callback_missing_output(  # pragma: no cover  # pylint: disable=unused-argument
        *, section: Section, output_format: Format, case: Case) -> None:
    """A broken callback function that is missing the required 'output' parameter."""


def broken_callback_wrong_case_type(  # pylint: disable=unused-argument  # pragma: no cover
        *, case: str, section: Section, output_format: Format, output: Any) -> None:
    """A broken callback function that has the wrong type of 'case' parameter (should be 'case: Case')."""


def broken_callback_wrong_section_type(  # pylint: disable=unused-argument  # pragma: no cover
        *, case: Case, section: str, output_format: Format, output: Any) -> None:
    """A broken callback function that has the wrong type of 'section' parameter (should be 'section: Section')."""


def broken_callback_wrong_format_type(    # pylint: disable=unused-argument  # pragma: no cover
        *, case: Case, section: Section, output_format: str, output: Any) -> None:
    """A broken callback function that has the wrong type of 'output_format' parameter
    (should be 'output_format: Format')."""


def broken_callback_wrong_output_type(  # pylint: disable=unused-argument  # pragma: no cover
        *, case: Case, section: Section, output_format: Format, output: str) -> None:
    """A broken callback function that has the wrong type of 'output' parameter (should be 'output: Any')."""


def broken_callback_extra_param(  # pylint: disable=unused-argument  # pragma: no cover
        *, case: Case, section: Section, output_format: Format, output: Any, extra_param: Any) -> None:
    """A broken callback function that has an extra parameter
    (should only have 'case', 'section', 'output_format', and 'output')."""


def broken_callback_no_type_hints(  # pylint: disable=unused-argument  # pragma: no cover
        case, section, output_format, output):  # type: ignore[no-untyped-def]
    """A broken callback function that has no type hints."""


def broken_callback_positional_only(  # pylint: disable=unused-argument  # pragma: no cover
        case: Case, section: Section, /, output_format: Format, output: Any) -> None:
    """A broken callback function that has positional-only parameters."""


def broken_callback_not_keyword_only(  # pylint: disable=unused-argument  # pragma: no cover
        case: Case, section: Section, output_format: Format, output: Any) -> None:
    """A broken callback function that is not keyword-only."""


def good_callback(  # pylint: disable=unused-argument
        *, case: Case, section: Section, output_format: Format, output: Any) -> None:
    """A good callback function that has the correct parameters and types."""


@pytest.mark.parametrize("testspec", [
    idspec("INIT_001", TestAction(
        name="Minimal good path initialization",
        action=Case,
        kwargs=CaseKWArgs(
            group='example',
            title='benchcase',
            description='A simple benchmark case.',
            action=benchcase),
        assertion=Assert.ISINSTANCE,
        expected=Case,
    )),
    idspec("INIT_002", TestAction(
        name="Maximal good path initialization",
        action=Case,
        kwargs=CaseKWArgs(
            group='example',
            title='benchcase',
            description='A simple benchmark case.',
            action=benchcase,
            iterations=100,
            warmup_iterations=10,
            min_time=0.1,
            max_time=10.0,
            variation_cols={},
            kwargs_variations={},
            options=[]),
        assertion=Assert.ISINSTANCE,
        expected=Case,
    )),
    idspec("INIT_003", TestAction(
        name="Missing group parameter",
        action=Case,
        kwargs=CaseKWArgs(
            title='benchcase',
            description='A simple benchmark case',
            action=benchcase),
        exception=TypeError,
    )),
    idspec("INIT_004", TestAction(
        name="Missing title parameter",
        action=Case,
        kwargs=CaseKWArgs(
            group='example',
            description='A simple benchmark case.',
            action=benchcase),
        exception=TypeError)),
    idspec("INIT_005", TestAction(
        name="Missing description parameter",
        action=Case,
        kwargs=CaseKWArgs(
            group='example',
            title='benchcase',
            action=benchcase),
        exception=TypeError)),
    idspec("INIT_006", TestAction(
        name="Missing action parameter",
        action=Case,
        kwargs=CaseKWArgs(
            group='example',
            title='benchcase',
            description='A simple benchmark case.'),
        exception=TypeError)),
    idspec("INIT_007", TestAction(
        name="Wrong type for group parameter",
        action=Case,
        kwargs=CaseKWArgs(
            group=123,  # type: ignore[arg-type]
            title='benchcase',
            description='A simple benchmark case.',
            action=benchcase),
        exception=SimpleBenchTypeError,
        exception_tag=ErrorTag.CASE_INVALID_GROUP_TYPE)),
    idspec("INIT_008", TestAction(
        name="Invalid (blank) value for group parameter",
        action=Case,
        kwargs=CaseKWArgs(
            group=' ',  # Invalid blank string
            title='benchcase',
            description='A simple benchmark case.',
            action=benchcase),
        exception=SimpleBenchValueError,
        exception_tag=ErrorTag.CASE_INVALID_GROUP_VALUE)),
    idspec("INIT_009", TestAction(
        name="Wrong type for title parameter",
        action=Case,
        kwargs=CaseKWArgs(
            group='example',
            title=123,  # type: ignore[arg-type]
            description='A simple benchmark case.',
            action=benchcase),
        exception=SimpleBenchTypeError,
        exception_tag=ErrorTag.CASE_INVALID_TITLE_TYPE)),
    idspec("INIT_010", TestAction(
        name="Invalid (blank) value for title parameter",
        action=Case,
        kwargs=CaseKWArgs(
            group='example',
            title=' ',  # Invalid blank string
            description='A simple benchmark case.',
            action=benchcase),
        exception=SimpleBenchValueError,
        exception_tag=ErrorTag.CASE_INVALID_TITLE_VALUE)),
    idspec("INIT_011", TestAction(
        name="Wrong type for description parameter",
        action=Case,
        kwargs=CaseKWArgs(
            group='example',
            title='benchcase',
            description=123,  # type: ignore[arg-type]
            action=benchcase),
        exception=SimpleBenchTypeError,
        exception_tag=ErrorTag.CASE_INVALID_DESCRIPTION_TYPE)),
    idspec("INIT_012", TestAction(
        name="Invalid (blank) value for description parameter",
        action=Case,
        kwargs=CaseKWArgs(
            group='example',
            title='benchcase',
            description=' ',  # Invalid blank string
            action=benchcase),
        exception=SimpleBenchValueError,
        exception_tag=ErrorTag.CASE_INVALID_DESCRIPTION_VALUE)),
    idspec("INIT_013", TestAction(
        name="Wrong type for 'action' parameter",
        action=Case,
        kwargs=CaseKWArgs(
            group='example',
            title='benchcase',
            description='A simple benchmark case.',
            action='not_a_function'),  # type: ignore[arg-type]
        exception=SimpleBenchTypeError,
        exception_tag=ErrorTag.CASE_INVALID_ACTION_NOT_CALLABLE)),
    idspec("INIT_014", TestAction(
        name="'action' function does not accept required argument 'bench'",
        action=Case,
        kwargs=CaseKWArgs(
            group='example',
            title='benchcase',
            description='A simple benchmark case.',
            action=broken_benchcase_missing_bench),  # type: ignore[arg-type]
        exception=SimpleBenchTypeError,
        exception_tag=ErrorTag.CASE_INVALID_ACTION_MISSING_BENCH_PARAMETER)),
    idspec("INIT_015", TestAction(
        name="'action' function does not accept required argument '**kwargs'",
        action=Case,
        kwargs=CaseKWArgs(
            group='example',
            title='benchcase',
            description='A simple benchmark case.',
            action=broken_benchcase_missing_kwargs),  # type: ignore[arg-type]
        exception=SimpleBenchTypeError,
        exception_tag=ErrorTag.CASE_INVALID_ACTION_MISSING_KWARGS_PARAMETER)),
    idspec("INIT_016", TestAction(
        name="'action' function is using wrong form for kwargs: Should specifically be '**kwargs'",
        action=Case,
        kwargs=CaseKWArgs(
            group='example',
            title='benchcase',
            description='A simple benchmark case.',
            action=broken_benchcase_wrong_kwargs_kind),  # type: ignore[arg-type]
        exception=SimpleBenchTypeError,
        exception_tag=ErrorTag.CASE_INVALID_ACTION_MISSING_KWARGS_PARAMETER)),
    idspec("INIT_017", TestAction(
        name="Wrong type for iterations parameter",
        action=Case,
        kwargs=CaseKWArgs(
            group='example',
            title='benchcase',
            description='A simple benchmark case.',
            action=benchcase,
            iterations='not_an_int'),  # type: ignore[arg-type]
        exception=SimpleBenchTypeError,
        exception_tag=ErrorTag.CASE_INVALID_ITERATIONS_TYPE)),
    idspec("INIT_018", TestAction(
        name="Invalid (non-positive) value for iterations parameter",
        action=Case,
        kwargs=CaseKWArgs(
            group='example',
            title='benchcase',
            description='A simple benchmark case.',
            action=benchcase,
            iterations=0),  # Invalid non-positive value
        exception=SimpleBenchValueError,
        exception_tag=ErrorTag.CASE_INVALID_ITERATIONS_VALUE)),
    idspec("INIT_019", TestAction(
        name="Wrong type for warmup_iterations parameter",
        action=Case,
        kwargs=CaseKWArgs(
            group='example',
            title='benchcase',
            description='A simple benchmark case.',
            action=benchcase,
            warmup_iterations='not_an_int',  # type: ignore[arg-type]
        ),
        exception=SimpleBenchTypeError,
        exception_tag=ErrorTag.CASE_INVALID_WARMUP_ITERATIONS_TYPE)),
    idspec("INIT_020", TestAction(
        name="Invalid (negative) value for warmup_iterations parameter",
        action=Case,
        kwargs=CaseKWArgs(
            group='example',
            title='benchcase',
            description='A simple benchmark case.',
            action=benchcase,
            warmup_iterations=-1),  # Invalid negative value
        exception=SimpleBenchValueError,
        exception_tag=ErrorTag.CASE_INVALID_WARMUP_ITERATIONS_VALUE)),
    idspec("INIT_021", TestAction(
        name="Wrong type for min_time parameter",
        action=Case,
        kwargs=CaseKWArgs(
            group='example',
            title='benchcase',
            description='A simple benchmark case.',
            action=benchcase,
            min_time='not_a_float'),  # type: ignore[arg-type]
        exception=SimpleBenchTypeError,
        exception_tag=ErrorTag.CASE_INVALID_MIN_TIME_TYPE)),
    idspec("INIT_022", TestAction(
        name="Invalid (non-positive) value for min_time parameter",
        action=Case,
        kwargs=CaseKWArgs(
            group='example',
            title='benchcase',
            description='A simple benchmark case.',
            action=benchcase,
            min_time=0.0),  # Invalid non-positive value
        exception=SimpleBenchValueError,
        exception_tag=ErrorTag.CASE_INVALID_MIN_TIME_VALUE)),
    idspec("INIT_023", TestAction(
        name="Wrong type for max_time parameter",
        action=Case,
        kwargs=CaseKWArgs(
            group='example',
            title='benchcase',
            description='A simple benchmark case.',
            action=benchcase,
            max_time='not_a_float'),  # type: ignore[arg-type]
        exception=SimpleBenchTypeError,
        exception_tag=ErrorTag.CASE_INVALID_MAX_TIME_TYPE)),
    idspec("INIT_024", TestAction(
        name="Invalid (non-positive) value for max_time parameter",
        action=Case,
        kwargs=CaseKWArgs(
            group='example',
            title='benchcase',
            description='A simple benchmark case.',
            action=benchcase,
            max_time=0.0),  # Invalid non-positive value
        exception=SimpleBenchValueError,
        exception_tag=ErrorTag.CASE_INVALID_MAX_TIME_VALUE)),
    idspec("INIT_025", TestAction(
        name="Invalid (max_time < min_time) values for time parameters",
        action=Case,
        kwargs=CaseKWArgs(
            group='example',
            title='benchcase',
            description='A simple benchmark case.',
            action=benchcase,
            min_time=5.0,
            max_time=1.0),  # Invalid: max_time < min_time
        exception=SimpleBenchValueError,
        exception_tag=ErrorTag.CASE_INVALID_TIME_RANGE)),
    idspec("INIT_026", TestAction(
        name="Invalid (not a SimpleRunner subclass) type for runner option",
        action=Case,
        kwargs=CaseKWArgs(
            group='example',
            title='benchcase',
            description='A simple benchmark case.',
            action=benchcase,
            runner=BadRunner()),  # type: ignore[arg-type]  # Invalid: Not a SimpleRunner subclass
        exception=SimpleBenchTypeError,
        exception_tag=ErrorTag.CASE_INVALID_RUNNER_NOT_SIMPLE_RUNNER_SUBCLASS)),
    idspec("INIT_027", TestAction(
        name="Invalid (not a dict) type for variation_cols parameter",
        action=Case,
        kwargs=CaseKWArgs(
            group='example',
            title='benchcase',
            description='A simple benchmark case.',
            action=benchcase,
            variation_cols='not_a_dict'),  # type: ignore[arg-type]
        exception=SimpleBenchTypeError,
        exception_tag=ErrorTag.CASE_INVALID_VARIATION_COLS_NOT_DICT)),
    idspec("INIT_028", TestAction(
        name="Invalid (contains key that is not type str) type for variation_cols parameter",
        action=Case,
        kwargs=CaseKWArgs(
            group='example',
            title='benchcase',
            description='A simple benchmark case.',
            action=benchcase,
            variation_cols={123: 'value'}),  # type: ignore[dict-item]  # Invalid key type
        exception=SimpleBenchValueError,
        exception_tag=ErrorTag.CASE_INVALID_VARIATION_COLS_ENTRY_KEY_NOT_IN_KWARGS)),
    idspec("INIT_029", TestAction(
        name="Invalid (contains key not in kwargs_variations) value for variation_cols parameter",
        action=Case,
        kwargs=CaseKWArgs(
            group='example',
            title='benchcase',
            description='A simple benchmark case.',
            action=benchcase,
            variation_cols={'param1': 'value'},  # Key not in kwargs_variations
            kwargs_variations={'param2': [1, 2, 3]}),
        exception=SimpleBenchValueError,
        exception_tag=ErrorTag.CASE_INVALID_VARIATION_COLS_ENTRY_KEY_NOT_IN_KWARGS)),
    idspec("INIT_030", TestAction(
        name="Invalid (contains value that is not type str) type for variation_cols parameter",
        action=Case,
        kwargs=CaseKWArgs(
            group='example',
            title='benchcase',
            description='A simple benchmark case.',
            action=benchcase,
            variation_cols={'param1': 123},  # type: ignore[dict-item]  # Invalid value type (not str)
            kwargs_variations={'param1': [1, 2, 3]}),
        exception=SimpleBenchTypeError,
        exception_tag=ErrorTag.CASE_INVALID_VARIATION_COLS_ENTRY_VALUE_NOT_STRING)),
    idspec("INIT_031", TestAction(
        name="Invalid (contains a blank string) value for variation_cols parameter",
        action=Case,
        kwargs=CaseKWArgs(
            group='example',
            title='benchcase',
            description='A simple benchmark case.',
            action=benchcase,
            variation_cols={'param1': ' '},  # Invalid blank string value
            kwargs_variations={'param1': [1, 2, 3]}),
        exception=SimpleBenchValueError,
        exception_tag=ErrorTag.CASE_INVALID_VARIATION_COLS_ENTRY_VALUE_BLANK)),
    idspec("INIT_032", TestAction(
        name="Invalid (not a dict) type for kwargs_variations parameter",
        action=Case,
        kwargs=CaseKWArgs(
            group='example',
            title='benchcase',
            description='A simple benchmark case.',
            action=benchcase,
            kwargs_variations='not_a_dict'),  # type: ignore[arg-type]
        exception=SimpleBenchTypeError,
        exception_tag=ErrorTag.CASE_INVALID_KWARGS_VARIATIONS_NOT_DICT)),
    idspec("INIT_033", TestAction(
        name="Invalid (contains key that is not type str) type for kwargs_variations parameter",
        action=Case,
        kwargs=CaseKWArgs(
            group='example',
            title='benchcase',
            description='A simple benchmark case.',
            action=benchcase,
            kwargs_variations={123: [1, 2, 3]}),  # type: ignore[dict-item]  # Invalid key type (not str)
        exception=SimpleBenchTypeError,
        exception_tag=ErrorTag.CASE_INVALID_KWARGS_VARIATIONS_ENTRY_KEY_TYPE)),
    idspec("INIT_034", TestAction(
        name="Invalid (contains key that is not a valid Python identifier) key for kwargs_variations parameter",
        action=Case,
        kwargs=CaseKWArgs(
            group='example',
            title='benchcase',
            description='A simple benchmark case.',
            action=benchcase,
            kwargs_variations={'invalid-key': [1, 2, 3]}),  # Invalid key format
        exception=SimpleBenchValueError,
        exception_tag=ErrorTag.CASE_INVALID_KWARGS_VARIATIONS_ENTRY_KEY_NOT_IDENTIFIER)),
    idspec("INIT_035", TestAction(
        name="'action' function has an extra parameter (should only have 'bench' and '**kwargs')",
        action=Case,
        kwargs=CaseKWArgs(
            group='example',
            title='benchcase',
            description='A simple benchmark case.',
            action=broken_benchcase_extra_param),  # type: ignore[arg-type]
        exception=SimpleBenchValueError,
        exception_tag=ErrorTag.CASE_INVALID_ACTION_PARAMETER_COUNT)),
    idspec("INIT_036", TestAction(
        name="Invalid (not a list) type for options parameter",
        action=Case,
        kwargs=CaseKWArgs(
            group='example',
            title='benchcase',
            description='A simple benchmark case.',
            action=benchcase,
            options='not_a_list'),  # type: ignore[arg-type]
        exception=SimpleBenchTypeError,
        exception_tag=ErrorTag.CASE_INVALID_OPTIONS_NOT_LIST)),
    idspec("INIT_037", TestAction(
        name="Invalid (contains item that is not a ReporterOption) type for options parameter",
        action=Case,
        kwargs=CaseKWArgs(
            group='example',
            title='benchcase',
            description='A simple benchmark case.',
            action=benchcase,
            options=[
                MockReporterOption('valid_option'),
                'not_a_reporter_option']),  # type: ignore[list-item]  # Invalid item type
        exception=SimpleBenchTypeError,
        exception_tag=ErrorTag.CASE_INVALID_OPTIONS_ENTRY_NOT_REPORTER_OPTION)),
    idspec("INIT_038", TestAction(
        name="Valid (empty) list for options parameter",
        action=Case,
        kwargs=CaseKWArgs(
            group='example',
            title='benchcase',
            description='A simple benchmark case.',
            action=benchcase,
            options=[]),  # Valid empty list
        assertion=Assert.ISINSTANCE,
        expected=Case,
    )),
    idspec("INIT_039", TestAction(
        name="Valid (non-empty) list for options parameter",
        action=Case,
        kwargs=CaseKWArgs(
            group='example',
            title='benchcase',
            description='A simple benchmark case.',
            action=benchcase,
            options=[MockReporterOption('option1'), MockReporterOption('option2')]),  # Valid non-empty list
        assertion=Assert.ISINSTANCE,
        expected=Case,
    )),
    idspec("INIT_040", TestAction(
        name="Empty list for kwargs_variations parameter (no variations defined for a parameter)",
        action=Case,
        kwargs=CaseKWArgs(
            group='example',
            title='benchcase',
            description='A simple benchmark case.',
            action=benchcase,
            kwargs_variations={'size': []}),  # Empty list for a parameter
        exception=SimpleBenchValueError,
        exception_tag=ErrorTag.CASE_INVALID_KWARGS_VARIATIONS_ENTRY_VALUE_EMPTY_LIST)),
    idspec("INIT_041", TestAction(
        name="Invalid (contains item that is not a list) type for kwargs_variations parameter",
        action=Case,
        kwargs=CaseKWArgs(
            group='example',
            title='benchcase',
            description='A simple benchmark case.',
            action=benchcase,
            kwargs_variations={'size': 'not_a_list'}),  # type: ignore[dict-item]  # Invalid item type
        exception=SimpleBenchTypeError,
        exception_tag=ErrorTag.CASE_INVALID_KWARGS_VARIATIONS_ENTRY_VALUE_NOT_LIST)),
    idspec("INIT_042", TestAction(
        name="Invalid type for callback parameter(str instead of callable)",
        action=Case,
        kwargs=CaseKWArgs(
            group='example',
            title='benchcase',
            description='A simple benchmark case.',
            action=benchcase,
            callback='not_a_function'),  # type: ignore[arg-type]
        exception=SimpleBenchTypeError,
        exception_tag=ErrorTag.CASE_INVALID_CALLBACK_NOT_CALLABLE_OR_NONE)),
    idspec("INIT_043", TestAction(
        name="Good callback function for callback parameter",
        action=Case,
        kwargs=CaseKWArgs(
            group='example',
            title='benchcase',
            description='A simple benchmark case.',
            action=benchcase,
            callback=good_callback),  # Valid callback function
        assertion=Assert.ISINSTANCE,
        expected=Case)),
    idspec("INIT_044", TestAction(
        name="Callback function missing required 'case' parameter",
        action=Case,
        kwargs=CaseKWArgs(
            group='example',
            title='benchcase',
            description='A simple benchmark case.',
            action=benchcase,
            callback=broken_callback_missing_case),  # type: ignore[arg-type]
        exception=SimpleBenchTypeError,
        exception_tag=ErrorTag.CASE_INVALID_CALLBACK_INCORRECT_SIGNATURE_MISSING_CASE_PARAMETER)),
    idspec("INIT_045", TestAction(
        name="Callback function missing required 'section' parameter",
        action=Case,
        kwargs=CaseKWArgs(
            group='example',
            title='benchcase',
            description='A simple benchmark case.',
            action=benchcase,
            callback=broken_callback_missing_section),  # type: ignore[arg-type]
        exception=SimpleBenchTypeError,
        exception_tag=ErrorTag.CASE_INVALID_CALLBACK_INCORRECT_SIGNATURE_MISSING_SECTION_PARAMETER)),
    idspec("INIT_046", TestAction(
        name="Callback function missing required 'output_format' parameter",
        action=Case,
        kwargs=CaseKWArgs(
            group='example',
            title='benchcase',
            description='A simple benchmark case.',
            action=benchcase,
            callback=broken_callback_missing_format),  # type: ignore[arg-type]
        exception=SimpleBenchTypeError,
        exception_tag=ErrorTag.CASE_INVALID_CALLBACK_INCORRECT_SIGNATURE_MISSING_OUTPUT_FORMAT_PARAMETER)),
    idspec("INIT_047", TestAction(
        name="Callback function missing required 'output' parameter",
        action=Case,
        kwargs=CaseKWArgs(
            group='example',
            title='benchcase',
            description='A simple benchmark case.',
            action=benchcase,
            callback=broken_callback_missing_output),  # type: ignore[arg-type]
        exception=SimpleBenchTypeError,
        exception_tag=ErrorTag.CASE_INVALID_CALLBACK_INCORRECT_SIGNATURE_MISSING_OUTPUT_PARAMETER)),
    idspec("INIT_048", TestAction(
        name="Callback function has wrong type for 'case' parameter",
        action=Case,
        kwargs=CaseKWArgs(
            group='example',
            title='benchcase',
            description='A simple benchmark case.',
            action=benchcase,
            callback=broken_callback_wrong_case_type),  # type: ignore[arg-type]
        exception=SimpleBenchTypeError,
        exception_tag=ErrorTag.CASE_INVALID_CALLBACK_INCORRECT_SIGNATURE_CASE_PARAMETER_TYPE)),
    idspec("INIT_049", TestAction(
        name="Callback function has wrong type for 'section' parameter",
        action=Case,
        kwargs=CaseKWArgs(
            group='example',
            title='benchcase',
            description='A simple benchmark case.',
            action=benchcase,
            callback=broken_callback_wrong_section_type),  # type: ignore[arg-type]
        exception=SimpleBenchTypeError,
        exception_tag=ErrorTag.CASE_INVALID_CALLBACK_INCORRECT_SIGNATURE_SECTION_PARAMETER_TYPE)),
    idspec("INIT_050", TestAction(
        name="Callback function has wrong type for 'output_format' parameter",
        action=Case,
        kwargs=CaseKWArgs(
            group='example',
            title='benchcase',
            description='A simple benchmark case.',
            action=benchcase,
            callback=broken_callback_wrong_format_type),  # type: ignore[arg-type]
        exception=SimpleBenchTypeError,
        exception_tag=ErrorTag.CASE_INVALID_CALLBACK_INCORRECT_SIGNATURE_OUTPUT_FORMAT_PARAMETER_TYPE)),
    idspec("INIT_051", TestAction(
        name="Callback function has wrong type for 'output' parameter",
        action=Case,
        kwargs=CaseKWArgs(
            group='example',
            title='benchcase',
            description='A simple benchmark case.',
            action=benchcase,
            callback=broken_callback_wrong_output_type),  # type: ignore[arg-type]
        exception=SimpleBenchTypeError,
        exception_tag=ErrorTag.CASE_INVALID_CALLBACK_INCORRECT_SIGNATURE_OUTPUT_PARAMETER_TYPE)),
    idspec("INIT_052", TestAction(
        name="Callback function has an extra parameter",
        action=Case,
        kwargs=CaseKWArgs(
            group='example',
            title='benchcase',
            description='A simple benchmark case.',
            action=benchcase,
            callback=broken_callback_extra_param),  # type: ignore[arg-type]
        exception=SimpleBenchTypeError,
        exception_tag=ErrorTag.CASE_INVALID_CALLBACK_INCORRECT_NUMBER_OF_PARAMETERS)),
])
def test_case_init(testspec: TestAction) -> None:
    """Test the initialization of the Case class."""
    testspec.run()


@pytest.mark.parametrize("testspec", [
    idspec("ATTR_001", TestSet(
        name="Test setting read-only attribute 'group'",
        attribute='group',
        value='new_group',
        obj=base_case(),
        exception=SimpleBenchAttributeError,
        exception_tag=ErrorTag.CASE_MODIFY_READONLY_GROUP)),
    idspec("ATTR_002", TestSet(
        name="Test setting read-only attribute 'title'",
        attribute='title',
        value='new_title',
        obj=base_case(),
        exception=SimpleBenchAttributeError,
        exception_tag=ErrorTag.CASE_MODIFY_READONLY_TITLE)),
    idspec("ATTR_003", TestSet(
        name="Test setting read-only attribute 'description'",
        attribute='description',
        value='new_description',
        obj=base_case(),
        exception=SimpleBenchAttributeError,
        exception_tag=ErrorTag.CASE_MODIFY_READONLY_DESCRIPTION)),
    idspec("ATTR_004", TestSet(
        name="Test setting read-only attribute 'action'",
        attribute='action',
        value=benchcase,
        obj=base_case(),
        exception=SimpleBenchAttributeError,
        exception_tag=ErrorTag.CASE_MODIFY_READONLY_ACTION)),
    idspec("ATTR_005", TestSet(
        name="Test setting read-only attribute 'iterations'",
        attribute='iterations',
        value=50,
        obj=base_case(),
        exception=SimpleBenchAttributeError,
        exception_tag=ErrorTag.CASE_MODIFY_READONLY_ITERATIONS)),
    idspec("ATTR_006", TestSet(
        name="Test read-only attribute 'warmup_iterations'",
        attribute='warmup_iterations',
        value=20,
        obj=base_case(),
        exception=SimpleBenchAttributeError,
        exception_tag=ErrorTag.CASE_MODIFY_READONLY_WARMUP_ITERATIONS)),
    idspec("ATTR_007", TestSet(
        name="Test setting read-only attribute 'min_time'",
        attribute='min_time',
        value=1.0,
        obj=base_case(),
        exception=SimpleBenchAttributeError,
        exception_tag=ErrorTag.CASE_MODIFY_READONLY_MIN_TIME)),
    idspec("ATTR_008", TestSet(
        name="Test setting read-only attribute 'max_time'",
        attribute='max_time',
        value=10.0,
        obj=base_case(),
        exception=SimpleBenchAttributeError,
        exception_tag=ErrorTag.CASE_MODIFY_READONLY_MAX_TIME)),
    idspec("ATTR_009", TestSet(
        name="Test setting read-only attribute 'variation_cols'",
        attribute='variation_cols',
        value={'param1': 'Param 1'},
        obj=base_case(),
        exception=SimpleBenchAttributeError,
        exception_tag=ErrorTag.CASE_MODIFY_READONLY_VARIATION_COLS)),
    idspec("ATTR_010", TestSet(
        name="Test read-only attribute 'kwargs_variations'",
        attribute='kwargs_variations',
        value={'param1': [1, 2, 3]},
        obj=base_case(),
        exception=SimpleBenchAttributeError,
        exception_tag=ErrorTag.CASE_MODIFY_READONLY_KWARGS_VARIATIONS)),
    idspec("ATTR_011", TestSet(
        name="Test read-only attribute 'runner'",
        attribute='runner',
        value=SimpleRunner(case=base_case(), kwargs={}),
        obj=base_case(),
        exception=SimpleBenchAttributeError,
        exception_tag=ErrorTag.CASE_MODIFY_READONLY_RUNNER)),
    idspec("ATTR_012", TestSet(
        name="Test setting read-only attribute 'callback'",
        attribute='callback',
        value=lambda case, section, fmt, output: None,
        obj=base_case(),
        exception=SimpleBenchAttributeError,
        exception_tag=ErrorTag.CASE_MODIFY_READONLY_CALLBACK)),
    idspec("ATTR_013", TestSet(
        name="Test setting read-only attribute 'results'",
        attribute='results',
        value=[Results(group='new_group', title='new_title', description='new_description', n=1)],
        obj=postrun_benchmark_case(),
        exception=SimpleBenchAttributeError,
        exception_tag=ErrorTag.CASE_MODIFY_READONLY_RESULTS)),
    idspec("ATTR_014", TestSet(
        name="Test setting read-only attribute 'options'",
        attribute='options',
        value=[],
        obj=base_case(),
        exception=SimpleBenchAttributeError,
        exception_tag=ErrorTag.CASE_MODIFY_READONLY_OPTIONS)),
])
def test_setting_read_only_attributes(testspec: TestSpec) -> None:
    """Test attempting to set read-only attributes on Case instances."""
    testspec.run()


@pytest.mark.parametrize("testspec", [
    idspec("GET_001", TestGet(
        name="Test getting attribute 'group'",
        attribute='group',
        obj=base_case(),
        expected=base_casekwargs().get('group'))),
    idspec("GET_002", TestGet(
        name="Test getting attribute 'title'",
        attribute='title',
        obj=base_case(),
        expected=base_casekwargs().get('title'))),
    idspec("GET_003", TestGet(
        name="Test getting attribute 'description'",
        attribute='description',
        obj=base_case(),
        expected=base_casekwargs().get('description'))),
    idspec("GET_004", TestGet(
        name="Test getting attribute 'action'",
        attribute='action',
        obj=base_case(),
        expected=base_casekwargs().get('action'))),
    idspec("GET_005", TestGet(
        name="Test getting attribute 'iterations'",
        attribute='iterations',
        obj=base_case(),
        expected=base_casekwargs().get('iterations'))),
    idspec("GET_006", TestGet(
        name="Test getting attribute 'warmup_iterations'",
        attribute='warmup_iterations',
        obj=base_case(),
        expected=base_casekwargs().get('warmup_iterations'))),
    idspec("GET_007", TestGet(
        name="Test getting attribute 'min_time'",
        attribute='min_time',
        obj=base_case(),
        expected=base_casekwargs().get('min_time'))),
    idspec("GET_008", TestGet(
        name="Test getting attribute 'max_time'",
        attribute='max_time',
        obj=base_case(),
        expected=base_casekwargs().get('max_time'))),
    idspec("GET_009", TestGet(
        name="Test getting attribute 'variation_cols'",
        attribute='variation_cols',
        obj=base_case(),
        expected=base_casekwargs().get('variation_cols'))),
    idspec("GET_010", TestGet(
        name="Test getting attribute 'kwargs_variations'",
        attribute='kwargs_variations',
        obj=base_case(),
        expected=base_casekwargs().get('kwargs_variations'))),
    idspec("GET_011", TestGet(
        name="Test getting attribute 'runner'",
        attribute='runner',
        obj=base_case(),
        expected=base_casekwargs().get('runner'))),
    idspec("GET_012", TestGet(
        name="Test getting attribute 'callback'",
        attribute='callback',
        obj=base_case(),
        expected=base_casekwargs().get('callback'))),
    idspec("GET_013", TestGet(
        name="Test getting attribute 'results'",
        attribute='results',
        obj=postrun_benchmark_case(),
        expected=postrun_benchmark_case().results)),
    idspec("GET_014", TestGet(
        name="Test getting attribute 'options'",
        attribute='options',
        obj=base_case(),
        expected=base_casekwargs().get('options'))),
])
def test_getting_attributes(testspec: TestSpec) -> None:
    """Test getting attributes on Case instances."""
    testspec.run()
