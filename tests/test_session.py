"""Tests for the session.py module."""
from __future__ import annotations
from argparse import ArgumentParser
from functools import cache
from pathlib import Path
import sys
from typing import Any, Sequence

import pytest
from rich.console import Console

from simplebench import Case, SimpleRunner, Results, Session, Verbosity
from simplebench.exceptions import (SimpleBenchTypeError, ErrorTag)
from simplebench.protocols import ActionRunner
from simplebench.reporters.reporter_option import ReporterOption
from simplebench.reporters.protocols import ReporterCallback
from simplebench.utils import collect_arg_list


from .testspec import TestAction, idspec, Assert, TestSpec, NO_EXPECTED_VALUE

_SAVED_ARGV = sys.argv.copy()
"""Saved copy of sys.argv for restoring after tests."""


class MockReporterOption(ReporterOption):
    """A mock ReporterOption for testing purposes."""
    def __init__(self, name: str) -> None:
        self.name = name


class NoDefaultValue:
    """A class to mark parameters that have no default value."""


class SessionKWArgs(dict):
    """A class to hold keyword arguments for initializing a Session instance.

    This class is used to facilitate testing of the Session class initialization
    with various combinations of parameters, including those that are optional and those
    that have no default value.
    """
    def __init__(  # pylint: disable=unused-argument
            self, *,
            cases: Sequence[Case] | NoDefaultValue = NoDefaultValue(),
            verbosity: Verbosity | NoDefaultValue = NoDefaultValue(),
            default_runner: type[SimpleRunner] | NoDefaultValue = NoDefaultValue(),
            args_parser: ArgumentParser | NoDefaultValue = NoDefaultValue(),
            progress: bool | NoDefaultValue = NoDefaultValue(),
            output_path: Path | NoDefaultValue = NoDefaultValue(),
            console: Console | NoDefaultValue = NoDefaultValue()) -> None:
        """Constructs a SessionKWArgs instance. This class is used to hold keyword arguments for
        initializing a Session instance in tests.

        Args:
            cases (Sequence[Case]): A sequence of Case instances.
            verbosity (Verbosity): The verbosity level for the session.
            default_runner (type[SimpleRunner]): The default runner class to use for the session.
            args_parser (ArgumentParser): The argument parser instance for the session.
            progress (bool): Whether to show progress information during the session.
            output_path (Path): The output path for the session results.
            console (Console): The console instance to use for the session.
        """
        kwargs = {}
        for key in ('cases', 'verbosity', 'default_runner', 'args_parser', 'progress', 'output_path', 'console'):
            value = locals()[key]
            if not isinstance(value, NoDefaultValue):
                kwargs[key] = value
        super().__init__(**kwargs)


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
            runner: type[SimpleRunner] | NoDefaultValue = NoDefaultValue(),  # pylint: disable=unused-argument
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


