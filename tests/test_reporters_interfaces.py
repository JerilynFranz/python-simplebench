"""Test simplebench/reporters/interfaces.py module"""
from __future__ import annotations
from argparse import ArgumentParser
from pathlib import Path
from typing import Any, Optional, Sequence

import pytest

from simplebench.case import Case
from simplebench.enums import Section, Target, Format
from simplebench.exceptions import SimpleBenchNotImplementedError, SimpleBenchValueError, SimpleBenchTypeError, ErrorTag
from simplebench.iteration import Iteration
from simplebench.protocols import ReporterCallback
from simplebench.reporters.choices import Choice, Choices
from simplebench.reporters.interfaces import Reporter
from simplebench.results import Results
from simplebench.session import Session

from .testspec import TestAction, TestSpec, idspec, NO_EXPECTED_VALUE


def mock_path() -> Path:
    """Return a mock Path instance for testing purposes."""
    return Path('/tmp/mock_report.txt')  # pragma: no cover (path not actually used)


def mock_callback(
        *, case: Case, section: Section, output_format: Format, output: Any) -> None:  # pylint: disable=unused-argument
    """A mock callback function for testing purposes."""
    return None  # pragma: no cover


class MockChoice(Choice):
    """A dummy Choice subclass for testing purposes.

    Creates a Choice with default parameters for testing that can be overridden as needed.

    """
    def __init__(self,
                 flags: Optional[list[str]] = None,
                 name: Optional[str] = None,
                 description: Optional[str] = None,
                 sections: Optional[Sequence[Section]] = None,
                 targets: Optional[Sequence[Target]] = None,
                 formats: Optional[Sequence[Format]] = None) -> None:
        super().__init__(
            reporter=MockReporter(),
            flags=flags or ['--dummy'],
            name=name or 'dummy',
            description=description or 'A dummy choice for testing.',
            sections=sections or [Section.OPS],
            targets=targets or [Target.CONSOLE, Target.CALLBACK, Target.FILESYSTEM],
            formats=formats or [Format.RICH_TEXT],
            extra=None)


class MockChoices(Choices):
    """A dummy Choices subclass for testing purposes."""
    def __init__(self) -> None:
        super().__init__()
        self.add(MockChoice())


class MockCase(Case):
    """A dummy Case subclass for testing purposes."""
    def __init__(self) -> None:
        super().__init__(
            group='test_case',
            title='Test Case',
            description='A test case for testing.',
            action=lambda bench, **kwargs: Results(
                group='test_case',
                title='Test Case',
                description='A test case for testing.',
                n=1))
        self.results.append(Results(
            group='test_case',
            title='Test Case',
            description='A test case for testing.',
            n=1,
            iterations=[Iteration(), Iteration(), Iteration()]))


class MockSession(Session):
    """A dummy Session subclass for testing purposes."""
    def __init__(self) -> None:

        super().__init__(cases=[MockCase()])


class MockReporterInit(Reporter):
    """A dummy Reporter subclass for testing init parameters.

    This class provides a testbed for testing initialization parameters.
    """
    def __init__(self,
                 *,
                 name: Optional[str] = None,
                 description: Optional[str] = None,
                 sections: Optional[set[Section]] = None,
                 targets: Optional[set[Target]] = None,
                 formats: Optional[set[Format]] = None,
                 choices: Optional[Choices] = None) -> None:
        super().__init__(
            name=name,  # type: ignore[reportArgumentType, arg-type]
            description=description,  # type: ignore[reportArgumentType, arg-type]
            sections=sections,  # type: ignore[reportArgumentType, arg-type]
            targets=targets,  # type: ignore[reportArgumentType, arg-type]
            formats=formats,  # type: ignore[reportArgumentType, arg-type]
            choices=choices)  # type: ignore[reportArgumentType, arg-type]

    def run_report(self,
                   *,
                   case: Case,
                   choice: Choice,
                   path: Optional[Path] = None,
                   session: Optional[Session] = None,
                   callback: Optional[ReporterCallback] = None) -> None:
        return None  # pragma: no cover (not actually used)


