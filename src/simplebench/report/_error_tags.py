"""Error tags for report module."""
from simplebench.doc_utils import enum_docstrings
from simplebench.exceptions import ErrorTag

__all__ = []


@enum_docstrings
class _ReportErrorTag(ErrorTag):
    """Error tags specific to the report module."""
    UNSUPPORTED_VERSION = "UNSUPPORTED_VERSION"
    """Report version is invalid or unsupported."""

    INVALID_VERSION_TYPE = "INVALID_VERSION_TYPE"
    """Report version type is invalid; expected an integer."""
