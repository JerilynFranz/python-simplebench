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
from collections.abc import Hashable, Iterator, Mapping, Sequence, Set
from typing import overload

from typechecked import Immutable

from simplebench.exceptions import SimpleBenchTypeError

from .._element_collection import ElementCollection, is_element_collection
from ._error_tags import _CoreDataErrorTag
from ._types import CORE_DATA_PRIMITIVE_TYPES_TUPLE, IMMUTABLE_CORE_DATA_TYPES_TUPLE, CoreDataTypes


class CoreDataSequence(Sequence[CoreDataTypes], Immutable, Hashable):
    """Deep-immutable Sequence container for CoreData types used in SimpleBench.

    This represents a sequence where all elements are of type :class:`CoreData`.

    When initializing, the provided iterable must be an :class:`ElementCollection`
    containing only elements of type :class:`CoreDataTypes`.

    The sequence itself is immutable once created with all contents being of valid CoreData types
    and converted to their respective immutable CoreData wrappers as needed.

    :param __iterable: An iterable of CoreData elements to initialize the sequence or :obj:`None`.
    :type __iterable: Iterable[CoreData] | None
    """

    def __init__(self, __iterable: ElementCollection | None = None) -> None:
        """Initialize the CoreDataSequence.

        If an iterable is provided, it must be an :class:`ElementCollection`
        containing only elements of type :class:`CoreData`.

        If no iterable is provided, an empty sequence is created.

        :param __iterable: An iterable of CoreData elements to initialize the sequence or :obj:`None`.
        :type __iterable: Iterable[CoreDataTypes] | None
        """
        # Import here to avoid circular imports
        from ._core_data_mapping import CoreDataMapping
        from ._core_data_set import CoreDataSet

        self._data: tuple[CoreDataTypes, ...]
        if __iterable is None:
            self._data: tuple[CoreDataTypes, ...] = ()
            return

        if not is_element_collection(__iterable):
            raise SimpleBenchTypeError(
                'CoreDataSequence must be initialized with an ElementCollection of CoreData.',
                tag=_CoreDataErrorTag.CORE_DATA_SEQUENCE_NOT_ELEMENT_COLLECTION)
        data: list[CoreDataTypes] = []

        for item in __iterable:
            if isinstance(item, Mapping):
                data.append(CoreDataMapping(item))
            elif isinstance(item, Sequence) and not isinstance(item, (str, bytes)):
                data.append(CoreDataSequence(item))
            elif isinstance(item, Set):
                data.append(CoreDataSet(item))
            elif isinstance(item, CORE_DATA_PRIMITIVE_TYPES_TUPLE):
                data.append(item)
            else:
                 raise SimpleBenchTypeError(
                    f'Invalid item type passed to CoreDataSequence: {item!r}. '
                    f'Must be a CoreData type: {IMMUTABLE_CORE_DATA_TYPES_TUPLE!r}.',
                    tag=_CoreDataErrorTag.CORE_DATA_SEQUENCE_INVALID_ITEM_TYPE)

        self._data = tuple(data)

    @overload
    def __getitem__(self, index: int) -> CoreDataTypes: ...

    @overload
    def __getitem__(self, index: slice) -> 'CoreDataSequence': ...

    def __getitem__(self, index: int | slice) -> 'CoreDataTypes | CoreDataSequence':
        """Get the item or slice at the specified index.

        :param index: The index or slice of the item(s) to retrieve.
        :type index: int | slice
        :returns: The item at the specified index or a CoreDataSequence for a slice.
        :rtype: CoreData | CoreDataSequence
        :raises IndexError: If the index is out of range.
        """
        if isinstance(index, slice):
            return CoreDataSequence(self._data[index])
        return self._data[index]

    def __setitem__(self, index: int, value: CoreDataTypes) -> None:
        """Raise an error since CoreDataSequence is immutable.

        :param index: The index to set.
        :type index: int
        :param value: The value to set.
        :type value: :class:`CoreDataTypes`
        :raises SimpleBenchTypeError: Always, since CoreDataSequence is immutable.
        """
        raise SimpleBenchTypeError(
            "CoreDataSequence is immutable and does not support item assignment.",
            tag=_CoreDataErrorTag.CORE_DATA_SEQUENCE_INVALID_ITEM_TYPE)

    def __contains__(self, item: object) -> bool:
        """Check if the item is in the CoreDataSequence.

        :param item: The item to check for membership.
        :type item: object
        :returns: :obj:`True` if the item is in the set, :obj:`False` otherwise.
        :rtype: bool
        """
        return item in self._data

    def __iter__(self) -> Iterator[CoreDataTypes]:
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
        return self._data == other._data

    def __hash__(self) -> int:
        """Return the hash of the CoreDataSequence.

        :returns: The hash of the sequence.
        :rtype: int
        """
        return hash(self._data)

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
