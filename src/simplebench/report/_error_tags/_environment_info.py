"""Error tags for generic environment issues."""

from simplebench.doc_utils import enum_docstrings
from simplebench.exceptions import ErrorTag


@enum_docstrings
class _EnvironmentInfoErrorTag(ErrorTag):
    """Error tags for generic environment issues."""

    INVALID_DATA_TYPE = 'INVALID_DATA_TYPE'
    """The provided data is not of the expected type."""

    INVALID_HASH_ID_TYPE = 'INVALID_HASH_ID_TYPE'
    """The provided hash_id is not a string."""

    INVALID_HASH_ID_VALUE = 'INVALID_HASH_ID_VALUE'
    """The provided hash_id is not a valid 64-character hexadecimal string."""

    INVALID_TITLE_TYPE = 'INVALID_TITLE_TYPE'
    """The provided title is not a string."""

    INVALID_TITLE_VALUE = 'INVALID_TITLE_VALUE'
    """The provided title is an empty string."""

    INVALID_DESCRIPTION = 'INVALID_DESCRIPTION'
    """The provided description is not a string."""

    INVALID_SEMANTIC_TYPE_TYPE = 'INVALID_SEMANTIC_TYPE_TYPE'
    """The provided semantic_type is not a string."""

    INVALID_SEMANTIC_TYPE_VALUE = 'INVALID_SEMANTIC_TYPE_VALUE'
    """The provided semantic_type does not match the required pattern 'namespace::type_name'."""

    INVALID_TYPE_VALUE = 'INVALID_TYPE_VALUE'
    """The provided type field does not match the expected value for this class."""

    INVALID_VERSION_VALUE = 'INVALID_VERSION_VALUE'
    """The provided version field does not match the expected value for this class."""
