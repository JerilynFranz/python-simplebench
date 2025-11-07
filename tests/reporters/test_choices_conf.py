"""Tests for simplebench.reporters.choices_conf module."""
# pylint: disable=unnecessary-direct-lambda-call
import pytest

from simplebench.exceptions import SimpleBenchValueError, SimpleBenchTypeError, SimpleBenchKeyError
from simplebench.reporters.choices import ChoicesConf, ChoicesErrorTag

from ..factories import choices_conf_factory, choice_conf_factory, default_choice_name
from ..kwargs import ChoicesConfKWArgs
from ..testspec import TestSpec, TestAction, idspec, Assert


@pytest.mark.parametrize(
    "testspec", [
        idspec('INIT_001', TestAction(
            name="No arguments - create an empty ChoicesConf instance",
            action=ChoicesConf,
            assertion=Assert.ISINSTANCE,
            validate_result=lambda result: len(result) == 0,
            expected=ChoicesConf)),
        idspec('INIT_002', TestAction(
            name="Initialize a ChoicesConf instance from a default ChoiceConf instance",
            action=ChoicesConf,
            args=[(choice_conf_factory(),)],
            validate_result=lambda result: len(result) == 1 and default_choice_name() in result,
            assertion=Assert.ISINSTANCE,
            expected=ChoicesConf)),
        idspec('INIT_003', TestAction(
            name="ChoicesConf initialized from a default ChoicesConf instance",
            action=ChoicesConf,
            args=[choices_conf_factory()],
            validate_result=lambda result: len(result) == 1 and default_choice_name() in result,
            assertion=Assert.ISINSTANCE,
            expected=ChoicesConf)),
        idspec('INIT_004', TestAction(
            name="ChoicesConf with invalid choices argument type - raises SimpleBenchTypeError",
            action=ChoicesConf,
            kwargs=ChoicesConfKWArgs(choices='not_a_sequence_of_ChoiceConf'),  # type: ignore[arg-type]
            exception=SimpleBenchTypeError,
            exception_tag=ChoicesErrorTag.CHOICES_INVALID_ARG_TYPE,
        )),
        idspec('INIT_005', TestAction(
            name="Choices with invalid item in choices argument iterable - raises SimpleBenchTypeError",
            action=ChoicesConf,
            kwargs=ChoicesConfKWArgs(choices=[choice_conf_factory(), 'not_a_choice']),  # type: ignore[list-item]
            exception=SimpleBenchTypeError,
            exception_tag=ChoicesErrorTag.CHOICES_INVALID_ARG_TYPE
        )),
    ]
)
def test_choices_init(testspec: TestSpec):
    """Test initializing ChoicesCOnf with various combinations paramters.

    This test verifies that the ChoicesConf class can be initialized correctly
    using different combinations of parameters provided through the
    ChoicesConfKWArgs class and that it raises appropriate exceptions for invalid
    inputs.
    """
    testspec.run()


