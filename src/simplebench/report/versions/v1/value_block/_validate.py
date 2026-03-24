"""Validation utilities for V1 ValueBlock.

This module provides functions to validate the fields of a ValueBlock
according to the specifications defined for version 1 reports.

Each function checks the type and value constraints for a specific field,
returns the validated and correctly typed value, and raises appropriate
exceptions if the validation fails.
"""

import re

from simplebench.exceptions import SimpleBenchTypeError
from simplebench.report._error_tags import _ValueBlockErrorTag
from simplebench.validators import (
    validate_float,
    validate_string,
    validate_string_with_regex,
)

from ..metric import Metric

_HASH_ID_REGEX = re.compile(r'^[a-f0-9]{64}$')

__all__: list[str] = []


def hash_id(val: str) -> str:
    """Validate the hash_id string.

    An empty string is allowed, which indicates that the hash_id should be
    computed automatically.

    :param value: The unique hash identifier for the value information.
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


def metric(val: Metric) -> Metric:
    """Validate the metric.

    :param Metric val: The metric to validate.
    :return Metric: The validated metric instance.
    :raise SimpleBenchTypeError: If the metric is not a Metric instance.
    """
    if not isinstance(val, Metric):
        raise SimpleBenchTypeError(
            f'Metric must be an instance of Metric class. Found type: {type(val).__name__}',
            _ValueBlockErrorTag.INVALID_METRIC_TYPE
        )
    return val


def value(val: float | int) -> float:
    """Validate the value.

    Validates that the value is a float or int and returns it as a float.

    :param float | int value: The value to validate.
    :return float: The validated value.
    :raise SimpleBenchTypeError: If the value is not a float or int.
    """
    return validate_float(val, 'value', _ValueBlockErrorTag.INVALID_VALUE_TYPE)
