"""Errors related to Git operations.

This module defines Git-specific exit codes and error tags
"""
from enum import Enum, IntEnum

from simplebench.enums import enum_docstrings


@enum_docstrings
class CommonCode(str, Enum):
    """Well-known Git exit codes across various commands."""
    SUCCESS = "SUCCESS"
    """The command completed successfully."""
    GENERAL_ERROR = "GENERAL_ERROR"
    """A general error occurred."""
    MISUSE_OF_SHELL_BUILTINS = "MISUSE_OF_SHELL_BUILTINS"
    """Misuse of shell builtins."""
    COMMAND_NOT_FOUND = "COMMAND_NOT_FOUND"
    """Command not found."""
    INVALID_ARGUMENTS = "INVALID_ARGUMENTS"
    """Invalid arguments were provided to the command."""
    NOT_A_REPOSITORY = "NOT_A_REPOSITORY"
    """The specified directory is not a Git repository."""
    USER_INTERRUPT = "USER_INTERRUPT"
    """The git command was interrupted by the user."""


@enum_docstrings
class BranchExitCode(IntEnum):
    """'git branch' command error codes."""
    NOT_A_REPOSITORY = 128
    """The specified directory is not a Git repository."""
    USER_INTERRUPT = 130
    """The git branch command was interrupted by the user."""


@enum_docstrings
class LogExitCode(IntEnum):
    """'git log' command error codes."""
    NOT_A_REPOSITORY = 128
    """The specified directory is not a Git repository."""
    USER_INTERRUPT = 130
    """The git log command was interrupted by the user."""


@enum_docstrings
class RevParseExitCode(IntEnum):
    """'git rev-parse' command error codes."""
    NOT_A_REPOSITORY = 128
    """The specified directory is not a Git repository."""
    USER_INTERRUPT = 130
    """The git rev-parse command was interrupted by the user."""


@enum_docstrings
class StatusExitCode(IntEnum):
    """'git status' command error codes."""
    NOT_A_REPOSITORY = 128
    """The specified directory is not a Git repository."""
    USER_INTERRUPT = 130
    """The git status command was interrupted by the user."""


GitExitCode: dict[str, type[IntEnum]] = {
    "branch": BranchExitCode,
    "log": LogExitCode,
    "rev-parse": RevParseExitCode,
    "status": StatusExitCode,
}
"""Git CLI exit codes indexed by command."""
