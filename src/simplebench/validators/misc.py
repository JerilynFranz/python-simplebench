"""Utility functions for validating arguments to attribute setters and constructors.

These functions raise appropriate exceptions with error tags from exceptions.py
and return the validated and/or normalized value.
"""

import re
from collections.abc import Sequence
from pathlib import Path
from typing import Any, TypeVar, overload

from simplebench.exceptions import ErrorTag, SimpleBenchTypeError, SimpleBenchValueError
from simplebench.validators._error_tags import _ValidatorsErrorTag

T = TypeVar('T')


@overload
def validate_bool(value: Any, name: str, error_tag: ErrorTag) -> bool:
    """Validate that the passed value is either a boolean (bool) value.

        (validation primitive - does not depend on other validators)

    If the value passes, type checkers will annotate the returned value
    as `bool`.

    :param value: The value being validated
    :param str name: The field name for the value
    :param ErrorTag error_tag: The ErrorTag to be used if it fails the validation
    :return: The validated boolean value.
    :rtype: bool
    :raises SimpleBenchTypeError: If the value is not a boolean.
    """


@overload
def validate_bool(value: Any, name: str, error_tag: ErrorTag, *, allow_none: bool) -> bool | None:
    """Validate that the passed value is either a bool or None.

        (validation primitive - does not depend on other validators)

    If the value passes, type checkers will annotate the returned value
    as `bool | None`.

    :param value: The value being validated
    :param str name: The field name for the value
    :param ErrorTag error_tag: The ErrorTag to be used if it fails the validation
    :param bool allow_none: If None should be allowed.
    :return: The validated boolean value or None.
    :rtype: bool | None
    :raises SimpleBenchTypeError: If the value is not a boolean or None.
    """


def validate_bool(value: Any, name: str, error_tag: ErrorTag, *, allow_none: bool = False) -> bool | None:
    """Validate that a value is a boolean.

            (validation primitive - does not depend on other validators)

    If allow_none is True, None is also accepted.

    If the allow_none parameter is not provided, it defaults to False and
    only boolean values are accepted. In that case, the return type is guaranteed
    to be bool and type checkers will accept it as bool for type narrowing.

    :param Any value: The value to validate.
    :param str name: The name of the field being validated (for error messages).
    :param ErrorTag error_tag: The error tag to use for type errors.
    :param bool allow_none: Whether to allow None as a valid value.
    :return: The validated boolean or None if allowed and provided.
    :rtype: bool | None
    :raises SimpleBenchTypeError:
        - If the value is not a boolean and allow_none==False
        - If the value is not a boolean or None and allow_none==True
        - If name is not a str
        - If error_tag is not an ErrorTag
        - If allow_none is not a bool
    """
    if not isinstance(name, str):
        raise SimpleBenchTypeError(
            f'Invalid name argument type: {type(name)}. Must be a str.',
            tag=_ValidatorsErrorTag.VALIDATE_BOOL_INVALID_NAME_ARG_TYPE,
        )
    if not isinstance(error_tag, ErrorTag):
        raise SimpleBenchTypeError(
            f'Invalid error_tag argument type: {type(error_tag)}. Must be an ErrorTag.',
            tag=_ValidatorsErrorTag.VALIDATE_BOOL_INVALID_ERROR_TAG_TYPE,
        )
    if not isinstance(allow_none, bool):
        raise SimpleBenchTypeError(
            f'Invalid allow_none argument type: {type(allow_none)}. Must be a bool.',
            tag=_ValidatorsErrorTag.VALIDATE_BOOL_INVALID_ALLOW_NONE_ARG_TYPE,
        )

    if not isinstance(value, bool):
        if allow_none:  # bool | None branch for not a bool
            if value is None:
                return None
            raise SimpleBenchTypeError(f'Invalid {name} type: {type(value)}. Must be a bool or None.', tag=error_tag)
        # bool-only branch for not a bool
        raise SimpleBenchTypeError(f'Invalid {name} type: {type(value)}. Must be a bool.', tag=error_tag)

    return value


def validate_int(value: Any, name: str, type_tag: ErrorTag) -> int:
    """Validate that a value is an integer.

        (validation primitive - does not depend on other validators)

    :param int value: The value to validate.
    :param str name: The name of the field being validated (for error messages).
    :param ErrorTag type_tag: The error tag to use for type errors.
    :return: The validated integer.
    :rtype: int
    :raises SimpleBenchTypeError: If the value is not an integer.
    """
    if not isinstance(value, int):
        raise SimpleBenchTypeError(f'Invalid {name} type: {type(value)}. Must be an int.', tag=type_tag)
    return value


