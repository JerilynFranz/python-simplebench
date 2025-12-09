"""JSON Results classes"""
from typing import TYPE_CHECKING

from .base.json_results import JSONResults
from .exceptions import _JSONResultsErrorTag

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


def from_dict(data: dict, version: int) -> JSONResults:
    """Create a JSONResults instance from a dictionary.

    It checks the version and instantates the appropriate sub-class

    :param data: Dictionary containing the JSON results data.
    :param version: The version of the JSON results data.
    :return: JSONResults sub-class instance.
    """
    _load_deferred_imports()
    return json_class(
        version,
        JSONResults,
        _JSONResultsErrorTag.INVALID_VERSION_TYPE,
        _JSONResultsErrorTag.UNSUPPORTED_VERSION).from_dict(data)
