"""JSON Metadata

This module provides functionality to handle metadata for SimpleBench reports.
"""
from typing import TYPE_CHECKING

from .base import Metadata
from .exceptions import _MetadataErrorTag

_JSON_CLASS_LOADED: bool = False

if TYPE_CHECKING:
    from .versions import json_class
    _JSON_CLASS_LOADED = True  # To avoid import issues during type checking
else:
    json_class = None   # pylint: disable=invalid-name


def _load_deferred_imports() -> None:
    """Load deferred imports."""
    global _JSON_CLASS_LOADED, json_class  # pylint: disable=global-statement
    if not _JSON_CLASS_LOADED:
        from .versions import json_class  # pylint: disable=import-outside-toplevel
        _JSON_CLASS_LOADED = True


def from_dict(data: dict, version: int) -> Metadata:
    """Create a JSONMetadata instance from a dictionary.
    It checks the passed version and instantates the appropriate sub-class

    :param data: Dictionary containing the JSON metadata.
    :param version: The version of the JSON metadata.
    :return: JSONMetadata sub-class instance.
    """
    return json_class(
        version,
        Metadata,
        _MetadataErrorTag.INVALID_VERSION_TYPE,
        _MetadataErrorTag.UNSUPPORTED_VERSION).from_dict(data)