def validate_float(value: Any, name: str, type_tag: ErrorTag) -> float:
    """Validate that a value is a float or integer.

            (validation primitive - does not depend on other validators)

    Validates that the value is either a float or an int.
    The return type is always a float.

    :param float | int value: The value to validate.
    :param str field_name: The name of the field being validated (for error messages).
    :param ErrorTag type_tag: The error tag to use for type errors.
    :return: The validated float.
    :rtype: float
    :raises SimpleBenchTypeError: If the value is not a float or int.
    :raises SimpleBenchValueError: If the value is NaN or infinite.
    """
    if not isinstance(value, (float, int)):  # Allow ints as valid floats
        raise SimpleBenchTypeError(f'Invalid {name} type: {type(value)}. Must be a float or int.', tag=type_tag)
    value = float(value)
    if value != value or value == float('inf') or value == float('-inf'):
        raise SimpleBenchValueError(f'Invalid {name} value: {value}. Must be a finite number.',
                                    tag=type_tag)
    return value


def validate_positive_int(value: Any, field_name: str, type_tag: ErrorTag, value_tag: ErrorTag) -> int:
    """Validate that a value is a positive integer.

        (validation primitive - does not depend on other validators)

    :param int value: The value to validate.
    :param str field_name: The name of the field being validated (for error messages).
    :param ErrorTag type_tag: The error tag to use for type errors.
    :param ErrorTag value_tag: The error tag to use for value errors.
    :return: The validated positive integer.
    :rtype: int
    :raises SimpleBenchTypeError: If the value is not an integer.
    :raises SimpleBenchValueError: If the value is not positive.
    """
    if not isinstance(value, int):
        raise SimpleBenchTypeError(f'Invalid {field_name} type: {type(value)}. Must be an int.', tag=type_tag)
    if value <= 0:
        raise SimpleBenchValueError(f'Invalid {field_name}: must be a positive integer.', tag=value_tag)
    return value


def validate_non_negative_int(value: Any, field_name: str, type_tag: ErrorTag, value_tag: ErrorTag) -> int:
    """Validate that a value is a non-negative integer.

        (validation primitive - does not depend on other validators)

    :param int value: The value to validate.
    :param str field_name: The name of the field being validated (for error messages).
    :param ErrorTag type_tag: The error tag to use for type errors.
    :param ErrorTag value_tag: The error tag to use for value errors.
    :return: The validated non-negative integer.
    :rtype: int
    :raises SimpleBenchTypeError: If the value is not an integer.
    :raises SimpleBenchValueError: If the value is negative.
    """
    if not isinstance(value, int):
        raise SimpleBenchTypeError(f'Invalid {field_name} type: {type(value)}. Must be an int.', tag=type_tag)
    if value < 0:
        raise SimpleBenchValueError(f'Invalid {field_name}: must be a non-negative integer.', tag=value_tag)
    return value


def validate_positive_float(value: Any, field_name: str, type_tag: ErrorTag, value_tag: ErrorTag) -> float:
    """Validate that a value is a positive float or integer.

    Validates that the value is either a float or an int and that it is positive.
    The return type is always a float.

    :param float | int value: The value to validate.
    :param str field_name: The name of the field being validated (for error messages).
    :param ErrorTag type_tag: The error tag to use for type errors.
    :param ErrorTag value_tag: The error tag to use for value errors.
    :return: The validated positive float.
    :rtype: float
    :raises SimpleBenchTypeError: If the value is not a float.
    :raises SimpleBenchValueError: If the value is not positive.
    """
    if not isinstance(value, (float, int)):  # Allow ints as valid floats
        raise SimpleBenchTypeError(f'Invalid {field_name} type: {type(value)}. Must be a float or int.', tag=type_tag)
    if value <= 0.0:
        raise SimpleBenchValueError(f'Invalid {field_name}: must be a positive float or int.', tag=value_tag)
    return float(value)


