"""Error tags for Values type validation."""

from enum import auto
from simplebench.doc_utils import enum_docstrings
from simplebench.exceptions import ErrorTag


@enum_docstrings
class _ValuesErrorTag(ErrorTag):
    """Error tags for Values type validation."""

    INVALID_VALUES_TYPE = auto()
    """The provided values is not an Iterable of int or float."""
    INVALID_VALUES_CONTENT_TYPE = auto()
    """One or more items in the provided values iterable is not an int or float."""
    VALUES_NOT_ELEMENT_COLLECTION_OR_CORE_DATA_SEQUENCE = auto()
    """The provided values is not an ElementCollection or CoreDataSequence."""
