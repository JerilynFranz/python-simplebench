"""Tests for the session.py module."""
from __future__ import annotations

import sys
from argparse import ArgumentParser
from functools import cache
from pathlib import Path
from typing import Any

import pytest
from rich.console import Console
from rich.progress import Progress

from simplebench import Case, Results, Session, Verbosity
from simplebench.exceptions import SimpleBenchTypeError, _SessionErrorTag
from simplebench.reporters.csv import CSVConfig
from simplebench.reporters.graph.scatterplot import ScatterPlotConfig
from simplebench.reporters.json import JSONConfig
from simplebench.reporters.reporter_manager import ReporterManager
from simplebench.reporters.rich_table import RichTableConfig
from simplebench.runners import SimpleRunner
from simplebench.tasks import RichProgressTasks
from simplebench.utils import collect_arg_list

from .factories import session_kwargs_factory
from .kwargs import SessionKWArgs
from .testspec import NO_EXPECTED_VALUE, Assert, TestAction, TestGet, TestSpec, idspec

_SAVED_ARGV = sys.argv.copy()
"""Saved copy of sys.argv for restoring after tests."""


def benchcase(bench: SimpleRunner, **kwargs) -> Results:
    """A simple benchmark case function.

    :param bench: The benchmark runner.
    :type bench: SimpleRunner
    :param kwargs: Keyword arguments for the benchmark.
    :return: The benchmark results.
    :rtype: Results
    """

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
            show_progress=True,
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
        exception_tag=_SessionErrorTag.PROPERTY_INVALID_CASE_ARG_IN_SEQUENCE
    )),
    idspec("INIT_004", TestAction(
        name="Invalid type for 'cases' parameter (not a sequence)",
        action=Session,
        kwargs=SessionKWArgs(
            # Invalid type for 'cases' parameter (not a sequence)
            cases=12345,  # type: ignore[arg-type]  # pyright: ignore[reportArgumentType]
        ),
        exception=SimpleBenchTypeError,
        exception_tag=_SessionErrorTag.PROPERTY_INVALID_CASES_ARG
    )),
    idspec("INIT_005", TestAction(
        name="Invalid type for 'verbosity' parameter (string instead of Verbosity)",
        action=Session,
        kwargs=SessionKWArgs(
            verbosity="not a Verbosity instance"),  # type: ignore[arg-type]  # pyright: ignore[reportArgumentType]
        exception=SimpleBenchTypeError,
        exception_tag=_SessionErrorTag.PROPERTY_INVALID_VERBOSITY_ARG
    )),
    idspec("INIT_006", TestAction(
        name="Invalid type for 'default_runner' parameter (string instead of type[SimpleRunner])",
        action=Session,
        kwargs=SessionKWArgs(
            default_runner="not a runner class"),  # type: ignore[arg-type]  # pyright: ignore[reportArgumentType]
        exception=SimpleBenchTypeError,
        exception_tag=_SessionErrorTag.PROPERTY_INVALID_DEFAULT_RUNNER_ARG
    )),
    idspec("INIT_007", TestAction(
        name="Invalid type for 'default_runner' parameter (not a SimpleRunner subclass type but is a type)",
        action=Session,
        kwargs=SessionKWArgs(default_runner=Case),  # type: ignore[arg-type]  # pyright: ignore[reportArgumentType]
        exception=SimpleBenchTypeError,
        exception_tag=_SessionErrorTag.PROPERTY_INVALID_DEFAULT_RUNNER_ARG
    )),
    idspec("INIT_008", TestAction(
        name="Invalid type for 'args_parser' parameter (string instead of ArgumentParser)",
        action=Session,
        kwargs=SessionKWArgs(
            args_parser="not an ArgumentParser"),  # type: ignore[arg-type]  # pyright: ignore[reportArgumentType]
        exception=SimpleBenchTypeError,
        exception_tag=_SessionErrorTag.PROPERTY_INVALID_ARGSPARSER_ARG
    )),
    idspec("INIT_009", TestAction(
        name="Invalid type for 'progress' parameter (string instead of bool)",
        action=Session,
        kwargs=SessionKWArgs(
            show_progress="not a bool"),  # type: ignore[arg-type]  # pyright: ignore[reportArgumentType]
        exception=SimpleBenchTypeError,
        exception_tag=_SessionErrorTag.PROPERTY_INVALID_PROGRESS_ARG
    )),
    idspec("INIT_010", TestAction(
        name="Invalid type for 'output_path' parameter (string instead of Path)",
        action=Session,
        kwargs=SessionKWArgs(
            output_path="not a Path"),  # type: ignore[arg-type]  # pyright: ignore[reportArgumentType]
        exception=SimpleBenchTypeError,
        exception_tag=_SessionErrorTag.PROPERTY_INVALID_OUTPUT_PATH_ARG
    )),
    idspec("INIT_011", TestAction(
        name="Invalid type for 'console' parameter (string instead of Console)",
        action=Session,
        kwargs=SessionKWArgs(
            console="not a Console"),  # type: ignore[arg-type]  # pyright: ignore[reportArgumentType]
        exception=SimpleBenchTypeError,
        exception_tag=_SessionErrorTag.PROPERTY_INVALID_CONSOLE_ARG
    )),
])
def test_session_init(testspec: TestSpec) -> None:
    """Tests the initialization of the Session class with various combinations of parameters.

    This test uses the SessionKWArgs class to generate different combinations of parameters
    for the Session class initialization. It checks that the Session instance is created successfully
    with each combination of parameters or raises the appropriate exception for invalid parameters.

    :param testspec: An TestSpec instance for specifying a test.
    :type testspec: TestSpec
    """
    testspec.run()


