"""ErrorTags for the runners module."""

from simplebench.doc_utils import enum_docstrings
from simplebench.exceptions import ErrorTag


@enum_docstrings
class _RunnerErrorTag(ErrorTag):
    """ErrorTags for the BenchmarkRunner module."""

    NOT_A_CASE = 'NOT_A_CASE'
    """The 'case' value is not a valid Case instance."""
    NOT_A_SESSION = 'NOT_A_SESSION'
    """The 'session' value is not a valid Session instance."""
    VARIATION_MARKS_NOT_A_VARIATION_MARKS = 'VARIATION_MARKS_NOT_A_VARIATION_MARKS'
    """The 'variation_marks' value is not a valid VariationMarks instance."""
