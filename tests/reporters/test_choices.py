"""Tests for simplebench.reporters.choices_conf module."""
import pytest

from simplebench.exceptions import SimpleBenchKeyError, SimpleBenchTypeError, SimpleBenchValueError
from simplebench.reporters.choices import Choices, _ChoicesErrorTag

from ..factories import choice_conf_factory, choice_factory, choices_factory, default_choice_name, reporter_factory
from ..kwargs import ChoicesKWArgs
from ..testspec import Assert, TestAction, TestGet, TestSpec, idspec


@pytest.mark.parametrize(
    "testspec", [
        idspec('INIT_001', TestGet(
            name="Choices with a list of Choice instances from a FactoryReporter",
            obj=reporter_factory(cache_id=None),
            attribute='choices',
            assertion=Assert.ISINSTANCE,
            expected=Choices)),
        idspec('INIT_002', TestGet(
            name="Get Choice instance from Choices using dict key access",
            obj=reporter_factory(cache_id=None),
            attribute='choices',
            assertion=Assert.IN,
            expected=default_choice_name())),
        idspec('INIT_003', TestAction(
            name="No arguments - creates empty Choices (len()==0)",
            action=Choices,
            assertion=Assert.LEN,
            expected=0)),
        idspec('INIT_004', TestAction(
            name="Choices initialized from a different Choices instance",
            action=Choices,
            args=[choices_factory(choices=(choice_conf_factory(),), cache_id=None)],
            assertion=Assert.IN,
            expected=default_choice_name())),
        idspec("INIT_005", TestAction(
            name="Choices initialized from an Iterable of Choice instances",
            action=Choices,
            args=[[choice_factory(cache_id=f'{__file__}:INIT_005')]],
            assertion=Assert.IN,
            expected=choice_factory(cache_id=f'{__file__}:INIT_005').name)),
        idspec('INIT_006', TestAction(
            name="Choices with invalid choices argument type - raises SimpleBenchTypeError",
            action=Choices,
            kwargs=ChoicesKWArgs(choices='not_a_sequence'),  # type: ignore[arg-type]
            exception=SimpleBenchTypeError,
            exception_tag=_ChoicesErrorTag.CHOICES_INVALID_ARG_TYPE,
        )),
        idspec('INIT_007', TestAction(
            name="Choices with invalid item in choices argument - raises SimpleBenchTypeError",
            action=Choices,
            kwargs=ChoicesKWArgs(choices=[choice_conf_factory(), 'not_a_choice']),  # type: ignore[list-item]
            exception=SimpleBenchTypeError,
            exception_tag=_ChoicesErrorTag.CHOICES_INVALID_ARG_TYPE
        )),
    ]
)
def test_choices_init(testspec: TestSpec):
    """Test initializing Choices with various combinations of keyword arguments.

    This test verifies that the Choices class can be initialized correctly
    using different combinations of parameters provided through the
    ChoicesKWArgs class. It checks that the attributes of the Choices instance
    match the expected values based on the provided keyword arguments.

    :param testspec: The test specification.
    :type testspec: TestSpec
    """
    testspec.run()


