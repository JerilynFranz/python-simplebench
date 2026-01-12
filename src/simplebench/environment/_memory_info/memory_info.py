"""System memory information utility functions."""

from functools import cache
from types import MappingProxyType
from typing import NamedTuple, cast

from simplebench.report.versions.v1 import ImmutableMemoryInfoData

_PSUTIL_AVAILABLE: bool = False  # pylint: disable=invalid-name
try:
    import psutil

    _PSUTIL_AVAILABLE = True  # pylint: disable=invalid-name
except ImportError:
    pass


__all__ = ['MemoryInfo', 'SwapMemory', 'VirtualMemory']


class SwapMemory(NamedTuple):
    """System swap memory information NamedTuple.

    :param total: Total swap memory in bytes.
    :param used: Used swap memory in bytes.
    :param free: Free swap memory in bytes.
    :param percent: Percentage of swap memory used.
    :param swap_in: Swap memory sent to disk in bytes.
    :param swap_out: Swap memory received from disk in bytes.
    """

    total: int
    """Total swap memory in bytes."""
    used: int
    """Used swap memory in bytes."""
    free: int
    """Free swap memory in bytes."""
    percent: float
    """Percentage of swap memory used."""
    swap_in: int
    """Swap memory sent to disk in bytes."""
    swap_out: int
    """Swap memory received from disk in bytes."""


class VirtualMemory(NamedTuple):
    """System virtual memory information NamedTuple.

    :param total: Total virtual memory in bytes.
    :param available: Available virtual memory in bytes.
    :param percent: Percentage of virtual memory used.
    :param used: Used virtual memory in bytes.
    :param free: Free virtual memory in bytes.
    """

    total: int
    """Total virtual memory in bytes."""
    available: int
    """Available virtual memory in bytes."""
    percent: float
    """Percentage of virtual memory used."""
    used: int
    """Used virtual memory in bytes."""
    free: int
    """Free virtual memory in bytes."""


def _uncached_swap_memory() -> SwapMemory:
    """Get the swap memory information from the :module:`psutil` module without caching.

    :return SwapMemory: The swap memory information.
    """
    if not _PSUTIL_AVAILABLE:
        return SwapMemory(0, 0, 0, 0.0, 0, 0)

    smem = psutil.swap_memory()  # type: ignore[reportPossiblyUnboundVariable]
    return SwapMemory(
        total=smem.total, used=smem.used, free=smem.free, percent=smem.percent, swap_in=smem.sin, swap_out=smem.sout
    )


@cache
def _get_swap_memory(cache_key: str | None = None) -> SwapMemory:  #  pylint: disable=unused-argument
    """Get the swap memory information from the :module:`psutil` module.

    If :module:`psutil` is not available, this will return None
    If a cache_key is provided, it can be used to identify a cache entry.
    It no cache_key is provided, a default cache entry is used.

    :param str | None cache_key: An optional key to identify a cache entry.
    :return int: The total swap memory in bytes.
    """
    return _uncached_swap_memory()


def _uncached_virtual_memory() -> VirtualMemory:
    """Get the virtual memory information from the :module:`psutil` module without caching.

    :return VirtualMemory: The virtual memory information.
    """
    if not _PSUTIL_AVAILABLE:
        return VirtualMemory(0, 0, 0.0, 0, 0)
    vmem = psutil.virtual_memory()  # type: ignore[reportPossiblyUnboundVariable]
    return VirtualMemory(
        total=vmem.total, available=vmem.available, percent=vmem.percent, used=vmem.used, free=vmem.free
    )


@cache
def _get_virtual_memory(cache_key: str | None = None) -> VirtualMemory:  #  pylint: disable=unused-argument
    """Get the virtual memory information from the :module:`psutil` module.

    If :module:`psutil` is not available, this will return 0.
    If a cache_key is provided, it can be used to identify a cache entry.
    It no cache_key is provided, a default cache entry is used.

    :param str | None cache_key: An optional key to identify a cache entry.
    :return int: The available memory in bytes.
    """
    return _uncached_virtual_memory()


class MemoryInfo:
    """A snapshot of the system's memory configuration.

    This class attempts to use the 'psutil' library to gather information
    about the system's memory. If 'psutil' is not installed,
    all values will be 0.

    To enable memory reporting, you can install it as an extra:
        pip install simplebench[memory]

    """

    __slots__ = ('_vmem', '_smem', '_dict_cache')

    def __init__(self, cache_key: str | None = None) -> None:
        """Initializes the MemoryInfo object by querying psutil.

        If cache_key is provided, it will be used to cache the memory
        information for faster subsequent access.

        A cache_key of None will return an uncached result.

        If psutil is not available, all memory values are set to 0.
        """
        if cache_key is None:
            self._vmem: VirtualMemory = _uncached_virtual_memory()
            self._smem: SwapMemory = _uncached_swap_memory()
        elif isinstance(cache_key, str):
            self._vmem = _get_virtual_memory(cache_key)
            self._smem = _get_swap_memory(cache_key)
        else:
            raise TypeError('cache_key must be a string or None')
        self._dict_cache: ImmutableMemoryInfoData | None = None

    @property
    def virtual_memory(self) -> VirtualMemory:
        """Get the virtual memory information.

        :return VirtualMemory: The virtual memory information.
        """
        return self._vmem

    @property
    def swap_memory(self) -> SwapMemory:
        """Get the swap memory information.

        :return SwapMemory: The swap memory information.
        """
        return self._smem

    def to_dict(self) -> ImmutableMemoryInfoData:
        """Return the MemoryInfo as an ImmutableMemoryInfoData dictionary.
        The returned dictionary is an immutable MappingProxyType and
        is cached for subsequent calls to this method.

        :return ImmutableMemoryInfoData: A dictionary representation of the MemoryInfo.
        """
        if self._dict_cache is None:
            self._dict_cache = cast(
                ImmutableMemoryInfoData,
                MappingProxyType(
                    {
                        'virtual_memory': MappingProxyType(
                            {
                                'total': self.virtual_memory.total,
                                'available': self.virtual_memory.available,
                                'percent': self.virtual_memory.percent,
                                'used': self.virtual_memory.used,
                                'free': self.virtual_memory.free,
                            }
                        ),
                        'swap_memory': MappingProxyType(
                            {
                                'total': self.swap_memory.total,
                                'used': self.swap_memory.used,
                                'free': self.swap_memory.free,
                                'percent': self.swap_memory.percent,
                                'swap_in': self.swap_memory.swap_in,
                                'swap_out': self.swap_memory.swap_out,
                            }
                        ),
                    }
                ),
            )
        return self._dict_cache
