"""Validation utility for hash ids

This module provides functions to validate the fields of a ValueBlock
according to the specifications defined for version 1 reports.

Each function checks the type and value constraints for a specific field,
returns the validated and correctly typed value, and raises appropriate
exceptions if the validation fails.
"""

import re

from simplebench.exceptions import ErrorTag, SimpleBenchValueError
from simplebench.validators import validate_string_with_regex

_HASH_ID_REGEX = re.compile(r'^(?:[a-f0-9]{64}|)$')
"""Validates the hash_id string.

An empty string is allowed, which indicates that the hash_id should be
computed automatically. Otherwise, the hash_id must be a valid 64-character hexadecimal string.
"""

__all__: list[str] = []


def validate_hash_id(val: str,
                     field_name: str,
                     type_error_tag: ErrorTag,
                     value_error_tag: ErrorTag,
                     *,
                     allow_empty: bool = True) -> str:
    """Validate the hash_id string.

    The hash_id must be a string that is either empty (if allow_empty is True)
    or a valid 64-character hexadecimal string.

    :param val: The unique hash identifier for the value information.
    :type val: str
    :param field_name: The name of the field being validated.
    :type field_name: str
    :param type_error_tag: The error tag to use if a type error occurs.
    :type type_error_tag: ErrorTag
    :param value_error_tag: The error tag to use if a value error occurs.
    :type value_error_tag: ErrorTag
    :param allow_empty: Whether to allow an empty string as a valid value. Defaults to True.
    :type allow_empty: bool
    :return: The validated hash_id string.
    :rtype: str
    :raises SimpleBenchTypeError: If the hash_id value is not a string.
    :raises SimpleBenchValueError: If the hash_id string is not a valid 64-character hexadecimal string
        (when not empty).
    """
    val = validate_string_with_regex(
        val, field_name, _HASH_ID_REGEX,
        type_error_tag,
        value_error_tag,
        message=f'{field_name} must be a valid 64-character hexadecimal string or an empty string'
    )
    if not allow_empty and val == '':
        raise SimpleBenchValueError(
            f"Empty string is not allowed for {field_name}",
            tag=value_error_tag)
    return val