class MockReporter(MockReporterInit):
    """A dummy Reporter subclass for testing purposes."""
    def __init__(self) -> None:
        super().__init__(
            name='dummy',
            description='A dummy reporter for testing.',
            sections={Section.OPS},
            targets={Target.CONSOLE, Target.CALLBACK, Target.FILESYSTEM},
            formats={Format.RICH_TEXT},
            choices=self._load_choices())

    def _load_choices(self) -> Choices:
        """Load the Choices instance for the reporter, including sections, output targets, and formats."""
        choices: Choices = Choices()
        choices.add(
            Choice(
                reporter=self,
                flags=['--dummy'],
                name='dummy',
                description='A dummy choice for testing.',
                sections=[Section.OPS],
                targets=[Target.CONSOLE, Target.CALLBACK, Target.FILESYSTEM],
                formats=[Format.RICH_TEXT],
                extra=None))
        return choices

    def run_report(self,
                   *,
                   case: Case,
                   choice: Choice,
                   path: Optional[Path] = None,
                   session: Optional[Session] = None,
                   callback: Optional[ReporterCallback] = None) -> None:
        return None


class BadSuperMockReporter(Reporter):
    """A dummy Reporter subclass for testing purposes.

    This class incorrectly calls super().run_report(), which should raise NotImplementedError
    when run() is called.
    """
    def __init__(self) -> None:
        super().__init__(
            name='dummy',
            description='A dummy reporter for testing.',
            sections={Section.OPS},
            targets={Target.CONSOLE, Target.CALLBACK, Target.FILESYSTEM},
            formats={Format.RICH_TEXT},
            choices=Choices([
                Choice(
                    reporter=self,
                    flags=['--dummy'],
                    name='dummy',
                    description='A dummy choice for testing.',
                    sections=[Section.OPS],
                    targets=[Target.CONSOLE, Target.CALLBACK, Target.FILESYSTEM],
                    formats=[Format.RICH_TEXT],
                    extra=None)
            ])
        )

    def run_report(self,  # pylint: disable=useless-parent-delegation
                   *,
                   case: Case,
                   choice: Choice,
                   path: Optional[Path] = None,
                   session: Optional[Session] = None,
                   callback: Optional[ReporterCallback] = None) -> None:
        """Incorrectly calls super().run_report(), which should raise NotImplementedError."""
        return super().run_report(case=case,
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
        name="configured subclass of Reporter() can be instantiated",
        action=BadSuperMockReporter,
        validate_result=lambda result: isinstance(result, BadSuperMockReporter))),
    idspec('REPORTER_003', TestAction(
        name=("calling run_report() on BadSuperMockReporter with bad run_report() super() delegation "
              "raises SimpleBenchNotImplementedError"),
        action=lambda: BadSuperMockReporter().run_report(case=MockCase(), choice=MockChoice()),
        exception=SimpleBenchNotImplementedError,
        exception_tag=ErrorTag.REPORTER_RUN_REPORT_NOT_IMPLEMENTED)),
    idspec('REPORTER_004', TestAction(
        name=("calling report() on Reporter with bad run_report() super() delegation "
              "raises SimpleBenchNotImplementedError"),
        action=lambda: BadSuperMockReporter().report(case=MockCase(), choice=MockChoice(), path=mock_path()),
        exception=SimpleBenchNotImplementedError,
        exception_tag=ErrorTag.REPORTER_RUN_REPORT_NOT_IMPLEMENTED)),
    idspec('REPORTER_005', TestAction(
        name="Correctly configured subclass of Reporter() can call report() successfully",
        action=lambda: MockReporter().report(case=MockCase(), choice=MockChoice(), path=mock_path()),
        validate_result=lambda result: result is None)),
    idspec('REPORTER_006', TestAction(
        name="Init of Reporter with missing name raises SimpleBenchNotImplementedError/REPORTER_NAME_NOT_IMPLEMENTED",
        action=MockReporterInit,
        exception=SimpleBenchNotImplementedError,
        exception_tag=ErrorTag.REPORTER_NAME_NOT_IMPLEMENTED,
        kwargs={
            'description': 'A dummy reporter for testing.',
            'sections': {Section.OPS},
            'targets': {Target.CONSOLE},
            'formats': {Format.RICH_TEXT},
            'choices': MockChoices()})),
    idspec('REPORTER_007', TestAction(
        name=("Init of Reporter with missing description raises "
              "SimpleBenchNotImplementedError/REPORTER_DESCRIPTION_NOT_IMPLEMENTED"),
        action=MockReporterInit,
        exception=SimpleBenchNotImplementedError,
        exception_tag=ErrorTag.REPORTER_DESCRIPTION_NOT_IMPLEMENTED,
        kwargs={
            'name': 'dummy',
            'sections': {Section.OPS},
            'targets': {Target.CONSOLE},
            'formats': {Format.RICH_TEXT},
            'choices': MockChoices()})),
    idspec('REPORTER_008', TestAction(
        name=("Init of Reporter with empty sections raises "
              "SimpleBenchNotImplementedError/REPORTER_SECTIONS_NOT_IMPLEMENTED"),
        action=MockReporterInit,
        exception=SimpleBenchNotImplementedError,
        exception_tag=ErrorTag.REPORTER_SECTIONS_NOT_IMPLEMENTED,
        kwargs={
            'name': 'dummy',
            'description': 'A dummy reporter for testing.',
            'sections': set(),
            'targets': {Target.CONSOLE},
            'formats': {Format.RICH_TEXT},
            'choices': MockChoices()})),
    idspec('REPORTER_009', TestAction(
        name=("Init of Reporter with empty targets raises "
              "SimpleBenchNotImplementedError/REPORTER_TARGETS_NOT_IMPLEMENTED"),
        action=MockReporterInit,
        exception=SimpleBenchNotImplementedError,
        exception_tag=ErrorTag.REPORTER_TARGETS_NOT_IMPLEMENTED,
        kwargs={
            'name': 'dummy',
            'description': 'A dummy reporter for testing.',
            'sections': {Section.OPS},
            'targets': set(),
            'formats': {Format.RICH_TEXT},
            'choices': MockChoices()})),
    idspec('REPORTER_010', TestAction(
        name=("Init of Reporter with empty formats raises "
              "SimpleBenchNotImplementedError/REPORTER_FORMATS_NOT_IMPLEMENTED"),
        action=MockReporterInit,
        exception=SimpleBenchNotImplementedError,
        exception_tag=ErrorTag.REPORTER_FORMATS_NOT_IMPLEMENTED,
        kwargs={
            'name': 'dummy',
            'description': 'A dummy reporter for testing.',
            'sections': {Section.OPS},
            'targets': {Target.CONSOLE},
            'formats': set(),
            'choices': MockChoices()})),
    idspec('REPORTER_011', TestAction(
        name=("Init of Reporter with missing choices raises "
              "SimpleBenchNotImplementedError/REPORTER_CHOICES_NOT_IMPLEMENTED"),
        action=MockReporterInit,
        exception=SimpleBenchNotImplementedError,
        exception_tag=ErrorTag.REPORTER_CHOICES_NOT_IMPLEMENTED,
        kwargs={
            'name': 'dummy',
            'description': 'A dummy reporter for testing.',
            'sections': {Section.OPS},
            'targets': {Target.CONSOLE},
            'formats': {Format.RICH_TEXT}})),
    idspec('REPORTER_012', TestAction(
        name=("Init of Reporter with choices not a Choices instance raises "
              "SimpleBenchTypeError/REPORTER_INVALID_CHOICES_ARG_TYPE"),
        action=MockReporterInit,
        exception=SimpleBenchTypeError,
        exception_tag=ErrorTag.REPORTER_INVALID_CHOICES_ARG_TYPE,
        kwargs={
            'name': 'dummy',
            'description': 'A dummy reporter for testing.',
            'sections': {Section.OPS},
            'targets': {Target.CONSOLE},
            'formats': {Format.RICH_TEXT},
            'choices': "not_a_choices_instance"})),
    idspec('REPORTER_013', TestAction(
        name=("Init of Reporter with sections containing non-Section enum raises "
              "SimpleBenchTypeError/REPORTER_INVALID_SECTIONS_ENTRY_TYPE"),
        action=MockReporterInit,
        exception=SimpleBenchTypeError,
        exception_tag=ErrorTag.REPORTER_INVALID_SECTIONS_ENTRY_TYPE,
        kwargs={
            'name': 'dummy',
            'description': 'A dummy reporter for testing.',
            'sections': {Section.OPS, "not_a_section_enum"},  # type: ignore[arg-type]
            'targets': {Target.CONSOLE},
            'formats': {Format.RICH_TEXT},
            'choices': MockChoices()})),
    idspec('REPORTER_014', TestAction(
        name=("Init of Reporter with targets containing non-Target enum raises "
              "SimpleBenchTypeError/REPORTER_INVALID_TARGETS_ENTRY_TYPE"),
        action=MockReporterInit,
        exception=SimpleBenchTypeError,
        exception_tag=ErrorTag.REPORTER_INVALID_TARGETS_ENTRY_TYPE,
        kwargs={
            'name': 'dummy',
            'description': 'A dummy reporter for testing.',
            'sections': {Section.OPS},
            'targets': {Target.CONSOLE, "not_a_target_enum"},  # type: ignore[arg-type]
            'formats': {Format.RICH_TEXT},
            'choices': MockChoices()})),
    idspec('REPORTER_015', TestAction(
        name=("Init of Reporter with formats containing non-Format enum raises "
              "SimpleBenchTypeError/REPORTER_INVALID_FORMATS_ENTRY_TYPE"),
        action=MockReporterInit,
        exception=SimpleBenchTypeError,
        exception_tag=ErrorTag.REPORTER_INVALID_FORMATS_ENTRY_TYPE,
        kwargs={
            'name': 'dummy',
            'description': 'A dummy reporter for testing.',
            'sections': {Section.OPS},
            'targets': {Target.CONSOLE},
            'formats': {Format.RICH_TEXT, "not_a_format_enum"},  # type: ignore[arg-type]
            'choices': MockChoices()})),
    idspec('REPORTER_016', TestAction(
        name="Init of Report with empty name raises SimpleBenchValueError/REPORTER_NAME_INVALID_VALUE",
        action=MockReporterInit,
        exception=SimpleBenchValueError,
        exception_tag=ErrorTag.REPORTER_NAME_INVALID_VALUE,
        kwargs={
            'name': '',
            'description': 'A dummy reporter for testing.',
            'sections': {Section.OPS},
            'targets': {Target.CONSOLE},
            'formats': {Format.RICH_TEXT},
            'choices': MockChoices()})),
    idspec('REPORTER_016', TestAction(
        name="Init of Report with empty name raises SimpleBenchValueError/REPORTER_NAME_INVALID_VALUE",
        action=MockReporterInit,
        exception=SimpleBenchValueError,
        exception_tag=ErrorTag.REPORTER_NAME_INVALID_VALUE,
        kwargs={
            'name': '',
            'description': 'A dummy reporter for testing.',
            'sections': {Section.OPS},
            'targets': {Target.CONSOLE},
            'formats': {Format.RICH_TEXT},
            'choices': MockChoices()})),
    idspec('REPORTER_017', TestAction(
        name="Init of Report with empty description raises SimpleBenchValueError/REPORTER_DESCRIPTION_INVALID_VALUE",
        action=MockReporterInit,
        exception=SimpleBenchValueError,
        exception_tag=ErrorTag.REPORTER_DESCRIPTION_INVALID_VALUE,
        kwargs={
            'name': 'dummy',
            'description': '',
            'sections': {Section.OPS},
            'targets': {Target.CONSOLE},
            'formats': {Format.RICH_TEXT},
            'choices': MockChoices()})),
    idspec('REPORTER_018', TestAction(
        name=("Init of Report with no defined Choices raises "
              "SimpleBenchNotImplementedError/REPORTER_CHOICES_NOT_IMPLEMENTED"),
        action=MockReporterInit,
        exception=SimpleBenchNotImplementedError,
        exception_tag=ErrorTag.REPORTER_CHOICES_NOT_IMPLEMENTED,
        kwargs={
            'name': 'dummy',
            'description': 'A dummy reporter for testing.',
            'sections': {Section.OPS},
            'targets': {Target.CONSOLE},
            'formats': {Format.RICH_TEXT},
            'choices': Choices()})),
])
def test_reporter_init(testspec: TestSpec) -> None:
    """Test Reporter init parameters."""
    testspec.run()


