"""Test simplebench/reporters/reporter/reporter.py module"""
from __future__ import annotations

from argparse import Namespace
from pathlib import Path
from typing import Any, Optional

import pytest

from simplebench.case import Case
from simplebench.enums import Format, Section, Target
from simplebench.exceptions import (SimpleBenchNotImplementedError,
                                    SimpleBenchTypeError,
                                    SimpleBenchValueError)
from simplebench.iteration import Iteration
from simplebench.reporters.choice import Choice, ChoiceConf
from simplebench.reporters.choices import Choices
from simplebench.reporters.protocols import ReporterCallback
from simplebench.reporters.reporter import Reporter, ReporterOptions
from simplebench.reporters.reporter.exceptions import ReporterErrorTag
from simplebench.reporters.reporter.protocols import ReporterProtocol
from simplebench.results import Results
from simplebench.runners import SimpleRunner
from simplebench.session import Session

from ...factories import (FactoryReporter, case_factory, choice_conf_factory,
                          choice_conf_kwargs_factory, choice_factory,
                          choices_factory, default_description,
                          default_reporter_callback, default_reporter_name,
                          namespace_factory, path_factory,
                          report_parameters_factory, reporter_factory,
                          reporter_kwargs_factory, session_factory)
from ...testspec import (NO_EXPECTED_VALUE, Assert, TestAction, TestGet,
                         TestSet, TestSpec, idspec)


def broken_benchcase_missing_bench(**kwargs: Any) -> Results:  # pylint: disable=unused-argument  # pragma: no cover
    """A broken benchmark case function that is missing the required 'bench' parameter.

    The function signature is intentionally incorrect for testing purposes.
    """
    # Nothing inside this actually runs since it's just for testing Reporter's
    # error handling for an invalid function type signature.
    return Results(  # made-up results for testing purposes
            group='test_case', title='Test Case',
            description='A test case for testing.',
            n=10, rounds=1, total_elapsed=3.0,
            iterations=[Iteration(elapsed=1.0), Iteration(elapsed=2.0)])


def broken_benchcase_missing_kwargs(
        bench: SimpleRunner) -> Results:  # pylint: disable=unused-argument  # pragma: no cover
    """A broken benchmark case function that is missing the required 'kwargs' parameter.

    The function signature is intentionally incorrect for testing purposes.
    """
    # Nothing inside this actually runs since it's just for testing Reporter's
    # error handling for an invalid function type signature.
    return Results(  # made-up results for testing purposes
            group='test_case', title='Test Case',
            description='A test case for testing.',
            n=10, rounds=1, total_elapsed=3.0,
            iterations=[Iteration(elapsed=1.0), Iteration(elapsed=2.0)])


class BadSuperReporter(Reporter):
    """A dummy Reporter subclass for testing purposes.

    This class incorrectly calls super().run_report(), which should raise NotImplementedError
    when run() is called.
    """
    def __init__(self) -> None:
        super().__init__(**reporter_kwargs_factory(cache_id=None))

    def run_report(self,  # pylint: disable=useless-parent-delegation
                   *,
                   args: Namespace,
                   case: Case,
                   choice: Choice,
                   path: Optional[Path] = None,
                   session: Optional[Session] = None,
                   callback: Optional[ReporterCallback] = None) -> None:
        """Incorrectly calls super().run_report(), which should raise NotImplementedError."""
        return super().run_report(
                                  args=args,
                                  case=case,
                                  choice=choice,
                                  path=path,
                                  session=session,
                                  callback=callback)


class GoodReporter(Reporter):
    """A good dummy Reporter subclass for testing purposes.

    """
    def __init__(self) -> None:
        super().__init__(**reporter_kwargs_factory(cache_id=None))

    def run_report(self,  # pylint: disable=useless-parent-delegation
                   *,
                   args: Namespace,
                   case: Case,
                   choice: Choice,
                   path: Optional[Path] = None,
                   session: Optional[Session] = None,
                   callback: Optional[ReporterCallback] = None) -> None:
        return


def test_good_reporter_subclassing() -> None:
    """Test that GoodReporter subclass can be instantiated and run_report works."""
    reporter = GoodReporter()
    if not isinstance(reporter, ReporterProtocol):  # type: ignore[reportGeneralTypeIssue]
        raise AssertionError("GoodReporter does not conform to ReporterProtocol")

    assert isinstance(reporter, Reporter)
    # Call run_report with minimal valid parameters
    reporter.run_report(
        args=namespace_factory(),
        case=case_factory(),
        choice=choice_factory()
    )  # Should not raise any exceptions


def test_factory_reporter_subclassing() -> None:
    """Test that FactoryReporter subclass can be instantiated and run_report works."""
    reporter = FactoryReporter(**reporter_kwargs_factory())
    if not isinstance(reporter, ReporterProtocol):  # type: ignore[reportGeneralTypeIssue]
        raise AssertionError("FactoryReporter does not conform to ReporterProtocol")

    assert isinstance(reporter, Reporter)
    # Call run_report with minimal valid parameters
    reporter.run_report(
        args=namespace_factory(),
        case=case_factory(),
        choice=choice_factory()
    )  # Should not raise any exceptions


