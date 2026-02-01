"""CPU information utility functions.

This provides an immutable CPUInfo class that gathers and exposes information
about the CPU environment at the time of its creation using
the :module:`cpuinfo` module.
"""

from functools import cache

from cpuinfo import get_cpu_info  # type: ignore
from typechecked import Immutable

from simplebench.report.versions.v1 import ImmutableCPUInfoData
from simplebench.validators import typed_dict_mimic, validate_core_data_mapping

from . import _validate

__all__: list[str] = []


class CPUInfo(Immutable):
    """Immutable object containing CPU information gathered from the :module:`cpuinfo` module.

    Because the CPU information can be quite detailed and complex,
    this is represented as a dictionary property called :attr:`info`
    that contains all the information returned by :func:`cpuinfo.get_cpu_info`
    after being validated and converted to an immutable :class:`~types.MappingProxyType`
    object typed as a :class:`ImmutableCPUInfoData` :class:`~typing.TypedDict`.

    This class snapshots the CPU information at initialization,
    providing a consistent view of the CPU environment that can be
    easily passed around and used in other parts of the application
    or reporting tools and makes it possible to serialize
    (such as by pickling) this information if needed.)

    It can cache the gathered CPU information based on an optional
    cache key provided at initialization time. If a cache key is provided,
    subsequent instances created with the same key will reuse the previously
    cached information instead of gathering it anew.

    :property ImmutableCPUInfoData info: An immutable dictionary containing all
        the CPU information gathered by the :module:`cpuinfo` module at the
        time of the instance's creation.
    """

    __slots__ = ('_cache_key', '_info')

    @cache
    @staticmethod
    def _get_cached_cpu_info(cache_key: str) -> ImmutableCPUInfoData:  #  pylint: disable=unused-argument
        """Get the cached CPU information from the `cpuinfo` module.

        The data is validated and converted to an immutable :class:`~types.MappingProxyType`
        object that is typed as a :class:`ImmutableCPUInfoData` :class:`~typing.TypedDict`
        for static type checking purposes.

        :param str | None cache_key: An optional key to identify a cache entry.
        :return ImmutableCPUInfoData: The CPU information as an immutable dictionary.
        """
        validated_data = validate_core_data_mapping(get_cpu_info(), 'CPUInfo.data')
        cpu_info: ImmutableCPUInfoData = typed_dict_mimic(validated_data, ImmutableCPUInfoData)
        return cpu_info

    def __init__(self, cache_key: str | None = None) -> None:
        """Initializes the instance by gathering data from the `cpuinfo` module.

        The returned instance is immutable.

        :param str | None cache_key: An optional key to identify a cache entry.
            If provided, this key can be used to manage multiple cache entries
            for snapshots taken at different times. If ``None``, then a new value
            is always gathered. (default: ``None``)

            When a cache_key is provided, and not already present in the cache,
            the CPU information is gathered from the `cpuinfo` module and stored
            in the cache under the given key. Subsequent instances created with
            the same key will reuse the previously cached information.

            If not ``None``, the cache_key must be a non-empty string containing
            only alphanumeric characters.

        :raises SimpleBenchTypeError: If cache_key is not a string or ``None``.
        :raises SimpleBenchValueError: If cache_key is an empty string or contains non-alphanumeric characters.
        """
        self._cache_key: str | None = _validate.cache_key(cache_key)
        cls = self.__class__
        if cache_key is None:  # No caching; always gather fresh data if None
            validated_data = validate_core_data_mapping(get_cpu_info(), 'CPUInfo.data')
            self._info = typed_dict_mimic({'data': validated_data}, ImmutableCPUInfoData)
        else:
            self._info = cls._get_cached_cpu_info(cache_key)

    @property
    def info(self) -> ImmutableCPUInfoData:
        """Get the CPU information dictionary.

        This dictionary contains all the CPU information gathered from the
        :module:`cpuinfo` module at the time of this instance's creation
        as an immutable :class:`ImmutableCPUInfoData` :class:`~typing.TypedDict`.

        It returns a :class:`~types.MappingProxyType` object, so it cannot be modified
        although it functionally behaves like a standard dictionary.

        Because the data is immutable, it is safe to share and pass around
        without risk of unintended modifications. Because it is typed as a
        :class:`ImmutableCPUInfoData`, static type checkers can verify correct
        usage of the data contained within it by checking for the presence
        and types of specific keys.

        The :func:`typechecked.is_immutable` function will recognize this
        dictionary as immutable.

        :return ImmutableCPUInfoData: The CPU information dictionary.
        """
        return self._info

    def to_dict(self) -> ImmutableCPUInfoData:
        """Get the CPU information dictionary.

        This dictionary contains all the CPU information gathered from the
        :module:`cpuinfo` module at the time of this instance's creation
        as an immutable :class:`ImmutableCPUInfoData` :class:`~typing.TypedDict`.

        It returns a :class:`~types.MappingProxyType` object, so it cannot be modified
        although it functionally behaves like a standard dictionary.

        Because the data is immutable, it is safe to share and pass around
        without risk of unintended modifications. Because it is typed as a
        :class:`ImmutableCPUInfoData`, static type checkers can verify correct
        usage of the data contained within it by checking for the presence
        and types of specific keys.

        The :func:`typechecked.is_immutable` function will recognize this
        dictionary as immutable.

        :return ImmutableCPUInfoData: The CPU information dictionary.
        """
        return self._info
