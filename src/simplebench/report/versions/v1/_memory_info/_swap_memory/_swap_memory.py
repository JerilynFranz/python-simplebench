"""SwapMemory version 1 class.

This class represents swap memory information in a memory-info object.

It implements validation and serialization/deserialization methods to and from dictionaries
for the swap_memory object in the following JSON Schema:

https://raw.githubusercontent.com/JerilynFranz/python-simplebench/main/schemas/v1/memory-info.json

"""
from simplebench.report._base import BaseSwapMemoryObject
from simplebench.report.versions.v1 import ImmutableSwapMemoryObjectDict, SwapMemoryObjectDict

from . import _validate


class SwapMemoryObject(BaseSwapMemoryObject):
    """Class representing swap memory information in a memory-info object."""
    __slots__ = ('_total', '_used', '_free', '_percent', '_swap_in', '_swap_out', '_hash_id')
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
        allowed_keys = cls.init_params()
        kwargs = cls.import_data(
            data=data,
            allowed_fields=allowed_keys,
            process_as={})
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
