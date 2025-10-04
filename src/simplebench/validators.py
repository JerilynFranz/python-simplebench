"""Utility functions for validating arguments to attribute setters and constructors.

These functions raise appropriate exceptions with error tags from exceptions.py
and return the validated and/or normalized value.
"""
from typing import Sequence

from .exceptions import SimpleBenchTypeError, SimpleBenchValueError, ErrorTag


def validate_non_empty_string(
        value: str, field_name: str, type_error_tag: ErrorTag, value_error_tag: ErrorTag) -> str:
    """Validate and normalize a non-empty string field.

    Any leading or trailing whitespace is stripped from the string before returning it.

    Args:
        value (str): The string value to validate.
        field_name (str): The name of the field being validated (for error messages).
        type_error_tag (ErrorTag): The error tag to use for type errors.
        value_error_tag (ErrorTag): The error tag to use for value errors.

    Returns:
        str: The stripped string value.

    Raises:
        SimpleBenchTypeError: If the value is not a string.
        SimpleBenchValueError: If the string is empty or only whitespace.
    """
    if not isinstance(value, str):
        raise SimpleBenchTypeError(
            f'Invalid {field_name} type: {type(value)}. Must be a string.',
            tag=type_error_tag
        )
    if not value.strip():
        raise SimpleBenchValueError(
            f'Invalid {field_name}: cannot be empty or whitespace.',
            tag=value_error_tag
        )
    return value.strip()


def validate_int(value: int, field_name: str, type_tag: ErrorTag) -> int:
    """Validate that a value is an integer.

    Args:
        value (int): The value to validate.
        field_name (str): The name of the field being validated (for error messages).
        type_tag (ErrorTag): The error tag to use for type errors.

    Returns:
        int: The validated integer.

    Raises:
        SimpleBenchTypeError: If the value is not an integer.
    """
    if not isinstance(value, int):
        raise SimpleBenchTypeError(
            f'Invalid {field_name} type: {type(value)}. Must be an int.',
            tag=type_tag
        )
    return value


def validate_float(value: float | int, field_name: str, type_tag: ErrorTag) -> float:
    """Validate that a value is a float or integer.

    Validates that the value is either a float or an int.
    The return type is always a float.

    Args:
        value (float | int): The value to validate.
        field_name (str): The name of the field being validated (for error messages).
        type_tag (ErrorTag): The error tag to use for type errors.

    Returns:
        float: The validated float.

    Raises:
        SimpleBenchTypeError: If the value is not a float.
    """
    if not isinstance(value, (float, int)):  # Allow ints as valid floats
        raise SimpleBenchTypeError(
            f'Invalid {field_name} type: {type(value)}. Must be a float or int.',
            tag=type_tag
        )
    return float(value)


def validate_positive_int(value: int, field_name: str, type_tag: ErrorTag, value_tag: ErrorTag) -> int:
    """Validate that a value is a positive integer.

    Args:
        value (int): The value to validate.
        field_name (str): The name of the field being validated (for error messages).
        type_tag (ErrorTag): The error tag to use for type errors.
        value_tag (ErrorTag): The error tag to use for value errors.

    Returns:
        int: The validated positive integer.

    Raises:
        SimpleBenchTypeError: If the value is not an integer.
        SimpleBenchValueError: If the value is not positive.
    """
    if not isinstance(value, int):
        raise SimpleBenchTypeError(
            f'Invalid {field_name} type: {type(value)}. Must be an int.',
            tag=type_tag
        )
    if value <= 0:
        raise SimpleBenchValueError(
            f'Invalid {field_name}: must be a positive integer.',
            tag=value_tag
        )
    return value


def validate_non_negative_int(value: int, field_name: str, type_tag: ErrorTag, value_tag: ErrorTag) -> int:
    """Validate that a value is a non-negative integer.

    Args:
        value (int): The value to validate.
        field_name (str): The name of the field being validated (for error messages).
        type_tag (ErrorTag): The error tag to use for type errors.
        value_tag (ErrorTag): The error tag to use for value errors.

    Returns:
        int: The validated non-negative integer.

    Raises:
        SimpleBenchTypeError: If the value is not an integer.
        SimpleBenchValueError: If the value is negative.
    """
    if not isinstance(value, int):
        raise SimpleBenchTypeError(
            f'Invalid {field_name} type: {type(value)}. Must be an int.',
            tag=type_tag
        )
    if value < 0:
        raise SimpleBenchValueError(
            f'Invalid {field_name}: must be a non-negative integer.',
            tag=value_tag
        )
    return value


