"""V1 SystemInfo implementation."""
from types import MappingProxyType
from typing import Any

from simplebench.report.base import BaseSystemInfo, JSONSchema

from . import _validate
from .system_info_schema import SystemInfoSchema
from .system_info_dict import ImmutableSystemInfoDict, SystemInfoData, SystemInfoDict

__all__: list[str] = []


class SystemInfo(BaseSystemInfo):
    """Class representing system execution environment in a report (V1)."""

    SCHEMA: type[JSONSchema] = SystemInfoSchema
    """The JSON schema class for version 1 reports."""

    TYPE: str = SCHEMA.TYPE
    """The JSON SystemInfo type property value for version 1 reports."""

    VERSION: int = SCHEMA.VERSION
    """The JSON SystemInfo version number."""

    ID: str = SCHEMA.ID
    """The JSON SystemInfo identifier property value for version 1 reports."""

    _init_params_cache: MappingProxyType[str, Any] | None = None

    @classmethod
    def _data_params(cls) -> MappingProxyType[str, Any]:
        """Get the constructor parameters for the schema data class.

        The parameters are cached after the first call for performance.

        It is returned as a read-only mapping and includes 'type' and 'version'.

        :return MappingProxyType[str, Any]: A read-only mapping of constructor parameter names and types.
        """
        if not cls._init_params_cache:
            params = cls.init_params(SystemInfoData)
            cls._init_params_cache = MappingProxyType(params)
        return cls._init_params_cache

    __slots__ = ('_hash_id', '_system', '_system_version', '_release', '_machine', '_dict_cache')

    def __init__(self, *, hash_id: str = '', system: str, system_version: str, release: str, machine: str) -> None:
        """Initialize the SystemInfo instance.

        :param str hash_id: The unique hash identifier for the system info.
        :param str system: The system OS identifier string.
        :param str system_version: The system version string.
        :param str release: The system release string.
        :param str machine: The machine type string.
        """
        self._system: str = _validate.system(system)
        self._system_version: str = _validate.system_version(system_version)
        self._release: str = _validate.release(release)
        self._machine: str = _validate.machine(machine)
        self._hash_id: str = _validate.hash_id(hash_id) or self._hash_id_helper(SystemInfoDict)
        self._dict_cache: ImmutableSystemInfoDict = self._to_dict_helper(ImmutableSystemInfoDict)

    @classmethod
    def from_dict(cls, data: SystemInfoData) -> 'SystemInfo':
        """Create a SystemInfo instance from a dictionary.

        .. code-block:: system3
           :caption: Example

            system_info = SystemInfo.from_dict(data)

        The dictionary must conform to the expected structure for the SystemInfo
        representation. The 'version' and 'type' properties are validated
        against the class's VERSION and TYPE attributes if they are present.

        :param data: The dictionary containing SystemInfo information.
        :return: A SystemInfo instance.
        """
        allowed_keys = dict(cls._data_params())
        allowed_keys['version'] = int
        allowed_keys['type'] = str
        kwargs = cls.import_data(
            data=data,
            allowed_fields=allowed_keys,
            skip_fields={'version', 'type'},
            optional_fields={'hash_id', 'version', 'type'},
            defaults={'version': cls.VERSION, 'type': cls.TYPE},
            match_on={'version': cls.VERSION, 'type': cls.TYPE},
        )
        return cls(**kwargs)

    def to_dict(self) -> ImmutableSystemInfoDict:
        """Return the SystemInfo as an immutable dictionary suitable for JSON serialization.

        This includes all properties defined in the :class:`SystemInfoSchema`
        for the version as mirrored in :class:`SystemInfoDict`.

        :return ImmutableSystemInfoDict: A dictionary representation of the SystemInfo.
        """
        return self._dict_cache

    @property
    def hash_id(self) -> str:
        """Get the hash_id property.

        :return: The hash_id string.
        """
        return self._hash_id

    @property
    def system(self) -> str:
        """Get the system property.

        :return: The system string.
        """
        return self._system

    @property
    def system_version(self) -> str:
        """Get the system_version property.

        :return: The system_version string.
        """
        return self._system_version

    @property
    def release(self) -> str:
        """Get the release property.

        :return: The release string.
        """
        return self._release

    @property
    def machine(self) -> str:
        """Get the machine property.

        :return: The machine string.
        """
        return self._machine

    def for_json(self) -> ImmutableSystemInfoDict:
        """Get the JSON-serializable dictionary representation of this SystemInfo.

        This method delegates to the for_json method of the dictionary returned by :meth:`to_dict`
        because the dictionary is actually an instance of :class:`CoreDataMapping`
        which has the for_json method to convert to a JSON-serializable dictionary.

        :return: The JSON-serializable dictionary representation of this SystemInfo.
        """
        return self.to_dict().for_json()  # type: ignore

    def as_json(self) -> str:
        """Get the JSON string representation of this SystemInfo.

        This method delegates to the as_json method of the dictionary returned by :meth:`to_dict`
        because the dictionary is actually an instance of :class:`CoreDataMapping`
        which has the as_json method to convert to a JSON string.

        :return: The JSON string representation of this SystemInfo.
        """
        return self.to_dict().as_json()  # type: ignore

    def __repr__(self) -> str:
        """Get the string representation of the SystemInfo instance.

        :return: The string representation of the SystemInfo.
        """
        # Get the init parameters excluding 'type' and'version' since they are fixed for this class
        init_params = dict(self._data_params())
        init_params.pop('type', None)
        init_params.pop('version', None)

        # Build the key-value argument string. Accessing the properties via getattr
        # will trigger their lazy calculation if they haven't been computed yet.
        calling_args = ', '.join(f'{key}={getattr(self, key)!r}' for key in init_params)
        return f'{self.__class__.__name__}({calling_args})'

    def __hash__(self) -> int:
        """Get the hash of the SystemInfo instance.

        :return: The hash value.
        """
        return hash(self.hash_id)

    def __eq__(self, other: object) -> bool:
        """Check equality between two SystemInfo instances.

        :param other: The other object to compare.
        :return: True if equal, False otherwise.
        """
        if not isinstance(other, SystemInfo):
            return NotImplemented
        return self.hash_id == other.hash_id

    def __copy__(self) -> 'SystemInfo':
        """Return the same instance since SystemInfo is immutable."""
        return self

    def __deepcopy__(self, memo: dict[int, Any]) -> 'SystemInfo':
        """Return the same instance since SystemInfo is immutable."""
        return self
