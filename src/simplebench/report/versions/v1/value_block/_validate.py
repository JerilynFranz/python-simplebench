"""Validation utilities for V1 ValueBlock.

This module provides functions to validate the fields of a ValueBlock
according to the specifications defined for version 1 reports.

Each function checks the type and value constraints for a specific field,
returns the validated and correctly typed value, and raises appropriate
exceptions if the validation fails.
"""

import re

from simplebench.report._error_tags import _ValueBlockErrorTag
from simplebench.validators import (
    validate_float,
    validate_namespaced_identifier,
    validate_positive_float,
    validate_string,
    validate_string_with_regex,
)

_HASH_ID_REGEX = re.compile(r'^[a-fA-F0-9]{64}$')

__all__: list[str] = []


def hash_id(val: str) -> str:
    """Validate the hash_id string.

    An empty string is allowed, which indicates that the hash_id should be
    computed automatically.

    :param value: The unique hash identifier for the vcs information.
    :return: The validated hash_id string.
    :raises SimpleBenchTypeError: If the hash_id value is not a string.
    :raises SimpleBenchValueError: If the hash_id string is not a valid 64-character hexadecimal string (when not empty).
    """
    val = validate_string(
        val,
        'hash_id',
        _ValueBlockErrorTag.INVALID_HASH_ID_TYPE,
        _ValueBlockErrorTag.INVALID_HASH_ID_VALUE,
        allow_empty=True,
        strip=True,
    )
    if val == '':
        return val  # Allow empty string for automatic hash_id generation

    return validate_string_with_regex(
        val,
        'hash_id',
        _HASH_ID_REGEX,
        _ValueBlockErrorTag.INVALID_HASH_ID_STRUCTURE,  # can't trigger type error here
        _ValueBlockErrorTag.INVALID_HASH_ID_STRUCTURE,
    )


def semantic_type(val: str) -> str:
    """Validate the semantic type.

    Checks that the semantic type is a valid namespaced identifier.

    :param str value: The semantic type string to validate.
    :return str: The validated semantic type string.
    :raise SimpleBenchTypeError: If the semantic type is not a string.
    :raises SimpleBenchValueError: If the semantic type string is invalid.
    """
    return validate_namespaced_identifier(
        val,
        'semantic_type',
        _ValueBlockErrorTag.INVALID_SEMANTIC_TYPE_TYPE,
        _ValueBlockErrorTag.INVALID_SEMANTIC_TYPE_VALUE,
    )


def timer(val: str | None) -> str:
    """Validate the timer.

    :param str | None val: The timer string to validate.
    :return str: The validated timer string.
    :raise SimpleBenchTypeError: If the timer is not a string or None.
    :raises SimpleBenchValueError: If the timer string is invalid.
    """
    if val is None:
        return ''

    timer_name: str = validate_string(
        val,
        'timer',
        _ValueBlockErrorTag.INVALID_TIMER_TYPE,
        _ValueBlockErrorTag.INVALID_TIMER_VALUE,
        allow_blank=False,
        allow_empty=True,
        strip=True,
    )

    return timer_name


def unit(val: str) -> str:
    """Validate the unit of measurement.

    :param str value: The unit of measurement string to validate.
    :return str: The validated unit of measurement string.
    :raise SimpleBenchTypeError: If the unit is not a string.
    :raises SimpleBenchValueError: If the unit string is invalid.
    """
    return validate_string(
        val,
        'unit',
        _ValueBlockErrorTag.INVALID_UNIT_TYPE,
        _ValueBlockErrorTag.INVALID_UNIT_VALUE,
        allow_blank=False,
        allow_empty=False,
        strip=True,
    )


def scale(val: float) -> float:
    """Validate the scale factor.

    Validate that the scale factor is a positive float (greater than zero).

    :param float value: The scale factor to validate.
    :return float: The validated scale factor.
    :raise SimpleBenchTypeError: If the scale is not a float.
    :raises SimpleBenchValueError: If the scale factor is not a positive number.
    """
    return validate_positive_float(
        val, 'scale',
        _ValueBlockErrorTag.INVALID_SCALE_TYPE,
        _ValueBlockErrorTag.INVALID_SCALE_VALUE
    )


def value(val: float | int) -> float:
    """Validate the value.

    Validates that the value is a float or int and returns it as a float.

    :param float | int value: The value to validate.
    :return float: The validated value.
    :raise SimpleBenchTypeError: If the value is not a float or int.
    """
    return validate_float(val, 'value', _ValueBlockErrorTag.INVALID_VALUE_TYPE)
