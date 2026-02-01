"""MemoryInfo version 1 base class.

This class represents machine information in a JSON report.

It implements validation and serialization/deserialization methods to and from dictionaries
for the following JSON Schema version:

https://raw.githubusercontent.com/JerilynFranz/python-simplebench/main/schemas/v1/memory-info.json

It is the base implemention of the JSON report memory info representation.

This makes the implementations of JSONMemoryInfo backwards compatible with future versions
of the JSON report schema and the V1 implementation itself is essentially a frozen snapshot
of the base MemoryInfo representation at the time of the V1 schema release.
"""

from types import MappingProxyType
from typing import Any

from simplebench.report.base import BaseMemoryInfo, JSONSchema

from . import _validate
from .memory_info_schema import MemoryInfoSchema
from .swap_memory import SwapMemoryObject
from .typeddict_types import ImmutableMemoryInfoDict, MemoryInfoData, MemoryInfoDict
from .virtual_memory import VirtualMemoryObject

__all__: list[str] = []


class MemoryInfo(BaseMemoryInfo):
    """Class representing machine information in a JSON report."""

    TYPE: str = MemoryInfoSchema.TYPE
    """The JSON MemoryInfo type property value for version 1 reports."""

    VERSION: int = MemoryInfoSchema.VERSION
    """The JSON MemoryInfo version number."""

    ID: str = MemoryInfoSchema.ID
    """The JSON MemoryInfo schema identifier for version 1 reports."""

    SCHEMA: type[JSONSchema] = MemoryInfoSchema
    """The JSON schema class for version 1 reports."""

    _init_params_cache: MappingProxyType[str, Any] = MappingProxyType({})
    """Cache for the constructor parameters of the ResultsInfo class."""

    _init_params_cache: MappingProxyType[str, Any] = MappingProxyType({})
    """Cache for the constructor parameters of the MemoryInfo class."""

    @classmethod
    def _data_params(cls) -> MappingProxyType[str, Any]:
        """Get the constructor parameters for the schema data class.

        The parameters are cached after the first call for performance.

        It is returned as a read-only mapping and includes 'type' and 'version'.

        :return MappingProxyType[str, Any]: A read-only mapping of constructor parameter names and types.
        """
        if not cls._init_params_cache:
            params = cls.init_params(MemoryInfoData)
            cls._init_params_cache = MappingProxyType(params)
        return cls._init_params_cache

    __slots__ = ('_hash_id', '_swap_memory', '_virtual_memory', '_dict_cache')

    def __init__(
        self, *, hash_id: str = '', swap_memory: SwapMemoryObject, virtual_memory: VirtualMemoryObject
    ) -> None:
        """Initialize MemoryInfo.

        :param str hash_id: The unique hash identifier for the MemoryInfo instance.
        :param SwapMemoryObject swap_memory: The swap memory information.
        :param VirtualMemoryObject virtual_memory: The virtual memory information.
        """
        self._hash_id = _validate.hash_id(hash_id)
        self._swap_memory = _validate.swap_memory(swap_memory)
        self._virtual_memory = _validate.virtual_memory(virtual_memory)
        self._dict_cache: ImmutableMemoryInfoDict = self._to_dict_helper(ImmutableMemoryInfoDict)
        self._hash_id: str = self._hash_id_helper(MemoryInfoDict)

    @classmethod
    def from_dict(cls, data: MemoryInfoData) -> 'MemoryInfo':
        """Create a MemoryInfo instance from a dictionary.

        .. code-block:: python
           :caption: Example

           memory_info = MemoryInfo.from_dict(data)

        :param data: The dictionary containing the MemoryInfo data.
        :return MemoryInfo: A MemoryInfo instance.
        """
        allowed_keys = cls._data_params()
        kwargs = cls.import_data(
            data=data,
            allowed_fields=allowed_keys,
            skip_fields={'version', 'type'},
            optional_fields={'hash_id', 'version', 'type'},
            defaults={'hash_id': '', 'version': cls.VERSION, 'type': cls.TYPE},
            match_on={'version': cls.VERSION, 'type': cls.TYPE},
            process_as={},
        )
        return cls(**kwargs)

    def to_dict(self) -> ImmutableMemoryInfoDict:
        """The MemoryInfo as an immutable dictionary.

        :return MemoryInfoDict: A dictionary representation of the MemoryInfo.
        """
        return self._dict_cache

    @property
    def hash_id(self) -> str:
        """Get the hash_id property.

        :return: The hash_id string.
        """
        return self._hash_id

    @property
    def swap_memory(self) -> SwapMemoryObject:
        """Get the swap memory information.

        :return SwapMemoryObject: The swap memory information.
        """
        return self._swap_memory

    @property
    def virtual_memory(self) -> VirtualMemoryObject:
        """Get the virtual memory information.

        :return VirtualMemoryObject: The virtual memory information.
        """
        return self._virtual_memory

    def __repr__(self) -> str:
        """Get the string representation of the MemoryInfo instance.

        :return: The string representation of the MemoryInfo.
        """
        # Get the init parameters excluding 'type' and 'version'
        init_params = dict(self._data_params())
        init_params.pop('type', None)
        init_params.pop('version', None)

        calling_args = ', '.join(f'{key}={getattr(self, key)!r}' for key in init_params)
        return f'{self.__class__.__name__}({calling_args})'

    def __hash__(self) -> int:
        """Get the hash of the MemoryInfo instance.

        :return: The hash value.
        """
        return hash(self.hash_id)

    def __eq__(self, other: object) -> bool:
        """Check equality between two MemoryInfo instances.

        :param other: The other object to compare.
        :return: True if equal, False otherwise.
        """
        if not isinstance(other, MemoryInfo):
            return NotImplemented
        return self.hash_id == other.hash_id
