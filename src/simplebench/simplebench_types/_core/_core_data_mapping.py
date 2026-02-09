"""Core data mapping type for SimpleBench

This is an immutable mapping of core data types used in SimpleBench.

It general it is interchangeable with standard Python mappings (dicts)
but enforces deep immutability and type constraints on the contents,
allowing only valid CoreData types and keys being non-empty, non-blank strings
that are valid Python identifiers.

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

When constructed from standard Python data structures, all contents are
converted to their respective immutable CoreData wrappers as needed and
the resulting structure is deeply immutable and acyclic.

While not actually a subclass of dict, it fully implements the Mapping interface
and can be used in most places where a read-only dict-like object is expected
without modification capabilities.

It is possible via the :meth:`replace` method to create cyclical references,
so care should be taken to avoid such scenarios as they may lead to unexpected
behavior and potentially non-serializability or infinite recursion during
operations like hashing, comparison, or serialization.
"""
import hashlib
from collections.abc import Hashable, ItemsView, Iterator, KeysView, Mapping, Sequence, Set, ValuesView
from typing import TYPE_CHECKING, Any, Generic, TypeVar

import simplejson
from typeguard import TypeCheckError, check_type

from simplebench.exceptions import SimpleBenchKeyError, SimpleBenchTypeError

from . import _common
from ._error_tags import _CoreDataErrorTag

if TYPE_CHECKING:
    from ._types import CoreDataTypes, ImmutableCoreDataTypes

T = TypeVar('T', bound='CoreDataTypes')
_T = TypeVar('_T')  # <-- Add this line for the default value in get()

