"""Errors related to Git operations."""
from simplebench.enums import enum_docstrings
from simplebench.exceptions import ErrorTag


@enum_docstrings
class _GitErrorTag(ErrorTag):
    """Error tags for Git operations."""
    GIT_NOT_AVAILABLE = "GIT_NOT_AVAILABLE"
    """Git is not available on the system."""
    GIT_COMMAND_FAILED = "GIT_COMMAND_FAILED"
    """The git command failed to execute properly."""
    GIT_NOT_A_REPOSITORY = "GIT_NOT_A_REPOSITORY"
    """The specified directory is not a Git repository."""
    INVALID_GIT_CWD_ARG_TYPE = "INVALID_GIT_CWD_ARG_TYPE"
    """The git_cwd argument provided is not a Path or None."""
    INVALID_CMD_ARG_TYPE = "INVALID_CMD_ARG_TYPE"
    """The cmd argument provided is not a list of strings."""
    INVALID_CMD_ARG_ELEMENT_VALUE = "INVALID_CMD_ARG_ELEMENT_VALUE"
    """An element in the cmd argument list is not a valid string."""
