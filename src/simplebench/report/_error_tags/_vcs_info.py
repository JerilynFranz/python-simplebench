"""Error tags for VCSInfo reporter base class."""

from enum import auto
from simplebench.doc_utils import enum_docstrings
from simplebench.exceptions import ErrorTag


@enum_docstrings
class _VCSInfoErrorTag(ErrorTag):
    """Error tags for VCSInfo reporter base class."""

    INVALID_HASH_ID_TYPE = auto()
    """The hash_id param type must be a string."""
    INVALID_HASH_ID_VALUE = auto()
    """The hash_id param value is not a valid hash ID.
    Must be either empty or a 64-character hexadecimal string."""
    INVALID_HASH_ID_STRUCTURE = auto()
    """The hash_id param value is not a 64-character hexadecimal string."""
    INVALID_VCS_TYPE = auto()
    """The vcs param type must be a string."""
    INVALID_VCS_VALUE = auto()
    """The vcs param value cannot be a blank or empty string."""
    INVALID_COMMIT_ID_TYPE = auto()
    """The commit_id param type must be a string."""
    INVALID_COMMIT_ID_VALUE = auto()
    """The commit_id param value cannot be a blank or empty string."""
    INVALID_COMMIT_DATETIME_TYPE = auto()
    """The commit_datetime param type must be a string."""
    INVALID_COMMIT_DATETIME_VALUE = auto()
    """The commit_datetime param value must be a valid ISO 8601 datetime string."""
    INVALID_BRANCH_TYPE = auto()
    """The branch param type must be a string."""
    INVALID_BRANCH_VALUE = auto()
    """The branch param value cannot be a blank or empty string."""
    INVALID_REPOSITORY_URL_TYPE = auto()
    """The repository_url param type must be a string."""
    INVALID_IS_DIRTY_TYPE = auto()
    """The is_dirty param type must be a boolean."""
    JSON_SCHEMA_VALIDATION_ERROR = auto()
    """The JSON data does not conform to the expected schema."""
