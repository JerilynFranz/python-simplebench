"""VCS exceptions."""

from simplebench.enums import enum_docstrings
from simplebench.exceptions import ErrorTag


@enum_docstrings
class _VCSInfoErrorTag(ErrorTag):
    """Error tags for VCSInfo related errors."""
    VCS_TYPE_INVALID_TYPE = "VCS_TYPE_INVALID_TYPE"
    """The provided VCS type is invalid or unsupported."""
    VCS_TYPE_INVALID_VALUE = "VCS_TYPE_INVALID_VALUE"
    """The provided VCS type value is not supported."""
    BRANCH_INVALID_TYPE = "BRANCH_INVALID_TYPE"
    """The branch attribute is not of type string."""
    COMMIT_ID_INVALID_TYPE = "COMMIT_ID_INVALID_TYPE"
    """The commit_id attribute is not of type string."""
    COMMIT_DATETIME_INVALID_TYPE = "COMMIT_DATETIME_INVALID_TYPE"
    """The commit_datetime attribute is not of type string."""
    COMMIT_DATETIME_INVALID_VALUE = "COMMIT_DATETIME_INVALID_VALUE"
    """The commit_datetime attribute is not a valid ISO 8601 datetime string."""
    DIRTY_INVALID_TYPE = "DIRTY_INVALID_TYPE"
    """The dirty attribute is not of type boolean."""
    COMMIT_ID_INVALID_VALUE = "COMMIT_ID_INVALID_VALUE"
    """The commit_id attribute does not match expected format."""
    NOT_IMPLEMENTED = "NOT_IMPLEMENTED"
    """The method is not implemented in the subclass."""
