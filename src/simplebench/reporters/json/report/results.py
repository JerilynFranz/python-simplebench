"""JSON Results classes"""
from .base_json_results import JSONResults
from .exceptions import _JSONResultsErrorTag
from .versions import json_class


def from_dict(data: dict, version: int) -> JSONResults:
    """Create a JSONResults instance from a dictionary.

    It checks the version and instantates the appropriate sub-class

    :param data: Dictionary containing the JSON results data.
    :param version: The version of the JSON results data.
    :return: JSONResults sub-class instance.
    """
    return json_class(
        version,
        JSONResults,
        _JSONResultsErrorTag.INVALID_VERSION_TYPE,
        _JSONResultsErrorTag.UNSUPPORTED_VERSION).from_dict(data)
