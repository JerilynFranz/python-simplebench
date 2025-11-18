"""Tests for the tests.factories module."""

from argparse import Namespace
from pathlib import Path

import pytest

from simplebench import utils
from simplebench.case import Case
from simplebench.enums import FlagType, Format, Section, Target
from simplebench.reporters.choice import Choice, ChoiceConf
from simplebench.reporters.choices import Choices, ChoicesConf
from simplebench.reporters.reporter import Reporter, ReporterOptions
from simplebench.runners import SimpleRunner
from simplebench.session import Session

from . import factories
from .kwargs import CaseKWArgs, ChoiceConfKWArgs, ChoicesConfKWArgs, ReporterKWArgs
from .testspec import Assert, TestAction, TestSpec, idspec


@pytest.mark.parametrize("testspec", [
    idspec('FACTORY_001', TestAction(
        name="reporter_factory produces a valid Reporter instance",
        action=factories.reporter_factory,
        assertion=Assert.ISINSTANCE,
        expected=Reporter)),
    idspec('FACTORY_002', TestAction(
        name="reporter_options_factory produces a valid ReporterOptions instance",
        action=factories.reporter_options_factory,
        assertion=Assert.ISINSTANCE,
        expected=ReporterOptions)),
    idspec('FACTORY_003', TestAction(
        name="choice_conf_factory produces a valid ChoiceConf instance",
        action=factories.choice_conf_factory,
        assertion=Assert.ISINSTANCE,
        expected=ChoiceConf)),
    idspec('FACTORY_004', TestAction(
        name="choices_conf_factory produces a valid ChoicesConf instance",
        action=factories.choices_conf_factory,
        assertion=Assert.ISINSTANCE,
        expected=ChoicesConf)),
    idspec('FACTORY_005', TestAction(
        name="choice_factory produces a valid Choice instance",
        action=factories.choice_factory,
        assertion=Assert.ISINSTANCE,
        expected=Choice)),
    idspec('FACTORY_006', TestAction(
        name="choices_factory produces a valid Choices instance",
        action=factories.choices_factory,
        assertion=Assert.ISINSTANCE,
        expected=Choices)),
    idspec('FACTORY_007', TestAction(
        name="session_factory produces a valid Session instance",
        action=factories.session_factory,
        assertion=Assert.ISINSTANCE,
        expected=Session)),
    idspec('FACTORY_008', TestAction(
        name="case_factory produces a valid Case instance",
        action=factories.case_factory,
        assertion=Assert.ISINSTANCE,
        expected=Case)),
    idspec('FACTORY_009', TestAction(
        name="extra_factory produces a valid DefaultExtra instance",
        action=factories.extra_factory,
        assertion=Assert.ISINSTANCE,
        expected=factories.DefaultExtra)),
    idspec('FACTORY_010', TestAction(
        name="path_factory produces a valid Path instance",
        action=factories.path_factory,
        assertion=Assert.ISINSTANCE,
        expected=Path)),
    idspec('FACTORY_011', TestAction(
        name="case_group_factory produces a valid str instance",
        action=factories.case_group_factory,
        assertion=Assert.ISINSTANCE,
        expected=str)),
    idspec('FACTORY_012', TestAction(
        name="title_factory produces a valid str instance",
        action=factories.title_factory,
        assertion=Assert.ISINSTANCE,
        expected=str)),
    idspec('FACTORY_013', TestAction(
        name="reporter_options_type_factory produces a valid ReporterOptions type",
        action=factories.reporter_options_type_factory,
        assertion=Assert.ISSUBCLASS,
        expected=ReporterOptions)),
    idspec('FACTORY_014', TestAction(
        name="subdir_factory produces a valid str instance",
        action=factories.subdir_factory,
        assertion=Assert.ISINSTANCE,
        expected=str)),
    idspec('FACTORY_015', TestAction(
        name="sections_factory produces a tuple of Section instances",
        action=factories.sections_factory,
        assertion=Assert.ISINSTANCE,
        validate_result=lambda result: isinstance(result, tuple) and all(isinstance(item, Section) for item in result),
        expected=tuple)),
    idspec('FACTORY_016', TestAction(
        name="targets_factory produces a tuple of Target instances",
        action=factories.targets_factory,
        assertion=Assert.ISINSTANCE,
        validate_result=lambda result: isinstance(result, tuple) and all(isinstance(item, Target) for item in result),
        expected=tuple)),
    idspec('FACTORY_017', TestAction(
        name="formats_factory produces a tuple of Format instances",
        action=factories.formats_factory,
        assertion=Assert.ISINSTANCE,
        validate_result=lambda result: isinstance(result, tuple) and all(isinstance(item, Format) for item in result),
        expected=tuple)),
    idspec('FACTORY_018', TestAction(
        name="output_format_factory produces a valid Format instance",
        action=factories.output_format_factory,
        assertion=Assert.ISINSTANCE,
        expected=Format)),
    idspec('FACTORY_019', TestAction(
        name="description_factory produces a valid str instance",
        action=factories.description_factory,
        assertion=Assert.ISINSTANCE,
        expected=str)),
    idspec('FACTORY_020', TestAction(
        name="reporter_name_factory produces a valid str instance",
        action=factories.reporter_name_factory,
        assertion=Assert.ISINSTANCE,
        expected=str)),
    idspec('FACTORY_021', TestAction(
        name="choice_name_factory produces a valid str instance",
        action=factories.choice_name_factory,
        assertion=Assert.ISINSTANCE,
        expected=str)),
    idspec('FACTORY_022', TestAction(
        name="choice_flags_factory produces a tuple of str instances",
        action=factories.choice_flags_factory,
        assertion=Assert.ISINSTANCE,
        validate_result=lambda result: isinstance(result, tuple) and all(isinstance(item, str) for item in result),
        expected=tuple)),
    idspec('FACTORY_023', TestAction(
        name="flag_type_factory produces a valid FlagType instance",
        action=factories.flag_type_factory,
        assertion=Assert.ISINSTANCE,
        expected=FlagType)),
    idspec('FACTORY_024', TestAction(
        name="file_suffix_factory produces a valid str instance",
        action=factories.file_suffix_factory,
        assertion=Assert.ISINSTANCE,
        expected=str)),
    idspec('FACTORY_025', TestAction(
        name="file_unique_factory produces a valid bool instance",
        action=factories.file_unique_factory,
        assertion=Assert.ISINSTANCE,
        expected=bool)),
    idspec('FACTORY_026', TestAction(
        name="file_append_factory produces a valid bool instance",
        action=factories.file_append_factory,
        assertion=Assert.ISINSTANCE,
        expected=bool)),
    idspec('FACTORY_027', TestAction(
        name="report_output_factory produces a valid str instance",
        action=factories.report_output_factory,
        assertion=Assert.ISINSTANCE,
        expected=str)),
    idspec('FACTORY_028', TestAction(
        name="report_parameters_factory produces a valid dict instance",
        action=factories.report_parameters_factory,
        assertion=Assert.ISINSTANCE,
        expected=dict)),
    idspec('FACTORY_029', TestAction(
        name="minimal_case_kwargs_factory produces a valid CaseKWArgs instance",
        action=factories.minimal_case_kwargs_factory,
        assertion=Assert.ISINSTANCE,
        expected=CaseKWArgs)
    ),
    idspec('FACTORY_030', TestAction(
        name="iterations_factory produces a valid int instance",
        action=factories.iterations_factory,
        assertion=Assert.ISINSTANCE,
        expected=int),
    ),
    idspec('FACTORY_031', TestAction(
        name="warmup_iterations_factory produces a valid int instance",
        action=factories.warmup_iterations_factory,
        assertion=Assert.ISINSTANCE,
        expected=int),
    ),
    idspec('FACTORY_032', TestAction(
        name="rounds_factory produces a valid int instance",
        action=factories.rounds_factory,
        assertion=Assert.ISINSTANCE,
        expected=int),
    ),
    idspec('FACTORY_033', TestAction(
        name="min_time_factory produces a valid float instance",
        action=factories.min_time_factory,
        assertion=Assert.ISINSTANCE,
        expected=float),
    ),
    idspec('FACTORY_034', TestAction(
        name="max_time_factory produces a valid float instance",
        action=factories.max_time_factory,
        assertion=Assert.ISINSTANCE,
        expected=float),
    ),
    idspec('FACTORY_035', TestAction(
        name="variation_cols_factory produces a dict instance",
        action=factories.variation_cols_factory,
        assertion=Assert.ISINSTANCE,
        expected=dict),
    ),
    idspec('FACTORY_036', TestAction(
        name="kwargs_variations_factory produces a dict instance",
        action=factories.kwargs_variations_factory,
        assertion=Assert.ISINSTANCE,
        expected=dict),
    ),
    idspec('FACTORY_037', TestAction(
        name="runner_factory produces a type[SimpleRunner]",
        action=factories.runner_factory,
        assertion=Assert.ISSUBCLASS,
        expected=SimpleRunner),
    ),
    idspec('FACTORY_038', TestAction(
        name="reporter_options_factory a valid ReporterOptions instance",
        action=factories.reporter_options_factory,
        assertion=Assert.ISINSTANCE,
        expected=ReporterOptions)
    ),
    idspec('FACTORY_039', TestAction(
        name="reporter_options_tuple_factory produces a tuple of ReporterOptions instances",
        action=factories.reporter_options_tuple_factory,
        assertion=Assert.ISINSTANCE,
        validate_result=lambda result: (
            isinstance(result, tuple) and all(isinstance(item, ReporterOptions) for item in result)),
        expected=tuple),
    ),
    idspec('FACTORY_040', TestAction(
        name="case_kwargs_factory produces a valid CaseKWArgs instance",
        action=factories.case_kwargs_factory,
        assertion=Assert.ISINSTANCE,
        expected=CaseKWArgs),
    ),
    idspec('FACTORY_041', TestAction(
        name="namespace_factory produces a valid Namespace instance",
        action=factories.namespace_factory,
        assertion=Assert.ISINSTANCE,
        expected=Namespace),
    ),
    idspec('FACTORY_042', TestAction(
        name="choices_conf_kwargs_factory produces a valid ChoicesConfKWArgs instance",
        action=factories.choices_conf_kwargs_factory,
        assertion=Assert.ISINSTANCE,
        expected=ChoicesConfKWArgs),
    ),
    idspec('FACTORY_043', TestAction(
        name="reporter_kwargs_factory produces a valid ReporterKWArgs instance",
        action=factories.reporter_kwargs_factory,
        assertion=Assert.ISINSTANCE,
        expected=ReporterKWArgs),
    ),
    idspec('FACTORY_044', TestAction(
        name="choice_conf_kwargs_factory produces a valid ChoiceConfKWArgs instance",
        action=factories.choice_conf_kwargs_factory,
        assertion=Assert.ISINSTANCE,
        expected=ChoiceConfKWArgs),
    ),

])
def test_factories(testspec: TestSpec) -> None:
    """Test the various factories.

    :param testspec: The test specification to run.
    :type testspec: TestSpec
    """
    testspec.run()


