"""Cache entry for immutable core data type references."""

import threading
import weakref
from collections import OrderedDict

from ._cache_key import CacheKey


class CacheEntry:
    """Cache entry for complex immutable core data types.

    :param type td_cls: The type associated with the cached object.
    :property object obj: The object having its validity cached.
    :property bool is_valid: Whether the object is valid.
    :property CacheKey cache_key: The cache key for the cached object.
    """

    def __init__(
        self,
        td_cls: type,
        obj: object,
        is_valid: bool,
        cache: OrderedDict[CacheKey, 'CacheEntry'],
        lock: threading.Lock,
    ) -> None:
        """Initialize the CacheEntry.

        :param ImmutableCoreDataTypes value: The immutable core data type value.
        :param bool is_valid: Whether the value is valid according to the TypedDict subclass.
        """
        cache_key = CacheKey(td_cls, obj)
        self._cache_key: CacheKey = cache_key
        self._is_valid: bool = is_valid

        def cleanup(ref: weakref.ReferenceType[object]) -> None:  # pylint: disable=unused-argument
            """Cleanup callback for when the cached object is garbage collected.

            :param weakref.ReferenceType[object] ref: The weak reference to the cached object.
            """
            with lock:
                if cache_key in cache:
                    del cache[cache_key]

        self._value: weakref.ReferenceType[object] = weakref.ref(obj, cleanup)

    @property
    def obj(self) -> object | None:
        """Get the cached object.

        :return object | None: The cached object or None if it has been garbage collected.
        """
        return self._value()

    @property
    def is_valid(self) -> bool:
        """Get whether the cached object is valid.

        :return bool: True if the object is valid, False otherwise.
        """
        return self._is_valid

    @property
    def cache_key(self) -> CacheKey:
        """Get the cache key of the cached value.

        :return CacheKey: The cache key of the cached value.
        """
        return self._cache_key
