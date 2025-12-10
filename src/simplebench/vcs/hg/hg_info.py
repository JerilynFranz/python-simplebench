"""Version Control System record for Hg (Mercurial)."""
import re

from simplebench.exceptions import SimpleBenchTypeError, SimpleBenchValueError

from ..vcs_info import VCSInfo
from ..vcs_type import VCSType
from .exceptions import _HgErrorTag


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

    def validate_commit_id(self, commit_id: str) -> None:
        """Validate the commit_id.

        :param commit_id: The commit ID to validate.
        :raises SimpleBenchTypeError: If commit_id is not a string or vcs_type is invalid.
        :raises SimpleBenchValueError: If commit_id does not match expected format or length.
        """
        if not isinstance(commit_id, str):
            raise SimpleBenchTypeError(
                f"commit_id must be a string, got {type(commit_id)}",
                tag=_HgErrorTag.COMMIT_ID_INVALID_TYPE)

        if not re.compile(r'^[0-9a-fA-F]{40}$').match(commit_id):
            raise SimpleBenchValueError(
                f"Invalid hg (Mercurial) commit ID: {commit_id}",
                tag=_HgErrorTag.COMMIT_ID_INVALID_VALUE)
