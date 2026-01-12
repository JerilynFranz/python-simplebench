"""Error tags for the Mark module."""

from simplebench.doc_utils import enum_docstrings
from simplebench.exceptions import ErrorTag


@enum_docstrings
class _MarkErrorTag(ErrorTag):
    """Error tags for the Mark module."""

    NAME_ARG_TYPE = 'NAME_ARG_TYPE'
    """Invalid name argument passed to the Mark() constructor - must be a string"""
    NAME_ARG_EMPTY = 'NAME_ARG_EMPTY'
    """Invalid name argument passed to the Mark() constructor - must not be an empty string"""