def choices_conf_add_testspecs() -> list[TestSpec]:
    """Returns a list of TestSpec instances for testing ChoicesConf add()"""
    testspecs: list[TestSpec] = []

    def add_choice_conf_to_empty_choices_with_keyword_arg() -> None:
        choices_conf = choices_conf_factory(cache_id=None, choices=tuple())
        assert len(choices_conf) == 0, "ChoicesConf not empty in test setup."
        choice_conf = choice_conf_factory(cache_id=None)
        choice_name = choice_conf.name
        assert choice_name is default_choice_name(), "Unexpected default choice name in test setup."
        choices_conf.add(choice=choice_conf)
        assert len(choices_conf) == 1, "ChoicesConf length not 1 after adding ChoiceConf."
        assert choice_name in choices_conf, (
            f"ChoiceConf name '{choice_name}' not found in ChoicesConf after addition.")
        assert choices_conf[choice_name] is choice_conf, (
            "ChoiceConf not added correctly to ChoicesConf - got "
            "different instance back for name than was added.")
    testspecs.append(
        idspec("ADD_001", TestAction(
            name="Add valid Choice instance to empty Choices via add(<keyword-argument>)",
            action=add_choice_conf_to_empty_choices_with_keyword_arg,
        )))

    def add_choice_to_empty_choices_with_positional_arg() -> None:
        choices_conf = choices_conf_factory(choices=tuple(), cache_id=None)
        assert len(choices_conf) == 0, "ChoicesConf not empty in test setup."
        choice_conf = choice_conf_factory(cache_id=None)
        choice_name = choice_conf.name
        assert choice_name is default_choice_name(), "Unexpected default choice name in test setup."
        choices_conf.add(choice_conf)
        assert len(choices_conf) == 1, "ChoicesConf length not 1 after adding ChoiceConf."
        assert choice_name in choices_conf, (
            f"ChoiceConf name '{choice_name}' not found in ChoicesConf after addition.")
        assert choices_conf[choice_name] is choice_conf, (
            "ChoiceConf not added correctly to ChoicesConf - got "
            "different instance back for name than was added.")
    testspecs.append(
        idspec("ADD_002", TestAction(
            name="Add valid Choice instance to empty Choices via add(<positional-argument>)",
            action=add_choice_to_empty_choices_with_positional_arg
        )))

    testspecs.append(
        idspec("ADD_003", TestAction(
            name="Add invalid type of object to Choices with add() - raises SimpleBenchTypeError",
            action=choices_conf_factory(cache_id=None).add,
            args=['not_a_choice'],
            exception=SimpleBenchTypeError,
            exception_tag=ChoicesErrorTag.ADD_CHOICE_INVALID_ARG_TYPE,
        )))

    def add_second_unique_choice_to_choices() -> None:
        choices = choices_conf_factory(choices=tuple(), cache_id=None)
        choice1 = choice_conf_factory(name='choice1', flags=('--unique-choice1',), cache_id=None)
        choice2 = choice_conf_factory(name='choice2', flags=('--unique-choice2',), cache_id=None)
        choices.add(choice1)
        choices.add(choice2)
        assert len(choices) == 2, (
            f"Expected 2 choices in ChoicesConf after adding two unique choices, got {len(choices)} instead")
        assert choices['choice1'] is choice1, "ChoiceConf 'choice1' not found correctly in ChoicesConf after addition."
        assert choices['choice2'] is choice2, "ChoiceConf 'choice2' not found correctly in ChoicesConf after addition."
    testspecs.append(
        idspec("ADD_004", TestAction(
            name="Add second (different) Choice name/flag to Choices using add()",
            action=add_second_unique_choice_to_choices,
        )))

    def add_duplicate_name_choice_to_choices_raises() -> None:
        choices = choices_conf_factory(choices=tuple(), cache_id=None)
        choice1 = choice_conf_factory(name='duplicate_choice', flags=('--unique-choice1',), cache_id=None)
        choice2 = choice_conf_factory(name='duplicate_choice', flags=('--unique-choice2',), cache_id=None)
        choices.add(choice1)
        choices.add(choice2)  # This should raise
    testspecs.append(
        idspec("ADD_005", TestAction(
            name="Add duplicate name Choice to Choices - raises SimpleBenchValueError",
            action=add_duplicate_name_choice_to_choices_raises,
            exception=SimpleBenchValueError,
            exception_tag=ChoicesErrorTag.SETITEM_DUPLICATE_CHOICE_NAME,
        )))

    def add_duplicate_flag_choice_to_choices_raises() -> None:
        choices = choices_conf_factory(choices=tuple(), cache_id=None)
        choice1 = choice_conf_factory(name='choice1', flags=('--duplicate-flag',), cache_id=None)
        choice2 = choice_conf_factory(name='choice2', flags=('--duplicate-flag',), cache_id=None)
        choices.add(choice1)
        choices.add(choice2)  # This should raise SimpleBenchValueError/SETITEM_DUPLICATE_CHOICE_FLAG
    testspecs.append(
        idspec("ADD_006", TestAction(
            name="Add duplicate flag Choice to Choices - raises SimpleBenchValueError",
            action=add_duplicate_flag_choice_to_choices_raises,
            exception=SimpleBenchValueError,
            exception_tag=ChoicesErrorTag.SETITEM_DUPLICATE_CHOICE_FLAG,
        )))

    return testspecs


@pytest.mark.parametrize("testspec", choices_conf_add_testspecs())
def test_choices_conf_add_method(testspec: TestSpec) -> None:
    """Test the ChoicesConf().add() method."""
    testspec.run()


