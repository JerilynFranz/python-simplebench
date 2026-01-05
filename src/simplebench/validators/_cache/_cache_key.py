"""Cache key for object references."""
from typing import Any, Hashable


class CacheKey:
    """Cache key for object references.

    Keys are based on the specified type and the id() of the object.

    They uniquely identify a specific object instance + a specific type
    for caching purposes. The type is included to allow caching of the same
    object instance under different type contexts.
    
    A weak reference is used to allow garbage collection
    of the cached value when no longer in use. A callback is registered to
    automatically remove the cache entry when the value is garbage collected.

    :property type cls_type: The type of the object.
    :property int instance_id: The id() of the object instance.
    """
    def __init__(self, cls_type: Hashable, obj: Any) -> None:
        """Initialize the CacheKey.

        :param Hashable cls_type: The type of the object.
        :param Any obj: The object value.
        """
        if cls_type is None:  # None is a special case, replace with type(None) instead
            cls_type = type(None)
        self.obj_type: Hashable = cls_type
        self.instance_id: int = id(obj)

    def __hash__(self) -> int:
        return hash((self.obj_type, self.instance_id))

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, CacheKey):
            return NotImplemented
        return (self.obj_type, self.instance_id) == (other.obj_type, other.instance_id)

    def __repr__(self):
        return f"CacheKey(cls_type={repr(self.obj_type)}, instance_id={self.instance_id})"
