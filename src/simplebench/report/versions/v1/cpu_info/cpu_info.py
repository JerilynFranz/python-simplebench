"""JSON CPUInfo version 1 class.

The CPUInfo class represents a version 1 JSON CPUInfo.

It provides methods to convert to and from dictionary representations
and includes schema validation specific to version 1 reports.

The version 1 CPUInfo is the first stable version of the JSON CPUInfo format
and serves as a foundation for future versions.

As the foundational version, this class is considered immutable. Future versions
will inherit from this class to extend its functionality, but this implementation
will not be changed.
"""
import hashlib
import re
from types import NoneType
from typing import Any, TypeAlias

from simplebench.exceptions import SimpleBenchTypeError
from simplebench.report._error_tags import _CPUInfoErrorTag
from simplebench.report.base import CPUInfo as BaseCPUInfo
from simplebench.report.base import JSONSchema
from simplebench.validators import validate_string

from . import validate
from .cpu_info_schema import CPUInfoSchema


class CPUInfo(BaseCPUInfo):
    """Class representing a JSON CPUInfo version 1."""
    TYPE: str = CPUInfoSchema.TYPE
    """The JSON CPUInfo type property value for version 1 reports."""

    VERSION: int = CPUInfoSchema.VERSION
    """The JSON CPUInfo version number."""

    SCHEMA: type[JSONSchema] = CPUInfoSchema
    """The JSON schema class for version 1 reports."""

    DataTypes: TypeAlias = dict[str, "DataTypes"] | list["DataTypes"] | str | int | float | bool | NoneType

    def __init__(self,
                 *,
                 hash_id: str = '',
                 data: dict[str, DataTypes]) -> None:
        """Initialize CPUInfo.

        :param str hash_id: The unique hash identifier for the CPU information.
            If not provided, it defaults to None and will be computed automatically.
        :param dict[str, DataTypes] data: The raw CPU information data collected from the system
            using the :package:`cpuinfo` library. It must be a dictionary.

            The dictionary must conform to the following rules:
            - It can have arbitrary keys and values but must be a tree composed of
              dictionaries, lists, strings, numbers, booleans, and nulls.
            - All keys in dictionaries must be non-blank, non-empty strings.
        """
        self._hash_id = validate.hash_id(hash_id)
        self._data = validate.data(data)

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

    @hash_id.setter
    def hash_id(self, value: str) -> None:
        """Set the hash_id property.

        It is validated to be a valid SHA-256 hexadecimal string or an empty string.

        :param value: The hash_id string to set.
        """
        hash_string = validate_string(
            value, "hash_id",
            _CPUInfoErrorTag.INVALID_HASH_ID_PROPERTY_TYPE,
            _CPUInfoErrorTag.INVALID_HASH_ID_PROPERTY_VALUE,
            allow_empty=True, strip=True)
        if hash_string == '':
            self._hash_id = ''
            return

        if not re.fullmatch(r'^[a-f0-9]{64}$', hash_string):
            raise SimpleBenchTypeError(
                "hash_id must be a valid SHA-256 hexadecimal string",
                tag=_CPUInfoErrorTag.INVALID_HASH_ID_PROPERTY_VALUE)
        self._hash_id: str = hash_string

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> 'CPUInfo':
        """Create a CPUInfo instance from a dictionary.

        .. code-block:: python
           :caption: Example

           cpu_info = CPUInfo.from_dict(data)


        The dictionary must conform to the expected structure for the CPUInfo
        representation. The 'version' and 'type' properties are validated
        against the class's VERSION and TYPE attributes if they are present.

        :param data: The dictionary containing CPU information.
        :return: A CPUInfo instance.
        """
        allowed_keys = cls.init_params()
        allowed_keys['version'] = int
        allowed_keys['type'] = str

        kwargs = cls.import_data(
            data=data,
            allowed=allowed_keys,
            skip={'version', 'type'},
            optional={'hash_id', 'version', 'type'},
            default={'hash_id': '', 'version': cls.VERSION, 'type': cls.TYPE},
            match_on={'version': cls.VERSION, 'type': cls.TYPE})
        return cls(**kwargs)

    def to_dict(self) -> dict[str, Any]:
        """Convert the CPUInfo to a dictionary suitable for JSON serialization.

        This includes all properties defined in the :class:`CPUInfoSchema`
        for the version.

        :return: A dictionary representation of the CPUInfo.
        """
        property_keys = self.init_params().keys()
        data = {key: getattr(self, key) for key in property_keys}
        data['type'] = self.TYPE
        data['version'] = self.VERSION

        return data
