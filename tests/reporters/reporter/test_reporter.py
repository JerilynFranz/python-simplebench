"""Test simplebench/reporters/reporter/reporter.py module"""
from __future__ import annotations

from argparse import Namespace
from pathlib import Path
from typing import Any, ClassVar, Optional

import pytest

from simplebench.case import Case
from simplebench.enums import Format, Section, Target
from simplebench.exceptions import SimpleBenchTypeError, SimpleBenchValueError
from simplebench.iteration import Iteration
from simplebench.reporters.choice import Choice, ChoiceConf
from simplebench.reporters.choices import Choices
from simplebench.reporters.log.versions.v1 import ReportMetadata
from simplebench.reporters.protocols import ReporterCallback
from simplebench.reporters.reporter import Reporter, ReporterOptions
from simplebench.reporters.reporter.exceptions import _ReporterErrorTag
from simplebench.reporters.reporter.protocols import ReporterProtocol
from simplebench.results import Results
from simplebench.runners import SimpleRunner
from simplebench.session import Session

from ...factories import (
    FactoryReporter,
    FactoryReporterOptions,
    case_factory,
    choice_conf_factory,
    choice_conf_kwargs_factory,
    choice_factory,
    choices_factory,
    default_description,
    default_reporter_callback,
    default_reporter_name,
    namespace_factory,
    path_factory,
    report_log_metadata_factory,
    report_parameters_factory,
    reporter_config_factory,
    reporter_factory,
    session_factory,
)
from ...testspec import NO_EXPECTED_VALUE, Assert, TestAction, TestGet, TestSet, TestSpec, idspec


def broken_benchcase_missing_bench(**kwargs: Any) -> Results:  # pylint: disable=unused-argument  # pragma: no cover
    """A broken benchmark case function that is missing the required 'bench' parameter.

    The function signature is intentionally incorrect for testing purposes.

    :param kwargs: Keyword arguments.
    :type kwargs: Any
    :return: A dummy Results instance.
    :rtype: Results
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

    :param bench: The benchmark runner.
    :type bench: SimpleRunner
    :return: A dummy Results instance.
    :rtype: Results
    """
    # Nothing inside this actually runs since it's just for testing Reporter's
    # error handling for an invalid function type signature.
    return Results(  # made-up results for testing purposes
            group='test_case', title='Test Case',
            description='A test case for testing.',
            n=10, rounds=1, total_elapsed=3.0,
            iterations=[Iteration(elapsed=1.0), Iteration(elapsed=2.0)])


class GoodReporterOptions(ReporterOptions):
    """A good dummy ReporterOptions subclass for testing purposes."""


class GoodReporter(Reporter):
    """A good dummy Reporter subclass for testing purposes.

    """
    _OPTIONS_TYPE: ClassVar[type[GoodReporterOptions]] = GoodReporterOptions  # pylint: disable=line-too-long  # type: ignore[reportInvalidVariableOverride]  # noqa: E501
    """The ReporterOptions subclass type for the reporter: `GoodReporterOptions`"""
    _OPTIONS_KWARGS: ClassVar[dict[str, Any]] = {}
    """Keyword arguments for constructing a GoodReporterOptions hardcoded default instance: `{}`"""

    def __init__(self) -> None:
        super().__init__(reporter_config_factory())

    def run_report(self,  # pylint: disable=useless-parent-delegation
                   *,
                   args: Namespace,
                   log_metadata: ReportMetadata,
                   case: Case,
                   choice: Choice,
                   path: Optional[Path] = None,
                   session: Optional[Session] = None,
                   callback: Optional[ReporterCallback] = None) -> None:
        return

    def render(self, *, case: Case, section: Section, options: ReporterOptions) -> str:
        """Dummy render method for testing.

        :param case: The benchmark case.
        :type case: Case
        :param section: The report section.
        :type section: Section
        :param options: The reporter options.
        :type options: ReporterOptions
        :return: An empty string.
        :rtype: str
        """
        return ""


