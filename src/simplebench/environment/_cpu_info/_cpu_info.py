"""CPU information utility functions.

This provides an immutable CPUInfo class that gathers and exposes information
about the CPU environment at the time of its creation using
the :module:`cpuinfo` module.
"""

from functools import cache

from cpuinfo import get_cpu_info  # type: ignore  # cpuinfo doesn't have type stubs
from typechecked import Immutable

from simplebench.report.versions.v1 import ImmutableCPUInfoData

from . import _validate

__all__: list[str] = []


class CPUInfo(Immutable):
    """Immutable object containing CPU information gathered from the :module:`cpuinfo` module.

    Because the CPU information can be quite detailed and complex,
    this is represented as a dictionary property called :attr:`info`
    that contains all the information returned by :func:`cpuinfo.get_cpu_info`
    after being validated and converted to an immutable
    :class:`~simplebench.simplebench_types.CoreDataMappingType`
    object type cast as a :class:`ImmutableCPUInfoData` :class:`~typing.TypedDict`
    value for static type checking purposes.

    This class snapshots the CPU information at initialization,
    providing a consistent view of the CPU environment that can be
    easily passed around and used in other parts of the application
    or reporting tools and makes it possible to serialize
    (such as by pickling) this information if needed.)

    .. note:: Unpickled CPUInfo instances will be equal to the original instance
        but do not share cached data instances with the original CPUInfo.

    It can cache the gathered CPU information based on an optional
    cache key provided at initialization time. If a cache key is provided,
    subsequent instances created with the same key will reuse the previously
    cached information instead of gathering it anew.

    If no cache key is provided (cache_key is :obj:`None`), a new snapshot of
    the CPU information is gathered each time an instance is created.

    This is done because the collection of CPU information can be time-consuming,
    and caching allows for efficient reuse of the data when multiple
    instances are created in the same runtime environment.
    """

    __slots__ = ('_cache_key', '_info')

    @cache
    @staticmethod
    def _get_cached_cpu_info(cache_key: str) -> ImmutableCPUInfoData:  #  pylint: disable=unused-argument
        """Get the cached CPU information from the `cpuinfo` module.

        The data is validated and converted a :class:`~simplebench.simplebench_types.CoreDataMappingType`
        object that is typed as a :class:`ImmutableCPUInfoData` :class:`~typing.TypedDict`
        for static type checking purposes.

        Cache is managed based on the provided cache key by the :func:`functools.cache` decorator.

        :param str | None cache_key: An optional key to identify a cache entry.
        :return ImmutableCPUInfoData: The CPU information as an immutable dictionary.
        """
        return _validate.cpu_info({'data': get_cpu_info() })

    def __init__(self, cache_key: str | None = None) -> None:
        """Initializes the instance by gathering data from the `cpuinfo` module.

        The returned instance is immutable.

        :param cache_key: (optional) A key to identify a cache entry.

            If provided, this key can be used to manage multiple cache entries
            for snapshots taken at different times. If :obj:`None`,
            then a new value is always gathered. (default: :obj:`None`)

            When a cache_key is provided, and not already present in the cache,
            the CPU information is gathered from the :module:`cpuinfo` module and stored
            in the cache under the given key. Subsequent instances created with
            the same key will reuse the previously cached information.

            If not :obj:`None`, the cache_key must be a non-empty string containing
            only alphanumeric characters.
        :type cache_key: str | None

        :raises SimpleBenchTypeError: If cache_key is not a string or :obj:`None`.
        :raises SimpleBenchValueError: If cache_key is an empty string or contains non-alphanumeric characters.
        """
        self._cache_key: str | None = _validate.cache_key(cache_key)
        self._info: ImmutableCPUInfoData = _validate.cpu_info(
            {'data': get_cpu_info() }) if cache_key is None else self.__class__._get_cached_cpu_info(cache_key)

    def to_dict(self) -> ImmutableCPUInfoData:
        """Get the CPU information dictionary.

        This dictionary contains all the CPU information gathered from the
        :module:`cpuinfo` module at the time of this instance's creation
        as an immutable :class:`ImmutableCPUInfoData` :class:`~typing.TypedDict`.

        It returns a :class:`~simplebench.simplebench_types.CoreDataMappingType`
        object, so it cannot be modified although it functionally behaves like a
        standard dictionary.

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

    def __repr__(self) -> str:
        """Get the string representation of the CPUInfo instance.

        The representation includes the cache key (if any) and the CPU information dictionary.

        It is useful for debugging and logging purposes but cannot be used to recreate
        the instance.

        :return: The string representation of the instance.
        :rtype: str
        """
        return f'{self.__class__.__name__}(cache_key={self._cache_key!r}, info={self._info!r})'

    def __eq__(self, other: object) -> bool:
        """Check equality between this CPUInfo instance and another object.

        Two CPUInfo instances are considered equal if their CPU information
        dictionaries are equal, regardless of their cache keys.

        :param other: The object to compare with.
        :return: True if the objects are equal, False otherwise.
        :rtype: bool
        """
        if not isinstance(other, CPUInfo):
            return NotImplemented
        return self._info == other._info

    def __hash__(self) -> int:
        """Get the hash value of the CPUInfo instance.

        The hash is computed based on the CPU information dictionary,
        allowing CPUInfo instances to be used in sets and as dictionary keys.

        :return: The hash value of the instance.
        :rtype: int
        """
        return hash(self._info)
