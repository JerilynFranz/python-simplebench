"""JSON Metadata classes"""

from .base_json_metadata import JSONMetadata
from .exceptions import _JSONMetadataErrorTag
from .versions import json_class


def from_dict(data: dict, version: int) -> JSONMetadata:
    """Create a JSONMetadata instance from a dictionary.
    It checks the passed version and instantates the appropriate sub-class

    :param data: Dictionary containing the JSON metadata.
    :param version: The version of the JSON metadata.
    :return: JSONMetadata sub-class instance.
    """
    return json_class(
        version,
        JSONMetadata,
        _JSONMetadataErrorTag.INVALID_VERSION_TYPE,
        _JSONMetadataErrorTag.UNSUPPORTED_VERSION).from_dict(data)
