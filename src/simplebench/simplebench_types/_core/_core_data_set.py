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
import hashlib
from collections.abc import Hashable, Iterator, Mapping, Sequence, Set
from typing import TYPE_CHECKING

from typechecked import Immutable

from simplebench.exceptions import SimpleBenchAssertionError, SimpleBenchTypeError

from .._element_collection import ElementCollection, is_element_collection
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


        self._data: frozenset[ImmutableCoreDataTypes]

        if __elements is None:
            self._data = frozenset()
            return

        if not is_element_collection(__elements):
            raise SimpleBenchTypeError(
                'CoreDataSet must be initialized with an ElementCollection of CoreData.',
                tag=_CoreDataErrorTag.CORE_DATA_SET_NOT_ELEMENT_COLLECTION)
        data: set[CoreDataTypes] = set()

        if all(isinstance(item, CORE_DATA_PRIMITIVE_TYPES_TUPLE) for item in __elements):
            self._data = frozenset(__elements)
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
        self._hash_cache: int | None = None
        self._content_hash_cache: str | None = None

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

    def _rich_compare_value(self, value: 'ImmutableCoreDataTypes') -> str:
        """Returns a string representation for rich comparison purposes.

        We don't actually care about the comparision value, just that
        it is consistent and largely guaranteed to be unique for
        each item value.

        Since in a set the order is not guaranteed, we generate a reproducible
        and consistent value by their string representation or content
        hash if they are immutable core data types. This ensures that
        two sets with the same content will have the same
        representation for comparison.

        Since it is only used in generating a cached content hash, this is
        efficient enough for our purposes.

        .. note:: This is a helper method for internal use only. It
              should not be used outside of this class. It's also
              vulnerable to infinite recursion if used on recursive
              data structure since it would never find a base case to stop.

              However, since CoreDataSet is immutable and cannot contain
              recursive references, this should not be an issue in practice.

        :returns: A sorted list of the set items.
        :rtype: list[CoreDataTypes]
        """
        from ._types import CORE_DATA_PRIMITIVE_TYPES_TUPLE

        if value is None:
            return ''
        if isinstance(value, CORE_DATA_PRIMITIVE_TYPES_TUPLE):
            return repr(value)
        if isinstance(value, CoreDataSet):
            return value.content_hash()

        raise SimpleBenchAssertionError(
            f'Unsupported CoreData type for rich comparison: {type(value)!r}',
            tag=_CoreDataErrorTag.CORE_DATA_COMPARISON_UNSUPPORTED_TYPE)

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
            values = sorted(self._data, key=self._rich_compare_value)
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

