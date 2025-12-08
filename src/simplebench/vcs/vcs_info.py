"""Hg (Mercurial) Info record."""
from dataclasses import asdict, dataclass

from simplebench.exceptions import SimpleBenchTypeError, SimpleBenchValueError

from .exceptions import _VCSInfoErrorTag
from .vcs_type import VCSType

_SUPPORTED_VCS_TYPES: set[VCSType] = {VCSType.GIT, VCSType.HG}
"""Set of currently supported VCS types for VCSInfo."""


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
        commit_datetime (str): The datetime of the current HEAD commit in ISO8601 format.
        dirty (bool): Whether there are uncommitted changes in the working directory.
    """
    vcs_type: VCSType
    branch: str
    commit_id: str
    commit_datetime: str
    dirty: bool

    def post_init(self) -> None:
        """Post-initialization hook for additional validation or processing."""
        if not isinstance(self.vcs_type, VCSType):
            raise SimpleBenchTypeError(
                f"vcs_type must be an instance of VCSType, got {type(self.vcs_type)}",
                tag=_VCSInfoErrorTag.VCS_TYPE_INVALID_TYPE)
        if self.vcs_type not in _SUPPORTED_VCS_TYPES:
            raise SimpleBenchValueError(
                f"Unsupported VCS type: {self.vcs_type}",
                tag=_VCSInfoErrorTag.VCS_TYPE_INVALID_VALUE)
        if not isinstance(self.branch, str):
            raise SimpleBenchTypeError(
                f"branch must be a string, got {type(self.branch)}",
                tag=_VCSInfoErrorTag.BRANCH_INVALID_TYPE)
        if not isinstance(self.commit_id, str):
            raise SimpleBenchTypeError(
                f"commit_id must be a string, got {type(self.commit_id)}",
                tag=_VCSInfoErrorTag.COMMIT_ID_INVALID_TYPE)
        if not isinstance(self.commit_datetime, str):
            raise SimpleBenchTypeError(
                f"commit_datetime must be a string, got {type(self.commit_datetime)}",
                tag=_VCSInfoErrorTag.COMMIT_DATETIME_INVALID_TYPE)
        if not isinstance(self.dirty, bool):
            raise SimpleBenchTypeError(
                f"dirty must be a boolean, got {type(self.dirty)}",
                tag=_VCSInfoErrorTag.DIRTY_INVALID_TYPE)

    def to_dict(self) -> dict[str, str | bool]:
        """Convert to dictionary for JSON serialization.

        :return: Dictionary representation of GitInfo.
        """
        return asdict(self)
