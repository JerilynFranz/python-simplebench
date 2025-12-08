"""Hg (Mercurial) Info record."""
from dataclasses import asdict, dataclass

from .vcs_type import VCSType


@dataclass(frozen=True, kw_only=True, repr=True)
class VCSInfo:
    """Dataclass to hold VCS Info about the repository.

    This a base class for holding version control system information that
    is common across different VCS types.

    The information is gathered from the appropriate VCS command line tools and
    gives basic information about the current repository state.

    It is intended to be serialized to JSON for reporting purposes
    and used in filtering benchmark results based on VCS matching.

    Attributes:
        vcs_type (VCSType): The type of version control system (e.g., 'git', 'hg').
        branch (str): The current branch name.
        commit_id (str): The current changeset id for HEAD
        date (str): The date of the current HEAD commit in ISO8601 format.
        dirty (bool): Whether there are uncommitted changes in the working directory.
    """
    vcs_type: VCSType
    branch: str
    commit_id: str
    date: str
    dirty: bool

    def to_dict(self) -> dict[str, str | bool]:
        """Convert to dictionary for JSON serialization.

        :return: Dictionary representation of GitInfo.
        """
        return asdict(self)
