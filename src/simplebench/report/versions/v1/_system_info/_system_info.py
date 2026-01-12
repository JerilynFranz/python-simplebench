"""V1 SystemInfo implementation."""

from simplebench.report.base import BaseSystemInfo, JSONSchema

from . import _validate
from ._system_info_schema import SystemInfoSchema
from ._typeddict_types import ImmutableSystemInfoDict, SystemInfoData, SystemInfoDict


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

    def __init__(self, *, hash_id: str, system: str, system_version: str, release: str, machine: str) -> None:
        """Initialize the SystemInfo instance.

        :param str hash_id: The unique hash identifier for the system info.
        :param str system: The system OS identifier string.
        :param str system_version: The system version string.
        :param str release: The system release string.
        :param str machine: The machine type string.
        """
        self._hash_id: str = _validate.hash_id(hash_id)
        self._system: str = _validate.system(system)
        self._system_version: str = _validate.system_version(system_version)
        self._release: str = _validate.release(release)
        self._machine: str = _validate.machine(machine)
        self._dict_cache: ImmutableSystemInfoDict | None = None

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
        allowed_keys = cls.init_params()
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
        if self._dict_cache is None:
            self._dict_cache = self._to_dict_helper(ImmutableSystemInfoDict)
        return self._dict_cache

    @property
    def hash_id(self) -> str:
        """Get the hash_id property.

        :return: The hash_id string.
        """
        if not self._hash_id:
            self._hash_id = self._hash_id_helper(SystemInfoDict)
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