@pytest.mark.parametrize('testspec', [
    idspec('REPORTER_001', TestAction(
        name="abstract base class Reporter() cannot be instantiated directly",
        action=Reporter,
        exception=TypeError)),
    idspec('REPORTER_002', TestAction(
        name="configured subclass of BadSuperFactoryReporter() can be instantiated",
        action=BadSuperReporter,
        assertion=Assert.ISINSTANCE,
        expected=BadSuperReporter)),
    idspec('REPORTER_003', TestAction(
        name=("calling run_report() on BadSuperFactoryReporter with bad run_report() super() delegation "
              "raises SimpleBenchNotImplementedError"),
        action=BadSuperReporter().run_report,
        kwargs={'args': namespace_factory(),
                'case': case_factory(),
                'choice': choice_factory()},
        exception=SimpleBenchNotImplementedError,
        exception_tag=ReporterErrorTag.RUN_REPORT_NOT_IMPLEMENTED)),
    idspec('REPORTER_004', TestAction(
        name="reporter_factory() is creating valid FactoryReporter instances",
        action=reporter_factory,
        assertion=Assert.ISINSTANCE,
        expected=FactoryReporter)),
    idspec('REPORTER_005', TestAction(
        name="Correctly configured subclass of Reporter() can call report() successfully",
        action=reporter_factory().report,
        kwargs=report_parameters_factory(),
        validate_result=lambda result: result is None)),
    idspec('REPORTER_006', TestAction(
        name="FactoryReporter() can be instantiated with parameters from reporter_kwargs_factory()",
        action=FactoryReporter,
        kwargs=reporter_kwargs_factory(),
        assertion=Assert.ISINSTANCE,
        expected=FactoryReporter)),
    idspec('REPORTER_007', TestAction(
        name="Correctly configured Reporter() can call report() successfully",
        action=FactoryReporter(**reporter_kwargs_factory()).report,
        kwargs=report_parameters_factory(),
        expected=NO_EXPECTED_VALUE)),
    idspec('REPORTER_008', TestAction(
        name="Init of Reporter with missing name raises TypeError",
        action=FactoryReporter,
        kwargs=reporter_kwargs_factory() - ['name'],
        exception=TypeError)),
    idspec('REPORTER_009', TestAction(
        name="Init of Reporter with missing description raises TypeError",
        action=FactoryReporter,
        kwargs=reporter_kwargs_factory() - ['description'],
        exception=TypeError)),
    idspec('REPORTER_010', TestAction(
        name="Init of Reporter with missing sections raises TypeError",
        action=FactoryReporter,
        kwargs=reporter_kwargs_factory() - ['sections'],
        exception=TypeError)),
    idspec('REPORTER_011', TestAction(
        name=("Init of FactoryReporter with empty targets raises "
              "SimpleBenchValueError/TARGETS_INVALID_ARG_TYPE"),
        action=FactoryReporter,
        kwargs=reporter_kwargs_factory().replace(targets=set()),
        exception=SimpleBenchValueError,
        exception_tag=ReporterErrorTag.TARGETS_ITEMS_ARG_VALUE)),
    idspec('REPORTER_012', TestAction(
        name=("Init of FactoryReporter with empty formats raises "
              "SimpleBenchValueError/SECTIONS_ITEMS_ARG_VALUE"),
        action=FactoryReporter,
        kwargs=reporter_kwargs_factory().replace(formats=set()),
        exception=SimpleBenchValueError,
        exception_tag=ReporterErrorTag.FORMATS_ITEMS_ARG_VALUE)),
    idspec('REPORTER_013', TestAction(
        name="Init of FactoryReporter with missing choices raises TypeError",
        action=FactoryReporter,
        kwargs=reporter_kwargs_factory() - ['choices'],
        exception=TypeError)),
    idspec('REPORTER_014', TestAction(
        name=("Init of FactoryReporter with choices not being a Choices instance raises "
              "SimpleBenchTypeError/INVALID_CHOICES_ARG_TYPE"),
        action=FactoryReporter,
        kwargs=reporter_kwargs_factory().replace(choices="not_a_choices_instance"),
        exception=SimpleBenchTypeError,
        exception_tag=ReporterErrorTag.CHOICES_INVALID_ARG_TYPE)),
    idspec('REPORTER_015', TestAction(
        name=("Init of FactoryReporter with sections containing a non-Section enum raises "
              "SimpleBenchTypeError/SECTION_INVALID_ENTRY_TYPE"),
        action=FactoryReporter,
        kwargs=reporter_kwargs_factory().replace(sections={Section.OPS, "not_a_section_enum"}),
        exception=SimpleBenchTypeError,
        exception_tag=ReporterErrorTag.SECTIONS_INVALID_ARG_TYPE)),
    idspec('REPORTER_016', TestAction(
        name=("Init of FactoryReporter with targets containing non-Target enum raises "
              "SimpleBenchTypeError/TARGETS_INVALID_ARG_TYPE"),
        action=FactoryReporter,
        kwargs=reporter_kwargs_factory().replace(targets={Target.CONSOLE, "not_a_target_enum"}),
        exception=SimpleBenchTypeError,
        exception_tag=ReporterErrorTag.TARGETS_INVALID_ARG_TYPE)),
    idspec('REPORTER_017', TestAction(
        name=("Init of FactoryReporter with formats set to a non-Format enum raises "
              "SimpleBenchTypeError/FORMATS_INVALID_ARG_TYPE"),
        action=FactoryReporter,
        kwargs=reporter_kwargs_factory().replace(formats={Format.JSON, "not_a_format_enum"}),
        exception=SimpleBenchTypeError,
        exception_tag=ReporterErrorTag.FORMATS_INVALID_ARG_TYPE)),
    idspec('REPORTER_018', TestAction(
        name=("Init of FactoryReporter with empty name raises "
              "SimpleBenchValueError/NAME_INVALID_ARG_VALUE"),
        action=FactoryReporter,
        kwargs=reporter_kwargs_factory().replace(name=''),
        exception=SimpleBenchValueError,
        exception_tag=ReporterErrorTag.NAME_INVALID_ARG_VALUE)),
    idspec('REPORTER_019', TestAction(
        name=("Init of FactoryReporter with blank name raises "
              "SimpleBenchValueError/NAME_INVALID_ARGVALUE"),
        action=FactoryReporter,
        kwargs=reporter_kwargs_factory().replace(name='  '),
        exception=SimpleBenchValueError,
        exception_tag=ReporterErrorTag.NAME_INVALID_ARG_VALUE)),
    idspec('REPORTER_020', TestAction(
        name=("Init of FactoryReporter with empty description raises "
              "SimpleBenchValueError/DESCRIPTION_INVALID_ARG_VALUE"),
        action=FactoryReporter,
        kwargs=reporter_kwargs_factory().replace(description=''),
        exception=SimpleBenchValueError,
        exception_tag=ReporterErrorTag.DESCRIPTION_INVALID_ARG_VALUE)),
    idspec('REPORTER_021', TestAction(
        name=("Init of FactoryReporter with blank description raises "
              "SimpleBenchValueError/DESCRIPTION_INVALID_ARG_VALUE"),
        action=FactoryReporter,
        kwargs=reporter_kwargs_factory().replace(description='   '),
        exception=SimpleBenchValueError,
        exception_tag=ReporterErrorTag.DESCRIPTION_INVALID_ARG_VALUE)),
    idspec('REPORTER_022', TestAction(
        name="Attempt to directly instantiate Reporter raises TypeError",
        action=Reporter,
        kwargs=reporter_kwargs_factory(),
        exception=TypeError)),
    idspec('REPORTER_023', TestAction(
        name=("Init of FactoryReporter with an options_type that is not "
              "a ReporterOptions subclass raises SimpleBenchTypeError"),
        action=FactoryReporter,
        kwargs=reporter_kwargs_factory().replace(options_type=str),
        exception=SimpleBenchTypeError,
        exception_tag=ReporterErrorTag.OPTIONS_TYPE_INVALID_VALUE)),
    idspec('REPORTER_024', TestAction(
        name="Init of FactoryReporter with subdir name longer than 64 characters raises SimpleBenchValueError",
        action=FactoryReporter,
        kwargs=reporter_kwargs_factory().replace(subdir='a' * 65),
        exception=SimpleBenchValueError,
        exception_tag=ReporterErrorTag.SUBDIR_TOO_LONG)),
    idspec('REPORTER_025', TestAction(
        name=("Init of FactoryReporter with subdir name containing "
              "non-alphanumeric characters raises SimpleBenchValueError"),
        action=FactoryReporter,
        kwargs=reporter_kwargs_factory().replace(subdir='invalid/subdir!'),
        exception=SimpleBenchValueError,
        exception_tag=ReporterErrorTag.SUBDIR_INVALID_ARG_VALUE)),
    idspec('REPORTER_026', TestAction(
        name="Init of FactoryReporter with file_suffix as non-string raises SimpleBenchTypeError",
        action=FactoryReporter,
        kwargs=reporter_kwargs_factory().replace(file_suffix=123),
        exception=SimpleBenchTypeError,
        exception_tag=ReporterErrorTag.FILE_SUFFIX_INVALID_ARG_TYPE)),
    idspec('REPORTER_027', TestAction(
        name="Init of FactoryReporter with file_suffix longer than 10 characters raises SimpleBenchValueError",
        action=FactoryReporter,
        kwargs=reporter_kwargs_factory().replace(file_suffix='a' * 11),
        exception=SimpleBenchValueError,
        exception_tag=ReporterErrorTag.FILE_SUFFIX_ARG_TOO_LONG)),
    idspec('REPORTER_028', TestAction(
        name=("Init of FactoryReporter with file_suffix containing "
              "non-alphanumeric characters raises SimpleBenchValueError"),
        action=FactoryReporter,
        kwargs=reporter_kwargs_factory().replace(file_suffix='invalid!'),
        exception=SimpleBenchValueError,
        exception_tag=ReporterErrorTag.FILE_SUFFIX_INVALID_ARG_VALUE)),
    idspec('REPORTER_029', TestAction(
        name="Init of FactoryReporter with file_unique as a non-boolean raises SimpleBenchTypeError",
        action=FactoryReporter,
        kwargs=reporter_kwargs_factory().replace(file_unique='not_a_bool'),
        exception=SimpleBenchTypeError,
        exception_tag=ReporterErrorTag.FILE_UNIQUE_INVALID_ARG_TYPE)),
    idspec('REPORTER_030', TestAction(
        name="Init of FactoryReporter with file_append as a non-boolean raises SimpleBenchTypeError",
        action=FactoryReporter,
        kwargs=reporter_kwargs_factory().replace(file_append='not_a_bool'),
        exception=SimpleBenchTypeError,
        exception_tag=ReporterErrorTag.FILE_APPEND_INVALID_ARG_TYPE)),
    idspec('REPORTER_031', TestAction(
        name="Init of FactoryReporter with file_unique and file_append both True raises SimpleBenchValueError",
        action=FactoryReporter,
        kwargs=reporter_kwargs_factory().replace(file_unique=True, file_append=True),
        exception=SimpleBenchValueError,
        exception_tag=ReporterErrorTag.FILE_UNIQUE_AND_FILE_APPEND_EXACTLY_ONE_REQUIRED)),
    idspec('REPORTER_032', TestAction(
        name="Init of FactoryReporter with file_unique and file_append both False raises SimpleBenchValueError",
        action=FactoryReporter,
        kwargs=reporter_kwargs_factory().replace(file_unique=False, file_append=False),
        exception=SimpleBenchValueError,
        exception_tag=ReporterErrorTag.FILE_UNIQUE_AND_FILE_APPEND_EXACTLY_ONE_REQUIRED)),
    idspec('REPORTER_033', TestAction(
        name="Init of FactoryReporter with file_append as True and file_unique as False works",
        action=FactoryReporter,
        kwargs=reporter_kwargs_factory().replace(file_append=True, file_unique=False),
        assertion=Assert.ISINSTANCE,
        expected=FactoryReporter)),
    idspec('REPORTER_034', TestAction(
        name="Init of FactoryReporter with file_unique as False and file_append as True works",
        action=FactoryReporter,
        kwargs=reporter_kwargs_factory().replace(file_unique=False, file_append=True),
        assertion=Assert.ISINSTANCE,
        expected=FactoryReporter)),
])
def test_reporter_init(testspec: TestSpec) -> None:
    """Test Reporter init parameters."""
    testspec.run()


