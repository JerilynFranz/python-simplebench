"""Cache entry for immutable core data type references."""
import threading
import weakref
from collections import OrderedDict

from simplebench.types import ImmutableCoreDataTypes

from .cache_key import CacheKey


class CacheEntry:
    """Cache entry for complex immutable core data types.
    
    :property ImmutableCoreDataTypes value: The immutable core data type value.
    :property bool is_valid: Whether the value is valid according to the TypedDict subclass.
    :property CacheKey cache_key: The type and id of the cached value ()
    """
    def __init__(self,
                 value: ImmutableCoreDataTypes,
                 is_valid: bool,
                 cache: OrderedDict[CacheKey, "CacheEntry"],
                 lock: threading.Lock) -> None:
        """Initialize the CacheEntry.

        :param ImmutableCoreDataTypes value: The immutable core data type value.
        :param bool is_valid: Whether the value is valid according to the TypedDict subclass.
        """
        cache_key = CacheKey(value)
        self._cache_key: CacheKey = cache_key
        self._is_valid: bool = is_valid

        def cleanup(ref: weakref.ReferenceType[ImmutableCoreDataTypes]) -> None:  # pylint: disable=unused-argument
            """Cleanup callback for when the cached value is garbage collected.

            :param weakref.ReferenceType[ImmutableCoreDataTypes] ref: The weak reference to the cached value.
            """
            with lock:
                if cache_key in cache:
                    del cache[cache_key]

        self._value: weakref.ReferenceType[ImmutableCoreDataTypes] = weakref.ref(value, cleanup)

    @property
    def value(self) -> ImmutableCoreDataTypes | None:
        """Get the cached immutable core data type value.

        :return ImmutableCoreDataTypes | None: The cached value or None if it has been garbage collected.
        """
        return self._value()

    @property
    def is_valid(self) -> bool:
        """Get whether the cached value is valid.

        :return bool: True if the value is valid, False otherwise.
        """
        return self._is_valid

    @property
    def cache_key(self) -> CacheKey:
        """Get the cache key of the cached value.

        :return CacheKey: The cache key of the cached value.
        """
        return self._cache_key
