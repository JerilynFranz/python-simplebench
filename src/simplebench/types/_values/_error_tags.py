"""Error tags for Values type validation."""

from simplebench.doc_utils import enum_docstrings
from simplebench.exceptions import ErrorTag


@enum_docstrings
class _ValuesErrorTag(ErrorTag):
    """Error tags for Values type validation."""

    INVALID_VALUES_TYPE = 'INVALID_VALUES_TYPE'
    """The provided values is not an Iterable of int or float."""
    INVALID_VALUES_CONTENT_TYPE = 'INVALID_VALUES_CONTENT_TYPE'
    """One or more items in the provided values iterable is not an int or float."""
