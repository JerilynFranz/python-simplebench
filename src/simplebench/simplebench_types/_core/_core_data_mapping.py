"""Core data mapping type for SimpleBench

This is an immutable mapping of core data types used in SimpleBench.

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

from simplebench.exceptions import SimpleBenchKeyError, SimpleBenchTypeError

from ._error_tags import _CoreDataErrorTag
from ._types import CORE_DATA_PRIMITIVE_TYPES_TUPLE, IMMUTABLE_CORE_DATA_TYPES_TUPLE, CoreDataTypes


class CoreDataMapping(Mapping[str, CoreDataTypes], Immutable, Hashable):
    """Deep-immutable Mapping container for CoreData types used in SimpleBench.

    This represents a mapping where all keys are strings and all values are of
    type :class:`CoreDataTypes`.

    When initializing, the provided iterable must be a Mapping
    containing only string keys and values of type :class:`CoreDataTypes`.

    The mapping itself is immutable once created with all contents being of valid CoreData types
    and converted to their respective immutable CoreData wrappers as needed.

    :param __iterable: A Mapping of str to CoreData elements to initialize the mapping or :obj:`None`.
    :type __iterable: Mapping[str, CoreDataTypes] | None
    """

    def __init__(self, __mapping: Mapping[str, CoreDataTypes] | None = None) -> None:
        """Initialize the CoreDataMapping.

        If a mapping is provided, it must be a Mapping of str to
        type :class:`CoreDataTypes`.

        If no mapping is provided, an empty mapping is created.

        :param __mapping: A mapping of str to CoreData elements to initialize the mapping or :obj:`None`.
        :type __mapping: Mapping[str, CoreDataTypes] | None
        """
        # Import here to avoid circular imports
        from ._core_data_sequence import CoreDataSequence
        from ._core_data_set import CoreDataSet

        self._data: dict[str, CoreDataTypes]
        if __mapping is None:
            self._data  = {}
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

        data: dict[str, CoreDataTypes] = {}

        for key, value in __mapping.items():
            if isinstance(value, Mapping):
                data[key] = CoreDataMapping(value)
            elif isinstance(value, Sequence) and not isinstance(value, (str, bytes)):
                data[key] = CoreDataSequence(value)
            elif isinstance(value, Set):
                data[key] = CoreDataSet(value)
            elif isinstance(value, CORE_DATA_PRIMITIVE_TYPES_TUPLE):
                data[key] = value
            else:
                 raise SimpleBenchTypeError(
                    f'Invalid value type passed to CoreDataMapping for key {key!r}: {value!r}. '
                    f'Must be a CoreData type: {IMMUTABLE_CORE_DATA_TYPES_TUPLE!r}.',
                    tag=_CoreDataErrorTag.CORE_DATA_MAPPING_INVALID_VALUE_TYPE)

        self._data = data

    def __getitem__(self, key: str) -> CoreDataTypes:
        """Get the value for the given key.

        :param key: The key.
        :type key: str
        :returns: The corresponding CoreDataTypes value.
        :rtype: CoreDataTypes
        :raises KeyError: If the key is not found.
        """
        try:
            return self._data[key]
        except KeyError as exc:
            raise SimpleBenchKeyError(
                f"Key {key!r} not found in CoreDataMapping.",
                tag=_CoreDataErrorTag.CORE_DATA_MAPPING_KEY_ERROR) from exc

    def __setitem__(self, key: str, value: CoreDataTypes) -> None:
        """Raise an error since CoreDataMapping is immutable.

        :param key: The key to set.
        :type key: str
        :param value: The value to set.
        :type value: CoreDataTypes
        :raises SimpleBenchTypeError: Always, since CoreDataMapping is immutable.
        """
        raise SimpleBenchTypeError(
            "CoreDataMapping is immutable and does not support item assignment.",
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

    def __hash__(self) -> int:
        """Return the hash of the CoreDataMapping.

        :returns: The hash of the mapping.
        :rtype: int
        """
        keys = tuple(sorted(self._data.keys()))
        items = ((key, self._data[key]) for key in keys)
        return hash(tuple(items))


    def thaw(self) -> dict[str, CoreDataTypes]:
        """Convert the CoreDataMapping to a standard mutable dict.

        :returns: A mutable dict representation of the CoreDataMapping.
        :rtype: dict[str, CoreDataTypes]
        """
        # Import here to avoid circular imports
        from ._core_data_sequence import CoreDataSequence
        from ._core_data_set import CoreDataSet

        thawed_dict: dict[str, CoreDataTypes] = {}
        for key, value in self._data.items():
            if isinstance(value, (CoreDataSet, CoreDataMapping, CoreDataSequence)):
                thawed_dict[key] = value.thaw()
            else:
                thawed_dict[key] = value
        return thawed_dict