def validate_non_negative_float(value: float | int, field_name: str, type_tag: ErrorTag, value_tag: ErrorTag) -> float:
    """Validate that a value is a non-negative float or integer.

        (validation primitive - does not depend on other validators)

    Validates that the value is either a float or an int and that it is non-negative.
    The return type is always a float.

    :param float | int value: The value to validate.
    :param str field_name: The name of the field being validated (for error messages).
    :param ErrorTag type_tag: The error tag to use for type errors.
    :param ErrorTag value_tag: The error tag to use for value errors.
    :return: The validated non-negative float.
    :rtype: float
    :raises SimpleBenchTypeError: If the value is not a float.
    :raises SimpleBenchValueError: If the value is negative.
    """
    if not isinstance(value, (float, int)):  # Allow ints as valid floats
        raise SimpleBenchTypeError(f'Invalid {field_name} type: {type(value)}. Must be a float or int.', tag=type_tag)
    if value < 0.0:
        raise SimpleBenchValueError(f'Invalid {field_name}: must be a non-negative float or int.', tag=value_tag)
    return float(value)


@overload
def validate_sequence_of_type(
    value: Any, types: type[T], field_name: str, type_tag: ErrorTag, value_tag: ErrorTag, *, allow_empty: bool = True
) -> list[T]: ...


@overload
def validate_sequence_of_type(
    value: Any,
    types: tuple[type, ...],
    field_name: str,
    type_tag: ErrorTag,
    value_tag: ErrorTag,
    *,
    allow_empty: bool = True,
) -> list[Any]: ...


def validate_sequence_of_type(
    value: Any,
    types: type[T] | tuple[type, ...],
    field_name: str,
    type_tag: ErrorTag,
    value_tag: ErrorTag,
    *,
    allow_empty: bool = True,
) -> list[T] | list[Any]:
    """Validate that a value is a sequence of specified type(s).

        (validation primitive - does not depend on other validators)

    When a single type is provided, the return type is automatically inferred as list[T].
    When multiple types are provided, the return type is list[Any], which allows the
    caller to narrow the type with an explicit annotation.

    :param Sequence[Any] value: The sequence of values to validate.
    :param types: A single type or tuple of allowed types.
    :type types: type[T] | tuple[type, ...] | LazyType[T, Any]
    :param str field_name: The name of the field being validated (for error messages).
    :param ErrorTag type_tag: The error tag to use for type errors.
    :param ErrorTag value_tag: The error tag to use for value errors.
    :param bool allow_empty: Whether to allow an empty sequence. Defaults to True.
    :return: For single type, returns list[T]. For multiple types,
        returns list[Any] which can be narrowed with explicit type annotation.
    :rtype: list[T] | list[Any]
    :raises SimpleBenchTypeError: If the value is not a sequence or contains invalid types.
    :raises SimpleBenchValueError: If the sequence is empty and allow_empty is False.

    Examples:
        Single type (automatic inference):

        .. code-block:: python

            names = validate_sequence_of_type(['Alice'], str, 'names', ...)
            # Type: list[str]

        Multiple types (manual narrowing):

        .. code-block:: python

            mixed: list[str | int] = validate_sequence_of_type(['a', 1], (str, int), 'items', ...)
            # Type: list[str | int]
    """
    if not isinstance(value, Sequence) or isinstance(value, str):
        raise SimpleBenchTypeError(
            f'Invalid {field_name} type: {type(value).__name__}. Must be a sequence (list, tuple, etc.).', tag=type_tag
        )

    if len(value) == 0 and not allow_empty:
        raise SimpleBenchValueError(f'Invalid {field_name}: sequence cannot be empty.', tag=value_tag)

    # Format type names for error messages
    if isinstance(types, tuple):
        type_names = ' or '.join(t.__name__ for t in types)
    else:
        type_names = types.__name__

    result: list[Any] = []
    for i, item in enumerate(value):
        if not isinstance(item, types):
            raise SimpleBenchTypeError(
                f'Invalid {field_name} element at index {i}: {type(item).__name__}. Must be {type_names}.', tag=type_tag
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
    allow_empty: bool = True,
) -> frozenset[T]: ...


@overload
def validate_frozenset_of_type(
    value: frozenset[Any],
    types: tuple[type, ...],
    field_name: str,
    type_tag: ErrorTag,
    value_tag: ErrorTag,
    allow_empty: bool = True,
) -> frozenset[Any]: ...