def choices_add_testspecs() -> list[TestSpec]:
    """Returns a list of TestSpec instances for testing Choices add().

    :return: A list of test specifications.
    :rtype: list[TestSpec]
    """
    testspecs: list[TestSpec] = []

    def add_choice_to_empty_choices_with_keyword_arg() -> None:
        cache_id = f'{__file__}:ADD_001'
        choices = choices_factory(cache_id=cache_id)
        choice = choice_factory(cache_id=cache_id)
        choices.add(choice=choice)
        assert len(choices) == 1 and choices[choice.name] is choice
    testspecs.append(
        idspec("ADD_001", TestAction(
            name="Add valid Choice instance to empty Choices via add(<keyword-argument>)",
            action=add_choice_to_empty_choices_with_keyword_arg,
        )))

    def add_choice_to_empty_choices_with_positional_arg() -> None:
        cache_id = f'{__file__}:ADD_002'
        choices = choices_factory(choices=None, cache_id=cache_id)
        choice = choice_factory(cache_id=cache_id)
        choices.add(choice)
        assert len(choices) == 1 and choices[choice.name] is choice
    testspecs.append(
        idspec("ADD_002", TestAction(
            name="Add valid Choice instance to empty Choices via add(<positional-argument>)",
            action=add_choice_to_empty_choices_with_positional_arg
        )))

    testspecs.append(
        idspec("ADD_003", TestAction(
            name="Add invalid type of object to Choices with add() - raises SimpleBenchTypeError",
            action=choices_factory(cache_id=None).add,
            args=['not_a_choice'],
            exception=SimpleBenchTypeError,
            exception_tag=_ChoicesErrorTag.ADD_CHOICE_INVALID_ARG_TYPE,
        )))

    def add_second_unique_choice_to_choices() -> None:
        cache_id = f'{__file__}:ADD_004'
        choices = choices_factory(cache_id=cache_id)
        choice1 = choice_factory(cache_id=cache_id, name='unique_choice', flags=('--unique-choice',))
        choice2 = choice_factory(cache_id=cache_id, name='another_unique_choice', flags=('--another-unique-choice',))
        choices.add(choice1)
        choices.add(choice2)
        assert (len(choices) == 2 and
                choices[choice1.name] is choice1 and
                choices[choice2.name] is choice2)
    testspecs.append(
        idspec("ADD_004", TestAction(
            name="Add second (different) Choice name/flag to Choices using add()",
            action=add_second_unique_choice_to_choices,
        )))

    def add_duplicate_name_choice_to_choices_raises() -> None:
        cache_id = f'{__file__}:ADD_005'
        choices = choices_factory(cache_id=cache_id)
        choice1 = choice_factory(cache_id=cache_id, name='duplicate_choice', flags=('--unique-choice1',))
        choice2 = choice_factory(cache_id=cache_id, name='duplicate_choice', flags=('--unique-choice2',))
        choices.add(choice1)
        choices.add(choice2)  # This should raise
    testspecs.append(
        idspec("ADD_005", TestAction(
            name="Add duplicate name Choice to Choices - raises SimpleBenchValueError",
            action=add_duplicate_name_choice_to_choices_raises,
            exception=SimpleBenchValueError,
            exception_tag=_ChoicesErrorTag.SETITEM_DUPLICATE_CHOICE_NAME,
        )))

    return testspecs


@pytest.mark.parametrize("testspec", choices_add_testspecs())
def test_choices_add_method(testspec: TestSpec) -> None:
    """Test the Choices.add() method.

    :param testspec: The test specification.
    :type testspec: TestSpec
    """
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
                choice_factory(cache_id=None, name='choice_one', flags=('--one',)),
                choice_factory(cache_id=None, name='choice_two', flags=('--two', '--deux')),
                choice_factory(cache_id=None, name='choice_three', flags=('--three',)),
                choice_factory(cache_id=None, name='choice_four', flags=('--fourth-item',)),
            ]).all_choice_args,
            assertion=Assert.EQUAL,
            expected={'one', 'two', 'deux', 'three', 'fourth_item'},
        )),
    ])
def test_choices_all_choice_args_method(testspec: TestSpec) -> None:
    """Test the Choices.all_choice_args() method.

    :param testspec: The test specification.
    :type testspec: TestSpec
    """
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
                choice_factory(cache_id=None, name='choice_one', flags=('--one',)),
                choice_factory(cache_id=None, name='choice_two', flags=('--two', '--deux')),
                choice_factory(cache_id=None, name='choice_three', flags=('--three',)),
                choice_factory(cache_id=None, name='choice_four', flags=('--fourth-item',)),
            ]).all_choice_flags,
            assertion=Assert.EQUAL,
            expected={'--one', '--two', '--deux', '--three', '--fourth-item'},
        )),
    ])
def test_choices_all_choice_flags_method(testspec: TestSpec) -> None:
    """Test the Choices.all_choice_flags() method.

    :param testspec: The test specification.
    :type testspec: TestSpec
    """
    testspec.run()


@pytest.mark.parametrize(
    "testspec", [
        idspec("GET_CHOICE_FOR_ARG_001", TestAction(
            name="Get Choice for existing arg",
            action=Choices(choices=[
                choice_factory(cache_id=f'{__file__}:GET_CHOICE_FOR_ARG_001', name='choice_one', flags=('--one',)),
                choice_factory(cache_id=None, name='choice_two', flags=('--two', '--deux')),
            ]).get_choice_for_arg,
            args=['one'],
            assertion=Assert.IS,
            expected=choice_factory(cache_id=f'{__file__}:GET_CHOICE_FOR_ARG_001', name='choice_one', flags=('--one',)),
        )),
        idspec("GET_CHOICE_FOR_ARG_002", TestAction(
            name="Get non-existing Choice arg (expect None)",
            action=Choices(choices=[
                choice_factory(cache_id=None, name='choice_one', flags=('--one',)),
                choice_factory(cache_id=None, name='choice_two', flags=('--two', '--deux')),
            ]).get_choice_for_arg,
            args=['nonexistent'],
            assertion=Assert.IS,
            expected=None,
        )),
        idspec("GET_CHOICE_FOR_ARG_003", TestAction(
            name="Get Choice with wrong type arg (raises SimpleBenchTypeError)",
            action=Choices(choices=[
                choice_factory(cache_id=None, name='choice_one', flags=('--one',)),
                choice_factory(cache_id=None, name='choice_two', flags=('--two', '--deux')),
            ]).get_choice_for_arg,
            args=[123],  # type: ignore[arg-type]
            exception=SimpleBenchTypeError,
            exception_tag=_ChoicesErrorTag.GET_CHOICE_FOR_ARG_INVALID_ARG_TYPE,
        )),
    ])
