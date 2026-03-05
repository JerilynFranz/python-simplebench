"""Validation logic for MetricType objects"""

import re

from simplebench.exceptions import SimpleBenchTypeError, SimpleBenchValueError
from simplebench.report._error_tags import _MetricTypeErrorTag
from simplebench.validators import (
    validate_hash_id,
    validate_namespaced_identifier,
    validate_string,
    validate_type,
)

from ..metric_category import MetricCategory

__all__: list[str] = []

_LABEL_REGEX = re.compile(r'^[A-Z](?:[A-Z0-9_]*[A-Z0-9])?$')


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
        _MetricTypeErrorTag.INVALID_HASH_ID_FIELD_TYPE,
        _MetricTypeErrorTag.INVALID_HASH_ID_FIELD_VALUE,
        allow_empty=True,
    )

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
    value = validate_type(value, str, 'label', _MetricTypeErrorTag.INVALID_LABEL_FIELD_TYPE)
    if not _LABEL_REGEX.match(value):
        raise SimpleBenchValueError(
            f"Label '{value}' does not match the required pattern: {_LABEL_REGEX.pattern!r}",
            tag=_MetricTypeErrorTag.INVALID_LABEL_FIELD_VALUE,
        )
    return value


def description(value: str) -> str:
    """Validate the description of the metric

    The description must be a string, and may be empty or blank.

    :raises SimpleBenchTypeError: If the description is not a string
    """
    return validate_string(
        value,
        'description',
        _MetricTypeErrorTag.INVALID_DESCRIPTION_FIELD,
        _MetricTypeErrorTag.INVALID_DESCRIPTION_FIELD,
        allow_blank=True,
        allow_empty=True,
    )


_UNIT_REGEX = re.compile(r'^[A-Za-z](?:[A-Za-z0-9/\-_\. ]*[A-Za-z0-9])?$')
"""Validates the unit of the metric

The unit must be a non-empty string that starts with a letter
and may contain letters, digits, slashes, hyphens, underscores, dots, and spaces.
It must not start or end with a slash, hyphen, underscore, or dot.
The unit must not be empty or blank.
"""


def unit(value: str) -> str:
    """Validate the unit of the metric

    The unit must be a non-empty string that starts with a letter
    and may contain letters, digits, slashes, hyphens, underscores, dots, and spaces.
    It must not start or end with a slash, hyphen, underscore, or dot.
    The unit must not be empty or blank.

    :raises SimpleBenchValueError: If the unit is invalid
    :raises SimpleBenchTypeError: If the unit is not a string
    """
    value = validate_type(value, str, 'unit', _MetricTypeErrorTag.INVALID_UNIT_FIELD_TYPE)
    if not _UNIT_REGEX.match(value):
        raise SimpleBenchValueError(
            f"Unit '{value}' does not match the required pattern: {_UNIT_REGEX.pattern!r}",
            tag=_MetricTypeErrorTag.INVALID_UNIT_FIELD_VALUE,
        )
    return value


def scale(value: float | int) -> float:
    """Validate the scale of the metric

    The scale must be a positive float (greater than 0.0). A type error will be raised if the value
    cannot be converted to a float.

    :raises SimpleBenchValueError: If the scale is not positive.
    :raises SimpleBenchTypeError: If the scale is not a float or int.
    """
    value = validate_type(value, (float, int), 'scale', _MetricTypeErrorTag.INVALID_SCALE_FIELD_TYPE)
    if value <= 0.0:
        raise SimpleBenchValueError(
            f"Scale '{value}' must be greater than 0.0", tag=_MetricTypeErrorTag.INVALID_SCALE_FIELD_VALUE
        )
    return float(value)


def semantic_type(value: str) -> str:
    """Validate the semantic type of the metric

    The semantic type must be a valid namespaced identifier, e.g. 'simplebench_std::operations_per_second'.
    The semantic type must not be empty or blank.

    :raises SimpleBenchValueError: If the semantic type is invalid
    :raises SimpleBenchTypeError: If the semantic type is not a string
    """
    return validate_namespaced_identifier(
        value,
        'semantic_type',
        _MetricTypeErrorTag.INVALID_SEMANTIC_TYPE_FIELD_TYPE,
        _MetricTypeErrorTag.INVALID_SEMANTIC_TYPE_FIELD_VALUE,
    )


def category(value: MetricCategory) -> MetricCategory:
    """Validate the category of the metric

    The category must be a valid MetricCategory enum value.

    :raises SimpleBenchTypeError: If the category is not a valid MetricCategory enum value
    """
    if not isinstance(value, MetricCategory):
        raise SimpleBenchTypeError(
            f"Metric category '{value}' is not a valid MetricCategory enum value",
            tag=_MetricTypeErrorTag.INVALID_CATEGORY_FIELD_TYPE,
        )
    return value