def choices_conf_extend_testspecs() -> list[TestSpec]:
    """Returns a list of TestSpec instances for testing ChoicesConf extend() method.

    Returns:
        list[TestSpec]:
            A list of TestSpec instances for testing the extend() method of ChoicesConf.
    """
    testspecs = []
    prefix = f"{__file__}:test_choices_extend_testspecs"

    def add_two_choices_via_extend_list_of_choice_confs() -> None:
        choices = choices_conf_factory(choices=tuple(), cache_id=f'{prefix}:EXTEND_001')
        choice1 = choice_conf_factory(name='choice_one', flags=('--one',), cache_id=f'{prefix}:EXTEND_001')
        choice2 = choice_conf_factory(name='choice_two', flags=('--two',), cache_id=f'{prefix}:EXTEND_001')
        choices.extend([choice1, choice2])
        assert len(choices) == 2, "ChoicesConf length not 2 after extend with two choices."
        assert choices[choice1.name] is choice1, "Choice 'choice_one' not found correctly after extend."
        assert choices[choice2.name] is choice2, "Choice 'choice_two' not found correctly after extend."
    testspecs.append(
        idspec("EXTENDS_001", TestAction(
            name="Choices extend - add two choices via extend([<choice1>, <choice2>]) and access them via dict key",
            action=add_two_choices_via_extend_list_of_choice_confs,
        )))

    def add_two_choices_via_extend_choices_conf() -> None:
        choices = choices_conf_factory(choices=tuple(), cache_id=f'{prefix}:EXTENDS_002')
        choice1 = choice_conf_factory(name='choice_three', flags=('--three',), cache_id=f'{prefix}:EXTENDS_002')
        choice2 = choice_conf_factory(name='choice_four', flags=('--four',), cache_id=f'{prefix}:EXTENDS_002')
        choices_to_add = choices_conf_factory(choices=(choice1, choice2), cache_id=f'{prefix}:EXTENDS_002')
        choices.extend(choices_to_add)
        assert len(choices) == 2, "ChoicesConf length not 2 after extend with ChoicesConf."
        assert choices[choice1.name] is choice1, "Choice 'choice_three' not found correctly after extend."
        assert choices[choice2.name] is choice2, "Choice 'choice_four' not found correctly after extend."
    testspecs.append(
        idspec("EXTENDS_002", TestAction(
            name="Choices extend - add two choices via extend(<choices>]) and access them via dict key",
            action=add_two_choices_via_extend_choices_conf,
        )))

    testspecs.extend([
        idspec("EXTENDS_003", TestAction(
            name="Choices extend - add invalid element in single-item list (raises SimpleBenchTypeError)",
            obj=choices_conf_factory(cache_id=f'{prefix}:EXTENDS_003'),
            action=choices_conf_factory(cache_id=f'{prefix}:EXTENDS_003').extend,
            args=['not_a_sequence'],  # type: ignore[arg-type]
            exception=SimpleBenchTypeError,
            exception_tag=ChoicesErrorTag.EXTEND_CHOICES_INVALID_ARG_TYPE,
        )),
        idspec("EXTENDS_004", TestAction(
            name="Choices extend - add invalid element in multi-item list (raises SimpleBenchTypeError)",
            obj=choices_conf_factory(cache_id=f'{prefix}:EXTENDS_004'),
            action=choices_conf_factory(cache_id=f'{prefix}:EXTENDS_004').extend,
            args=[[
                choice_conf_factory(name='choice_one', flags=('--one',), cache_id=f'{prefix}:EXTENDS_004'),
                'something_invalid'
            ]],
            exception=SimpleBenchTypeError,
            exception_tag=ChoicesErrorTag.EXTEND_CHOICES_INVALID_ARG_TYPE,
        )),
    ])
    return testspecs


@pytest.mark.parametrize("testspec", choices_conf_extend_testspecs())
def test_choices_extend(testspec: TestSpec) -> None:
    """Test the Choices extend() method."""
    testspec.run()


def choices_conf_remove_testspecs() -> list[TestSpec]:
    """Returns a list of TestSpec instances for testing ChoicesConf remove() method.

    Returns:
        list[TestSpec]:
            A list of TestSpec instances for testing the remove() method of ChoicesConf.
    """
    testspecs = []

    def choice_conf_to_remove() -> None:
        choices_conf = choices_conf_factory(choices=tuple(), cache_id=None)
        choice_conf = choice_conf_factory(name='choice_to_remove', flags=('--remove-me',), cache_id=None)
        choices_conf.add(choice_conf)
        assert len(choices_conf) == 1, "ChoicesConf not setup correctly for remove test."
        choices_conf.remove(choice_conf.name)
        assert len(choices_conf) == 0, "ChoicesConf not empty after removing the only choice."
    testspecs.append(
        idspec("REMOVE_001", TestAction(
            name="Remove existing Choice from Choices",
            action=choice_conf_to_remove,
        )))

    def remove_non_existing_choice_raises() -> None:
        choices_conf = choices_conf_factory(choices=tuple(), cache_id=None)
        choice_conf = choice_conf_factory(name='choice_to_remove', flags=('--remove-me',), cache_id=None)
        choices_conf.add(choice_conf)
        choices_conf.remove('non_existing_choice')  # This should raise SimpleBenchKeyError
    testspecs.append(
        idspec("REMOVE_002", TestAction(
            name="Remove non-existing Choice from Choices (raises SimpleBenchKeyError)",
            action=remove_non_existing_choice_raises,
            exception=SimpleBenchKeyError,
            exception_tag=ChoicesErrorTag.DELITEM_UNKNOWN_CHOICE_NAME,
        )))

    return testspecs


@pytest.mark.parametrize("testspec", choices_conf_remove_testspecs())
def test_choices_remove(testspec: TestSpec) -> None:
    """Test the Choices.remove() method."""
    testspec.run()