def test_good_reporter_subclassing() -> None:
    """Test that GoodReporter subclass can be instantiated and run_report works."""
    reporter = GoodReporter()
    if not isinstance(reporter, ReporterProtocol):  # type: ignore[reportGeneralTypeIssue]
        raise AssertionError("GoodReporter does not conform to ReporterProtocol")

    assert isinstance(reporter, Reporter)
    # Call run_report with minimal valid parameters
    reporter.run_report(
        args=namespace_factory(),
        log_metadata=report_log_metadata_factory(),
        case=case_factory(),
        choice=choice_factory()
    )  # Should not raise any exceptions


def test_factory_reporter_subclassing() -> None:
    """Test that FactoryReporter subclass can be instantiated and run_report works."""
    reporter = FactoryReporter(reporter_config_factory())
    if not isinstance(reporter, ReporterProtocol):  # type: ignore[reportGeneralTypeIssue]
        raise AssertionError("FactoryReporter does not conform to ReporterProtocol")

    assert isinstance(reporter, Reporter)
    # Call run_report with minimal valid parameters
    reporter.run_report(
        args=namespace_factory(),
        log_metadata=report_log_metadata_factory(),
        case=case_factory(),
        choice=choice_factory(),
        path=path_factory()
    )  # Should not raise any exceptions


@pytest.mark.parametrize('testspec', [
    idspec('REPORTER_001', TestAction(
        name="abstract base class Reporter() cannot be instantiated directly",
        action=Reporter,
        exception=TypeError)),
    idspec('REPORTER_002', TestAction(
        name="reporter_factory() is creating valid FactoryReporter instances",
        action=reporter_factory,
        assertion=Assert.ISINSTANCE,
        expected=FactoryReporter)),
    idspec('REPORTER_003', TestAction(
        name="Correctly configured subclass of Reporter() can call report() successfully",
        action=reporter_factory().report,
        kwargs=report_parameters_factory(),
        validate_result=lambda result: result is None)),
    idspec('REPORTER_004', TestAction(
        name="FactoryReporter() can be instantiated with parameters from reporter_config_factory()",
        action=FactoryReporter,
        args=[reporter_config_factory()],
        assertion=Assert.ISINSTANCE,
        expected=FactoryReporter)),
    idspec('REPORTER_005', TestAction(
        name="Correctly configured Reporter() can call report() successfully",
        action=FactoryReporter(reporter_config_factory()).report,
        kwargs=report_parameters_factory(),
        expected=NO_EXPECTED_VALUE)),
    idspec('REPORTER_006', TestAction(
        name="Attempt to directly instantiate Reporter raises TypeError",
        action=Reporter,
        args=[reporter_config_factory()],
        exception=TypeError)),
])
def test_reporter_init(testspec: TestSpec) -> None:
    """Test Reporter init parameters.

    :param testspec: The test specification.
    :type testspec: TestSpec
    """
    testspec.run()


