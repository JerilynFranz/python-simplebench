"""Tests for simplebench.reporters.choices module."""
from argparse import Namespace
from functools import cache
from pathlib import Path
from typing import Sequence, Optional

import pytest

from simplebench.case import Case
from simplebench.exceptions import SimpleBenchValueError, SimpleBenchTypeError, SimpleBenchKeyError
from simplebench.session import Session
from simplebench.reporters.protocols import ReporterCallback
from simplebench.enums import Section, Target, Format, FlagType
from simplebench.reporters.reporter import Reporter, ReporterOptions
from simplebench.reporters.choice import Choice
from simplebench.reporters.choices import Choices, ChoicesErrorTag

from ..kwargs import ChoicesKWArgs
from ..testspec import TestSpec, TestAction, idspec, Assert, NO_EXPECTED_VALUE


class MockReporterExtras:
    """A mock ReporterExtras subclass for testing Choice initialization."""
    def __init__(self, full_data: bool = False) -> None:
        self.full_data = full_data


class MockReporter(Reporter):
    """A mock Reporter subclass for testing Choice initialization."""
    def __init__(self) -> None:  # pylint: disable=useless-parent-delegation
        super().__init__(
            name='mock',
            description='Mock reporter.',
            sections={Section.OPS, Section.TIMING, Section.MEMORY, Section.PEAK_MEMORY},
            default_targets={Target.CONSOLE},
            targets={Target.FILESYSTEM, Target.CALLBACK},
            subdir='mockreports',
            options_type=ReporterOptions,
            file_suffix='mock',
            file_unique=True,
            file_append=False,
            formats={Format.JSON},
            choices=Choices([
                Choice(
                    reporter=self,
                    flags=['--mock'],
                    flag_type=FlagType.BOOLEAN,
                    name='mock',
                    description='statistical results to mock',
                    sections=[Section.OPS, Section.TIMING, Section.MEMORY, Section.PEAK_MEMORY],
                    targets=[Target.FILESYSTEM, Target.CALLBACK, Target.CONSOLE],
                    output_format=Format.JSON,
                    file_suffix='mock',
                    file_unique=True,
                    file_append=False,
                    options=ReporterOptions(),
                    extra=MockReporterExtras(full_data=False)),
            ]))

    def run_report(self,
                   *,
                   args: Namespace,
                   case: Case,
                   choice: Choice,
                   path: Optional[Path] = None,
                   session: Optional[Session] = None,
                   callback: Optional[ReporterCallback] = None) -> None:
        """Mock implementation of run_report."""

    def render(self, *, case: Case, section: Section, options: ReporterOptions) -> str:
        return "mocked_rendered_output"


@cache
def sample_reporter() -> Reporter:
    """Factory function to return a sample MockReporter instance for testing."""
    return MockReporter()


@cache
def choice_instance(cache_id: str = 'default', *,  # pylint: disable=unused-argument
                    name: str = 'mock', flags: Sequence[str] = ('--mock',)) -> Choice:
    """Factory function to return the same mock Choice instance for testing."""
    return Choice(
        reporter=sample_reporter(),
        flags=flags,
        flag_type=FlagType.BOOLEAN,
        name=name,
        description='A mock choice.',
        sections=[Section.OPS], targets=[Target.CONSOLE],
        output_format=Format.JSON,
        extra='mock_extra')


