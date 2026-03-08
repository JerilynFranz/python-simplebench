"""ErrorTags for JSON Reporter for benchmark results using JSON files."""

from enum import auto
from simplebench.doc_utils import enum_docstrings
from simplebench.exceptions import ErrorTag


@enum_docstrings
class _JSONOptionsErrorTag(ErrorTag):
    """Error tags for JSON options."""

    INVALID_FULL_DATA_ARG_TYPE = auto()
    """The ``full_data`` argument is of an invalid type (expected :class:`bool`)."""
