"""VCS information collection module."""
from .git import Git, GitInfo
from .hg import Hg, HgInfo
from .utils import identify_repo_starting_path

__all__ = [
    "identify_repo_starting_path",
    "GitInfo",
    "Hg",
    "HgInfo",
    "Git",
]
