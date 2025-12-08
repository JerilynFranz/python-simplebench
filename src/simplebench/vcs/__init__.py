"""VCS information collection module."""
from .git import Git, GitInfo
from .hg import Hg, HgInfo

__all__ = [
    "GitInfo",
    "Hg",
    "HgInfo",
    "Git",
]
