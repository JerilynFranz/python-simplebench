"""Errors related to Mercurial (hg) operations."""
from simplebench.enums import enum_docstrings
from simplebench.exceptions import ErrorTag


@enum_docstrings
class _HgErrorTag(ErrorTag):
    """Error tags for Mercurial (hg) operations."""
    HG_NOT_AVAILABLE = "HG_NOT_AVAILABLE"
    """Mercurial (hg) is not available on the system."""
    HG_COMMAND_FAILED = "HG_COMMAND_FAILED"
    """The hg command failed to execute properly."""
    HG_NOT_A_REPOSITORY = "HG_NOT_A_REPOSITORY"
    """The specified directory is not a Mercurial (hg) repository."""
    INVALID_HG_CWD_ARG_TYPE = "INVALID_HG_CWD_ARG_TYPE"
    """The hg_cwd argument provided is not a Path or None."""
    INVALID_CMD_ARG_TYPE = "INVALID_CMD_ARG_TYPE"
    """The cmd argument provided is not a list of strings."""
    INVALID_CMD_ARG_ELEMENT_VALUE = "INVALID_CMD_ARG_ELEMENT_VALUE"
    """An element in the cmd argument list is not a valid string."""
