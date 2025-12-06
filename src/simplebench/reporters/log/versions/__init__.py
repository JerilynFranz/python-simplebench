"""JSON logging versioned classes.

This module provides functionality to manage different versions of JSON log
entries for version numbers and dynamic retrieval of the appropriate class
implementations based on the specified version.
"""
from types import ModuleType
from typing import TypeAlias, TypeVar

from simplebench.exceptions import ErrorTag, SimpleBenchTypeError, SimpleBenchValueError
from simplebench.validators import validate_int

from ..base import ReportLogEntry, ReportLogEntrySchema
from ..exceptions import _ReportLogEntryErrorTag, _ReportLogEntrySchemaErrorTag
from . import v1

JSONErrorTags: TypeAlias = _ReportLogEntryErrorTag |_ReportLogEntrySchemaErrorTag
"""Type alias for all JSON log entry related error tags."""

CLASSES = (ReportLogEntry, ReportLogEntrySchema)
"""Tuple of all JSON log entry related classes."""

CLASS_TYPES = (type[ReportLogEntry], type[ReportLogEntrySchema])
"""Tuple of all JSON log entry related class types."""

T = TypeVar('T', type[ReportLogEntry], type[ReportLogEntrySchema])
"""Type variable for JSON log entry related class types."""

_known_versions: dict[int, ModuleType] = {
    1: v1,
}
"""Mapping of known JSON log entry versions to their modules."""

CURRENT_VERSION: int = max(_known_versions.keys())
"""The current JSON log entry entry version number."""


def validate_version(version: int,
                     type_tag: ErrorTag,
                     value_tag: ErrorTag) -> int:
    """Validate if the given version is supported.

    :param version: The version number to validate.
    :param type_tag: The error tag to use for type errors.
    :param value_tag: The error tag to use for value errors.
    :return: The validated version number.
    :raises SimpleBenchTypeError: If the version is not an integer.
    :raises SimpleBenchValueError: If the version is not supported.
    """
    validate_int(version, 'version', type_tag)
    if version not in _known_versions:
        raise SimpleBenchValueError(
            f"Unsupported JSON version: {version}",
            tag=value_tag)
    return version


def json_class(version: int,
               class_type: T,
               type_tag: ErrorTag,
               unsupported_tag: ErrorTag) -> T:

    """Get the JSON class type for a given version and class type."""
    validate_version(version,
                     type_tag,
                     unsupported_tag)
    versioned_module: ModuleType = _known_versions[version]
    if not hasattr(versioned_module, class_type.__name__):
        raise SimpleBenchTypeError(
            f"{class_type.__name__} class not found for version {version}",
            tag=unsupported_tag)
    json_class_ref: T = getattr(versioned_module, class_type.__name__)
    if not issubclass(json_class_ref, class_type):
        raise SimpleBenchTypeError(
            f"Invalid {class_type.__name__} class for version {version}",
            tag=unsupported_tag)
    return json_class_ref


__all__ = [
    "CURRENT_VERSION",
    "json_class",
]
