"""Cache for immutable core data type references used in TypedDict validation.
"""
import threading
from collections import OrderedDict

from simplebench.exceptions import SimpleBenchTypeError, SimpleBenchValueError
from simplebench.types import ImmutableCoreDataTypes

from ._error_tags import _ReportElementTypedDictCacheErrorTag
from .cache_entry import CacheEntry
from .cache_key import CacheKey

_MIN_CACHE_SIZE = 100
"""Minimum size of the immutable core data types cache.

This is the smallest allowed size after trimming to ensure effective caching.
Do not set below about 100 to ensure reasonable cache effectiveness.
"""

_MAX_CACHE_SIZE = 16384
"""Maximum size of the immutable core data types cache."""

_CACHE_LOCK: threading.Lock = threading.Lock()
"""Lock for thread-safe access to the immutable core data types cache."""

_IMMUTABLE_ITEMS_CACHE: OrderedDict[CacheKey, CacheEntry] = OrderedDict()
"""Cache for immutable core data type references.

Key: (TypedDict subclass, id(instance))

This structure allows efficient caching and retrieval of immutable core data type
references while minimizing memory usage and lookup time. It is thread-safe
and optimized for performance. It is NOT used to cache mutable data types checks.

It allows quick checks for previously seen TypedDict checks to avoid redundant validation
of the same structure multiple times during report processing. If a subtree matches a cached
immutable core data type + typedict subclass type, it can be reused directly from the cache
without re-validation of the subtree.
"""

_CACHE_LOCK = threading.Lock()
"""Lock for thread-safe access to the immutable core data types cache."""

def valid_in_immutables_cache(value: ImmutableCoreDataTypes) -> bool | None:
    """
    Check if an immutable core data type reference is cached and return its validity
    as matching the TypedDict subclass specification for structure.

    If it was not found in the cache or if the found object is not the same
    object instance as the value passed for cache lookup, it returns `None`.
    This is a strict identity check, not just equality.

    The cache key is based on the type of the value and its id().

    Access is optimized for performance with optimistic lock-free read access and
    thread-safe locking if a cache modification is needed.

    :param ImmutableCoreDataTypes value: The immutable core data value to check.
    :return bool | None: The cached validity if found, or None if not found in cache.
    """
    key: CacheKey = CacheKey(value)
    if key in _IMMUTABLE_ITEMS_CACHE:
        try:  # optimistic access for performance
            entry: CacheEntry = _IMMUTABLE_ITEMS_CACHE[key]
            cached_value = entry.value
            if cached_value is None:
                # Stale reference, remove from cache.
                with _CACHE_LOCK:
                    del _IMMUTABLE_ITEMS_CACHE[key]
                return None
            if cached_value is value:
                return entry.is_valid
        except KeyError:
            # Item was removed between the 'in' check and access by another thread
            return None
    return None


def cache_immutable_reference(entry: CacheEntry) -> None:
    """Cache an immutable core data CacheEntry

    :param ImmutableCoreDataTypes value: The immutable core data type to cache.
    """
    with _CACHE_LOCK:
        _IMMUTABLE_ITEMS_CACHE.setdefault(entry.cache_key, entry)
        trim_immutables_cache(_MAX_CACHE_SIZE)

def trim_immutables_cache(size: int) -> None:
    """Trim the immutable core data type cache to the specified size.

    If the cache exceeds the specified size, the oldest entries are removed
    until the cache size is at or below 75% of the specified
    size (rounding down).

    This helps maintain cache efficiency while preventing unbounded growth
    and minimizing performance impact from frequent trimming.

    The smallest allowed size is set by `_MIN_CACHE_SIZE`.

    Cache trimming is performed within a thread-safe lock.

    :param int size: The maximum size of the cache.
    :raises SimpleBenchTypeError: If size is not an integer.
    :raises SimpleBenchValueError: If size is less than 1.
    """
    if not isinstance(size, int):
        raise SimpleBenchTypeError(
            'Cache size must be an integer.',
            tag=_ReportElementTypedDictCacheErrorTag.INVALID_CACHE_SIZE_TYPE)

    # Minimum size to ensure effective caching and no exceptions during trimming
    if size < _MIN_CACHE_SIZE:
        raise SimpleBenchValueError(
            f'Cache size must be at least {_MIN_CACHE_SIZE}.',
            tag=_ReportElementTypedDictCacheErrorTag.INVALID_CACHE_SIZE)

    with _CACHE_LOCK:
        target_size = max(int(size * 0.75), 2)  # backstopped at 2 to prevent exceptions
        while len(_IMMUTABLE_ITEMS_CACHE) > target_size:
            _IMMUTABLE_ITEMS_CACHE.popitem(last=False)

def clear_immutables_cache() -> None:
    """Clear the entire immutable core data types cache."""
    with _CACHE_LOCK:
        _IMMUTABLE_ITEMS_CACHE.clear()

def get_immutables_cache_size() -> int:
    """Get the current size of the immutable core data types cache.

    :return int: The number of entries in the cache.
    """
    with _CACHE_LOCK:
        return len(_IMMUTABLE_ITEMS_CACHE)


class CacheEntryFactory:
    """Factory for creating CacheEntry instances."""
    def __call__(self, value: ImmutableCoreDataTypes, is_valid: bool) -> CacheEntry:
        """Create a CacheEntry instance.

        :param ImmutableCoreDataTypes value: The immutable core data type value.
        :param bool is_valid: Whether the value is valid according to the TypedDict subclass.
        :return CacheEntry: The created CacheEntry instance.
        """
        return CacheEntry(value, is_valid, _IMMUTABLE_ITEMS_CACHE, _CACHE_LOCK)
