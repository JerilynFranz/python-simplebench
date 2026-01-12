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

from typing import cast

from simplebench.report._base import BaseMemoryInfo, JSONSchema

from . import _validate
from ._memory_info_schema import MemoryInfoSchema
from ._swap_memory import SwapMemoryObject
from ._typeddict_types import ImmutableMemoryInfoDict, MemoryInfoData, MemoryInfoDict
from ._virtual_memory import VirtualMemoryObject


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

    def __init__(
        self, *, hash_id: str = '', swap_memory: SwapMemoryObject, virtual_memory: VirtualMemoryObject
    ) -> None:
        """Initialize MemoryInfo.

        :param str hash_id: The unique hash identifier for the machine information.
        :param int total_physical: Total physical memory in bytes.
        :param int total_swap: Total configured swap memory in bytes.
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
            process_as={},
        )
        return cls(**kwargs)

    def to_dict(self) -> ImmutableMemoryInfoDict:
        """The MemoryInfo as an immutable dictionary.

        :return MemoryInfoDict: A dictionary representation of the MemoryInfo.
        """
        return cast(ImmutableMemoryInfoDict, self._dict_cache)

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
