"""report Extras base class.

This class represents Extras in a report.

It implements validation and serialization/deserialization methods to and from dictionaries
for a extras property object in a report ResultsInfo object.

It is not a standalone JSON schema object, but rather a component of the overall JSON report schema object

It is the base implemention of a extras object representation.
"""

from collections.abc import Iterable, Iterator, Mapping
from typing import Any

from simplebench.exceptions import SimpleBenchAttributeError, SimpleBenchKeyError
from simplebench.report._error_tags import _ExtrasErrorTag
from simplebench.simplebench_types import CoreDataMapping, CoreDataTypes, Immutable

__all__: list[str] = []


class ExtrasObject(Mapping[str, CoreDataTypes], Immutable):
    """Immutable base class representing the 'extras' object in a report ResultsInfo object.
    """

    __slots__ = ('_extras', '_hash_id')

    def __init__(self, __extras: Mapping[str, CoreDataTypes]) -> None:
        """Initialize a ExtrasObject v1 instance.

        :param Mapping[str, CoreDataTypes] extras: The extras dictionary. The keys are extra names
            and the values are :class:`CoreDataTypes` objects.
        """
        self._extras: CoreDataMapping[str] = CoreDataMapping(__extras)
        self._hash_id: int = hash(('ExtrasObject', self._extras))

    @classmethod
    def from_dict(cls, data: Mapping[str, CoreDataTypes]) -> 'ExtrasObject':
        """Create a Extras object instance from a dictionary.

        Because ExtrasObject is essentially a wrapper around a CoreDataMapping
        of extra names to extra items, the method just passes the input
        dictionary to the constructor.

        The from_dict method is provided for API consistency and to allow for potential future
        validation or transformation logic when creating an ExtrasObject from a dictionary.

        It also provides a clear and explicit way to create an ExtrasObject from a dictionary,
        which is used by the Hydrator base class when importing from dictionaries.

        :param data: Dictionary containing the JSON results object data.
        :return: JSON Extras object instance.
        :rtype: ExtrasObject
        """
        return cls(data)

    def to_dict(self) -> CoreDataMapping:
        """Convert the Extras object instance to a dictionary.

        This just returns the internal CoreDataMapping of extras,
        which is already a dictionary-like object mapping extra names
        to their corresponding CoreDataTypes values.

        :return: Dictionary representation of the Extras object.
        :rtype: CoreDataMapping[str]
        """
        return self.extras

    def for_json(self) -> CoreDataMapping:
        """Get the JSON-serializable dictionary representation of this ExtrasObject.

        This method delegates to the for_json method of the internal CoreDataMapping of
        extras, which will convert all the values to their JSON-serializable forms.

        :return: The JSON-serializable dictionary representation of this ExtrasObject.
        :rtype: CoreDataMapping
        """
        return self.extras.for_json()  # type: ignore

    def as_json(self) -> str:
        """Get the JSON string representation of this ExtrasObject.

        This method delegates to the as_json method of the internal CoreDataMapping of
        extras, which will convert the entire dictionary to a JSON string.

        :return: The JSON string representation of this ExtrasObject.
        :rtype: str
        """
        return self.extras.as_json()  # type: ignore

    def thaw(self) -> 'dict[str, CoreDataTypes] | CoreDataMapping':
        """Get the thawed (mutable) dictionary representation of this ExtrasObject.

        This method delegates to the thaw method of the internal CoreDataMapping of
        extras, which will return a mutable dictionary representation.

        :return: The thawed (mutable) dictionary representation of this ExtrasObject.
        :rtype: dict[str, CoreDataTypes] | CoreDataMapping
        """
        return self.extras.thaw()

    @property
    def extras(self) -> CoreDataMapping[str]:
        """Get the extras dictionary.

        :return: The extras dictionary, mapping extra names to their corresponding CoreDataTypes values.
        :rtype: CoreDataMapping[str]
        """
        return self._extras

    def __eq__(self, other: object) -> bool:
        """Check equality with another ExtrasObject.

        Two ExtrasObject instances are considered equal if their extras dictionaries are equal.

        :param other: The object to compare with.
        :return: True if the objects are equal, False otherwise.
        :rtype: bool
        """
        if not isinstance(other, ExtrasObject):
            return NotImplemented
        return self.extras == other.extras

    def __hash__(self) -> int:
        """Compute the hash of this ExtrasObject.

        The hash is computed based on the extras dictionary, which is converted to a frozenset
        of its items to ensure it is hashable.

        :return: The hash of this ExtrasObject.
        :rtype: int
        """
        return hash(self.extras)

    def __repr__(self) -> str:
        """Get the string representation of this ExtrasObject.

        :return: The string representation of this ExtrasObject.
        :rtype: str
        """
        return f'ExtrasObject({self.extras.thaw()!r})'


    @property
    def hash_id(self) -> str:
        """Get the hash ID of the ExtrasObject.

        The hash ID is a SHA-256 hash of the metric names and their corresponding
        metric item hash IDs, ensuring immutability and consistent hashing.

        :return str: The hash ID string.
        """
        return self._extras.content_hash()

    def __setitem__(self, key: str, value: Any) -> None:
        """Set a value in the extras dictionary.

        Disabled because the ExtrasObject is immutable. Attempting to
        set an item will raise an error.

        :param key: The metric name.
        :param value: The CoreDataTypes object (either a StatsBlock or a ValueBlock).
        :raises SimpleBenchAttributeError: Always, since the ExtrasObject is immutable.
        """
        raise SimpleBenchAttributeError(
            'ExtrasObject is immutable and cannot be modified after initialization.',
            tag=_ExtrasErrorTag.EXTRAS_OBJECT_IMMUTABLE,
            name=key,
            obj=self,
        )

    def __getitem__(self, key: str) -> 'CoreDataTypes':
        """Get a metric item from the metrics dictionary.

        :param key: The metric name.
        :return: The CoreDataTypes object (either a StatsBlock or a ValueBlock).
        :raises SimpleBenchKeyError: If the metric name does not exist.
        """
        try:
            return self._extras[key]
        except KeyError as e:
            raise SimpleBenchKeyError(
                f"Metric name '{key}' does not exist in metrics.",
                tag=_ExtrasErrorTag.KEY_ERROR_INVALID_EXTRA_NAME_VALUE,
            ) from e

    def __delitem__(self, key: str) -> None:
        """Delete a metric item from the metrics dictionary.

        Disabled because the ExtrasObject is immutable. Attempting to delete an item will raise an error.

        :param key: The metric name.
        :raises SimpleBenchAttributeError: Always, since the ExtrasObject is immutable.
        """
        raise SimpleBenchAttributeError(
            f"Metric '{key}' cannot be deleted because the ExtrasObject is immutable.",
            tag=_ExtrasErrorTag.EXTRAS_OBJECT_IMMUTABLE,
            name=key,
            obj=self,
        )

    def __len__(self) -> int:
        """Get the number of metric items in the metrics dictionary.

        :return int: The number of metric items.
        """
        return len(self._extras)

    def __iter__(self) -> Iterator[str]:
        """Get an iterator over the metric names in the metrics dictionary.

        :return Iterator[str]: An iterator over the metric names.
        """
        return iter(self._extras)

    def __or__(self, other: object) -> 'ExtrasObject':
        """Return a new ExtrasObject that is the union of this and another ExtrasObject.

        .. code-block:: python
            new_metrics = this_metrics | other_metrics

        :param other: The other ExtrasObject to union with.
        :return ExtrasObject: A new ExtrasObject that is the union of both.
        """
        if isinstance(other, ExtrasObject):
            return self.__class__(dict(self._extras) | dict(other._extras))
        return NotImplemented

    def __ror__(self, other: object) -> 'ExtrasObject':
        """Return a new ExtrasObject that is the union of another ExtrasObject and this one. (reversed)

        .. code-block:: python
            new_metrics = other_metrics | this_metrics

        :param other: The other ExtrasObject to union with.
        :return ExtrasObject: A new ExtrasObject that is the union of both.
        """
        if isinstance(other, ExtrasObject):
            return self.__class__(dict(other._extras) | dict(self._extras))
        return NotImplemented

    def __ior__(self, other: object) -> 'ExtrasObject':
        """In-place union of this ExtrasObject with another ExtrasObject.

        Disabled because the ExtrasObject is immutable. Attempting to perform an in-place union will raise an error.
        """
        return NotImplemented

    def __contains__(self, key: object) -> bool:
        """Check if a metric name is in the metrics dictionary.

        :param key: The metric name to check for.
        :return bool: True if the metric name exists, False otherwise.
        """
        return key in self._extras

    def __copy__(self) -> 'ExtrasObject':
        """Return the same instance since ExtrasObject is immutable.

        :return ExtrasObject: The same instance of ExtrasObject.
        """
        return self

    def __deepcopy__(self, memo: dict[int, Any]) -> 'ExtrasObject':
        """Return a deep copy of the ExtrasObject.

        Since ExtrasObject is immutable, this method simply returns the same instance.

        :return ExtrasObject: The same instance of ExtrasObject.
        """
        return self

    def copy(self) -> 'ExtrasObject':
        """Get a copy of the ExtrasObject.

        It does not create a new instance since ExtrasObject is immutable, but it provides
        a copy method for API consistency.

        :return ExtrasObject: The same ExtrasObject instance.
        """
        return self

    @classmethod
    def fromkeys(cls, iterable: Iterable, value: CoreDataTypes | None = None) -> 'ExtrasObject':
        return NotImplemented

    def __getstate__(self) -> tuple[dict[str, Any] | None, tuple[Any, ...]]:
        """Prepare the object's state for pickling, prioritizing size.

        This method ensures that the pickled representation of the ExtrasObject
        is compact. It does this by excluding any cached or redundant attributes
        and only including the essential data needed to reconstruct the object.

        This prioritizes a small pickled size and fast subsequent unpickling over
        preserving the lazy-evaluation state across serialization.

        :return: A state tuple for pickling.
        :rtype: tuple[dict[str, Any] | None, tuple[Any, ...]]
        """
        slot_values: list[Any] = []
        for slot in self.__slots__:
            slot_values.append(getattr(self, slot))

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
        slot_values = state[1]
        for slot, value in zip(self.__slots__, slot_values, strict=True):
            self.__setattr__(slot, value)