def validate_frozenset_of_type(
    value: frozenset[Any],
    types: type[T] | tuple[type, ...],
    field_name: str,
    type_tag: ErrorTag,
    value_tag: ErrorTag,
    allow_empty: bool = True,
) -> frozenset[T] | frozenset[Any]:
    """Validate that a value is a frozenset of specified type(s).

        (validation primitive - does not depend on other validators)

    When a single type is provided, the return type is automatically inferred as frozenset[T].
    When multiple types are provided, the return type is frozenset[Any], which allows the
    caller to narrow the type with an explicit annotation.

    Single type (automatic type inference) example:

    .. code-block:: python

        friends_names: frozenset[str] = frozenset(['Alice', 'Bob'])
        names = validate_frozenset_of_type(
            friends_names, str, 'names', ErrorTag.SOME_TYPE_TAG, ErrorTag.SOME_VALUE_TAG, allow_empty=False
        )
        # Type: frozenset[str]

    Multiple types (manual narrowing) example:

    .. code-block:: python

        mixed_values: frozenset[str | int] = frozenset(['a', 1, 'b', 2])
        mixed: frozenset[str | int] = validate_frozenset_of_type(
            mixed_values, (str, int), 'items', ErrorTag.SOME_TYPE_TAG, ErrorTag.SOME_VALUE_TAG, allow_empty=True
        )
        # Type: frozenset[str | int]

    :param Any value: The frozenset of values to validate.
    :param types: A single type or tuple of allowed types.
    :type types: type[T] | tuple[type, ...]
    :param str field_name: The name of the field being validated (for error messages).
    :param ErrorTag type_tag: The error tag to use for type errors.
    :param ErrorTag value_tag: The error tag to use for value errors.
    :param bool allow_empty: Whether to allow an empty iterable. Defaults to True.
    :return: For single type, returns `frozenset[T]`. For multiple types, returns `frozenset[Any]`
        which can be narrowed with explicit type annotation.
    :rtype: frozenset
    :raises SimpleBenchTypeError: If the value is not a frozenset or contains invalid types.
    :raises SimpleBenchValueError: If the frozenset is empty and allow_empty is False.
    """
    if not isinstance(value, frozenset):
        raise SimpleBenchTypeError(
            f'Invalid {field_name} type: {type(value).__name__}. Must be a frozenset.', tag=type_tag
        )

    if len(value) == 0 and not allow_empty:
        raise SimpleBenchValueError(f'Invalid {field_name}: sequence cannot be empty.', tag=value_tag)

    # Format type names for error messages
    if isinstance(types, tuple):
        type_names = ' or '.join(t.__name__ for t in types)
    else:
        type_names = types.__name__

    for i, item in enumerate(value):
        if not isinstance(item, types):
            raise SimpleBenchTypeError(
                f'Invalid {field_name} element at index {i}: {type(item).__name__}. Must be {type_names}.', tag=type_tag
            )
    result: frozenset[T] = frozenset(value)
    # Return the now validated frozenset
    return result


def validate_sequence_of_numbers(
    value: Sequence[int | float], field_name: str, type_tag: ErrorTag, value_tag: ErrorTag, allow_empty: bool = True
) -> Sequence[int | float]:
    """Validate that a value is a sequence of numbers (ints or floats).

        (validation primitive - does not depend on other validators)

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

    :param Sequence[int | float] value: The sequence of values to validate.
    :param str field_name: The name of the field being validated (for error messages).
    :param ErrorTag type_tag: The error tag to use for type errors.
    :param ErrorTag value_tag: The error tag to use for value errors.
    :param bool allow_empty: Whether to allow a empty sequence. Defaults to True.
    :return: The validated Sequence of numbers.
    :rtype: Sequence[int | float]
    :raises SimpleBenchTypeError: If the value is not a sequence or contains non-numeric types.
    :raises SimpleBenchValueError: If the sequence is empty and allow_empty is False.
    """
    if not isinstance(value, Sequence) or isinstance(value, str):
        raise SimpleBenchTypeError(
            f'Invalid {field_name} type: {type(value)}. Must be a sequence (list, tuple, etc.) of numbers.',
            tag=type_tag,
        )
    if len(value) == 0 and not allow_empty:
        raise SimpleBenchValueError(f'Invalid {field_name}: sequence cannot be empty.', tag=value_tag)
    for i, item in enumerate(value):
        if not isinstance(item, (int, float)):
            raise SimpleBenchTypeError(
                f'Invalid {field_name} element at index {i}: {type(item)}. Must be an int or float.', tag=type_tag
            )
    return value


