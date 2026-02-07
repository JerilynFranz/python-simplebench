"""Tests for the session.py module."""
# ruff: noqa: F401

import sys
from argparse import ArgumentParser
from functools import cache
from pathlib import Path
from typing import Any

import pytest
from rich.console import Console
from rich.progress import Progress
from testspec import NO_EXPECTED_VALUE, Assert, TestAction, TestGet, TestSpec, idspec, PytestAction, PytestGet

from simplebench import Case, Results, Verbosity
from simplebench.benchmark_runner import SimpleRunner, BenchmarkRunner
from simplebench.display.rich_progress_tasks import RichProgressTasks
from simplebench.exceptions import SimpleBenchArgumentError, SimpleBenchTypeError
from simplebench.reporters.choice import ChoiceConf
from simplebench.reporters.choices import ChoicesConf
from simplebench.reporters.csv import CSVConfig
from simplebench.reporters.reporter_manager import ReporterManager
from simplebench.session import Session, _SessionErrorTag
from simplebench.simplebench_types import VariationMarks
from simplebench.utils import collect_arg_list, flag_to_arg

from .factories import session_factory, session_kwargs_factory
from .kwargs import SessionKWArgs

_SAVED_ARGV = sys.argv.copy()
"""Saved copy of sys.argv for restoring after tests."""


def benchcase(bench: BenchmarkRunner, variation_marks: VariationMarks) -> Results:
    """A simple benchmark case function.

    :param bench: The benchmark runner.
    :type bench: BenchmarkRunner
    :param variation_marks: Variation marks for the benchmark.
    :type variation_marks: VariationMarks
    :return: The benchmark results.
    """

    def action() -> None:
        """A simple benchmark case function."""
        sum(range(1000))  # Example operation to benchmark
    return bench.run(n=1000, action=action, variation_marks=variation_marks)


