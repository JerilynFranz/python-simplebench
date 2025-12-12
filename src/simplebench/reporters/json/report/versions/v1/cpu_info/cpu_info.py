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
            hash_input = (
                f"arch:{self.arch}\x00" +
                f"bits:{self.bits}\x00" +
                f"count:{self.count}\x00" +
                f"arch_string_raw:{self.arch_string_raw}\x00" +
                f"brand_raw:{self.brand_raw}"
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
        if not isinstance(data, dict):
            raise SimpleBenchTypeError(
                "data must be a dictionary",
                tag=_CPUInfoErrorTag.INVALID_DATA_ARG_TYPE)

        known_keys = {
            'hash_id',
            'arch',
            'bits',
            'count',
            'arch_string_raw',
            'brand_raw',
        }

        version = data.get('version') or cls.VERSION
        if not isinstance(version, int):
            raise SimpleBenchTypeError(
                "The 'version' property must be of type 'int' if set",
                tag=_CPUInfoErrorTag.INVALID_VERSION_TYPE)

        if version != cls.VERSION:
            raise SimpleBenchTypeError(
                f"The 'version' property must have the value {cls.VERSION} if set",
                tag=_CPUInfoErrorTag.UNSUPPORTED_VERSION)

        type_str = data.get('type') or cls.TYPE
        if not isinstance(type_str, str):
            raise SimpleBenchTypeError(
                "The 'type' property must be of type 'str' if set",
                tag=_CPUInfoErrorTag.INVALID_VERSION_TYPE)

        if type_str != cls.TYPE:
            raise SimpleBenchTypeError(
                f"The 'type' property must have tye value '{cls.TYPE}' if set",
                tag=_CPUInfoErrorTag.UNSUPPORTED_VERSION)

        extra_keys = set(data.keys()) - known_keys - {'version', 'type'}
        if extra_keys:
            raise SimpleBenchTypeError(
                f"Unexpected keys in data dictionary: {extra_keys}",
                tag=_CPUInfoErrorTag.INVALID_DATA_ARG_EXTRA_KEYS)
        missing_keys = known_keys - data.keys() - {'hash_id'}
        if missing_keys:
            raise SimpleBenchTypeError(
                f"Missing required keys in data dictionary: {missing_keys}",
                tag=_CPUInfoErrorTag.INVALID_DATA_ARG_MISSING_KEYS)

        instance = cls(
            hash_id=data.get('hash_id', ''),
            arch=data['arch'],
            bits=data['bits'],
            count=data['count'],
            arch_string_raw=data['arch_string_raw'],
            brand_raw=data['brand_raw'])

        return instance

    def to_dict(self) -> dict[str, Any]:
        """Convert the CPUInfo to a dictionary suitable for JSON serialization.

        This includes all properties defined in the :class:`CPUInfoSchema`
        for the version.

        :return: A dictionary representation of the CPUInfo.
        """
        cls = self.__class__
        result: dict[str, Any] = {
            'version': cls.VERSION,
            'type': cls.TYPE,
            'hash_id': self.hash_id,
            'arch': self.arch,
            'bits': self.bits,
            'count': self.count,
            'arch_string_raw': self.arch_string_raw,
            'brand_raw': self.brand_raw,
        }
        return result
