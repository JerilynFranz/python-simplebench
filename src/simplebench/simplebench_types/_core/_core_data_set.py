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
from collections.abc import Hashable, Iterable, Iterator, Mapping, Sequence, Set
from types import NoneType
from typing import TYPE_CHECKING, Any, Generic, TypeVar

import simplejson
from typeguard import TypeCheckError, check_type

from simplebench.exceptions import SimpleBenchTypeError
from simplebench.protocols import Thawable

from .._element_collection import ElementCollection
from . import _common
from ._error_tags import _CoreDataErrorTag

if TYPE_CHECKING:
    from ._types import CoreDataMapping, CoreDataTypes, ImmutableCoreDataTypes

T = TypeVar('T', bound='ImmutableCoreDataTypes')
_T = TypeVar('_T')  # <-- Add this line for the default value in get()

class CoreDataSet(Set[T],
                  ElementCollection[T],
                  Hashable,
                  Thawable,
                  Generic[T]):
    """Deep-immutable Set container for CoreData types used in SimpleBench.

    This represents a set where all elements are of type :class:`CoreData`.

    When initializing, the provided iterable must be an :class:`ElementCollection`
    containing only elements of type :class:`CoreDataTypes`.

    The set itself is immutable once created with all contents being of valid CoreData types
    and converted to their respective immutable CoreData wrappers as needed.

    :param __elements: An iterable of CoreData elements to initialize the set or :obj:`None`.
    :type __elements: ElementCollection[CoreDataTypes] | None
    """
    _generic_type: type | None = None
    """Generic type for the elements in the set, if specified. This is used for type validation when a generic type is
    defined for the set."""
    __immutable__: bool = True  # Marker for Immutable protocol
    __slots__ = ('_version', '_data', '_hash_cache', '_hash_id_cache', '__weakref__')

    def __init__(
            self,
            __elements: 'Iterable[T] | None' = None) -> None:
        """Initialize the CoreDataSet.

        The provided iterable must be a Set or Sequence that contains only elements of type :class:`CoreDataTypes`.

        It accepts str and bytes as a sequence of characters or bytes for
        compatibility with ordinary sets.

        However, each character or byte will be treated as an individual string
        or bytes element. This means that initializing with a string like "abc"
        will result in a set containing 'a', 'b', and 'c' as separate elements
        NOT 'abc'.

        .. code-block:: python
            :caption: Examples of string and bytes initialization

            a = CoreDataSet("abc")
            assert a == CoreDataSet({'a', 'b', 'c'})
            b = CoreDataSet(b"abc")
            assert b == CoreDataSet({b'a', b'b', b'c'})
            c = CoreDataSet(["abc"])
            assert c == CoreDataSet({'abc'})
            d = CoreDataSet([b"abc"])
            assert d == CoreDataSet({b'abc'})

        .. note:: CoreDataSet can process mappings and sequences by converting them
                  into :class:`CoreDataMapping` and :class:`CoreDataSequence` respectively.

                  This means you can directly pass in nested structures of mutable
                  mappings and sequences, and they will be safely wrapped.

                  This is not perfectly symmetric with thawing since thawing
                  a CoreDataSet will always yield a Python :class:`set` which cannot
                  contain unhashable types such as dicts. When thawed, nested
                  mappings will remain as :class:`CoreDataMapping` instances.

                  This design choice allows for more convenient construction of
                  CoreDataSet instances from common Python data structures.

        If no iterable is provided, an empty set is created.

        :param __elements: An iterable of CoreData elements to initialize the set or :obj:`None`.
        :type __elements: ElementCollection[CoreDataTypes] | None
        """
        from ._core_data_mapping import CoreDataMapping
        from ._core_data_sequence import CoreDataSequence
        from ._types import CORE_DATA_PRIMITIVE_TYPES_TUPLE, CORE_DATA_TYPES_TUPLE

        self._version: int = 1
        self._hash_cache: int | None = None
        self._hash_id_cache: str | None = None
        self._data: set[T]

        if __elements is None:
            self._data = set()
            return

        if not isinstance(__elements, (Set, Sequence)):
            raise SimpleBenchTypeError(
                f'CoreDataSet requires a Set or Sequence to initialize, '
                f'got {type(__elements)!r}.',
                tag=_CoreDataErrorTag.CORE_DATA_SET_NOT_ELEMENT_COLLECTION)

        data: set[T] = set()

        if all(isinstance(item, CORE_DATA_PRIMITIVE_TYPES_TUPLE) for item in __elements):
            self._data = set(__elements)  # type: ignore[arg-type]  # all primitive types are immutable
            return

        cls = self.__class__
        for item in __elements:
            if cls._generic_type is not None:
                try:
                    check_type(item, cls._generic_type)
                except TypeCheckError as exc:
                    raise SimpleBenchTypeError(
                        f'Item {item!r} does not match the expected generic type '
                        f'{cls._generic_type!r} for this CoreDataSet.',
                        tag=_CoreDataErrorTag.CORE_DATA_SET_GENERIC_TYPE_MISMATCH) from exc
            if isinstance(item, (str, int, float, bool, NoneType)):
                data.add(item)  # type: ignore
            elif isinstance(item, (CoreDataMapping, CoreDataSequence, CoreDataSet)):
                data.add(item)  # type: ignore
            elif isinstance(item, Mapping):
                data.add(CoreDataMapping(item))  # type: ignore
            elif isinstance(item, Set):
                data.add(CoreDataSet(item))  # type: ignore
            elif isinstance(item, Sequence) and not isinstance(item, (str, bytes)):
                data.add(CoreDataSequence(item))  # type: ignore
            else: # Invalid type of data passed
                 raise SimpleBenchTypeError(
                    f'Invalid item type passed to CoreDataSet: {item!r}. '
                    f'Must be a CoreData type: {CORE_DATA_TYPES_TUPLE!r}.',
                    tag=_CoreDataErrorTag.CORE_DATA_SET_INVALID_ITEM_TYPE)

        # We've already validated all items are ImmutableCoreDataTypes
        self._data = set(data)  # type: ignore[arg-type]

    def __contains__(self, item: object) -> bool:
        """Check if the item is in the CoreDataSet.

        :param item: The item to check for membership.
        :type item: object
        :returns: :obj:`True` if the item is in the set, :obj:`False` otherwise.
        :rtype: bool
        """
        return item in self._data

    def __iter__(self) -> Iterator['ImmutableCoreDataTypes']:  # type: ignore[override]
        """Return an iterator over the CoreDataSet.

        :returns: An iterator over the elements in the set.
        :rtype: Iterator[CoreDataTypes]
        """
        return iter(self._data)  # type: ignore[return-value]

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
        return self.hash_id() == other.hash_id()

    def hash_id(self) -> str:
        """Return a SHA256 hash of the CoreDataSet content.

        :returns: The SHA256 hash of the set content as a hexadecimal string.
        :rtype: str
        """
        from ._core_data_mapping import CoreDataMapping
        from ._core_data_sequence import CoreDataSequence
        if self._hash_id_cache is None:
            hasher = hashlib.sha256()
            # We don't care what the order is, just that it is consistent
            values = sorted(self._data, key=_common.rich_compare_value)  # type: ignore
            for item in values:
                if isinstance(item, (CoreDataSequence, CoreDataMapping, CoreDataSet)):
                    hasher.update(item.hash_id().encode('utf-8'))
                else:
                    hasher.update(repr(item).encode('utf-8'))
            self._hash_id_cache = hasher.hexdigest()
        return self._hash_id_cache

    def __hash__(self) -> int:
        """Return the hash of the CoreDataSet.

        :returns: The hash of the set.
        :rtype: int
        """
        if self._hash_cache is None:
            self._hash_cache = hash(self.hash_id())
        return self._hash_cache

    def thaw(self,
             preserve_immutability: bool = False
             ) -> 'set[str | int | float | bool | frozenset | tuple | None | CoreDataMapping]':
        """Convert the CoreDataSet to a mutable set of immutable :data:`CoreDataTypes`.

        This method returns a mutable :class:`set` containing
        the closest available immutable representations of the CoreDataTypes.

        We can't recursively thaw to mutable types because set requires its
        elements to be hashable, and mutable types are not (or should not be) hashable.

        As there is no immutable built-in Mapping type in Python, nested
        :class:`CoreDataMapping` instances remain as :class:`CoreDataMapping` instances.

        - For primitive types, they are returned as-is since they are already immutable.
        - For nested :class:`CoreDataSet`, they are converted to :class:`frozenset`.
        - For nested :class:`CoreDataMapping` they remain as :class:`CoreDataMapping`.
        - For nested :class:`CoreDataSequence` they are converted to :class:`tuple`.

        There is a problem with thawing nested mappings since Python sets cannot
        contain unhashable types like dicts. Therefore, nested mappings remain
        as :class:`CoreDataMapping` instances to preserve hashability.

        :param preserve_immutability: This parameter is currently unused in this method
                                      since nested CoreDataMapping instances must remain
                                      as-is to maintain hashability in the resulting set.
                                      It is included for API consistency with other thaw methods.
        :type preserve_immutability: bool
        :returns: A mutable set representation of the CoreDataSet.
        :rtype: set[CoreDataTypes]
        """
        from ._core_data_mapping import CoreDataMapping
        from ._core_data_sequence import CoreDataSequence

        thaw_set: set[str | int | float | bool | frozenset | tuple | None | CoreDataMapping] = set()
        for value in self._data:
            if isinstance(value, CoreDataSet):
                thaw_set.add(frozenset(value.thaw(preserve_immutability=True)))
            elif isinstance(value, CoreDataSequence):
                thaw_set.add(tuple(value.thaw(preserve_immutability=True)))
            elif isinstance(value, CoreDataMapping):
                thaw_set.add(value)  # must remain as CoreDataMapping for hashability
            else:
                thaw_set.add(value) # type: ignore  # primitive types are returned as-is
        return set(thaw_set)

    def for_json(self) -> list['CoreDataTypes']:
        """Convert the CoreDataSet to a JSON-serializable list.

        JSON-serialization inherently loses some type information since JSON
        does not have a set type, so this method is intended for serialization
        purposes only and not for general data manipulation.

        This differs from :meth:`thaw` in that :meth:`thaw` returns mutable types where possible
        and so cannot unwrap nested `CoreData*` types within sets, while :meth:`for_json`
        focuses solely on preparing the data for JSON serialization and
        so converts nested `CoreData*` types appropriately to JSON-serializable forms
        regardless of Python semantics like sets vs lists or mutability constraints.

        :returns: A JSON-serializable list representation of the CoreDataSet.
        :rtype: list[CoreDataTypes]
        """
        from ._core_data_mapping import CoreDataMapping
        from ._core_data_sequence import CoreDataSequence

        json_list: list[CoreDataTypes] = []
        for value in self._data:
            if isinstance(value, (CoreDataMapping, CoreDataSequence, CoreDataSet)):
                json_list.append(value.for_json())
            elif isinstance(value, bytes):  # bytes are converted to data URLs for JSON compatibility
                json_list.append(_common.data_url(value))
            else:
                json_list.append(value)  # type: ignore  # primitive types are JSON-serializable as-is
        return list(json_list)

    def as_json(self) -> str:
        """Serialize the CoreDataSet to a JSON string.

        :returns: A JSON string representation of the CoreDataSet.
        :rtype: str
        """
        return simplejson.dumps(
            self.for_json(), sort_keys=True, for_json=True, iterable_as_array=True)

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

    def __copy__(self) -> 'CoreDataSet':
        """Return the same CoreDataSet.

        Since the CoreDataSet instance is immutable and composed of
        immutable components, there is no need to perform a shallow copy
        of its contents. Instead, we simply return the instance itself
        which is a extremely fast O(1) operation.

        If a true shallow copy is required for some reason, the caller
        can manually create a new instance by passing the thawed contents
        to the constructor.

        :return CoreDataSet: The same CoreDataSet instance.
        """
        # because the CoreDataSet is immutable, we return self
        # instead of performing an actual copy.
        return self
