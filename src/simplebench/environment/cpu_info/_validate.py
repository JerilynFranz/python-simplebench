"""Validators for environment.cpu_info module."""

from simplebench.validators import validate_string

from ._error_tags import _CPUInfoErrorTag


def cache_key(value: str | None) -> str | None:
    """Validate the cache_key parameter.

    The cache_key must be a non-blank string containing only alphanumeric characters.

    :param str | None value: The cache_key string to validate.
    :return str | None: The validated cache_key string.
    :raises SimpleBenchTypeError: If the value is not a string or ``None``.
    :raises SimpleBenchValueError: If the value is not a non-blank alphanumeric string.
    """
    if value is None:
        return None
    return validate_string(
        value, "cache_key",
        _CPUInfoErrorTag.INVALID_CACHE_KEY_PARAM_TYPE,
        _CPUInfoErrorTag.INVALID_CACHE_KEY_PARAM_VALUE,
        strip=False, allow_empty=False, alphanumeric_only=True,
        message="cache_key must be a non-empty string containing only alphanumeric characters.")
