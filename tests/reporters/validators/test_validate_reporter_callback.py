"""Tests for :func:`~simplebench.reporters.validators.validate_reporter_callback`."""
from __future__ import annotations

from typing import Any

import pytest

from simplebench.case import Case
from simplebench.enums import Format, Section
from simplebench.exceptions import SimpleBenchTypeError
from simplebench.reporters.protocols import ReporterCallback
from simplebench.reporters.validators import validate_reporter_callback
from simplebench.reporters.validators.exceptions import ReportersValidatorsErrorTag

from ...testspec import Assert, TestAction, TestSpec, idspec


def mock_callback_valid(  # pylint: disable=unused-argument
        *, case: Case, section: Section, output_format: Format, output: Any) -> None:
    """A valid mock callback function."""


def mock_callback_not_keyword_only(   # pylint: disable=unused-argument
        case: Case, *, section: Section, output_format: Format, output: Any) -> None:
    """A mock callback function with a non-keyword-only parameter."""


def mock_callback_missing_output(  # pylint: disable=unused-argument
        *, case: Case, section: Section, output_format: Format) -> None:
    """A mock callback function missing the 'output' parameter."""


def mock_callback_wrong_type_output(  # pylint: disable=unused-argument
        *, case: Case, section: Section, output_format: Format, output: str) -> None:
    """A mock callback function with wrong type for 'output' parameter (str instead of Any)."""


def mock_callback_missing_output_type_hint(  # pylint: disable=unused-argument
        *, case: Case, section: Section, output_format, output) -> None:
    """A mock callback function missing the type hint for 'output_format' parameter."""


def mock_callback_missing_output_format(  # pylint: disable=unused-argument
        *, case: Case, section: Section, output: Any) -> None:
    """A mock callback function missing the 'output_format' parameter."""


def mock_callback_wrong_type_output_format(  # pylint: disable=unused-argument
        *, case: Case, section: Section, output_format: str, output: Any) -> None:
    """A mock callback function with wrong type for 'output_format' parameter (str instead of Format)."""


def mock_callback_missing_output_format_type_hint(  # pylint: disable=unused-argument
        *, case: Case, section: Section, output_format, output: Any) -> None:
    """A mock callback function missing the type hint for 'output_format' parameter."""


def mock_callback_missing_section(  # pylint: disable=unused-argument
        *, case: Case, output_format: Format, output: Any) -> None:
    """A mock callback function missing the 'section' parameter."""


def mock_callback_wrong_type_section(  # pylint: disable=unused-argument
        *, case: Case, section: str, output_format: Format, output: Any) -> None:
    """A mock callback function with wrong type for 'section' parameter (str instead of Section)."""


def mock_callback_missing_section_type_hint(  # pylint: disable=unused-argument
        *, case: Case, section, output_format: Format, output: Any) -> None:
    """A mock callback function missing the type hint for 'section' parameter."""


def mock_callback_missing_case(  # pylint: disable=unused-argument
        *, section: Section, output_format: Format, output: Any) -> None:
    """A mock callback function missing the 'case' parameter."""


def mock_callback_wrong_type_case(  # pylint: disable=unused-argument
        *, case: str, section: Section, output_format: Format, output: Any) -> None:
    """A mock callback function with wrong type for 'case' parameter (str instead of Case)."""


def mock_callback_missing_case_type_hint(  # pylint: disable=unused-argument
        *, case, section: Section, output_format: Format, output: Any) -> None:
    """A mock callback function missing the type hint for 'case' parameter."""


def mock_callback_not_none(  # pylint: disable=unused-argument
        *, case: Case, section: Section, output_format: Format, output: Any) -> str:
    """A mock callback function that returns something other than None."""
    return "I should have returned None at Albuquerque!"  # pragma: no cover


def mock_callback_missing_return_type(  # pylint: disable=unused-argument
        *, case: Case, section: Section, output_format: Format, output: Any):
    """A mock callback function that is missing a return type annotation."""


def mock_callback_extra_param(  # pylint: disable=unused-argument
        *, case: Case, section: Section, output_format: Format, output: Any, extra: Any) -> None:
    """A mock callback function that correctly returns None."""


