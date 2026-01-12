"""Validators for the RawDataBlock class"""

import re
from collections.abc import Sequence
from typing import Any

from simplebench.report._error_tags import _RawDataBlockErrorTag
from simplebench.types import Values
from simplebench.validators import (
    validate_namespaced_identifier,
    validate_positive_float,
    validate_string,
    validate_string_with_regex,
)

_HASH_ID_REGEX = re.compile(r'^[0-9a-f]{64}$')
"""Regular expression for validating hash_id strings.

The hash_id must be a 64-character hexadecimal string.
"""


def hash_id(value: str) -> str:
    """Validate the hash_id.

    The hash_id must be either an empty string or a 64-character hexadecimal string.

    :param str value: The hash_id string to validate.
    :return str: The validated hash_id string.
    :raise SimpleBenchTypeError: If the hash_id is not a string.
    :raise SimpleBenchValueError: If the hash_id has an invalid value.
    """
    validate_string(
        value,
        'hash_id',
        _RawDataBlockErrorTag.INVALID_HASH_ID_TYPE,
        _RawDataBlockErrorTag.INVALID_HASH_ID_VALUE,  # impossible to trigger the value error here
        strip=True,
        allow_blank=True,
        allow_empty=True,
    )

    return validate_string_with_regex(
        value,
        'hash_id',
        _HASH_ID_REGEX,
        _RawDataBlockErrorTag.INVALID_HASH_ID_TYPE,  # impossible to trigger the type error here
        _RawDataBlockErrorTag.INVALID_HASH_ID_VALUE,
    )


def data(value: Values | Sequence[int | float]) -> Values:
    """Validate the data.

    If the input is already a `Values` instance, it is returned as-is.
    Otherwise, a new `Values` instance is created from the input sequence.

    :param Values | Sequence[int | float] value: The data to validate.
    :return Values: The validated data.
    :raise SimpleBenchTypeError: If the data is not of type Values.
    """
    if isinstance(value, Values):
        return value
    return Values(value)


def scale(value: float) -> float:
    """Validate that scale is a positive floating point number (greater than 0).

    :param float value: The value to validate.
    :return float: The validated positive floating point value.
    :raise SimpleBenchTypeError: If the value is not a float.
    :raise SimpleBenchValueError: If the value is not positive.
    """
    return validate_positive_float(
        value, 'scale', _RawDataBlockErrorTag.INVALID_SCALE_TYPE, _RawDataBlockErrorTag.INVALID_SCALE_VALUE
    )


def semantic_type(value: Any) -> str:
    """Validate the semantic_type

    The semantic_type must be a valid namespaced identifier.

    :param Any value: The semantic type string to validate.
    :return str: The validated semantic type string.
    :raise SimpleBenchTypeError: If the semantic type is not a string.
    :raise SimpleBenchValueError: If the semantic type string is invalid.
    """
    return validate_namespaced_identifier(
        value,
        'semantic_type',
        _RawDataBlockErrorTag.INVALID_SEMANTIC_TYPE_TYPE,
        _RawDataBlockErrorTag.INVALID_SEMANTIC_TYPE_VALUE,
    )


def timer(value: Any) -> str | None:
    """Validate the timer.
    :param value: The timer string to validate.
    :return str | None: The validated timer string or None.
    :raise SimpleBenchTypeError: If the timer is not a string or None.
    :raises SimpleBenchValueError: If the timer string is invalid.
    """
    if value is None:
        return None

    timer_name: str = validate_string(
        value,
        'timer',
        _RawDataBlockErrorTag.INVALID_TIMER_TYPE,
        _RawDataBlockErrorTag.INVALID_TIMER_VALUE,
        allow_blank=False,
    )

    return timer_name


def unit(value: str) -> str:
    """Validates that unit is a non-blank string.

    :param str value: The value to validate.
    :return str: The validated string value.
    :raise SimpleBenchTypeError: If the value is not a string.
    :raise SimpleBenchValueError: If the value is blank.
    """
    return validate_string(
        value,
        'unit',
        _RawDataBlockErrorTag.INVALID_UNIT_TYPE,
        _RawDataBlockErrorTag.INVALID_UNIT_VALUE,
        allow_blank=False,
    )
