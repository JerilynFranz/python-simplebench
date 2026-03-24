"""Thread related exceptions for the simplebench package."""

from enum import auto
from simplebench.doc_utils import enum_docstrings
from simplebench.exceptions import ErrorTag


@enum_docstrings
class _ThreadErrorTag(ErrorTag):
    """ErrorTags for timeout-related errors."""

    INVALID_THREAD_ID_TYPE = auto()
    """The provided thread ID is not of type `ThreadId` (`int`)."""
    INVALID_THREAD_ID_VALUE = auto()
    """The provided thread ID is not a non-negative integer."""
