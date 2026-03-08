"""
ErrorTags for simplebench.report.validate.report_element_typed_dict.cache
"""

from enum import auto
from simplebench.doc_utils import enum_docstrings
from simplebench.exceptions import ErrorTag


@enum_docstrings
class _ValidationCacheErrorTag(ErrorTag):
    """Error tags for report element validation errors."""

    NONE_VALUE_NOT_ALLOWED = auto()
    """The value provided to create a CacheKey was None."""
    INVALID_CACHE_SIZE = auto()
    """The provided cache size is invalid."""
    INVALID_CACHE_SIZE_TYPE = auto()
    """The provided cache size is not an integer."""
