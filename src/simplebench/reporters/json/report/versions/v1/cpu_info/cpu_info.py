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
from typing import Any

from simplebench.exceptions import SimpleBenchTypeError
from simplebench.reporters.json.report.base import CPUInfo as BaseCPUInfo
from simplebench.reporters.json.report.base import JSONSchema
from simplebench.reporters.json.report.exceptions import _CPUInfoErrorTag
from simplebench.validators import validate_int, validate_string

from .cpu_info_schema import CPUInfoSchema


class CPUInfo(BaseCPUInfo):
    """Class representing a JSON CPUInfo version 1."""
    TYPE: str = CPUInfoSchema.TYPE
    """The JSON CPUInfo type property value for version 1 reports."""

    VERSION: int = CPUInfoSchema.VERSION
    """The JSON CPUInfo version number."""

    SCHEMA: type[JSONSchema] = CPUInfoSchema
    """The JSON schema class for version 1 reports."""

    def __init__(self,
                 *,
                 hash_id: str = '',
                 arch: str,
                 bits: int,
                 count: int,
                 arch_string_raw: str,
                 brand_raw: str) -> None:
        """Initialize CPUInfo.
        :param hash_id: The unique hash identifier for the CPU information.
            If not provided, it defaults to None and will be computed automatically.
        :param arch: The CPU architecture.
        :param bits: The CPU bitness (e.g., 32 or 64).
        :param count: The number of CPU cores.
        :param arch_string_raw: The raw architecture string.
        :param brand_raw: The raw brand string.
        """
        self.hash_id = hash_id
        self.arch = arch
        self.bits = bits
        self.count = count
        self.arch_string_raw = arch_string_raw
        self.brand_raw = brand_raw

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

    @property
    def arch(self) -> str:
        """Get the arch property.

        :return: The arch string.
        """
        return self._arch

    @arch.setter
    def arch(self, value: str) -> None:
        """Set the arch property.

        :param value: The arch string to set.
        """
        self._arch: str = validate_string(
            value, "arch",
            _CPUInfoErrorTag.INVALID_ARCH_TYPE,
            _CPUInfoErrorTag.INVALID_ARCH_VALUE_EMPTY_OR_BLANK_STRING,
            allow_empty=False, allow_blank=False, strip=True)

    @property
    def bits(self) -> int:
        """Get the bits property.

        :return: The bits integer.
        """
        return self._bits

    @bits.setter
    def bits(self, value: int) -> None:
        """Set the bits property.

        :param value: The bits integer to set.
        """
        self._bits: int = validate_int(
            value, "bits",
            _CPUInfoErrorTag.INVALID_BITS_TYPE)
        if self._bits < 16:
            raise SimpleBenchTypeError(
                "bits must be greater than or equal to 16",
                tag=_CPUInfoErrorTag.INVALID_BITS_VALUE)

    @property
    def count(self) -> int:
        """Get the CPU core count property.

        :return: The core count integer.
        """
        return self._count

    @count.setter
    def count(self, value: int) -> None:
        """Set the CPU core count property.

        :param value: The core count integer to set.
        """
        self._count: int = validate_int(
            value, "count",
            _CPUInfoErrorTag.INVALID_COUNT_TYPE)
        if self._count < 1:
            raise SimpleBenchTypeError(
                "count must be greater than or equal to 1",
                tag=_CPUInfoErrorTag.INVALID_COUNT_VALUE)

    @property
    def arch_string_raw(self) -> str:
        """Get the arch_string_raw property.

        :return: The arch_string_raw string.
        """
        return self._arch_string_raw

    @arch_string_raw.setter
    def arch_string_raw(self, value: str) -> None:
        """Set the arch_string_raw property.

        :param value: The arch_string_raw string to set.
        """
        self._arch_string_raw: str = validate_string(
            value, "arch_string_raw",
            _CPUInfoErrorTag.INVALID_ARCH_STRING_RAW_TYPE,
            _CPUInfoErrorTag.INVALID_ARCH_STRING_RAW_VALUE_BLANK_STRING,
            allow_empty=True, allow_blank=False, strip=True)

    @property
    def brand_raw(self) -> str:
        """Get the brand_raw property.

        :return: The brand_raw string.
        """
        return self._brand_raw

    @brand_raw.setter
    def brand_raw(self, value: str) -> None:
        """Set the brand_raw property.

        :param value: The brand_raw string to set.
        """
        self._brand_raw: str = validate_string(
            value, "brand_raw",
            _CPUInfoErrorTag.INVALID_BRAND_RAW_TYPE,
            _CPUInfoErrorTag.INVALID_BRAND_RAW_VALUE_BLANK_STRING,
            allow_empty=True, allow_blank=False, strip=True)

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
            optional={'hash_id'},
            default={'hash_id': ''},
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
