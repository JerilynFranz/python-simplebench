"""Test the simplebench.reporters.validators.validate_report_renderer function."""
from argparse import Namespace
from pathlib import Path

import pytest

from tests.testspec import TestSpec, TestAction, idspec, Assert

from simplebench.case import Case
from simplebench.enums import Section, Target, Format, FlagType
from simplebench.exceptions import SimpleBenchTypeError
from simplebench.reporters.protocols import ReporterCallback
from simplebench.reporters.reporter import Reporter
from simplebench.reporters.reporter.options import ReporterOptions
from simplebench.reporters.validators.exceptions import ReportersValidatorsErrorTag
from simplebench.reporters.validators.validators import validate_report_renderer
from simplebench.reporters.choice import Choice
from simplebench.reporters.choices import Choices
from simplebench.session import Session


class MockReporterOptions(ReporterOptions):
    """A mock ReporterOptions subclass for testing purposes."""


class MockReporter(Reporter):
    """A mock reporter subclass for testing purposes."""
    def __init__(self):
        super().__init__(
            name='json',
            description='Outputs benchmark results to mock renderer.',
            options_type=MockReporterOptions,
            sections={Section.NULL},
            targets={Target.FILESYSTEM, Target.CALLBACK, Target.CONSOLE},
            formats={Format.JSON},
            choices=Choices([
                Choice(
                    reporter=self,
                    flags=['--mock-options'],
                    flag_type=FlagType.TARGET_LIST,
                    name='mock-options',
                    description='statistical results to JSON (filesystem, console, callback, default=filesystem)',
                    sections=[Section.NULL],  # All sections are always included
                    targets=[Target.FILESYSTEM, Target.CALLBACK, Target.CONSOLE],
                    output_format=Format.RICH_TEXT,
                    options=MockReporterOptions()),
            ]),
            file_suffix='mock',
            file_unique=True,
            file_append=False
        )

    def run_report(self,
                   *,
                   args: Namespace,
                   case: Case,
                   choice: Choice,
                   path: Path | None = None,
                   session: Session | None = None,
                   callback: ReporterCallback | None = None) -> None:
        """A mock run_report method."""
        self.render_by_section(  # pragma: no cover
            renderer=self.render, args=args, case=case, choice=choice, path=path, session=session, callback=callback)

    def render(self, *, case: Case, section: Section, options: ReporterOptions) -> str:  # pylint: disable=unused-argument  # noqa: E501
        """A mock render method."""
        return "Mock Report"  # pragma: no cover

    def invalid_render_no_options(self, *, case: Case, section: Section) -> str:  # pylint: disable=unused-argument
        """An invalid render method for testing purposes."""
        return "Invalid Mock Report render method that is missing options parameter"  # pragma: no cover

    def invalid_render_no_section(self, *, case: Case, options: ReporterOptions) -> str:  # pylint: disable=unused-argument  # noqa: E501
        """An invalid render method for testing purposes."""
        return "Invalid Mock Report render method that is missing section parameter"  # pragma: no cover

    def invalid_render_no_case(self, *, section: Section, options: ReporterOptions) -> str:  # pylint: disable=unused-argument  # noqa: E501
        """An invalid render method for testing purposes."""
        return "Invalid Mock Report render method that is missing case parameter"  # pragma: no cover

    def invalid_render_extra_parameter(
            self, *, case: Case, section: Section, options: ReporterOptions, extra: str) -> str:  # pylint: disable=unused-argument # noqa: E501
        """An invalid render method for testing purposes."""
        return "Invalid Mock Report render method that has an extra parameter"  # pragma: no cover

    def invalid_render_not_keyword_only(
            self, case: Case, section: Section, options: ReporterOptions) -> str:  # pylint: disable=unused-argument
        """An invalid render method for testing purposes."""
        return "Invalid Mock Report render method that has non-keyword-only parameters"  # pragma: no cover

    def invalid_render_wrong_return_type(
            self, *, case: Case, section: Section, options: ReporterOptions) -> int:  # pylint: disable=unused-argument
        """An invalid render method for testing purposes."""
        return 42  # Invalid return type (should be str) # pragma: no cover


MOCK_REPORTER_INSTANCE = MockReporter()


@pytest.mark.parametrize(
    "testspec", [
        idspec("PROTOCOL_001", TestAction(
            name="valid report renderer",
            action=validate_report_renderer,
            args=[MOCK_REPORTER_INSTANCE.render],
            assertion=Assert.EQUAL,
            expected=MOCK_REPORTER_INSTANCE.render
        )),
        idspec("PROTOCOL_002", TestAction(
            name="invalid report renderer missing options parameter",
            action=validate_report_renderer,
            args=[MockReporter().invalid_render_no_options],
            exception=SimpleBenchTypeError,
            exception_tag=ReportersValidatorsErrorTag.INVALID_CALL_INCORRECT_SIGNATURE_MISSING_PARAMETER
        )),
        idspec("PROTOCOL_003", TestAction(
            name="invalid report renderer missing section parameter",
            action=validate_report_renderer,
            args=[MockReporter().invalid_render_no_section],
            exception=SimpleBenchTypeError,
            exception_tag=ReportersValidatorsErrorTag.INVALID_CALL_INCORRECT_SIGNATURE_MISSING_PARAMETER
        )),
        idspec("PROTOCOL_004", TestAction(
            name="invalid report renderer missing case parameter",
            action=validate_report_renderer,
            args=[MockReporter().invalid_render_no_case],
            exception=SimpleBenchTypeError,
            exception_tag=ReportersValidatorsErrorTag.INVALID_CALL_INCORRECT_SIGNATURE_MISSING_PARAMETER
        )),
        idspec("PROTOCOL_005", TestAction(
            name="invalid report renderer with extra parameter",
            action=validate_report_renderer,
            args=[MockReporter().invalid_render_extra_parameter],
            exception=SimpleBenchTypeError,
            exception_tag=ReportersValidatorsErrorTag.REPORT_RENDERER_INCORRECT_NUMBER_OF_PARAMETERS
        )),
        idspec("PROTOCOL_006", TestAction(
            name="invalid report renderer with non-keyword-only parameters",
            action=validate_report_renderer,
            args=[MockReporter().invalid_render_not_keyword_only],
            exception=SimpleBenchTypeError,
            exception_tag=ReportersValidatorsErrorTag.INVALID_CALL_INCORRECT_SIGNATURE_PARAMETER_NOT_KEYWORD_ONLY
        )),
        idspec("PROTOCOL_007", TestAction(
            name="invalid report renderer not callable",
            action=validate_report_renderer,
            args=["not_a_callable"],
            exception=SimpleBenchTypeError,
            exception_tag=ReportersValidatorsErrorTag.REPORT_RENDERER_NOT_CALLABLE
        )),
        idspec("PROTOCOL_008", TestAction(
            name="invalid report renderer with incorrect return type",
            action=validate_report_renderer,
            args=[MockReporter().invalid_render_wrong_return_type],
            exception=SimpleBenchTypeError,
            exception_tag=ReportersValidatorsErrorTag.REPORT_RENDERER_INCORRECT_RETURN_ANNOTATION_TYPE
        )),
    ])
def test_validate_report_renderer_valid(testspec: TestSpec) -> None:
    """Test validate_report_renderer with valid and invalid report renderers."""
    testspec.run()