class CoreDataMapping(Mapping[str, T], Hashable, Generic[T]):
    """Deep-immutable Mapping container for CoreData types used in SimpleBench.

    This represents a mapping where all keys are strings and all values are of
    type :class:`ImmutableCoreDataTypes`.

    When initializing, the provided iterable must be a Mapping
    containing only string keys and values of type :class:`CoreDataTypes`.

    The mapping itself is immutable once created with all contents being of valid CoreData types
    and converted to their respective immutable CoreData wrappers as needed.

    The keys must be non-empty, non-blank strings and valid Python identifiers.

    :param __mapping: A Mapping of str to CoreDataTypes elements to initialize the mapping or :obj:`None`.
    :type __mapping: Mapping[str, CoreDataTypes] | None
    """
    _generic_type: type | None = None
    """Marker for generic type parameter for runtime checking purposes by CoreDataMapping."""

    __immutable__: bool = True  # Marker for Immutable protocol
    __slots__ = ('_version', '_data', '_hash_cache', '_content_hash_cache')

    def __init__(self, __mapping: Mapping[str, 'CoreDataTypes'] | None = None) -> None:
        """Initialize the CoreDataMapping.

        If a mapping is provided, it must be a Mapping of str to
        type :class:`CoreDataTypes`.

        If no mapping is provided, an empty mapping is created.

        :param __mapping: A mapping of str to CoreDataTypes elements to initialize the mapping or :obj:`None`.
        :type __mapping: Mapping[str, CoreDataTypes] | None
        """
        # Import here to avoid circular imports
        from ._core_data_sequence import CoreDataSequence
        from ._core_data_set import CoreDataSet
        from ._types import CORE_DATA_PRIMITIVE_TYPES_TUPLE, CORE_DATA_TYPES_TUPLE

        self._version: int = 1
        self._hash_cache: int | None = None
        self._content_hash_cache: str | None = None

        self._data: dict[str, T]
        if __mapping is None:
            self._data = {}
            return

        if not isinstance(__mapping, Mapping):
            raise SimpleBenchTypeError(
                'CoreDataMapping must be initialized with a Mapping of str to CoreData.',
                tag=_CoreDataErrorTag.CORE_DATA_MAPPING_INVALID_ARG_TYPE)

        if not all(isinstance(key, str) for key in __mapping.keys()):
            raise SimpleBenchTypeError(
                'All keys in CoreDataMapping must be of type str and valid identifiers.',
                tag=_CoreDataErrorTag.CORE_DATA_MAPPING_INVALID_KEY_TYPE)

        if not all(key.isidentifier() for key in __mapping.keys()):
            raise SimpleBenchTypeError(
                'All keys in CoreDataMapping must be non-empty, non-blank strings and valid identifiers.',
                tag=_CoreDataErrorTag.CORE_DATA_MAPPING_INVALID_KEY_VALUE)

        data: dict[str, T] = {}

        if all(isinstance(value, CORE_DATA_PRIMITIVE_TYPES_TUPLE) for value in __mapping.values()):
            self._data = dict(__mapping)  # type: ignore  # all values are immutable primitives
            return

        cls = self.__class__
        for key, value in __mapping.items():
            if cls._generic_type is not None:
                try:
                    check_type(value, cls._generic_type)
                except TypeCheckError as exc:
                    raise SimpleBenchTypeError(
                        f'Value for key {key!r} does not match the expected type '
                        f'{cls._generic_type!r} for this CoreDataMapping.',
                        tag=_CoreDataErrorTag.CORE_DATA_MAPPING_GENERIC_TYPE_MISMATCH) from exc
            if isinstance(value, CORE_DATA_PRIMITIVE_TYPES_TUPLE):
                data[key] = value  # type: ignore  # value is an immutable primitive
            elif isinstance(value, (CoreDataMapping, CoreDataSequence, CoreDataSet)):
                data[key] = value  # type: ignore  # value is already a CoreData type, so we can use it directly without conversion
            elif isinstance(value, Mapping):
                data[key] = CoreDataMapping(value)  # type: ignore
            elif isinstance(value, Sequence) and not isinstance(value, (str, bytes)):
                data[key] = CoreDataSequence(value)  # type: ignore
            elif isinstance(value, Set):
                data[key] = CoreDataSet(value)  # type: ignore
            else:
                raise SimpleBenchTypeError(
                    f'Invalid value type passed to CoreDataMapping for key {key!r}: {value!r}. '
                    f'Must be a CoreData type: {CORE_DATA_TYPES_TUPLE!r}.',
                    tag=_CoreDataErrorTag.CORE_DATA_MAPPING_INVALID_VALUE_TYPE)

        self._data = data

    # override is necessary to for type checker to accept the default parameter
    # in the same way as dict.get() (no restrictions on the return type)
    def get(self, key: str, default: _T = None) -> 'CoreDataTypes | _T':  # type: ignore[override,assignment]
        """Get the value for the given key, or default if not found.

        :param key: The key.
        :type key: str
        :param default: The default value to return if the key is not found.
        :type default: Any
        :returns: The corresponding CoreDataTypes value or the default.
        :rtype: CoreDataTypes | Any
        :raises KeyError: If the key is not found and no default is provided.
        """
        try:
            return self._data.get(key, default)  # type: ignore[return-value]
        except KeyError as exc:
            raise SimpleBenchKeyError(
                f'Key {key!r} not found in CoreDataMapping.',
                tag=_CoreDataErrorTag.CORE_DATA_MAPPING_KEY_ERROR) from exc

    def keys(self) -> KeysView[str]:
        """Return an iterator over the keys in the CoreDataMapping.

        :returns: An iterator over the keys.
        :rtype: KeysView[str]
        """
        return self._data.keys()

    def values(self) -> ValuesView['ImmutableCoreDataTypes']:  # type: ignore[return-value,override]
        """Return an iterator over the values in the CoreDataMapping.

        :returns: An iterator over the values.
        :rtype: ValuesView['ImmutableCoreDataTypes']
        """
        return self._data.values()  # type: ignore[return-value]

    def items(self) -> ItemsView[str, 'ImmutableCoreDataTypes']:  # type: ignore[return-value,override]
        """Return an iterator over the items in the CoreDataMapping.

        :returns: An iterator over the items.
        :rtype: ItemsView[str, 'ImmutableCoreDataTypes']
        """
        return self._data.items()  # type: ignore[return-value]

    def copy(self) -> 'CoreDataMapping':
        """Because CoreDataMapping is immutable, returns self.

        This method is provided for API compatibility but does
        not create a new instance of CoreDataMapping.

        There is no performance or memory overhead since the instance
        is immutable.

        :returns: The same CoreDataMapping instance.
        :rtype: CoreDataMapping
        """
        return self

    def __getitem__(self, key: str) -> 'ImmutableCoreDataTypes':  # type: ignore[override]
        """Get the value for the given key.

        :param key: The key.
        :type key: str
        :returns: The corresponding ImmutableCoreDataTypes value.
        :rtype: ImmutableCoreDataTypes
        :raises SimpleBenchKeyError: If the key is not found.
        """
        try:
            return self._data[key]  # type: ignore[return-value]
        except KeyError as exc:
            raise SimpleBenchKeyError(
                f'Key {key!r} not found in CoreDataMapping.',
                tag=_CoreDataErrorTag.CORE_DATA_MAPPING_KEY_ERROR) from exc

    def __setitem__(self, key: str, value: 'ImmutableCoreDataTypes') -> None:
        """Raise an error since CoreDataMapping is immutable.

        :param key: The key to set.
        :type key: str
        :param value: The value to set.
        :type value: ImmutableCoreDataTypes
        :raises SimpleBenchTypeError: Always, since CoreDataMapping is immutable.
        """
        raise SimpleBenchTypeError(
            'CoreDataMapping is immutable and does not support item assignment.',
            tag=_CoreDataErrorTag.CORE_DATA_MAPPING_IMMUTABLE)

    def __contains__(self, key: object) -> bool:
        """Check if the CoreDataMapping contains the given key.

        :param key: The key to check.
        :type key: object
        :returns: True if the key is in the CoreDataMapping, False otherwise.
        :rtype: bool
        """
        return key in self._data

    def __iter__(self) -> Iterator[str]:
        """Return an iterator over the CoreDataMapping.

        :returns: An iterator over the keys in the mapping.
        :rtype: Iterator[str]
        """
        return iter(self._data)

    def __len__(self) -> int:
        """Return the number of elements in the CoreDataMapping.

        :returns: The number of elements in the mapping.
        :rtype: int
        """
        return len(self._data)

    def __repr__(self) -> str:
        """Return the string representation of the CoreDataMapping.

        :returns: The string representation of the mapping.
        :rtype: str
        """
        return f'CoreDataMapping({self._data!r})'

    def __eq__(self, other: object) -> bool:
        """Check equality with another CoreDataMapping.

        :param other: The other object to compare.
        :type other: object
        :returns: :obj:`True` if the mappings are equal, :obj:`False` otherwise.
        :rtype: bool
        """
        if not isinstance(other, CoreDataMapping):
            return False
        return self._data == other._data

    def content_hash(self) -> str:
        """Return a SHA256 hash of the CoreDataMapping content.

        :returns: The SHA256 hash of the sequence content as a hexadecimal string.
        :rtype: str
        """
        from ._core_data_sequence import CoreDataSequence
        from ._core_data_set import CoreDataSet
        if self._content_hash_cache is None:
            hasher = hashlib.sha256()
            for key in sorted(self._data.keys()):
                hasher.update(key.encode('utf-8'))
                value = self._data[key]
                if isinstance(value, (CoreDataMapping, CoreDataSequence, CoreDataSet)):
                    hasher.update(value.content_hash().encode('utf-8'))
                else:
                    hasher.update(repr(value).encode('utf-8'))
            self._content_hash_cache = hasher.hexdigest()
        return self._content_hash_cache

    def __hash__(self) -> int:
        """Return the hash of the CoreDataMapping.

        :returns: The hash of the mapping.
        :rtype: int
        """
        if self._hash_cache is None:
            self._hash_cache = hash(self.content_hash())
        return self._hash_cache

    def replace(self, **changes: 'CoreDataTypes') -> 'CoreDataMapping':
        """Return a new CoreDataMapping with specified changes applied.

        This method creates and returns a new CoreDataMapping instance by applying
        the provided key-value pairs as updates to the existing mapping.
        If a key already exists, its value is replaced; if it does not exist,
        the key-value pair is added. The original CoreDataMapping remains unchanged.

        .. code-block:: python
            original = CoreDataMapping({'a': 1, 'b': 2})
            modified = original.replace(b=3, c=4)
            # original is still CoreDataMapping({'a': 1, 'b': 2})
            # modified is CoreDataMapping({'a': 1, 'b': 3, 'c': 4})

        .. warning:: It is **possible** to create a CoreDataMapping with
            cyclical references using this method. Care should be taken
            to avoid such scenarios as they may lead to unexpected behavior
            and potentially non-serializability or infinite recursion during
            operations like hashing, comparison, or serialization.

            Normally, CoreDataMapping instances should be acyclic because
            their construction from standard data structures prevents cycles.

        :param changes: Key-value pairs to update in the mapping.
        :type changes: **CoreDataTypes
        :returns: A new CoreDataMapping with the specified changes applied.
        :rtype: CoreDataMapping
        :raises SimpleBenchTypeError: If the changes argument is not a Mapping
                                      or contains invalid keys or values.
        """
        if not all(key.isidentifier() for key in changes.keys()):
            raise SimpleBenchTypeError(
                'All keys in CoreDataMapping.replace() must be non-empty, non-blank strings and valid identifiers.',
                tag=_CoreDataErrorTag.CORE_DATA_MAPPING_INVALID_KEY_VALUE)

        # A shallow copy of the existing data to hold the modified data.
        # We don't need to validate keys or values because the constructor
        # will do that for us when we create the new instance
        return CoreDataMapping(dict(self._data) | changes)

    def thaw(self, preserve_immutability: bool = False) -> 'dict[str, CoreDataTypes] | CoreDataMapping':
        """Convert the CoreDataMapping to a standard mutable dict.

        :param preserve_immutability: If True, the nested :class:`CoreDataMapping`
            instances are preserved as-is instead of being thawed
            to mutable :class:`dict`. Defaults to :obj:`False`. This is useful
            when the caller wants to maintain the immutability of nested mappings
            and mainly used for internal purposes when recursively thawing CoreDataSet instances.
        :type preserve_immutability: bool
        :returns: A mutable dict representation of the CoreDataMapping.
        :rtype: dict[str, CoreDataTypes] | CoreDataMapping
        """
        # Import here to avoid circular imports
        from ._core_data_sequence import CoreDataSequence
        from ._core_data_set import CoreDataSet

        if preserve_immutability:
            return self
        thawed_dict: dict[str, CoreDataTypes] = {}
        for key, value in self._data.items():
            if isinstance(value, (CoreDataSet, CoreDataMapping, CoreDataSequence)):
                thawed_dict[key] = value.thaw(preserve_immutability=preserve_immutability)
            else:
                thawed_dict[key] = value
        return thawed_dict

    def for_json(self) -> dict[str, 'CoreDataTypes']:
        """Convert the CoreDataMapping to a JSON-serializable dict.

        JSON-serialization inherently loses some type information since JSON
        does not have a set type, so this method is intended for serialization
        purposes only and not for general data manipulation.

        This differs from `thaw` in that `thaw` returns mutable types where possible
        and so cannot unwrap nested CoreData* types within sets, while `for_json`
        focuses solely on preparing the data for JSON serialization and
        so converts nested CoreData* types appropriately to JSON-serializable forms
        regardless of Python semantics like sets vs lists or mutability constraints.

        :returns: A JSON-serializable dict representation of the CoreDataMapping.
        :rtype: dict[str, 'CoreDataTypes']
        """
        from ._core_data_sequence import CoreDataSequence
        from ._core_data_set import CoreDataSet

        json_dict: dict[str, CoreDataTypes] = {}
        for key, value in self._data.items():
            if isinstance(value, (CoreDataMapping, CoreDataSequence, CoreDataSet)):
                json_dict[key] = value.for_json()
            elif isinstance(value, bytes):  # bytes are converted to data URLs for JSON compatibility
                json_dict[key] = _common.data_url(value)
            else:
                json_dict[key] = value
        return json_dict


    def as_json(self) -> str:
        """Serialize the CoreDataMapping to a JSON string.

        :returns: A JSON string representation of the CoreDataMapping.
        :rtype: str
        """
        return simplejson.dumps(
            self.for_json(), sort_keys=True, for_json=True, iterable_as_array=True)

    def __deepcopy__(self, memo: dict[int, Any]) -> 'CoreDataMapping':
        """Return the same CoreDataMapping.

        Since the CoreDataMapping instance is immutable and composed of
        immutable components, there is no need to perform a deep copy
        of its contents. Instead, we simply return the instance itself
        which is a extremely fast O(1) operation.

        If a true deep copy is required for some reason, the caller
        can manually create a new instance by passing the thawed contents
        to the constructor.

        :param memo: The memoization dictionary used by `copy.deepcopy`.
                     It is not used in this optimized implementation.
        :return CoreDataMapping: The same CoreDataMapping instance.
        """
        # because the CoreDataMapping is immutable, we return self
        # instead of performing an actual copy.
        return self

    def __copy__(self) -> 'CoreDataMapping':
        """Return the same CoreDataMapping.

        Since the CoreDataMapping instance is immutable and composed of
        immutable components, there is no need to perform a shallow copy
        of its contents. Instead, we simply return the same instance
        which is a extremely fast O(1) operation.

        If a true copy is required for some reason, the caller
        can manually create a new instance by passing the thawed contents
        to the constructor.

        :return CoreDataMapping: The same CoreDataMapping instance.
        """
        # because the CoreDataMapping is immutable, we return self
        # instead of performing an actual copy.
        return self
