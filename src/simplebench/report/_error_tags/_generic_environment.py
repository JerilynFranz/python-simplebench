"""Error tags for generic environment issues."""

from simplebench.doc_utils import enum_docstrings
from simplebench.exceptions import ErrorTag


@enum_docstrings
class _GenericEnvironmentErrorTag(ErrorTag):
    """Error tags for generic environment issues."""

    INVALID_DATA_TYPE = 'INVALID_DATA_TYPE'
    """The provided data is not of the expected type."""

    INVALID_HASH_ID_TYPE = 'INVALID_HASH_ID_TYPE'
    """The provided hash_id is not a string."""

    INVALID_HASH_ID_VALUE = 'INVALID_HASH_ID_VALUE'
    """The provided hash_id is not a valid 64-character hexadecimal string."""
