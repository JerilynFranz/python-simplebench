"""
ErrorTags for simplebench.report.validate.report_element_typed_dict.cache
"""
from simplebench.doc_utils import enum_docstrings
from simplebench.exceptions import ErrorTag


@enum_docstrings
class _ReportElementTypedDictCacheErrorTag(ErrorTag):
    """Error tags for report element validation errors."""
    INVALID_CACHE_SIZE = "INVALID_CACHE_SIZE"
    """The provided cache size is invalid."""
    INVALID_CACHE_SIZE_TYPE = "INVALID_CACHE_SIZE_TYPE"
    """The provided cache size is not an integer."""
