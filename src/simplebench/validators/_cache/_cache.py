"""Cache for validation results.
"""
import logging
import threading
from collections import OrderedDict
from typing import Any, Hashable

from simplebench.exceptions import SimpleBenchTypeError, SimpleBenchValueError

from ._cache_entry import CacheEntry, ObjectWrapper
from ._cache_key import CacheKey
from ._error_tags import _ValidationCacheErrorTag

log = logging.getLogger(__name__)

class ValidationCache:
    """Cache for validated references.

    This structure allows efficient caching and retrieval of references while
    with their validity state while minimizing memory usage and lookup time.
    It is thread-safe and optimized for performance.

    It allows quick checks for previously seen validation checks to avoid redundant
    validation of the same structure multiple times during report processing.
    """
    def __init__(self, min_cache_size: int = 100, max_cache_size: int = 16384) -> None:
        """Initialize the ValidationCache.
        
        :param int min_cache_size: Minimum size of the cache.
            This is the smallest allowed size after trimming to ensure effective caching.
            Do not set below about 100 to ensure reasonable cache effectiveness.
        :param int max_cache_size: Maximum size of the cache.
        """
        self._min_cache_size: int = min_cache_size
        """Minimum size of the cache.
        This is the smallest allowed size after trimming to ensure effective caching.
        Do not set below about 100 to ensure reasonable cache effectiveness.
        """
        self._max_cache_size: int = max_cache_size
        """Maximum size of the cache."""

        self._cache_lock: threading.RLock = threading.RLock()
        """Lock for thread-safe access to the cache."""

        self._cache: OrderedDict[CacheKey, CacheEntry] = OrderedDict()
        """Cache for validated references.

        This structure allows efficient caching and retrieval of references while
        with their validity state while minimizing memory usage and lookup time.
        It is thread-safe and optimized for performance.

        It allows quick checks for previously seen validation checks to avoid redundant validation
        of the same structure multiple times during report processing. If a subtree matches a cached
        object id and class it can be reused directly from the cache without re-validation of the subtree.
        """

    def valid_in_cache(self, td_cls: Hashable, obj: object) -> bool | None:
        """
        Check if a reference validity is cached and return its validity if found.

        If it was not found in the cache or if the found object is not the same
        object instance as the value passed for cache lookup, it returns `None`.
        This is a strict identity check that the obj in the cache is the same object,
        not just 'equal' to it.

        The cache key is based on the type of the value and its id().

        Access is optimized for performance with optimistic lock-free read access and
        thread-safe locking if a cache modification is needed.

        :param Hashable td_cls: The type hint of the value reference to check.
        :param object obj: The object reference to check.
        :return bool | None: The cached validity if found, or None if not found in cache.
        """
        log.debug("valid_in_cache: Checking cache for object of type '%s' with id %d",
                  td_cls, id(obj))
        key: CacheKey = CacheKey(td_cls, obj)
        if key in self._cache:
            try:  # optimistic access for performance
                entry: CacheEntry = self._cache[key]
                wrapped_value: ObjectWrapper | None = entry.obj_wrapper
                if wrapped_value is None:
                    # Stale reference, remove from cache.
                    with self._cache_lock:
                        del self._cache[key]
                    return None
                if wrapped_value.obj is obj:  # strict identity check, which is why we keep the object in the wrapper
                    return entry.is_valid
            except KeyError:
                # Item was removed between the 'in' check and access by another thread
                return None
        return None

    def add_cache_entry(self,
            td_cls: Hashable, obj: object, is_valid: bool, noncachable_types: set[type[Any]] | None = None) -> None:
        """Cache a CacheEntry

        :param Hashable td_cls: The type hint of the object.
        :param object obj: The object to cache.
        :param bool is_valid: The validity of the object.
        """
        log.debug("add_cache_entry: Caching object of type '%s' with id %d as valid=%s",
                  td_cls, id(obj), is_valid)
        if noncachable_types is not None and type(obj) in noncachable_types:
            log.debug("add_cache_entry: Not caching object of type '%s' as it is in noncachable_types",
                      td_cls)
            return
        item = CacheEntry(td_cls, obj, is_valid, self._cache, self._cache_lock)
        with self._cache_lock:
            self._cache.setdefault(item.cache_key, item)
        self.trim_cache(self._max_cache_size)

    def trim_cache(self, size: int) -> None:
        """Trim the cache to the specified size.

        If the cache exceeds the specified size, the oldest entries are removed
        until the cache size is at or below 75% of the specified
        size (rounding down).

        This helps maintain cache efficiency while preventing unbounded growth
        and minimizing performance impact from frequent trimming.

        The smallest allowed size is set by `self._min_cache_size`.

        Cache trimming is performed within a thread-safe lock.

        :param int size: The maximum size of the cache.
        :raises SimpleBenchTypeError: If size is not an integer.
        :raises SimpleBenchValueError: If size is less than 1.
        """
        log.debug("trim_cache: Cache size %d. Trimming cache to size %d", len(self._cache), size)

        with self._cache_lock:
            if len(self._cache) <= size:
                return

        if not isinstance(size, int):
            raise SimpleBenchTypeError(
                'Cache size must be an integer.',
                tag=_ValidationCacheErrorTag.INVALID_CACHE_SIZE_TYPE)

        # Minimum size to ensure effective caching and no exceptions during trimming
        if size < self._min_cache_size:
            raise SimpleBenchValueError(
                f'Cache size must be at least {self._min_cache_size}.',
                tag=_ValidationCacheErrorTag.INVALID_CACHE_SIZE)

        with self._cache_lock:
            target_size = max(int(size * 0.75), 2)  # backstopped at 2 to prevent exceptions
            while len(self._cache) > target_size:
                self._cache.popitem(last=False)
        log.debug("trim_cache: Cache trimmed to size %d", len(self._cache))

    def clear(self) -> None:
        """Clear the entire cache."""
        log.debug("clear_cache: Clearing entire cache")
        with self._cache_lock:
            self._cache.clear()

    def get_cache_size(self) -> int:
        """Get the current size of the cache.

        :return int: The number of entries in the cache.
        """
        log.debug("get_cache_size: Getting current cache size")
        with self._cache_lock:
            return len(self._cache)