@pytest.mark.parametrize('testspec', [
    idspec('REPORT_001', TestAction(
        name=("report() with non-Case arg raises "
              "SimpleBenchTypeError/REPORTER_REPORT_INVALID_CASE_ARG"),
        action=reporter_factory().report,
        kwargs={'args': namespace_factory(),
                'log_metadata': report_log_metadata_factory(),
                'case': "not_a_case_instance",
                'choice': choice_conf_factory()},
        exception=SimpleBenchTypeError,
        exception_tag=_ReporterErrorTag.REPORT_INVALID_CASE_ARG)),
    idspec('REPORT_002', TestAction(
        name=("report() with non-Choice arg raises "
              "SimpleBenchTypeError/REPORTER_REPORT_INVALID_CHOICE_ARG"),
        action=reporter_factory().report,
        kwargs={'args': namespace_factory(),
                'log_metadata': report_log_metadata_factory(),
                'case': case_factory(),
                'choice': "not_a_choice_conf_instance"},
        exception=SimpleBenchTypeError,
        exception_tag=_ReporterErrorTag.REPORT_INVALID_CHOICE_ARG)),
    idspec('REPORT_003', TestAction(
        name=("report() with non-Choice choice arg raises "
              "SimpleBenchTypeError/REPORTER_REPORT_INVALID_CHOICE_ARG"),
        action=reporter_factory().report,
        kwargs={'args': namespace_factory(),
                'log_metadata': report_log_metadata_factory(),
                'case': case_factory(),
                'choice': Choices()},  # passing Choices instead of Choice
        exception=SimpleBenchTypeError,
        exception_tag=_ReporterErrorTag.REPORT_INVALID_CHOICE_ARG)),
    idspec('REPORT_004', TestAction(
        name=("report() with Section not in Reporter's sections raises "
              "SimpleBenchValueError/REPORTER_REPORT_UNSUPPORTED_SECTION"),
        action=reporter_factory().report,
        kwargs={'args': namespace_factory(),
                'log_metadata': report_log_metadata_factory(),
                'case': case_factory(),
                'choice': Choice(
                    reporter=reporter_factory(),
                    choice_conf=ChoiceConf(
                        **choice_conf_kwargs_factory().replace(sections=[Section.NULL])))},
        exception=SimpleBenchValueError,
        exception_tag=_ReporterErrorTag.REPORT_UNSUPPORTED_SECTION)),
    idspec('REPORT_005', TestAction(
        name=("report() with Target not in Reporter's targets raises "
              "SimpleBenchValueError/REPORTER_REPORT_UNSUPPORTED_TARGET"),
        action=reporter_factory().report,
        kwargs={'args': namespace_factory(),
                'log_metadata': report_log_metadata_factory(),
                'case': case_factory(),
                'choice': Choice(
                    reporter=reporter_factory(),
                    choice_conf=ChoiceConf(
                        **choice_conf_kwargs_factory().replace(targets=[Target.CUSTOM])))},
        exception=SimpleBenchValueError,
        exception_tag=_ReporterErrorTag.REPORT_UNSUPPORTED_TARGET)),
    idspec('REPORT_006', TestAction(
        name=("report() with output_format not in Reporter's formats raises "
              "SimpleBenchValueError/REPORTER_REPORT_UNSUPPORTED_FORMAT"),
        action=reporter_factory().report,
        kwargs={'args': namespace_factory(),
                'log_metadata': report_log_metadata_factory(),
                'case': case_factory(),
                'choice': Choice(
                    reporter=reporter_factory(),
                    choice_conf=ChoiceConf(
                        **choice_conf_kwargs_factory().replace(output_format=Format.CUSTOM)))},
        exception=SimpleBenchValueError,
        exception_tag=_ReporterErrorTag.REPORT_UNSUPPORTED_FORMAT)),
    idspec('REPORT_007', TestAction(
        name="report() with valid Case and Choice runs successfully",
        action=reporter_factory().report,
        kwargs={'args': namespace_factory(),
                'log_metadata': report_log_metadata_factory(),
                'case': case_factory(),
                'choice': choice_factory(),
                'path': path_factory()},
        expected=NO_EXPECTED_VALUE)),
    idspec('REPORT_008', TestAction(
        name="report() with valid callback runs successfully",
        action=reporter_factory().report,
        kwargs={'args': namespace_factory(),
                'log_metadata': report_log_metadata_factory(),
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
                'log_metadata': report_log_metadata_factory(),
                'case': case_factory(),
                'choice': Choice(
                    reporter=reporter_factory(),
                    choice_conf=ChoiceConf(
                        **choice_conf_kwargs_factory().replace(targets=[Target.CALLBACK]))),
                'callback': "not_a_callback"},
        exception=SimpleBenchTypeError,
        exception_tag=_ReporterErrorTag.REPORT_INVALID_CALLBACK_ARG)),
    idspec('REPORT_010', TestAction(
        name="report() with valid path runs successfully",
        action=reporter_factory().report,
        kwargs={'args': namespace_factory(),
                'log_metadata': report_log_metadata_factory(),
                'case': case_factory(),
                'choice': choice_factory(),
                'path': path_factory()},
        expected=NO_EXPECTED_VALUE)),
    idspec('REPORT_011', TestAction(
        name=("report() with invalid path raises "
              "SimpleBenchTypeError/REPORTER_REPORT_INVALID_PATH_ARG"),
        action=reporter_factory().report,
        kwargs={'args': namespace_factory(),
                'log_metadata': report_log_metadata_factory(),
                'case': case_factory(),
                'choice': choice_factory(),
                'path': "not_a_path"},
        exception=SimpleBenchTypeError,
        exception_tag=_ReporterErrorTag.REPORT_INVALID_PATH_ARG)),
    idspec('REPORT_012', TestAction(
        name=("report() with valid session runs successfully"),
        action=reporter_factory().report,
        kwargs={'args': namespace_factory(),
                'log_metadata': report_log_metadata_factory(),
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
                'log_metadata': report_log_metadata_factory(),
                'case': case_factory(),
                'choice': choice_factory(),
                'path': path_factory(),
                'session': "not_a_session"},
        exception=SimpleBenchTypeError,
        exception_tag=_ReporterErrorTag.REPORT_INVALID_SESSION_ARG)),
    idspec('REPORT_014', TestAction(
        name="report() invalid args type raises SimpleBenchTypeError/REPORT_INVALID_ARGS_ARG_TYPE",
        action=reporter_factory().report,
        kwargs={'args': "not_a_namespace",
                'log_metadata': report_log_metadata_factory(),
                'case': case_factory(),
                'choice': choice_factory(),
                'path': path_factory(),
                'session': session_factory()},
        exception=SimpleBenchTypeError,
        exception_tag=_ReporterErrorTag.REPORT_INVALID_ARGS_ARG_TYPE)),
    idspec('REPORT_015', TestAction(
        name="report() with missing args raises TypeError",
        action=reporter_factory().report,
        kwargs={'log_metadata': report_log_metadata_factory(),
                'case': case_factory(),
                'choice': choice_factory(),
                'path': path_factory(),
                'session': session_factory()},
        exception=TypeError)),
    idspec('REPORT_016', TestAction(
        name="report() with missing case raises TypeError",
        action=reporter_factory().report,
        kwargs={'args': namespace_factory(),
                'log_metadata': report_log_metadata_factory(),
                'choice': choice_factory(),
                'path': path_factory(),
                'session': session_factory()},
        exception=TypeError)),
    idspec('REPORT_017', TestAction(
        name="report() with missing choice raises TypeError",
        action=reporter_factory().report,
        kwargs={'args': namespace_factory(),
                'log_metadata': report_log_metadata_factory(),
                'case': case_factory(),
                'path': path_factory(),
                'session': session_factory()},
        exception=TypeError)),
])
def test_report(testspec: TestSpec) -> None:
    """Test Reporter.report() method.

    :param testspec: The test specification.
    :type testspec: TestSpec
    """
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
        exception_tag=_ReporterErrorTag.ADD_CHOICE_INVALID_ARG_TYPE)),
    idspec('REPORTER_ADD_CHOICE_003', TestAction(
        name=("Passing Choice with a section not supported by the Reporter to add_choice() raises "
              "SimpleBenchTypeError/REPORTER_ADD_CHOICE_INVALID_SECTION_ARG"),
        action=reporter_factory().add_choice,
        args=[Choice(
                reporter=reporter_factory(),
                choice_conf=ChoiceConf(
                    **choice_conf_kwargs_factory().replace(sections=[Section.NULL])))],
        exception=SimpleBenchValueError,
        exception_tag=_ReporterErrorTag.ADD_CHOICE_UNSUPPORTED_SECTION)),
    idspec('REPORTER_ADD_CHOICE_004', TestAction(
        name=("Passing Choice with a target not supported by the Reporter to add_choice() raises "
              "SimpleBenchTypeError/REPORTER_ADD_CHOICE_INVALID_TARGET_ARG"),
        action=reporter_factory().add_choice,
        args=[Choice(
            reporter=reporter_factory(),
            choice_conf=ChoiceConf(
                **choice_conf_kwargs_factory().replace(targets=[Target.CUSTOM])))],
        exception=SimpleBenchValueError,
        exception_tag=_ReporterErrorTag.ADD_CHOICE_UNSUPPORTED_TARGET)),
    idspec('REPORTER_ADD_CHOICE_005', TestAction(
        name=("Passing Choice with a output_format not supported by the Reporter to add_choice() raises "
              "SimpleBenchTypeError/ADD_FORMAT_UNSUPPORTED_FORMAT"),
        action=reporter_factory().add_choice,
        args=[Choice(
            reporter=reporter_factory(),
            choice_conf=ChoiceConf(
                **choice_conf_kwargs_factory().replace(output_format=Format.CUSTOM)))],
        exception=SimpleBenchValueError,
        exception_tag=_ReporterErrorTag.ADD_CHOICE_UNSUPPORTED_FORMAT)),
])
def test_add_choice(testspec: TestSpec) -> None:
    """Test Reporter.add_choice() method.

    :param testspec: The test specification.
    :type testspec: TestSpec
    """
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
    """Test Reporter attributes.

    :param testspec: The test specification.
    :type testspec: TestSpec
    """
    testspec.run()


