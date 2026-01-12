"""Validation functions for GenericEnvironment."""

import re
from typing import Any, Final

from simplebench.report._error_tags import _GenericEnvironmentErrorTag
from simplebench.types import ImmutableCoreDataMappingType
from simplebench.validators import validate_core_data_mapping, validate_string, validate_string_with_regex

_HASH_RE: Final[re.Pattern[str]] = re.compile(r'^[a-f0-9]{64}$')
"""Regular expression pattern for validating 64-character hexadecimal strings."""


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
        _GenericEnvironmentErrorTag.INVALID_HASH_ID_TYPE,
        _GenericEnvironmentErrorTag.INVALID_HASH_ID_VALUE,
        allow_empty=True,
        strip=True,
    )
    if hash_string == '':
        return ''

    return validate_string_with_regex(
        hash_string,
        'hash_id',
        _HASH_RE,
        _GenericEnvironmentErrorTag.INVALID_HASH_ID_TYPE,
        _GenericEnvironmentErrorTag.INVALID_HASH_ID_VALUE,
        message='{name} must be 64-character hexadecimal string. Found: {value}',
    )


def data_as_core_data_mapping(data: Any, context: str) -> ImmutableCoreDataMappingType:
    """Validate that kwargs dictionary contains only core data mapping types."""
    return validate_core_data_mapping(data, context, max_depth=5)
