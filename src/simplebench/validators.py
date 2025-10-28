"""Utility functions for validating arguments to attribute setters and constructors.

These functions raise appropriate exceptions with error tags from exceptions.py
and return the validated and/or normalized value.
"""
from pathlib import Path
from typing import Any, cast, TypeVar, Sequence, Iterable, overload

from .exceptions import SimpleBenchTypeError, SimpleBenchValueError, ErrorTag, ValidatorsErrorTag


T = TypeVar('T')


def validate_type(*, value: Any, expected: type[T], name: str, error_tag: ErrorTag) -> T:
    """Validate that a value is of the expected type.

    The returned value is guaranteed to be of type expected and acts to type-narrow
    the returned value.

    Args:
        value (Any): The value to validate.
        expected (type[T]): The expected type of the value.
        name (str): The name of the field being validated (for error messages).
        error_tag (ErrorTag): The error tag to use for type errors.

    Returns:
        T: The validated value of type T.

    Raises:
        SimpleBenchTypeError: If the value is not of the expected type.
    """
    if not isinstance(expected, type):
        raise SimpleBenchTypeError(
            f'Invalid expected argument type: {type(expected)}. Must be a type.',
            tag=ValidatorsErrorTag.VALIDATE_TYPE_INVALID_EXPECTED_ARG_TYPE
        )
    if not isinstance(name, str):
        raise SimpleBenchTypeError(
            f'Invalid name argument type: {type(name)}. Must be a str.',
            tag=ValidatorsErrorTag.VALIDATE_TYPE_INVALID_NAME_ARG_TYPE
        )
    if not isinstance(value, expected):
        raise SimpleBenchTypeError(
            f'Invalid "{name}" type: {type(value)}. Must be {expected.__name__}.',
            tag=error_tag
        )
    return cast(T, value)


