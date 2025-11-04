"""Tests for simplebench.reporters.choices module."""
# pylint: disable=unnecessary-direct-lambda-call
from argparse import Namespace
from functools import lru_cache
from pathlib import Path
from typing import Optional, Any

import pytest

from simplebench.case import Case
from simplebench.exceptions import SimpleBenchValueError, SimpleBenchTypeError, SimpleBenchKeyError
from simplebench.session import Session
from simplebench.reporters.protocols import ReporterCallback
from simplebench.enums import Section, Target, Format, FlagType
from simplebench.reporters.reporter import Reporter, ReporterOptions
from simplebench.reporters.choice import Choice, ChoiceConf
from simplebench.reporters.choices import Choices, ChoicesErrorTag

from ..kwargs import ChoicesKWArgs
from ..testspec import TestSpec, TestAction, TestGet, idspec, Assert


@lru_cache(typed=True)
def choice_conf_instance(cache_id: str = 'default',  # pylint: disable=unused-argument
                         name: str = 'mock', flags: tuple[str, ...] = ('--mock',)) -> ChoiceConf:
    """Factory function to return the same mock ChoiceConf instance for testing.

    It caches the instance based on the cache_id so that multiple calls with the same
    cache_id return the same instance.

    Args:
        cache_id (str, default='default'):
            An identifier to cache different ChoiceConf instances if needed.
        name (str, default='mock'):
            The name of the ChoiceConf instance.
        flags (tuple[str, ...], default=('--mock',)):
            The flags associated with the ChoiceConf instance.
    """
    return ChoiceConf(
        flags=flags,
        flag_type=FlagType.BOOLEAN,
        name=name,
        description='A mock choice.',
        sections=[Section.OPS], targets=[Target.CONSOLE],
        output_format=Format.JSON,
        file_suffix='mock',
        file_unique=True,
        file_append=False,
        options=ReporterOptions(),
        extra='mock_extra')


@lru_cache(typed=True)
def choice_instance(cache_id: str = 'default',
                    name: str = 'mock',
                    flags: tuple[str, ...] = ('--mock',)) -> Choice:
    """Factory function to return a single cached Choice instance for testing.

    The caching ensures *identity* of the Choice instance across multiple calls.
    Because Choice instances are immutable, this is safe to do. It effectively
    makes the Choice instance a singleton per cache_id, name, and flags.

    The choice instance is created using MockReporter() and is
    extracted from the MockReporter.choices attribute.

    It is cached based on the cache_id so that multiple calls with the same
    cache_id, name, and flags return the same instance.

    The default Choice instance has the name 'mock' and flag '--mock'.

    Args:
        cache_id (str, default="default"):
            An identifier to cache different Choice instances if needed.
        name (str, default='mock'):
            The name of the Choice instance.
        flags (tuple[str, ...], default=('--mock',)):
            The flags associated with the Choice instance.
    """
    choice_conf = choice_conf_instance(cache_id, name=name, flags=flags)
    reporter = reporter_instance(cache_id, choice_confs=(choice_conf,))
    return reporter.choices[name]


@lru_cache(typed=True)
def reporter_instance(cache_id: str = "default",  # pylint: disable=unused-argument
                      choice_confs: tuple[ChoiceConf, ...] | None = None) -> Reporter:
    """Factory function to return a cached Reporter instance for testing.

    The instance is a MockReporter. It is cached based on the cache_id.
    This makes it possible to have multiple cached instances and for
    each to retain its own state if needed.

    Args:
        cache_id (str, default="default"):
            An identifier to cache different Reporter instances if needed.
        choice_confs (tuple[ChoiceConf, ...] | None, default=None):
            A tuple of ChoiceConf instances to initialize the Reporter with.
    """
    return MockReporter(choice_confs=choice_confs)


@lru_cache(typed=True)
def choices_instance(cache_id: str = "default", *,  # pylint: disable=unused-argument
                     choices: tuple[Choice, ...] | Choices | None = None) -> Choices:
    """Factory function to return a cached Choices instance for testing.

    Args:
        cache_id (str, default="default"):
            An identifier to cache different Choices instances if needed.
        choices (tuple[Choice, ...] | Choices | None, default=None):
            A sequence of Choice instances or a Choices instance to initialize the Choices instance.
    """
    if choices is None:
        result = Choices()
        if not isinstance(result, Choices):
            raise TypeError(f"{cache_id}: Invalid type for choices instance: {result!r}")
        return result
    if isinstance(choices, Choices):
        result = Choices(choices)
        if not isinstance(result, Choices):
            raise TypeError(f"{cache_id}: Invalid type for choices instance: {result!r}")
        return result
    if isinstance(choices, tuple) and all(isinstance(c, Choice) for c in choices):
        result = Choices(choices=choices)
        if not isinstance(result, Choices):
            raise TypeError(f"{cache_id}: Invalid type for choices instance: {result!r}")
        return result
    raise TypeError(f"Invalid type for choices argument: {choices!r}")


