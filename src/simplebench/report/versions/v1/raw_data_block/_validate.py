"""Validators for the RawDataBlock class"""

import re
from collections.abc import Sequence
from typing import Any

from simplebench.exceptions import SimpleBenchTypeError, SimpleBenchValueError
from simplebench.report._error_tags import _RawDataBlockErrorTag
from simplebench.simplebench_types import Values
from simplebench.validators import (
    validate_string,
    validate_string_with_regex,
)

from ..metric import Metric


def metric(value: Any) -> Metric:
    """Validate the metric.

    The metric must be an instance of the Metric class.

    :param Any value: The metric to validate.
    :return Metric: The validated Metric instance.
    :raise SimpleBenchTypeError: If the metric is not an instance of Metric.
    """
    from ..metric import Metric  # Import here to avoid circular import issues
    if not isinstance(value, Metric):
        raise SimpleBenchTypeError(
            f"Expected Metric instance for metric, got {type(value).__name__}",
            tag=_RawDataBlockErrorTag.INVALID_METRIC_TYPE,
        )
    return value


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

    if value == '':
        return value

    return validate_string_with_regex(
        value,
        'hash_id',
        _HASH_ID_REGEX,
        _RawDataBlockErrorTag.INVALID_HASH_ID_TYPE,  # impossible to trigger the type error here
        _RawDataBlockErrorTag.INVALID_HASH_ID_VALUE,
    )


def rounds(value: int) -> int:
    """Validate that rounds is a positive integer."""
    if not isinstance(value, int) or isinstance(value, bool):
        raise SimpleBenchTypeError(
            f"Expected int for rounds, got {type(value).__name__}",
            tag=_RawDataBlockErrorTag.INVALID_ROUNDS_TYPE,
        )
    if value <= 0:
        raise SimpleBenchValueError(
            "Rounds must be positive",
            tag=_RawDataBlockErrorTag.INVALID_ROUNDS_VALUE,
        )
    return value


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
