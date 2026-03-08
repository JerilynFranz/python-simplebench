"""ErrorTags for the runners module."""

from enum import auto
from simplebench.doc_utils import enum_docstrings
from simplebench.exceptions import ErrorTag


@enum_docstrings
class _RunnerErrorTag(ErrorTag):
    """ErrorTags for the BenchmarkRunner module."""

    NOT_A_CASE = auto()
    """The 'case' value is not a valid Case instance."""
    NOT_A_SESSION = auto()
    """The 'session' value is not a valid Session instance."""
    VARIATION_MARKS_NOT_A_VARIATION_MARKS = auto()
    """The 'variation_marks' value is not a valid VariationMarks instance."""
