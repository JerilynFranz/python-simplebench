"""Cache key for immutable core data type references."""
from simplebench.types import ImmutableCoreDataTypes


class CacheKey:
    """Cache key for immutable core data type references.

    Keys are based on the TypedDict subclass type and the id() of the instance.
    They uniquely identify a specific immutable core data type instance
    for caching purposes. A weak reference is used to allow garbage collection
    of the cached value when no longer in use. A callback is registered to
    automatically remove the cache entry when the value is garbage collected.

    :property type cls_type: The TypedDict subclass type.
    :property int instance_id: The id() of the immutable core data type instance.
    """
    def __init__(self, value: ImmutableCoreDataTypes) -> None:
        """Initialize the CacheKey.

        :param ImmutableCoreDataTypes value: The immutable core data type value.
        """
        self.cls_type: type = type(value)
        self.instance_id: int = id(value)

    def __hash__(self) -> int:
        return hash((self.cls_type, self.instance_id))

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, CacheKey):
            return NotImplemented
        return (self.cls_type, self.instance_id) == (other.cls_type, other.instance_id)

    def __repr__(self):
        return f"CacheKey(cls_type={self.cls_type.__name__}, instance_id={self.instance_id})"
