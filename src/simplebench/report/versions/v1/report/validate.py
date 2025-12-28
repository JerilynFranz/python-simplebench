"""Validation functions for V1 report version."""
from __future__ import annotations

from types import MappingProxyType
from typing import TYPE_CHECKING, Sequence

from simplebench.exceptions import SimpleBenchValueError
from simplebench.report._error_tags import _ReportErrorTag
from simplebench.type_proxies import is_case
from simplebench.types import ImmutableVariationColsType, VariationColsType
from simplebench.validators import (
    validate_iso8601_datetime,
    validate_sequence_of_str,
    validate_sequence_of_type,
    validate_string,
    validate_type,
)

from .. import MachineInfo, ResultsInfo

if TYPE_CHECKING:
    from simplebench.case import Case


def timestamp(value: str) -> str:
    """Validate a timestamp string in ISO 8601 format.

    :param str value: The timestamp string to validate.
    :return str: The validated timestamp string.
    :raises SimpleBenchTypeError: If the timestamp is not a string.
    :raises SimpleBenchValueError: If the timestamp is not a valid ISO 8601 string.
    """
    return validate_iso8601_datetime(
            value, 'timestamp',
            _ReportErrorTag.INVALID_TIMESTAMP_PROPERTY_TYPE,
            _ReportErrorTag.INVALID_TIMESTAMP_PROPERTY_VALUE)

def group(value: str) -> str:
    """Validate a group string.

    :param str value: The group string to validate.
    :return str: The validated group string.
    :raises SimpleBenchTypeError: If the group is not a string.
    :raises SimpleBenchValueError: If the group is an empty string.
    """
    return validate_string(
            value, "group",
            _ReportErrorTag.INVALID_GROUP_PROPERTY_TYPE,
            _ReportErrorTag.EMPTY_GROUP_PROPERTY_VALUE,
            allow_empty=False)

def title(value: str) -> str:
    """Validate a title string.

    :param str value: The title string to validate.
    :return str: The validated title string.
    :raises SimpleBenchTypeError: If the title is not a string.
    :raises SimpleBenchValueError: If the title is an empty string.
    """
    return validate_string(
            value, "title",
            _ReportErrorTag.INVALID_TITLE_PROPERTY_TYPE,
            _ReportErrorTag.EMPTY_TITLE_PROPERTY_VALUE,
            allow_empty=False)

def description(value: str) -> str:
    """Validate a description string.

    :param str value: The description string to validate.
    :return str: The validated description string.
    :raises SimpleBenchTypeError: If the description is not a string.
    :raises SimpleBenchValueError: If the description is an empty string.
    """
    return validate_string(
            value, "description",
            _ReportErrorTag.INVALID_DESCRIPTION_PROPERTY_TYPE,
            _ReportErrorTag.EMPTY_DESCRIPTION_PROPERTY_VALUE,
            allow_empty=False)

def variation_cols(value: VariationColsType) -> ImmutableVariationColsType:
    """Validate a variation_cols dictionary.

    :param VariationColsType value: The variation_cols dictionary to validate.
    :return ImmutableVariationColsType: The validated variation_cols as an immutable mapping.
    :raises SimpleBenchTypeError: If variation_cols is not a dict.
    :raises SimpleBenchValueError: If the keys or values in variation_cols are not strings.
    """
    if not isinstance(value, dict):
        raise SimpleBenchValueError(
            "variation_cols must be a dictionary",
            tag=_ReportErrorTag.INVALID_VARIATION_COLS_PROPERTY_TYPE)

    validate_sequence_of_str(
        value.keys(), "variation_cols keys",
        _ReportErrorTag.INVALID_VARIATION_COLS_KEYS_TYPE,
        _ReportErrorTag.INVALID_VARIATION_COLS_KEYS_VALUE,
        allow_empty=False)

    validate_sequence_of_str(
        value.values(), "variation_cols values",
        _ReportErrorTag.INVALID_VARIATION_COLS_VALUES_TYPE,
        _ReportErrorTag.INVALID_VARIATION_COLS_VALUES_VALUE,
        allow_empty=False)

    return MappingProxyType(value)

def results(value: Sequence[ResultsInfo]) -> tuple[ResultsInfo, ...]:
    """Validate a Sequence of ResultsInfo instances.

    :param Sequence[ResultsInfo] value: Sequence of ResultsInfo to validate.
    :return tuple[ResultsInfo, ...]: A validated tuple of ResultsInfo instances.
    :raises SimpleBenchTypeError: If results is not a Sequence of ResultsInfo.
    """
    return tuple(validate_sequence_of_type(
        value, ResultsInfo, 'results',
        _ReportErrorTag.INVALID_RESULTS_TYPE,
        _ReportErrorTag.INVALID_RESULTS_VALUE,
    ))

def machine(value: MachineInfo) -> MachineInfo:
    """Validate that the value is a MachineInfo instance.

    :param MachineInfo value: The object to validate.
    :raises SimpleBenchValueError: If the object is not a MachineInfo instance.
    """
    return validate_type(
        value, MachineInfo, "machine",
        _ReportErrorTag.INVALID_MACHINE_PROPERTY_TYPE,
        message="{name} must be a MachineInfo instance",
    )

def case(value: Case) -> None:
    """Validate that the given object is a Case instance.

    :param value: The object to validate.
    :raises SimpleBenchValueError: If the object is not a Case instance.
    """
    if not is_case(value):
        raise SimpleBenchValueError(
            f"The provided object is a {type(value).__name__}, expected a Case instance.",
            tag=_ReportErrorTag.INVALID_CASE,
        )


def case_has_been_run(value: Case) -> None:
    """Validate that the given Case instance has been run.

    :param value: The Case instance to validate.
    :raises SimpleBenchValueError: If the Case has not been run.
    """
    if not value.has_run:
        raise SimpleBenchValueError(
            "The provided Case instance has not been run yet.",
            tag=_ReportErrorTag.CASE_HAS_NOT_BEEN_RUN,
        )
