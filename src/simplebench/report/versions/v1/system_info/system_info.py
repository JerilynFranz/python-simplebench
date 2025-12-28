"""V1 SystemInfo implementation."""
import hashlib
from typing import Any

from simplebench.report.base import BaseSystemInfo, JSONSchema

from . import validate
from .system_info_schema import SystemInfoSchema


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

    def __init__(self, *,
                 hash_id: str,
                 system: str,
                 system_version: str,
                 release: str,
                 machine: str) -> None:
        """Initialize the SystemInfo instance.

        :param str hash_id: The unique hash identifier for the system info.
        :param str system: The system OS identifier string.
        :param str system_version: The system version string.
        :param str release: The system release string.
        :param str machine: The machine type string.
        """
        self._hash_id = validate.hash_id(hash_id)
        self._system = validate.system(system)
        self._system_version = validate.system_version(system_version)
        self._release = validate.release(release)
        self._machine = validate.machine(machine)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> 'SystemInfo':
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
            allowed=allowed_keys,
            skip={'version', 'type'},
            optional={'hash_id', 'version', 'type'},
            default={'version': cls.VERSION, 'type': cls.TYPE},
            match_on={'version': cls.VERSION, 'type': cls.TYPE})
        return cls(**kwargs)

    def to_dict(self) -> dict[str, Any]:
        """Convert the SystemInfo to a dictionary suitable for JSON serialization.

        This includes all properties defined in the :class:`SystemInfoSchema`
        for the version.

        :return: A dictionary representation of the SystemInfo.
        """
        property_keys = self.init_params().keys()
        data = {key: getattr(self, key) for key in property_keys}
        data['type'] = self.TYPE
        data['version'] = self.VERSION

        return data

    @property
    def hash_id(self) -> str:
        """Get the hash_id property.

        :return: The hash_id string.
        """
        if self._hash_id == '':
            # Get all __init__ params except 'hash_id' itself.
            # Sorting ensures a consistent order for hashing.
            hash_keys = sorted(k for k in self.init_params() if k != 'hash_id')

            # Create a null-byte separated string of "key:value" pairs.
            hash_input = "\x00".join(
                f"{key}:{getattr(self, key)}" for key in hash_keys
            ).encode('utf-8')

            self._hash_id = hashlib.sha256(hash_input).hexdigest()
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
