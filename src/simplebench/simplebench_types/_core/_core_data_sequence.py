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
        - complex
        - NoneType
    - Sequences of the above types
    - Mappings of str to the above types
    - Sets of the above types
"""
import hashlib
from collections.abc import Hashable, Iterator, Mapping, Sequence, Set
from typing import TYPE_CHECKING, overload

from typechecked import Immutable

from simplebench._log import _log
from simplebench.exceptions import SimpleBenchTypeError

from .._element_collection import ElementCollection, is_element_collection
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

    :param __elements: An iterable of CoreDataTypes elements to initialize the sequence or :obj:`None`.
    :type __elements: Iterable[CoreDataTypes] | None
    """
    def __init__(self, __elements: 'ElementCollection[CoreDataTypes] | None' = None) -> None:
        """Initialize the CoreDataSequence.

        If an iterable is provided, it must be an :class:`ElementCollection`
        containing only elements of type :class:`CoreDataTypes`.

        If no iterable is provided, an empty sequence is created.

        :param __elements: An element collection of CoreDataTypes elements to initialize
            the sequence or :obj:`None`.
        :type __elements: Iterable[CoreDataTypes] | None
        """
        # Import here to avoid circular imports
        from ._core_data_mapping import CoreDataMapping
        from ._core_data_set import CoreDataSet
        from ._types import CORE_DATA_PRIMITIVE_TYPES_TUPLE, CORE_DATA_TYPES_TUPLE

        _log.debug('Initializing CoreDataSequence with iterable: %r', __elements)
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
        self._hash_cache: int | None = None
        self._content_hash_cache: str | None = None

    @overload
    def __getitem__(self, index: int) -> ImmutableCoreDataTypes: ...

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
            self._hash_cache = hash(self._data)
        return self._hash_cache

    def thaw(self) -> list[CoreDataTypes]:
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