@pytest.mark.parametrize("testspec", [
    idspec("LIST_OF_STRINGS_001", TestAction(
        name="Collect list of strings flag with specific values",
        kwargs={
            'args': factories.argument_parser_factory(
                arguments=[factories.list_of_strings_flag_factory(
                    flag='--test-flag',
                    choices=['value1', 'value2', 'value3'])]
            ).parse_args(['--test-flag', 'value1', 'value2', 'value3']),
            'flag': '--test-flag',
        },
        action=utils.collect_arg_list,
        validate_result=lambda result: set(result) == set(['value1', 'value2', 'value3']))),
    idspec("LIST_OF_STRINGS_002", TestAction(
        name="Verify allowed zero entries",
        action=utils.collect_arg_list,
        kwargs={
            'flag': '--test-flag',
            'args': factories.argument_parser_factory(
                arguments=[factories.list_of_strings_flag_factory(
                    flag='--test-flag',
                    choices=['value1', 'value2', 'value3'])]
            ).parse_args(['--test-flag']),
        },
        assertion=Assert.LEN,
        expected=0)),
])
def test_list_of_strings_flag_factory(testspec: TestSpec) -> None:
    """Test the list_of_strings_flag_factory function.

    :param testspec: The test specification to run.
    :type testspec: TestSpec
    """
    testspec.run()
