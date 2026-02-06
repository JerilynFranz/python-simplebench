"""Tests for choices.py module."""
# ruff: noqa: F401

import pytest

from simplebench.exceptions import SimpleBenchTypeError, SimpleBenchValueError
from simplebench.metrics import MetricsSelection
from simplebench.reporters.choice.choice_conf import ChoiceConf, _ChoiceConfErrorTag

from simplebench_tests.factories import default_choice_conf, default_choice_conf_kwargs
from testspec import Assert, TestAction, TestGet, TestSpec, idspec, PytestAction


@pytest.mark.parametrize(
    "testspec", [
        PytestAction('INIT_001',
            name="ChoiceConf with all parameters",
            action=ChoiceConf, kwargs=default_choice_conf_kwargs(),
            assertion=Assert.ISINSTANCE,
            expected=ChoiceConf),
        PytestAction("INIT_002",
            name="ChoiceConf with no extra parameter",
            action=ChoiceConf, kwargs=default_choice_conf_kwargs() - {'extra'},
            assertion=Assert.ISINSTANCE,
            expected=ChoiceConf),
        PytestAction("INIT_003",
            name="ChoiceConf with missing output_format argument - raises TypeError",
            action=ChoiceConf, kwargs=default_choice_conf_kwargs() - {'output_format'},
            exception=TypeError),
        PytestAction("INIT_005",
            name="ChoiceConf with wrong type output_format argument - raises SimpleBenchTypeError",
            action=ChoiceConf, kwargs=default_choice_conf_kwargs().replace(output_format=''),
            exception=SimpleBenchTypeError,
            exception_tag=_ChoiceConfErrorTag.OUTPUT_FORMAT_INVALID_ARG_TYPE),
        PytestAction("INIT_007",
            name="ChoiceConf with missing targets argument - raises TypeError",
            action=ChoiceConf, kwargs=default_choice_conf_kwargs() - ['targets'],
            exception=TypeError),
        PytestAction("INIT_008",
            name="ChoiceConf with empty list targets argument - raises SimpleBenchValueError",
            action=ChoiceConf, kwargs=default_choice_conf_kwargs().replace(targets=[]),
            exception=SimpleBenchValueError,
            exception_tag=_ChoiceConfErrorTag.TARGETS_INVALID_ARG_VALUE),
        PytestAction("INIT_009",
            name="ChoiceConf with wrong type targets argument - raises SimpleBenchTypeError",
            action=ChoiceConf, kwargs=default_choice_conf_kwargs().replace(targets="not_targets"),
            exception=SimpleBenchTypeError,
            exception_tag=_ChoiceConfErrorTag.TARGETS_INVALID_ARG_TYPE),
        PytestAction("INIT_010",
            name="ChoiceConf with incorrect targets list item type - raises SimpleBenchTypeError",
            action=ChoiceConf, kwargs=default_choice_conf_kwargs().replace(targets=['invalid_target']),
            exception=SimpleBenchTypeError,
            exception_tag=_ChoiceConfErrorTag.TARGETS_INVALID_ARG_TYPE),
        PytestAction("INIT_011",
            name="ChoiceConf with missing metrics argument - raises TypeError",
            action=ChoiceConf, kwargs=default_choice_conf_kwargs() - {'metrics'},
            exception=TypeError),
        PytestAction("INIT_013",
            name="ChoiceConf with wrong type metrics argument - raises SimpleBenchTypeError",
            action=ChoiceConf, kwargs=default_choice_conf_kwargs().replace(metrics="not_metrics"),
            exception=SimpleBenchTypeError,
            exception_tag=_ChoiceConfErrorTag.METRICS_INVALID_ARG_TYPE),
        PytestAction("INIT_015",
            name="ChoiceConf with missing description argument - raises TypeError",
            action=ChoiceConf, kwargs=default_choice_conf_kwargs() - {'description'},
            exception=TypeError),
        PytestAction("INIT_016",
            name="ChoiceConf with blank string description argument - raises SimpleBenchValueError",
            action=ChoiceConf, kwargs=default_choice_conf_kwargs().replace(description='   '),
            exception=SimpleBenchValueError,
            exception_tag=_ChoiceConfErrorTag.DESCRIPTION_INVALID_ARG_VALUE),
        PytestAction("INIT_017",
            name="ChoiceConf with wrong type description argument - raises SimpleBenchTypeError",
            action=ChoiceConf, kwargs=default_choice_conf_kwargs().replace(description=123),
            exception=SimpleBenchTypeError,
            exception_tag=_ChoiceConfErrorTag.DESCRIPTION_INVALID_ARG_TYPE),
        PytestAction("INIT_018",
            name="ChoiceConf with missing name argument - raises TypeError",
            action=ChoiceConf, kwargs=default_choice_conf_kwargs() - {'name'},
            exception=TypeError),
        PytestAction("INIT_019",
            name="ChoiceConf with blank string name argument - raises SimpleBenchValueError",
            action=ChoiceConf, kwargs=default_choice_conf_kwargs().replace(name='   '),
            exception=SimpleBenchValueError,
            exception_tag=_ChoiceConfErrorTag.NAME_INVALID_ARG_VALUE),
        PytestAction("INIT_020",
            name="ChoiceConf with wrong type name argument - raises SimpleBenchTypeError",
            action=ChoiceConf, kwargs=default_choice_conf_kwargs().replace(name=123),
            exception=SimpleBenchTypeError,
            exception_tag=_ChoiceConfErrorTag.NAME_INVALID_ARG_TYPE),
        PytestAction("INIT_021",
            name="ChoiceConf with missing flags argument - raises TypeError",
            action=ChoiceConf, kwargs=default_choice_conf_kwargs() - {'flags'},
            exception=TypeError),
        PytestAction("INIT_022",
            name="ChoiceConf with empty list flags argument - raises SimpleBenchValueError",
            action=ChoiceConf, kwargs=default_choice_conf_kwargs().replace(flags=[]),
            exception=SimpleBenchValueError,
            exception_tag=_ChoiceConfErrorTag.FLAGS_INVALID_ARGS_VALUE),
        PytestAction("INIT_023",
            name="ChoiceConf with flag with whitespace - raises SimpleBenchValueError",
            action=ChoiceConf,
            kwargs=default_choice_conf_kwargs().replace(flags=['--valid', '--bad flag']),
            exception=SimpleBenchValueError,
            exception_tag=_ChoiceConfErrorTag.FLAGS_INVALID_ARGS_VALUE),
        PytestAction("INIT_024",
            name="ChoiceConf with wrong type flags argument - raises SimpleBenchTypeError",
            action=ChoiceConf, kwargs=default_choice_conf_kwargs().replace(flags='--sample'),
            exception=SimpleBenchTypeError,
            exception_tag=_ChoiceConfErrorTag.FLAGS_INVALID_ARG_TYPE),
    ]
)
def test_initialization(testspec: TestSpec) -> None:
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
        PytestAction("PROPS_001",
            name="ChoiceConf flags property",
            action=lambda: default_choice_conf(),
            validate_attr="flags",
            assertion=Assert.EQUAL,
            expected=frozenset(default_choice_conf_kwargs()['flags'])),
        PytestAction("PROPS_002",
            name="ChoiceConf name property",
            action=lambda: default_choice_conf(),
            validate_attr="name",
            assertion=Assert.EQUAL,
            expected=default_choice_conf_kwargs()['name']),
        PytestAction("PROPS_003",
            name="ChoiceConf description property",
            action=lambda: default_choice_conf(),
            validate_attr="description",
            assertion=Assert.EQUAL,
            expected=default_choice_conf_kwargs()['description']),
        PytestAction("PROPS_004",
            name="ChoiceConf metrics property",
            action=lambda: default_choice_conf(),
            validate_attr="metrics",
            assertion=Assert.EQUAL,
            expected=default_choice_conf_kwargs()['metrics']),
        PytestAction("PROPS_005",
            name="ChoiceConf targets property",
            action=lambda: default_choice_conf(),
            validate_attr="targets",
            assertion=Assert.EQUAL,
            expected=frozenset(default_choice_conf_kwargs()['targets'])),
        PytestAction("PROPS_006",
            name="ChoiceConf output_format property",
            action=lambda: default_choice_conf(),
            validate_attr="output_format",
            assertion=Assert.EQUAL,
            expected=default_choice_conf_kwargs()['output_format']),
        PytestAction("PROPS_007",
            name="ChoiceConf extra property",
            action=lambda: default_choice_conf(),
            validate_attr="extra",
            assertion=Assert.EQUAL,
            expected=default_choice_conf_kwargs()['extra']),
    ]
)
def test_choice_properties(testspec: TestSpec) -> None:
    """Test Choice properties return expected values.

    :param testspec: The test specification.
    :type testspec: TestSpec
    """
    testspec.run()