def validate_sequence_of_str(
    value: Any,
    name: str,
    type_tag: ErrorTag,
    value_tag: ErrorTag,
    *,
    allow_empty: bool = True,
    allow_blank: bool = True,
    allow_whitespace: bool = True,
) -> list[str]:
    """Validate that a value is a sequence of strings.

        (validation primitive - does not depend on other validators)

    This function checks that the input is a sequence (list, tuple, etc.) of strings,
    and that each string meets the specified criteria.

    It can enforce that the sequence is not empty, and that individual strings are not blank
    or do not contain any whitespace, based on the provided flags.

    :param Sequence[Any] value: The sequence of values to validate.
    :param str name: The name of the field being validated (for error messages).
    :param ErrorTag type_tag: The error tag to use for type errors.
    :param ErrorTag value_tag: The error tag to use for value errors.
    :param bool allow_empty: Whether to allow an empty sequence. Defaults to True.
    :param bool allow_blank: Whether to allow blank strings in the sequence. Defaults to True.
    :param bool allow_whitespace: Whether to allow strings that contain whitespace. Defaults to True.
    :return: The validated list of strings.
    :rtype: list[str]
    :raises SimpleBenchTypeError: If the value is not a sequence or contains non-string types.
    :raises SimpleBenchValueError: If the sequence is empty and allow_empty is False or an element is
            blank and allow_blank is False.
    """
    if not all(isinstance(item, str) for item in value):
        raise SimpleBenchTypeError(f'Invalid {name} type: {type(value)}. Must be a sequence of strings.', tag=type_tag)
    if not allow_empty and len(value) == 0:
        raise SimpleBenchValueError(f'Invalid {name}: sequence cannot be empty.', tag=value_tag)

    list_of_str: list[str] = list(value)
    if not allow_blank:
        for i, item in enumerate(list_of_str):
            if item.strip() == '':
                raise SimpleBenchValueError(
                    f'Invalid {name} element at index {i}: cannot be blank or whitespace.', tag=value_tag
                )
    if not allow_whitespace:
        for i, item in enumerate(list_of_str):
            if any(c.isspace() for c in item):
                raise SimpleBenchValueError(
                    f'Invalid {name} element at index {i}: cannot contain whitespace characters.', tag=value_tag
                )
    return list_of_str


def validate_int_range(
    number: Any, name: str, type_tag: ErrorTag, value_tag: ErrorTag, min_value: int, max_value: int
) -> int:
    """Validate that a value is an integer within a specified range.

        (validation primitive - does not depend on other validators)

    :param Any number: The value to validate.
    :param str name: The name of the field being validated (for error messages).
    :param ErrorTag type_tag: The error tag to use for type errors.
    :param ErrorTag value_tag: The error tag to use for value errors.
    :param int min_value: The minimum value of the range.
    :param int max_value: The maximum value of the range.
    :raises SimpleBenchValueError: If min_value is greater than max_value.
    :raises SimpleBenchTypeError: If field_name is not a str.
    :raises SimpleBenchTypeError: If type_tag or value_tag is not an ErrorTag.
    :raises SimpleBenchTypeError: If number, min_value, or max_value is not an int.
    :raises SimpleBenchValueError: If number is not within the specified range.
    """
    if not isinstance(name, str):
        raise SimpleBenchTypeError(
            f'Invalid call to validate_int_range: field_name type: {type(name)}. Must be a str.',
            tag=_ValidatorsErrorTag.INVALID_FIELD_NAME_TYPE,
        )
    if not isinstance(min_value, int):
        raise SimpleBenchTypeError(
            f'Invalid call to validate_int_range: min_value type {type(min_value)}. Must be an int.',
            tag=_ValidatorsErrorTag.INVALID_MIN_VALUE_TYPE,
        )
    if not isinstance(max_value, int):
        raise SimpleBenchTypeError(
            f'Invalid call to validate_int_range: max_value type {type(max_value)}. Must be an int.',
            tag=_ValidatorsErrorTag.INVALID_MAX_VALUE_TYPE,
        )
    if min_value > max_value:
        raise SimpleBenchValueError(
            f'Invalid call to validate_int_range: min_value ({min_value}) '
            f'cannot be greater than max_value ({max_value}).',
            tag=_ValidatorsErrorTag.INVALID_RANGE,
        )
    if not isinstance(number, int):
        raise SimpleBenchTypeError(f'Invalid {name} type: {type(number)}. Must be an int.', tag=type_tag)
    if not min_value <= number <= max_value:
        raise SimpleBenchValueError(
            f'Invalid {name}: {number}. Must be an int between {min_value} and {max_value}, inclusive.', tag=value_tag
        )

    return number


