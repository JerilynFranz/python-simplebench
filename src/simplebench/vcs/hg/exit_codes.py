"""Mercurial (Hg) exit codes and error tags."""
from enum import IntEnum

from simplebench.enums import enum_docstrings


@enum_docstrings
class HgExitCode(IntEnum):
    """Exit codes for Mercurial (hg) commands."""
    SUCCESS = 0
    """The command completed successfully."""
    GENERAL_ERROR = 1
    """A general error occurred."""
    INPUT_OR_PARSE_ERROR = 10
    """A user input or a configuration-related parsing error occurred.
    It means that the command was used incorrectly."""
    STATE_ERROR = 20
    """The repository is in an invalid state for the requested operation."""
    CONFIG_ERROR = 30
    """A configuration-related error occurred."""
    HOOK_ABORT_ERROR = 40
    """A validation hook failed."""
    STORAGE_ERROR = 50
    """A storage-related error occurred."""
    REMOTE_ERROR = 100
    """A remote repository related error occurred."""
    SECURITY_ERROR = 150
    """A security-related error occurred."""
    INTERVENTION_REQUIRED = 240
    """User intervention is required to continue."""
    CANCELLED = 250
    """The operation was cancelled by the user."""
    REPO_NOT_FOUND = 255
    """The specified directory is not a Mercurial repository."""


def exit_code_to_name(code: int) -> str:
    """Convert an hg exit code to its name.

    If known, returns the name of the exit code. If unknown, returns "UNKNOWN_EXIT_CODE: {value}".

    :param code: The exit code to convert.
    :return: The name of the exit code, or "UKNOWN_EXIT_CODE: {value}" if not found.
    """
    try:
        return HgExitCode(code).name
    except ValueError:
        return f"UNKNOWN_EXIT_CODE: {code}"
