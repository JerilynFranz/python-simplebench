"""ErrorTags for JSON Reporter for benchmark results using JSON files."""
from simplebench.enums import enum_docstrings
from simplebench.exceptions import ErrorTag


@enum_docstrings
class JSONOptionsErrorTag(ErrorTag):
    """Error tags for JSON options."""
    INVALID_FULL_DATA_ARG_TYPE = "invalid_full_data_ARG_TYPE"
    """The 'full_data' argument is of an invalid type (expected bool)."""