def validate_string(
        value: Any,
        field_name: str,
        type_error_tag: ErrorTag,
        value_error_tag: ErrorTag,
        strip: bool = True,
        allow_empty: bool = True,
        allow_blank: bool = True,
        alphanumeric_only: bool = False) -> str:
    """Validate and normalize a string field.

    Validates that the value is a string. Optionally strips leading/trailing whitespace,
    checks for emptiness, blankness (whitespace-only strings), and alphanumeric content.

    The returned value is guaranteed to be of type str and acts to type-narrow
    the returned value.

    The following combinations of options conflict with each other and will raise a
    SimpleBenchValueError if set together:

    - `strip=True, allow_blank=True, allow_empty=False`
        This conflicts because stripping leading/trailing whitespace turns blank strings
        into empty strings - and allow_empty=False forbids empty strings.

        This implies that any string that consists only of whitespace
        would be invalid, which contradicts the allow_blank=True option.
    - `strip=False, allow_blank=True, alphanumeric_only=True`
        Allowing unstripped blank strings while requiring alphanumeric-only is contradictory.
        Blank strings contain no alphanumeric characters. Without stripping, blank strings
        consisting only of whitespace will still contain that whitespace and so cannot satisfy both
        the alphanumeric only condition AND the allow blank condition.

        This could result in subtle bugs.

    Explanation of options:
        strip=True means leading/trailing whitespace is removed before other checks.
        allow_empty=False means the string cannot be empty ("").
        allow_blank=False means the string cannot be empty or consist only of whitespace.
        alphanumeric_only=True means the string only contain alphanumeric characters (a-z, A-Z, 0-9).

    Args:
        value (Any): The value to validate as being a string.
        field_name (str): The name of the field being validated (for error messages).
        type_error_tag (ErrorTag): The error tag to use for type errors.
        value_error_tag (ErrorTag): The error tag to use for value errors.
        strip (bool, default=True): Whether to strip leading/trailing whitespace.
        allow_empty (bool, default=True): Whether to allow empty strings.
        allow_blank (bool, default=True): Whether to allow blank strings (strings that consist only of whitespace).
        alphanumeric_only (bool, default=False): Whether to allow only alphanumeric characters.

    Raises:
        SimpleBenchTypeError: If the value is not a str.
        SimpleBenchValueError: If the string fails any of the specified checks or if options contradict.
    """
    if not isinstance(strip, bool):
        raise SimpleBenchTypeError(
            f'Invalid strip type: {type(strip)}. Must be a bool.',
            tag=ValidatorsErrorTag.INVALID_STRIP_ARG_TYPE
        )
    if not isinstance(allow_empty, bool):
        raise SimpleBenchTypeError(
            f'Invalid allow_empty type: {type(allow_empty)}. Must be a bool.',
            tag=ValidatorsErrorTag.INVALID_ALLOW_EMPTY_ARG_TYPE
        )
    if not isinstance(allow_blank, bool):
        raise SimpleBenchTypeError(
            f'Invalid allow_blank type: {type(allow_blank)}. Must be a bool.',
            tag=ValidatorsErrorTag.INVALID_ALLOW_BLANK_ARG_TYPE
        )
    if not isinstance(alphanumeric_only, bool):
        raise SimpleBenchTypeError(
            f'Invalid alphanumeric_only type: {type(alphanumeric_only)}. Must be a bool.',
            tag=ValidatorsErrorTag.INVALID_ALPHANUMERIC_ONLY_ARG_TYPE
        )
    if allow_blank:
        if strip and not allow_empty:
            raise SimpleBenchValueError(
                'Conflicting options: cannot have strip=True, allow_blank=True, and allow_empty=False together.',
                tag=ValidatorsErrorTag.CONFLICTING_STRING_VALIDATION_OPTIONS_ALLOW_EMPTY
            )
        if alphanumeric_only and not strip:
            raise SimpleBenchValueError(
                'Conflicting options: cannot have strip=False, allow_blank=True, and alphanumeric_only=True together.',
                tag=ValidatorsErrorTag.CONFLICTING_STRING_VALIDATION_OPTIONS_ALPHANUMERIC_ONLY
            )
    if not isinstance(value, str):
        raise SimpleBenchTypeError(
            f'Invalid {field_name} type: {type(value)}. Must be a str.',
            tag=type_error_tag
        )
    if strip:
        value = value.strip()

    if not allow_empty and value == '':
        raise SimpleBenchValueError(
            f'Invalid {field_name}: cannot be empty string.',
            tag=value_error_tag
        )

    if not allow_blank and value.strip() == '':
        raise SimpleBenchValueError(
            f'Invalid {field_name}: cannot be blank string (consist only of whitespace).',
            tag=value_error_tag
        )

    # isalnum returns False for empty strings, so we only check it if not allow_empty
    # or the string is not empty
    if (not allow_empty or value != '') and alphanumeric_only and not value.isalnum():
        raise SimpleBenchValueError(
            f'Invalid {field_name}: must consist only of alphanumeric characters [A-Za-z0-9]: "{value}".',
            tag=value_error_tag
        )

    return value


def validate_non_blank_string(
        value: Any,
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
        value: Any,
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


def validate_int(value: Any, field_name: str, type_tag: ErrorTag) -> int:
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


def validate_float(value: Any, field_name: str, type_tag: ErrorTag) -> float:
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


def validate_positive_int(value: Any, field_name: str, type_tag: ErrorTag, value_tag: ErrorTag) -> int:
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


def validate_non_negative_int(value: Any, field_name: str, type_tag: ErrorTag, value_tag: ErrorTag) -> int:
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
        value: Any, field_name: str, type_tag: ErrorTag, value_tag: ErrorTag) -> float:
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


@overload
def validate_sequence_of_type(
        value: Sequence[Any],
        types: type[T],
        field_name: str,
        type_tag: ErrorTag,
        value_tag: ErrorTag,
        allow_empty: bool = True) -> list[T]: ...


@overload
def validate_sequence_of_type(
        value: Sequence[Any],
        types: tuple[type, ...],
        field_name: str,
        type_tag: ErrorTag,
        value_tag: ErrorTag,
        allow_empty: bool = True) -> list[Any]: ...


