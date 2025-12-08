"""Hg (Mercurial) Version Control System utilities."""
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

from .exceptions import _HgErrorTag
from .exit_codes import _HgExitCode
from .hg_info import HgInfo

# Global caches for hg availability and version.
# These are cached globally because the state of the hg executable is system-wide
# and probing it is an expensive operation we want to avoid doing for every Hg
# instantiation.
_HG_IS_AVAILABLE_CACHE: bool | None = None
"""Cache for hg availability check across Hg instances."""

_HG_VERSION_CACHE: str | None = None
"""Cache for hg version string across Hg instances."""


class Hg:
    """Mercurial (hg) Version Control System facade."""

    def __init__(self, cwd: Path | None = None) -> None:
        """Initialize the Hg facade.

        If cwd is provided, sets the initial hg working directory.
        """
        if cwd is not None:
            self.hg_cwd = validate_type(
                cwd, Path, "cwd",
                _HgErrorTag.INVALID_HG_CWD_ARG_TYPE)
        else:
            self.hg_cwd = None

        self._hg_available: bool = False
        """Indicates if hg is available on the system (private attribute)."""

    def run(self, cmd: Sequence[str], cwd: Path | None = None) -> str:
        """Run an hg command and return its output.

        If cwd is None, uses the current working directory set either by
        hg_cwd() or os.getcwd() if hg_cwd() is None.

        The cwd parameter allows overriding the hg working directory but
        does not change the hg_cwd() setting.

        Basically it allows running hg commands in different directories
        without changing the Hg object's working directory state

        Precedence for working directory:
        1. cwd parameter if provided
        2. hg_cwd() if set
        3. Current working directory (Path.cwd())

        :param cmd: List of command arguments for hg.
        :param cwd: The working directory to run the command in.
            If None, uses the current working directory.
        :return: The command output as a string, or None if an error occurred.
        :raises SimpleBenchTypeError: If cmd is not a sequence of strings or if cwd is not a Path or None.
        :raises SimpleBenchRepositoryActionFailedError: If the command fails.
        :raises SimpleBenchSubprocessExecutableNotFoundError: If the hg command is not found.
        """
        cmd = validate_sequence_of_str(
            cmd, "cmd",
            _HgErrorTag.INVALID_CMD_ARG_TYPE,
            _HgErrorTag.INVALID_CMD_ARG_ELEMENT_VALUE,
            allow_empty=False, allow_blank=False)

        if cwd is not None:
            cwd = validate_type(
                cwd, Path, "cwd",
                _HgErrorTag.INVALID_HG_CWD_ARG_TYPE)

        working_cwd = cwd or self.hg_cwd or Path.cwd()
        try:
            result = subprocess.run(
                ["hg"] + cmd,
                cwd=str(working_cwd),
                capture_output=True,
                text=True,
                check=True
            )
        except FileNotFoundError as exc:
            raise SimpleBenchSubprocessExecutableNotFoundError(
                "The 'hg' command line tool was not found.",
                tag=_HgErrorTag.HG_NOT_AVAILABLE
            ) from exc
        except subprocess.CalledProcessError as exc:
            if exc.returncode == _HgExitCode.REPO_NOT_FOUND:
                raise SimpleBenchNotARepositoryError(
                    "The specified directory is not a Mercurial (hg) repository.",
                    tag=_HgErrorTag.HG_NOT_A_REPOSITORY
                ) from exc
            else:
                raise SimpleBenchRepositoryActionFailedError(
                    f"The hg command failed with exit code {exc.returncode}: {exc.stderr.strip()}",
                    tag=_HgErrorTag.HG_COMMAND_FAILED
                ) from exc
        return result.stdout.strip()

    @property
    def hg_cwd(self) -> Path | None:
        """The current hg working directory.

        :return: The current hg working directory as a Path, or None if not set.
        """
        hg_cwd: Path | None = getattr(self, '_hg_cwd', None)
        return hg_cwd

    @hg_cwd.setter
    def hg_cwd(self, value: Path | None) -> None:
        """Set the current hg working directory.

        :param value: The new hg working directory as a Path, or None to unset.
        :type value: Path | None
        """
        if value is not None and not isinstance(value, Path):
            raise SimpleBenchTypeError(
                f"Expected a Path or None for 'hg_cwd', got: {type(value)}",
                tag=_HgErrorTag.INVALID_HG_CWD_ARG_TYPE)
        self._hg_cwd = value

    @property
    def version(self) -> str:
        """Return the hg version string.

        :return: output of 'hg version --template "{ver}"' as a string.
        :raises SimpleBenchRepositoryActionFailedError: If the 'hg version' command fails.
        :raises SimpleBenchSubprocessExecutableNotFoundError: If the hg command is not available.
        """
        global _HG_VERSION_CACHE  # pylint: disable=global-statement
        if _HG_VERSION_CACHE is None:
            _HG_VERSION_CACHE = self.run(["version", "--template", "{ver})"])
        return _HG_VERSION_CACHE

    @property
    def is_available(self) -> bool:
        """Return whether the 'hg' command line tool is available.

        :return: True if hg is available, False otherwise.
        :raises subprocess.CalledProcessError: If the hg command fails.
        :raises FileNotFoundError: If the hg command is not found.
        """
        global _HG_IS_AVAILABLE_CACHE  # pylint: disable=global-statement
        if _HG_IS_AVAILABLE_CACHE is None:
            try:
                hg_version = self.run(cmd=["version"])
                hg_regex = re.compile(r'Mercurial\s+Distributed\s+SCM', re.IGNORECASE)
                match = hg_regex.search(hg_version)
                _HG_IS_AVAILABLE_CACHE = bool(match)

            # These exceptions indicate hg is not available
            except (FileNotFoundError, subprocess.CalledProcessError):
                _HG_IS_AVAILABLE_CACHE = False

            # Other exceptions are not caught and will propagate

        return _HG_IS_AVAILABLE_CACHE

    def validate_available(self) -> None:
        """Validate that the 'hg' command line tool is available.

        This is done by calling is_available() and raising an exception if not available.
        It is more-or-less a 'backstop' validator for other hg functions to ensure they
        are only called when hg is available.

        :raises SimpleBenchSubprocessExecutableNotFoundError: If hg is not available.
        :raises SimpleBenchRepositoryActionFailedError: If the test 'hg version' command fails.
        """
        if not self.is_available:
            raise SimpleBenchSubprocessExecutableNotFoundError(
                "The 'hg' command line tool is not available.",
                tag=_HgErrorTag.HG_NOT_AVAILABLE
            )

    def is_repo(self, cwd: Path | None = None) -> bool:
        """Check if the current directory is inside a hg repository.

        :param cwd: The working directory to check. If None, uses the current hg_cwd or os.getcwd().
        :return: True if inside a hg repository, False otherwise.
        :raises subprocess.CalledProcessError: If the command fails.
        :raises FileNotFoundError: If the hg command is not found.
        """
        try:
            root_path = self.run(cmd=["root"], cwd=cwd)
            return root_path is not None
        except SimpleBenchNotARepositoryError:
            return False

    def validate_is_repo(self, cwd: Path | None = None) -> None:
        """Check if the current directory is inside a hg repository.

        This is done by calling is_repo() and raising an exception if not in a repo.

        Normally, code interacting with hg repositories should check for
        repository presence via calling is_repo() before calling any other
        hg-related functions.

        It is more-or-less a 'backstop' validator for other hg functions to
        ensure they are only called when hg is available and from inside a
        valid hg repository.

        :param cwd: The working directory to check. If None, uses the current hg_cwd or os.getcwd().
        :raise SimpleBenchNotARepositoryError: If not inside a hg repository.
        :raise SimpleBenchSubprocessExecutableNotFoundError: If the hg command is not found.
        :raise SimpleBenchRepositoryActionFailedError: If the command fails.
        """
        if not self.is_repo(cwd=cwd):
            raise SimpleBenchNotARepositoryError(
                "The current directory is not inside a Mercurial (hg) repository.",
                tag=_HgErrorTag.HG_NOT_A_REPOSITORY
            )

    def root(self, cwd: Path | None = None) -> Path:
        """Get the root path of the hg repository.

        :param cwd: The working directory to check. If None, uses the current hg_cwd or os.getcwd().
        :return: The root path as a Path object.
        :raises SimpleBenchNotARepositoryError: If not inside a hg repository.
        :raises SimpleBenchRepositoryActionFailedError: If the command fails.
        :raises SimpleBenchSubprocessExecutableNotFoundError: If the hg command is not found.
        """
        self.validate_is_repo(cwd=cwd)
        return Path(self.run(cmd=["root"], cwd=cwd))

    def is_dirty(self, cwd: Path | None = None) -> bool:
        """Check if the hg repository has uncommitted changes.

        :param cwd: The working directory to check. If None, uses the current hg_cwd or os.getcwd().
        :return: True if there are uncommitted changes, False if clean, or None if not a hg repository.
        :raises SimpleBenchNotARepositoryError: If not inside a hg repository.
        :raises SimpleBenchRepositoryActionFailedError: If the hg command fails.
        :raises SimpleBenchSubprocessExecutableNotFoundError: If the hg command is not found
        """
        self.validate_is_repo(cwd=cwd)
        # If there is any output from status(), the repo is dirty
        return bool(self.status(cwd=cwd))

    def status(self, cwd: Path | None = None) -> str:
        """Run 'hg status' and return its output.

        Any output other than an empty string indicates uncommitted changes.

        :param cwd: The working directory to check. If None, uses the current hg_cwd or os.getcwd().
        :return: The command output as a string.
        :raises SimpleBenchNotARepositoryError: If not inside a hg repository.
        :raises SimpleBenchRepositoryActionFailedError: If the hg command fails.
        :raises SimpleBenchSubprocessExecutableNotFoundError: If the hg command is not found.
        """
        self.validate_is_repo(cwd=cwd)
        return self.run(cmd=["status"], cwd=cwd)

    def head(self, cwd: Path | None = None) -> HgInfo:
        """Fetch hg repository information for the current HEAD.

        The result is parsed from 'hg id' command

        :param cwd: The working directory to check. If None, uses the current hg_cwd or os.getcwd().
        :return: A HgInfo object with hg info.
        :raises SimpleBenchRepositoryActionFailedError: If the command fails.
        :raises SimpleBenchSubprocessExecutableNotFoundError: If the hg command is not found.
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
        return HgInfo(
            branch_name=branch_name,
            changeset_id=changeset_id,
            date=date,
            dirty=dirty
        )