@pytest.mark.parametrize("testspec", [
    idspec("INIT_001", TestAction(
        name="No parameters - all defaults",
        action=Session,
        assertion=Assert.ISINSTANCE,
        expected=Session,
    )),
    idspec("INIT_002", TestAction(
        name="All Session parameters set to valid values",
        action=Session,
        kwargs=SessionKWArgs(
            cases=[
                Case(group="Group1",
                     title="Case1",
                     description="A test case",
                     action=benchcase)
            ],
            verbosity=Verbosity.VERBOSE,
            default_runner=SimpleRunner,
            args_parser=ArgumentParser(prog="testprog"),
            progress=True,
            output_path=Path("/tmp/output"),
            console=Console(),
        ),
        assertion=Assert.ISINSTANCE,
        expected=Session,
    )),
    idspec("INIT_003", TestAction(
        name="Invalid type for 'cases' parameter (string instead of Sequence[Case])",
        action=Session,
        kwargs=SessionKWArgs(
            # Invalid type for 'cases' parameter (str instead of Sequence[Case])
            cases="not a sequence of cases",  # type: ignore[arg-type]  # pyright: ignore[reportArgumentType]
        ),
        exception=SimpleBenchTypeError,
        exception_tag=ErrorTag.SESSION_PROPERTY_INVALID_CASE_ARG_IN_SEQUENCE
    )),
    idspec("INIT_004", TestAction(
        name="Invalid type for 'cases' parameter (not a sequence)",
        action=Session,
        kwargs=SessionKWArgs(
            # Invalid type for 'cases' parameter (not a sequence)
            cases=12345,  # type: ignore[arg-type]  # pyright: ignore[reportArgumentType]
        ),
        exception=SimpleBenchTypeError,
        exception_tag=ErrorTag.SESSION_PROPERTY_INVALID_CASES_ARG
    )),
    idspec("INIT_005", TestAction(
        name="Invalid type for 'verbosity' parameter (string instead of Verbosity)",
        action=Session,
        kwargs=SessionKWArgs(
            verbosity="not a Verbosity instance"),  # type: ignore[arg-type]  # pyright: ignore[reportArgumentType]
        exception=SimpleBenchTypeError,
        exception_tag=ErrorTag.SESSION_PROPERTY_INVALID_VERBOSITY_ARG
    )),
    idspec("INIT_006", TestAction(
        name="Invalid type for 'default_runner' parameter (string instead of type[SimpleRunner])",
        action=Session,
        kwargs=SessionKWArgs(
            default_runner="not a runner class"),  # type: ignore[arg-type]  # pyright: ignore[reportArgumentType]
        exception=SimpleBenchTypeError,
        exception_tag=ErrorTag.SESSION_PROPERTY_INVALID_DEFAULT_RUNNER_ARG
    )),
    idspec("INIT_007", TestAction(
        name="Invalid type for 'default_runner' parameter (not a SimpleRunner subclass type but is a type)",
        action=Session,
        kwargs=SessionKWArgs(default_runner=Case),  # type: ignore[arg-type]  # pyright: ignore[reportArgumentType]
        exception=SimpleBenchTypeError,
        exception_tag=ErrorTag.SESSION_PROPERTY_INVALID_DEFAULT_RUNNER_ARG
    )),
    idspec("INIT_008", TestAction(
        name="Invalid type for 'args_parser' parameter (string instead of ArgumentParser)",
        action=Session,
        kwargs=SessionKWArgs(
            args_parser="not an ArgumentParser"),  # type: ignore[arg-type]  # pyright: ignore[reportArgumentType]
        exception=SimpleBenchTypeError,
        exception_tag=ErrorTag.SESSION_PROPERTY_INVALID_ARGSPARSER_ARG
    )),
    idspec("INIT_009", TestAction(
        name="Invalid type for 'progress' parameter (string instead of bool)",
        action=Session,
        kwargs=SessionKWArgs(
            progress="not a bool"),  # type: ignore[arg-type]  # pyright: ignore[reportArgumentType]
        exception=SimpleBenchTypeError,
        exception_tag=ErrorTag.SESSION_PROPERTY_INVALID_PROGRESS_ARG
    )),
    idspec("INIT_010", TestAction(
        name="Invalid type for 'output_path' parameter (string instead of Path)",
        action=Session,
        kwargs=SessionKWArgs(
            output_path="not a Path"),  # type: ignore[arg-type]  # pyright: ignore[reportArgumentType]
        exception=SimpleBenchTypeError,
        exception_tag=ErrorTag.SESSION_PROPERTY_INVALID_OUTPUT_PATH_ARG
    )),
    idspec("INIT_011", TestAction(
        name="Invalid type for 'console' parameter (string instead of Console)",
        action=Session,
        kwargs=SessionKWArgs(
            console="not a Console"),  # type: ignore[arg-type]  # pyright: ignore[reportArgumentType]
        exception=SimpleBenchTypeError,
        exception_tag=ErrorTag.SESSION_PROPERTY_INVALID_CONSOLE_ARG
    )),
])
def test_session_init(testspec: TestSpec) -> None:
    """Tests the initialization of the Session class with various combinations of parameters.

    This test uses the SessionKWArgs class to generate different combinations of parameters
    for the Session class initialization. It checks that the Session instance is created successfully
    with each combination of parameters or raises the appropriate exception for invalid parameters.
    Args:
        testspec (TestSpec): An TestSpec instance for specifying a test.
    """
    testspec.run()


def pre_action(extras: dict[str, Any]) -> None:
    """Helper function to perform pre-action tasks."""
    if extras and "pre_action" in extras:
        pre_args = extras.get("pre_action_args", [])
        extras["pre_action"](*pre_args)


def post_action(extras: dict[str, Any]) -> None:
    """Helper function to perform post-action tasks."""
    if extras and "post_action" in extras:
        post_args = extras.get("post_action_args", [])
        extras["post_action"](*post_args)


def restore_argv() -> None:
    """Helper function to restore sys.argv after argparse testing."""
    try:
        sys.argv = _SAVED_ARGV.copy()
    except Exception as e:
        raise RuntimeError(f"Failed to restore sys.argv: {e}") from e