def validate_sequence_of_type(
        value: Sequence[Any],
        types: type[T] | tuple[type, ...],
        field_name: str,
        type_tag: ErrorTag,
        value_tag: ErrorTag,
        allow_empty: bool = True) -> list[T] | list[Any]:
    """Validate that a value is a sequence of specified type(s).

    When a single type is provided, the return type is automatically inferred as list[T].
    When multiple types are provided, the return type is list[Any], which allows the
    caller to narrow the type with an explicit annotation.

    Args:
        value (Sequence[Any]): The sequence of values to validate.
        types (type[T] | tuple[type, ...]): A single type or tuple of allowed types.
        field_name (str): The name of the field being validated (for error messages).
        type_tag (ErrorTag): The error tag to use for type errors.
        value_tag (ErrorTag): The error tag to use for value errors.
        allow_empty (bool): Whether to allow an empty sequence. Defaults to True.

    Returns:
        list[T] | list[Any]: For single type, returns list[T]. For multiple types,
            returns list[Any] which can be narrowed with explicit type annotation.

    Raises:
        SimpleBenchTypeError: If the value is not a sequence or contains invalid types.
        SimpleBenchValueError: If the sequence is empty and allow_empty is False.

    Examples:
        Single type (automatic inference):
            names = validate_sequence_of_type(['Alice'], str, 'names', ...)
            # Type: list[str]

        Multiple types (manual narrowing):
            mixed: list[str | int] = validate_sequence_of_type(
                ['a', 1], (str, int), 'items', ...
            )
            # Type: list[str | int]
    """
    if not isinstance(value, Sequence) or isinstance(value, str):
        raise SimpleBenchTypeError(
            f'Invalid {field_name} type: {type(value).__name__}. '
            f'Must be a sequence (list, tuple, etc.).',
            tag=type_tag
        )

    if len(value) == 0 and not allow_empty:
        raise SimpleBenchValueError(
            f'Invalid {field_name}: sequence cannot be empty.',
            tag=value_tag
        )

    # Format type names for error messages
    if isinstance(types, tuple):
        type_names = ' or '.join(t.__name__ for t in types)
    else:
        type_names = types.__name__

    result: list[Any] = []
    for i, item in enumerate(value):
        if not isinstance(item, types):
            raise SimpleBenchTypeError(
                f'Invalid {field_name} element at index {i}: {type(item).__name__}. '
                f'Must be {type_names}.',
                tag=type_tag
            )
        result.append(item)

    return result


@overload
def validate_iterable_of_type(
        value: Iterable[Any],
        types: type[T],
        field_name: str,
        type_tag: ErrorTag,
        value_tag: ErrorTag,
        allow_empty: bool = True) -> list[T]: ...


@overload
def validate_iterable_of_type(
        value: Iterable[Any],
        types: tuple[type, ...],
        field_name: str,
        type_tag: ErrorTag,
        value_tag: ErrorTag,
        allow_empty: bool = True) -> list[Any]: ...


def validate_iterable_of_type(
        value: Iterable[Any],
        types: type[T] | tuple[type, ...],
        field_name: str,
        type_tag: ErrorTag,
        value_tag: ErrorTag,
        allow_empty: bool = True) -> list[T] | list[Any]:
    """Validate that a value is an iterable of specified type(s).

    When a single type is provided, the return type is automatically inferred as list[T].
    When multiple types are provided, the return type is list[Any], which allows the
    caller to narrow the type with an explicit annotation.

    Args:
        value (Iterable[Any]): The iterable of values to validate.
        types (type[T] | tuple[type, ...]): A single type or tuple of allowed types.
        field_name (str): The name of the field being validated (for error messages).
        type_tag (ErrorTag): The error tag to use for type errors.
        value_tag (ErrorTag): The error tag to use for value errors.
        allow_empty (bool): Whether to allow an empty iterable. Defaults to True.

    Returns:
        list[T] | list[Any]: For single type, returns list[T]. For multiple types,
            returns list[Any] which can be narrowed with explicit type annotation.

    Raises:
        SimpleBenchTypeError: If the value is not an iterable or contains invalid types.
        SimpleBenchValueError: If the iterable is empty and allow_empty is False.

    Examples:
        Single type (automatic inference):
            names = validate_iterable_of_type(['Alice'], str, 'names', ...)
            # Type: list[str]

        Multiple types (manual narrowing):
            mixed: list[str | int] = validate_iterable_of_type(
                ['a', 1], (str, int), 'items', ...
            )
            # Type: list[str | int]
    """
    if not isinstance(value, Iterable) or isinstance(value, str):
        raise SimpleBenchTypeError(
            f'Invalid {field_name} type: {type(value).__name__}. '
            f'Must be an iterable (list, tuple, etc.).',
            tag=type_tag
        )

    value = list(value)  # Convert to list for length check and indexing

    if len(value) == 0 and not allow_empty:
        raise SimpleBenchValueError(
            f'Invalid {field_name}: sequence cannot be empty.',
            tag=value_tag
        )

    # Format type names for error messages
    if isinstance(types, tuple):
        type_names = ' or '.join(t.__name__ for t in types)
    else:
        type_names = types.__name__

    result: list[Any] = []
    for i, item in enumerate(value):
        if not isinstance(item, types):
            raise SimpleBenchTypeError(
                f'Invalid {field_name} element at index {i}: {type(item).__name__}. '
                f'Must be {type_names}.',
                tag=type_tag
            )
        result.append(item)

    return result


