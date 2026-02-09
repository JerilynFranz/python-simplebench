"""Error tags for immutable validators."""
from simplebench.doc_utils import enum_docstrings
from simplebench.exceptions import ErrorTag


@enum_docstrings
class _ImmutableErrorTag(ErrorTag):
    """Error tags for immutable validators."""

    RECURSION_LIMIT_EXCEEDED = "RECURSION_LIMIT_EXCEEDED"
    """Indicates that the maximum recursion depth was exceeded while checking immutability."""

    OBJECT_NOT_IMMUTABLE = "OBJECT_NOT_IMMUTABLE"
    """Indicates that the provided object is not immutable."""

    NAME_NOT_STRING = "NAME_NOT_STRING"
    """Indicates that the 'name' parameter is not a string."""

    NAME_IS_EMPTY_OR_BLANK_STRING = "NAME_IS_EMPTY_OR_BLANK_STRING"
    """Indicates that the 'name' parameter is an empty or blank string."""

    DEPTH_NOT_INTEGER = "DEPTH_NOT_INTEGER"
    """Indicates that the 'depth' parameter is not an integer."""

    DEPTH_NOT_POSITIVE_INTEGER = "DEPTH_NOT_POSITIVE_INTEGER"
    """Indicates that the 'depth' parameter is not a positive integer."""

    MESSAGE_NOT_STRING = "MESSAGE_NOT_STRING"
    """Indicates that the 'message' parameter is not a string."""
