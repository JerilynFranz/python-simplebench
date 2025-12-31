"""JSON execution environment classes"""
from typing import TYPE_CHECKING

from ._error_tags import _ExecutionEnvironmentErrorTag
from ._base import BaseExecutionEnvironment

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


def execution_environment_by_version(version: int) -> type[BaseExecutionEnvironment]:
    """Retrieve a ExecutionEnvironment class for the specified version.

    :param version: The JSON report version number.
    :return: A ExecutionEnvironment class for the specified version.
    """
    _load_deferred_imports()

    return json_class(
        version,
        BaseExecutionEnvironment,
        _ExecutionEnvironmentErrorTag.INVALID_VERSION_TYPE,
        _ExecutionEnvironmentErrorTag.UNSUPPORTED_VERSION)


def from_dict(data: dict) -> BaseExecutionEnvironment:
    """Create a json ExecutionEnvironment instance from a dictionary, with validation.

    It checks the version in the data and instantates the appropriate sub-class

    :param data: Dictionary containing the JSON ExecutionEnvironment data.
    :return: ExecutionEnvironment sub-class instance.
    """
    _load_deferred_imports()

    version: int = data.get('version', 0)  # Default to 0 if not present

    report_class: type[BaseExecutionEnvironment] = json_class(
        version,
        BaseExecutionEnvironment,
        _ExecutionEnvironmentErrorTag.INVALID_VERSION_TYPE,
        _ExecutionEnvironmentErrorTag.UNSUPPORTED_VERSION)
    return report_class.from_dict(data)
