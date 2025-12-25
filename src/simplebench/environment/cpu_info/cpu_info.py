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
    __slots__ = ('_use_cache', '_detached', '_info')

    _cpu_info_cache: CPUInfoDictType = {}

    def __init__(self, *,
                 use_cache: bool = True,
                 detached: bool = False,
                ) -> None:
        """Initializes the instance by gathering data from the `cpuinfo` module.
        
        - If ``use_cache`` is ``True`` and ``detached`` is ``False``, the instance uses the
          cached CPU information from the `cpuinfo` module.
        - If ``use_cache`` is ``True`` and ``detached`` is ``True``, the instance makes a deep copy
          of the cached CPU information to ensure it is detached from future changes.
        - If ``use_cache`` is ``False`` and ``detached`` is ``True``, the instance gathers fresh CPU information
          and uses it directly. This instance will not be affected by future changes to the cache.
        - If both ``use_cache`` and ``detached`` are ``False``, a ``SimpleBenchValueError`` is raised
          because this combination does not make sense.

        The FIRST time this class is instantiated it will populate the class-level cache.

        :param bool use_cache: If ``True``, class-level cached CPU information is used
            to initialized the CPUInfo instance if available; otherwise, fresh
            information is gathered. It cannot be set to ``False`` if ``detached``
            is also set to ``False``. (default: ``True``)
        :param bool detached: If ``True``, the CPU information in this instance
            will be detached from any changes to the class-level cache
            for CPU information in the `cpuinfo` module. This means that even if the
            class-level cache is updated later, this instance will retain the
            CPU information as it was at the time of initialization. It cannot
            be set to ``False`` if ``use_cache`` is also set to ``False``.
        :raises SimpleBenchValueError: If both ``use_cache`` and ``detached`` are set to ``False``.

        """
        validate.use_cache_and_detached(use_cache, detached)

        self._detached: bool = detached
        self._use_cache: bool = use_cache
        self._info: CPUInfoDictType = {}

        self._get_cached_cpu_info()  # Ensure cache is populated at first use

        if detached:
            if use_cache:
                self._info = deepcopy(self._get_cached_cpu_info())
            else:
                self._info = get_cpu_info()

    @classmethod
    def _get_cached_cpu_info(cls) -> CPUInfoDictType:
        """Get the cached CPU information from the `cpuinfo` module.

        If the class-level cache is empty, this method gathers fresh CPU information
        and populates the cache.

        :return CPUInfoDictType: The cached CPU information.
        """
        if not cls._cpu_info_cache:
            cls._cpu_info_cache = validate.cpu_info_dict(
                                        name="info",
                                        value=get_cpu_info())
        return cls._cpu_info_cache

    @property
    def info(self) -> CPUInfoDictType:
        """Get the CPU information dictionary.

        This is a deep copy of the dictionary returned by :func:`cpuinfo.get_cpu_info`
        at the time of this object's initialization.

        To prevent external modifications of the internal state, this property
        always returns a deep copy of the dictionary.

        :return CPUInfoDictType: The CPU information dictionary.
        """
        if self._detached:
            return deepcopy(self._info)

        # This is necessary to ensure cache refreshes if not detached
        return deepcopy(self._get_cached_cpu_info())

    @classmethod
    def refresh_cache(cls) -> None:
        """Refresh the class-level cached CPU information.

        This method gathers fresh CPU information from the `cpuinfo` module
        and updates the class-level cache. Instances of `CPUInfo` that are not detached
        will reflect the updated cache when their `info` property is accessed.
        """
        cls._cpu_info_cache = get_cpu_info()
