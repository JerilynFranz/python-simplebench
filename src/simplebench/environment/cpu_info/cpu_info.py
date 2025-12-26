"""CPU information utility functions.

This provides an immutable CPUInfo class that gathers and exposes information
about the CPU environment at the time of its creation using
the :module:`cpuinfo` module.
"""
from copy import deepcopy
from functools import cache

from cpuinfo import get_cpu_info

from . import validate
from .types import CPUInfoDictType


class CPUInfo:
    """Wraps CPU information gathered from the :module:`cpuinfo` module.

    Because the CPU information can be quite detailed and complex,
    this is represented as a dictionary property called :attr:`info`
    that contains all the information returned by :func:`cpuinfo.get_cpu_info`.

    This class snapshots the CPU information at initialization,
    providing a consistent view of the CPU environment that can be
    easily passed around and used in other parts of the application
    or reporting tools and makes it possible to serialize
    (such as by pickling) this information if needed.)
    """
    __slots__ = ('_cache_key', '_info')

    @cache
    @staticmethod
    def _get_cached_cpu_info(cache_key: str) -> CPUInfoDictType:  #  pylint: disable=unused-argument
        """Get the cached CPU information from the `cpuinfo` module.

        :param str | None cache_key: An optional key to identify a cache entry.
        :return CPUInfoDictType: The cached CPU information.
        """
        return get_cpu_info()

    def __init__(self, cache_key: str | None = None) -> None:
        """Initializes the instance by gathering data from the `cpuinfo` module.

        The returned instance is immutable.
        
        :param str | None cache_key: An optional key to identify a cache entry.
            If provided, this key can be used to manage multiple cache entries
            for snapshots taken at different times. If ``None``, the a new value
            is always gathered. (default: ``None``)

            When a cache_key is provided, and not already present in the cache,
            the CPU information is gathered from the `cpuinfo` module and stored
            in the cache under the given key. Subsequent instances created with
            the same key will reuse the cached information.

            If not ``None``, the cache_key must be a non-empty string containing
            only alphanumeric characters.

        :raises SimpleBenchTypeError: If cache_key is not a string or ``None``.
        :raises SimpleBenchValueError: If cache_key is an empty string or contains non-alphanumeric characters.
        """
        self._cache_key: str | None = validate.cache_key(cache_key)
        cls = self.__class__
        self._info = get_cpu_info() if cache_key is None else deepcopy(cls._get_cached_cpu_info(cache_key))



    @property
    def info(self) -> CPUInfoDictType:
        """Get the CPU information dictionary.

        This is a deep copy of the dictionary returned by :func:`cpuinfo.get_cpu_info`
        at the time of this object's initialization.

        To prevent external modifications of the internal state, this property
        always returns a deep copy of the dictionary.

        :return CPUInfoDictType: The CPU information dictionary.
        """
        return deepcopy(self._info)