class MockReporterExtras:
    """A mock ReporterExtras subclass for testing Choice initialization."""
    def __init__(self, full_data: bool = False) -> None:
        self.full_data = full_data


class MockReporter(Reporter):
    """A mock Reporter subclass for testing Choice initialization.

    It provides a minimal implementation of the abstract methods required by the Reporter base class.

    It initializes with a single ChoiceConf instance for testing purposes by default.
    This can be overridden by providing a different list of ChoiceConf instances.

    The default ChoiceConf instance is created using the choice_conf_instance factory function and
    has the name 'mock' and flag '--mock'.

    Args
    """
    def __init__(  # pylint: disable=useless-parent-delegation
            self, choice_confs: tuple[ChoiceConf, ...] | None = None) -> None:
        """Constructs a MockReporter instance for testing.

        A single ChoiceConf instance is used by default for testing purposes.
        This can be overridden by providing a different list of ChoiceConf instances.

        The default ChoiceConf instance is created using the choice_conf_instance
        factory function and has the name 'mock' and flag '--mock'.

        Args:
            choice_confs (tuple[ChoiceConf, ...] | None, default=None):
                A tuple of ChoiceConf instances to initialize the Reporter with.
                If None, a single default ChoiceConf instance is used.
        """
        choice_confs = choice_confs or (choice_conf_instance(),)
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
            choices=choice_confs
        )

    def run_report(self,
                   *,
                   args: Namespace,
                   case: Case,
                   choice: Choice,
                   path: Optional[Path] = None,
                   session: Optional[Session] = None,
                   callback: Optional[ReporterCallback] = None) -> None:
        """Mock implementation of run_report."""

    def render(
            self, *, case: Case, section: Section, options: ReporterOptions) -> str:  # pylint: disable=unused-argument
        """Mock implementation of render method."""
        return "mocked_rendered_output"


@lru_cache(typed=True)
def sample_reporter() -> Reporter:
    """Factory function to return a sample MockReporter instance for testing."""
    return MockReporter()


def assert_helper(testspec: TestSpec, result: Any, msg: str | None = None) -> None:
    """Helper function to perform assertions in tests."""
    if not isinstance(testspec, TestSpec):
        raise TypeError(f"Invalid testspec type in validation: {type(testspec)}")
    if not result:
        if msg is None:
            msg = "Validation assertion failed."
        pytest.fail(f"validate assertion failed for testspec: {testspec}: {msg}")