@pytest.mark.parametrize(
    "testspec", [
        idspec('INIT_001', TestAction(
            name="Choices with a list of Choice instances",
            action=Choices,
            kwargs=ChoicesKWArgs(
                choices=[
                    choice_instance(),
                ]),
            validate_result=lambda result: len(result) == 1 and result['mock'] is choice_instance(),
            assertion=Assert.ISINSTANCE,
            expected=Choices)),
        idspec('INIT_002', TestAction(
            name="Missing choices argument - creates default empty Choices",
            action=Choices,
            kwargs=ChoicesKWArgs(),
            validate_result=lambda result: len(result) == 0,
            assertion=Assert.ISINSTANCE,
            expected=Choices)),
        idspec('INIT_003', TestAction(
            name="Choices initialized using a different Choices instance",
            action=Choices,
            kwargs=ChoicesKWArgs(choices=Choices(choices=[choice_instance()])),
            validate_result=lambda result: len(result) == 1 and result['mock'] is choice_instance(),
            assertion=Assert.ISINSTANCE,
            expected=Choices)),
        idspec('INIT_004', TestAction(
            name="Choices with invalid choices argument type - raises SimpleBenchTypeError",
            action=Choices,
            kwargs=ChoicesKWArgs(choices='not_a_sequence'),  # type: ignore[arg-type]
            exception=SimpleBenchTypeError,
            exception_tag=ChoicesErrorTag.INVALID_CHOICES_ARG_TYPE,
        )),
    ]
)
def test_choices_init(testspec: TestSpec):
    """Test initializing Choices with various combinations of keyword arguments.

    This test verifies that the Choices class can be initialized correctly
    using different combinations of parameters provided through the
    ChoicesKWArgs class. It checks that the attributes of the Choices instance
    match the expected values based on the provided keyword arguments.
    """
    testspec.run()


@cache
def choices_instance(cache_id: str = "default", *,  # pylint: disable=unused-argument
                     choices: Sequence[Choice] | Choices | None = None) -> Choices:
    """Factory function to return a cached Choices instance for testing.

    Args:
        cache_id (str, default="default"):
            An identifier to cache different Choices instances if needed.
        choices (Sequence[Choice] | Choices | None, default=None):
            A sequence of Choice instances or a Choices instance to initialize the Choices instance.
    """
    return Choices() if choices is None else Choices(choices=choices)


@pytest.mark.parametrize(
    "testspec", [
        idspec("ADD_001", TestAction(
            name="Add valid Choice instance to Choices via choices.add(<keyword-argument>)",
            obj=choices_instance('ADD_001'),
            action=choices_instance('ADD_001').add,
            kwargs={'choice': choice_instance()},
            validate_obj=lambda choices: len(choices) == 1 and choices['mock'] is choice_instance(),
            expected=NO_EXPECTED_VALUE,
        )),
        idspec("ADD_002", TestAction(
            name="Add valid Choice instance to Choices via choices.add(<positional-argument>)",
            obj=choices_instance('ADD_002'),
            action=choices_instance('ADD_002').add,
            args=[choice_instance()],
            validate_obj=lambda choices: len(choices) == 1 and choices['mock'] is choice_instance(),
            expected=NO_EXPECTED_VALUE,
        )),
        idspec("ADD_003", TestAction(
            name="Add invalid type of object to Choices - raises SimpleBenchTypeError",
            obj=choices_instance('ADD_003'),
            action=choices_instance('ADD_003').add,
            args=['not_a_choice'],  # type: ignore[arg-type]
            exception=SimpleBenchTypeError,
            exception_tag=ChoicesErrorTag.ADD_INVALID_CHOICE_ARG_TYPE,
        )),
        idspec("ADD_004", TestAction(
            name="Add different Choice name to Choices",
            obj=choices_instance("ADD_004", choices=(choice_instance(
                "ADD_004", name='unique_choice', flags=('--unique-choice',)),)),
            action=choices_instance("ADD_004", choices=(choice_instance(
                "ADD_004", name='unique_choice', flags=('--unique-choice',)),)).add,
            args=[choice_instance(
                "ADD_004", name='another_unique_choice', flags=('--another-unique-choice',))],
            validate_obj=lambda choices: (
                len(choices) == 2 and
                choices['unique_choice'] is choice_instance(
                    "ADD_004", name='unique_choice', flags=('--unique-choice',)) and
                choices['another_unique_choice'] is choice_instance(
                    "ADD_004", name='another_unique_choice', flags=('--another-unique-choice',))),
            expected=NO_EXPECTED_VALUE,
        )),
        idspec("ADD_005", TestAction(
            name="Add duplicate Choice to Choices - raises SimpleBenchValueError",
            obj=choices_instance('ADD_005', choices=(choice_instance(),)),
            action=choices_instance('ADD_005', choices=(choice_instance(),)).add,
            args=[choice_instance()],
            exception=SimpleBenchValueError,
            exception_tag=ChoicesErrorTag.SETITEM_DUPLICATE_CHOICE_NAME)
        ),
    ]
)
def test_choices_add_method(testspec: TestSpec) -> None:
    """Test the Choices.add() method."""
    testspec.run()