def validate_float_range(
    number: Any, field_name: str, type_tag: ErrorTag, value_tag: ErrorTag, min_value: float, max_value: float
) -> float:
    """Validate that a value is a float within a specified range.

    Accepts both float and int types for the number parameter,
    but always returns a float.

        (validation primitive - does not depend on other validators)

    :param float number: The value to validate.
    :param str field_name: The name of the field being validated (for error messages).
    :param ErrorTag type_tag: The error tag to use for type errors.
    :param ErrorTag value_tag: The error tag to use for value errors.
    :param float min_value: The minimum value of the range.
    :param float max_value: The maximum value of the range.
    :raises SimpleBenchValueError: If min_value is greater than max_value.
    :raises SimpleBenchTypeError: If field_name is not a str.
    :raises SimpleBenchTypeError: If type_tag or value_tag is not an ErrorTag.
    :raises SimpleBenchTypeError: If number, min_value, or max_value is not a float..
    :raises SimpleBenchValueError: If number is not within the specified range.
    """
    if not isinstance(field_name, str):
        raise SimpleBenchTypeError(
            f'Invalid call to validate_float_range: field_name type: {type(field_name)}. Must be a str.',
            tag=_ValidatorsErrorTag.INVALID_FIELD_NAME_TYPE,
        )
    if not isinstance(min_value, float):
        raise SimpleBenchTypeError(
            f'Invalid call to validate_float_range: min_value type {type(min_value)}. Must be a float.',
            tag=_ValidatorsErrorTag.INVALID_MIN_VALUE_TYPE,
        )
    if not isinstance(max_value, float):
        raise SimpleBenchTypeError(
            f'Invalid call to validate_float_range: max_value type {type(max_value)}. Must be a float.',
            tag=_ValidatorsErrorTag.INVALID_MAX_VALUE_TYPE,
        )
    if min_value > max_value:
        raise SimpleBenchValueError(
            f'Invalid call to validate_float_range: min_value ({min_value}) '
            f'cannot be greater than max_value ({max_value}).',
            tag=_ValidatorsErrorTag.INVALID_RANGE,
        )
    if not isinstance(number, float | int):  # Allow ints as valid floats
        raise SimpleBenchTypeError(f'Invalid {field_name} type: {type(number)}. Must be a float or int.', tag=type_tag)
    if not min_value <= number <= max_value:
        raise SimpleBenchValueError(
            f'Invalid {field_name}: {number}. Must be a float between {min_value} and {max_value}, inclusive.',
            tag=value_tag,
        )

    return float(number)


# Validate filename stem regex: alphanumeric characters, dashes, and underscores only,
# at least one character long, cannot start or end with an underscore or dash.
# Length is checked separately.
_FILENAME_STEM_RE = re.compile(r'^[A-Za-z0-9](?:[-_A-Za-z0-9]*[A-Za-z0-9])?$')


