"""VCS exceptions."""

from enum import auto
from simplebench.doc_utils import enum_docstrings
from simplebench.exceptions import ErrorTag


@enum_docstrings
class _VCSInfoErrorTag(ErrorTag):
    """Error tags for VCSInfo related errors."""

    VCS_TYPE_INVALID_TYPE = auto()
    """The provided VCS type is invalid or unsupported."""
    VCS_TYPE_INVALID_VALUE = auto()
    """The provided VCS type value is not supported."""
    BRANCH_INVALID_TYPE = auto()
    """The branch attribute is not of type string."""
    COMMIT_ID_INVALID_TYPE = auto()
    """The commit_id attribute is not of type string."""
    COMMIT_DATETIME_INVALID_TYPE = auto()
    """The commit_datetime attribute is not of type string."""
    COMMIT_DATETIME_INVALID_VALUE = auto()
    """The commit_datetime attribute is not a valid ISO 8601 datetime string."""
    DIRTY_INVALID_TYPE = auto()
    """The dirty attribute is not of type boolean."""
    COMMIT_ID_INVALID_VALUE = auto()
    """The commit_id attribute does not match expected format."""
    NOT_IMPLEMENTED = auto()
    """The method is not implemented in the subclass."""