@pytest.mark.parametrize(
    "testspec", [
        idspec('INIT_001', TestGet(
            name="Choices with a list of Choice instances from a MockReporter",
            obj=MockReporter(),
            attribute='choices',
            assertion=Assert.ISINSTANCE,
            expected=Choices)),
        idspec('INIT_002', TestGet(
            name="Get Choice instance from Choices using dict key access",
            obj=reporter_instance('INIT_002'),
            attribute='choices',
            validate=lambda testspec, obj: assert_helper(
                testspec, 'mock' in obj.choices, 'Expected "mock" key in Choices instance.'))),
        idspec('INIT_003', TestAction(
            name="No arguments - creates default empty Choices",
            action=Choices,
            validate_result=lambda result: len(result) == 0,
            assertion=Assert.ISINSTANCE,
            expected=Choices)),
        idspec('INIT_004', TestAction(
            name="Choices initialized using from a different Choices instance",
            action=Choices,
            kwargs=ChoicesKWArgs(choices=MockReporter().choices),
            validate_result=lambda result: len(result) == 1 and 'mock' in result,
            assertion=Assert.ISINSTANCE,
            expected=Choices)),
        idspec("INIT_005", TestAction(
            name="Choices initialized from an Iterable of Choice instances",
            action=Choices,
            kwargs=ChoicesKWArgs(choices=list(MockReporter().choices.values())),
            validate_result=lambda result: len(result) == 1 and 'mock' in result,
            assertion=Assert.ISINSTANCE,
            expected=Choices)),
        idspec('INIT_006', TestAction(
            name="Choices with invalid choices argument type - raises SimpleBenchTypeError",
            action=Choices,
            kwargs=ChoicesKWArgs(choices='not_a_sequence'),  # type: ignore[arg-type]
            exception=SimpleBenchTypeError,
            exception_tag=ChoicesErrorTag.CHOICES_INVALID_ARG_TYPE,
        )),
        idspec('INIT_007', TestAction(
            name="Choices with invalid item in choices argument - raises SimpleBenchTypeError",
            action=Choices,
            kwargs=ChoicesKWArgs(choices=[choice_conf_instance(), 'not_a_choice']),  # type: ignore[list-item]
            exception=SimpleBenchTypeError,
            exception_tag=ChoicesErrorTag.CHOICES_INVALID_ARG_TYPE
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


def choices_add_testspecs() -> list[TestSpec]:
    """Returns a list of TestSpec instances for testing Choices add()"""
    testspecs: list[TestSpec] = []

    def add_choice_to_empty_choices_with_keyword_arg() -> None:
        cache_id = f'{__name__}:ADD_001'
        choices = choices_instance(cache_id)
        choice = choice_instance(cache_id)
        choices.add(choice=choice)
        assert len(choices) == 1 and choices['mock'] is choice
    testspecs.append(
        idspec("ADD_001", TestAction(
            name="Add valid Choice instance to empty Choices via add(<keyword-argument>)",
            action=add_choice_to_empty_choices_with_keyword_arg,
        )))

    def add_choice_to_empty_choices_with_positional_arg() -> None:
        cache_id = f'{__name__}:ADD_002'
        choices = choices_instance(cache_id)
        choice = choice_instance(cache_id)
        choices.add(choice)
        assert len(choices) == 1 and choices['mock'] is choice
    testspecs.append(
        idspec("ADD_002", TestAction(
            name="Add valid Choice instance to empty Choices via add(<positional-argument>)",
            action=add_choice_to_empty_choices_with_positional_arg
        )))

    testspecs.append(
        idspec("ADD_003", TestAction(
            name="Add invalid type of object to Choices with add() - raises SimpleBenchTypeError",
            action=choices_instance(f'{__name__}:ADD_003').add,
            args=['not_a_choice'],
            exception=SimpleBenchTypeError,
            exception_tag=ChoicesErrorTag.ADD_CHOICE_INVALID_ARG_TYPE,
        )))

    def add_second_unique_choice_to_choices() -> None:
        cache_id = f'{__name__}:ADD_004'
        choices = choices_instance(cache_id)
        choice1 = choice_instance(cache_id, name='unique_choice', flags=('--unique-choice',))
        choice2 = choice_instance(cache_id, name='another_unique_choice', flags=('--another-unique-choice',))
        choices.add(choice1)
        choices.add(choice2)
        assert (len(choices) == 2 and
                choices['unique_choice'] is choice1 and
                choices['another_unique_choice'] is choice2)
    testspecs.append(
        idspec("ADD_004", TestAction(
            name="Add second (different) Choice name/flag to Choices using add()",
            action=add_second_unique_choice_to_choices,
        )))

    def add_duplicate_name_choice_to_choices_raises() -> None:
        cache_id = f'{__name__}:ADD_005'
        choices = choices_instance(cache_id)
        choice1 = choice_instance(cache_id, name='duplicate_choice', flags=('--unique-choice1',))
        choice2 = choice_instance(cache_id, name='duplicate_choice', flags=('--unique-choice2',))
        choices.add(choice1)
        choices.add(choice2)  # This should raise
    testspecs.append(
        idspec("ADD_005", TestAction(
            name="Add duplicate name Choice to Choices - raises SimpleBenchValueError",
            action=add_duplicate_name_choice_to_choices_raises,
            exception=SimpleBenchValueError,
            exception_tag=ChoicesErrorTag.SETITEM_DUPLICATE_CHOICE_NAME,
        )))

    return testspecs


@pytest.mark.parametrize("testspec", choices_add_testspecs())
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
            exception_tag=ChoicesErrorTag.EXTEND_CHOICES_INVALID_ARG_TYPE,
        )),
        idspec("EXTENDS_004", TestAction(
            name="Choices extend - add two choices via extend([<choice1>, <choice2>]) and access them via dict key",
            obj=choices_instance("EXTENDS_001"),
            action=choices_instance("EXTENDS_001").extend,
            args=[[
                choice_instance('EXTENDS_001', name='choice_one', flags=('--one',)),
                'something_invalid']],
            exception=SimpleBenchTypeError,
            exception_tag=ChoicesErrorTag.EXTEND_CHOICES_INVALID_ARG_TYPE,
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