def validate_filename(filename: Any) -> str:
    """Validate a filename for use in the filesystem.

        (validation primitive - does not depend on other validators)

    It validates that:
        - The filename is a string.
        - The filename suffix (if present) is alphanumeric and no longer than 10 characters.
        - The filename stem (name without suffix) is made of alphanumeric characters,
          underscores, or dashes, and is at least one character long.
        - The filename stem does not start or end with an underscore or dash.
        - The total filename length does not exceed 255 characters.

    :param str filename: The filename to validate.
    :return: The validated filename.
    :rtype: str
    :raises SimpleBenchTypeError: If the filename is not a string.
    :raises SimpleBenchValueError: If the filename is invalid.
    """
    if not isinstance(filename, str):
        raise SimpleBenchTypeError(
            f'Invalid filename type: {type(filename)}. Must be a str.',
            tag=_ValidatorsErrorTag.VALIDATE_FILENAME_INVALID_FILENAME_ARG_TYPE,
        )

    file = Path(filename)
    file_suffix = file.suffix.replace('.', '', 1)
    if file_suffix != '' and len(file_suffix) > 10:
        raise SimpleBenchValueError(
            f"Filename suffix cannot be longer than 10 characters (passed suffix was '{file_suffix}')",
            tag=_ValidatorsErrorTag.VALIDATE_FILENAME_SUFFIX_TOO_LONG,
        )
    if file_suffix != '' and not file_suffix.isalnum():
        raise SimpleBenchValueError(
            'Filename suffix must be alphanumeric (contain only A-Z, a-z, 0-9)',
            tag=_ValidatorsErrorTag.VALIDATE_FILENAME_SUFFIX_NOT_ALPHANUMERIC,
        )
    file_stem = file.stem
    if file_stem == '':
        raise SimpleBenchValueError(
            'Filename must have a valid stem (name without suffix). It cannot be empty or blank.',
            tag=_ValidatorsErrorTag.VALIDATE_FILENAME_INVALID_STEM,
        )
    if not re.match(_FILENAME_STEM_RE, file_stem):
        raise SimpleBenchValueError(
            'Filename stem (name without suffix) must consist of '
            'only alphanumeric (A-Z, a-z, 0-9), underscore (_), or dash (-) characters, '
            'cannot start or end with an underscore or dash, and must be '
            'at least one character long '
            f"(passed stem was '{file_stem}')",
            tag=_ValidatorsErrorTag.VALIDATE_FILENAME_STEM_NOT_ALPHANUMERIC,
        )
    if len(filename) > 255:
        raise SimpleBenchValueError(
            f"Filename cannot be longer than 255 characters (passed filename was '{filename}')",
            tag=_ValidatorsErrorTag.VALIDATE_FILENAME_TOO_LONG,
        )
    return filename

# Validate directory path element regex: alphanumeric characters, dashes, and underscores only,
# at least one character long, cannot start or end with an underscore or dash.
#
_DIRPATH_ELEMENT_RE = re.compile(r'^[A-Za-z0-9](?:[-_A-Za-z0-9]*[A-Za-z0-9])?$')


def validate_dirname(dirname: Any, *, allow_empty: bool = False) -> str:
    """Validate a directory name for use in the filesystem.

    This is a single directory name (not a full path).

        (validation primitive - does not depend on other validators)

    It validates that:
        - The directory name is a string.
        - The directory name is made of alphanumeric characters,
          underscores, or dashes, and is at least one character long.
        - The directory name does not start or end with an underscore or dash.
        - If allow_empty is False, that the directory name is not an empty string. If
          allow_empty is True, an empty string is considered to be a valid dirname (default is
        - The total directory name length does not exceed 64 characters.

    :param dirname: The directory name to validate.
    :type dirname: str
    :param allow_empty: Whether to allow an empty directory name. Defaults to False.
    :type allow_empty: bool
    :return: The validated directory name.
    :rtype: str
    :raises SimpleBenchTypeError: If the directory name is not a string.
    :raises SimpleBenchValueError: If the directory name is invalid.
    """
    if not isinstance(dirname, str):
        raise SimpleBenchTypeError(
            f'Invalid directory name type: {type(dirname)}. Must be a str.',
            tag=_ValidatorsErrorTag.VALIDATE_DIRNAME_INVALID_DIRNAME_ARG_TYPE,
        )

    if dirname == '':
        if allow_empty:
            return ''

        raise SimpleBenchValueError(
            'Directory name cannot be an empty string.',
            tag=_ValidatorsErrorTag.VALIDATE_DIRNAME_EMPTY_NOT_ALLOWED)

    if not re.match(_DIRPATH_ELEMENT_RE, dirname):
        raise SimpleBenchValueError(
            'Dirname must consist of '
            'only alphanumeric (A-Z, a-z, 0-9), underscore (_), or dash (-) characters, '
            'cannot start or end with an underscore or dash, and must be '
            'at least one character long ',
            tag=_ValidatorsErrorTag.VALIDATE_DIRNAME_INVALID_CHARACTERS,
        )

    if len(dirname) > 64:
        raise SimpleBenchValueError(
            f"Directory name cannot be longer than 64 characters (passed directory name was '{dirname}')",
            tag=_ValidatorsErrorTag.VALIDATE_DIRNAME_TOO_LONG,
        )
    return dirname


