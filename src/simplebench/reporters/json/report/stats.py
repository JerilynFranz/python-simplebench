"""JSON Stats classes"""

from .base import JSONStats
from .exceptions import _JSONStatsErrorTag
from .versions import json_class


def from_dict(data: dict, version: int) -> JSONStats:
    """Create a JSONStats instance from a dictionary.
    It checks the version in the data and instantates the appropriate sub-class

    :param data: Dictionary containing the JSON stats data.
    :param version: The version of the JSON stats data.
    :return: JSONStats sub-class instance.
    """
    return json_class(
        version,
        JSONStats,
        _JSONStatsErrorTag.INVALID_VERSION_TYPE,
        _JSONStatsErrorTag.UNSUPPORTED_VERSION).from_dict(data)
