"""Validation functions for metrics."""

import re

from simplebench.exceptions import SimpleBenchValueError
from simplebench.report._error_tags import _MetricErrorTag
from simplebench.validators import validate_hash_id, validate_string, validate_type

from ..metric_type import MetricType

__all__: list[str] = []


def hash_id(value: str) -> str:
    """Validate the hash_id string.

    The hash_id must be a string that is either empty or a valid 64-character hexadecimal string.

    :raises SimpleBenchValueError: If the hash_id string is not a valid 64-character hexadecimal string
        (when not empty).
    :raises SimpleBenchTypeError: If the hash_id value is not a string.
    """
    return validate_hash_id(
        value,
        'hash_id',
        _MetricErrorTag.INVALID_HASH_ID_FIELD_TYPE,
        _MetricErrorTag.INVALID_HASH_ID_FIELD_VALUE,
        allow_empty=True,
    )

def title(value: str) -> str:
    """Validate the title of the metric

    The title must be a string, and may not be empty or blank.

    :param value: The value to validate as the title of the metric.
    :type value: str
    :raises SimpleBenchTypeError: If the title is not a string
    :raises SimpleBenchValueError: If the title is empty or blank
    """
    return validate_string(
        value, 'title',
        _MetricErrorTag.INVALID_TITLE_FIELD_TYPE,
        _MetricErrorTag.INVALID_TITLE_FIELD_VALUE,
        allow_blank=False,
        allow_empty=False,
        strip=True,
    )


def description(value: str) -> str:
    """Validate the description of the metric

    The description must be a string, and may be empty or blank.

    :param value: The value to validate as the description of the metric.
    :type value: str
    :raises SimpleBenchTypeError: If the description is not a string
    """
    return validate_string(
        value, 'description',
        _MetricErrorTag.INVALID_DESCRIPTION_FIELD,
        _MetricErrorTag.INVALID_DESCRIPTION_FIELD,
        allow_blank=False,
        allow_empty=True,
        strip=True,
    )


_LABEL_REGEX: re.Pattern = re.compile(r'^[A-Z](?:[A-Z0-9_]*[A-Z0-9])?$')
"""Regex pattern for validating the label of the metric

It must start with an uppercase letter, end with an uppercase letter or digit,
and may contain uppercase letters, digits, and underscores in between.
"""


def label(value: str) -> str:
    """Validate the label of the metric

    The label must be a non-empty string that starts with an uppercase letter and ends with an uppercase letter,
    and may contain uppercase letters, digits, and underscores in between.
    It must not start or end with an underscore.
    The label must not be empty or blank.
    The label must not contain any characters other than uppercase letters, digits, and underscores.

    :raises SimpleBenchValueError: If the label is invalid
    :raises SimpleBenchTypeError: If the label is not a string
    """
    validate_type(value, str, 'label', _MetricErrorTag.INVALID_LABEL_FIELD_TYPE)
    if not _LABEL_REGEX.match(value):
        raise SimpleBenchValueError(
            f"Label '{value}' does not match the required pattern: {_LABEL_REGEX.pattern!r}",
            tag=_MetricErrorTag.INVALID_LABEL_FIELD_VALUE,
        )
    return value


def metric_type(value: MetricType) -> MetricType:
    """Validate the metric_type of the metric

    The metric_type must be an instance of MetricType,
    and must be registered in the metric_types_registry.

    :param value: The value to validate as the metric_type of the metric.
    :type value: MetricType
    :raises SimpleBenchTypeError: If the metric_type is not an instance of MetricType
    """
    return validate_type(value, MetricType, 'metric_type', _MetricErrorTag.INVALID_METRIC_TYPE_FIELD_TYPE)
