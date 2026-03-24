"""SwapMemory version 1 class.

This class represents swap memory information in a memory-info object.

It implements validation and serialization/deserialization methods to and from dictionaries
for the swap_memory object in the following JSON Schema:

https://raw.githubusercontent.com/JerilynFranz/python-simplebench/main/schemas/v1/memory-info.json
"""

from types import MappingProxyType
from typing import Any

from simplebench.report.base import BaseSwapMemoryObject

from . import _validate
from .swap_memory_dict import ImmutableSwapMemoryObjectDict, SwapMemoryObjectDict

__all__: list[str] = []


class SwapMemoryObject(BaseSwapMemoryObject):
    """Class representing swap memory information in a memory-info object."""

    _init_params_cache: MappingProxyType[str, Any] = MappingProxyType({})
    """Cache for the constructor parameters of the SwapMemoryObject class."""

    @classmethod
    def _data_params(cls) -> MappingProxyType[str, Any]:
        """Get the constructor parameters for the schema data class.

        The parameters are cached after the first call for performance.

        It is returned as a read-only mapping.

        :return MappingProxyType[str, Any]: A read-only mapping of constructor parameter names and types.
        """
        if not cls._init_params_cache:
            params = cls.init_params(SwapMemoryObjectDict)
            cls._init_params_cache = MappingProxyType(params)
        return cls._init_params_cache

    __slots__ = ('_total', '_used', '_free', '_percent', '_swap_in', '_swap_out', '_hash_id', '_dict_cache')

    def __init__(self, *,
            total: int,
            used: int,
            free: int,
            percent: float,
            swap_in: int,
            swap_out: int) -> None:
        """Initialize MemoryInfo.

        :param total: Total swap memory in bytes.
        :param used: Used swap memory in bytes.
        :param free: Free swap memory in bytes.
        :param percent: Percentage of swap memory used.
        :param swap_in: Swap memory sent to disk in bytes.
        :param swap_out: Swap memory received from disk in bytes.
        """
        self._total: int = _validate.total(total)
        self._used: int = _validate.used(used)
        self._free: int = _validate.free(free)
        self._percent: float = _validate.percent(percent)
        self._swap_in: int = _validate.swap_in(swap_in)
        self._swap_out: int = _validate.swap_out(swap_out)
        self._hash_id: str = self._hash_id_helper(ImmutableSwapMemoryObjectDict)
        self._dict_cache: ImmutableSwapMemoryObjectDict = self._to_dict_helper(ImmutableSwapMemoryObjectDict)

    @classmethod
    def from_dict(cls, data: SwapMemoryObjectDict) -> 'SwapMemoryObject':
        """Create a SwapMemoryObject instance from a dictionary.

        .. code-block:: python
           :caption: Example

           swap_memory = SwapMemoryObject.from_dict(data)

        :param data: The dictionary containing the SwapMemoryObject data.
        :return SwapMemoryObject: A SwapMemoryObject instance.
        """
        allowed_keys = cls._data_params()
        kwargs = cls.import_data(data=data, allowed_fields=allowed_keys, process_as={})
        return cls(**kwargs)

    def to_dict(self) -> ImmutableSwapMemoryObjectDict:
        """Return an immutable dictionary representation of the SwapMemoryObject.

        :return ImmutableSwapMemoryObjectDict: A dictionary representation of the SwapMemoryObject.
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

    @property
    def percent(self) -> float:
        """Get the percentage of swap memory used.

        :return: The percentage of swap memory used.
        """
        return self._percent

    @property
    def swap_in(self) -> int:
        """Get the swap memory sent to disk in bytes.

        :return: The swap memory sent to disk in bytes.
        """
        return self._swap_in

    @property
    def swap_out(self) -> int:
        """Get the swap memory received from disk in bytes.

        :return: The swap memory received from disk in bytes.
        """
        return self._swap_out

    def for_json(self) -> SwapMemoryObjectDict:
        """Get the JSON-serializable dictionary representation of this SwapMemoryObject.

        This method delegates to the for_json method of the dictionary returned by :meth:`to_dict`
        because the dictionary is actually an instance of :class:`CoreDataMapping`
        which has the for_json method to convert to a JSON-serializable dictionary.

        :return: The JSON-serializable dictionary representation of this SwapMemoryObject.
        """
        return self.to_dict().for_json()  # type: ignore

    def as_json(self) -> str:
        """Get the JSON string representation of this SwapMemoryObject.

        This method delegates to the as_json method of the dictionary returned by :meth:`to_dict`
        because the dictionary is actually an instance of :class:`CoreDataMapping`
        which has the as_json method to convert to a JSON string.

        :return: The JSON string representation of this SwapMemoryObject.
        """
        return self.to_dict().as_json()  # type: ignore

    def __repr__(self) -> str:
        """Get the string representation of the SwapMemoryObject instance.

        :return: The string representation of the SwapMemoryObject.
        """
        # Get the init parameters excluding 'type' and 'version'
        init_params = dict(self._data_params())
        init_params.pop('type', None)
        init_params.pop('version', None)

        calling_args = ', '.join(f'{key}={getattr(self, key)!r}' for key in init_params)
        return f'{self.__class__.__name__}({calling_args})'

    def __hash__(self) -> int:
        """Get the hash of the SwapMemoryObject instance.

        :return: The hash value.
        """
        return hash(self.hash_id)

    def __eq__(self, other: object) -> bool:
        """Check equality between two SwapMemoryObject instances.

        :param other: The other object to compare.
        :return: True if equal, False otherwise.
        """
        if not isinstance(other, SwapMemoryObject):
            return NotImplemented
        return self.hash_id == other.hash_id

    def __copy__(self) -> 'SwapMemoryObject':
        """Return the same instance since SwapMemoryObject is immutable."""
        return self

    def __deepcopy__(self, memo: dict[int, Any]) -> 'SwapMemoryObject':
        """Return the same instance since SwapMemoryObject is immutable."""
        return self