@overload
def validate_frozenset_of_type(
        value: frozenset[Any],
        types: type[T],
        field_name: str,
        type_tag: ErrorTag,
        value_tag: ErrorTag,
        allow_empty: bool = True) -> frozenset[T]: ...


@overload
def validate_frozenset_of_type(
        value: frozenset[Any],
        types: tuple[type, ...],
        field_name: str,
        type_tag: ErrorTag,
        value_tag: ErrorTag,
        allow_empty: bool = True) -> frozenset[Any]: ...


def validate_frozenset_of_type(
        value: frozenset[Any],
        types: type[T] | tuple[type, ...],
        field_name: str,
        type_tag: ErrorTag,
        value_tag: ErrorTag,
        allow_empty: bool = True) -> frozenset[T] | frozenset[Any]:
    """Validate that a value is a frozenset of specified type(s).

    When a single type is provided, the return type is automatically inferred as frozenset[T].
    When multiple types are provided, the return type is frozenset[Any], which allows the
    caller to narrow the type with an explicit annotation.

    Single type (automatic type inference) example:

        friends_names: frozenset[str] = frozenset(['Alice', 'Bob'])
        names = validate_frozenset_of_type(
            friends_names, str, 'names',
            ErrorTag.SOME_TYPE_TAG,
            ErrorTag.SOME_VALUE_TAG,
            allow_empty=False
        )
        # Type: frozenset[str]

    Multiple types (manual narrowing) example:

        mixed_values: frozenset[str | int] = frozenset(['a', 1, 'b', 2])
        mixed: frozenset[str | int] = validate_frozenset_of_type(
            mixed_values, (str, int), 'items',
            ErrorTag.SOME_TYPE_TAG,
            ErrorTag.SOME_VALUE_TAG,
            allow_empty=True)
        # Type: frozenset[str | int]

    Args:
        value (Any): The frozenset of values to validate.
        types (type[T] | tuple[type, ...]): A single type or tuple of allowed types.
        field_name (str): The name of the field being validated (for error messages).
        type_tag (ErrorTag): The error tag to use for type errors.
        value_tag (ErrorTag): The error tag to use for value errors.
        allow_empty (bool): Whether to allow an empty iterable. Defaults to True.

    Returns:
        frozenset:
            For single type, returns `frozenset[T]`. For multiple types, returns `frozenset[Any]`
            which can be narrowed with explicit type annotation.

    Raises:
        SimpleBenchTypeError: If the value is not a frozenset or contains invalid types.
        SimpleBenchValueError: If the frozenset is empty and allow_empty is False.
    """
    if not isinstance(value, frozenset):
        raise SimpleBenchTypeError(
            f'Invalid {field_name} type: {type(value).__name__}. '
            f'Must be a frozenset.',
            tag=type_tag
        )

    if len(value) == 0 and not allow_empty:
        raise SimpleBenchValueError(
            f'Invalid {field_name}: sequence cannot be empty.',
            tag=value_tag
        )

    # Format type names for error messages
    if isinstance(types, tuple):
        type_names = ' or '.join(t.__name__ for t in types)
    else:
        type_names = types.__name__

    for i, item in enumerate(value):
        if not isinstance(item, types):
            raise SimpleBenchTypeError(
                f'Invalid {field_name} element at index {i}: {type(item).__name__}. '
                f'Must be {type_names}.',
                tag=type_tag
            )
    result: frozenset[T] = frozenset(value)
    # Return the now validated frozenset
    return result


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


