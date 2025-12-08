"""Validators for dates and times."""

from datetime import datetime, timezone

from simplebench.exceptions import ErrorTag, SimpleBenchTypeError, SimpleBenchValueError


def validate_iso8601_datetime(dt_str: str,
                              type_tag: ErrorTag,
                              value_tag: ErrorTag) -> str:
    """Validate that a string is a valid ISO 8601 datetime and return a string representation in UTC time.

    The datetime string is parsed as an ISO8601 date and then returned in UTC timezone as the canonical form.

    :param dt_str: The datetime string in ISO 8601 format.
    :return: A datetime object representing the input string.
    :raises SimpleBenchValueError: If the input string is not a valid ISO 8601 datetime.
    :raises SimpleBenchTypeError: If the input is not a string.
    """
    if not isinstance(dt_str, str):
        raise SimpleBenchTypeError(
            f"Expected a string for ISO 8601 datetime, got {type(dt_str)}",
            tag=type_tag)
    if not dt_str:
        raise SimpleBenchValueError(
            "ISO 8601 datetime string cannot be empty",
            tag=value_tag)
    try:
        dt = datetime.fromisoformat(dt_str)
        dt = dt.replace(tzinfo=timezone.utc)
        return dt.isoformat()
    except ValueError as e:
        raise SimpleBenchValueError(
            f"Invalid ISO 8601 datetime string: {dt_str}",
            tag=value_tag) from e
