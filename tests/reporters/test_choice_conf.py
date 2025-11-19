"""Tests for choices.py module."""
import pytest

from simplebench.exceptions import SimpleBenchTypeError, SimpleBenchValueError
from simplebench.reporters.choice.choice_conf import ChoiceConf, _ChoiceConfErrorTag
from tests.factories import default_choice_conf, default_choice_conf_kwargs
from tests.testspec import Assert, TestAction, TestGet, TestSpec, idspec


@pytest.mark.parametrize(
    "testspec", [
        idspec('INIT_001', TestAction(
            name="ChoiceConf with all parameters",
            action=ChoiceConf,
            kwargs=default_choice_conf_kwargs(),
            assertion=Assert.ISINSTANCE,
            expected=ChoiceConf,
        )),
        idspec("INIT_002", TestAction(
            name="ChoiceConf with no extra parameter",
            action=ChoiceConf,
            kwargs=default_choice_conf_kwargs() - ['extra'],
            assertion=Assert.ISINSTANCE,
            expected=ChoiceConf,
        )),
        idspec("INIT_003", TestAction(
            name="ChoiceConf with missing output_format argument - raises TypeError",
            action=ChoiceConf,
            kwargs=default_choice_conf_kwargs() - ['output_format'],
            exception=TypeError,
        )),
        idspec("INIT_005", TestAction(
            name="ChoiceConf with wrong type output_format argument - raises SimpleBenchTypeError",
            action=ChoiceConf,
            kwargs=default_choice_conf_kwargs().replace(output_format=''),
            exception=SimpleBenchTypeError,
            exception_tag=_ChoiceConfErrorTag.OUTPUT_FORMAT_INVALID_ARG_TYPE,
        )),
        idspec("INIT_007", TestAction(
            name="ChoiceConf with missing targets argument - raises TypeError",
            action=ChoiceConf,
            kwargs=default_choice_conf_kwargs() - ['targets'],
            exception=TypeError,
        )),
        idspec("INIT_008", TestAction(
            name="ChoiceConf with empty list targets argument - raises SimpleBenchValueError",
            action=ChoiceConf,
            kwargs=default_choice_conf_kwargs().replace(targets=[]),
            exception=SimpleBenchValueError,
            exception_tag=_ChoiceConfErrorTag.TARGETS_INVALID_ARG_VALUE,
        )),
        idspec("INIT_009", TestAction(
            name="ChoiceConf with wrong type targets argument - raises SimpleBenchTypeError",
            action=ChoiceConf,
            kwargs=default_choice_conf_kwargs().replace(targets="not_targets"),
            exception=SimpleBenchTypeError,
            exception_tag=_ChoiceConfErrorTag.TARGETS_INVALID_ARG_TYPE,
        )),
        idspec("INIT_010", TestAction(
            name="ChoiceConf with incorrect targets list item type - raises SimpleBenchTypeError",
            action=ChoiceConf,
            kwargs=default_choice_conf_kwargs().replace(targets=['invalid_target']),
            exception=SimpleBenchTypeError,
            exception_tag=_ChoiceConfErrorTag.TARGETS_INVALID_ARG_TYPE,
        )),
        idspec("INIT_011", TestAction(
            name="ChoiceConf with missing sections argument - raises TypeError",
            action=ChoiceConf,
            kwargs=default_choice_conf_kwargs() - ['sections'],
            exception=TypeError,
        )),
        idspec("INIT_012", TestAction(
            name="ChoiceConf with empty list sections argument - raises SimpleBenchValueError",
            action=ChoiceConf,
            kwargs=default_choice_conf_kwargs().replace(sections=[]),
            exception=SimpleBenchValueError,
            exception_tag=_ChoiceConfErrorTag.SECTIONS_INVALID_ARG_VALUE,
        )),
        idspec("INIT_013", TestAction(
            name="ChoiceConf with wrong type sections argument - raises SimpleBenchTypeError",
            action=ChoiceConf,
            kwargs=default_choice_conf_kwargs().replace(sections="not_sections"),
            exception=SimpleBenchTypeError,
            exception_tag=_ChoiceConfErrorTag.SECTIONS_INVALID_ARG_TYPE,
        )),
        idspec("INIT_014", TestAction(
            name="ChoiceConf with incorrect sections list item type - raises SimpleBenchTypeError",
            action=ChoiceConf,
            kwargs=default_choice_conf_kwargs().replace(sections=['invalid_section']),
            exception=SimpleBenchTypeError,
            exception_tag=_ChoiceConfErrorTag.SECTIONS_INVALID_ARG_TYPE,
        )),
        idspec("INIT_015", TestAction(
            name="ChoiceConf with missing description argument - raises TypeError",
            action=ChoiceConf,
            kwargs=default_choice_conf_kwargs() - ['description'],
            exception=TypeError,
        )),
        idspec("INIT_016", TestAction(
            name="ChoiceConf with blank string description argument - raises SimpleBenchValueError",
            action=ChoiceConf,
            kwargs=default_choice_conf_kwargs().replace(description='   '),
            exception=SimpleBenchValueError,
            exception_tag=_ChoiceConfErrorTag.DESCRIPTION_INVALID_ARG_VALUE,
        )),
        idspec("INIT_017", TestAction(
            name="ChoiceConf with wrong type description argument - raises SimpleBenchTypeError",
            action=ChoiceConf,
            kwargs=default_choice_conf_kwargs().replace(description=123),
            exception=SimpleBenchTypeError,
            exception_tag=_ChoiceConfErrorTag.DESCRIPTION_INVALID_ARG_TYPE,
        )),
        idspec("INIT_018", TestAction(
            name="ChoiceConf with missing name argument - raises TypeError",
            action=ChoiceConf,
            kwargs=default_choice_conf_kwargs() - ['name'],
            exception=TypeError,
        )),
        idspec("INIT_019", TestAction(
            name="ChoiceConf with blank string name argument - raises SimpleBenchValueError",
            action=ChoiceConf,
            kwargs=default_choice_conf_kwargs().replace(name='   '),
            exception=SimpleBenchValueError,
            exception_tag=_ChoiceConfErrorTag.NAME_INVALID_ARG_VALUE,
        )),
        idspec("INIT_020", TestAction(
            name="ChoiceConf with wrong type name argument - raises SimpleBenchTypeError",
            action=ChoiceConf,
            kwargs=default_choice_conf_kwargs().replace(name=123),
            exception=SimpleBenchTypeError,
            exception_tag=_ChoiceConfErrorTag.NAME_INVALID_ARG_TYPE,
        )),
        idspec("INIT_021", TestAction(
            name="ChoiceConf with missing flags argument - raises TypeError",
            action=ChoiceConf,
            kwargs=default_choice_conf_kwargs() - ['flags'],
            exception=TypeError,
        )),
        idspec("INIT_022", TestAction(
            name="ChoiceConf with empty list flags argument - raises SimpleBenchValueError",
            action=ChoiceConf,
            kwargs=default_choice_conf_kwargs().replace(flags=[]),
            exception=SimpleBenchValueError,
            exception_tag=_ChoiceConfErrorTag.FLAGS_INVALID_ARGS_VALUE,
        )),
        idspec("INIT_023", TestAction(
            name="ChoiceConf with flag with whitespace - raises SimpleBenchValueError",
            action=ChoiceConf,
            kwargs=default_choice_conf_kwargs().replace(flags=['--valid', '--bad flag']),
            exception=SimpleBenchValueError,
            exception_tag=_ChoiceConfErrorTag.FLAGS_INVALID_ARGS_VALUE,
        )),
        idspec("INIT_024", TestAction(
            name="ChoiceConf with wrong type flags argument - raises SimpleBenchTypeError",
            action=ChoiceConf,
            kwargs=default_choice_conf_kwargs().replace(flags='--sample'),
            exception=SimpleBenchTypeError,
            exception_tag=_ChoiceConfErrorTag.FLAGS_INVALID_ARG_TYPE,
        )),
    ]
)
def test_initialization(testspec: TestSpec):
    """Test initializing Choice with various combinations of keyword arguments.

    This test verifies that the Choice class can be initialized correctly
    using different combinations of parameters provided through the
    ChoiceConfKWArgs class. It checks that the attributes of the Choice instance
    match the expected values based on the provided keyword arguments.

    :param testspec: The test specification.
    :type testspec: TestSpec
    """
    testspec.run()


