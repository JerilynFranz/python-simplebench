"""Error tags for the Mark module."""

from simplebench.doc_utils import enum_docstrings
from simplebench.exceptions import ErrorTag


@enum_docstrings
class _MarkErrorTag(ErrorTag):
    """Error tags for the Mark module."""

    LABEL_ARG_TYPE = 'LABEL_ARG_TYPE'
    """Invalid label argument passed to the Mark() constructor - must be a string"""
    LABEL_ARG_EMPTY = 'LABEL_ARG_EMPTY'
    """Invalid label argument passed to the Mark() constructor - must not be an empty string"""
    LABEL_ARG_NAN = 'LABEL_ARG_NAN'
    """Invalid label argument passed to the Mark() constructor - must not be NaN"""
