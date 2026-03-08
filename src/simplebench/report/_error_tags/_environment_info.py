"""Error tags for generic environment issues."""

from enum import auto
from simplebench.doc_utils import enum_docstrings
from simplebench.exceptions import ErrorTag


@enum_docstrings
class _EnvironmentInfoErrorTag(ErrorTag):
    """Error tags for generic environment issues."""

    INVALID_DATA_TYPE = auto()
    """The provided data is not of the expected type."""

    INVALID_HASH_ID_TYPE = auto()
    """The provided hash_id is not a string."""

    INVALID_HASH_ID_VALUE = auto()
    """The provided hash_id is not a valid 64-character hexadecimal string."""

    INVALID_TITLE_TYPE = auto()
    """The provided title is not a string."""

    INVALID_TITLE_VALUE = auto()
    """The provided title is an empty string."""

    INVALID_DESCRIPTION = auto()
    """The provided description is not a string."""

    INVALID_SEMANTIC_TYPE_TYPE = auto()
    """The provided semantic_type is not a string."""

    INVALID_SEMANTIC_TYPE_VALUE = auto()
    """The provided semantic_type does not match the required pattern 'namespace::type_name'."""

    INVALID_TYPE_VALUE = auto()
    """The provided type field does not match the expected value for this class."""

    INVALID_VERSION_VALUE = auto()
    """The provided version field does not match the expected value for this class."""
