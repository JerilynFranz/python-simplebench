"""Error tags for SimpleBench types"""

from simplebench.doc_utils import enum_docstrings
from simplebench.exceptions import ErrorTag


@enum_docstrings
class _CoreTypeErrorTags(ErrorTag):
    """Error tags for core type errors."""

    INVALID_CACHE_TYPE = 'INVALID_CACHE_TYPE'
    """The provided cache size is not an integer."""
    INVALID_CACHE_SIZE = 'INVALID_CACHE_SIZE'
    """The provided cache size is less than 1."""