def validate_positive_float(
        value: float | int, field_name: str, type_tag: ErrorTag, value_tag: ErrorTag) -> float:
    """Validate that a value is a positive float or integer.

    Validates that the value is either a float or an int and that it is positive.
    The return type is always a float.

    Args:
        value (float | int): The value to validate.
        field_name (str): The name of the field being validated (for error messages).
        type_tag (ErrorTag): The error tag to use for type errors.
        value_tag (ErrorTag): The error tag to use for value errors.

    Returns:
        float: The validated positive float.

    Raises:
        SimpleBenchTypeError: If the value is not a float.
        SimpleBenchValueError: If the value is not positive.
    """
    if not isinstance(value, (float, int)):  # Allow ints as valid floats
        raise SimpleBenchTypeError(
            f'Invalid {field_name} type: {type(value)}. Must be a float or int.',
            tag=type_tag
        )
    if value <= 0.0:
        raise SimpleBenchValueError(
            f'Invalid {field_name}: must be a positive float or int.',
            tag=value_tag
        )
    return float(value)


def validate_non_negative_float(
        value: float | int, field_name: str, type_tag: ErrorTag, value_tag: ErrorTag) -> float:
    """Validate that a value is a non-negative float or integer.

    Validates that the value is either a float or an int and that it is non-negative.
    The return type is always a float.

    Args:
        value (float | int): The value to validate.
        field_name (str): The name of the field being validated (for error messages).
        type_tag (ErrorTag): The error tag to use for type errors.
        value_tag (ErrorTag): The error tag to use for value errors.

    Returns:
        float: The validated non-negative float.

    Raises:
        SimpleBenchTypeError: If the value is not a float.
        SimpleBenchValueError: If the value is negative.
    """
    if not isinstance(value, (float, int)):  # Allow ints as valid floats
        raise SimpleBenchTypeError(
            f'Invalid {field_name} type: {type(value)}. Must be a float or int.',
            tag=type_tag
        )
    if value < 0.0:
        raise SimpleBenchValueError(
            f'Invalid {field_name}: must be a non-negative float or int.',
            tag=value_tag
        )
    return float(value)


def validate_sequence_of_numbers(
        value: Sequence[int | float],
        field_name: str,
        type_tag: ErrorTag,
        value_tag: ErrorTag,
        allow_empty: bool = True) -> Sequence[int | float]:
    """Validate that a value is a sequence of numbers (ints or floats).

    Args:
        value (Sequence[int | float]): The sequence of values to validate.
        field_name (str): The name of the field being validated (for error messages).
        type_tag (ErrorTag): The error tag to use for type errors.
        value_tag (ErrorTag): The error tag to use for value errors.
        allow_empty (bool): Whether to allow an empty sequence. Defaults to True.

    Returns:
        Sequence[int | float]: The validated Sequence of numbers.

    Raises:
        SimpleBenchTypeError: If the value is not a sequence or contains non-numeric types.
        SimpleBenchValueError: If the sequence is empty.
    """
    if not isinstance(value, Sequence) or isinstance(value, str):
        raise SimpleBenchTypeError(
            f'Invalid {field_name} type: {type(value)}. Must be a sequence (list, tuple, etc.) of numbers.',
            tag=type_tag
        )
    if not value and not allow_empty:
        raise SimpleBenchValueError(
            f'Invalid {field_name}: sequence cannot be empty.',
            tag=value_tag
        )
    for i, item in enumerate(value):
        if not isinstance(item, (int, float)):
            raise SimpleBenchTypeError(
                f'Invalid {field_name} element at index {i}: {type(item)}. Must be an int or float.',
                tag=type_tag
            )
    return value
