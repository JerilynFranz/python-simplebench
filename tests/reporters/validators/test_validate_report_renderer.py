"""Test the simplebench.reporters.validators.validate_report_renderer function."""
from argparse import Namespace
from pathlib import Path
from typing import Any, ClassVar, TypeVar

import pytest
from rich.table import Table
from rich.text import Text

from simplebench.case import Case
from simplebench.enums import Section
from simplebench.exceptions import SimpleBenchTypeError
from simplebench.reporters.choice import Choice
from simplebench.reporters.protocols import ReporterCallback
from simplebench.reporters.reporter import Reporter
from simplebench.reporters.reporter.options import ReporterOptions
from simplebench.reporters.validators import validate_report_renderer
from simplebench.reporters.validators.exceptions import ReportersValidatorsErrorTag
from simplebench.session import Session

from ...factories import reporter_kwargs_factory
from ...testspec import Assert, TestAction, TestSpec, idspec

T = TypeVar('T')


class MockReporterOptions(ReporterOptions):
    """A mock ReporterOptions subclass for testing purposes."""


class MockReporter(Reporter):
    """A mock reporter subclass for testing purposes."""

    _OPTIONS_TYPE: ClassVar[type[MockReporterOptions]] = MockReporterOptions  # pylint: disable=line-too-long  # type: ignore[reportIncompatibleVariableOveride]  # noqa: E501
    """The specific ReporterOptions subclass associated with this reporter."""
    _OPTIONS_KWARGS: ClassVar[dict[str, Any]] = {}
    """The default keyword arguments for the MockReporterOptions subclass."""

    def __init__(self):
        super().__init__(**reporter_kwargs_factory(cache_id=None))

    def run_report(self,
                   *,
                   args: Namespace,
                   case: Case,
                   choice: Choice,
                   path: Path | None = None,
                   session: Session | None = None,
                   callback: ReporterCallback | None = None) -> None:
        """A mock run_report method.

        :param args: The command-line arguments.
        :type args: Namespace
        :param case: The benchmark case.
        :type case: Case
        :param choice: The reporter choice.
        :type choice: Choice
        :param path: The output path.
        :type path: Path | None
        :param session: The benchmark session.
        :type session: Session | None
        :param callback: The reporter callback.
        :type callback: ReporterCallback | None
        """
        self.render_by_section(  # pragma: no cover
            renderer=self.render, args=args, case=case, choice=choice, path=path, session=session, callback=callback)

    def render(
            self, *, case: Case, section: Section, options: ReporterOptions) -> str:  # pylint: disable=unused-argument  # noqa: E501
        """A mock render method.

        :param case: The benchmark case.
        :type case: Case
        :param section: The report section.
        :type section: Section
        :param options: The reporter options.
        :type options: ReporterOptions
        :return: A mock report.
        :rtype: str
        """
        return "Mock Report"  # pragma: no cover

    def invalid_render_no_options(
            self, *, case: Case, section: Section) -> str:  # pylint: disable=unused-argument
        """An invalid render method for testing purposes.

        :param case: The benchmark case.
        :type case: Case
        :param section: The report section.
        :type section: Section
        :return: An error message.
        :rtype: str
        """
        return "Invalid Mock Report render method that is missing options parameter"  # pragma: no cover

    def invalid_render_options_wrong_type(
            self, *, case: Case, section: Section, options: str) -> str:  # pylint: disable=unused-argument  # noqa: E501
        """An invalid render method for testing purposes.

        :param case: The benchmark case.
        :type case: Case
        :param section: The report section.
        :type section: Section
        :param options: The reporter options.
        :type options: str
        :return: An error message.
        :rtype: str
        """
        return "Invalid Mock Report render method that has options parameter of wrong type"  # pragma: no cover

    def invalid_render_options_missing_type_hint(
            self, *, case: Case, section: Section, options) -> str:  # pylint: disable=unused-argument  # noqa: E501
        """An invalid render method for testing purposes.

        :param case: The benchmark case.
        :type case: Case
        :param section: The report section.
        :type section: Section
        :param options: The reporter options.
        :return: An error message.
        :rtype: str
        """
        return "Invalid Mock Report render method that has options parameter missing type hint"  # pragma: no cover

    def invalid_render_no_section(
            self, *, case: Case, options: ReporterOptions) -> str:  # pylint: disable=unused-argument  # noqa: E501
        """An invalid render method for testing purposes.

        :param case: The benchmark case.
        :type case: Case
        :param options: The reporter options.
        :type options: ReporterOptions
        :return: An error message.
        :rtype: str
        """
        return "Invalid Mock Report render method that is missing section parameter"  # pragma: no cover

    def invalid_render_section_wrong_type(
            self, *, case: Case, section: str, options: ReporterOptions) -> str:  # pylint: disable=unused-argument,line-too-long  # noqa: E501
        """An invalid render method for testing purposes.

        :param case: The benchmark case.
        :type case: Case
        :param section: The report section.
        :type section: str
        :param options: The reporter options.
        :type options: ReporterOptions
        :return: An error message.
        :rtype: str
        """
        return "Invalid Mock Report render method that has section parameter of wrong type"  # pragma: no cover

    def invalid_render_section_missing_type_hint(
            self, *, case: Case, section, options: ReporterOptions) -> str:  # pylint: disable=unused-argument,line-too-long  # noqa: E501
        """An invalid render method for testing purposes.

        :param case: The benchmark case.
        :type case: Case
        :param section: The report section.
        :param options: The reporter options.
        :type options: ReporterOptions
        :return: An error message.
        :rtype: str
        """
        return "Invalid Mock Report render method that has section parameter missing type hint"  # pragma: no cover

    def invalid_render_no_case(
            self, *, section: Section, options: ReporterOptions) -> str:  # pylint: disable=unused-argument  # noqa: E501
        """An invalid render method for testing purposes.

        :param section: The report section.
        :type section: Section
        :param options: The reporter options.
        :type options: ReporterOptions
        :return: An error message.
        :rtype: str
        """
        return "Invalid Mock Report render method that is missing case parameter"  # pragma: no cover

    def invalid_render_case_wrong_type(
            self, *, case: str, section: Section, options: ReporterOptions) -> str:  # pylint: disable=unused-argument,line-too-long  # noqa: E501
        """An invalid render method for testing purposes.

        :param case: The benchmark case.
        :type case: str
        :param section: The report section.
        :type section: Section
        :param options: The reporter options.
        :type options: ReporterOptions
        :return: An error message.
        :rtype: str
        """
        return "Invalid Mock Report render method that has case parameter of wrong type"  # pragma: no cover

    def invalid_render_case_missing_type_hint(
            self, *, case, section: Section, options: ReporterOptions) -> str:  # pylint: disable=unused-argument,line-too-long  # noqa: E501
        """An invalid render method for testing purposes.

        :param case: The benchmark case.
        :param section: The report section.
        :type section: Section
        :param options: The reporter options.
        :type options: ReporterOptions
        :return: An error message.
        :rtype: str
        """
        return "Invalid Mock Report render method that has case parameter missing type hint"  # pragma: no cover

    def invalid_render_extra_parameter(
            self, *, case: Case, section: Section, options: ReporterOptions, extra: str) -> str:  # pylint: disable=unused-argument # noqa: E501
        """An invalid render method for testing purposes.

        :param case: The benchmark case.
        :type case: Case
        :param section: The report section.
        :type section: Section
        :param options: The reporter options.
        :type options: ReporterOptions
        :param extra: An extra parameter.
        :type extra: str
        :return: An error message.
        :rtype: str
        """
        return "Invalid Mock Report render method that has an extra parameter"  # pragma: no cover

    def invalid_render_not_keyword_only(
            self, case: Case, section: Section, options: ReporterOptions) -> str:  # pylint: disable=unused-argument
        """An invalid render method for testing purposes.

        :param case: The benchmark case.
        :type case: Case
        :param section: The report section.
        :type section: Section
        :param options: The reporter options.
        :type options: ReporterOptions
        :return: An error message.
        :rtype: str
        """
        return "Invalid Mock Report render method that has non-keyword-only parameters"  # pragma: no cover

    def invalid_render_wrong_return_type(  # pylint: disable=unused-argument
            self, *,
            case: Case,
            section: Section,
            options: ReporterOptions) -> tuple[int, float]:
        """An invalid render method for testing purposes.

        :param case: The benchmark case.
        :type case: Case
        :param section: The report section.
        :type section: Section
        :param options: The reporter options.
        :type options: ReporterOptions
        :return: An invalid return type.
        :rtype: tuple[int, float]
        """
        return (42, 3.14)  # Invalid return type (should be str, bytes, Text, or Table) # pragma: no cover

    def invalid_render_missing_return_type(  # pylint: disable=unused-argument
            self, *,
            case: Case,
            section: Section,
            options: ReporterOptions):
        """An invalid render method for testing purposes.

        :param case: The benchmark case.
        :type case: Case
        :param section: The report section.
        :type section: Section
        :param options: The reporter options.
        :type options: ReporterOptions
        """
        return "Invalid Mock Report render method that is missing return type annotation"  # pragma: no cover

    def valid_render_with_all_possible_return_types(  # pylint: disable=unused-argument
            self, *,
            case: Case,
            section: Section,
            options: ReporterOptions) -> bytes | str | Text | Table:
        """A valid render method that declares all allowed return types.

        :param case: The benchmark case.
        :type case: Case
        :param section: The report section.
        :type section: Section
        :param options: The reporter options.
        :type options: ReporterOptions
        :return: A valid return type.
        :rtype: bytes | str | Text | Table
        """
        return b"Valid Mock Report render method returning bytes"  # pragma: no cover

    def invalid_render_with_extra_return_type(  # pylint: disable=unused-argument
            self, *,
            case: Case,
            section: Section,
            options: ReporterOptions) -> str | int:
        """An invalid render method that declares an extra disallowed return type.

        :param case: The benchmark case.
        :type case: Case
        :param section: The report section.
        :type section: Section
        :param options: The reporter options.
        :type options: ReporterOptions
        :return: An invalid return type.
        :rtype: str | int
        """
        return "Invalid Mock Report render method returning str and int"  # pragma: no cover

    def invalid_render_with_unexpected_return_type(  # pylint: disable=unused-argument
            self, *,
            case: Case,
            section: Section,
            options: ReporterOptions) -> float:
        """An invalid render method that declares an unexpected return type.

        :param case: The benchmark case.
        :type case: Case
        :param section: The report section.
        :type section: Section
        :param options: The reporter options.
        :type options: ReporterOptions
        :return: An invalid return type.
        :rtype: float
        """
        return 3.14  # pragma: no cover

    def invalid_render_with_any_return_type(  # pylint: disable=unused-argument
            self, *,
            case: Case,
            section: Section,
            options: ReporterOptions) -> Any:
        """An invalid render method that declares an unexpected return type.

        :param case: The benchmark case.
        :type case: Case
        :param section: The report section.
        :type section: Section
        :param options: The reporter options.
        :type options: ReporterOptions
        :return: An invalid return type.
        :rtype: Any
        """
        return 3.14  # pragma: no cover

    def invalid_render_with_none_return_type(  # pylint: disable=unused-argument
            self, *,
            case: Case,
            section: Section,
            options: ReporterOptions) -> None:
        """An invalid render method that declares a None return type.

        :param case: The benchmark case.
        :type case: Case
        :param section: The report section.
        :type section: Section
        :param options: The reporter options.
        :type options: ReporterOptions
        """
        return None  # pragma: no cover

    def invalid_render_with_union_including_none(  # pylint: disable=unused-argument
            self, *,
            case: Case,
            section: Section,
            options: ReporterOptions) -> str | None:
        """An invalid render method that declares a union with None.

        :param case: The benchmark case.
        :type case: Case
        :param section: The report section.
        :type section: Section
        :param options: The reporter options.
        :type options: ReporterOptions
        :return: An invalid return type.
        :rtype: str | None
        """
        return "Invalid"  # pragma: no cover

    def invalid_render_with_typevar_return_type(  # pylint: disable=unused-argument
            self, *,
            case: Case,
            section: Section,
            options: ReporterOptions) -> T:  # type: ignore[reportInvalidTypeVarUse, type-var]
        """An invalid render method that declares a TypeVar return type.

        :param case: The benchmark case.
        :type case: Case
        :param section: The report section.
        :type section: Section
        :param options: The reporter options.
        :type options: ReporterOptions
        :return: An invalid return type.
        :rtype: T
        """
        return "Invalid"  # type: ignore[return-value]  # pragma: no cover

    def valid_render_with_forward_ref(  # pylint: disable=unused-argument
            self, *,
            case: Case,
            section: Section,
            options: ReporterOptions) -> 'str':
        """A valid render method that uses a forward reference string.

        :param case: The benchmark case.
        :type case: Case
        :param section: The report section.
        :type section: Section
        :param options: The reporter options.
        :type options: ReporterOptions
        :return: A valid return type.
        :rtype: 'str'
        """
        return "Valid"  # pragma: no cover