def pre_action(extras: dict[str, Any]) -> None:
    """Helper function to perform pre-action tasks.

    :param extras: A dictionary of extra arguments.
    :type extras: dict[str, Any]
    """
    if extras and "pre_action" in extras:
        pre_args = extras.get("pre_action_args", [])
        extras["pre_action"](*pre_args)


def post_action(extras: dict[str, Any]) -> None:
    """Helper function to perform post-action tasks.

    :param extras: A dictionary of extra arguments.
    :type extras: dict[str, Any]
    """
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
    """Helper function to set sys.argv for argparse testing.

    :param args: A list of strings to set as sys.argv.
    :type args: list[str]
    """
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

    :param args: A list of strings to set as sys.argv.
    :type args: list[str]
    :return: A dictionary with pre_action and post_action keys.
    :rtype: dict[str, Any]
    """
    if not isinstance(args, list) or not all(isinstance(arg, str) for arg in args):
        raise ValueError("args must be a list of strings")
    return {"pre_action": set_argv, "pre_action_args": [args],
            "post_action": restore_argv, "post_action_args": []}


@cache
def session_instance() -> Session:
    """Helper function to create a persistent default Session instance.

    :return: A Session instance.
    :rtype: Session
    """
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
        exception_tag=_SessionErrorTag.PARSE_ARGS_INVALID_ARGS_TYPE)),
    idspec("PARSE_ARGS_UNINIT_006", TestAction(
        name="Parse args - invalid type (list with non-str) with uninitialized argparser",
        action=Session().parse_args,
        kwargs={"args": ["--json", 123]},  # type: ignore[list-item]  # pyright: ignore[reportArgumentType]
        exception=SimpleBenchTypeError,
        exception_tag=_SessionErrorTag.PARSE_ARGS_INVALID_ARGS_TYPE)),
])
def test_uninitialized_parse_args(testspec: TestAction) -> None:
    """Tests the parse_args method of the Session class.

    :param testspec: The test specification to run.
    :type testspec: TestAction
    """
    pre_action(testspec.extra)
    testspec.run()
    post_action(testspec.extra)


@cache
def session_with_reporters() -> Session:
    """Helper function to create a persistent Session instance initialized with reporters.

    :return: A Session instance.
    :rtype: Session
    """
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
            validate_obj=lambda obj: collect_arg_list(args=obj.args, flag="--json") == ["console"],
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
    """Tests the parse_args method of a Session instance with reporters loaded.

    :param testspec: The test specification to run.
    :type testspec: TestAction
    """
    pre_action(testspec.extra)
    testspec.run()
    post_action(testspec.extra)


def reading_properties_testspec() -> list[TestAction]:
    """Generate testspecs for reading Session properties."""
    session_kwargs = session_kwargs_factory()
    session = Session(**session_kwargs)
    testspecs: list[TestAction] = [
        idspec("READ_PROP_001", TestGet(
            name="Read 'cases' property",
            obj=session,
            attribute="cases",
            assertion=Assert.EQUAL,
            expected=tuple(session_kwargs['cases']),
        )),
        idspec("READ_PROP_002", TestGet(
            name="Read 'default_runner' property",
            obj=session,
            attribute="default_runner",
            assertion=Assert.IS,
            expected=session_kwargs['default_runner'],
        )),
        idspec("READ_PROP_003", TestGet(
            name="Read 'args_parser' property",
            obj=session,
            attribute="args_parser",
            assertion=Assert.IS,
            expected=session_kwargs['args_parser'],
        )),
        idspec("READ_PROP_004", TestGet(
            name="Read 'verbosity' property",
            obj=session,
            attribute="verbosity",
            assertion=Assert.EQUAL,
            expected=session_kwargs['verbosity'],
        )),
        idspec("READ_PROP_005", TestGet(
            name="Read 'progress' property",
            obj=session,
            attribute="progress",
            assertion=Assert.ISINSTANCE,
            expected=Progress,
        )),
        idspec("READ_PROP_006", TestGet(
            name="Read 'output_path' property",
            obj=session,
            attribute="output_path",
            assertion=Assert.IS,
            expected=session_kwargs['output_path'],
        )),
        idspec("READ_PROP_007", TestGet(
            name="Read 'console' property",
            obj=session,
            attribute="console",
            assertion=Assert.IS,
            expected=session_kwargs['console'],
        )),
        idspec("READ_PROP_008", TestGet(
            name="Read 'show_progress' property",
            obj=session,
            attribute="show_progress",
            assertion=Assert.EQUAL,
            expected=session_kwargs['show_progress'],
        )),
        idspec("READ_PROP_009", TestGet(
            name="Read 'reporter_manager' property",
            obj=session,
            attribute="reporter_manager",
            assertion=Assert.ISINSTANCE,
            expected=ReporterManager,
        )),
        idspec("READ_PROP_010", TestGet(
            name="Read 'tasks' property",
            obj=session,
            attribute="tasks",
            assertion=Assert.ISINSTANCE,
            expected=RichProgressTasks,
        )),
    ]

    return testspecs


@pytest.mark.parametrize("testspec", reading_properties_testspec())
def test_reading_properties(testspec: TestSpec) -> None:
    """Tests reading properties of the Session class."""
    testspec.run()



def session_add_reporter_flags_testspecs() -> list[TestAction]:
    """Generate testspecs for the add_reporter_flags method of the Session class."""
    session = Session()
    reporter_manager = session.reporter_manager
    reporters = reporter_manager.all_reporters()

    csv_reporter_name = CSVConfig.reporter_name
    json_reporter_name = "json"
    rich_table_reporter_name = "rich_table"
    scatterplot_reporter_name = "scatterplot"


    testspecs: list[TestAction] = [
        
    ]
    return testspecs

def test_session_add_reporter_flags() -> None:
    """Tests the add_reporter_flags method of the Session class."""
    session = Session()
    # Initially, args_parser should have no reporter flags
    initial_args = vars(session.args_parser.parse_args([]))
    assert all(not key.startswith('json') and not key.startswith('csv')
               for key in initial_args.keys())

    # Add reporter flags
    session.add_reporter_flags()
    updated_args = vars(session.args_parser.parse_args([]))
    assert 'json' in updated_args
    assert 'csv' in updated_args

