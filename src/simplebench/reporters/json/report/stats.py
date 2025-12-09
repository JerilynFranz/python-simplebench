"""JSON Stats classes"""
from typing import TYPE_CHECKING

from .base.json_stats import JSONStats
from .exceptions import _JSONStatsErrorTag

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


def from_dict(data: dict, version: int) -> JSONStats:
    """Create a JSONStats instance from a dictionary.
    It checks the version in the data and instantates the appropriate sub-class

    :param data: Dictionary containing the JSON stats data.
    :param version: The version of the JSON stats data.
    :return: JSONStats sub-class instance.
    """
    _load_deferred_imports()
    return json_class(
        version,
        JSONStats,
        _JSONStatsErrorTag.INVALID_VERSION_TYPE,
        _JSONStatsErrorTag.UNSUPPORTED_VERSION).from_dict(data)
