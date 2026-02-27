"""Validation functions for GenericEnvironment."""

import re
from typing import Any, Final

from simplebench.report._error_tags import _EnvironmentInfoErrorTag
from simplebench.simplebench_types import CoreDataMapping
from simplebench.validators import validate_core_data_mapping, validate_string, validate_string_with_regex

_HASH_RE: Final[re.Pattern[str]] = re.compile(r'^[a-f0-9]{64}$')
"""Regular expression pattern for validating 64-character hexadecimal strings."""


def title(value: str) -> str:
    """Validate title property.

    It is validated to be a non-empty string.

    :param str value: The title string to validate.
    :return str: The validated title string.
    :raises SimpleBenchTypeError: If value is not a string.
    :raises SimpleBenchValueError: If value is an empty string.
    """
    return validate_string(
        value,
        'title',
        _EnvironmentInfoErrorTag.INVALID_TITLE_TYPE,
        _EnvironmentInfoErrorTag.INVALID_TITLE_VALUE,
        allow_empty=False,
        allow_blank=False,
        strip=True,
    )


def description(value: str) -> str:
    """Validate description property.

    It is validated to be a string (empty string allowed).

    :param str value: The description string to validate.
    :return str: The validated description string.
    :raises SimpleBenchTypeError: If value is not a string.
    """
    return validate_string(
        value,
        'description',
        _EnvironmentInfoErrorTag.INVALID_DESCRIPTION,
        _EnvironmentInfoErrorTag.INVALID_DESCRIPTION,  # No separate value error since all strings are valid
        allow_empty=True,
        strip=True,
    )


_SEMANTIC_TYPE_RE: Final[re.Pattern[str]] = re.compile(
    r'^[A-Za-z0-9](?:[_A-Za-z0-9]*[A-Za-z0-9])?::[A-Za-z0-9](?:[_A-Za-z0-9]*[A-Za-z0-9])?$')
"""Regular expression pattern for validating semantic_type strings in the format 'namespace::type_name'."""


def semantic_type(value: str) -> str:
    """Validate semantic_type property.

    It is validated to be a string matching the pattern 'namespace::type_name'.

    :param str value: The semantic_type string to validate.
    :return str: The validated semantic_type string.
    :raises SimpleBenchTypeError: If value is not a string.
    :raises SimpleBenchValueError: If value does not match the required pattern.
    """
    return validate_string_with_regex(
        value,
        'semantic_type',
        _SEMANTIC_TYPE_RE,
        _EnvironmentInfoErrorTag.INVALID_SEMANTIC_TYPE_TYPE,
        _EnvironmentInfoErrorTag.INVALID_SEMANTIC_TYPE_VALUE,
        message='{name} must be in the format "namespace::type_name". Found: {value}',
    )


def hash_id(value: str) -> str:
    """Validate hash_id property.

    It is validated to be a 64-character hexadecimal string or an empty string.

    :param str value: The hash_id string to validate.
    :return str: The validated hash_id string.
    :raises SimpleBenchTypeError: If value is not a string.
    :raises SimpleBenchValueError: If value is not a 64-character hexadecimal string
    """
    hash_string = validate_string(
        value,
        'hash_id',
        _EnvironmentInfoErrorTag.INVALID_HASH_ID_TYPE,
        _EnvironmentInfoErrorTag.INVALID_HASH_ID_VALUE,
        allow_empty=True,
        strip=True,
    )
    if hash_string == '':
        return ''

    return validate_string_with_regex(
        hash_string,
        'hash_id',
        _HASH_RE,
        _EnvironmentInfoErrorTag.INVALID_HASH_ID_TYPE,
        _EnvironmentInfoErrorTag.INVALID_HASH_ID_VALUE,
        message='{name} must be 64-character hexadecimal string. Found: {value}',
    )

def data_as_core_data_mapping(data: Any, context: str) -> CoreDataMapping:
    """Validate that kwargs dictionary contains only core data mapping types."""
    return validate_core_data_mapping(data, context)

