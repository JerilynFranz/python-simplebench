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
    KWARGS_NOT_A_MAPPING = 'KWARGS_NOT_A_MAPPING'
    """The 'kwargs' value is not a valid mapping."""
    VARIATION_MARKS_NOT_A_MAPPING = 'VARIATION_MARKS_NOT_A_MAPPING'
    """The 'variation_marks' value is not a valid mapping."""