@pytest.mark.parametrize('testspec', [
    idspec('REPORT_001', TestAction(
        name=("report() with non-Case arg raises "
              "SimpleBenchTypeError/REPORTER_REPORT_INVALID_CASE_ARG"),
        action=reporter_factory().report,
        kwargs={'args': namespace_factory(),
                'case': "not_a_case_instance",
                'choice': choice_conf_factory()},
        exception=SimpleBenchTypeError,
        exception_tag=ReporterErrorTag.REPORT_INVALID_CASE_ARG)),
    idspec('REPORT_002', TestAction(
        name=("report() with non-Choice arg raises "
              "SimpleBenchTypeError/REPORTER_REPORT_INVALID_CHOICE_ARG"),
        action=reporter_factory().report,
        kwargs={'args': namespace_factory(),
                'case': case_factory(),
                'choice': "not_a_choice_conf_instance"},
        exception=SimpleBenchTypeError,
        exception_tag=ReporterErrorTag.REPORT_INVALID_CHOICE_ARG)),
    idspec('REPORT_003', TestAction(
        name=("report() with non-Choice choice arg raises "
              "SimpleBenchTypeError/REPORTER_REPORT_INVALID_CHOICE_ARG"),
        action=reporter_factory().report,
        kwargs={'args': namespace_factory(),
                'case': case_factory(),
                'choice': Choices()},  # passing Choices instead of Choice
        exception=SimpleBenchTypeError,
        exception_tag=ReporterErrorTag.REPORT_INVALID_CHOICE_ARG)),
    idspec('REPORT_004', TestAction(
        name=("report() with Section not in Reporter's sections raises "
              "SimpleBenchValueError/REPORTER_REPORT_UNSUPPORTED_SECTION"),
        action=reporter_factory().report,
        kwargs={'args': namespace_factory(),
                'case': case_factory(),
                'choice': Choice(
                    reporter=reporter_factory(),
                    choice_conf=ChoiceConf(
                        **choice_conf_kwargs_factory().replace(sections=[Section.NULL])))},
        exception=SimpleBenchValueError,
        exception_tag=ReporterErrorTag.REPORT_UNSUPPORTED_SECTION)),
    idspec('REPORT_005', TestAction(
        name=("report() with Target not in Reporter's targets raises "
              "SimpleBenchValueError/REPORTER_REPORT_UNSUPPORTED_TARGET"),
        action=reporter_factory().report,
        kwargs={'args': namespace_factory(),
                'case': case_factory(),
                'choice': Choice(
                    reporter=reporter_factory(),
                    choice_conf=ChoiceConf(
                        **choice_conf_kwargs_factory().replace(targets=[Target.CUSTOM])))},
        exception=SimpleBenchValueError,
        exception_tag=ReporterErrorTag.REPORT_UNSUPPORTED_TARGET)),
    idspec('REPORT_006', TestAction(
        name=("report() with output_format not in Reporter's formats raises "
              "SimpleBenchValueError/REPORTER_REPORT_UNSUPPORTED_FORMAT"),
        action=reporter_factory().report,
        kwargs={'args': namespace_factory(),
                'case': case_factory(),
                'choice': Choice(
                    reporter=reporter_factory(),
                    choice_conf=ChoiceConf(
                        **choice_conf_kwargs_factory().replace(output_format=Format.CUSTOM)))},
        exception=SimpleBenchValueError,
        exception_tag=ReporterErrorTag.REPORT_UNSUPPORTED_FORMAT)),
    idspec('REPORT_007', TestAction(
        name="report() with valid Case and Choice runs successfully",
        action=reporter_factory().report,
        kwargs={'args': namespace_factory(),
                'case': case_factory(),
                'choice': choice_factory(),
                'path': path_factory()},
        expected=NO_EXPECTED_VALUE)),
    idspec('REPORT_008', TestAction(
        name="report() with valid callback runs successfully",
        action=reporter_factory().report,
        kwargs={'args': namespace_factory(),
                'case': case_factory(),
                'choice': Choice(
                    reporter=reporter_factory(),
                    choice_conf=ChoiceConf(
                        **choice_conf_kwargs_factory().replace(targets=[Target.CALLBACK]))),
                'callback': default_reporter_callback},
        expected=NO_EXPECTED_VALUE)),
    idspec('REPORT_009', TestAction(
        name=("report() with invalid callback raises"
              "SimpleBenchTypeError/REPORTER_REPORT_INVALID_CALLBACK_ARG"),
        action=reporter_factory().report,
        kwargs={'args': namespace_factory(),
                'case': case_factory(),
                'choice': Choice(
                    reporter=reporter_factory(),
                    choice_conf=ChoiceConf(
                        **choice_conf_kwargs_factory().replace(targets=[Target.CALLBACK]))),
                'callback': "not_a_callback"},
        exception=SimpleBenchTypeError,
        exception_tag=ReporterErrorTag.REPORT_INVALID_CALLBACK_ARG)),
    idspec('REPORT_010', TestAction(
        name="report() with valid path runs successfully",
        action=reporter_factory().report,
        kwargs={'args': namespace_factory(),
                'case': case_factory(),
                'choice': choice_factory(),
                'path': path_factory()},
        expected=NO_EXPECTED_VALUE)),
    idspec('REPORT_011', TestAction(
        name=("report() with invalid path raises "
              "SimpleBenchTypeError/REPORTER_REPORT_INVALID_PATH_ARG"),
        action=reporter_factory().report,
        kwargs={'args': namespace_factory(),
                'case': case_factory(),
                'choice': choice_factory(),
                'path': "not_a_path"},
        exception=SimpleBenchTypeError,
        exception_tag=ReporterErrorTag.REPORT_INVALID_PATH_ARG)),
    idspec('REPORT_012', TestAction(
        name=("report() with valid session runs successfully"),
        action=reporter_factory().report,
        kwargs={'args': namespace_factory(),
                'case': case_factory(),
                'choice': choice_factory(),
                'path': path_factory(),
                'session': session_factory()},
        expected=NO_EXPECTED_VALUE)),
    idspec('REPORT_013', TestAction(
        name=("report() with invalid session raises "
              "SimpleBenchTypeError/REPORTER_REPORT_INVALID_SESSION_ARG"),
        action=reporter_factory().report,
        kwargs={'args': namespace_factory(),
                'case': case_factory(),
                'choice': choice_factory(),
                'path': path_factory(),
                'session': "not_a_session"},
        exception=SimpleBenchTypeError,
        exception_tag=ReporterErrorTag.REPORT_INVALID_SESSION_ARG)),
    idspec('REPORT_014', TestAction(
        name="report() invalid args type raises SimpleBenchTypeError/REPORT_INVALID_ARGS_ARG_TYPE",
        action=reporter_factory().report,
        kwargs={'args': "not_a_namespace",
                'case': case_factory(),
                'choice': choice_factory(),
                'path': path_factory(),
                'session': session_factory()},
        exception=SimpleBenchTypeError,
        exception_tag=ReporterErrorTag.REPORT_INVALID_ARGS_ARG_TYPE)),
    idspec('REPORT_015', TestAction(
        name="report() with missing args raises TypeError",
        action=reporter_factory().report,
        kwargs={'case': case_factory(),
                'choice': choice_factory(),
                'path': path_factory(),
                'session': session_factory()},
        exception=TypeError)),
    idspec('REPORT_016', TestAction(
        name="report() with missing case raises TypeError",
        action=reporter_factory().report,
        kwargs={'args': namespace_factory(),
                'choice': choice_factory(),
                'path': path_factory(),
                'session': session_factory()},
        exception=TypeError)),
    idspec('REPORT_017', TestAction(
        name="report() with missing choice raises TypeError",
        action=reporter_factory().report,
        kwargs={'args': namespace_factory(),
                'case': case_factory(),
                'path': path_factory(),
                'session': session_factory()},
        exception=TypeError)),
])
def test_report(testspec: TestSpec) -> None:
    """Test Reporter.report() method."""
    testspec.run()


