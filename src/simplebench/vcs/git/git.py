"""Git Version Control System facade."""
from __future__ import annotations

import re
import subprocess
from pathlib import Path
from typing import Sequence

from simplebench.exceptions import (
    SimpleBenchNotARepositoryError,
    SimpleBenchRepositoryActionFailedError,
    SimpleBenchSubprocessExecutableNotFoundError,
    SimpleBenchTypeError,
)
from simplebench.utils import timestamp_to_iso8601
from simplebench.validators import validate_sequence_of_str, validate_type

from .exceptions import _GitErrorTag
from .exit_codes import _GitExitCode
from .git_info import GitInfo

# Global caches for git availability and version.
# These are cached globally because the state of the git executable is system-wide
# and probing it is an expensive operation we want to avoid doing for every Git
# instantiation.
_GIT_IS_AVAILABLE_CACHE: bool | None = None
"""Cache for git availability check across Git instances."""

_GIT_VERSION_CACHE: str | None = None
"""Cache for git version string across Git instances."""


class Git:
    """Git Version Control System facade."""

    def __init__(self, cwd: Path | None = None) -> None:
        """Initialize the Git facade.

        If cwd is provided, sets the initial git working directory.
        """
        if cwd is not None:
            self.git_cwd = validate_type(
                cwd, Path, "cwd",
                _GitErrorTag.INVALID_GIT_CWD_ARG_TYPE)
        else:
            self.git_cwd = None

    def run(self, cmd: Sequence[str], cwd: Path | None = None) -> str:
        """Run an git command and return its output.

        If cwd is None, uses the current working directory set either by
        git_cwd() or os.getcwd() if git_cwd() is None.

        The cwd parameter allows overriding the git working directory
        while executing the command but does not change the git_cwd() setting.

        Basically it allows running git commands in different directories
        without changing the Git object's working directory state

        Precedence for working directory:
        1. cwd parameter if provided
        2. git_cwd() if set
        3. Current working directory (Path.cwd())

        :param cmd: List of command arguments for git.
        :param cwd: The working directory to run the command in.
            If None, uses the current working directory.
        :return: The command output as a string, or None if an error occurred.
        :raises SimpleBenchTypeError: If cmd is not a sequence of strings or if cwd is not a Path or None.
        :raises SimpleBenchRepositoryActionFailedError: If the command fails.
        :raises SimpleBenchSubprocessExecutableNotFoundError: If the git command is not found.
        """
        cmd = validate_sequence_of_str(
            cmd, "cmd",
            _GitErrorTag.INVALID_CMD_ARG_TYPE,
            _GitErrorTag.INVALID_CMD_ARG_ELEMENT_VALUE,
            allow_empty=False, allow_blank=False)

        if cwd is not None:
            cwd = validate_type(
                cwd, Path, "cwd",
                _GitErrorTag.INVALID_GIT_CWD_ARG_TYPE)

        working_cwd = cwd or self.git_cwd or Path.cwd()

        try:
            result = subprocess.run(
                ["git"] + cmd,
                cwd=str(working_cwd),
                capture_output=True,
                text=True,
                check=True
            )
        except FileNotFoundError as exc:
            raise SimpleBenchSubprocessExecutableNotFoundError(
                "The 'git' command line tool was not found.",
                tag=_GitErrorTag.GIT_NOT_AVAILABLE
            ) from exc
        except subprocess.CalledProcessError as exc:
            if exc.returncode == _GitExitCode.REPO_NOT_FOUND:
                raise SimpleBenchNotARepositoryError(
                    "The specified directory is not a Git repository.",
                    tag=_GitErrorTag.GIT_NOT_A_REPOSITORY
                ) from exc
            else:
                raise SimpleBenchRepositoryActionFailedError(
                    f"The git command failed with exit code {exc.returncode}: {exc.stderr.strip()}",
                    tag=_GitErrorTag.GIT_COMMAND_FAILED
                ) from exc
        return result.stdout.strip()

    @property
    def git_cwd(self) -> Path | None:
        """The current git working directory.

        :return: The current git working directory as a Path, or None if not set.
        """
        git_cwd: Path | None = getattr(self, '_git_cwd', None)
        return git_cwd

    @git_cwd.setter
    def git_cwd(self, value: Path | None) -> None:
        """Set the current git working directory.

        :param value: The new git working directory as a Path, or None to unset.
        :type value: Path | None
        """
        if value is not None and not isinstance(value, Path):
            raise SimpleBenchTypeError(
                f"Expected a Path or None for 'git_cwd', got: {type(value)}",
                tag=_GitErrorTag.INVALID_GIT_CWD_ARG_TYPE)
        self._git_cwd = value

    @property
    def version(self) -> str:
        """Return the git version string.

        :return: output of 'git --version"' with version number extracted.
        :raises SimpleBenchRepositoryActionFailedError: If the 'git version' command fails.
        :raises SimpleBenchSubprocessExecutableNotFoundError: If the git command is not available.
        """
        global _GIT_VERSION_CACHE  # pylint: disable=global-statement
        if _GIT_VERSION_CACHE is None:
            raw_version = self.run(["--version"])
            git_version_regex = re.compile(r'git version (\d+\.\d+\.\d+)')
            match = git_version_regex.search(raw_version)
            if match is not None:
                _GIT_VERSION_CACHE: str = match.group(1)
            else:
                _GIT_VERSION_CACHE = raw_version

        return _GIT_VERSION_CACHE

    @property
    def is_available(self) -> bool:
        """Return whether the 'git' command line tool is available.

        :return: True if git is available, False otherwise.
        :raises subprocess.CalledProcessError: If the git command fails.
        :raises FileNotFoundError: If the git command is not found.
        """
        global _GIT_IS_AVAILABLE_CACHE  # pylint: disable=global-statement
        if _GIT_IS_AVAILABLE_CACHE is None:
            try:
                git_version = self.run(cmd=["--version"])
                git_regex = re.compile(r'git version', re.IGNORECASE)
                match = git_regex.search(git_version)
                _GIT_IS_AVAILABLE_CACHE = bool(match)

            # These exceptions indicate git is not available
            except (FileNotFoundError, subprocess.CalledProcessError):
                _GIT_IS_AVAILABLE_CACHE = False

            # Other exceptions are not caught and will propagate

        return _GIT_IS_AVAILABLE_CACHE

    def validate_available(self) -> None:
        """Validate that the 'git' command line tool is available.

        This is done by calling is_available() and raising an exception if not available.
        It is more-or-less a 'backstop' validator for other git functions to ensure they
        are only called when git is available.

        :raises SimpleBenchSubprocessExecutableNotFoundError: If git is not available.
        :raises SimpleBenchRepositoryActionFailedError: If the test 'git version' command fails.
        """
        if not self.is_available:
            raise SimpleBenchSubprocessExecutableNotFoundError(
                "The 'git' command line tool is not available.",
                tag=_GitErrorTag.GIT_NOT_AVAILABLE
            )

    def is_repo(self, cwd: Path | None = None) -> bool:
        """Check if the current directory is inside a git repository.

        :param cwd: The working directory to check. If None, uses the current git_cwd or os.getcwd().
        :return: True if inside a git repository, False otherwise.
        :raises subprocess.CalledProcessError: If the command fails.
        :raises FileNotFoundError: If the git command is not found.
        """
        try:
            root_path = self.run(cmd=["status"], cwd=cwd)
            return root_path is not None
        except SimpleBenchNotARepositoryError:
            return False

    def validate_is_repo(self, cwd: Path | None = None) -> None:
        """Check if the current directory is inside a git repository.

        This is done by calling is_repo() and raising an exception if not in a repo.

        Normally, code interacting with git repositories should check for
        repository presence via calling is_repo() before calling any other
        git-related functions.

        It is more-or-less a 'backstop' validator for other git functions to
        ensure they are only called when git is available and from inside a
        valid git repository.

        :param cwd: The working directory to check. If None, uses the current git_cwd or os.getcwd().
        :raise SimpleBenchNotARepositoryError: If not inside a git repository.
        :raise SimpleBenchSubprocessExecutableNotFoundError: If the git command is not found.
        :raise SimpleBenchRepositoryActionFailedError: If the command fails.
        """
        if not self.is_repo(cwd=cwd):
            raise SimpleBenchNotARepositoryError(
                "The current directory is not inside a Git repository.",
                tag=_GitErrorTag.GIT_NOT_A_REPOSITORY
            )

    def root(self, cwd: Path | None = None) -> Path:
        """Get the root path of the git repository.

        :param cwd: The working directory to check. If None, uses the current git_cwd or os.getcwd().
        :return: The root path as a Path object.
        :raises SimpleBenchNotARepositoryError: If not inside a git repository.
        :raises SimpleBenchRepositoryActionFailedError: If the command fails.
        :raises SimpleBenchSubprocessExecutableNotFoundError: If the git command is not found.
        """
        self.validate_is_repo(cwd=cwd)
        return Path(self.run(cmd=["root"], cwd=cwd))

    def is_dirty(self, cwd: Path | None = None) -> bool:
        """Check if the git repository has uncommitted changes.

        :param cwd: The working directory to check. If None, uses the current git_cwd or os.getcwd().
        :return: True if there are uncommitted changes, False if clean, or None if not a git repository.
        :raises SimpleBenchNotARepositoryError: If not inside a git repository.
        :raises SimpleBenchRepositoryActionFailedError: If the git command fails.
        :raises SimpleBenchSubprocessExecutableNotFoundError: If the git command is not found
        """
        self.validate_is_repo(cwd=cwd)
        # If there is any output from status(), the repo is dirty
        return bool(self.status(cwd=cwd))

    def status(self, cwd: Path | None = None) -> str:
        """Run 'git status' and return its output.

        Any output other than an empty string indicates uncommitted changes.

        :param cwd: The working directory to check. If None, uses the current git_cwd or os.getcwd().
        :return: The command output as a string.
        :raises SimpleBenchNotARepositoryError: If not inside a git repository.
        :raises SimpleBenchRepositoryActionFailedError: If the git command fails.
        :raises SimpleBenchSubprocessExecutableNotFoundError: If the git command is not found.
        """
        self.validate_is_repo(cwd=cwd)
        return self.run(cmd=["status"], cwd=cwd)

    def head(self, cwd: Path | None = None) -> GitInfo:
        """Fetch git repository information for the current HEAD.

        The result is parsed from 'git id' command

        :param cwd: The working directory to check. If None, uses the current git_cwd or os.getcwd().
        :return: A GitInfo object with git info.
        :raises SimpleBenchRepositoryActionFailedError: If the command fails.
        :raises SimpleBenchSubprocessExecutableNotFoundError: If the git command is not found.
        """
        self.validate_is_repo(cwd=cwd)
        head_data = self.run(
            cmd=[
                "id", "--rev", ".",
                "--template", "branch: {branch}\ndate: {date}\nchangeset: {node}\n"],
            cwd=cwd)

        branch_name: str = ""
        changeset_id: str = ""
        epoch_date: float = 0.0
        for line in head_data.splitlines():
            if not line:
                continue
            key, value = line.split(": ", 1)
            match key:
                case "branch":
                    branch_name = value.strip()
                case "changeset":
                    changeset_id = value.strip()
                case "date":
                    epoch_date: float = float(value.strip())
                case _:
                    continue
        date: str = timestamp_to_iso8601(epoch_date)
        dirty: bool = self.is_dirty(cwd=cwd)
        return GitInfo(
            branch_name=branch_name,
            changeset_id=changeset_id,
            date=date,
            dirty=dirty
        )