@pytest.mark.parametrize("testspec", [
    idspec("CALLBACK_001", TestAction(
        name="valid callback",
        action=validate_reporter_callback, args=[mock_callback_valid],
        assertion=Assert.EQUAL, expected=mock_callback_valid)),
    idspec("CALLBACK_002", TestAction(
        name="invalid callback not keyword-only parameter",
        action=validate_reporter_callback, args=[mock_callback_not_keyword_only],
        exception=SimpleBenchTypeError,
        exception_tag=ReportersValidatorsErrorTag.INVALID_CALL_INCORRECT_SIGNATURE_PARAMETER_NOT_KEYWORD_ONLY)),
    idspec("CALLBACK_003", TestAction(
        name="invalid callback missing 'output' parameter",
        action=validate_reporter_callback, args=[mock_callback_missing_output],
        exception=SimpleBenchTypeError,
        exception_tag=ReportersValidatorsErrorTag.INVALID_CALL_INCORRECT_SIGNATURE_MISSING_PARAMETER)),
    idspec("CALLBACK_004", TestAction(
        name="invalid callback wrong type for 'output' parameter",
        action=validate_reporter_callback, args=[mock_callback_wrong_type_output],
        exception=SimpleBenchTypeError,
        exception_tag=ReportersValidatorsErrorTag.INVALID_CALL_INCORRECT_SIGNATURE_PARAMETER_TYPE)),
    idspec("CALLBACK_005", TestAction(
        name="invalid callback missing type hint for 'output' parameter",
        action=validate_reporter_callback, args=[mock_callback_missing_output_type_hint],
        exception=SimpleBenchTypeError,
        exception_tag=ReportersValidatorsErrorTag.INVALID_CALL_INCORRECT_SIGNATURE_MISSING_PARAMETER_TYPE_HINT)),
    idspec("CALLBACK_006", TestAction(
        name="invalid callback missing 'output_format' parameter",
        action=validate_reporter_callback, args=[mock_callback_missing_output_format],
        exception=SimpleBenchTypeError,
        exception_tag=ReportersValidatorsErrorTag.INVALID_CALL_INCORRECT_SIGNATURE_MISSING_PARAMETER)),
    idspec("CALLBACK_007", TestAction(
        name="invalid callback missing type hint for 'output_format' parameter",
        action=validate_reporter_callback, args=[mock_callback_missing_output_format_type_hint],
        exception=SimpleBenchTypeError,
        exception_tag=ReportersValidatorsErrorTag.INVALID_CALL_INCORRECT_SIGNATURE_MISSING_PARAMETER_TYPE_HINT)),
    idspec("CALLBACK_008", TestAction(
        name="invalid callback wrong type for 'output_format' parameter",
        action=validate_reporter_callback, args=[mock_callback_wrong_type_output_format],
        exception=SimpleBenchTypeError,
        exception_tag=ReportersValidatorsErrorTag.INVALID_CALL_INCORRECT_SIGNATURE_PARAMETER_TYPE)),
    idspec("CALLBACK_009", TestAction(
        name="invalid callback missing 'section' parameter",
        action=validate_reporter_callback, args=[mock_callback_missing_section],
        exception=SimpleBenchTypeError,
        exception_tag=ReportersValidatorsErrorTag.INVALID_CALL_INCORRECT_SIGNATURE_MISSING_PARAMETER)),
    idspec("CALLBACK_010", TestAction(
        name="invalid callback wrong type for 'section' parameter",
        action=validate_reporter_callback, args=[mock_callback_wrong_type_section],
        exception=SimpleBenchTypeError,
        exception_tag=ReportersValidatorsErrorTag.INVALID_CALL_INCORRECT_SIGNATURE_PARAMETER_TYPE)),
    idspec("CALLBACK_011", TestAction(
        name="invalid callback missing type hint for 'section' parameter",
        action=validate_reporter_callback, args=[mock_callback_missing_section_type_hint],
        exception=SimpleBenchTypeError,
        exception_tag=ReportersValidatorsErrorTag.INVALID_CALL_INCORRECT_SIGNATURE_MISSING_PARAMETER_TYPE_HINT)),
    idspec("CALLBACK_012", TestAction(
        name="invalid callback missing 'case' parameter",
        action=validate_reporter_callback, args=[mock_callback_missing_case],
        exception=SimpleBenchTypeError,
        exception_tag=ReportersValidatorsErrorTag.INVALID_CALL_INCORRECT_SIGNATURE_MISSING_PARAMETER)),
    idspec("CALLBACK_013", TestAction(
        name="invalid callback wrong type for 'case' parameter",
        action=validate_reporter_callback, args=[mock_callback_wrong_type_case],
        exception=SimpleBenchTypeError,
        exception_tag=ReportersValidatorsErrorTag.INVALID_CALL_INCORRECT_SIGNATURE_PARAMETER_TYPE)),
    idspec("CALLBACK_0014", TestAction(
        name="invalid callback missing type hint for 'case' parameter",
        action=validate_reporter_callback, args=[mock_callback_missing_case_type_hint],
        exception=SimpleBenchTypeError,
        exception_tag=ReportersValidatorsErrorTag.INVALID_CALL_INCORRECT_SIGNATURE_MISSING_PARAMETER_TYPE_HINT)),
    idspec("CALLBACK_015", TestAction(
        name="invalid callback not returning None",
        action=validate_reporter_callback, args=[mock_callback_not_none],
        exception=SimpleBenchTypeError,
        exception_tag=ReportersValidatorsErrorTag.REPORTER_CALLBACK_INCORRECT_RETURN_ANNOTATION_TYPE)),
    idspec("CALLBACK_016", TestAction(
        name="invalid callback with extra parameter",
        action=validate_reporter_callback, args=[mock_callback_extra_param],
        exception=SimpleBenchTypeError,
        exception_tag=ReportersValidatorsErrorTag.REPORTER_CALLBACK_INCORRECT_NUMBER_OF_PARAMETERS)),
    idspec("CALLBACK_017", TestAction(
        name="Callback is None with allow_none=True",
        action=validate_reporter_callback, args=[None], kwargs={"allow_none": True},
        assertion=Assert.EQUAL, expected=None)),
    idspec("CALLBACK_018", TestAction(
        name="Callback is None with allow_none=False",
        action=validate_reporter_callback, args=[None], kwargs={"allow_none": False},
        exception=SimpleBenchTypeError,
        exception_tag=ReportersValidatorsErrorTag.REPORTER_CALLBACK_NOT_CALLABLE_OR_NONE)),
    idspec("CALLBACK_019", TestAction(
        name="Callback is missing return type annotation",
        action=validate_reporter_callback, args=[mock_callback_missing_return_type],
        exception=SimpleBenchTypeError,
        exception_tag=ReportersValidatorsErrorTag.REPORTER_CALLBACK_MISSING_RETURN_ANNOTATION)),
])
def test_validate_reporter_callback(testspec: TestSpec) -> None:
    """Test validate_reporter_callback function."""
    testspec.run()


def checking_type_narrowing() -> None:  # pragma: no cover
    """Function to check type narrowing behavior of validate_reporter_callback.

    These are not actual tests but are here to ensure that type checkers
    correctly narrow the types based on the presence or absence of the
    allow_none parameter. It is not even run as part of the test suite.

    There is literally no runtime effect of this function and the only effect
    is to allow visual inspection of the type narrowing behavior in IDEs
    and static type checkers.
    """
    # TODO: integrate mypy directly into the test suite to automatically verify this behavior

    # Without allow_none parameter (valid_callback is annotated as ReporterCallback)
    valid_callback: ReporterCallback = validate_reporter_callback(mock_callback_valid)

    # With allow_none=True (valid_or_none_callback is annoated as ReporterCallback | None)
    valid_or_none_callback: ReporterCallback | None = validate_reporter_callback(mock_callback_valid, allow_none=True)

    # With allow_none=False (valid_or_none_callback is annoated as ReporterCallback | None)
    valid_or_none_callback = validate_reporter_callback(mock_callback_valid, allow_none=False)

    _ = valid_callback  # To avoid unused variable warnings
    _ = valid_or_none_callback  # To avoid unused variable warnings
