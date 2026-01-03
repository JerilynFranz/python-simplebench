"""
ErrorTags for simplebench.report.validate.report_element_typed_dict.cache
"""
from simplebench.doc_utils import enum_docstrings
from simplebench.exceptions import ErrorTag


@enum_docstrings
class _ValidationCacheErrorTag(ErrorTag):
    """Error tags for report element validation errors."""
    NONE_VALUE_NOT_ALLOWED = "NONE_VALUE_NOT_ALLOWED"
    """The value provided to create a CacheKey was None."""
    INVALID_CACHE_SIZE = "INVALID_CACHE_SIZE"
    """The provided cache size is invalid."""
    INVALID_CACHE_SIZE_TYPE = "INVALID_CACHE_SIZE_TYPE"
    """The provided cache size is not an integer."""