@pytest.mark.parametrize("testspec", [
    PytestAction("INIT_001",
        name="No parameters - all defaults",
        action=Session,
        assertion=Assert.ISINSTANCE,
        expected=Session,
    ),
    PytestAction("INIT_002",
        name="All Session parameters set to valid values",
        action=Session,
        kwargs=SessionKWArgs(
            cases=[
                Case(group="Group1",
                     title="Case1",
                     description="A test case",
                     action_wrapper=benchcase)
            ],
            verbosity=Verbosity.VERBOSE,
            default_runners=[SimpleRunner],
            args_parser=ArgumentParser(prog="testprog"),
            show_progress=True,
            output_path=Path("/tmp/output"),
            console=Console(),
        ),
        assertion=Assert.ISINSTANCE,
        expected=Session,
    ),
    PytestAction("INIT_003",
        name="Invalid type for 'cases' parameter (string instead of Sequence[Case])",
        action=Session, kwargs=SessionKWArgs(cases="not a sequence of cases"),  # type: ignore[arg-type]
        exception=SimpleBenchTypeError,
        exception_tag=_SessionErrorTag.PROPERTY_INVALID_CASE_ARG_IN_SEQUENCE
    ),
    PytestAction("INIT_004",
        name="Invalid type for 'cases' parameter (not a sequence)",
        action=Session, kwargs=SessionKWArgs(cases=12345),  # type: ignore[arg-type]
        exception=SimpleBenchTypeError,
        exception_tag=_SessionErrorTag.PROPERTY_INVALID_CASES_ARG
    ),
    PytestAction("INIT_005",
        name="Invalid type for 'verbosity' parameter (string instead of Verbosity)",
        action=Session, kwargs=SessionKWArgs(verbosity="not a Verbosity instance"),  # type: ignore[arg-type]
        exception=SimpleBenchTypeError,
        exception_tag=_SessionErrorTag.PROPERTY_INVALID_VERBOSITY_ARG
    ),
    PytestAction("INIT_006",
        name="Invalid type for 'default_runner' parameter (string instead of type[SimpleRunner])",
        action=Session, kwargs=SessionKWArgs(default_runners="not a runner class"),  # type: ignore[arg-type]
        exception=SimpleBenchTypeError,
        exception_tag=_SessionErrorTag.PROPERTY_INVALID_DEFAULT_RUNNER_ARG
    ),
    PytestAction("INIT_007",
        name="Invalid type for 'default_runner' parameter (not a SimpleRunner subclass type but is a type)",
        action=Session, kwargs=SessionKWArgs(default_runners=Case),  # type: ignore[arg-type]
        exception=SimpleBenchTypeError,
        exception_tag=_SessionErrorTag.PROPERTY_INVALID_DEFAULT_RUNNER_ARG
    ),
    PytestAction("INIT_008",
        name="Invalid type for 'args_parser' parameter (string instead of ArgumentParser)",
        action=Session,
        kwargs=SessionKWArgs(args_parser="not an ArgumentParser"),  # type: ignore[arg-type]
        exception=SimpleBenchTypeError,
        exception_tag=_SessionErrorTag.PROPERTY_INVALID_ARGSPARSER_ARG
    ),
    PytestAction("INIT_009",
        name="Invalid type for 'progress' parameter (string instead of bool)",
        action=Session,
        kwargs=SessionKWArgs(show_progress="not a bool"),  # type: ignore[arg-type]
        exception=SimpleBenchTypeError,
        exception_tag=_SessionErrorTag.PROPERTY_INVALID_PROGRESS_ARG
    ),
    PytestAction("INIT_010",
        name="Invalid type for 'output_path' parameter (string instead of Path)",
        action=Session,
        kwargs=SessionKWArgs(output_path="not a Path"),  # type: ignore[arg-type]
        exception=SimpleBenchTypeError,
        exception_tag=_SessionErrorTag.PROPERTY_INVALID_OUTPUT_PATH_ARG
    ),
    PytestAction("INIT_011",
        name="Invalid type for 'console' parameter (string instead of Console)",
        action=Session,
        kwargs=SessionKWArgs(console="not a Console"),  # type: ignore[arg-type]
        exception=SimpleBenchTypeError,
        exception_tag=_SessionErrorTag.PROPERTY_INVALID_CONSOLE_ARG
    ),
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


def setup(extras: dict[str, Any]) -> None:
    """Helper function to perform setup tasks.

    It checks for a "setup" key in the extras dictionary
    and calls the associated function with any provided "setup_args".

    :param extras: A dictionary of extra arguments.
    :type extras: dict[str, Any]
    """
    if extras and "setup" in extras:
        setup_args = extras.get("setup_args", [])
        extras["setup"](*setup_args)


def teardown(extras: dict[str, Any]) -> None:
    """Helper function to perform teardown tasks.

    It checks for a "teardown" key in the extras dictionary
    and calls the associated function with any provided "teardown_args".

    :param extras: A dictionary of extra arguments.
    :type extras: dict[str, Any]
    """
    if extras and "teardown" in extras:
        teardown_args = extras.get("teardown_args", [])
        extras["teardown"](*teardown_args)


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

    This function returns a dictionary with setup and teardown keys
    to set and restore sys.argv around a test action.

    :param args: A list of strings to set as sys.argv.
    :type args: list[str]
    :return: A dictionary with setup and teardown keys.
    :rtype: dict[str, Any]
    """
    if not isinstance(args, list) or not all(isinstance(arg, str) for arg in args):
        raise ValueError("args must be a list of strings")
    return {"setup": set_argv, "setup_args": [args],
            "teardown": restore_argv, "teardown_args": []}


@cache
def session_instance() -> Session:
    """Helper function to create a persistent default Session instance.

    :return: A Session instance.
    :rtype: Session
    """
    return Session()


@pytest.mark.parametrize("testspec", [
    PytestAction("PARSE_ARGS_UNINIT_001",
        name="Parse sys.argv --help with uninitialized argparser",
        action=Session().parse_args,
        exception=SystemExit,  # argparse throws SystemExit on --help
        extra=parseargs_helper(["--help"])),
    PytestAction("PARSE_ARGS_UNINIT_002",
        name="Parse passed args with uninitialized argparser",
        action=Session().parse_args, kwargs={"args": ["--help"]},
        exception=SystemExit),  # argparse throws SystemExit on --help
    PytestAction("PARSE_ARGS_UNINT_003",
        name="Parse empty args with uninitialized argparser",
        action=Session().parse_args, kwargs={"args": []},
        expected=NO_EXPECTED_VALUE),
    PytestAction("PARSE_ARGS_UNINIT_004",
        name="Parse sys.argv '--quiet' with uninitialized argparser",
        action=Session().parse_args,
        exception=SystemExit,   # With no options set, argparse should error on unknown args
        extra=parseargs_helper(["--quiet"])),
    PytestAction("PARSE_ARGS_UNINIT_005",
        name="Parse args - invalid type (int) with uninitialized argparser",
        action=Session().parse_args, kwargs={"args": 123},
        exception=SimpleBenchTypeError,
        exception_tag=_SessionErrorTag.PARSE_ARGS_INVALID_ARGS_TYPE),
    PytestAction("PARSE_ARGS_UNINIT_006",
        name="Parse args - invalid type (list with non-str) with uninitialized argparser",
        action=Session().parse_args, kwargs={"args": ["--json", 123]},
        exception=SimpleBenchTypeError,
        exception_tag=_SessionErrorTag.PARSE_ARGS_INVALID_ARGS_TYPE),
])
def test_uninitialized_parse_args(testspec: TestAction) -> None:
    """Tests the parse_args method of the Session class.

    :param testspec: The test specification to run.
    :type testspec: TestAction
    """
    setup(testspec.extra)
    testspec.run()
    teardown(testspec.extra)


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


def parse_args_testspecs() -> list[TestSpec]:
    """Generate testspecs for the parse_args method of a Session instance with reporters loaded."""
    testspecs: list[TestSpec] = [
        PytestAction("PARSE_ARGS_001",
            name="Parse '--help' with initialized argparser",
            action=session_factory(cache_id='PARSE_ARGS_001').parse_args, args=[["--help"]],
            exception=SystemExit),  # argparse throws SystemExit on --help
        PytestAction("PARSE_ARGS_002",
            name="Parse '--json' with initialized argparser (.json should be [['console']])",
            action=session_factory(cache_id='PARSE_ARGS_002').parse_args, args=[["--json", "console"]],
            obj=session_factory(cache_id='PARSE_ARGS_002'),
            validate_obj=lambda obj: collect_arg_list(args=obj.args, flag="--json") == ["console"],
            expected=NO_EXPECTED_VALUE),
        PytestAction("PARSE_ARGS_003",
            name="Parse no arguments with initialized argparser (.json should be False)",
            action=session_factory(cache_id='PARSE_ARGS_003').parse_args, args=[[]],
            obj=session_factory(cache_id='PARSE_ARGS_003'),
            validate_obj=lambda obj: not obj.args.json,
            expected=NO_EXPECTED_VALUE),
    ]
    return testspecs


@pytest.mark.parametrize("testspec", parse_args_testspecs())
def test_parse_args(testspec: TestAction) -> None:
    """Tests the parse_args method of a Session instance with reporters loaded.

    :param testspec: The test specification to run.
    :type testspec: TestAction
    """
    setup(testspec.extra)
    testspec.run()
    teardown(testspec.extra)


def reading_properties_testspec() -> list[TestSpec]:
    """Generate testspecs for reading Session properties.

    :return: A list of TestSpecs for testing Session properties.
    :rtype: list[TestSpec]
    """
    session_kwargs = session_kwargs_factory()

    testspecs: list[TestSpec] = [
        PytestAction("READ_PROP_001",
            name="Read 'cases' property",
            action=Session, kwargs=session_kwargs,
            validate_attr="cases",
            assertion=Assert.EQUAL,
            expected=session_kwargs['cases'],
        ),
        PytestAction("READ_PROP_002",
            name="Read 'default_runners' property",
            action=Session, kwargs=session_kwargs,
            validate_attr="default_runners",
            assertion=Assert.IS,
            expected=session_kwargs['default_runners'],
        ),
        PytestAction("READ_PROP_003",
            name="Read 'args_parser' property",
            action=Session, kwargs=session_kwargs,
            validate_attr="args_parser",
            assertion=Assert.IS,
            expected=session_kwargs['args_parser'],
        ),
        PytestAction("READ_PROP_004",
            name="Read 'verbosity' property",
            action=Session, kwargs=session_kwargs,
            validate_attr="verbosity",
            assertion=Assert.EQUAL,
            expected=session_kwargs['verbosity'],
        ),
        PytestAction("READ_PROP_005",
            name="Read 'progress' property",
            action=Session, kwargs=session_kwargs,
            validate_attr="progress",
            assertion=Assert.ISINSTANCE,
            expected=Progress,
        ),
        PytestAction("READ_PROP_006",
            name="Read 'output_path' property",
            action=Session, kwargs=session_kwargs,
            validate_attr="output_path",
            assertion=Assert.IS,
            expected=session_kwargs['output_path'],
        ),
        PytestAction("READ_PROP_007",
            name="Read 'console' property",
            action=Session, kwargs=session_kwargs,
            validate_attr="console",
            assertion=Assert.IS,
            expected=session_kwargs['console'],
        ),
        PytestAction("READ_PROP_008",
            name="Read 'show_progress' property",
            action=Session, kwargs=session_kwargs,
            validate_attr="show_progress",
            assertion=Assert.EQUAL,
            expected=session_kwargs['show_progress'],
        ),
        PytestAction("READ_PROP_009",
            name="Read 'reporter_manager' property",
            action=Session, kwargs=session_kwargs,
            validate_attr="reporter_manager",
            assertion=Assert.ISINSTANCE,
            expected=ReporterManager,
        ),
        PytestAction("READ_PROP_010",
            name="Read 'tasks' property",
            action=Session, kwargs=session_kwargs,
            validate_attr="tasks",
            assertion=Assert.ISINSTANCE,
            expected=RichProgressTasks,
        ),
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
    session.add_reporter_flags()
    updated_args = vars(session.args_parser.parse_args([]))
    test_counter = 1
    testspecs: list[TestAction] = []
    for reporter in reporters.values():
        for choice in reporter.choices.values():
            for flag in choice.flags:
                testspecs.append(idspec(
                    f"ADD_FLAG_{test_counter:03}",
                    TestAction(
                        name=f"Flag '{flag}' from choice '{choice.name}' was added to argparser",
                        action=updated_args.__contains__,
                        args=[flag_to_arg(flag)],
                        assertion=Assert.EQUAL,
                        expected=True,
                    )
                ))
                test_counter += 1
    testspecs.append(idspec(
        f"ADD_FLAG_{test_counter:03}",
        TestAction(
            name="Sanity check that at least one flag value was set",
            action=len,
            args=[testspecs],
            assertion=Assert.GREATER_THAN_OR_EQUAL,
            expected=1)
    ))
    test_counter += 1

    # Try to add a reporter flag that duplicates an existing flag we know exists
    # We get a flag from CSVConfig so we can pre-add it to the argparser to cause a duplicate
    # when we try to add it again via add_reporter_flags
    # This should raise a SimpleBenchArgumentError and tests that the error handling works
    csv_config = CSVConfig()
    choices = csv_config.choices
    choice_conf = next(iter(choices.values()))  # first choice
    flags = choice_conf.flags
    arg_parser = ArgumentParser()
    for flag in flags:
        arg_parser.add_argument(flag, action='store_true')  # pre-add to create duplicate
    session = Session(args_parser=arg_parser)
    testspecs.append(idspec(
        f"ADD_FLAG_{test_counter:03}",
        TestAction(
            name="Adding duplicate flag to argparser raises SimpleBenchArgumentError",
            action=session.add_reporter_flags,
            exception=SimpleBenchArgumentError,
            exception_tag=_SessionErrorTag.ARGUMENT_ERROR_ADDING_FLAGS
        )
    ))
    test_counter += 1

    return testspecs


@pytest.mark.parametrize("testspec", session_add_reporter_flags_testspecs())
def test_session_add_reporter_flags(testspec: TestAction) -> None:
    """Tests the add_reporter_flags method of the Session class."""
    testspec.run()


def session_report_keys_testspec() -> list[TestSpec]:
    """Tests the report_keys method of the Session class."""
    csv_config = CSVConfig()
    csv_choices: ChoicesConf = csv_config.choices
    first_choice: ChoiceConf = next(iter(csv_choices.values()))
    flag = list(first_choice.flags)[0]
    arg = flag_to_arg(flag)
    argv = [flag, "filesystem"]
    session = Session()
    session.parse_args(args=argv)
    testspecs = [
        idspec(
            "REPORT_KEYS_001",
            TestAction(
                name="Session.report_keys returns correct set key",
                action=session.report_keys,
                assertion=Assert.EQUAL,
                expected=[arg],
            )
        )
    ]
    return testspecs


@pytest.mark.parametrize("testspec", session_report_keys_testspec())
def test_session_report_keys(testspec: TestAction) -> None:
    """Tests the report_keys method of the Session class."""
    testspec.run()
