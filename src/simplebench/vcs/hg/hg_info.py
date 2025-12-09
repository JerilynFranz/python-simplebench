"""Version Control System record for Hg (Mercurial)."""
from ..vcs_info import VCSInfo
from ..vcs_type import VCSType


class HgInfo(VCSInfo):
    """Dataclass to hold Hg (Mercurial) repository information.

    Attributes:
        branch (str): The current branch name.
        commit_id (str): The current changeset hash.
        date (str): The date of the current commit in ISO format.
        dirty (bool): Whether there are uncommitted changes in the working directory.
    """
    def __init__(self, branch: str, commit_id: str, commit_datetime: str, dirty: bool) -> None:
        """Initialize HgInfo with branch, commit, commit_datetime, and dirty status.

        :param branch: The current branch name.
        :param commit_id: The current commit hash.
        :param commit_datetime: The date of the current commit in ISO format.
        :param dirty: Whether there are uncommitted changes in the working directory.
        """
        super().__init__(
            vcs_type=VCSType.HG,
            branch=branch,
            commit_id=commit_id,
            commit_datetime=commit_datetime,
            dirty=dirty,
        )
