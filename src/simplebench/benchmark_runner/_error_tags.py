"""ErrorTags for the runners module."""
from simplebench.doc_utils import enum_docstrings
from simplebench.exceptions import ErrorTag


@enum_docstrings
class _RunnerErrorTag(ErrorTag):
    """ErrorTags for the BenchmarkRunner module."""
    NOT_A_CASE = "NOT_A_CASE"
    """The 'case' value is not a valid Case instance."""
    NOT_A_SESSION = "NOT_A_SESSION"
    """The 'session' value is not a valid Session instance."""
    KWARGS_NOT_A_DICT = "KWARGS_NOT_A_DICT"
    """The 'kwargs' value is not a valid dictionary."""
    VARIATION_MARKS_NOT_A_DICT = "VARIATION_MARKS_NOT_A_DICT"
    """The 'variation_marks' value is not a valid dictionary."""
