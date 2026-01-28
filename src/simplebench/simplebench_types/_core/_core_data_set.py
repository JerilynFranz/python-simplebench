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
        - complex
        - NoneType
    - Sequences of the above types
    - Mappings of str to the above types
    - Sets of the above types
"""
from collections.abc import Hashable, Iterator, Mapping, Sequence, Set

from typechecked import Immutable

from simplebench.exceptions import SimpleBenchTypeError

from .._element_collection import ElementCollection, is_element_collection
from ._error_tags import _CoreDataErrorTag
from ._types import CORE_DATA_PRIMITIVE_TYPES_TUPLE, IMMUTABLE_CORE_DATA_TYPES_TUPLE, CoreDataTypes


class CoreDataSet(Set[CoreDataTypes], ElementCollection, Immutable, Hashable):
    """Deep-immutable Set container for CoreData types used in SimpleBench.

    This represents a set where all elements are of type :class:`CoreData`.

    When initializing, the provided iterable must be an :class:`ElementCollection`
    containing only elements of type :class:`CoreDataTypes`.

    The set itself is immutable once created with all contents being of valid CoreData types
    and converted to their respective immutable CoreData wrappers as needed.

    :param __iterable: An iterable of CoreData elements to initialize the set or :obj:`None`.
    :type __iterable: Iterable[CoreData] | None
    """

    def __init__(self, __iterable: ElementCollection | None = None) -> None:
        """Initialize the CoreDataSet.

        If an iterable is provided, it must be an :class:`ElementCollection`
        containing only elements of type :class:`CoreData`.

        If no iterable is provided, an empty set is created.

        :param __iterable: An iterable of CoreData elements to initialize the set or :obj:`None`.
        :type __iterable: Iterable[CoreData] | None
        """
        # Import here to avoid circular imports
        from ._core_data_mapping import CoreDataMapping
        from ._core_data_sequence import CoreDataSequence

        self._data: frozenset[CoreDataTypes]

        if __iterable is None:
            self._data = frozenset()
            return

        if not is_element_collection(__iterable):
            raise SimpleBenchTypeError(
                'CoreDataSet must be initialized with an ElementCollection of CoreData.',
                tag=_CoreDataErrorTag.CORE_DATA_SET_NOT_ELEMENT_COLLECTION)
        data: Set[CoreDataTypes] = set()

        if all(isinstance(item, CORE_DATA_PRIMITIVE_TYPES_TUPLE) for item in __iterable):
            self._data = frozenset(__iterable)
            return

        for item in __iterable:
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

            else: # Never
                 raise SimpleBenchTypeError(
                    f'Invalid item type passed to CoreDataSet: {item!r}. '
                    f'Must be a CoreData type: {IMMUTABLE_CORE_DATA_TYPES_TUPLE!r}.',
                    tag=_CoreDataErrorTag.CORE_DATA_SET_INVALID_ITEM_TYPE)

        self._data = frozenset(data)

    def __contains__(self, item: object) -> bool:
        """Check if the item is in the CoreDataSet.

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

    def __hash__(self) -> int:
        """Return the hash of the CoreDataSet.

        :returns: The hash of the set.
        :rtype: int
        """
        return hash(self._data)

    def thaw(self) -> set[CoreDataTypes]:
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