@pytest.mark.parametrize(
    "testspec", [
        idspec("ALL_CHOICE_ARGS_001", TestAction(
            name="Get all Choice args from Choices with no choices (expect empty set)",
            action=Choices().all_choice_args,
            assertion=Assert.EQUAL,
            expected=set(),
        )),
        idspec("ALL_CHOICE_ARGS_002", TestAction(
            name="Get all Choice args from Choices with multiple choices",
            action=Choices(choices=[
                choice_instance('ALL_CHOICE_ARGS_002', name='choice_one', flags=('--one',)),
                choice_instance('ALL_CHOICE_ARGS_002', name='choice_two', flags=('--two', '--deux')),
                choice_instance('ALL_CHOICE_ARGS_002', name='choice_three', flags=('--three',)),
                choice_instance('ALL_CHOICE_ARGS_002', name='choice_four', flags=('--fourth-item',)),
            ]).all_choice_args,
            assertion=Assert.EQUAL,
            expected={'one', 'two', 'deux', 'three', 'fourth_item'},
        )),
    ])
def test_choices_all_choice_args_method(testspec: TestSpec) -> None:
    """Test the Choices.all_choice_args() method."""
    testspec.run()


@pytest.mark.parametrize(
    "testspec", [
        idspec("ALL_CHOICE_FLAGS_001", TestAction(
            name="Get all Choice flags from Choices with no choices (expect empty set)",
            action=Choices().all_choice_flags,
            assertion=Assert.EQUAL,
            expected=set(),
        )),
        idspec("ALL_CHOICE_FLAGS_002", TestAction(
            name="Get all Choice flags from Choices with multiple choices",
            action=Choices(choices=[
                choice_instance('ALL_CHOICE_FLAGS_002', name='choice_one', flags=('--one',)),
                choice_instance('ALL_CHOICE_FLAGS_002', name='choice_two', flags=('--two', '--deux')),
                choice_instance('ALL_CHOICE_FLAGS_002', name='choice_three', flags=('--three',)),
                choice_instance('ALL_CHOICE_FLAGS_002', name='choice_four', flags=('--fourth-item',)),
            ]).all_choice_flags,
            assertion=Assert.EQUAL,
            expected={'--one', '--two', '--deux', '--three', '--fourth-item'},
        )),
    ])
def test_choices_all_choice_flags_method(testspec: TestSpec) -> None:
    """Test the Choices.all_choice_flags() method."""
    testspec.run()


@pytest.mark.parametrize(
    "testspec", [
        idspec("GET_CHOICE_FOR_ARG_001", TestAction(
            name="Get Choice for existing arg",
            action=Choices(choices=[
                choice_instance('GET_CHOICE_FOR_ARG_001', name='choice_one', flags=('--one',)),
                choice_instance('GET_CHOICE_FOR_ARG_001', name='choice_two', flags=('--two', '--deux')),
            ]).get_choice_for_arg,
            args=['one'],
            assertion=Assert.IS,
            expected=choice_instance('GET_CHOICE_FOR_ARG_001', name='choice_one', flags=('--one',)),
        )),
        idspec("GET_CHOICE_FOR_ARG_002", TestAction(
            name="Get non-existing Choice arg (expect None)",
            action=Choices(choices=[
                choice_instance('GET_CHOICE_FOR_ARG_002', name='choice_one', flags=('--one',)),
                choice_instance('GET_CHOICE_FOR_ARG_002', name='choice_two', flags=('--two', '--deux')),
            ]).get_choice_for_arg,
            args=['nonexistent'],
            assertion=Assert.IS,
            expected=None,
        )),
        idspec("GET_CHOICE_FOR_ARG_003", TestAction(
            name="Get Choice with wrong type arg (raises SimpleBenchTypeError)",
            action=Choices(choices=[
                choice_instance('GET_CHOICE_FOR_ARG_003', name='choice_one', flags=('--one',)),
                choice_instance('GET_CHOICE_FOR_ARG_003', name='choice_two', flags=('--two', '--deux')),
            ]).get_choice_for_arg,
            args=[123],  # type: ignore[arg-type]
            exception=SimpleBenchTypeError,
            exception_tag=ChoicesErrorTag.GET_CHOICE_FOR_ARG_INVALID_ARG_TYPE,
        )),
    ])