@pytest.mark.parametrize('testspec', [
    idspec('REPORTER_ADD_CHOICE_001', TestAction(
        name="Adding a valid Choice to a Reporter works",
        action=reporter_factory().add_choice,
        args=[Choice(
            reporter=reporter_factory(),
            choice_conf=ChoiceConf(
                **choice_conf_kwargs_factory().replace(name='new_choice', flags=['--new-choice'])))],
        expected=NO_EXPECTED_VALUE)),
    idspec('REPORTER_ADD_CHOICE_002', TestAction(
        name=("Passing wrong type object to add_choice() raises "
              "SimpleBenchTypeError/REPORTER_ADD_CHOICE_INVALID_CHOICE_ARG"),
        action=reporter_factory().add_choice,
        args=["not_a_choice_conf_instance"],
        exception=SimpleBenchTypeError,
        exception_tag=ReporterErrorTag.ADD_CHOICE_INVALID_ARG_TYPE)),
    idspec('REPORTER_ADD_CHOICE_003', TestAction(
        name=("Passing Choice with a section not supported by the Reporter to add_choice() raises "
              "SimpleBenchTypeError/REPORTER_ADD_CHOICE_INVALID_SECTION_ARG"),
        action=reporter_factory().add_choice,
        args=[Choice(
                reporter=reporter_factory(),
                choice_conf=ChoiceConf(
                    **choice_conf_kwargs_factory().replace(sections=[Section.NULL])))],
        exception=SimpleBenchValueError,
        exception_tag=ReporterErrorTag.ADD_CHOICE_UNSUPPORTED_SECTION)),
    idspec('REPORTER_ADD_CHOICE_004', TestAction(
        name=("Passing Choice with a target not supported by the Reporter to add_choice() raises "
              "SimpleBenchTypeError/REPORTER_ADD_CHOICE_INVALID_TARGET_ARG"),
        action=reporter_factory().add_choice,
        args=[Choice(
            reporter=reporter_factory(),
            choice_conf=ChoiceConf(
                **choice_conf_kwargs_factory().replace(targets=[Target.CUSTOM])))],
        exception=SimpleBenchValueError,
        exception_tag=ReporterErrorTag.ADD_CHOICE_UNSUPPORTED_TARGET)),
    idspec('REPORTER_ADD_CHOICE_005', TestAction(
        name=("Passing Choice with a output_format not supported by the Reporter to add_choice() raises "
              "SimpleBenchTypeError/ADD_FORMAT_UNSUPPORTED_FORMAT"),
        action=reporter_factory().add_choice,
        args=[Choice(
            reporter=reporter_factory(),
            choice_conf=ChoiceConf(
                **choice_conf_kwargs_factory().replace(output_format=Format.CUSTOM)))],
        exception=SimpleBenchValueError,
        exception_tag=ReporterErrorTag.ADD_CHOICE_UNSUPPORTED_FORMAT)),
])
def test_add_choice(testspec: TestSpec) -> None:
    """Test Reporter.add_choice() method."""
    testspec.run()


