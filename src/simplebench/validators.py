"""Utility functions for validating arguments to attribute setters and constructors.

These functions raise appropriate exceptions with error tags from exceptions.py
and return the validated and/or normalized value.
"""
from typing import Sequence

from .exceptions import SimpleBenchTypeError, SimpleBenchValueError, ErrorTag


def validate_non_blank_string(
        value: str,
        field_name: str,
        type_error_tag: ErrorTag,
        value_error_tag: ErrorTag) -> str:
    """Validate and normalize a non-blank string field.

    Any leading or trailing whitespace is stripped from the string before returning it.

    The validation checks that the value is a string and that it is not blank or only whitespace.
    The returned value is guaranteed to be non-blank and non-blank and to be of type str.

    Args:
        value (str): The string value to validate.
        field_name (str): The name of the field being validated (for error messages).
        type_error_tag (ErrorTag): The error tag to use for type errors.
        value_error_tag (ErrorTag): The error tag to use for value errors.

    Returns:
        str: The stripped string value.

    Raises:
        SimpleBenchTypeError: If the value is not a string.
        SimpleBenchValueError: If the string is blank or only whitespace.
    """
    if not isinstance(value, str):
        raise SimpleBenchTypeError(
            f'Invalid {field_name} type: {type(value)}. Must be a string.',
            tag=type_error_tag
        )
    stripped_value = value.strip()
    if not stripped_value:
        raise SimpleBenchValueError(
            f'Invalid {field_name}: cannot be blank or whitespace.',
            tag=value_error_tag
        )
    return stripped_value


def validate_non_blank_string_or_is_none(
        value: str | None,
        field_name: str,
        type_error_tag: ErrorTag,
        value_error_tag: ErrorTag,
        allow_none: bool = True) -> str | None:
    """Validate and normalize a non-blank string field.

    Any leading or trailing whitespace is stripped from the string before returning it.
    The validation checks that the value is a string and that it is not blank or only whitespace.
    If the value is None and allow_none is True, None is returned.

    The validated value is guaranteed to either be non-blank and non-blank and of type str, or
    None if allow_none is True and None is provided as the value.

    Args:
        value (str): The string value to validate.
        field_name (str): The name of the field being validated (for error messages).
        type_error_tag (ErrorTag): The error tag to use for type errors.
        value_error_tag (ErrorTag): The error tag to use for value errors.
        allow_none (bool): Whether to allow None as a valid value. Defaults to True.

    Returns:
        str | None: The stripped string value or None if allowed and provided.

    Raises:
        SimpleBenchTypeError: If the value is not a str, or None (if allow_none is False).
        SimpleBenchValueError: If the string is blank or only whitespace.
    """
    if value is None:
        if allow_none:
            return None
        raise SimpleBenchTypeError(
            f'Invalid {field_name}: cannot be None.',
            tag=value_error_tag
        )
    return validate_non_blank_string(value, field_name, type_error_tag, value_error_tag)


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

    Because this function checks for Sequence[int | float], it will accept lists, tuples, sets, and other
    sequence types, but not str or bytes.

    The type declaration for the value argument and return type is Sequence[int | float]
    to indicate that the sequence should contain a mix of ints and/or floats.

    Because this is a validation function, the actual type of the value argument can be
    and static type checkers may warn if the caller does not pass a value that is already
    declared as Sequence[int | float]. This is acceptable because the purpose of this
    function is to validate the type and contents of the value argument - the warnings
    from the type checkers are synergetic with the purpose of this function.

    Because the returned value is declared to be a Sequence of int or float, this
    has the effect of narrowing the type for callers that use type checkers.

    If you wish to suppress static type checker warnings for a specific call to this function,
    you can use a type: ignore[arg-type] comment on that line.

    Args:
        value (Sequence[int | float]): The sequence of values to validate.
        field_name (str): The name of the field being validated (for error messages).
        type_tag (ErrorTag): The error tag to use for type errors.
        value_tag (ErrorTag): The error tag to use for value errors.
        allow_empty (bool): Whether to allow a empty sequence. Defaults to True.

    Returns:
        Sequence[int | float]: The validated Sequence of numbers.

    Raises:
        SimpleBenchTypeError: If the value is not a sequence or contains non-numeric types.
        SimpleBenchValueError: If the sequence is empty and allow_empty is False.
    """
    if not isinstance(value, Sequence) or isinstance(value, str):
        raise SimpleBenchTypeError(
            f'Invalid {field_name} type: {type(value)}. Must be a sequence (list, tuple, etc.) of numbers.',
            tag=type_tag
        )
    if len(value) == 0 and not allow_empty:
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
