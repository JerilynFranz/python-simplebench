"""Hg (Mercurial) Info record."""
from abc import ABC, abstractmethod
from dataclasses import asdict, dataclass

from simplebench.exceptions import SimpleBenchNotImplementedError, SimpleBenchTypeError, SimpleBenchValueError
from simplebench.validators import validate_iso8601_datetime

from .exceptions import _VCSInfoErrorTag
from .vcs_type import VCSType

_SUPPORTED_VCS_TYPES: set[VCSType] = {VCSType.GIT, VCSType.HG}
"""Set of currently supported VCS types for VCSInfo."""


@dataclass(frozen=True, kw_only=True, repr=True)
class VCSInfo(ABC):
    """Abstract base Dataclass to hold VCS Info about the repository.

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
        self.validate_commit_id(self.commit_id)
        validate_iso8601_datetime(
            self.commit_datetime,
            type_tag=_VCSInfoErrorTag.COMMIT_DATETIME_INVALID_TYPE,
            value_tag=_VCSInfoErrorTag.COMMIT_DATETIME_INVALID_VALUE)

        if not isinstance(self.dirty, bool):
            raise SimpleBenchTypeError(
                f"dirty must be a boolean, got {type(self.dirty)}",
                tag=_VCSInfoErrorTag.DIRTY_INVALID_TYPE)

    def to_dict(self) -> dict[str, str | bool]:
        """Convert to dictionary for JSON serialization.

        :return: Dictionary representation of GitInfo.
        """
        return asdict(self)

    @abstractmethod
    def validate_commit_id(self, commit_id: str) -> None:
        """Validate the commit_id. Abstraction to be implemented by subclasses.

        :param commit_id: The commit ID to validate.
        :raises SimpleBenchTypeError: If commit_id is not a string.
        :raises SimpleBenchValueError: If commit_id does not match expected format.
        """
        raise SimpleBenchNotImplementedError(
            "Subclasses must implement validate_commit_id method.",
            tag=_VCSInfoErrorTag.NOT_IMPLEMENTED)
