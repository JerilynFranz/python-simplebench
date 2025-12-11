"""Validators for identifiers used in SimpleBench."""
import re

from simplebench.exceptions import SimpleBenchTypeError, SimpleBenchValueError

from .exceptions import _ValidatorsErrorTag

_IDENTIFIER_REGEX = re.compile(r"^[A-Za-z0-9](?:[_A-Za-z0-9]*[A-Za-z0-9])?::[A-Za-z0-9](?:[_A-Za-z0-9]*[A-Za-z0-9])?$")


def validate_namespaced_identifier(identifier: str) -> str:
    """Validate a namespaced identifier of the form 'namespace::type_name'.

    The namespace and type_name must start and end with an alphanumeric character
    and can contain underscores in between.

    :param identifier: The namespaced identifier to validate.
    :return: The validated namespaced identifier.
    :raises SimpleBenchValueError: If the identifier is not valid.
    """
    if not isinstance(identifier, str):
        raise SimpleBenchTypeError(
            f"Identifier must be a string, got {type(identifier).__name__}",
            tag=_ValidatorsErrorTag.INVALID_NAMESPACED_IDENTIFIER_TYPE)

    if not _IDENTIFIER_REGEX.match(identifier):
        raise SimpleBenchValueError(
            f"Invalid namespaced identifier '{identifier}'. "
            "It must be in the format 'namespace::type_name', "
            "where both namespace and type_name start and end with an alphanumeric character "
            "and can contain underscores in between.",
            tag=_ValidatorsErrorTag.INVALID_NAMESPACED_IDENTIFIER
        )

    return identifier
