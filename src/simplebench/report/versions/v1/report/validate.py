"""Validation functions for V1 report version."""
from typing import TYPE_CHECKING, Any, Sequence

from simplebench.exceptions import SimpleBenchValueError
from simplebench.report._error_tags import _ReportErrorTag
from simplebench.type_proxies import is_case
from simplebench.validators import validate_iso8601_datetime, validate_sequence_of_str, validate_string

if TYPE_CHECKING:
    from simplebench.case import Case


def case(value: 'Case') -> None:
    """Validate that the given object is a Case instance.

    :param value: The object to validate.
    :raises SimpleBenchValueError: If the object is not a Case instance.
    """
    if not is_case(value):
        raise SimpleBenchValueError(
            f"The provided object is a {type(value).__name__}, expected a Case instance.",
            tag=_ReportErrorTag.INVALID_CASE,
        )


def case_has_been_run(case: 'Case') -> None:
    """Validate that the given Case instance has been run.

    :param case: The Case instance to validate.
    :raises SimpleBenchValueError: If the Case has not been run.
    """
    if not case.has_run:
        raise SimpleBenchValueError(
            "The provided Case instance has not been run yet.",
            tag=_ReportErrorTag.CASE_HAS_NOT_BEEN_RUN,
        )
