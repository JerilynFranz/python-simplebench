"""Validators for identifiers used in SimpleBench."""
import re

from simplebench.exceptions import ErrorTag, SimpleBenchTypeError, SimpleBenchValueError

from ._error_tags import _ValidatorsErrorTag

_IDENTIFIER_REGEX = re.compile(r"^[A-Za-z0-9](?:[_A-Za-z0-9]*[A-Za-z0-9])?::[A-Za-z0-9](?:[_A-Za-z0-9]*[A-Za-z0-9])?$")


def validate_namespaced_identifier(
        identifier: str,
        field_name: str = '',
        type_error_tag: ErrorTag = _ValidatorsErrorTag.INVALID_NAMESPACED_IDENTIFIER_TYPE,
        value_error_tag: ErrorTag = _ValidatorsErrorTag.INVALID_NAMESPACED_IDENTIFIER) -> str:
    """Validate a namespaced identifier of the form 'namespace::type_name'.

    The namespace and type_name must start and end with an alphanumeric character
    and can contain underscores in between.

    :param identifier: The namespaced identifier to validate.
    :param field_name: The name of the field being validated.
        If not provided, no field name is included in the error message.
    :param type_error_tag: The error tag to use if the identifier is not a string
        If not provided, a default error tag is used.
    :param value_error_tag: The tag to use if the identifier is not valid.
        If not provided, a default error tag is used.
    :return: The validated namespaced identifier.
    :raises SimpleBenchValueError: If the identifier is not valid.
    """
    if not isinstance(field_name, str):
        raise SimpleBenchTypeError(
            f"Field name must be a string, got {type(field_name).__name__}",
            tag=_ValidatorsErrorTag.INVALID_FIELD_NAME_TYPE)
    if not isinstance(type_error_tag, ErrorTag):
        raise SimpleBenchTypeError(
            f"Type error tag must be an instance of ErrorTag, got {type(type_error_tag).__name__}",
            tag=_ValidatorsErrorTag.INVALID_TYPE_ERROR_TAG_TYPE)
    if not isinstance(value_error_tag, ErrorTag):
        raise SimpleBenchTypeError(
            f"Value error tag must be an instance of ErrorTag, got {type(value_error_tag).__name__}",
            tag=_ValidatorsErrorTag.INVALID_VALUE_ERROR_TAG_TYPE)
    if not isinstance(identifier, str):
        raise SimpleBenchTypeError(
            f"Identifier must be a string, got {type(identifier).__name__}",
            tag=type_error_tag)

    if not _IDENTIFIER_REGEX.match(identifier):
        raise SimpleBenchValueError(
            f"Invalid namespaced identifier '{identifier}'{f' for field {field_name}' if field_name else ''}. "
            "It must be in the format 'namespace::type_name', "
            "where both namespace and type_name start and end with an alphanumeric character "
            "and can contain underscores in between.",
            tag=value_error_tag
        )

    return identifier