def validate_sequence_of_str(
        value: Any,
        field_name: str,
        type_tag: ErrorTag,
        value_tag: ErrorTag,
        allow_empty: bool = True,
        allow_blank: bool = True,
        allow_whitespace: bool = True) -> list[str]:
    """Validate that a value is a sequence of strings.

    This function checks that the input is a sequence (list, tuple, etc.) of strings,
    and that each string meets the specified criteria.

    It can enforce that the sequence is not empty, and that individual strings are not blank
    or do not contain any whitespace, based on the provided flags.

    Args:
        value (Sequence[Any]): The sequence of values to validate.
        field_name (str): The name of the field being validated (for error messages).
        type_tag (ErrorTag): The error tag to use for type errors.
        value_tag (ErrorTag): The error tag to use for value errors.
        allow_empty (bool): Whether to allow an empty sequence. Defaults to True.
        allow_blank (bool): Whether to allow blank strings in the sequence. Defaults to True.
        allow_whitespace (bool): Whether to allow strings that contain whitespace. Defaults to True.

    Returns:
        list[str]: The validated list of strings.

    Raises:
        SimpleBenchTypeError: If the value is not a sequence or contains non-string types.
        SimpleBenchValueError: If the sequence is empty and allow_empty is False or an element is
                blank and allow_blank is False.
    """
    list_of_str: list[str] = validate_sequence_of_type(
                                value, str,
                                field_name,
                                type_tag,
                                value_tag,
                                allow_empty)
    if not allow_blank:
        for i, item in enumerate(list_of_str):
            if item.strip() == '':
                raise SimpleBenchValueError(
                    f'Invalid {field_name} element at index {i}: cannot be blank or whitespace.',
                    tag=value_tag
                )
    if not allow_whitespace:
        for i, item in enumerate(list_of_str):
            if any(c.isspace() for c in item):
                raise SimpleBenchValueError(
                    f'Invalid {field_name} element at index {i}: cannot contain whitespace characters.',
                    tag=value_tag
                )
    return list_of_str


def validate_int_range(number: Any,
                       field_name: str,
                       type_tag: ErrorTag,
                       value_tag: ErrorTag,
                       min_value: int,
                       max_value: int) -> int:
    """Validate that a value is an integer within a specified range.

    Args:
        number (Any): The value to validate.
        field_name (str): The name of the field being validated (for error messages).
        type_tag (ErrorTag): The error tag to use for type errors.
        value_tag (ErrorTag): The error tag to use for value errors.
        min_value (int): The minimum value of the range.
        max_value (int): The maximum value of the range.

    Raises:
        SimpleBenchValueError: If min_value is greater than max_value.
        SimpleBenchTypeError: If field_name is not a str.
        SimpleBenchTypeError: If type_tag or value_tag is not an ErrorTag.
        SimpleBenchTypeError: If number, min_value, or max_value is not an int.
        SimpleBenchValueError: If number is not within the specified range.
    """
    if not isinstance(field_name, str):
        raise SimpleBenchTypeError(
            f'Invalid call to validate_int_range: field_name type: {type(field_name)}. Must be a str.',
            tag=ValidatorsErrorTag.INVALID_FIELD_NAME_TYPE)
    if not isinstance(min_value, int):
        raise SimpleBenchTypeError(
            f'Invalid call to validate_int_range: min_value type {type(min_value)}. Must be an int.',
            tag=ValidatorsErrorTag.INVALID_MIN_VALUE_TYPE)
    if not isinstance(max_value, int):
        raise SimpleBenchTypeError(
            f'Invalid call to validate_int_range: max_value type {type(max_value)}. Must be an int.',
            tag=ValidatorsErrorTag.INVALID_MAX_VALUE_TYPE)
    if min_value > max_value:
        raise SimpleBenchValueError(
            f'Invalid call to validate_int_range: min_value ({min_value}) '
            f'cannot be greater than max_value ({max_value}).',
            tag=ValidatorsErrorTag.INVALID_RANGE)
    if not isinstance(number, int):
        raise SimpleBenchTypeError(
            f'Invalid {field_name} type: {type(number)}. Must be an int.',
            tag=type_tag)
    if not min_value <= number <= max_value:
        raise SimpleBenchValueError(
            f'Invalid {field_name}: {number}. Must be an int between {min_value} and {max_value}, inclusive.',
            tag=value_tag)

    return number


