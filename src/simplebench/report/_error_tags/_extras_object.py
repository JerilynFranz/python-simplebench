"""Extras exceptions for JSON report v1."""

from simplebench.doc_utils import enum_docstrings
from simplebench.exceptions import ErrorTag

__all__: list[str] = []


@enum_docstrings
class _ExtrasErrorTag(ErrorTag):
    """Error tags for JSON Extras v1 exceptions."""
    EXTRAS_OBJECT_IMMUTABLE = 'EXTRAS_OBJECT_IMMUTABLE'
    """The ExtrasObject is immutable and cannot be modified after initialization."""
    KEY_ERROR_INVALID_EXTRA_NAME_VALUE = 'KEY_ERROR_INVALID_EXTRA_NAME_VALUE'
    """The extra name key does not exist in extras."""
