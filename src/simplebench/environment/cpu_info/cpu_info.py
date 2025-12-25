"""CPU information utility functions.

This provides a CPUInfo class that gathers and exposes information
about the CPU environment at the time of its creation using
the :module:`cpuinfo` module.
"""
from copy import deepcopy

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
    (such as by pickling) this information if needed.


    The class supports two parameters to control how the CPU information
    is gathered and stored:
    - ``use_cache``: If ``True``, the class-level cached CPU information
        from the :module:`cpuinfo` module is used if available; otherwise,
        fresh information is gathered. If ``False``, fresh information
        is always gathered. (default: ``True``)
    - ``detached``: If ``True``, the CPU information in this instance
        will be detached from any changes to the class-level cache
        for CPU information in the :module:`cpuinfo` module. This means that even if the
        class-level cache is updated later, this instance will retain the
        CPU information as it was at the time of initialization. If ``False``,
        the instance will reference the class-level cache directly.

    Note that both ``use_cache`` and ``detached`` cannot be set to ``False``
    at the same time, as this combination does not make sense.
    """
    __slots__ = ('_cache_key', '_info')

    _cpu_info_cache: dict[str, CPUInfoDictType] = {}

    def __init__(self, *, cache_key: str | None = None) -> None:
        """Initializes the instance by gathering data from the `cpuinfo` module.
        
        :param str | None cache_key: An optional key to identify a cache entry.
            If provided, this key can be used to manage multiple cache entries
            for different CPU configurations or environments. If ``None``,
            the a new value is always gathered. (default: ``None``)
       
        :raises SimpleBenchTypeError: If cache_key is not a string or ``None``.
        :raises SimpleBenchValueError: If cache_key is an empty string or contains non-alphanumeric characters.
        """
        self._cache_key: str | None = validate.cache_key(cache_key)
        self._info = self._get_cached_cpu_info(cache_key)


    @classmethod
    def _get_cached_cpu_info(cls, cache_key: str | None) -> CPUInfoDictType:
        """Get the cached CPU information from the `cpuinfo` module.

        :param str | None cache_key: An optional key to identify a cache entry.
        :return CPUInfoDictType: The cached CPU information.
        """
        if cache_key is None:
            return get_cpu_info()

        if cache_key not in cls._cpu_info_cache:
            cls._cpu_info_cache[cache_key] = validate.cpu_info_dict(name="info", value=get_cpu_info())
        return cls._cpu_info_cache[cache_key]

    @property
    def info(self) -> CPUInfoDictType:
        """Get the CPU information dictionary.

        This is a deep copy of the dictionary returned by :func:`cpuinfo.get_cpu_info`
        at the time of this object's initialization.

        To prevent external modifications of the internal state, this property
        always returns a deep copy of the dictionary.

        :return CPUInfoDictType: The CPU information dictionary.
        """
        if self._cache_key is None:
            return deepcopy(self._info)

        # This is necessary to ensure cache refreshes in a shared cache
        return deepcopy(self._get_cached_cpu_info(self._cache_key))

    @classmethod
    def _refresh_cache_key(cls, cache_key: str) -> None:
        """Private method to refresh the class-level keyed cache CPU information."""
        cls._cpu_info_cache[cache_key] = validate.cpu_info_dict(name="cpu_info",
                                                                value=get_cpu_info())

    def refresh_info(self) -> None:
        """Refresh the CPU information.

        This method forces a refresh of the CPU information
        from the :module:`cpu_info` module.

        - If the instance is detached (was created with no ``cache_key``),
          only its internal state is updated.
        - If the instance is attached to a shared cache (was created with a ``cache_key``),
          the corresponding cache entry is updated, affecting all other instances
          attached to the same key.
        """
        if self._cache_key is None:
            self._info = validate.cpu_info_dict(name="cpu_info", value=get_cpu_info())
            return
        self._refresh_cache_key(self._cache_key)

    def detach_from_cache(self) -> None:
        """Detach this instance from the class-level cache.

        After calling this method, the instance will retain its current
        CPU information independently of any future changes to any
        class-level cache in the :module:`cpu_info` module.
        """
        if self._cache_key is None:
            return
        self._info = deepcopy(self._get_cached_cpu_info(self._cache_key))
        self._cache_key = None