@pytest.mark.parametrize('testspec', [
    idspec('INSTANCE_ATTRIBUTES_001', TestGet(
        name="Reporter().name attribute has the expected default value",
        obj=reporter_factory(),
        attribute='name',
        assertion=Assert.EQUAL,
        expected=default_reporter_name())),
    idspec('INSTANCE_ATTRIBUTES_002', TestSet(
        name="Reporter().name attribute is immutable",
        obj=reporter_factory(),
        attribute='name',
        value='new_name',
        exception=AttributeError)),
    idspec('INSTANCE_ATTRIBUTES_003', TestGet(
        name="Reporter().description attribute has the expected default value",
        obj=reporter_factory(),
        attribute='description',
        assertion=Assert.EQUAL,
        expected=default_description())),
    idspec('INSTANCE_ATTRIBUTES_004', TestSet(
        name="Reporter().description attribute is immutable",
        obj=reporter_factory(),
        attribute='description',
        value='new_description',
        exception=AttributeError)),
    idspec('INSTANCE_ATTRIBUTES_005', TestGet(
        name="Reporter().choices attribute is a Choices instance",
        obj=reporter_factory(),
        attribute='choices',
        assertion=Assert.ISINSTANCE,
        expected=Choices)),
    idspec('INSTANCE_ATTRIBUTES_006', TestSet(
        name="Reporter().choices attribute is immutable",
        obj=reporter_factory(),
        attribute='choices',
        value=choices_factory(),
        exception=AttributeError)),
])
def test_reporter_instance_attributes(testspec: TestSpec) -> None:
    """Test Reporter attributes."""
    testspec.run()