def test_choices_get_choice_for_arg_method(testspec: TestSpec) -> None:
    """Test the Choices.get_choice_for_arg() method."""
    testspec.run()


@pytest.mark.parametrize(
    "testspec", [
        idspec("EXTENDS_001", TestAction(
            name="Choices extend - add two choices via extend([<choice1>, <choice2>]) and access them via dict key",
            obj=choices_instance("EXTENDS_001"),
            action=choices_instance("EXTENDS_001").extend,
            args=[[
                choice_instance('EXTENDS_001', name='choice_one', flags=('--one',)),
                choice_instance('EXTENDS_001', name='choice_two', flags=('--two',))]],
            validate_obj=lambda choices: (
                len(choices) == 2 and
                choices['choice_one'] is choice_instance('EXTENDS_001', name='choice_one', flags=('--one',)) and
                choices['choice_two'] is choice_instance('EXTENDS_001', name='choice_two', flags=('--two',))
            ),
        )),
        idspec("EXTENDS_002", TestAction(
            name="Choices extend - add two choices via extend(<choices>]) and access them via dict key",
            obj=choices_instance("EXTENDS_002"),
            action=choices_instance("EXTENDS_002").extend,
            args=[Choices(choices=[
                choice_instance('EXTENDS_002', name='choice_three', flags=('--three',)),
                choice_instance('EXTENDS_002', name='choice_four', flags=('--four',)),
            ])],
            validate_obj=lambda choices: (
                len(choices) == 2 and
                choices['choice_three'] is choice_instance('EXTENDS_002', name='choice_three', flags=('--three',)) and
                choices['choice_four'] is choice_instance('EXTENDS_002', name='choice_four', flags=('--four',))
            ),
        )),
        idspec("EXTENDS_003", TestAction(
            name="Choices extend - add invalid type (raises SimpleBenchTypeError)",
            obj=choices_instance("EXTENDS_003"),
            action=choices_instance("EXTENDS_003").extend,
            args=['not_a_sequence'],  # type: ignore[arg-type]
            exception=SimpleBenchTypeError,
            exception_tag=ChoicesErrorTag.EXTEND_INVALID_CHOICES_ARG_SEQUENCE_TYPE,
        )),
        idspec("EXTENDS_004", TestAction(
            name="Choices extend - add two choices via extend([<choice1>, <choice2>]) and access them via dict key",
            obj=choices_instance("EXTENDS_001"),
            action=choices_instance("EXTENDS_001").extend,
            args=[[
                choice_instance('EXTENDS_001', name='choice_one', flags=('--one',)),
                'something_invalid']],
            exception=SimpleBenchTypeError,
            exception_tag=ChoicesErrorTag.EXTEND_INVALID_CHOICES_ARG_SEQUENCE_TYPE,
        )),
    ])
def test_choices_extend(testspec: TestSpec) -> None:
    """Test the Choices extend() method."""
    testspec.run()


@pytest.mark.parametrize(
    "testspec", [
        idspec("REMOVE_001", TestAction(
            name="Remove existing Choice from Choices",
            obj=choices_instance("REMOVE_001", choices=(
                choice_instance('REMOVE_001', name='choice_to_remove', flags=('--remove-me',)),
            )),
            action=choices_instance("REMOVE_001", choices=(
                choice_instance('REMOVE_001', name='choice_to_remove', flags=('--remove-me',)),
            )).remove,
            args=['choice_to_remove'],
            validate_obj=lambda choices: (
                len(choices) == 0
            ),
        )),
        idspec("REMOVE_002", TestAction(
            name="Remove non-existing Choice from Choices (raises SimpleBenchKeyError)",
            obj=choices_instance("REMOVE_002", choices=(
                choice_instance('REMOVE_002', name='existing_choice', flags=('--i-exist',)),
            )),
            action=choices_instance("REMOVE_002", choices=(
                choice_instance('REMOVE_002', name='existing_choice', flags=('--i-exist',)),
            )).remove,
            args=['non_existing_choice'],
            exception=SimpleBenchKeyError,
            exception_tag=ChoicesErrorTag.DELITEM_UNKNOWN_CHOICE_NAME
        )),
    ])
