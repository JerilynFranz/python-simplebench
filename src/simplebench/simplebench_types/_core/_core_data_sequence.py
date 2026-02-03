"""Core data sequence type for SimpleBench

This is an immutable sequence of core data types used in SimpleBench.

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
from typing import TYPE_CHECKING, Any, overload

import simplejson
from typechecked import Immutable

from simplebench._log import _log
from simplebench.exceptions import SimpleBenchTypeError

from .._element_collection import ElementCollection, is_element_collection
from . import _common
from ._error_tags import _CoreDataErrorTag

if TYPE_CHECKING:
    from ._types import CoreDataTypes, ImmutableCoreDataTypes


class CoreDataSequence(Sequence['ImmutableCoreDataTypes'],
                       ElementCollection['ImmutableCoreDataTypes'],
                       Immutable,
                       Hashable):
    """Deep-immutable Sequence container for CoreData types used in SimpleBench.

    This represents a sequence where all elements are of type :class:`CoreData`.

    When initializing, the provided collection must be an :class:`ElementCollection`
    containing only elements of type :class:`CoreDataTypes`.

    The sequence itself is immutable once created with all contents being of valid CoreData types
    and converted to their respective immutable CoreData wrappers as needed.

    :param __elements: A collection of CoreDataTypes elements to initialize the sequence or :obj:`None`.
    :type __elements: Iterable[CoreDataTypes] | None
    """
    __slots__ = ('_version', '_data', '_hash_cache', '_content_hash_cache')

    def __init__(self, __elements: 'ElementCollection[CoreDataTypes] | None' = None) -> None:
        """Initialize the CoreDataSequence.

        If a collection is provided, it must be an :class:`ElementCollection`
        containing only elements of type :class:`CoreDataTypes`.

        If no collection is provided, an empty sequence is created.

        :param __elements: A collection of CoreDataTypes elements to initialize
            the sequence or :obj:`None`.
        :type __elements: ElementCollection[CoreDataTypes] | None
        """
        # Import here to avoid circular imports
        from ._core_data_mapping import CoreDataMapping
        from ._core_data_set import CoreDataSet
        from ._types import CORE_DATA_PRIMITIVE_TYPES_TUPLE, CORE_DATA_TYPES_TUPLE

        _log.debug('Initializing CoreDataSequence with iterable: %r', __elements)
        self._version: int = 1
        self._hash_cache: int | None = None
        self._content_hash_cache: str | None = None

        self._data: tuple[ImmutableCoreDataTypes, ...]
        if __elements is None:
            self._data = ()
            return

        if not is_element_collection(__elements):
            raise SimpleBenchTypeError(
                'CoreDataSequence must be initialized with an ElementCollection of CoreData.',
                tag=_CoreDataErrorTag.CORE_DATA_SEQUENCE_NOT_ELEMENT_COLLECTION)

        data: list[ImmutableCoreDataTypes] = []
        if all(isinstance(item, CORE_DATA_PRIMITIVE_TYPES_TUPLE) for item in __elements):
            self._data = tuple(__elements)
            return

        for item in __elements:
            if isinstance(item, CORE_DATA_PRIMITIVE_TYPES_TUPLE):
                data.append(item)
            elif isinstance(item, (CoreDataMapping, CoreDataSequence, CoreDataSet)):
                data.append(item)
            elif isinstance(item, Mapping):
                data.append(CoreDataMapping(item))
            elif isinstance(item, Set):
                data.append(CoreDataSet(item))
            elif isinstance(item, Sequence) and not isinstance(item, (str, bytes)):
                data.append(CoreDataSequence(item))

            else:
                 raise SimpleBenchTypeError(
                    f'Invalid item type passed to CoreDataSequence: {item!r}. '
                    f'Must be a CoreData type: {CORE_DATA_TYPES_TUPLE!r}.',
                    tag=_CoreDataErrorTag.CORE_DATA_SEQUENCE_INVALID_ITEM_TYPE)

        self._data = tuple(data)


    @overload
    def __getitem__(self, index: int) -> 'ImmutableCoreDataTypes': ...

    @overload
    def __getitem__(self, index: slice) -> 'CoreDataSequence': ...

    def __getitem__(self, index: int | slice) -> 'ImmutableCoreDataTypes':
        """Get the item or slice at the specified index.

        If an integer index is provided, returns the element at that position,
        which may be any member of :class:`ImmutableCoreDataTypes` (including
        nested CoreDataSequence, CoreDataSet, CoreDataMapping, or primitive types).

        If a slice is provided, returns a new :class:`CoreDataSequence` containing
        the sliced elements.

        :param index: The index or slice of the item(s) to retrieve.
        :type index: int | slice
        :returns: The item at the specified index, or a CoreDataSequence for a slice.
        :rtype: ImmutableCoreDataTypes or CoreDataSequence
        :raises IndexError: If the index is out of range.
        """
        if isinstance(index, slice):
            return CoreDataSequence(self._data[index])
        return self._data[index]

    def __setitem__(self, index: int, value: 'ImmutableCoreDataTypes') -> None:
        """Raise an error since CoreDataSequence is immutable.

        :param index: The index to set.
        :type index: int
        :param value: The value to set.
        :type value: :class:`ImmutableCoreDataTypes`
        :raises SimpleBenchTypeError: Always, since CoreDataSequence is immutable.
        """
        raise SimpleBenchTypeError(
            'CoreDataSequence is immutable and does not support item assignment.',
            tag=_CoreDataErrorTag.CORE_DATA_SEQUENCE_INVALID_ITEM_TYPE)

    def __contains__(self, item: object) -> bool:
        """Check if the item is in the CoreDataSequence.

        :param item: The item to check for membership.
        :type item: object
        :returns: :obj:`True` if the item is in the sequence, :obj:`False` otherwise.
        :rtype: bool
        """
        return item in self._data

    def __iter__(self) -> Iterator['ImmutableCoreDataTypes']:
        """Return an iterator over the CoreDataSequence.

        :returns: An iterator over the elements in the sequence.
        :rtype: Iterator[ImmutableCoreDataTypes]
        """
        return iter(self._data)

    def __len__(self) -> int:
        """Return the number of elements in the CoreDataSequence.

        :returns: The number of elements in the sequence.
        :rtype: int
        """
        return len(self._data)

    def __repr__(self) -> str:
        """Return the string representation of the CoreDataSequence.

        :returns: The string representation of the sequence.
        :rtype: str
        """
        return f'CoreDataSequence({self._data!r})'

    def __eq__(self, other: object) -> bool:
        """Check equality with another CoreDataSequence.

        :param other: The other object to compare.
        :type other: object
        :returns: :obj:`True` if the sequences are equal, :obj:`False` otherwise.
        :rtype: bool
        """
        if not isinstance(other, CoreDataSequence):
            return False
        return self.content_hash() == other.content_hash()

    def content_hash(self) -> str:
        """Return a SHA256 hash of the CoreDataSequence content.

        :returns: The SHA256 hash of the sequence content as a hexadecimal string.
        :rtype: str
        """
        from ._core_data_mapping import CoreDataMapping
        from ._core_data_set import CoreDataSet
        if self._content_hash_cache is None:
            hasher = hashlib.sha256()
            for item in self._data:
                if isinstance(item, (CoreDataSequence, CoreDataMapping, CoreDataSet)):
                    hasher.update(item.content_hash().encode('utf-8'))
                else:
                    hasher.update(repr(item).encode('utf-8'))
            self._content_hash_cache = hasher.hexdigest()
        return self._content_hash_cache

    def __hash__(self) -> int:
        """Return the hash of the CoreDataSequence.

        :returns: The hash of the sequence.
        :rtype: int
        """
        if self._hash_cache is None:
            self._hash_cache = hash(self.content_hash())
        return self._hash_cache

    def thaw(self) -> list['CoreDataTypes']:
        """Convert the CoreDataSequence to a standard mutable list.

        :returns: A mutable list representation of the CoreDataSequence.
        :rtype: list[CoreDataTypes]
        """
        # Import here to avoid circular imports
        from ._core_data_mapping import CoreDataMapping
        from ._core_data_set import CoreDataSet

        thawed_list: list[CoreDataTypes] = []
        for value in self._data:
            if isinstance(value, (CoreDataSet, CoreDataMapping, CoreDataSequence)):
                thawed_list.append(value.thaw())
            else:
                thawed_list.append(value)
        return thawed_list

    def for_json(self) -> list['CoreDataTypes']:
        """Convert the CoreDataSequence to a JSON-serializable list.

        :returns: A JSON-serializable list representation of the CoreDataSequence.
        :rtype: list[CoreDataTypes]
        """
        return self.thaw()

    def as_json(self) -> str:
        """Serialize the CoreDataSequence to a JSON string.

        :returns: A JSON string representation of the CoreDataSequence.
        :rtype: str
        """
        return simplejson.dumps(
            self.for_json(), sort_keys=True, separators=(',', ':'), for_json=True, iterable_as_array=True)

    def count(self, value: 'ImmutableCoreDataTypes') -> int:
        """Return the number of occurrences of value in the CoreDataSequence.

        This method counts how many times the specified value appears
        in the sequence. It is similar to the built-in list.count() method
        but adapted for CoreData types. It uses rich comparison to ensure
        that values are compared correctly according to their content.

        It is an intelligent count that uses rich comparison to ensure
        that values are compared correctly according to their content.

        This means that a comparision of a nested CoreDataSequence, CoreDataSet, or
        CoreDataMapping will compare their contents rather than their
        object identities.

        This is similar to how count is performed in standard Python collections,
        but has been adapted for improved performance for the CoreData types
        used in SimpleBench.

        .. note:: This method may be less efficient than a simple
              count when performed one time due to the need for
              rich comparison, especially for large sequences or
              deeply nested structures.

              This is partially mitigated by the fact that
              CoreDataSequence is immutable, so the content hashes
              can be cached for faster comparisons if multiple counts
              are performed without requiring re-comparision of all
              intermediate values.

        :param value: The value to count.
        :type value: ImmutableCoreDataTypes
        :returns: The number of occurrences of value.
        :rtype: int
        """
        from ._core_data_mapping import CoreDataMapping
        from ._core_data_set import CoreDataSet
        from ._types import CORE_DATA_PRIMITIVE_TYPES_TUPLE

        if not (isinstance(value, CORE_DATA_PRIMITIVE_TYPES_TUPLE) or
              isinstance(value, (CoreDataSequence, CoreDataMapping, CoreDataSet))):
              raise SimpleBenchTypeError(
            f'Invalid value type passed to CoreDataSequence.count(): {value!r}. '
            f'Must be a CoreData type: {CORE_DATA_PRIMITIVE_TYPES_TUPLE!r} '
            f'or CoreDataSequence, CoreDataMapping, CoreDataSet.',
            tag=_CoreDataErrorTag.CORE_DATA_SEQUENCE_INVALID_ITEM_TYPE)
        comparison_value = _common.rich_compare_value(value)
        count = 0
        for item in self._data:
            if _common.rich_compare_value(item) == comparison_value:
                count += 1
        return count

    def __getstate__(self) -> tuple[dict[str, Any] | None, tuple[Any, ...]]:
        """Prepare the object's state for pickling, prioritizing size.

        This method ensures that the pickled representation of the CoreDataSequence
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
                f'Unsupported CoreDataSequence pickled version: {version!r}.',
                tag=_CoreDataErrorTag.CORE_DATA_SEQUENCE_UNSUPPORTED_PICKLE_VERSION)

        match version:
            case 1:
                for slot, value in zip(slots, slot_values, strict=True):
                    # Use object.__setattr__ to bypass our immutable setters.
                    object.__setattr__(self, slot, value)
            case _:
                raise SimpleBenchTypeError(
                    f'Unsupported CoreDataSequence pickled version: {version!r}.',
                    tag=_CoreDataErrorTag.CORE_DATA_SEQUENCE_UNSUPPORTED_PICKLE_VERSION)

    def __deepcopy__(self, memo: dict[int, Any]) -> 'CoreDataSequence':
        """Return the same CoreDataSequence.

        Since the CoreDataSequence instance is immutable and composed of
        immutable components, there is no need to perform a deep copy
        of its contents. Instead, we simply return the instance itself
        which is a extremely fast O(1) operation.

        If a true deep copy is required for some reason, the caller
        can manually create a new instance by passing the thawed contents
        to the constructor.

        :param memo: The memoization dictionary used by `copy.deepcopy`.
                     It is not used in this optimized implementation.
        :return CoreDataSequence: The same CoreDataSequence instance.
        """
        # because the CoreDataSequence is immutable, we return self
        # instead of performing an actual copy.
        return self
