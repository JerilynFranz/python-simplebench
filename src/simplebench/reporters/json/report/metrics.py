"""JSON metrics classes"""
from typing import TYPE_CHECKING

from .base import Metrics
from .exceptions import _MetricsErrorTag

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


def metrics(version: int) -> type[Metrics]:
    """Retrieve a Metrics class for the specified version.

    :param version: The JSON report version number.
    :return: A Metrics class for the specified version.
    """
    _load_deferred_imports()

    return json_class(
        version,
        Metrics,
        _MetricsErrorTag.INVALID_VERSION_TYPE,
        _MetricsErrorTag.UNSUPPORTED_VERSION)


def from_dict(data: dict) -> Metrics:
    """Create a json Metrics instance from a dictionary, with validation.

    It checks the version in the data and instantates the appropriate sub-class

    :param data: Dictionary containing the JSON Metrics data.
    :return: Metrics sub-class instance.
    """
    _load_deferred_imports()

    version: int = data.get('version', 0)  # Default to 0 if not present

    report_class: type[Metrics] = json_class(
        version,
        Metrics,
        _MetricsErrorTag.INVALID_VERSION_TYPE,
        _MetricsErrorTag.UNSUPPORTED_VERSION)
    return report_class.from_dict(data)