def test_choices_remove(testspec: TestSpec) -> None:
    """Test the Choices.remove() method."""
    testspec.run()


@pytest.mark.parametrize(
    "testspec", [
        idspec("SETITEM_001", TestAction(
            name="Set item via __setitem__ method with valid Choice",
            obj=choices_instance("SETITEM_001"),
            action=choices_instance("SETITEM_001").__setitem__,
            args=['new_choice', choice_instance(
                'SETITEM_001', name='new_choice', flags=('--new-choice',))],
            validate_obj=lambda choices: (
                len(choices) == 1 and
                choices['new_choice'] is choice_instance(
                    'SETITEM_001', name='new_choice', flags=('--new-choice',))
            ),
        )),
        idspec("SETITEM_002", TestAction(
            name="Set item via __setitem__ method with invalid key type (raises SimpleBenchTypeError)",
            obj=choices_instance("SETITEM_002"),
            action=choices_instance("SETITEM_002").__setitem__,
            args=[123, choice_instance(
                'SETITEM_002', name='some_choice', flags=('--some-choice',))],
            exception=SimpleBenchTypeError,
            exception_tag=ChoicesErrorTag.SETITEM_INVALID_KEY_TYPE,
        )),
        idspec("SETITEM_003", TestAction(
            name="Set item via __setitem__ method with invalid type (raises SimpleBenchTypeError)",
            obj=choices_instance("SETITEM_003"),
            action=choices_instance("SETITEM_003").__setitem__,
            args=['invalid_choice', 'not_a_choice_instance'],
            exception=SimpleBenchTypeError,
            exception_tag=ChoicesErrorTag.SETITEM_INVALID_VALUE_TYPE,
        )),
        idspec("SETITEM_004", TestAction(
            name="Set item via __setitem__ method with mismatched choice name (raises SimpleBenchValueError)",
            obj=choices_instance("SETITEM_004"),
            action=choices_instance("SETITEM_004").__setitem__,
            args=['mismatched_name', choice_instance(
                'SETITEM_004', name='actual_name', flags=('--some-flag',))],
            exception=SimpleBenchValueError,
            exception_tag=ChoicesErrorTag.SETITEM_KEY_NAME_MISMATCH,
        )),
        idspec("SETITEM_005", TestAction(
            name="Set item via __setitem__ method with duplicate choice name (raises SimpleBenchValueError)",
            obj=choices_instance("SETITEM_005", choices=(
                choice_instance('SETITEM_005', name='duplicate_choice', flags=('--dup-flag',)),
            )),
            action=choices_instance("SETITEM_005", choices=(
                choice_instance('SETITEM_005', name='duplicate_choice', flags=('--dup-flag',)),
            )).__setitem__,
            args=['duplicate_choice', choice_instance(
                'SETITEM_005', name='duplicate_choice', flags=('--another-flag',))],
            exception=SimpleBenchValueError,
            exception_tag=ChoicesErrorTag.SETITEM_DUPLICATE_CHOICE_NAME,
        )),
        idspec("SETITEM_006", TestAction(
            name="Set item via __setitem__ method with duplicate flag (across choices) (raises SimpleBenchValueError)",
            obj=choices_instance("SETITEM_006", choices=(
                choice_instance('SETITEM_006', name='existing_choice', flags=('--common-flag',)),
            )),
            action=choices_instance("SETITEM_006", choices=(
                choice_instance('SETITEM_006', name='existing_choice', flags=('--common-flag',)),
            )).__setitem__,
            args=['new_choice', choice_instance(
                'SETITEM_006', name='new_choice', flags=('--common-flag',))],
            exception=SimpleBenchValueError,
            exception_tag=ChoicesErrorTag.SETITEM_DUPLICATE_CHOICE_FLAG,
        )),
    ])
def test_setitem_dunder_method(testspec: TestSpec) -> None:
    """Test that the __setitem__ dunder method of Choices works correctly."""
    testspec.run()