def reporter_class_methods_testspecs() -> list[TestSpec]:
    """Generate TestSpecs for Reporter class methods."""
    testspec: list[TestSpec] = [
        idspec('CLASS_METHODS_001', TestAction(
            name="Reporter.get_hardcoded_default_options() class method returns expected value with expected type",
            action=Reporter.get_hardcoded_default_options,
            assertion=Assert.ISINSTANCE,
            expected=ReporterOptions)),
        idspec('CLASS_METHODS_002', TestAction(
            name="Reporter.get_default_options() class method returns ReporterOptions with expected type",
            action=Reporter.get_default_options,
            assertion=Assert.ISINSTANCE,
            expected=ReporterOptions)),
        idspec('CLASS_METHODS_003', TestAction(
            name="Reporter.set_default_options() sets default options",
            action=Reporter.set_default_options,
            args=[ReporterOptions()],
            expected=NO_EXPECTED_VALUE)),
        idspec('CLASS_METHODS_004', TestAction(
            name=("Reporter.set_default_options() with bad type raises "
                  "SimpleBenchTypeError/SET_DEFAULT_OPTIONS_INVALID_ARG_TYPE"),
            action=Reporter.set_default_options,
            args=["not_a_reporter_options_instance"],
            exception=SimpleBenchTypeError,
            exception_tag=ReporterErrorTag.SET_DEFAULT_OPTIONS_INVALID_OPTIONS_ARG_TYPE)),
    ]

    def vanilla_default_options_is_hardcoded_default_options() -> None:
        """Validate that get_default_options() returns the same value as get_hardcoded_default_options().

        After resetting the default options by calling set_default_options(None),
        the get_default_options() class method should return the same object instance as
        returned by the get_hardcoded_default_options() class method.

        Returns:
            None
        Raises:
            AssertionError if the test fails.
        """
        Reporter.set_default_options(None)  # Reset to hard coded defaults
        hard_coded_options = Reporter.get_hardcoded_default_options()
        original_default_options = Reporter.get_default_options()
        assert hard_coded_options is original_default_options, (
            "get_default_options() does not return the hard coded instance after reset with None")
    testspec.append(idspec(
        'CLASS_METHODS_005', TestAction(
            name=("Reporter.get_default_options() returns hard coded default options by default"),
            action=vanilla_default_options_is_hardcoded_default_options)))

    def default_options_changes_after_set() -> None:
        """Validate that get_default_options() returns a different instance after set_default_options().

        After calling set_default_options() with a new ReporterOptions instance,
        the get_default_options() class method should return a different instance
        than it did before the set_default_options() call.

        Additionally, after resetting the default options by calling set_default_options(None),
        get_default_options() should again return the original hard coded instance.

        Returns:
            None
        Raises:
            AssertionError if the test fails.
        """
        Reporter.set_default_options(None)  # Reset to hard coded defaults
        hardcoded_options: ReporterOptions = Reporter.get_default_options()
        new_options = ReporterOptions()
        Reporter.set_default_options(new_options)
        post_set_options = Reporter.get_default_options()

        assert hardcoded_options is not post_set_options, (
            "get_default_options() did not return a different instance after set_default_options()")
        assert new_options is post_set_options, (
            "get_default_options() does not return the new ReporterOptions instance after set_default_options()")
    testspec.append(idspec(
        'CLASS_METHODS_006', TestAction(
            name=("Reporter.get_default_options() returns different instance after set_default_options()"),
            action=default_options_changes_after_set)))

    def default_options_sets_and_resets() -> None:
        """Validate that default options set and reset correctly).

        Validate that after calling set_default_options() with a new ReporterOptions instance,
        the get_default_options() class method returns a different instance
        than it did before the set_default_options() call and that after resetting the default options
        by calling set_default_options(None), get_default_options() again returns the original hard coded instance

        Returns:
            None
        Raises:
            AssertionError if the test fails.
        """
        Reporter.set_default_options(None)  # Reset to hard coded defaults
        hardcoded_options: ReporterOptions = Reporter.get_hardcoded_default_options()
        new_options = ReporterOptions()
        Reporter.set_default_options(new_options)
        post_set_options = Reporter.get_default_options()

        assert hardcoded_options is not post_set_options, (
            "get_default_options() did not return a different instance after set_default_options()")
        assert new_options is post_set_options, (
            "get_default_options() does not return the new ReporterOptions instance after set_default_options()")

        Reporter.set_default_options(None)  # Reset to hard coded defaults
        reset_options = Reporter.get_default_options()
        assert hardcoded_options is reset_options, (
            "get_default_options() does not return the hard coded instance after reset with None")
    testspec.append(idspec(
        'CLASS_METHODS_007', TestAction(
            name=("default options can be set and reset correctly"),
            action=default_options_sets_and_resets)))

    return testspec


