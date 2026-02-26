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

It does not support sorting or mutation after creation.
"""
import hashlib
from collections.abc import Hashable, Iterator, Mapping, Sequence, Set
from types import NoneType
from typing import TYPE_CHECKING, Any, Generic, TypeVar, overload

import simplejson
from typeguard import TypeCheckError, check_type

from simplebench._log import _log
from simplebench.exceptions import SimpleBenchTypeError
from simplebench.protocols import Thawable

from .._element_collection import ElementCollection, is_element_collection
from . import _common
from ._error_tags import _CoreDataErrorTag

if TYPE_CHECKING:
    from ._types import CoreDataTypes, ImmutableCoreDataTypes

# TypeVar restricted to ImmutableCoreDataTypes for static type checking
T = TypeVar('T', bound='CoreDataTypes')

class CoreDataSequence(Sequence[T],
                       ElementCollection[T],
                       Hashable,
                       Thawable,
                       Generic[T]):
    """Deep-immutable Sequence container for CoreData types used in SimpleBench.

    This represents a sequence where all elements are of type :class:`CoreData`.

    When initializing, the provided collection must be an :class:`ElementCollection`
    containing only elements of type :class:`CoreDataTypes`.

    The sequence itself is immutable once created with all contents being of valid CoreData types
    and converted to their respective immutable CoreData wrappers as needed.

    :param __elements: A collection of CoreDataTypes elements to initialize the sequence or :obj:`None`.
    :type __elements: Iterable[CoreDataTypes] | None
    """
    _generic_type: type | None = None
    """Marker for generic type parameter for runtime checking purposes.

    This is used by subclasses to specify a particular type constraint for the elements of the sequence,
    such as in the case of the :class:`Values` subclass which sets this to `float` to indicate that all elements
    must be floats. The CoreDataSequence base class itself enforces the generic type constraint if this attribute
    is set, allowing for flexible yet type-safe subclasses that can represent specific kinds of sequences with
    additional validation on their contents.
    """

    __immutable__: bool = True  # Marker for Immutable protocol
    __slots__ = ('_version', '_data', '_hash_cache', '_hash_id_cache', '__weakref__')

    def __init__(self, __elements: 'ElementCollection[T] | None' = None) -> None:
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
        self._hash_id_cache: str | None = None

        self._data: tuple[T, ...]
        if __elements is None:
            self._data = ()
            return

        if not is_element_collection(__elements):
            raise SimpleBenchTypeError(
                'CoreDataSequence must be initialized with an ElementCollection of CoreData.',
                tag=_CoreDataErrorTag.CORE_DATA_SEQUENCE_NOT_ELEMENT_COLLECTION)

        data: list[T] = []
        # The following import is kept for runtime type checks

        if all(isinstance(item, CORE_DATA_PRIMITIVE_TYPES_TUPLE) for item in __elements):
            self._data = tuple(__elements)
            return

        cls = self.__class__
        generic_type: type | None = getattr(cls, '_generic_type', None)
        for item in __elements:
            if generic_type is not None:
                try:
                    check_type(item, generic_type)
                except TypeCheckError as exc:
                    raise SimpleBenchTypeError(
                        f'Item {item!r} is not of the expected generic type {generic_type}.',
                        tag=_CoreDataErrorTag.CORE_DATA_SEQUENCE_INVALID_ITEM_TYPE) from exc
            if isinstance(item, (str, int, float, bool, NoneType)):
                data.append(item)  # type: ignore
            elif isinstance(item, (CoreDataMapping, CoreDataSequence, CoreDataSet)):
                data.append(item)  # type: ignore
            elif isinstance(item, Mapping):
                data.append(CoreDataMapping(item))  # type: ignore
            elif isinstance(item, Sequence) and not isinstance(item, (str, bytes)):
                data.append(CoreDataSequence(item))  # type: ignore
            elif isinstance(item, Set):
                data.append(CoreDataSet(item))  # type: ignore
            else:
                 raise SimpleBenchTypeError(
                    f'Invalid item type passed to CoreDataSequence: {item!r}. '
                    f'Must be a CoreData type: {CORE_DATA_TYPES_TUPLE!r}.',
                    tag=_CoreDataErrorTag.CORE_DATA_SEQUENCE_INVALID_ITEM_TYPE)

        self._data = tuple(data)


    @overload
    def __getitem__(self, index: int) -> T: ...

    @overload
    def __getitem__(self, index: slice) -> 'CoreDataSequence[T]': ...

    def __getitem__(self, index: int | slice) -> T | 'CoreDataSequence[T]':
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
        try:
            if isinstance(index, slice):
                return self.__class__(self._data[index])
            return self._data[index]
        except IndexError as e:
            raise IndexError(
                f'Index {index!r} out of range for CoreDataSequence of length {len(self._data)}.'
            ) from e
        except TypeError as e:
            raise SimpleBenchTypeError(
                f'Invalid index type for CoreDataSequence: {index!r}. Must be int or slice.',
                tag=_CoreDataErrorTag.CORE_DATA_SEQUENCE_INVALID_INDEX_TYPE) from e

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

    def __iter__(self) -> Iterator[T]:
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
        return self.hash_id() == other.hash_id()

    def hash_id(self) -> str:
        """Return a SHA256 hash of the CoreDataSequence content.

        :returns: The SHA256 hash of the sequence content as a hexadecimal string.
        :rtype: str
        """
        from ._core_data_mapping import CoreDataMapping
        from ._core_data_set import CoreDataSet
        if self._hash_id_cache is None:
            hasher = hashlib.sha256()
            for item in self._data:
                if isinstance(item, (CoreDataSequence, CoreDataMapping, CoreDataSet)):
                    hasher.update(item.hash_id().encode('utf-8'))
                else:
                    hasher.update(repr(item).encode('utf-8'))
            self._hash_id_cache = hasher.hexdigest()
        return self._hash_id_cache

    def __hash__(self) -> int:
        """Return the hash of the CoreDataSequence.

        :returns: The hash of the sequence.
        :rtype: int
        """
        if self._hash_cache is None:
            self._hash_cache = hash(self.hash_id())
        return self._hash_cache

    def thaw(self, preserve_immutability: bool = False) -> list['CoreDataTypes'] | tuple['CoreDataTypes', ...]:
        """Convert the CoreDataSequence to a standard mutable list.

        :param preserve_immutability: If :obj:`True`, nested :class:`CoreDataMapping`
            instances are preserved as-is instead of being thawed
            to mutable :class:`dict` and nested :class:`CoreDataSequence` instances
            are thawed to tuples instead of lists.

            Defaults to :obj:`False`. This is useful
            when the caller wants to maintain the immutability of nested types
            and mainly used for internal purposes when thawing CoreDataSet instances.

        :type preserve_immutability: bool

        :returns: A mutable list representation of the CoreDataSequence.
        :rtype: list[CoreDataTypes]
        """
        from ._core_data_mapping import CoreDataMapping
        from ._core_data_set import CoreDataSet

        thawed_list: list[CoreDataTypes] = []
        for value in self._data:
            if isinstance(value, (CoreDataSet, CoreDataMapping, CoreDataSequence)):
                thawed_list.append(value.thaw(preserve_immutability=preserve_immutability))
            else:
                thawed_list.append(value) # type: ignore[list-item]
        if preserve_immutability:
            return tuple(thawed_list)
        return thawed_list

    def for_json(self) -> list['CoreDataTypes']:
        """Convert the CoreDataSequence to a JSON-serializable list.

        JSON-serialization inherently loses some type information since JSON
        does not have a set type, so this method is intended for serialization
        purposes only and not for general data manipulation.

        This differs from `thaw` in that `thaw` returns mutable types where possible
        and so cannot unwrap nested CoreData* types within sets, while `for_json`
        focuses solely on preparing the data for JSON serialization and
        so converts nested CoreData* types appropriately to JSON-serializable forms
        regardless of Python semantics like sets vs lists or mutability constraints.

        :returns: A JSON-serializable list representation of the CoreDataSequence.
        :rtype: list[CoreDataTypes]
        """
        from ._core_data_mapping import CoreDataMapping
        from ._core_data_set import CoreDataSet

        json_list: list[CoreDataTypes] = []
        for value in self._data:
            if isinstance(value, (CoreDataMapping, CoreDataSequence, CoreDataSet)):
                json_list.append(value.for_json())
            elif isinstance(value, bytes):  # bytes are converted to data URLs for JSON compatibility
                json_list.append(_common.data_url(value))
            else:
                json_list.append(value)  # type: ignore[list-item]
        return list(json_list)

    def as_json(self) -> str:
        """Serialize the CoreDataSequence to a JSON string.

        :returns: A JSON string representation of the CoreDataSequence.
        :rtype: str
        """
        return simplejson.dumps(
            self.for_json(), sort_keys=True, for_json=True, iterable_as_array=True)

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

        if not (isinstance(value,
                    (str, int, float, bool, NoneType, CoreDataSequence, CoreDataMapping, CoreDataSet))):
              raise SimpleBenchTypeError(
            f'Invalid value type passed to CoreDataSequence.count(): {value!r}. '
            f'Must be a CoreData type: {CORE_DATA_PRIMITIVE_TYPES_TUPLE!r} '
            f'or CoreDataSequence, CoreDataMapping, CoreDataSet.',
            tag=_CoreDataErrorTag.CORE_DATA_SEQUENCE_INVALID_ITEM_TYPE)
        comparison_value = _common.rich_compare_value(value)
        count = 0
        for item in self._data:
            if _common.rich_compare_value(item) == comparison_value:  # type: ignore
                count += 1
        return count

    def as_tuple(self) -> tuple[T, ...]:
        """Return the contents of the CoreDataSequence as a tuple.

        :returns: The contents of the sequence as a tuple.
        :rtype: tuple[ImmutableCoreDataTypes, ...]
        """
        return self._data

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
