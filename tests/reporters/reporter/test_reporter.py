"""Test simplebench/reporters/interfaces.py module"""
from __future__ import annotations
from argparse import Namespace
from pathlib import Path
from typing import Any, Optional

import pytest

from simplebench.case import Case
from simplebench.enums import Section, Target, Format
from simplebench.exceptions import SimpleBenchNotImplementedError, SimpleBenchValueError, SimpleBenchTypeError
from simplebench.iteration import Iteration
from simplebench.reporters.protocols import ReporterCallback
from simplebench.reporters.choice import Choice, ChoiceConf
from simplebench.reporters.choices import Choices
from simplebench.reporters.reporter.exceptions import ReporterErrorTag
from simplebench.reporters.reporter import Reporter
from simplebench.results import Results
from simplebench.runners import SimpleRunner
from simplebench.session import Session

from ...factories import (
    choice_factory, choice_conf_factory, reporter_kwargs_factory, default_reporter_callback,
    case_factory, namespace_factory, reporter_factory, FactoryReporter, path_factory,
    default_description, report_parameters_factory, choice_conf_kwargs_factory,
    session_factory, default_reporter_name, choices_factory)
from ...testspec import TestAction, TestSpec, idspec, NO_EXPECTED_VALUE, Assert


def broken_benchcase_missing_bench(**kwargs: Any) -> Results:  # pylint: disable=unused-argument  # pragma: no cover
    """A broken benchmark case function that is missing the required 'bench' parameter.

    The function signature is intentionally incorrect for testing purposes.
    """
    # Nothing inside this actually runs since it's just for testing Reporter's
    # error handling for an invalid function type signature.
    return Results(  # made-up results for testing purposes
            group='test_case', title='Test Case',
            description='A test case for testing.',
            n=10, total_elapsed=3.0,
            iterations=[Iteration(elapsed=1.0), Iteration(elapsed=2.0)])


def broken_benchcase_missing_kwargs(
        bench: SimpleRunner) -> Results:  # pylint: disable=unused-argument  # pragma: no cover
    """A broken benchmark case function that is missing the required 'bench' parameter.

    The function signature is intentionally incorrect for testing purposes.
    """
    # Nothing inside this actually runs since it's just for testing Reporter's
    # error handling for an invalid function type signature.
    return Results(  # made-up results for testing purposes
            group='test_case', title='Test Case',
            description='A test case for testing.',
            n=10, total_elapsed=3.0,
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
        name="configured subclass of Reporter() can be instantiated",
        action=reporter_factory,
        assertion=Assert.ISINSTANCE,
        expected=FactoryReporter)),
    idspec('REPORTER_005', TestAction(
        name="Correctly configured subclass of Reporter() can call report() successfully",
        action=reporter_factory().report,
        kwargs=report_parameters_factory(),
        validate_result=lambda result: result is None)),
    idspec('REPORTER_006', TestAction(
        name="Correctly configured Reporter() can be instantated",
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
        name=("Init of Reporter with missing name raises "
              "SimpleBenchTypeError/NAME_INVALID_ARG_TYPE"),
        action=FactoryReporter,
        kwargs=reporter_kwargs_factory() - ['name'],
        exception=SimpleBenchTypeError,
        exception_tag=ReporterErrorTag.NAME_INVALID_ARG_TYPE)),
    idspec('REPORTER_009', TestAction(
        name=("Init of Reporter with missing description raises "
              "SimpleBenchTypeError/DESCRIPTION_INVALID_ARG_TYPE"),
        action=FactoryReporter,
        kwargs=reporter_kwargs_factory() - ['description'],
        exception=SimpleBenchTypeError,
        exception_tag=ReporterErrorTag.DESCRIPTION_INVALID_ARG_TYPE)),
    idspec('REPORTER_010', TestAction(
        name=("Init of Reporter with missing sections raises "
              "SimpleBenchTypeError/SECTIONS_INVALID_ARG_TYPE"),
        action=FactoryReporter,
        kwargs=reporter_kwargs_factory() - ['sections'],
        exception=SimpleBenchTypeError,
        exception_tag=ReporterErrorTag.SECTIONS_INVALID_ARG_TYPE)),
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
        name=("Init of FactoryReporter with missing choices raises "
              "SimpleBenchTypeError/CHOICES_INVALID_ARG_TYPE"),
        action=FactoryReporter,
        kwargs=reporter_kwargs_factory() - ['choices'],
        exception=SimpleBenchTypeError,
        exception_tag=ReporterErrorTag.CHOICES_INVALID_ARG_TYPE)),
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
])
def test_reporter_report(testspec: TestSpec) -> None:
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


def test_attributes() -> None:
    """Test Reporter attributes.

    Verify that Reporter attributes are correctly set and immutable.
    """
    reporter = reporter_factory()
    assert reporter.name == default_reporter_name(), "Failed to get Reporter.name"
    assert reporter.description == default_description(), "Failed to get Reporter.description"
    choices = reporter.choices
    assert isinstance(choices, Choices), "Failed to get Reporter.choices"

    # Verify immutability of attributes
    with pytest.raises(AttributeError):
        reporter.name = default_reporter_name()  # type: ignore[assignment,misc]
    with pytest.raises(AttributeError):
        reporter.description = default_description()  # type: ignore[assignment,misc]
    with pytest.raises(AttributeError):
        reporter.choices = choices_factory()  # type: ignore[assignment,misc]
