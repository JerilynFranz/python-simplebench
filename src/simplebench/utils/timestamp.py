"""Time related utilities."""
import time

from simplebench.exceptions import SimpleBenchValueError
from simplebench.validators.misc import validate_float, validate_string

from .exceptions import _UtilsErrorTag


def timestamp_to_iso8601(timestamp: float) -> str:
    """Convert a timestamp in seconds since epoch to an ISO 8601 string in UTC.

    :param timestamp: The timestamp in seconds since epoch.
    :return: The ISO 8601 formatted timestamp string in UTC.
    :raises SimpleBenchTypeError: If the timestamp argument is not a float.
    """
    validate_float(
        timestamp, "timestamp",
        _UtilsErrorTag.TIMESTAMP_TO_ISO8601_INVALID_TIMESTAMP_ARG_TYPE)
    return time.strftime("%Y-%m-%dT%H:%M:%S%z", time.gmtime(timestamp))


def iso8601_to_timestamp(iso8601_str: str) -> float:
    """Convert an ISO 8601 formatted timestamp string in UTC to a timestamp in seconds since epoch.

    :param iso8601_str: The ISO 8601 formatted timestamp string in UTC.
    :return: The timestamp in seconds since epoch.
    :raises SimpleBenchTypeError: If the iso8601_str argument is not a str.
    :raises SimpleBenchValueError: If the iso8601_str argument is an empty str or is not a valid ISO 8601 timestamp.
    """
    validate_string(
        iso8601_str, "iso8601_str",
        _UtilsErrorTag.TIMESTAMP_TO_ISO8601_INVALID_ISO8601_STR_ARG_TYPE,
        _UtilsErrorTag.TIMESTAMP_TO_ISO8601_EMPTY_ISO8601_STR_ARG_VALUE,
        allow_empty=False)

    try:
        struct_time = time.strptime(iso8601_str, "%Y-%m-%dT%H:%M:%S%z")
        return time.mktime(struct_time)
    except ValueError as e:
        raise SimpleBenchValueError(
            f"Invalid ISO 8601 timestamp string: {iso8601_str}",
            tag=_UtilsErrorTag.TIMESTAMP_TO_ISO8601_INVALID_ISO8601_STR_ARG_TYPE,
        ) from e
