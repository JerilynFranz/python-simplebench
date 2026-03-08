"""Error tags for report module."""

from enum import auto
from simplebench.doc_utils import enum_docstrings
from simplebench.exceptions import ErrorTag

__all__: list[str] = []


@enum_docstrings
class _ReportErrorTag(ErrorTag):
    """Error tags specific to the report module."""

    UNSUPPORTED_VERSION = auto()
    """Report version is invalid or unsupported."""

    INVALID_VERSION_TYPE = auto()
    """Report version type is invalid; expected an integer."""
