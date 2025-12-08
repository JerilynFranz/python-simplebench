"""VCS information collection module."""
from pathlib import Path

from .git import Git, GitInfo
from .hg import Hg, HgInfo
from .utils import identify_repo_starting_path
from .vcs_info import VCSInfo
from .vcs_type import VCSType

__all__ = [
    "identify_repo_starting_path",
    "GitInfo",
    "Hg",
    "HgInfo",
    "Git",
    "VCSInfo",
    "VCSType",
]


def get_vcs_info(cwd: str | None = None) -> VCSInfo | None:
    """Get VCS information for the repository at the given path.

    This function attempts to identify the version control system (VCS)
    used in the specified directory and retrieves relevant information
    about the repository.

    :param cwd: The path to the repository. If None, uses the current working directory.
    :return: VCSInfo object containing information about the repository.
    :raises RuntimeError: If no supported VCS is found in the specified directory.
    """
    start_path = identify_repo_starting_path(Path(cwd) if cwd else None)

    git = Git(cwd=start_path)
    if git.is_repo():
        return git.head()

    hg = Hg(cwd=start_path)
    if hg.is_repo():
        return hg.head()

    return None
