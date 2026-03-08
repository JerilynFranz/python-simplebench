"""Errors related to Mercurial (hg) operations."""

from enum import auto
from simplebench.doc_utils import enum_docstrings
from simplebench.exceptions import ErrorTag


@enum_docstrings
class _HgErrorTag(ErrorTag):
    """Error tags for Mercurial (hg) operations."""

    HG_NOT_AVAILABLE = auto()
    """Mercurial (hg) is not available on the system."""
    HG_COMMAND_FAILED = auto()
    """The hg command failed to execute properly."""
    HG_NOT_A_REPOSITORY = auto()
    """The specified directory is not a Mercurial (hg) repository."""
    INVALID_HG_CWD_ARG_TYPE = auto()
    """The hg_cwd argument provided is not a Path or None."""
    INVALID_CMD_ARG_TYPE = auto()
    """The cmd argument provided is not a list of strings."""
    INVALID_CMD_ARG_ELEMENT_VALUE = auto()
    """An element in the cmd argument list is not a valid string."""
    COMMIT_ID_INVALID_TYPE = auto()
    """The commit_id attribute is not of type string."""
    COMMIT_ID_INVALID_VALUE = auto()
    """The commit_id attribute does not match expected format."""
