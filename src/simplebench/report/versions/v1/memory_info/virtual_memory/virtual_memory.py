"""VirtualMemory version 1 class.

This class represents virtual memory information in a memory-info object.

It implements validation and serialization/deserialization methods to and from dictionaries
for the virtual_memory object in the following JSON Schema:

https://raw.githubusercontent.com/JerilynFranz/python-simplebench/main/schemas/v1/memory-info.json

"""

from types import MappingProxyType
from typing import Any

from simplebench.report.base import BaseVirtualMemoryObject

from . import _validate
from .virtual_memory_dict import ImmutableVirtualMemoryObjectDict, VirtualMemoryObjectDict

__all__: list[str] = []


class VirtualMemoryObject(BaseVirtualMemoryObject):
    """Class representing virtual memory information in a memory-info object."""

    _init_params_cache: MappingProxyType[str, Any] = MappingProxyType({})
    """Cache for the constructor parameters of the VirtualMemoryObject class."""

    @classmethod
    def _data_params(cls) -> MappingProxyType[str, Any]:
        """Get the constructor parameters for the schema data class.

        The parameters are cached after the first call for performance.

        It is returned as a read-only mapping.

        :return MappingProxyType[str, Any]: A read-only mapping of constructor parameter names and types.
        """
        if not cls._init_params_cache:
            params = cls.init_params(VirtualMemoryObjectDict)
            cls._init_params_cache = MappingProxyType(params)
        return cls._init_params_cache

    __slots__ = ('_total', '_available', '_percent', '_used', '_free', '_hash_id', '_dict_cache')

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
        allowed_keys = cls._data_params()
        kwargs = cls.import_data(data=data, allowed_fields=allowed_keys, process_as={})
        return cls(**kwargs)

    def to_dict(self) -> ImmutableVirtualMemoryObjectDict:
        """Return an immutable dictionary representation of the VirtualMemoryObject.

        :return ImmutableVirtualMemoryObjectDict: A dictionary representation of the VirtualMemoryObject.
        """
        return self._dict_cache

    def for_json(self) -> VirtualMemoryObjectDict:
        """Get the JSON-serializable dictionary representation of this VirtualMemoryObject.

        This method delegates to the for_json method of the dictionary returned by :meth:`to_dict`
        because the dictionary is actually an instance of :class:`CoreDataMapping`
        which has the for_json method to convert to a JSON-serializable dictionary.

        :return: The JSON-serializable dictionary representation of this VirtualMemoryObject.
        """
        return self.to_dict().for_json()  # type: ignore

    def as_json(self) -> str:
        """Get the JSON string representation of this VirtualMemoryObject.

        This method delegates to the as_json method of the dictionary returned by :meth:`to_dict`
        because the dictionary is actually an instance of :class:`CoreDataMapping`
        which has the as_json method to convert to a JSON string.

        :return: The JSON string representation of this VirtualMemoryObject.
        """
        return self.to_dict().as_json()  # type: ignore

    @property
    def hash_id(self) -> str:
        """Get the hash_id property.

        :return: The hash_id string.
        :rtype: str
        """
        return self._hash_id

    @property
    def total(self) -> int:
        """Get the total swap memory in bytes.

        :return: The total swap memory in bytes.
        :rtype: int
        """
        return self._total

    @property
    def available(self) -> int:
        """Get the available swap memory in bytes.

        :return: The available swap memory in bytes.
        :rtype: int
        """
        return self._available

    @property
    def percent(self) -> float:
        """Get the percentage of virtual memory used.

        :return: The percentage of virtual memory used.
        :rtype: float
        """
        return self._percent

    @property
    def used(self) -> int:
        """Get the used swap memory in bytes.

        :return: The used swap memory in bytes.
        :rtype: int
        """
        return self._used

    @property
    def free(self) -> int:
        """Get the free swap memory in bytes.

        :return: The free swap memory in bytes.
        :rtype: int
        """
        return self._free

    def __repr__(self) -> str:
        """Get the string representation of the VirtualMemoryObject instance.

        :return: The string representation of the VirtualMemoryObject.
        :rtype: str
        """
        # Get the init parameters excluding 'type' and 'version'
        init_params = dict(self._data_params())
        init_params.pop('type', None)
        init_params.pop('version', None)

        calling_args = ', '.join(f'{key}={getattr(self, key)!r}' for key in init_params)
        return f'{self.__class__.__name__}({calling_args})'

    def __hash__(self) -> int:
        """Get the hash of the VirtualMemoryObject instance.

        :return: The hash value.
        :rtype: int
        """
        return hash(self.hash_id)

    def __eq__(self, other: object) -> bool:
        """Check equality between two VirtualMemoryObject instances.

        :param other: The other object to compare.
        :return: :obj:`True` if equal, :obj:`False` otherwise.
        :rtype: bool
        """
        if not isinstance(other, VirtualMemoryObject):
            return NotImplemented
        return self.hash_id == other.hash_id

    def __copy__(self) -> 'VirtualMemoryObject':
        """Return the same instance since VirtualMemoryObject is immutable."""
        return self

    def __deepcopy__(self, memo: dict[int, Any]) -> 'VirtualMemoryObject':
        """Return the same instance since VirtualMemoryObject is immutable."""
        return self