@pytest.mark.parametrize('testspec', [
    idspec('REPORT_001', TestAction(
        name="report() with non-Case arg raises SimpleBenchTypeError/REPORTER_REPORT_INVALID_CASE_ARG",
        action=lambda: MockReporter().report(
                        case="not_a_case_instance",  # type: ignore[arg-type]
                        choice=MockChoice()),
        exception=SimpleBenchTypeError,
        exception_tag=ErrorTag.REPORTER_REPORT_INVALID_CASE_ARG)),
    idspec('REPORT_002', TestAction(
        name="report() with non-Choice arg raises SimpleBenchTypeError/REPORTER_REPORT_INVALID_CHOICE_ARG",
        action=lambda: MockReporter().report(
                        case=MockCase(),
                        choice="not_a_choice_instance"),  # type: ignore[arg-type]
        exception=SimpleBenchTypeError,
        exception_tag=ErrorTag.REPORTER_REPORT_INVALID_CHOICE_ARG)),
    idspec('REPORT_003', TestAction(
        name="report() with non-Choice choise arg raises SimpleBenchTypeError/REPORTER_REPORT_INVALID_CHOICE_ARG",
        action=lambda: MockReporter().report(
                        case=MockCase(),
                        choice=Choices()),  # type: ignore[arg-type]
        exception=SimpleBenchTypeError,
        exception_tag=ErrorTag.REPORTER_REPORT_INVALID_CHOICE_ARG)),
    idspec('REPORT_004', TestAction(
        name=("report() with Section not in Reporter's sections raises "
              "SimpleBenchValueError/REPORTER_REPORT_UNSUPPORTED_SECTION"),
        action=lambda: MockReporter().report(
                        case=MockCase(),
                        choice=Choice(
                            reporter=MockReporter(),
                            flags=['--not-registered'],
                            name='not_registered',
                            description='A choice not registered with the reporter.',
                            sections=[Section.NULL],
                            targets=[Target.CONSOLE],
                            formats=[Format.RICH_TEXT],
                            extra=None)),
        exception=SimpleBenchValueError,
        exception_tag=ErrorTag.REPORTER_REPORT_UNSUPPORTED_SECTION)),
    idspec('REPORT_005', TestAction(
        name=("report() with Target not in Reporter's targets raises "
              "SimpleBenchValueError/REPORTER_REPORT_UNSUPPORTED_TARGET"),
        action=lambda: MockReporter().report(
                        case=MockCase(),
                        choice=Choice(
                            reporter=MockReporter(),
                            flags=['--not-registered'],
                            name='not_registered',
                            description='A choice not registered with the reporter.',
                            sections=[Section.OPS],
                            targets=[Target.CUSTOM],
                            formats=[Format.RICH_TEXT],
                            extra=None)),
        exception=SimpleBenchValueError,
        exception_tag=ErrorTag.REPORTER_REPORT_UNSUPPORTED_TARGET)),
    idspec('REPORT_006', TestAction(
        name=("report() with Format not in Reporter's formats raises "
              "SimpleBenchValueError/REPORTER_REPORT_UNSUPPORTED_FORMAT"),
        action=lambda: MockReporter().report(
                        case=MockCase(),
                        choice=Choice(
                            reporter=MockReporter(),
                            flags=['--not-registered'],
                            name='not_registered',
                            description='A choice not registered with the reporter.',
                            sections=[Section.OPS],
                            targets=[Target.CONSOLE],
                            formats=[Format.CUSTOM],
                            extra=None)),
        exception=SimpleBenchValueError,
        exception_tag=ErrorTag.REPORTER_REPORT_UNSUPPORTED_FORMAT)),
    idspec('REPORT_007', TestAction(
        name="report() with valid Case and Choice runs successfully",
        action=lambda: MockReporter().report(
                        case=MockCase(),
                        choice=Choice(
                            reporter=MockReporter(),
                            flags=['--not-registered'],
                            name='not_registered',
                            description='A choice not registered with the reporter.',
                            sections=[Section.OPS],
                            targets=[Target.CONSOLE],
                            formats=[Format.RICH_TEXT],
                            extra=None)),
        validate_result=lambda result: result is None)),
    idspec('REPORT_008', TestAction(
        name="report() with valid callback runs successfully",
        action=lambda: MockReporter().report(
                        case=MockCase(),
                        choice=Choice(
                            reporter=MockReporter(),
                            flags=['--not-registered'],
                            name='not_registered',
                            description='A choice not registered with the reporter.',
                            sections=[Section.OPS],
                            targets=[Target.CALLBACK],
                            formats=[Format.RICH_TEXT],
                            extra=None),
                        callback=mock_callback),
        expected=NO_EXPECTED_VALUE)),
    idspec('REPORT_009', TestAction(
        name=("report() with invalid callback raises SimpleBenchTypeError/REPORTER_REPORT_INVALID_CALLBACK_ARG"),
        action=lambda: MockReporter().report(
            case=MockCase(),
            choice=Choice(
                reporter=MockReporter(),
                flags=['--not-registered'],
                name='not_registered',
                description='A choice not registered with the reporter.',
                sections=[Section.OPS],
                targets=[Target.CALLBACK],
                formats=[Format.RICH_TEXT],
                extra=None),
            callback="not_a_callback"),  # type: ignore[arg-type]
        exception=SimpleBenchTypeError,
        exception_tag=ErrorTag.REPORTER_REPORT_INVALID_CALLBACK_ARG)),
    idspec('REPORT_010', TestAction(
        name="report() with valid path runs successfully",
        action=lambda: MockReporter().report(
                        case=MockCase(),
                        choice=Choice(
                            reporter=MockReporter(),
                            flags=['--not-registered'],
                            name='not_registered',
                            description='A choice not registered with the reporter.',
                            sections=[Section.OPS],
                            targets=[Target.FILESYSTEM],
                            formats=[Format.RICH_TEXT],
                            extra=None),
                        path=mock_path()),
        expected=NO_EXPECTED_VALUE)),  # pragma: no cover (path not actually used)
    idspec('REPORT_011', TestAction(
        name=("report() with invalid path raises SimpleBenchTypeError/REPORTER_REPORT_INVALID_PATH_ARG"),
        action=lambda: MockReporter().report(
            case=MockCase(),
            choice=Choice(
                reporter=MockReporter(),
                flags=['--not-registered'],  # type: ignore[arg-type]
                name='not_registered',
                description='A choice not registered with the reporter.',
                sections=[Section.OPS],
                targets=[Target.FILESYSTEM],
                formats=[Format.RICH_TEXT],
                extra=None),
            path="not_a_path"),  # type: ignore[arg-type]
        exception=SimpleBenchTypeError,
        exception_tag=ErrorTag.REPORTER_REPORT_INVALID_PATH_ARG)),
    idspec('REPORT_012', TestAction(
        name=("report() with valid session runs successfully"),
        action=lambda: MockReporter().report(
                        case=MockCase(),
                        choice=Choice(
                            reporter=MockReporter(),
                            flags=['--not-registered'],
                            name='not_registered',
                            description='A choice not registered with the reporter.',
                            sections=[Section.OPS],
                            targets=[Target.CONSOLE],
                            formats=[Format.RICH_TEXT],
                            extra=None),
                        session=MockSession()),
        expected=NO_EXPECTED_VALUE)),  # pragma: no cover (session not actually used),
    idspec('REPORT_013', TestAction(
        name=("report() with invalid session raises SimpleBenchTypeError/REPORTER_REPORT_INVALID_SESSION_ARG"),
        action=lambda: MockReporter().report(
            case=MockCase(),
            choice=Choice(
                reporter=MockReporter(),
                flags=['--not-registered'],
                name='not_registered',
                description='A choice not registered with the reporter.',
                sections=[Section.OPS],
                targets=[Target.CONSOLE],
                formats=[Format.RICH_TEXT],
                extra=None),
            session="not_a_session"),  # type: ignore[arg-type]
        exception=SimpleBenchTypeError,
        exception_tag=ErrorTag.REPORTER_REPORT_INVALID_SESSION_ARG)),
])
def test_reporter_report(testspec: TestSpec) -> None:
    """Test Reporter.report() method."""
    testspec.run()


