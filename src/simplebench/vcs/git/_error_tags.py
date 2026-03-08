"""Errors related to Git operations."""

from enum import auto
from simplebench.doc_utils import enum_docstrings
from simplebench.exceptions import ErrorTag


@enum_docstrings
class _GitErrorTag(ErrorTag):
    """Error tags for Git operations by the Git class."""

    GIT_NOT_AVAILABLE = auto()
    """Git is not available on the system."""
    GIT_COMMAND_FAILED = auto()
    """The git command failed to execute properly."""
    GIT_NOT_A_REPOSITORY = auto()
    """The specified directory is not a Git repository."""
    INVALID_GIT_CWD_ARG_TYPE = auto()
    """The git_cwd argument provided is not a Path or None."""
    INVALID_CMD_ARG_TYPE = auto()
    """The cmd argument provided is not a list of strings."""
    INVALID_CMD_ARG_ELEMENT_VALUE = auto()
    """An element in the cmd argument list is not a valid string."""
    USER_INTERRUPT = auto()
    """The git command was interrupted by the user."""
    COMMIT_ID_INVALID_TYPE = auto()
    """The commit_id attribute is not of type string."""
    COMMIT_ID_INVALID_VALUE = auto()
    """The commit_id attribute does not match expected format."""
