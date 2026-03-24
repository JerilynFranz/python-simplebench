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
from types import MappingProxyType
from typing import Any

from simplebench.report.base import BaseVCSInfo, JSONSchema

from . import _validate
from .vcs_info_dict import ImmutableVCSInfoDict, VCSInfoData
from .vcs_info_schema import VCSInfoSchema

__all__: list[str] = []


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

    _init_params_cache: MappingProxyType[str, Any] = MappingProxyType({})
    """Cache for the constructor parameters of the VCSInfo class."""

    @classmethod
    def _data_params(cls) -> MappingProxyType[str, Any]:
        """Get the constructor parameters for the schema data class.

        The parameters are cached after the first call for performance.

        It is returned as a read-only mapping and includes 'type' and 'version'.

        :return MappingProxyType[str, Any]: A read-only mapping of constructor parameter names and types.
        """
        if not cls._init_params_cache:
            params = cls.init_params(VCSInfoData)
            cls._init_params_cache = MappingProxyType(params)
        return cls._init_params_cache

    __slots__ = (
        '_vcs',
        '_commit_id',
        '_commit_datetime',
        '_branch',
        '_repository_url',
        '_is_dirty',
        '_hash_id',
        '_dict_cache',
    )

    def __init__(
        self,
        *,
        hash_id: str = '',
        vcs: str,
        commit_id: str,
        commit_datetime: str,
        branch: str,
        repository_url: str,
        is_dirty: bool,
    ) -> None:
        """Initialize JSONVCSInfo.

        :param str hash_id: The unique hash identifier for the vcs information.
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
        self._dict_cache: ImmutableVCSInfoDict = self._to_dict_helper(ImmutableVCSInfoDict)

    @classmethod
    def from_dict(cls, data: VCSInfoData) -> 'VCSInfo':
        """Create a VCSInfo instance from a dictionary.

        .. code-block:: python
           :caption: Example

           vcs_info = VCSInfo.from_dict(data)

        :param data: The dictionary containing vcs information.
        :return: A VCSInfo instance.
        """
        allowed_keys = dict(cls._data_params())
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

    def for_json(self) -> ImmutableVCSInfoDict:
        """Get the JSON-serializable dictionary representation of this VCSInfo.

        This method delegates to the for_json method of the dictionary returned by :meth:`to_dict`
        because the dictionary is actually an instance of :class:`CoreDataMapping`
        which has the for_json method to convert to a JSON-serializable dictionary.

        :return: The JSON-serializable dictionary representation of this VCSInfo.
        """
        return self.to_dict().for_json()  # type: ignore

    def as_json(self) -> str:
        """Get the JSON string representation of this VCSInfo.

        This method delegates to the as_json method of the dictionary returned by :meth:`to_dict`
        because the dictionary is actually an instance of :class:`CoreDataMapping`
        which has the as_json method to convert to a JSON string.

        :return: The JSON string representation of this VCSInfo.
        """
        return self.to_dict().as_json()  # type: ignore

    def __repr__(self) -> str:
        """Get the string representation of the VCSInfo instance.

        :return: The string representation of the VCSInfo.
        """
        # Get the init parameters excluding 'type', 'version', and 'semantic_type' since they are fixed for this class
        init_params = dict(self._data_params())
        init_params.pop('type', None)
        init_params.pop('version', None)

        # Build the key-value argument string. Accessing the properties via getattr
        # will trigger their lazy calculation if they haven't been computed yet.
        calling_args = ', '.join(f'{key}={getattr(self, key)!r}' for key in init_params)
        return f'{self.__class__.__name__}({calling_args})'

    def __hash__(self) -> int:
        """Get the hash of the VCSInfo instance.

        :return: The hash value.
        """
        return hash(self.hash_id)

    def __eq__(self, other: object) -> bool:
        """Check equality between two VCSInfo instances.

        :param other: The other object to compare.
        :return: True if equal, False otherwise.
        """
        if not isinstance(other, VCSInfo):
            return NotImplemented
        return self.hash_id == other.hash_id

    def __copy__(self) -> 'VCSInfo':
        """Return the same instance since VCSInfo is immutable."""
        return self

    def __deepcopy__(self, memo: dict[int, Any]) -> 'VCSInfo':
        """Return the same instance since VCSInfo is immutable."""
        return self
