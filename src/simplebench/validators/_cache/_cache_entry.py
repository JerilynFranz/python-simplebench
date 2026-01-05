"""Cache entry for validation results."""
import threading
import weakref
from collections import OrderedDict
from typing import Any, Hashable

from ._cache_key import CacheKey


class ObjectWrapper:
    """A wrapper to allow weak references to any object.
    
    :property Any obj: The wrapped object.
    """
    __slots__ = ("obj", "__weakref__")

    def __init__(self, obj: Any):
        """Initialize the ObjectWrapper.

        :param Any obj: The object to wrap.
        """
        self.obj = obj


class CacheEntry:
    """Cache entry for validation results.
    
    :param Hashable td_cls: The type associated with the cached object.
    :property object obj: The object having its validity cached.
    :property bool is_valid: Whether the object is valid.
    :property CacheKey cache_key: The cache key for the cached object.
    """
    def __init__(self,
                 td_cls: Hashable,
                 obj: object,
                 is_valid: bool,
                 cache: OrderedDict[CacheKey, "CacheEntry"],
                 lock: threading.RLock) -> None:
        """Initialize the CacheEntry.

        :param ImmutableCoreDataTypes value: The immutable core data type value.
        :param bool is_valid: Whether the value is valid according to the TypedDict subclass.
        """
        cache_key = CacheKey(td_cls, obj)
        self._cache_key: CacheKey = cache_key
        self._is_valid: bool = is_valid

        def cleanup(ref: weakref.ReferenceType[ObjectWrapper]) -> None:  # pylint: disable=unused-argument
            """Cleanup callback for when the cached object is garbage collected.

            :param weakref.ReferenceType[object] ref: The weak reference to the cached object.
            """
            with lock:
                if cache_key in cache:
                    del cache[cache_key]

        self._value: weakref.ReferenceType[ObjectWrapper] = weakref.ref(ObjectWrapper(obj), cleanup)

    @property
    def obj_wrapper(self) -> ObjectWrapper | None:
        """Get the cached wrapper object.

        The returned object may be None if it has been garbage collected.
        If the object is still alive, it is wrapped in an ObjectWrapper and the real object
        can be accessed via the `obj` attribute of the wrapper.

        This allows weak referencing of any object, even those that do not support weak references directly
        or `None` values.

        .. code-block:: python

            cached_entry = cache_entry.obj_wrapper
            if cached_entry is not None:
                real_obj = cached_entry.obj
            else:
                # The cached object has been garbage collected

        :return ObjectWrapper | None: The wrapper to the cached object or None if it has been garbage collected.
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
