"""Validators for the RawDataBlock class"""
from typing import Any

from simplebench.report._error_tags import _RawDataBlockErrorTag
from simplebench.types import Values
from simplebench.validators import (
    validate_namespaced_identifier,
    validate_positive_float,
    validate_string,
    validate_type,
)


def validate_data(value: Values) -> Values:
    """Validate the data.

    :param Values value: The data to validate.
    :return Values: The validated data.
    :raise SimpleBenchTypeError: If the data is not of type Values.
    """
    return validate_type(
        value, Values, 'data',
        _RawDataBlockErrorTag.INVALID_DATA_TYPE)


def validate_scale(value: float) -> float:
    """Validate that scale is a positive floating point number (greater than 0).

    :param float value: The value to validate.
    :return float: The validated positive floating point value.
    :raise SimpleBenchTypeError: If the value is not a float.
    :raise SimpleBenchValueError: If the value is not positive.
    """
    return validate_positive_float(
            value, 'scale',
            _RawDataBlockErrorTag.INVALID_SCALE_TYPE,
            _RawDataBlockErrorTag.INVALID_SCALE_VALUE)


def validate_semantic_type(value: Any) -> str:
    """Validate the semantic_type

    The semantic_type must be a valid namespaced identifier.

    :param Any value: The semantic type string to validate.
    :return str: The validated semantic type string.
    :raise SimpleBenchTypeError: If the semantic type is not a string.
    :raise SimpleBenchValueError: If the semantic type string is invalid.
    """
    return validate_namespaced_identifier(
            value, 'semantic_type',
            _RawDataBlockErrorTag.INVALID_SEMANTIC_TYPE_TYPE,
            _RawDataBlockErrorTag.INVALID_SEMANTIC_TYPE_VALUE)


def validate_timer(value: Any) -> str | None:
    """Validate the timer.
    :param value: The timer string to validate.
    :return str | None: The validated timer string or None.
    :raise SimpleBenchTypeError: If the timer is not a string or None.
    :raises SimpleBenchValueError: If the timer string is invalid.
    """
    if value is None:
        return None

    timer_name: str = validate_string(
        value, 'timer',
        _RawDataBlockErrorTag.INVALID_TIMER_TYPE,
        _RawDataBlockErrorTag.INVALID_TIMER_VALUE,
        allow_blank=False)

    return timer_name


def validate_cpu_timer(value: Any) -> str | None:
    """Validate the cpu_timer.
    :param value: The cpu timer string to validate.
    :return str | None: The validated cpu timer string or None.
    :raise SimpleBenchTypeError: If the cpu_timer is not a string or None.
    :raises SimpleBenchValueError: If the cpu timer string is invalid.
    """
    if value is None:
        return None

    timer_name: str = validate_string(
        value, 'timer',
        _RawDataBlockErrorTag.INVALID_TIMER_TYPE,
        _RawDataBlockErrorTag.INVALID_TIMER_VALUE,
        allow_blank=False)

    return timer_name


def validate_unit(value: str) -> str:
    """Validates that unit is a non-blank string.

    :param str value: The value to validate.
    :return str: The validated string value.
    :raise SimpleBenchTypeError: If the value is not a string.
    :raise SimpleBenchValueError: If the value is blank.
    """
    return validate_string(
                value, 'unit',
                _RawDataBlockErrorTag.INVALID_UNIT_TYPE,
                _RawDataBlockErrorTag.INVALID_UNIT_VALUE,
                allow_blank=False)
