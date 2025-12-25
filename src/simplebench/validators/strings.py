"""String validators for SimpleBench."""
import re
from typing import Any

from simplebench.exceptions import ErrorTag, SimpleBenchTypeError, SimpleBenchValueError

from ._error_tags import _ValidatorsErrorTag


def validate_string(  # noqa: C901
        value: Any,
        name: str,
        type_error_tag: ErrorTag,
        value_error_tag: ErrorTag, *,
        strip: bool = False,
        allow_empty: bool = True,
        allow_blank: bool = True,
        alphanumeric_only: bool = False,
        message: str = '') -> str:
    """Validate and normalize a string field.

    (validation primitive - does not depend on other validators)

    Validates that the value is a string. Optionally strips leading/trailing whitespace,
    checks for emptiness, blankness (whitespace-only strings), and alphanumeric content.

    The returned value is guaranteed to be of type str and acts to type-narrow
    the returned value.

    Following the principle of 'least astonishment', the validator does not modify
    the input string unless strip=True is set. If strip=True is set, the string is
    stripped of leading and trailing whitespace before other checks are applied.

    Explanation of options:
        strip=True means leading/trailing whitespace is removed before other checks.
        allow_empty=True means the string cannot be empty ("").
        allow_blank=True means the string can contain only whitespace characters.
        alphanumeric_only=True means the string only contain alphanumeric characters (a-z, A-Z, 0-9).

    Interaction of options:

    If `strip=True, allow_empty=True, allow_blank=False` is provided, `allow_empty=False`
    takes precedence over `allow_blank=True` as the more specific check. Therefore '   ' would be
    stripped to '' and then accepted as empty.

    If `strip=True, allow_blank=True, allow_empty=False` is provided, `allow_empty=False`
    takes precedence over `allow_blank=True` because after stripping a blank string becomes
    an empty string and `allow_empty=False` is the more specific check.
    Therefore ' ' would be stripped to '' and then rejected as empty.

    If `strip=False, allow_blank=True, alphanumeric_only=True` is provided, `alphanumeric_only=True`
    takes precedence over `allow_blank=True` because a blank string with whitespace is not alphanumeric
    by definition.

    `alphanumeric_only=True` behaves differently than `str().isalnum()` in that it allows empty strings if
    `allow_empty=True` is also provided.

    :param Any value: The value to validate as being a string.
    :param str name: The name of the field being validated (for error messages).
    :param ErrorTag type_error_tag: The error tag to use for type errors.
    :param ErrorTag value_error_tag: The error tag to use for value errors.
    :param bool strip: Whether to strip leading/trailing whitespace.
    :param bool allow_empty: Whether to allow empty strings.
    :param bool allow_blank: Whether to allow blank strings (strings that consist
        only of whitespace).
    :param bool alphanumeric_only: Whether to allow only alphanumeric characters.
    :param str message: Specific message to include in the error for value errors.
        Defaults to a generic message if not provided. A string format substitution
        will be done with the targets ``{name}`` and ``{value}`` on the passed
        message. (kwarg-only, optional)
    :return str: The validated string.
    :raises SimpleBenchTypeError: If the value is not a str.
    :raises SimpleBenchValueError: If the string fails any of the specified checks or if options contradict.
    """
    if not isinstance(strip, bool):
        raise SimpleBenchTypeError(
            f'Invalid strip type: {type(strip)}. Must be a bool.',
            tag=_ValidatorsErrorTag.INVALID_STRIP_ARG_TYPE
        )
    if not isinstance(allow_empty, bool):
        raise SimpleBenchTypeError(
            f'Invalid allow_empty type: {type(allow_empty)}. Must be a bool.',
            tag=_ValidatorsErrorTag.INVALID_ALLOW_EMPTY_ARG_TYPE
        )
    if not isinstance(allow_blank, bool):
        raise SimpleBenchTypeError(
            f'Invalid allow_blank type: {type(allow_blank)}. Must be a bool.',
            tag=_ValidatorsErrorTag.INVALID_ALLOW_BLANK_ARG_TYPE
        )
    if not isinstance(alphanumeric_only, bool):
        raise SimpleBenchTypeError(
            f'Invalid alphanumeric_only type: {type(alphanumeric_only)}. Must be a bool.',
            tag=_ValidatorsErrorTag.INVALID_ALPHANUMERIC_ONLY_ARG_TYPE
        )
    if not isinstance(value, str):
        raise SimpleBenchTypeError(
            f'Invalid {name} type: {type(value)}. Must be a str.',
            tag=type_error_tag
        )

    if not isinstance(message, str):
        raise SimpleBenchTypeError(
            f'Invalid message type: {type(message)}. Must be a str.',
            tag=_ValidatorsErrorTag.INVALID_MESSAGE_ARG_TYPE
        )

    formatted_message = message.format(name=name, value=value)

    if strip:
        value = value.strip()

    if value == '':  # Empty string
        if allow_empty:
            return value
        raise SimpleBenchValueError(
            formatted_message or f'Invalid {name}: cannot be empty string.',
            tag=value_error_tag)

    if value.strip() == '':  # Blank string (only whitespace)
        if allow_blank and not alphanumeric_only:
            return value
        raise SimpleBenchValueError(
            formatted_message or f'Invalid {name}: cannot be blank string (consist only of whitespace).',
            tag=value_error_tag)

    if alphanumeric_only:
        if value.isalnum():
            return value
        raise SimpleBenchValueError(
            (formatted_message or
             f'Invalid {name}: must consist only of alphanumeric characters [A-Za-z0-9]: "{value}".'),
            tag=value_error_tag)

    return value


