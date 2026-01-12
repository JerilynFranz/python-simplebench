"""Error tags for VCSInfo reporter base class."""

from simplebench.doc_utils import enum_docstrings
from simplebench.exceptions import ErrorTag


@enum_docstrings
class _VCSInfoErrorTag(ErrorTag):
    """Error tags for VCSInfo reporter base class."""

    INVALID_HASH_ID_TYPE = 'INVALID_HASH_ID_TYPE'
    """The hash_id param type must be a string."""
    INVALID_HASH_ID_VALUE = 'INVALID_HASH_ID_VALUE'
    """The hash_id param value is not a valid hash ID.
    Must be either empty or a 64-character hexadecimal string."""
    INVALID_HASH_ID_STRUCTURE = 'INVALID_HASH_ID_STRUCTURE'
    """The hash_id param value is not a 64-character hexadecimal string."""
    INVALID_VCS_TYPE = 'INVALID_VCS_TYPE'
    """The vcs param type must be a string."""
    INVALID_VCS_VALUE = 'INVALID_VCS_VALUE'
    """The vcs param value cannot be a blank or empty string."""
    INVALID_COMMIT_ID_TYPE = 'INVALID_COMMIT_ID_TYPE'
    """The commit_id param type must be a string."""
    INVALID_COMMIT_ID_VALUE = 'INVALID_COMMIT_ID_VALUE'
    """The commit_id param value cannot be a blank or empty string."""
    INVALID_COMMIT_DATETIME_TYPE = 'INVALID_COMMIT_DATETIME_TYPE'
    """The commit_datetime param type must be a string."""
    INVALID_COMMIT_DATETIME_VALUE = 'INVALID_COMMIT_DATETIME_VALUE'
    """The commit_datetime param value must be a valid ISO 8601 datetime string."""
    INVALID_BRANCH_TYPE = 'INVALID_BRANCH_TYPE'
    """The branch param type must be a string."""
    INVALID_REPOSITORY_URL_TYPE = 'INVALID_REPOSITORY_URL_TYPE'
    """The repository_url param type must be a string."""
    INVALID_IS_DIRTY_TYPE = 'INVALID_IS_DIRTY_TYPE'
    """The is_dirty param type must be a boolean."""
    JSON_SCHEMA_VALIDATION_ERROR = 'JSON_SCHEMA_VALIDATION_ERROR'
    """The JSON data does not conform to the expected schema."""