@pytest.mark.parametrize('testspec', [
    idspec('REPORTER_ADD_CHOICE_001', TestAction(
        name="Adding a valid Choice to a Reporter works",
        action=lambda: MockReporter().add_choice(choice=MockChoice(name='dummy2', flags=['--dummy2'])),
        expected=NO_EXPECTED_VALUE)),
    idspec('REPORTER_ADD_CHOICE_002', TestAction(
        name=("Passing wrong type object to add_choice() raises "
              "SimpleBenchTypeError/REPORTER_ADD_CHOICE_INVALID_CHOICE_ARG"),
        action=lambda: MockReporter().add_choice(choice="not_a_choice_instance"),  # type: ignore[arg-type]
        exception=SimpleBenchTypeError,
        exception_tag=ErrorTag.REPORTER_ADD_CHOICE_INVALID_ARG_TYPE)),
    idspec('REPORTER_ADD_CHOICE_003', TestAction(
        name=("Passing Choice with a section not supported by the Reporter to add_choice() raises "
              "SimpleBenchTypeError/REPORTER_ADD_CHOICE_INVALID_SECTION_ARG"),
        action=lambda: MockReporter().add_choice(
            choice=MockChoice(name='dummy2', flags=['--dummy2'], sections=[Section.NULL])),
        exception=SimpleBenchValueError,
        exception_tag=ErrorTag.REPORTER_ADD_CHOICE_UNSUPPORTED_SECTION)),
    idspec('REPORTER_ADD_CHOICE_004', TestAction(
        name=("Passing Choice with a target not supported by the Reporter to add_choice() raises "
              "SimpleBenchTypeError/REPORTER_ADD_CHOICE_INVALID_TARGET_ARG"),
        action=lambda: MockReporter().add_choice(
            choice=MockChoice(name='dummy2', flags=['--dummy2'], targets=[Target.CUSTOM])),
        exception=SimpleBenchValueError,
        exception_tag=ErrorTag.REPORTER_ADD_CHOICE_UNSUPPORTED_TARGET)),
    idspec('REPORTER_ADD_CHOICE_005', TestAction(
        name=("Passing Choice with a format not supported by the Reporter to add_choice() raises "
              "SimpleBenchTypeError/REPORTER_ADD_CHOICE_INVALID_FORMAT_ARG"),
        action=lambda: MockReporter().add_choice(
            choice=MockChoice(name='dummy2', flags=['--dummy2'], formats=[Format.CUSTOM])),
        exception=SimpleBenchValueError,
        exception_tag=ErrorTag.REPORTER_ADD_CHOICE_UNSUPPORTED_FORMAT)),
])
def test_add_choice(testspec: TestSpec) -> None:
    """Test Reporter.add_choice() method."""
    testspec.run()


