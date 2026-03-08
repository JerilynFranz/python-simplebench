"""Extras exceptions for JSON report v1."""

from enum import auto
from simplebench.doc_utils import enum_docstrings
from simplebench.exceptions import ErrorTag

__all__: list[str] = []


@enum_docstrings
class _ExtrasErrorTag(ErrorTag):
    """Error tags for JSON Extras v1 exceptions."""
    EXTRAS_OBJECT_IMMUTABLE = auto()
    """The ExtrasObject is immutable and cannot be modified after initialization."""
    KEY_ERROR_INVALID_EXTRA_NAME_VALUE = auto()
    """The extra name key does not exist in extras."""
