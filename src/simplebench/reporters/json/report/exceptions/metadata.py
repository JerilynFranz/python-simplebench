"""Exceptions for JSON metadata classes."""
from simplebench.enums import enum_docstrings
from simplebench.exceptions import ErrorTag


@enum_docstrings
class _MetadataErrorTag(ErrorTag):
    """Error tags for JSON metadata exceptions."""
    INVALID_TYPE_TYPE = "INVALID_TYPE_TYPE"
    """The type is not of type str."""
    INVALID_TYPE_VALUE = "INVALID_TYPE_VALUE"
    """The type has an incorrect value."""
    INVALID_VERSION_TYPE = "INVALID_VERSION_TYPE"
    """The version is not of type integer."""
    INVALID_VERSION_VALUE = "INVALID_VERSION_VALUE"
    """The version has an incorrect value."""
    UNSUPPORTED_VERSION = "UNSUPPORTED_VERSION"
    """The version is not supported."""
