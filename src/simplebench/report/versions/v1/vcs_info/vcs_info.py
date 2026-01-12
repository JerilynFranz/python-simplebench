"""VCSInfo version 1 base class.

This class represents vcs information in a JSON report.

It implements validation and serialization/deserialization methods to and from dictionaries
for the following JSON Schema version:

https://raw.githubusercontent.com/JerilynFranz/python-simplebench/main/schemas/v1/vcs-info.json

It is the base implemention of the JSON report vcs info representation.

This makes the implementations of VCSInfo backwards compatible with future versions
of the JSON report schema and the V1 implementation itself is essentially a frozen snapshot
of the base VCSInfo representation at the time of the V1 schema release.
"""

from simplebench.report.base import BaseVCSInfo, JSONSchema

from . import _validate
from .typeddict_types import ImmutableVCSInfoDict, VCSInfoData
from .vcs_info_schema import VCSInfoSchema

__all__ = []


class VCSInfo(BaseVCSInfo):  # pylint: disable=too-many-instance-attributes
    """Class representing vcs information in a JSON report."""

    TYPE: str = VCSInfoSchema.TYPE
    """The JSON VCSInfo type property value for version 1 reports."""

    VERSION: int = VCSInfoSchema.VERSION
    """The JSON VCSInfo version number."""

    ID: str = VCSInfoSchema.ID
    """The JSON VCSInfo schema identifier for version 1 reports."""

    SCHEMA: type[JSONSchema] = VCSInfoSchema
    """The JSON schema class for version 1 reports."""

    def __init__(
        self,
        *,  # pylint: disable=too-many-arguments
        hash_id: str = '',
        vcs: str,
        commit_id: str,
        commit_datetime: str,
        branch: str,
        repository_url: str,
        is_dirty: bool,
    ) -> None:
        """Initialize JSONVCSInfo.

        :param str hash_id: The unique hash identifier for the machine information.
            If not provided, it defaults to an empty string and will be computed automatically.
        :param str vcs: The version control system string.
        :param str commit_id: The unique identifier of the current revision.
        :param str commit_datetime: The datetime of the commit in ISO 8601 format.
        :param str branch: The current branch name.
        :param str repository_url: The URL of the primary remote repository or empty string.
        :param bool is_dirty: Whether there are uncommitted changes.
        """
        self._vcs: str = _validate.vcs(vcs)
        self._commit_id: str = _validate.commit_id(commit_id)
        self._commit_datetime: str = _validate.commit_datetime(commit_datetime)
        self._branch: str = _validate.branch(branch)
        self._repository_url: str = _validate.repository_url(repository_url)
        self._is_dirty: bool = _validate.is_dirty(is_dirty)
        self._hash_id: str = _validate.hash_id(hash_id)
        if self._hash_id == '':
            self._hash_id = self._hash_id_helper(VCSInfoData)
        self._dict_cache: ImmutableVCSInfoDict | None = None

    @classmethod
    def from_dict(cls, data: VCSInfoData) -> 'VCSInfo':
        """Create a VCSInfo instance from a dictionary.

        .. code-block:: python
           :caption: Example

           vcs_info = VCSInfo.from_dict(data)

        :param data: The dictionary containing vcs information.
        :return: A VCSInfo instance.
        """
        allowed_keys = cls.init_params()
        allowed_keys['version'] = int
        allowed_keys['type'] = str

        kwargs = cls.import_data(
            data=data,
            allowed_fields=allowed_keys,
            skip_fields={'version', 'type'},
            optional_fields={'hash_id', 'version', 'type'},
            defaults={'hash_id': '', 'version': cls.VERSION, 'type': cls.TYPE},
            match_on={'version': cls.VERSION, 'type': cls.TYPE},
        )
        return cls(**kwargs)

    def to_dict(self) -> ImmutableVCSInfoDict:
        """Convert the VCSInfo to a dictionary.

        This is a lazy implementation that caches the dictionary representation
        after the first conversion for efficiency. Subsequent calls return
        the cached version.

        :return: A dictionary representation of the VCSInfo.
        """
        if self._dict_cache is None:
            self._dict_cache = self._to_dict_helper(ImmutableVCSInfoDict)
        return self._dict_cache

    @property
    def hash_id(self) -> str:
        """Get the hash_id property.

        :return: The hash_id string.
        """
        return self._hash_id

    @property
    def vcs(self) -> str:
        """Get the vcs property.

        :return: The vcs string.
        """
        return self._vcs

    @property
    def commit_id(self) -> str:
        """Get the commit_id property.

        :return: The commit_id string.
        """
        return self._commit_id

    @property
    def commit_datetime(self) -> str:
        """Get the commit_datetime property.

        :return: The commit_datetime string.
        """
        return self._commit_datetime

    @property
    def branch(self) -> str:
        """Get the branch property.

        :return: The branch string.
        """
        return self._branch

    @property
    def repository_url(self) -> str:
        """Get the repository_url property.

        :return: The repository_url string.
        """
        return self._repository_url

    @property
    def is_dirty(self) -> bool:
        """Get the is_dirty property.

        :return: The is_dirty boolean value.
        """
        return self._is_dirty
