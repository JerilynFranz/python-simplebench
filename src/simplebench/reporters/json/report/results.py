"""JSON Results classes"""
from typing import TYPE_CHECKING

from .base import JSONSchema, ResultsInfo
from .exceptions import _ResultsInfoErrorTag

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


def results_info(version: int) -> type[ResultsInfo]:
    """Retrieve a ResultsInfo class for the specified version.

    :param version: The JSON report version number.
    :return: A ResultsInfo class for the specified version.
    """
    _load_deferred_imports()

    return json_class(
        version,
        ResultsInfo,
        _ResultsInfoErrorTag.INVALID_VERSION_TYPE,
        _ResultsInfoErrorTag.UNSUPPORTED_VERSION
    )


def from_dict(data: dict, version: int) -> ResultsInfo:
    """Create a JSONResults instance from a dictionary.

    It checks the version and instantates the appropriate sub-class

    :param data: Dictionary containing the JSON results data.
    :param version: The version of the JSON results data.
    :return: JSONResults sub-class instance.
    """
    _load_deferred_imports()
    return json_class(
        version,
        ResultsInfo,
        _ResultsInfoErrorTag.INVALID_VERSION_TYPE,
        _ResultsInfoErrorTag.UNSUPPORTED_VERSION).from_dict(data)


def schema(version: int) -> type[JSONSchema]:
    """Retrieve a ResultsSchema instance for the specified version.

    :param version: The JSON report version number.
    :return: A ResultsSchema instance for the specified version.
    """
    _load_deferred_imports()

    return json_class(
        version,
        ResultsInfo,
        _ResultsInfoErrorTag.INVALID_VERSION_TYPE,
        _ResultsInfoErrorTag.UNSUPPORTED_VERSION
    ).SCHEMA