def validate_non_blank_string(
        value: Any,
        name: str,
        type_error_tag: ErrorTag,
        value_error_tag: ErrorTag) -> str:
    """Validate and normalize a non-blank string field.

    (validation primitive - does not depend on other validators)

    Any leading or trailing whitespace is stripped from the string before returning it.

    The validation checks that the value is a string and that it is not blank or only whitespace.
    The returned value is guaranteed to be non-blank and non-blank and to be of type str.

    :param str value: The string value to validate.
    :param str name: The name of the field being validated (for error messages).
    :param ErrorTag type_error_tag: The error tag to use for type errors.
    :param ErrorTag value_error_tag: The error tag to use for value errors.
    :return: The stripped string value.
    :rtype: str
    :raises SimpleBenchTypeError: If the value is not a string.
    :raises SimpleBenchValueError: If the string is blank or only whitespace.
    """
    if not isinstance(value, str):
        raise SimpleBenchTypeError(
            f'Invalid {name} type: {type(value)}. Must be a string.',
            tag=type_error_tag
        )
    stripped_value = value.strip()
    if not stripped_value:
        raise SimpleBenchValueError(
            f'Invalid {name}: cannot be blank or whitespace.',
            tag=value_error_tag
        )
    return stripped_value


def validate_non_blank_string_or_is_none(
        value: Any,
        name: str,
        type_error_tag: ErrorTag,
        value_error_tag: ErrorTag,
        allow_none: bool = True) -> str | None:
    """Validate and normalize a non-blank string field.

        (validation primitive - does not depend on other validators)

    Any leading or trailing whitespace is stripped from the string before returning it.
    The validation checks that the value is a string and that it is not blank or only whitespace.
    If the value is None and allow_none is True, None is returned.

    The validated value is guaranteed to either be non-blank and non-blank and of type str, or
    None if allow_none is True and None is provided as the value.

    :param str value: The string value to validate.
    :param str name: The name of the field being validated (for error messages).
    :param ErrorTag type_error_tag: The error tag to use for type errors.
    :param ErrorTag value_error_tag: The error tag to use for value errors.
    :param bool allow_none: Whether to allow None as a valid value. Defaults to True.
    :return: The stripped string value or None if allowed and provided.
    :rtype: str | None
    :raises SimpleBenchTypeError: If the value is not a str, or None (if allow_none is False).
    :raises SimpleBenchValueError: If the string is blank or only whitespace.
    """
    if value is None:
        if allow_none:
            return None
        raise SimpleBenchTypeError(
            f'Invalid {name}: cannot be None.',
            tag=value_error_tag
        )
    if not isinstance(value, str):
        raise SimpleBenchTypeError(
            f'Invalid {name} type: {type(value)}. Must be a string.',
            tag=type_error_tag
        )
    stripped_value = value.strip()
    if not stripped_value:
        raise SimpleBenchValueError(
            f'Invalid {name}: cannot be blank or whitespace.',
            tag=value_error_tag
        )
    return stripped_value

def validate_string_with_regex(
        value: str,
        name: str,
        pattern: re.Pattern,
        type_error_tag: ErrorTag,
        value_error_tag: ErrorTag,
        *,
        message: str = '') -> str:
    """Validate that a string matches a specified regex pattern.

            (validation primitive - does not depend on other validators)

    :param str value: The string to validate.
    :param str name: The name of the property being validated (for error messages).
    :param re.Pattern pattern: The regex pattern that the string must match.
    :param ErrorTag type_error_tag: The error tag to use if the type is incorrect.
    :param ErrorTag value_error_tag: The error tag to use if the value does not match the pattern.
    :param str message: Specific message to include in the error for value errors.
        Defaults to a generic message. A string format substitution will be done with
        the targets ``{name}`` and ``{value}`` on a passed string. (kwarg-only, optional)
    :return str: The validated string.
    :raises SimpleBenchTypeError: If any of the calling parameters are of an incorrect type.
    :raises SimpleBenchValueError: If the value does not match the pattern.
    """
    func_name = 'validate_string_against_regex'
    if not isinstance(name, str):
        raise SimpleBenchTypeError(
            f"Invalid call to {func_name}: ``name`` parameter must be a string.",
            tag=type_error_tag
        )

    if not isinstance(value, str):
        raise SimpleBenchTypeError(
            f"{name} must be a string.",
            tag=type_error_tag
        )

    compiled_pattern: re.Pattern
    if isinstance(pattern, str):
        try:
            compiled_pattern = re.compile(pattern)
        except re.error as e:
            raise SimpleBenchValueError(
                f"Invalid call to {func_name}: ``pattern`` string {{ {pattern} }} could not "
                f"be compiled to a regex pattern.",
                tag=type_error_tag) from e
    elif isinstance(pattern, re.Pattern):
        compiled_pattern = pattern

    else:
        raise SimpleBenchTypeError(
            f"Invalid call to {func_name}: ``pattern`` parameter must be a "
            f"re.Pattern instance or a string not type {type(pattern)}.",
            tag=type_error_tag
        )

    if not isinstance(message, str):
        raise SimpleBenchTypeError(
            f"Invalid call to {func_name}: ``message`` parameter must be a string.",
            tag=type_error_tag
        )

    formatted_message: str
    if message:
        formatted_message = message.format(name=name, value=value)
    else:
        formatted_message = "{name} is invalid. {{ {value} }} does not match required pattern."

    if not compiled_pattern.match(value):
        raise SimpleBenchValueError(
            formatted_message,
            tag=value_error_tag
        )

    return value
