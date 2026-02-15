"""KWArgs subclass for VCSInfo.__init__."""

from simplebench.report.versions.v1.vcs_info.vcs_info import VCSInfo
from simplebench_tests.kwargs import KWArgs, NoDefaultValue, NO_DEFAULT_VALUE

class VCSInfoKWArgs(KWArgs):
    """KWArgs for VCSInfo.__init__"""

    def __init__(self, *,
            hash_id: str | NoDefaultValue = NO_DEFAULT_VALUE,
            vcs: str | NoDefaultValue = NO_DEFAULT_VALUE,
            commit_id: str | NoDefaultValue = NO_DEFAULT_VALUE,
            commit_datetime: str | NoDefaultValue = NO_DEFAULT_VALUE,
            branch: str | NoDefaultValue = NO_DEFAULT_VALUE,
            repository_url: str | NoDefaultValue = NO_DEFAULT_VALUE,
            is_dirty: bool | NoDefaultValue = NO_DEFAULT_VALUE) -> None:
        """Initialize JSONVCSInfo.

        :param str hash_id: The unique hash identifier for the machine information.
            If not provided, it defaults to an empty string and will be computed automatically.
        :param str vcs: The version control system string.
        :param str commit_id: The unique identifier of the current revision.
        :param str commit_datetime: The datetime of the commit in ISO 8601 format.
        :param str branch: The current branch name.
        :param str repository_url: The URL of the primary remote repository or empty string.
        :param bool is_dirty: Whether there are uncommitted changes."""
        super().__init__(VCSInfo.__init__, kwargs=locals(), globalns=globals())

