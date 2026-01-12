"""VirtualMemory version 1 class.

This class represents virtual memory information in a memory-info object.

It implements validation and serialization/deserialization methods to and from dictionaries
for the virtual_memory object in the following JSON Schema:

https://raw.githubusercontent.com/JerilynFranz/python-simplebench/main/schemas/v1/memory-info.json

"""

from simplebench.report.base import BaseSwapMemoryObject

from . import _validate
from ._typeddict_types import ImmutableVirtualMemoryObjectDict, VirtualMemoryObjectDict

__all__ = ['VirtualMemoryObject']


class VirtualMemoryObject(BaseSwapMemoryObject):
    """Class representing virtual memory information in a memory-info object."""

    __slots__ = ('_total', '_available', '_percent', '_used', '_free', '_hash_id')

    def __init__(self, *, total: int, available: int, percent: float, used: int, free: int) -> None:
        """Initialize MemoryInfo.

        :param int total: Total virtual memory in bytes.
        :param int available: Available virtual memory in bytes.
        :param float percent: Percentage of virtual memory used.
        :param int used: Used virtual memory in bytes.
        :param int free: Free virtual memory in bytes.
        """
        self._total: int = _validate.total(total)
        self._available: int = _validate.available(available)
        self._percent: float = _validate.percent(percent)
        self._used: int = _validate.used(used)
        self._free: int = _validate.free(free)
        self._hash_id: str = self._hash_id_helper(ImmutableVirtualMemoryObjectDict)
        self._dict_cache: ImmutableVirtualMemoryObjectDict = self._to_dict_helper(ImmutableVirtualMemoryObjectDict)

    @classmethod
    def from_dict(cls, data: VirtualMemoryObjectDict) -> 'VirtualMemoryObject':
        """Create a VirtualMemoryObject instance from a dictionary.
        .. code-block:: python
           :caption: Example

           virtual_memory = VirtualMemoryObject.from_dict(data)
        :param data: The dictionary containing the VirtualMemoryObject data.
        :return VirtualMemoryObject: A VirtualMemoryObject instance.
        """
        allowed_keys = cls.init_params()
        kwargs = cls.import_data(data=data, allowed_fields=allowed_keys, process_as={})
        return cls(**kwargs)

    def to_dict(self) -> ImmutableVirtualMemoryObjectDict:
        """Return an immutable dictionary representation of the VirtualMemoryObject.

        :return ImmutableVirtualMemoryObjectDict: A dictionary representation of the VirtualMemoryObject.
        """
        return self._dict_cache

    @property
    def hash_id(self) -> str:
        """Get the hash_id property.

        :return: The hash_id string.
        """
        return self._hash_id

    @property
    def total(self) -> int:
        """Get the total swap memory in bytes.

        :return: The total swap memory in bytes.
        """
        return self._total

    @property
    def available(self) -> int:
        """Get the available swap memory in bytes.

        :return: The available swap memory in bytes.
        """
        return self._available

    @property
    def percent(self) -> float:
        """Get the percentage of virtual memory used.

        :return: The percentage of virtual memory used.
        """
        return self._percent

    @property
    def used(self) -> int:
        """Get the used swap memory in bytes.

        :return: The used swap memory in bytes.
        """
        return self._used

    @property
    def free(self) -> int:
        """Get the free swap memory in bytes.

        :return: The free swap memory in bytes.
        """
        return self._free