def test_choices_get_choice_for_arg_method(testspec: TestSpec) -> None:
    """Test the Choices.get_choice_for_arg() method.

    :param testspec: The test specification.
    :type testspec: TestSpec
    """
    testspec.run()


def choices_extend_testspecs() -> list[TestSpec]:
    """Returns a list of TestSpec instances for testing Choices extend().

    :return: A list of test specifications.
    :rtype: list[TestSpec]
    """
    testspecs: list[TestSpec] = []
    prefix = f"{__file__}:test_choices_extend_testspecs"

    def add_two_choices_via_extend_list() -> None:
        choices = choices_factory(choices=(), cache_id=None)
        choice1 = choice_factory(name='choice_one', flags=('--one',), cache_id=None)
        choice2 = choice_factory(name='choice_two', flags=('--two',), cache_id=None)
        choices.extend([choice1, choice2])
        assert (len(choices) == 2 and
                choices[choice1.name] is choice1 and
                choices[choice2.name] is choice2)
    testspecs.append(
        idspec("EXTENDS_001", TestAction(
            name="Choices extend - add two choices via extend([<choice1>, <choice2>]) and access them via dict key",
            action=add_two_choices_via_extend_list,
        )))

    def add_two_choices_via_extend_choices() -> None:
        choices = choices_factory(choices=(), cache_id=None)
        choice3 = choice_conf_factory(name='choice_three', flags=('--three',), cache_id=None)
        choice4 = choice_conf_factory(name='choice_four', flags=('--four',), cache_id=None)
        source_choices = choices_factory(choices=(choice3, choice4), cache_id=None)
        choices.extend(source_choices)
        assert (len(choices) == 2 and
                choices[choice3.name] is source_choices[choice3.name] and
                choices[choice4.name] is source_choices[choice4.name])
    testspecs.append(
        idspec("EXTENDS_002", TestAction(
            name="Choices extend - add two choices via extend(<choices>]) and access them via dict key",
            action=add_two_choices_via_extend_choices,
        )))

    testspecs.extend([
        idspec("EXTENDS_003", TestAction(
            name="Choices extend - add invalid type in single-item list (raises SimpleBenchTypeError)",
            action=choices_factory(cache_id=f'{prefix}:EXTENDS_003', choices=()).extend,
            args=['not_a_sequence'],
            exception=SimpleBenchTypeError,
            exception_tag=_ChoicesErrorTag.EXTEND_CHOICES_INVALID_ARG_TYPE,
        )),
        idspec("EXTENDS_004", TestAction(
            name="Choices extend - add invalid element in multi-item list (raises SimpleBenchTypeError)",
            action=choices_factory(cache_id=f'{prefix}:EXTENDS_004', choices=()).extend,
            args=[[choice_factory(), 'something_invalid']],
            exception=SimpleBenchTypeError,
            exception_tag=_ChoicesErrorTag.EXTEND_CHOICES_INVALID_ARG_TYPE,
        )),
    ])

    return testspecs


@pytest.mark.parametrize("testspec", choices_extend_testspecs())
def test_choices_extend(testspec: TestSpec) -> None:
    """Test the Choices extend() method.

    :param testspec: The test specification.
    :type testspec: TestSpec
    """
    testspec.run()