@pytest.mark.parametrize(
    "testspec", [
        idspec("PROPS_001", TestGet(
            name="ChoiceConf flags property",
            attribute="flags",
            obj=default_choice_conf(),
            assertion=Assert.EQUAL,
            expected=frozenset(default_choice_conf_kwargs()['flags']),
        )),
        idspec("PROPS_002", TestGet(
            name="ChoiceConf name property",
            attribute="name",
            obj=default_choice_conf(),
            assertion=Assert.EQUAL,
            expected=default_choice_conf_kwargs()['name'],
        )),
        idspec("PROPS_003", TestGet(
            name="ChoiceConf description property",
            attribute="description",
            obj=default_choice_conf(),
            assertion=Assert.EQUAL,
            expected=default_choice_conf_kwargs()['description'],
        )),
        idspec("PROPS_004", TestGet(
            name="ChoiceConf sections property",
            attribute="sections",
            obj=default_choice_conf(),
            assertion=Assert.EQUAL,
            expected=frozenset(default_choice_conf_kwargs()['sections']),
        )),
        idspec("PROPS_005", TestGet(
            name="ChoiceConf targets property",
            attribute="targets",
            obj=default_choice_conf(),
            assertion=Assert.EQUAL,
            expected=frozenset(default_choice_conf_kwargs()['targets']),
        )),
        idspec("PROPS_006", TestGet(
            name="ChoiceConf output_format property",
            attribute="output_format",
            obj=default_choice_conf(),
            assertion=Assert.EQUAL,
            expected=default_choice_conf_kwargs()['output_format'],
        )),
        idspec("PROPS_007", TestGet(
            name="ChoiceConf extra property",
            attribute="extra",
            obj=default_choice_conf(),
            assertion=Assert.EQUAL,
            expected=default_choice_conf_kwargs()['extra'],
        )),
    ]
)
def test_choice_properties(testspec: TestSpec):
    """Test Choice properties return expected values.

    :param testspec: The test specification.
    :type testspec: TestSpec
    """
    testspec.run()
