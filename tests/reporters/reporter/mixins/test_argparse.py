"""Tests for argparse mixins in reporters."""
import pytest

from simplebench.enums import Target
from simplebench.exceptions import SimpleBenchTypeError, SimpleBenchValueError
from simplebench.reporters.reporter.exceptions import ReporterErrorTag

from ....factories import (choice_factory, flag_name_factory, reporter_factory,
                           reporter_namespace_factory)
from ....testspec import Assert, TestAction, TestSpec, idspec


@pytest.mark.parametrize('testspec', [
    idspec('SELECT_TARGETS_FROM_ARGS_001', TestAction(
        name="select_targets_from_args() with args specifying console target returns console target",
        action=reporter_factory().select_targets_from_args,
        kwargs={'args': reporter_namespace_factory([flag_name_factory(), Target.CONSOLE.value]),
                'choice': choice_factory(),
                'default_targets': {Target.FILESYSTEM}},
        assertion=Assert.EQUAL,
        expected={Target.CONSOLE})),
    idspec('SELECT_TARGETS_FROM_ARGS_002', TestAction(
        name="select_targets_from_args() with no specified target returns default targets",
        action=reporter_factory().select_targets_from_args,
        kwargs={'args': reporter_namespace_factory([flag_name_factory()]),
                'choice': choice_factory(),
                'default_targets': {Target.FILESYSTEM}},
        assertion=Assert.EQUAL,
        expected={Target.FILESYSTEM})),
    idspec('SELECT_TARGETS_FROM_ARGS_004', TestAction(
        name="select_targets_from_args() with args specifying multiple targets returns all specified targets",
        action=reporter_factory().select_targets_from_args,
        kwargs={'args': reporter_namespace_factory(
                            [flag_name_factory(), Target.CONSOLE.value, Target.FILESYSTEM.value]),
                'choice': choice_factory(),
                'default_targets': {Target.FILESYSTEM}},
        assertion=Assert.EQUAL,
        expected={Target.CONSOLE, Target.FILESYSTEM})),
    idspec('SELECT_TARGETS_FROM_ARGS_005', TestAction(
        name=("select_targets_from_args() incorrect args type raises SimpleBenchTypeError"),
        action=reporter_factory().select_targets_from_args,
        kwargs={'args': "not_a_namespace", 'choice': choice_factory(), 'default_targets': {Target.FILESYSTEM}},
        exception=SimpleBenchTypeError,
        exception_tag=ReporterErrorTag.SELECT_TARGETS_FROM_ARGS_INVALID_ARGS_ARG)),
    idspec('SELECT_TARGETS_FROM_ARGS_006', TestAction(
        name=("select_targets_from_args() incorrect choice type raises SimpleBenchTypeError"),
        action=reporter_factory().select_targets_from_args,
        kwargs={'args': reporter_namespace_factory([flag_name_factory()]),
                'choice': "not_a_choice_instance",
                'default_targets': {Target.FILESYSTEM}},
        exception=SimpleBenchTypeError,
        exception_tag=ReporterErrorTag.SELECT_TARGETS_FROM_ARGS_INVALID_CHOICE_ARG)),
    idspec('SELECT_TARGETS_FROM_ARGS_007', TestAction(
        name=("select_targets_from_args() incorrect default_targets type raises SimpleBenchTypeError"),
        action=reporter_factory().select_targets_from_args,
        kwargs={'args': reporter_namespace_factory([flag_name_factory()]),
                'choice': choice_factory(),
                'default_targets': "not_a_set_of_targets"},
        exception=SimpleBenchTypeError,
        exception_tag=ReporterErrorTag.SELECT_TARGETS_FROM_ARGS_INVALID_DEFAULT_TARGETS_ARG)),
    idspec('SELECT_TARGETS_FROM_ARGS_008', TestAction(
        name="select_targets_from_args() with args including unsupported target raises SimpleBenchValueError",
        action=reporter_factory().select_targets_from_args,
        kwargs={'args': reporter_namespace_factory(
                            args=[flag_name_factory(), Target.CUSTOM.value],
                            choices=[Target.CUSTOM.value, Target.FILESYSTEM.value]),
                'choice': choice_factory(),
                'default_targets': {Target.FILESYSTEM}},
        exception=SimpleBenchValueError,
        exception_tag=ReporterErrorTag.SELECT_TARGETS_FROM_ARGS_UNSUPPORTED_TARGET)),
    idspec('SELECT_TARGETS_FROM_ARGS_009', TestAction(
        name=("select_targets_from_args() with an arg that does not match any "
              "Target enums raises SimpleBenchValueError"),
        action=reporter_factory().select_targets_from_args,
        kwargs={'args': reporter_namespace_factory(
                            args=[flag_name_factory(), "non_existent_target"],
                            choices=["non_existent_target"]),
                'choice': choice_factory(),
                'default_targets': {Target.FILESYSTEM}},
        exception=SimpleBenchValueError,
        exception_tag=ReporterErrorTag.SELECT_TARGETS_FROM_ARGS_UNKNOWN_TARGET_IN_ARGS)),
    idspec('SELECT_TARGETS_FROM_ARGS_010', TestAction(
        name="select_targets_from_args() with default target not supported by choice raises SimpleBenchValueError",
        action=reporter_factory().select_targets_from_args,
        kwargs={'args': reporter_namespace_factory([flag_name_factory()]),
                'choice': choice_factory(),
                'default_targets': {Target.CUSTOM}},
        exception=SimpleBenchValueError,
        exception_tag=ReporterErrorTag.SELECT_TARGETS_FROM_ARGS_DEFAULT_TARGET_UNSUPPORTED)),
])
def test_select_targets_from_args(testspec: TestSpec) -> None:
    """Test Reporter.select_targets_from_args() method."""
    testspec.run()