def choices_remove_testspecs() -> list[TestSpec]:
    """Returns a list of TestSpec instances for testing Choices remove().

    :return: A list of test specifications.
    :rtype: list[TestSpec]
    """
    testspecs: list[TestSpec] = []

    def remove_existing_choice() -> Choices:
        choice = choice_conf_factory(cache_id=None)
        choices = choices_factory(choices=(choice,), cache_id=None)
        choices.remove(choice.name)
        return choices
    testspecs.append(
        idspec("REMOVE_001", TestAction(
            name="Remove existing Choice from Choices",
            action=remove_existing_choice,
            assertion=Assert.LEN,
            expected=0,
        )))

    testspecs.append(
        idspec("REMOVE_002", TestAction(
            name="Remove non-existing Choice from Choices (raises SimpleBenchKeyError)",
            action=choices_factory(choices=None, cache_id=None).remove,
            args=['non_existing_choice'],
            exception=SimpleBenchKeyError,
            exception_tag=_ChoicesErrorTag.DELITEM_UNKNOWN_CHOICE_NAME,
        )))

    return testspecs


@pytest.mark.parametrize("testspec", choices_remove_testspecs())
def test_choices_remove(testspec: TestSpec) -> None:
    """Test the Choices.remove() method.

    :param testspec: The test specification.
    :type testspec: TestSpec
    """
    testspec.run()


def choices_setitem_testspecs() -> list[TestSpec]:
    """Returns a list of TestSpec instances for testing Choices __setitem__().

    :return: A list of test specifications.
    :rtype: list[TestSpec]
    """
    testspecs: list[TestSpec] = []

    def set_item_with_valid_choice() -> None:
        choices = choices_factory(choices=None, cache_id=None)
        choice = choice_factory(cache_id=None)
        choices[choice.name] = choice
        assert len(choices) == 1 and choices[choice.name] is choice
    testspecs.append(
        idspec("SETITEM_001", TestAction(
            name="Set item via __setitem__ method with valid Choice instance",
            action=set_item_with_valid_choice,
        )))

    testspecs.extend([
        idspec("SETITEM_002", TestAction(
            name="Set item via __setitem__ method with invalid key type (raises SimpleBenchTypeError)",
            action=choices_factory(choices=(), cache_id=None).__setitem__,
            args=[123, choice_factory(cache_id=None)],
            exception=SimpleBenchTypeError,
            exception_tag=_ChoicesErrorTag.SETITEM_INVALID_KEY_TYPE,
        )),
        idspec("SETITEM_003", TestAction(
            name="Set item via __setitem__ method with invalid type (raises SimpleBenchTypeError)",
            action=choices_factory(choices=(), cache_id=None).__setitem__,
            args=['invalid_choice', 'not_a_choice_instance'],
            exception=SimpleBenchTypeError,
            exception_tag=_ChoicesErrorTag.SETITEM_INVALID_VALUE_TYPE,
        )),
        idspec("SETITEM_004", TestAction(
            name="Set item via __setitem__ method with mismatched choice name (raises SimpleBenchValueError)",
            action=choices_factory(choices=(), cache_id=None).__setitem__,
            args=['mismatched_name', choice_factory(name='actual_name', flags=('--some-flag',), cache_id=None)],
            exception=SimpleBenchValueError,
            exception_tag=_ChoicesErrorTag.SETITEM_KEY_NAME_MISMATCH,
        )),
        idspec("SETITEM_005", TestAction(
            name="Set item via __setitem__ method with duplicate choice name (raises SimpleBenchValueError)",
            action=choices_factory(
                choices=(choice_conf_factory(name='duplicate_choice', flags=('--a-flag',), cache_id=None),),
                cache_id=None).__setitem__,
            args=['duplicate_choice',
                  choice_factory(name='duplicate_choice', flags=('--another-flag',), cache_id=None)],
            exception=SimpleBenchValueError,
            exception_tag=_ChoicesErrorTag.SETITEM_DUPLICATE_CHOICE_NAME,
        )),
        idspec("SETITEM_006", TestAction(
            name="Set item via __setitem__ method with duplicate flag (across choices) (raises SimpleBenchValueError)",
            action=choices_factory(
                choices=(choice_conf_factory(name='existing_choice', flags=('--duplicate-flag',), cache_id=None),),
                cache_id=None).__setitem__,
            args=['new_choice', choice_factory(name='new_choice', flags=('--duplicate-flag',), cache_id=None)],
            exception=SimpleBenchValueError,
            exception_tag=_ChoicesErrorTag.SETITEM_DUPLICATE_CHOICE_FLAG,
        )),
    ])
    return testspecs


@pytest.mark.parametrize("testspec", choices_setitem_testspecs())
def test_setitem_dunder_method(testspec: TestSpec) -> None:
    """Test that the __setitem__ dunder method of Choices works correctly.

    :param testspec: The test specification.
    :type testspec: TestSpec
    """
    testspec.run()