@pytest.mark.parametrize('testspec', reporter_class_methods_testspecs())
def test_reporter_class_methods(testspec: TestSpec) -> None:
    """Test Reporter class methods and properties."""
    testspec.run()


def find_options_by_type_testspecs() -> list[TestSpec]:
    """Generate TestSpecs the find_options_by_type instance method."""

    class ReporterOptionsOne(ReporterOptions):
        """A dummy ReporterOptions subclass for testing purposes."""

    class ReporterOptionsTwo(ReporterOptions):
        """A second dummy ReporterOptions subclass for testing purposes."""

    options_one = ReporterOptionsOne()
    options_two = ReporterOptionsTwo()
    empty_options_list: list[ReporterOptions] = []
    options_two_only_list: list[ReporterOptions] = [options_two]
    fully_populated_options_list: list[ReporterOptions] = [options_one, options_two]
    reporter = reporter_factory()

    testspecs: list[TestSpec] = [
        idspec('FIND_OPTIONS_BY_TYPE_001', TestAction(
            name="find_options_by_type() with empty list returns None",
            action=reporter.find_options_by_type,
            kwargs={'options': empty_options_list, 'cls': ReporterOptionsOne},
            assertion=Assert.IS_NONE)),
        idspec('FIND_OPTIONS_BY_TYPE_002', TestAction(
            name="find_options_by_type() full list with single matching type returns correct item",
            action=reporter.find_options_by_type,
            kwargs={'options': fully_populated_options_list, 'cls': ReporterOptionsTwo},
            assertion=Assert.IS,
            expected=options_two)),
        idspec('FIND_OPTIONS_BY_TYPE_003', TestAction(
            name="find_options_by_type() list with only one matching type returns correct item",
            action=reporter.find_options_by_type,
            kwargs={'options': options_two_only_list, 'cls': ReporterOptionsTwo},
            assertion=Assert.IS,
            expected=options_two)),
        idspec('FIND_OPTIONS_BY_TYPE_004', TestAction(
            name="find_options_by_type() with options but no matching type returns None",
            action=reporter.find_options_by_type,
            kwargs={'options': options_two_only_list, 'cls': ReporterOptionsOne},
            assertion=Assert.IS_NONE)),
        idspec('FIND_OPTIONS_BY_TYPE_005', TestAction(
            name=("find_options_by_type() with invalid cls arg raises "
                  "SimpleBenchTypeError/FIND_OPTIONS_BY_TYPE_INVALID_CLS_ARG_TYPE"),
            action=reporter.find_options_by_type,
            kwargs={'options': fully_populated_options_list, 'cls': "not_a_reporter_options_type"},
            exception=SimpleBenchTypeError,
            exception_tag=ReporterErrorTag.FIND_OPTIONS_BY_TYPE_INVALID_CLS_ARG_TYPE)),
        idspec('FIND_OPTIONS_BY_TYPE_006', TestAction(
            name=("find_options_by_type() with invalid options arg raises "
                  "SimpleBenchTypeError/FIND_OPTIONS_BY_TYPE_INVALID_OPTIONS_ARG"),
            action=reporter.find_options_by_type,
            kwargs={'options': "not_a_list", 'cls': ReporterOptionsOne},
            exception=SimpleBenchTypeError,
            exception_tag=ReporterErrorTag.FIND_OPTIONS_BY_TYPE_INVALID_OPTIONS_ARG)),
        idspec('FIND_OPTIONS_BY_TYPE_007', TestAction(
            name=("find_options_by_type() with options arg containing invalid item type raises "
                  "SimpleBenchTypeError/FIND_OPTIONS_BY_TYPE_INVALID_OPTIONS_ARG"),
            action=reporter.find_options_by_type,
            kwargs={'options': [options_one, "not_a_reporter_options_instance"], 'cls': ReporterOptionsOne},
            exception=SimpleBenchTypeError,
            exception_tag=ReporterErrorTag.FIND_OPTIONS_BY_TYPE_INVALID_OPTIONS_ARG)),
        idspec('FIND_OPTIONS_BY_TYPE_008', TestAction(
            name="find_options_by_type() with None options arg returns None",
            action=reporter.find_options_by_type,
            kwargs={'options': None, 'cls': ReporterOptionsOne},
            assertion=Assert.IS_NONE)),
    ]

    return testspecs


@pytest.mark.parametrize('testspec', find_options_by_type_testspecs())
def test_find_options_by_type(testspec: TestSpec) -> None:
    """Test Reporter.find_options_by_type() method."""
    testspec.run()


def run_report_testspecs() -> list[TestSpec]:
    """Generate TestSpecs for Reporter.run_report()."""
    testspecs: list[TestSpec] = [
        idspec('RUN_REPORT_001', TestAction(
            name="run_report() with all valid args runs successfully",
            action=reporter_factory().run_report,
            kwargs={
                'args': namespace_factory(),
                'case': case_factory(),
                'choice': choice_factory(),
                'path': path_factory(),
                'session': session_factory(),
                'callback': default_reporter_callback,
            },
            expected=NO_EXPECTED_VALUE)),
        idspec('RUN_REPORT_002', TestAction(
            name="run_report() with minimal args runs successfully",
            action=reporter_factory().run_report,
            kwargs={
                'args': namespace_factory(),
                'case': case_factory(),
                'choice': choice_factory(),
            })),
    ]
    return testspecs


@pytest.mark.parametrize('testspec', run_report_testspecs())
def test_run_report(testspec: TestSpec) -> None:
    """Test Reporter.run_report() method."""
    testspec.run()