MOCK_REPORTER_INSTANCE = MockReporter()


valid_render_with_all_possible_return_types = MOCK_REPORTER_INSTANCE.valid_render_with_all_possible_return_types
invalid_render_with_extra_return_type = MOCK_REPORTER_INSTANCE.invalid_render_with_extra_return_type
invalid_render_with_unexpected_return_type = MOCK_REPORTER_INSTANCE.invalid_render_with_unexpected_return_type
invalid_render_with_any_return_type = MOCK_REPORTER_INSTANCE.invalid_render_with_any_return_type
invalid_render_with_none_return_type = MOCK_REPORTER_INSTANCE.invalid_render_with_none_return_type
invalid_render_with_union_including_none = MOCK_REPORTER_INSTANCE.invalid_render_with_union_including_none
invalid_render_with_typevar_return_type = MOCK_REPORTER_INSTANCE.invalid_render_with_typevar_return_type
valid_render_with_forward_ref = MOCK_REPORTER_INSTANCE.valid_render_with_forward_ref


@pytest.mark.parametrize(
    "testspec", [
        idspec("PROTOCOL_001", TestAction(
            name="valid report renderer",
            action=validate_report_renderer, args=[MOCK_REPORTER_INSTANCE.render],
            assertion=Assert.EQUAL, expected=MOCK_REPORTER_INSTANCE.render
        )),
        idspec("PROTOCOL_002", TestAction(
            name="invalid report renderer missing options parameter",
            action=validate_report_renderer, args=[MockReporter().invalid_render_no_options],
            exception=SimpleBenchTypeError,
            exception_tag=ReportersValidatorsErrorTag.INVALID_CALL_INCORRECT_SIGNATURE_MISSING_PARAMETER
        )),
        idspec("PROTOCOL_003", TestAction(
            name="invalid report renderer options parameter wrong type",
            action=validate_report_renderer, args=[MockReporter().invalid_render_options_wrong_type],
            exception=SimpleBenchTypeError,
            exception_tag=ReportersValidatorsErrorTag.INVALID_CALL_INCORRECT_SIGNATURE_PARAMETER_TYPE
        )),
        idspec("PROTOCOL_004", TestAction(
            name="invalid report renderer options parameter missing type hint",
            action=validate_report_renderer, args=[MockReporter().invalid_render_options_missing_type_hint],
            exception=SimpleBenchTypeError,
            exception_tag=ReportersValidatorsErrorTag.INVALID_CALL_INCORRECT_SIGNATURE_MISSING_PARAMETER_TYPE_HINT
        )),
        idspec("PROTOCOL_005", TestAction(
            name="invalid report renderer missing section parameter",
            action=validate_report_renderer, args=[MockReporter().invalid_render_no_section],
            exception=SimpleBenchTypeError,
            exception_tag=ReportersValidatorsErrorTag.INVALID_CALL_INCORRECT_SIGNATURE_MISSING_PARAMETER
        )),
        idspec("PROTOCOL_006", TestAction(
            name="invalid report renderer section parameter wrong type",
            action=validate_report_renderer, args=[MockReporter().invalid_render_section_wrong_type],
            exception=SimpleBenchTypeError,
            exception_tag=ReportersValidatorsErrorTag.INVALID_CALL_INCORRECT_SIGNATURE_PARAMETER_TYPE
        )),
        idspec("PROTOCOL_007", TestAction(
            name="invalid report renderer section parameter missing type hint",
            action=validate_report_renderer, args=[MockReporter().invalid_render_section_missing_type_hint],
            exception=SimpleBenchTypeError,
            exception_tag=ReportersValidatorsErrorTag.INVALID_CALL_INCORRECT_SIGNATURE_MISSING_PARAMETER_TYPE_HINT
        )),
        idspec("PROTOCOL_008", TestAction(
            name="invalid report renderer missing case parameter",
            action=validate_report_renderer, args=[MockReporter().invalid_render_no_case],
            exception=SimpleBenchTypeError,
            exception_tag=ReportersValidatorsErrorTag.INVALID_CALL_INCORRECT_SIGNATURE_MISSING_PARAMETER
        )),
        idspec("PROTOCOL_009", TestAction(
            name="invalid report renderer case parameter wrong type",
            action=validate_report_renderer, args=[MockReporter().invalid_render_case_wrong_type],
            exception=SimpleBenchTypeError,
            exception_tag=ReportersValidatorsErrorTag.INVALID_CALL_INCORRECT_SIGNATURE_PARAMETER_TYPE
        )),
        idspec("PROTOCOL_010", TestAction(
            name="invalid report renderer case parameter missing type hint",
            action=validate_report_renderer, args=[MockReporter().invalid_render_case_missing_type_hint],
            exception=SimpleBenchTypeError,
            exception_tag=ReportersValidatorsErrorTag.INVALID_CALL_INCORRECT_SIGNATURE_MISSING_PARAMETER_TYPE_HINT
        )),
        idspec("PROTOCOL_011", TestAction(
            name="invalid report renderer with extra parameter",
            action=validate_report_renderer, args=[MockReporter().invalid_render_extra_parameter],
            exception=SimpleBenchTypeError,
            exception_tag=ReportersValidatorsErrorTag.REPORT_RENDERER_INCORRECT_NUMBER_OF_PARAMETERS
        )),
        idspec("PROTOCOL_012", TestAction(
            name="invalid report renderer with non-keyword-only parameters",
            action=validate_report_renderer, args=[MockReporter().invalid_render_not_keyword_only],
            exception=SimpleBenchTypeError,
            exception_tag=ReportersValidatorsErrorTag.INVALID_CALL_INCORRECT_SIGNATURE_PARAMETER_NOT_KEYWORD_ONLY
        )),
        idspec("PROTOCOL_013", TestAction(
            name="invalid report renderer not callable",
            action=validate_report_renderer, args=["not_a_callable"],
            exception=SimpleBenchTypeError,
            exception_tag=ReportersValidatorsErrorTag.REPORT_RENDERER_NOT_CALLABLE
        )),
        idspec("PROTOCOL_014", TestAction(
            name="invalid report renderer with incorrect return type",
            action=validate_report_renderer, args=[MockReporter().invalid_render_wrong_return_type],
            exception=SimpleBenchTypeError,
            exception_tag=ReportersValidatorsErrorTag.REPORT_RENDERER_UNEXPECTED_RETURN_ANNOTATION_TYPE
        )),
        idspec("PROTOCOL_015", TestAction(
            name="invalid report renderer missing return type annotation",
            action=validate_report_renderer, args=[MockReporter().invalid_render_missing_return_type],
            exception=SimpleBenchTypeError,
            exception_tag=ReportersValidatorsErrorTag.REPORT_RENDERER_MISSING_RETURN_ANNOTATION
        )),
        idspec("PROTOCOL_016", TestAction(
            name="valid report renderer with all possible return types",
            action=validate_report_renderer, args=[valid_render_with_all_possible_return_types],
            assertion=Assert.EQUAL, expected=valid_render_with_all_possible_return_types
        )),
        idspec("PROTOCOL_017", TestAction(
            name="invalid report renderer with extra return type",
            action=validate_report_renderer, args=[invalid_render_with_extra_return_type],
            exception=SimpleBenchTypeError,
            exception_tag=ReportersValidatorsErrorTag.REPORT_RENDERER_INCORRECT_RETURN_ANNOTATION_TYPE
        )),
        idspec("PROTOCOL_018", TestAction(
            name="invalid report renderer with unexpected return type",
            action=validate_report_renderer, args=[invalid_render_with_unexpected_return_type],
            exception=SimpleBenchTypeError,
            exception_tag=ReportersValidatorsErrorTag.REPORT_RENDERER_UNEXPECTED_RETURN_ANNOTATION_TYPE
        )),
        idspec("PROTOCOL_019", TestAction(
            name="invalid report renderer with Any return type",
            action=validate_report_renderer, args=[invalid_render_with_any_return_type],
            exception=SimpleBenchTypeError,
            exception_tag=ReportersValidatorsErrorTag.REPORT_RENDERER_UNEXPECTED_RETURN_ANNOTATION_TYPE
        )),

        idspec("PROTOCOL_020", TestAction(
            name="invalid report renderer with None return type",
            action=validate_report_renderer, args=[invalid_render_with_none_return_type],
            exception=SimpleBenchTypeError,
            exception_tag=ReportersValidatorsErrorTag.REPORT_RENDERER_UNEXPECTED_RETURN_ANNOTATION_TYPE
        )),
        idspec("PROTOCOL_021", TestAction(
            name="invalid report renderer with union including None",
            action=validate_report_renderer, args=[invalid_render_with_union_including_none],
            exception=SimpleBenchTypeError,
            exception_tag=ReportersValidatorsErrorTag.REPORT_RENDERER_INCORRECT_RETURN_ANNOTATION_TYPE
        )),
        idspec("PROTOCOL_022", TestAction(
            name="invalid report renderer with TypeVar return type",
            action=validate_report_renderer, args=[invalid_render_with_typevar_return_type],
            exception=SimpleBenchTypeError,
            exception_tag=ReportersValidatorsErrorTag.REPORT_RENDERER_UNEXPECTED_RETURN_ANNOTATION_TYPE
        )),
        idspec("PROTOCOL_023", TestAction(
            name="valid report renderer with forward reference return type",
            action=validate_report_renderer, args=[valid_render_with_forward_ref],
            assertion=Assert.EQUAL, expected=valid_render_with_forward_ref
        )),
    ])
def test_validate_report_renderer_valid(testspec: TestSpec) -> None:
    """Test validate_report_renderer with valid and invalid report renderers.

    :param testspec: The test specification.
    :type testspec: TestSpec
    """
    testspec.run()