def setitem_dunder_method_testspecs() -> list[TestSpec]:
    """Returns a list of TestSpec instances for testing ChoicesConf __setitem__ method.

    Returns:
        list[TestSpec]:
            A list of TestSpec instances for testing the __setitem__ method of ChoicesConf.
    """
    testspecs = []

    def setitem_new_choice() -> None:
        choices = choices_conf_factory(choices=tuple(), cache_id=None)
        choice_conf = choice_conf_factory(name='new_choice', flags=('--new-choice',), cache_id=None)
        choices['new_choice'] = choice_conf
        assert len(choices) == 1, "ChoicesConf length not 1 after choices['new_choice'] = choice_conf"
        assert choices[choice_conf.name] is choice_conf, (
            "choices['new_choice'] = choice_conf did not set the ChoiceConf correctly.")
    testspecs.append(
        idspec("SETITEM_001", TestAction(
            name="Set item via __setitem__ method with valid Choice",
            action=setitem_new_choice,
        )))

    def setitem_invalid_key_type_raises() -> None:
        choices = choices_conf_factory(choices=tuple(), cache_id=None)
        choice_conf = choice_conf_factory(name='some_choice', flags=('--some-choice',), cache_id=None)
        choices[123] = choice_conf  # type: ignore[reportArgumentType,index]
    testspecs.append(
        idspec("SETITEM_002", TestAction(
            name="Set item via __setitem__ method with invalid key type (raises SimpleBenchTypeError)",
            action=setitem_invalid_key_type_raises,
            exception=SimpleBenchTypeError,
            exception_tag=ChoicesErrorTag.SETITEM_INVALID_KEY_TYPE,
        )))

    def setitem_invalid_value_type_raises() -> None:
        choices = choices_conf_factory(choices=tuple(), cache_id=None)
        choices['invalid_choice'] = 'not_a_choice_instance'  # type: ignore[reportArgumentType, assignment]
    testspecs.append(
        idspec("SETITEM_003", TestAction(
            name="Set item via __setitem__ method with invalid value type (raises SimpleBenchTypeError)",
            action=setitem_invalid_value_type_raises,
            exception=SimpleBenchTypeError,
            exception_tag=ChoicesErrorTag.SETITEM_INVALID_VALUE_TYPE,
        )))

    def setitem_mismatched_choice_name_raises() -> None:
        choices = choices_conf_factory(choices=tuple(), cache_id=None)
        choice_conf = choice_conf_factory(name='actual_name', flags=('--some-flag',), cache_id=None)
        choices['mismatched_name'] = choice_conf
    testspecs.append(
        idspec("SETITEM_004", TestAction(
            name="Set item via __setitem__ method with mismatched choice name (raises SimpleBenchValueError)",
            action=setitem_mismatched_choice_name_raises,
            exception=SimpleBenchValueError,
            exception_tag=ChoicesErrorTag.SETITEM_KEY_NAME_MISMATCH,
        )))

    def setitem_duplicate_choice_name_raises() -> None:
        choices = choices_conf_factory(
            choices=(choice_conf_factory(name='duplicate_choice', flags=('--dup-flag',), cache_id=None),),
            cache_id=None)
        choice_conf = choice_conf_factory(name='duplicate_choice', flags=('--another-flag',), cache_id=None)
        choices['duplicate_choice'] = choice_conf
    testspecs.append(
        idspec("SETITEM_005", TestAction(
            name="Set item via __setitem__ method with duplicate choice name (raises SimpleBenchValueError)",
            action=setitem_duplicate_choice_name_raises,
            exception=SimpleBenchValueError,
            exception_tag=ChoicesErrorTag.SETITEM_DUPLICATE_CHOICE_NAME,
        )))

    def setitem_duplicate_choice_flag_raises() -> None:
        choices = choices_conf_factory(
            choices=(choice_conf_factory(name='existing_choice', flags=('--common-flag',), cache_id=None),),
            cache_id=None)
        choice_conf = choice_conf_factory(name='new_choice', flags=('--common-flag',), cache_id=None)
        choices['new_choice'] = choice_conf
    testspecs.append(
        idspec("SETITEM_006", TestAction(
            name="Set item via __setitem__ method with duplicate flag (across choices) (raises SimpleBenchValueError)",
            action=setitem_duplicate_choice_flag_raises,
            exception=SimpleBenchValueError,
            exception_tag=ChoicesErrorTag.SETITEM_DUPLICATE_CHOICE_FLAG,
        )))

    return testspecs


@pytest.mark.parametrize("testspec", setitem_dunder_method_testspecs())
def test_setitem_dunder_method(testspec: TestSpec) -> None:
    """Test that the __setitem__ dunder method of Choices works correctly."""
    testspec.run()
