"""Core data set type for SimpleBench

This is an immutable set of core data types used in SimpleBench.

Allowed types are:
    - CoreDataMapping
    - CoreDataSequence
    - CoreDataSet
    - Core data primitive types:
        - str
        - bytes
        - int
        - float
        - bool
        - NoneType
    - Sequences of the above types
    - Mappings of str to the above types
    - Sets of the above types
"""
import hashlib
from collections.abc import Hashable, Iterator, Mapping, Sequence, Set
from typing import TYPE_CHECKING, Any

from typechecked import Immutable

from simplebench.exceptions import SimpleBenchAssertionError, SimpleBenchTypeError

from .._element_collection import ElementCollection, is_element_collection
from . import _common
from ._error_tags import _CoreDataErrorTag

if TYPE_CHECKING:
    from ._types import CoreDataTypes, ImmutableCoreDataTypes


class CoreDataSet(Set['ImmutableCoreDataTypes'],
                  ElementCollection['ImmutableCoreDataTypes'],
                  Immutable,
                  Hashable):
    """Deep-immutable Set container for CoreData types used in SimpleBench.

    This represents a set where all elements are of type :class:`CoreData`.

    When initializing, the provided iterable must be an :class:`ElementCollection`
    containing only elements of type :class:`CoreDataTypes`.

    The set itself is immutable once created with all contents being of valid CoreData types
    and converted to their respective immutable CoreData wrappers as needed.

    :param __elements: An iterable of CoreData elements to initialize the set or :obj:`None`.
    :type __elements: Iterable[CoreData] | None
    """

    def __init__(self, __elements: 'ElementCollection[CoreDataTypes] | None' = None) -> None:
        """Initialize the CoreDataSet.

        If an iterable is provided, it must be an :class:`ElementCollection`
        containing only elements of type :class:`CoreDataTypes`.

        If no iterable is provided, an empty set is created.

        :param __elements: An iterable of CoreData elements to initialize the set or :obj:`None`.
        :type __elements: Iterable[CoreData] | None
        """
        from ._core_data_mapping import CoreDataMapping
        from ._core_data_sequence import CoreDataSequence
        from ._types import CORE_DATA_PRIMITIVE_TYPES_TUPLE, CoreDataTypes, ImmutableCoreDataTypes

        self._hash_cache: int | None = None
        self._content_hash_cache: str | None = None
        self._data: set[ImmutableCoreDataTypes]

        if __elements is None:
            self._data = set()
            return

        if not is_element_collection(__elements):
            raise SimpleBenchTypeError(
                'CoreDataSet must be initialized with an ElementCollection of CoreData.',
                tag=_CoreDataErrorTag.CORE_DATA_SET_NOT_ELEMENT_COLLECTION)
        data: set[CoreDataTypes] = set()

        if all(isinstance(item, CORE_DATA_PRIMITIVE_TYPES_TUPLE) for item in __elements):
            self._data = set(__elements)
            return

        for item in __elements:
            if isinstance(item, CORE_DATA_PRIMITIVE_TYPES_TUPLE):
                data.add(item)
            elif isinstance(item, (CoreDataMapping, CoreDataSequence, CoreDataSet)):
                data.add(item)
            elif isinstance(item, Mapping):
                data.add(CoreDataMapping(item))
            elif isinstance(item, Set):
                data.add(CoreDataSet(item))
            elif isinstance(item, Sequence) and not isinstance(item, (str, bytes)):
                data.add(CoreDataSequence(item))
            else: # Invalid type of data passed
                 raise SimpleBenchAssertionError(
                    f'Invalid item type passed to CoreDataSet: {item!r}. '
                    f'Must be a CoreData type: {CORE_DATA_PRIMITIVE_TYPES_TUPLE!r}.',
                    tag=_CoreDataErrorTag.CORE_DATA_SET_INVALID_ITEM_TYPE)

        # Wrap in frozenset to ensure immutability
        # We've already validated all items are ImmutableCoreDataTypes
        self._data = frozenset(data)  # type: ignore[arg-type]

    def __contains__(self, item: object) -> bool:
        """Check if the item is in the CoreDataSet.

        :param item: The item to check for membership.
        :type item: object
        :returns: :obj:`True` if the item is in the set, :obj:`False` otherwise.
        :rtype: bool
        """
        return item in self._data

    def __iter__(self) -> Iterator['ImmutableCoreDataTypes']:
        """Return an iterator over the CoreDataSet.

        :returns: An iterator over the elements in the set.
        :rtype: Iterator[CoreDataTypes]
        """
        return iter(self._data)

    def __len__(self) -> int:
        """Return the number of elements in the CoreDataSet.

        :returns: The number of elements in the set.
        :rtype: int
        """
        return len(self._data)

    def __repr__(self) -> str:
        """Return the string representation of the CoreDataSet.

        :returns: The string representation of the set.
        :rtype: str
        """
        return f'CoreDataSet({self._data!r})'

    def __eq__(self, other: object) -> bool:
        """Check equality with another CoreDataSet.

        :param other: The other object to compare.
        :type other: object
        :returns: :obj:`True` if the sets are equal, :obj:`False` otherwise.
        :rtype: bool
        """
        if not isinstance(other, CoreDataSet):
            return False
        return self._data == other._data

    def content_hash(self) -> str:
        """Return a SHA256 hash of the CoreDataSet content.

        :returns: The SHA256 hash of the set content as a hexadecimal string.
        :rtype: str
        """
        from ._core_data_mapping import CoreDataMapping
        from ._core_data_sequence import CoreDataSequence
        if self._content_hash_cache is None:
            hasher = hashlib.sha256()
            # We don't care what the order is, just that it is consistent
            values = sorted(self._data, key=_common.rich_compare_value)
            for item in values:
                if isinstance(item, (CoreDataSequence, CoreDataMapping, CoreDataSet)):
                    hasher.update(item.content_hash().encode('utf-8'))
                else:
                    hasher.update(repr(item).encode('utf-8'))
            self._content_hash_cache = hasher.hexdigest()
        return self._content_hash_cache


    def __hash__(self) -> int:
        """Return the hash of the CoreDataSet.

        :returns: The hash of the set.
        :rtype: int
        """
        if self._hash_cache is None:
            self._hash_cache = hash(self._data)
        return self._hash_cache

    def thaw(self) -> set['CoreDataTypes']:
        """Convert the CoreDataSequence to a standard mutable set.

        :returns: A mutable set representation of the CoreDataSequence.
        :rtype: set[CoreDataTypes]
        """
        # Import here to avoid circular imports
        from ._core_data_mapping import CoreDataMapping
        from ._core_data_sequence import CoreDataSequence

        thawed_set: set[CoreDataTypes] = set()
        for value in self._data:
            if isinstance(value, (CoreDataSet, CoreDataMapping, CoreDataSequence)):
                thawed_set.add(value.thaw())
            else:
                thawed_set.add(value)
        return thawed_set

    def __getstate__(self) -> tuple[dict[str, Any] | None, tuple[Any, ...]]:
        """Prepare the object's state for pickling, prioritizing size.

        This method ensures that the pickled representation of the CoreDataSet
        is as compact as possible. It achieves this by excluding any cached
        attributes that can be recomputed upon unpickling, such as hash caches.

        Because the internal data is stored as python built-in types (tuples,
        dicts, sets and other python primitive types), the pickled size is minimized.

        Future versions of SimpleBench may change the pickling format, so
        pickled data should not be considered stable across versions.

        A version number is included in the pickled state to allow for
        potential future migrations if the internal structure changes.

        It is always in the 0th index of the state tuple.

        :return: A state tuple for pickling.
        :rtype: tuple[dict[str, Any] | None, tuple[Any, ...]]
        """
        slot_values: list[Any] = []
        for slot in self.__slots__:
            if slot in ('_data', '_version'):
                slot_values.append(getattr(self, slot))
            else:
                slot_values.append(None)

        # Build the state tuple for a __slots__ class. The first element is for
        # __dict__ (None in our case) and the second is a tuple of the slotted values.
        state = tuple(slot_values)
        return (None, state)

    def __setstate__(self, state: tuple[dict[str, Any] | None, tuple[Any, ...]]) -> None:
        """Restore the object's state from a pickled representation.

        This method is the counterpart to `__getstate__`. It takes the state
        tuple and repopulates the instance's `__slots__`.

        .. note::
            This method bypasses `__init__`, which is standard for unpickling.

        :param state: The state tuple from unpickling.
        :type state: tuple[dict[str, Any] | None, tuple[Any, ...]]
        """
        # The first element of the state tuple is for __dict__, which is None for this class.
        # The second element is a tuple of values for the __slots__.
        slots_by_version = {1: ('_version', '_data', '_hash_cache', '_content_hash_cache')}
        slot_values = state[1]
        version = slot_values[0]
        slots = slots_by_version.get(version)
        if slots is None:
            raise SimpleBenchTypeError(
                f'Unsupported CoreDataSet pickled version: {version!r}.',
                tag=_CoreDataErrorTag.CORE_DATA_SET_UNSUPPORTED_PICKLE_VERSION)

        match version:
            case 1:
                for slot, value in zip(slots, slot_values, strict=True):
                    # Use object.__setattr__ to bypass our immutable setters.
                    object.__setattr__(self, slot, value)
            case _:
                raise SimpleBenchTypeError(
                    f'Unsupported CoreDataSet pickled version: {version!r}.',
                    tag=_CoreDataErrorTag.CORE_DATA_SET_UNSUPPORTED_PICKLE_VERSION)

    def __deepcopy__(self, memo: dict[int, Any]) -> 'CoreDataSet':
        """Return the same CoreDataSet.

        Since the CoreDataSet instance is immutable and composed of
        immutable components, there is no need to perform a deep copy
        of its contents. Instead, we simply return the instance itself
        which is a extremely fast O(1) operation.

        If a true deep copy is required for some reason, the caller
        can manually create a new instance by passing the thawed contents
        to the constructor.

        :param memo: The memoization dictionary used by `copy.deepcopy`.
                     It is not used in this optimized implementation.
        :return CoreDataSet: The same CoreDataSet instance.
        """
        # because the CoreDataSet is immutable, we return self
        # instead of performing an actual copy.
        return self
