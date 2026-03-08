"""Error tags for the Mark module."""

from enum import auto
from simplebench.doc_utils import enum_docstrings
from simplebench.exceptions import ErrorTag


@enum_docstrings
class _MarkErrorTag(ErrorTag):
    """Error tags for the Mark module."""

    LABEL_ARG_TYPE = auto()
    """Invalid label argument passed to the Mark() constructor - must be a string"""
    LABEL_ARG_EMPTY = auto()
    """Invalid label argument passed to the Mark() constructor - must not be an empty string"""
    LABEL_ARG_NAN = auto()
    """Invalid label argument passed to the Mark() constructor - must not be NaN"""