class MockReporterForChoices(MockReporterInit):
    """A dummy Reporter subclass for testing add_flags_to_argparse()."""
    def __init__(self, *, choices: Choices) -> None:
        super().__init__(
            name='dummy',
            description='A dummy reporter for testing.',
            sections={Section.OPS},
            targets={Target.CONSOLE},
            formats={Format.RICH_TEXT},
            choices=choices)


@pytest.mark.parametrize('testspec', [
    idspec('REPORTER_ADD_FLAGS_001', TestAction(
        name="Adding a valid flag to an ArgumentParser",
        action=lambda: MockReporterForChoices(
            choices=Choices(choices=[MockChoice()])).add_flags_to_argparse(ArgumentParser()),
        expected=NO_EXPECTED_VALUE)),
    idspec('REPORTER_ADD_FLAGS_002', TestAction(
        name=("Passing a non-ArgumentParser to add_flags_to_argparse raises "
              "SimpleBenchTypeError/REPORTER_ADD_FLAGS_INVALID_PARSER_ARG"),
        action=lambda: MockReporterForChoices(
            choices=Choices(choices=[
                MockChoice(),
            ])).add_flags_to_argparse("not_an_argument_parser"),  # type: ignore[arg-type]
        exception=SimpleBenchTypeError,
        exception_tag=ErrorTag.REPORTER_ADD_FLAGS_INVALID_PARSER_ARG_TYPE)),
])
def test_reporter_add_flags_to_argparse(testspec: TestSpec) -> None:
    """Test Reporter.add_flags_to_argparse() method."""
    testspec.run()


def test_attributes() -> None:
    """Test Reporter attributes.

    Verify that Reporter attributes are correctly set and immutable.
    """
    reporter: MockReporter = MockReporter()
    assert reporter.name == 'dummy', "Failed to get Reporter.name"
    assert reporter.description == 'A dummy reporter for testing.', "Failed to get Reporter.description"
    choices = reporter.choices
    assert isinstance(choices, Choices), "Failed to get Reporter.choices"
    with pytest.raises(AttributeError):
        reporter.name = "new_name"  # type: ignore[assignment, misc]
    with pytest.raises(AttributeError):
        reporter.description = "new_description"  # type: ignore[assignment, misc]
    with pytest.raises(AttributeError):
        reporter.choices = Choices(choices=[MockChoice()])  # type: ignore[assignment, misc]
