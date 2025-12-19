"""Error tags for LazyProperty exceptions."""
from simplebench.doc_utils import enum_docstrings
from simplebench.exceptions import ErrorTag


@enum_docstrings
class _LazyPropertyErrorTags(ErrorTag):
    """Error tags for LazyProperty exceptions."""
    INVALID_FUNC = "INVALID_FUNC"
    """The func provided to the LazyProperty constructor is not callable."""
    INVALID_FUNC_WRONG_PARAM_COUNT = "INVALID_FUNC_WRONG_PARAM_COUNT"
    """The func provided to the LazyProperty constructor does not take exactly one parameter."""