def reporter_class_methods_testspecs() -> list[TestSpec]:
    """Generate TestSpecs for Reporter class methods.

    :return: A list of test specifications.
    :rtype: list[TestSpec]
    """
    testspec: list[TestSpec] = [
        idspec('CLASS_METHODS_001', TestAction(
            name="Reporter.get_hardcoded_default_options() class method returns expected value with expected type",
            action=FactoryReporter.get_hardcoded_default_options,
            assertion=Assert.ISINSTANCE,
            expected=FactoryReporterOptions)),
        idspec('CLASS_METHODS_002', TestAction(
            name="Reporter.get_default_options() class method returns ReporterOptions with expected type",
            action=FactoryReporter.get_default_options,
            assertion=Assert.ISINSTANCE,
            expected=FactoryReporterOptions)),
        idspec('CLASS_METHODS_003', TestAction(
            name="Reporter.set_default_options() sets default options",
            action=FactoryReporter.set_default_options,
            args=[FactoryReporterOptions()],
            expected=NO_EXPECTED_VALUE)),
        idspec('CLASS_METHODS_004', TestAction(
            name=("Reporter.set_default_options() with bad type raises "
                  "SimpleBenchTypeError/SET_DEFAULT_OPTIONS_INVALID_ARG_TYPE"),
            action=FactoryReporter.set_default_options,
            args=["not_a_reporter_options_instance"],
            exception=SimpleBenchTypeError,
            exception_tag=_ReporterErrorTag.SET_DEFAULT_OPTIONS_INVALID_OPTIONS_ARG_TYPE)),
    ]

    def vanilla_default_options_is_hardcoded_default_options() -> None:
        """Validate that get_default_options() returns the same value as get_hardcoded_default_options().

        After resetting the default options by calling set_default_options(None),
        the get_default_options() class method should return the same object instance as
        returned by the get_hardcoded_default_options() class method.

        :return: None
        :raises AssertionError: if the test fails.
        """
        FactoryReporter.set_default_options(None)  # Reset to hard coded defaults
        hard_coded_options = FactoryReporter.get_hardcoded_default_options()
        original_default_options = FactoryReporter.get_default_options()
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

        :return: None
        :raises AssertionError: if the test fails.
        """
        FactoryReporter.set_default_options(None)  # Reset to hard coded defaults
        hardcoded_options = FactoryReporter.get_default_options()
        new_options = FactoryReporterOptions()
        FactoryReporter.set_default_options(new_options)
        post_set_options = FactoryReporter.get_default_options()

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

        :return: None
        :raises AssertionError: if the test fails.
        """
        FactoryReporter.set_default_options(None)  # Reset to hard coded defaults
        hardcoded_options: FactoryReporterOptions = FactoryReporter.get_hardcoded_default_options()
        new_options = FactoryReporterOptions()
        FactoryReporter.set_default_options(new_options)
        post_set_options = FactoryReporter.get_default_options()
        assert hardcoded_options is not post_set_options, (
            "get_default_options() did not return a different instance after set_default_options()")
        assert new_options is post_set_options, (
            "get_default_options() does not return the new ReporterOptions instance after set_default_options()")

        FactoryReporter.set_default_options(None)  # Reset to hard coded defaults
        reset_options = FactoryReporter.get_default_options()
        assert hardcoded_options is reset_options, (
            "get_default_options() does not return the hard coded instance after reset with None")
    testspec.append(idspec(
        'CLASS_METHODS_007', TestAction(
            name=("default options can be set and reset correctly"),
            action=default_options_sets_and_resets)))

    return testspec


