"""Hg (Mercurial) Info record."""
from dataclasses import asdict, dataclass


@dataclass(frozen=True, kw_only=True, repr=True)
class HgInfo:
    """Dataclass to hold Hg Info about the repository.

    The information is gathered from the 'hg' command line tool and
    gives basic information about the current repository state.

    It is intended to be serialized to JSON for reporting purposes
    and used in filtering benchmark results based on VCS matching.

    Attributes:
        branch_name (str): The current branch name.
        changeset_id (str): The current changeset id for HEAD
        date (str): The date of the current HEAD commit in ISO8601 format.
        dirty (bool): Whether there are uncommitted changes in the working directory.
    """
    branch_name: str
    changeset_id: str
    date: str
    dirty: bool

    def to_dict(self) -> dict[str, str | bool]:
        """Convert to dictionary for JSON serialization.

        :return: Dictionary representation of GitInfo.
        """
        return asdict(self)
