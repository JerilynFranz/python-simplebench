"""Cache for immutable core data type references used in TypedDict validation.
"""
import threading
from collections import OrderedDict

from simplebench.exceptions import SimpleBenchTypeError, SimpleBenchValueError

from ._cache_entry import CacheEntry
from ._cache_key import CacheKey
from ._error_tags import _ReportElementTypedDictCacheErrorTag

_MIN_CACHE_SIZE = 100
"""Minimum size of the cache.

This is the smallest allowed size after trimming to ensure effective caching.
Do not set below about 100 to ensure reasonable cache effectiveness.
"""

_MAX_CACHE_SIZE = 16384
"""Maximum size of the cache."""

_CACHE_LOCK: threading.Lock = threading.Lock()
"""Lock for thread-safe access to the cache."""

_CACHE: OrderedDict[CacheKey, CacheEntry] = OrderedDict()
"""Cache for validated references.

This structure allows efficient caching and retrieval of references while
with their validity state whileminimizing memory usage and lookup time. It is thread-safe
and optimized for performance.

It allows quick checks for previously seen validation checks to avoid redundant validation
of the same structure multiple times during report processing. If a subtree matches a cached
object id and class it can be reused directly from the cache without re-validation of the subtree.
"""

_CACHE_LOCK = threading.Lock()
"""Lock for thread-safe access to the cache."""

def valid_in_cache(td_cls: type, obj: object) -> bool | None:
    """
    Check if a reference validity is cached and return its validity if found.

    If it was not found in the cache or if the found object is not the same
    object instance as the value passed for cache lookup, it returns `None`.
    This is a strict identity check, not just equality.

    The cache key is based on the type of the value and its id().

    Access is optimized for performance with optimistic lock-free read access and
    thread-safe locking if a cache modification is needed.

    :param type td_cls: The type of the value reference to check.
    :param object obj: The object reference to check.
    :return bool | None: The cached validity if found, or None if not found in cache.
    """
    key: CacheKey = CacheKey(td_cls, obj)
    if key in _CACHE:
        try:  # optimistic access for performance
            entry: CacheEntry = _CACHE[key]
            cached_value = entry.obj
            if cached_value is None:
                # Stale reference, remove from cache.
                with _CACHE_LOCK:
                    del _CACHE[key]
                return None
            if cached_value is obj:
                return entry.is_valid
        except KeyError:
            # Item was removed between the 'in' check and access by another thread
            return None
    return None

def add_cache_entry(td_cls: type, obj: object, is_valid: bool) -> None:
    """Cache a CacheEntry

    :param object obj: The object to cache.
    :param bool is_valid: The validity of the object.
    """
    item = CacheEntry(td_cls, obj, is_valid, _CACHE, _CACHE_LOCK)
    with _CACHE_LOCK:
        _CACHE.setdefault(item.cache_key, item)
        trim_cache(_MAX_CACHE_SIZE)

def trim_cache(size: int) -> None:
    """Trim the cache to the specified size.

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
        while len(_CACHE) > target_size:
            _CACHE.popitem(last=False)

def clear_cache() -> None:
    """Clear the entire cache."""
    with _CACHE_LOCK:
        _CACHE.clear()

def get_cache_size() -> int:
    """Get the current size of the cache.

    :return int: The number of entries in the cache.
    """
    with _CACHE_LOCK:
        return len(_CACHE)

__all__ = [
    "valid_in_cache",
    "add_cache_entry",
    "clear_cache",
]