@pytest.mark.parametrize('testspec', reporter_class_methods_testspecs())
def test_reporter_class_methods(testspec: TestSpec) -> None:
    """Test Reporter class methods and properties.

    :param testspec: The test specification.
    :type testspec: TestSpec
    """
    testspec.run()


def find_options_by_type_testspecs() -> list[TestSpec]:
    """Generate TestSpecs the find_options_by_type instance method.

    :return: A list of test specifications.
    :rtype: list[TestSpec]
    """

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
            exception_tag=_ReporterErrorTag.FIND_OPTIONS_BY_TYPE_INVALID_CLS_ARG_TYPE)),
        idspec('FIND_OPTIONS_BY_TYPE_006', TestAction(
            name=("find_options_by_type() with invalid options arg raises "
                  "SimpleBenchTypeError/FIND_OPTIONS_BY_TYPE_INVALID_OPTIONS_ARG"),
            action=reporter.find_options_by_type,
            kwargs={'options': "not_a_list", 'cls': ReporterOptionsOne},
            exception=SimpleBenchTypeError,
            exception_tag=_ReporterErrorTag.FIND_OPTIONS_BY_TYPE_INVALID_OPTIONS_ARG)),
        idspec('FIND_OPTIONS_BY_TYPE_007', TestAction(
            name=("find_options_by_type() with options arg containing invalid item type raises "
                  "SimpleBenchTypeError/FIND_OPTIONS_BY_TYPE_INVALID_OPTIONS_ARG"),
            action=reporter.find_options_by_type,
            kwargs={'options': [options_one, "not_a_reporter_options_instance"], 'cls': ReporterOptionsOne},
            exception=SimpleBenchTypeError,
            exception_tag=_ReporterErrorTag.FIND_OPTIONS_BY_TYPE_INVALID_OPTIONS_ARG)),
        idspec('FIND_OPTIONS_BY_TYPE_008', TestAction(
            name="find_options_by_type() with None options arg returns None",
            action=reporter.find_options_by_type,
            kwargs={'options': None, 'cls': ReporterOptionsOne},
            assertion=Assert.IS_NONE)),
    ]

    return testspecs


@pytest.mark.parametrize('testspec', find_options_by_type_testspecs())
def test_find_options_by_type(testspec: TestSpec) -> None:
    """Test Reporter.find_options_by_type() method.

    :param testspec: The test specification.
    :type testspec: TestSpec
    """
    testspec.run()


def run_report_testspecs() -> list[TestSpec]:
    """Generate TestSpecs for Reporter.run_report().

    :return: A list of test specifications.
    :rtype: list[TestSpec]
    """
    testspecs: list[TestSpec] = [
        idspec('RUN_REPORT_001', TestAction(
            name="run_report() with all valid args runs successfully",
            action=reporter_factory().run_report,
            kwargs={
                'args': namespace_factory(),
                'log_metadata': report_log_metadata_factory(),
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
                'log_metadata': report_log_metadata_factory(),
                'case': case_factory(),
                'choice': choice_factory(),
                'path': path_factory(),
            })),
    ]
    return testspecs


@pytest.mark.parametrize('testspec', run_report_testspecs())
def test_run_report(testspec: TestSpec) -> None:
    """Test Reporter.run_report() method.

    :param testspec: The test specification.
    :type testspec: TestSpec
    """
    testspec.run()