def set_argv(args: list[str]) -> None:
    """Helper function to set sys.argv for argparse testing."""
    if not isinstance(args, list) or not all(isinstance(arg, str) for arg in args):
        raise ValueError("args must be a list of strings")
    try:
        sys.argv = ["prog"] + args
    except Exception as e:
        sys.argv = _SAVED_ARGV.copy()
        raise e from e


def parseargs_helper(args: list[str]) -> dict[str, Any]:
    """Helper function to configure extra args for argparse testing.

    This function returns a dictionary with pre_action and post_action keys
    to set and restore sys.argv around a test action.
    """
    if not isinstance(args, list) or not all(isinstance(arg, str) for arg in args):
        raise ValueError("args must be a list of strings")
    return {"pre_action": set_argv, "pre_action_args": [args],
            "post_action": restore_argv, "post_action_args": []}


@cache
def session_instance() -> Session:
    """Helper function to create a persistent default Session instance."""
    return Session()


@pytest.mark.parametrize("testspec", [
    idspec("PARSE_ARGS_UNINIT_001", TestAction(
        name="Parse sys.argv --help with uninitialized argparser",
        action=Session().parse_args,
        exception=SystemExit,  # argparse throws SystemExit on --help
        extra=parseargs_helper(["--help"]))),
    idspec("PARSE_ARGS_UNINIT_002", TestAction(
        name="Parse passed args with uninitialized argparser",
        action=Session().parse_args,
        kwargs={"args": ["--help"]},
        exception=SystemExit)),  # argparse throws SystemExit on --help
    idspec("PARSE_ARGS_UNINT_003", TestAction(
        name="Parse empty args with uninitialized argparser",
        action=Session().parse_args,
        kwargs={"args": []},
        expected=NO_EXPECTED_VALUE)),
    idspec("PARSE_ARGS_UNINIT_004", TestAction(
        name="Parse sys.argv '--quiet' with uninitialized argparser",
        action=Session().parse_args,
        exception=SystemExit,
        extra=parseargs_helper(["--quiet"]))),
    idspec("PARSE_ARGS_UNINIT_005", TestAction(
        name="Parse args - invalid type (int) with uninitialized argparser",
        action=Session().parse_args,
        kwargs={"args": 123},  # type: ignore[arg-type]  # pyright: ignore[reportArgumentType]
        exception=SimpleBenchTypeError,
        exception_tag=ErrorTag.SESSION_PARSE_ARGS_INVALID_ARGS_TYPE)),
    idspec("PARSE_ARGS_UNINIT_006", TestAction(
        name="Parse args - invalid type (list with non-str) with uninitialized argparser",
        action=Session().parse_args,
        kwargs={"args": ["--json", 123]},  # type: ignore[list-item]  # pyright: ignore[reportArgumentType]
        exception=SimpleBenchTypeError,
        exception_tag=ErrorTag.SESSION_PARSE_ARGS_INVALID_ARGS_TYPE)),
])
def test_uninitialized_parse_args(testspec: TestAction) -> None:
    """Tests the parse_args method of the Session class."""
    pre_action(testspec.extra)
    testspec.run()
    post_action(testspec.extra)


@cache
def session_with_reporters() -> Session:
    """Helper function to create a persistent Session instance initialized with reporters."""
    session = session_instance()
    session.add_reporter_flags()
    return session


NO_ATTRIBUTE = object()


@pytest.mark.parametrize("testspec", [
    idspec("PARSE_ARGS_001", TestAction(
            name="Parse '--help' with initialized argparser",
            action=session_with_reporters().parse_args,
            args=[["--help"]],
            exception=SystemExit)),  # argparse throws SystemExit on --help
    idspec("PARSE_ARGS_002", TestAction(
            name="Parse '--json' with initialized argparser (.json should be [['console']])",
            action=session_with_reporters().parse_args,
            obj=session_with_reporters(),
            args=[["--json", "console"]],
            validate_obj=lambda obj: collect_arg_list(obj.args, "--json") == ["console"],
            expected=NO_EXPECTED_VALUE)),
    idspec("PARSE_ARGS_003", TestAction(
            name="Parse no arguments with initialized argparser (.json should be False)",
            action=session_with_reporters().parse_args,
            obj=session_with_reporters(),
            args=[[]],
            validate_obj=lambda obj: not obj.args.json,
            expected=NO_EXPECTED_VALUE)),
])
def test_parse_args(testspec: TestAction) -> None:
    """Tests the parse_args method of a Session instance with reporters loaded."""
    pre_action(testspec.extra)
    testspec.run()
    post_action(testspec.extra)