def validate_dirpath(dirpath: Any, allow_empty: bool = False, field_name: str = 'dirpath') -> str:
    """Validate a directory path for use in the filesystem.

    It validates that:
        - The directory path is a string.
        - The complete directory path is no longer than 255 characters.
        - The directory path does not contain characters other than alphanumeric characters (A-Za-z0-9),
          underscores (-), dashes (-), slashes ( / ), or backslashes ( \\ ).
        - That individual directory path element names do not start or end with a dash (-) or underscore (_).
        - That individual directory path element names are at least one character long but no longer than 64 characters.
          (this does not apply to the full path, only to each element between slashes or backslashes and is checked
          separately).
        - If allow_empty is False, that the directory path is not an empty string. If allow_empty is True,
          an empty string is considered to be a valid dirpath (default is False).

    Backslashes ( \\ ) are converted to slashes ( / ) for validation purposes.

    :param str dirpath: The directory path to validate.
    :param bool allow_empty: Whether to allow an empty directory path. Defaults to False.
    :param str field_name: The name of the field being validated (for error messages). Defaults to 'dirpath'.
    :return: The validated directory path.
    :rtype: str
    :raises SimpleBenchTypeError: If the directory path is not a string.
    :raises SimpleBenchValueError: If the directory path is invalid.
    """
    if not isinstance(allow_empty, bool):
        raise SimpleBenchTypeError(
            f'Invalid allow_empty type: {type(allow_empty)}. Must be a bool.',
            tag=_ValidatorsErrorTag.VALIDATE_DIRPATH_INVALID_ALLOW_EMPTY_ARG_TYPE)
    if not isinstance(field_name, str):
        raise SimpleBenchTypeError(
            f'Invalid field_name type: {type(field_name)}. Must be a str.',
            tag=_ValidatorsErrorTag.VALIDATE_DIRPATH_INVALID_FIELD_NAME_ARG_TYPE)

    if not isinstance(dirpath, str):
        raise SimpleBenchTypeError(
            f'Invalid {field_name} type: {type(dirpath)}. Must be a str.',
            tag=_ValidatorsErrorTag.VALIDATE_DIRPATH_INVALID_DIRPATH_ARG_TYPE)

    if not allow_empty and dirpath == '':
        raise SimpleBenchValueError(
            'Directory path cannot be an empty string.',
            tag=_ValidatorsErrorTag.VALIDATE_DIRPATH_INVALID_DIRPATH_ARG_VALUE)

    if not dirpath and allow_empty:
        return ''

    if len(dirpath) > 255:
        raise SimpleBenchValueError(
            f"Directory path cannot be longer than 255 characters (passed directory path was '{dirpath}')",
            tag=_ValidatorsErrorTag.VALIDATE_DIRPATH_TOO_LONG,
        )

    if not re.match(r'^[A-Za-z0-9_\\/-]+$', dirpath):
        raise SimpleBenchValueError(
            'Directory path must consist of only alphanumeric characters (A-Za-z0-9), underscores (_), dashes (-), '
            f"slashes (/) or backslashes (\\) (passed directory path was '{dirpath}')",
            tag=_ValidatorsErrorTag.VALIDATE_DIRPATH_INVALID_CHARACTERS,
        )

    # Use the validated 'dirpath' variable consistently and simplify the check.
    if dirpath.startswith(('/', '\\')) or dirpath.endswith(('/', '\\')):
        raise SimpleBenchValueError(
            'Directory path cannot start or end with a slash (/) or backslash (\\)',
            tag=_ValidatorsErrorTag.VALIDATE_DIRPATH_INVALID_START_END,
        )

    path = Path(dirpath)
    for element in path.parts:
        if not element:
            raise SimpleBenchValueError(
                'Directory path cannot contain empty elements, which can be caused by '
                f"consecutive slashes (e.g., '//') (passed directory path was '{dirpath}')",
                tag=_ValidatorsErrorTag.VALIDATE_DIRPATH_ELEMENT_EMPTY,
            )

        if not re.match(_DIRPATH_ELEMENT_RE, element):
            raise SimpleBenchValueError(
                'Directory path elements (names between slashes or backslashes) must consist of '
                'only alphanumeric (A-Z, a-z, 0-9), underscore (_), or dash (-) characters, '
                'cannot start or end with an underscore or dash, and must be '
                f"at least one character long (invalid element was '{element}')",
                tag=_ValidatorsErrorTag.VALIDATE_DIRPATH_ELEMENT_HAS_INVALID_CHARACTERS,
            )
        if len(element) > 64:
            raise SimpleBenchValueError(
                'Directory path elements (names between slashes or backslashes) cannot be longer than 64 characters '
                f"(invalid element was '{element}')",
                tag=_ValidatorsErrorTag.VALIDATE_DIRPATH_ELEMENT_TOO_LONG,
            )

    return path.as_posix()
