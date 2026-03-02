"""Validation functions for ResultsInfo v1."""
import re
from collections.abc import Mapping
from typing import TYPE_CHECKING

from simplebench.exceptions import SimpleBenchTypeError, SimpleBenchValueError
from simplebench.report._error_tags import _ResultsInfoErrorTag
from simplebench.simplebench_types import CoreDataMapping
from simplebench.validators import (
    validate_float,
    validate_string,
    validate_string_with_regex,
    validate_type,
)

if TYPE_CHECKING:
    from simplebench.report.versions.v1 import ExtrasObject, MetricsObject

__all__: list[str] = []

_HASH_RE: re.Pattern[str] = re.compile(r'^[a-f0-9]{64}$')
"""Regular expression pattern for validating 64-character hexadecimal strings."""


def hash_id(value: str) -> str:
    """Validate hash_id property.

    It is validated to be a 64-character hexadecimal string or an empty string.

    :param str value: The hash_id string to validate.
    :return str: The validated hash_id string.
    :raises SimpleBenchTypeError: If value is not a string.
    :raises SimpleBenchValueError: If value is not either empty or a 64-character hexadecimal string
    """
    hash_string = validate_string(
        value,
        'hash_id',
        _ResultsInfoErrorTag.INVALID_HASH_ID_TYPE,
        _ResultsInfoErrorTag.INVALID_HASH_ID_VALUE,
        allow_empty=True,
        strip=True,
    )
    if hash_string == '':
        return ''

    return validate_string_with_regex(
        hash_string,
        'hash_id',
        _HASH_RE,
        _ResultsInfoErrorTag.INVALID_HASH_ID_TYPE,
        _ResultsInfoErrorTag.INVALID_HASH_ID_VALUE,
        message='{name} must be 64-character hexadecimal string. Found: {value}',
    )


def group(value: str) -> str:
    """Validate the group property.

    :param str value: The group value to validate.
    :return str: The validated group value.
    :raises SimpleBenchTypeError: If the group is not a string.
    :raises SimpleBenchValueError: If the group is an empty string.
    """
    return validate_string(
        value,
        'group',
        _ResultsInfoErrorTag.INVALID_GROUP_TYPE,
        _ResultsInfoErrorTag.INVALID_GROUP_VALUE_EMPTY_STRING,
        allow_empty=False,
        allow_blank=False,
        strip=True,
    )


def title(value: str) -> str:
    """Validate the title property.

    :param str value: The title value to validate.
    :return str: The validated title value.
    :raises SimpleBenchTypeError: If the title is not a string.
    :raises SimpleBenchValueError: If the title is an empty string.
    """
    return validate_string(
        value,
        'title',
        _ResultsInfoErrorTag.INVALID_TITLE_TYPE,
        _ResultsInfoErrorTag.INVALID_TITLE_VALUE_EMPTY_STRING,
        allow_empty=False,
        allow_blank=False,
        strip=True,
    )


def description(value: str) -> str:
    """Validate the description property.

    :param str value: The description value to validate.
    :return str: The validated description value.
    :raises SimpleBenchTypeError: If the description is not a string.
    :raises SimpleBenchValueError: If the description is an empty string.
    """
    return validate_string(
        value,
        'description',
        _ResultsInfoErrorTag.INVALID_DESCRIPTION_TYPE,
        _ResultsInfoErrorTag.INVALID_DESCRIPTION_EMPTY_STRING,
        allow_empty=False,
        allow_blank=False,
        strip=True,
    )


def n(value: float) -> float:
    """Validate the n property.

    :param float value: The n value to validate.
    :return float: The validated n value.
    :raises SimpleBenchTypeError: If n is not a float.
    :raises SimpleBenchValueError: If n is less than 1.
    """
    value = validate_float(value, 'n', _ResultsInfoErrorTag.INVALID_N_TYPE)
    if value < 1:
        raise SimpleBenchValueError(f'n must be >= 1, got {value}', tag=_ResultsInfoErrorTag.INVALID_N_VALUE)
    return value


def variation_marks(value: Mapping[str, str]) -> CoreDataMapping[str]:
    """Validate the variation_marks property.

    Validates that `variation_marks` is a mapping of strings to strings
    and converts it to an CoreDataMapping[str] if it is not already.

    :param Mapping[str, str] value: The variation_marks values to validate.
    :return CoreDataMapping[str]: The validated variation_marks values dictionary
    :raises SimpleBenchTypeError: If variation_marks is not a mapping of strings to strings.
    """
    if not isinstance(value, Mapping):
        raise SimpleBenchTypeError(
            f'variation_marks must be a mapping of strings to strings, got {type(value)}',
            tag=_ResultsInfoErrorTag.INVALID_VARIATION_MARKS_TYPE)
    if not all(isinstance(k, str) and isinstance(v, str) for k, v in value.items()):
        raise SimpleBenchTypeError(
            'All keys and values in variation_marks must be strings',
            tag=_ResultsInfoErrorTag.INVALID_VARIATION_MARKS_CONTENT
        )
    return value if isinstance(value, CoreDataMapping) else CoreDataMapping(value)


def metrics(value: 'MetricsObject') -> 'MetricsObject':
    """Validate the metrics property.

    :param MetricsObject value: The metrics value to validate.
    :return MetricsObject: The validated metrics value.
    :raises SimpleBenchTypeError: If metrics is not a MetricsObject.
    """
    from .. import METRIC_ITEM_TYPES, MetricItem, MetricsObject

    validate_type(
        value,
        MetricsObject,
        'metrics',
        _ResultsInfoErrorTag.INVALID_METRICS_TYPE,
        message=f'metrics must be a MetricsObject, got {type(value)}',
    )
    if not all(isinstance(item, METRIC_ITEM_TYPES) for item in value.values()):
        mismatched_items = [type(item) for item in value.values() if not isinstance(item, METRIC_ITEM_TYPES)]
        raise SimpleBenchTypeError(
            f'All items in metrics must be one of {MetricItem!r}. Found mismatched item types: {mismatched_items!r}',
            tag=_ResultsInfoErrorTag.INVALID_METRICS_CONTENT
        )

    return value


def extra_info(value: 'ExtrasObject') -> 'ExtrasObject':
    """Validate the extra_info property.

    Validates that `extra_info` an ExtrasObject instance, which is a mapping
    of strings to CoreDataTypes

    :param ExtrasObject value: The extra_info value to validate.
    :return ExtrasObject: The validated extra_info values dictionary.
    :raises SimpleBenchTypeError: If extra_info is not an ExtrasObject instance.
    """
    from .. import ExtrasObject

    if not isinstance(value, ExtrasObject):
        raise SimpleBenchTypeError(
            f'extra_info must be an ExtrasObject instance, got {type(value)}',
            tag=_ResultsInfoErrorTag.INVALID_EXTRA_INFO_TYPE)
    return value