def validate_float_range(
        number: Any,
        field_name: str,
        type_tag: ErrorTag,
        value_tag: ErrorTag,
        min_value: float,
        max_value: float) -> float:
    """Validate that a value is a float within a specified range.

    Args:
        number (float): The value to validate.
        field_name (str): The name of the field being validated (for error messages).
        type_tag (ErrorTag): The error tag to use for type errors.
        value_tag (ErrorTag): The error tag to use for value errors.
        min_value (float): The minimum value of the range.
        max_value (float): The maximum value of the range.

    Raises:
        SimpleBenchValueError: If min_value is greater than max_value.
        SimpleBenchTypeError: If field_name is not a str.
        SimpleBenchTypeError: If type_tag or value_tag is not an ErrorTag.
        SimpleBenchTypeError: If number, min_value, or max_value is not a float..
        SimpleBenchValueError: If number is not within the specified range.
    """
    if not isinstance(field_name, str):
        raise SimpleBenchTypeError(
            f'Invalid call to validate_float_range: field_name type: {type(field_name)}. Must be a str.',
            tag=ValidatorsErrorTag.INVALID_FIELD_NAME_TYPE)
    if not isinstance(min_value, float):
        raise SimpleBenchTypeError(
            f'Invalid call to validate_float_range: min_value type {type(min_value)}. Must be a float.',
            tag=ValidatorsErrorTag.INVALID_MIN_VALUE_TYPE)
    if not isinstance(max_value, float):
        raise SimpleBenchTypeError(
            f'Invalid call to validate_float_range: max_value type {type(max_value)}. Must be a float.',
            tag=ValidatorsErrorTag.INVALID_MAX_VALUE_TYPE)
    if min_value > max_value:
        raise SimpleBenchValueError(
            f'Invalid call to validate_float_range: min_value ({min_value}) '
            f'cannot be greater than max_value ({max_value}).',
            tag=ValidatorsErrorTag.INVALID_RANGE)
    if not isinstance(number, float):
        raise SimpleBenchTypeError(
            f'Invalid {field_name} type: {type(number)}. Must be a float.',
            tag=type_tag)
    if not min_value <= number <= max_value:
        raise SimpleBenchValueError(
            f'Invalid {field_name}: {number}. Must be a float between {min_value} and {max_value}, inclusive.',
            tag=value_tag)

    return number


def validate_filename(filename: Any) -> str:
    """Validate a filename for use in the filesystem.

    It validates that:
        - The filename is a string.
        - The filename suffix (if present) is alphanumeric and no longer than 10 characters.
        - The filename stem (name without suffix) is alphanumeric and at least one character long.
        - The total filename length does not exceed 255 characters.

    Args:
        filename (str): The filename to validate.

    Returns:
        str: The validated filename.

    Raises:
        SimpleBenchTypeError: If the filename is not a string.
        SimpleBenchValueError: If the filename is invalid.
    """
    filename = validate_type(
        value=filename, expected=str, name='filename',
        error_tag=ValidatorsErrorTag.VALIDATE_FILENAME_INVALID_FILENAME_ARG_TYPE)

    file = Path(filename)
    file_suffix = file.suffix.replace('.', '')
    if file_suffix != '' and len(file_suffix) > 10:
        raise SimpleBenchValueError(
            f"Filename suffix cannot be longer than 10 characters (passed suffix was '{file_suffix}')",
            tag=ValidatorsErrorTag.VALIDATE_FILENAME_SUFFIX_TOO_LONG)
    if file_suffix != '' and not file_suffix.isalnum():
        raise SimpleBenchValueError(
            "Filename suffix must be alphanumeric (contain only A-Z, a-z, 0-9)",
            tag=ValidatorsErrorTag.VALIDATE_FILENAME_SUFFIX_NOT_ALPHANUMERIC)
    file_stem = file.stem
    if file_stem == '':
        raise SimpleBenchValueError(
            "Filename must have a valid stem (name without suffix)",
            tag=ValidatorsErrorTag.VALIDATE_FILENAME_INVALID_STEM)
    if not file_stem.isalnum():
        raise SimpleBenchValueError(
            "Filename stem (name without suffix) must be alphanumeric "
            "contain at least one character and only contain characters from A-Z, a-z, 0-9)",
            tag=ValidatorsErrorTag.VALIDATE_FILENAME_STEM_NOT_ALPHANUMERIC)
    if len(filename) > 255:
        raise SimpleBenchValueError(
            f"Filename cannot be longer than 255 characters (passed filename was '{filename}')",
            tag=ValidatorsErrorTag.VALIDATE_FILENAME_TOO_LONG)
    return filename
