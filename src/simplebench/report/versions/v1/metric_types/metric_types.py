"""Definition for a MetricTypes object for the simplebench library."""
import hashlib
from collections.abc import Iterable, Iterator, Mapping, Sequence, Set
from typing import Any

from simplebench.exceptions import SimpleBenchKeyError, SimpleBenchTypeError
from simplebench.report._error_tags import _MetricTypesErrorTag
from simplebench.report.base import ReportElement
from simplebench.simplebench_types import CoreDataMapping, Never

from ..metric_type import MetricType, MetricTypeData
from . import _validate

__all__: list[str] = []


class MetricTypes(ReportElement, Mapping[str, MetricType]):
    """Definition for a MetricTypes object, which is a Mapping of str to MetricType instances.
    """

    __slots__ = ('_dict', '_hash_id')

    def __init__(self, __metric_types: 'Iterable[MetricType] | MetricTypes') -> None:
        """Initialize a MetricTypes instance.

         The constructor accepts an iterable of MetricType objects
         or another MetricTypes object to initialize this MetricTypes instance with.
        """
        metric_types = _validate.metric_types(__metric_types)
        self._dict: dict[str, MetricType] = {metric_type.label: metric_type for metric_type in metric_types}
        self._hash_id: str = self._compute_hash_id()

    def _compute_hash_id(self) -> str:
        """Compute the hash ID for the MetricTypes object based on the hash IDs of the individual
        MetricType objects it contains.

        The hash ID is computed by creating a tuple of the hash IDs of the individual MetricType objects,
        and then hashing that tuple to produce a unique identifier for the combination of metric_types.

        :return: The computed hash ID for the MetricTypes object.
        :rtype: str
        """
        metric_type_hash_ids: tuple[str, ...] = tuple(metric_type.hash_id for metric_type in sorted(
            self._dict.values(), key=lambda m: m.hash_id))
        hash_input = '\x00'.join(metric_type_hash_ids).encode('utf-8')
        return hashlib.sha256(hash_input).hexdigest()

    @classmethod
    def from_dict(cls, data: Mapping[str, MetricTypeData]) -> 'MetricTypes':
        """Initialize the MetricTypes instance from a mapping.

        :param data: The mapping containing the metric type data.
        :type data: Mapping[str, MetricTypeData]
        """
        if not isinstance(data, Mapping):
            raise SimpleBenchTypeError(
                f"Expected a mapping to initialize MetricTypes, got {type(data).__name__}",
                tag=_MetricTypesErrorTag.INVALID_METRICS_FIELD_TYPE,
            )
        metric_types_list: list[MetricType] = []
        for key, value in data.items():
            if isinstance(value, Mapping):
                metric_type = MetricType.from_dict(value)
                # implicitly checks that the key is a string since metric_type.label is always a string
                if metric_type.label != key:
                    raise SimpleBenchKeyError(
                        f"Key '{key}' in metric types mapping does not match the "
                        f"'label' field of the MetricType: '{metric_type.label}'",
                        tag=_MetricTypesErrorTag.MISMATCHED_KEY,
                    )
                metric_types_list.append(metric_type)
            else:
                raise SimpleBenchTypeError(
                    "Expected a mapping of str to MetricType data mappings, but found "
                    f"value of type {type(value).__name__} for key '{key}'",
                    tag=_MetricTypesErrorTag.INVALID_METRIC_TYPES_FIELD_TYPE,
                )
        return cls(metric_types_list)

    def to_dict(self) -> CoreDataMapping:
        """Convert the MetricTypes instance to a dictionary.

        Returns an immutable dictionary representation of the MetricTypes instance.
        It is actually a :class:`~simplebench.simplebench_types.CoreDataMapping` instance.

        :return: A dictionary representation of the MetricTypes instance.
        :rtype: CoreDataMapping
        """
        output_dict = {metric_type.label: metric_type.to_dict() for metric_type in self._dict.values()}
        return CoreDataMapping(output_dict)  # type: ignore

    def for_json(self) -> CoreDataMapping:
        """Convert the MetricTypes instance to a JSON-serializable dictionary.

        This is the same as `to_dict` since the output of `to_dict` is already JSON-serializable.

        :return: A JSON-serializable dictionary representation of the MetricTypes instance.
        :rtype: CoreDataMapping
        """
        return self.to_dict()

    def as_json(self) -> str:
        """Convert the MetricTypes instance to a JSON string.

        :return: A JSON string representation of the MetricTypes instance.
        :rtype: str
        """
        return self.to_dict().as_json()  # type: ignore

    @property
    def hash_id(self) -> str:
        """The hash ID of the metric types."""
        return self._hash_id

    def __repr__(self) -> str:
        """Get the string representation of the MetricTypes instance.

        :return: The string representation of the MetricTypes instance.
        :rtype: str
        """
        calling_args: tuple[MetricType, ...] = tuple(self._dict.values())
        return f'{self.__class__.__name__}({calling_args!r})'

    def __hash__(self) -> int:
        """Get the hash of the MetricTypes instance.

        :return: The hash value.
        :rtype: int
        """
        return hash(self.hash_id)

    def __eq__(self, other: object) -> bool:
        """Check equality between two MetricTypes instances.

        :param other: The other object to compare.
        :return: True if equal, False otherwise.
        :rtype: bool
        :raises SimpleBenchTypeError: If the other object is not a MetricTypes instance.
        """
        if not isinstance(other, MetricTypes):
            raise SimpleBenchTypeError(
                f"Cannot compare MetricTypes with object of type {type(other).__name__}",
                tag=_MetricTypesErrorTag.INCOMPARABLE_TYPE,
            )
        return self.hash_id == other.hash_id

    def __copy__(self) -> 'MetricTypes':
        """Create a copy of the MetricTypes instance.

        It returns self since the MetricTypes instance is immutable and can be shared safely.

        :return: The MetricTypes instance.
        :rtype: MetricTypes
        """
        return self

    def __deepcopy__(self, memo: dict[int, Any]) -> 'MetricTypes':
        """Create a deep copy of the MetricTypes instance.

        It returns self since the MetricTypes instance is immutable and can be shared safely.

        :return: The MetricTypes instance.
        :rtype: MetricTypes
        """
        return self

    def __getitem__(self, key: str) -> MetricType:
        """Get the MetricType for the given key.

        :param key: The key.
        :type key: str
        :returns: The corresponding MetricType.
        :rtype: MetricType
        :raises SimpleBenchKeyError: If the key is not found.
        """
        if key in self._dict:
            return self._dict[key]
        raise SimpleBenchKeyError(
            f'Key "{key}" not found in MetricTypes object',
            tag=_MetricTypesErrorTag.METRIC_TYPE_NOT_FOUND)

    def get(self, key: str) -> MetricType:  # type: ignore[override]
        """Get the MetricType for the given key, or raise an error if the key is not found.

        It does not support a default value since MetricTypes is immutable and all valid keys should
        always be present. This is a deliberate design choice to ensure that any access
        to a key that is not defined results in an error.

        If a key is accessed that is not defined, it indicates a bug in the code
        that needs to be fixed, rather than a case where a default value would be appropriate.

        :param key: The key.
        :type key: str
        :returns: The corresponding value.
        :rtype: MetricType
        """
        return self.__getitem__(key)

    def __setitem__(self, key: str, value: Never) -> None:
        """Always raises an error since MetricTypes is immutable and does
        not support item assignment.

        :param key: The key to set.
        :type key: str
        :param value: The value to set.
        :type value: Never
        :raises SimpleBenchTypeError: Always, since MetricTypes is immutable.
        """
        raise SimpleBenchTypeError(
            'MetricTypes is immutable and does not support item assignment.',
            tag=_MetricTypesErrorTag.MAPPING_IMMUTABLE)

    def __add__(self, other: 'MetricTypes | MetricType') -> 'MetricTypes':
        """Create a new MetricTypes object by combining two MetricTypes objects
        or adding a single MetricType object.

        :param other: The MetricTypes or MetricType object to add.
        :type other: MetricTypes or MetricType
        :return: A new MetricTypes object containing the combined metric types.
        :rtype: MetricTypes
        :raises SimpleBenchTypeError: If the other object is not a MetricTypes instance.
        :raises SimpleBenchKeyError: If there are duplicate metric type labels when combining.
        """
        return self._internal_add_or_union(other, allow_duplicates=False)

    def _internal_add_or_union(self,
                               other: 'MetricTypes | MetricType',
                               *,
                               allow_duplicates: bool = False) -> 'MetricTypes':
        """Internal method to create a new MetricTypes object by combining two MetricTypes objects
        or adding a single MetricType object, with an option to allow duplicates.

        :param other: The MetricTypes or MetricType object to add.
        :param allow_duplicates: Whether to allow duplicate metric type labels when combining.
            If False, a SimpleBenchKeyError will be raised if duplicate labels are found.
            If True, duplicate labels will be allowed and the last one encountered will be used.
        :return: A new MetricTypes object containing the combined metric types.
        :raises SimpleBenchTypeError: If the other object is not a MetricTypes instance or a MetricType instance.
        :raises SimpleBenchKeyError: If there are duplicate metric type labels when combining and
            allow_duplicates is False.
        """
        if not isinstance(other, (MetricTypes, MetricType)):
            raise SimpleBenchTypeError(
                'Can only add MetricTypes or MetricType objects.',
                tag=_MetricTypesErrorTag.INVALID_ADDEND_TYPE
            )
        if isinstance(other, MetricType):
            new_dict = dict(self._dict)
            label = other.label
            if label in new_dict and not allow_duplicates:
                raise SimpleBenchKeyError(
                    f'Duplicate metric type label "{label}" found when adding MetricType to MetricTypes object',
                    tag=_MetricTypesErrorTag.DUPLICATE_METRIC_TYPE_LABEL)
            new_dict.update({other.label: other})
            return MetricTypes(new_dict.values())
        else:
            new_dict = dict(self._dict)
            for metric_type in other._dict.values():
                label = metric_type.label
                if label in new_dict and not allow_duplicates:
                    raise SimpleBenchKeyError(
                        f'Duplicate metric type label "{label}" found when adding MetricTypes to MetricTypes object',
                        tag=_MetricTypesErrorTag.DUPLICATE_METRIC_TYPE_LABEL)
                new_dict.update({label: metric_type})
            return MetricTypes(new_dict.values())

    def __sub__(self, other: 'MetricTypes | MetricType | Sequence[str] | Set[str]') -> 'MetricTypes':
        """Create a new MetricTypes object by subtracting another MetricTypes or MetricType object's keys
        or a sequence or set of string label identifiers.

        The new object will contain all metric types from this object, except for those
        whose keys are also present in the `other` object.

        - Subtracting a single MetricType object will remove the metric type with the same label as that MetricType
            from the new object.
        - Subtracting a MetricTypes object will remove all metric types with labels that are present in the
            `other` MetricTypes object from the new object.
        - Subtracting a sequence or set of string label identifiers will remove all metric types with labels that are
            present in the sequence or set from the new object.

        Subtracting a non-existent key will simply be ignored and will not raise an error.

        :param other: The MetricTypes or MetricType object or a sequence or set of string label identifiers
            whose keys will be subtracted.
        :return: A new MetricTypes object with the subtracted metric types.
        :raises SimpleBenchTypeError: If the other object is not a MetricTypes instance, a MetricType instance, or
            a sequence or set of string label identifiers.
        """
        if isinstance(other, (str, bytes)):
            raise SimpleBenchTypeError(
                'Cannot subtract a single string label identifier. To subtract by label, '
                'provide a sequence or set of string label identifiers.',
                tag=_MetricTypesErrorTag.INVALID_SUBTRAHEND_TYPE
            )
        if not isinstance(other, (MetricTypes, MetricType, Sequence, Set)):
            raise SimpleBenchTypeError(
                'Can only subtract MetricTypes or MetricType objects or '
                'Sequences or Sets of string label identifiers.',
                tag=_MetricTypesErrorTag.INVALID_SUBTRAHEND_TYPE
            )
        if isinstance(other, (Sequence, Set)):
            new_dict = dict(self._dict)
            for label in other:
                if label in new_dict:
                    del new_dict[label]
            return MetricTypes(new_dict.values())

        # Create an iterable of metric types from `self` that are not in `other`.
        if isinstance(other, MetricType):
            metric_types_to_keep = (value for key, value in self.items() if key != other.label)
        else:  # MetricTypes
            metric_types_to_keep = (value for key, value in self.items() if key not in other)

        # Return a new MetricTypes object initialized with the filtered metric types.
        return MetricTypes(metric_types_to_keep)

    def __or__(self, other: 'MetricTypes | MetricType') -> 'MetricTypes':
        """Create a new MetricTypes object representing the union (same as +
        except it allows duplicates and does not raise an error if duplicate labels are found).

        :param other: The MetricTypes object to perform the union with.
        :return: A new MetricTypes object representing the union.
        """
        return self._internal_add_or_union(other, allow_duplicates=True)

    def __and__(self, other: 'MetricTypes') -> 'MetricTypes':
        """Create a new MetricTypes object representing the intersection.

        The new object will contain only the metric types whose keys are present
        in both this object and the `other` object.

        :param other: The MetricTypes object to intersect with.
        :return: A new MetricTypes object representing the intersection.
        :raises SimpleBenchTypeError: If the other object is not a MetricTypes instance.
        """
        if not isinstance(other, MetricTypes):
            raise SimpleBenchTypeError(
                f"Cannot perform intersection with object of type {type(other).__name__}",
                tag=_MetricTypesErrorTag.INCOMPARABLE_TYPE,
            )

        intersecting_metric_types = (value for key, value in self.items() if key in other)
        return MetricTypes(intersecting_metric_types)

    def __xor__(self, other: 'MetricTypes') -> 'MetricTypes':
        """Create a new MetricTypes object representing the symmetric difference.

        The new object will contain metric types that are in either this object or
        the `other` object, but not in both.

        :param other: The MetricTypes object to perform the symmetric difference with.
        :return: A new MetricTypes object representing the symmetric difference.
        :raises SimpleBenchTypeError: If the other object is not a MetricTypes instance.
        """
        if not isinstance(other, MetricTypes):
            raise SimpleBenchTypeError(
                f"Cannot perform symmetric difference with object of type {type(other).__name__}",
                tag=_MetricTypesErrorTag.INCOMPARABLE_TYPE,
            )

        sym_diff_keys = set(self.keys()) ^ set(other.keys())
        sym_diff_metric_types = []
        for key in sym_diff_keys:
            if key in self:
                sym_diff_metric_types.append(self[key])
            else:
                sym_diff_metric_types.append(other[key])

        return MetricTypes(sym_diff_metric_types)

    def __iadd__(self, other: 'MetricTypes | MetricType') -> 'MetricTypes':
        """Perform in-place addition (extend).

        Not implemented because MetricTypes is immutable and does not support in-place modification.
        This method will always raise a SimpleBenchTypeError.

        :param other: The MetricTypes object to add.
        :return: The modified MetricTypes object.
        :raises SimpleBenchTypeError: Always, since MetricTypes is immutable and does not
            support in-place modification.
        """
        raise SimpleBenchTypeError(
            'MetricTypes objects are immutable and do not support in-place addition.',
            tag=_MetricTypesErrorTag.MAPPING_IMMUTABLE
        )

    def __isub__(self, other: 'MetricTypes | MetricType | Sequence[str] | Set[str]') -> 'MetricTypes':
        """Perform in-place subtraction.

        Not implemented because MetricTypes is immutable and does not support in-place modification.
        This method will always raise a SimpleBenchTypeError.

        :param other: The MetricTypes object, MetricType object, sequence of keys, or set of keys to remove.
        :return: The modified MetricTypes object.
        :raises SimpleBenchTypeError: Always, since MetricTypes is immutable and does not
            support in-place modification.
        """
        raise SimpleBenchTypeError(
            'MetricTypes objects are immutable and do not support in-place subtraction.',
            tag=_MetricTypesErrorTag.MAPPING_IMMUTABLE
        )

    def __delitem__(self, name: str) -> None:
        """Delete a mapping value from the MetricTypes object.

        :param name: The key to delete.
        :type name: str

        :raises SimpleBenchTypeError: Always, since MetricTypes is immutable and does not support item deletion.
        """
        raise SimpleBenchTypeError(
            f'Cannot delete key "{name}" from MetricTypes object since it is immutable.',
            tag=_MetricTypesErrorTag.MAPPING_IMMUTABLE
        )

    def __contains__(self, name: Any) -> bool:
        """Return True if the key exists in the MetricTypes object.

        :param name: The key to check.
        :type name: str
        :return: True if the key exists in the MetricTypes object."""
        return name in self._dict

    def __iter__(self) -> Iterator[str]:
        """Return an iterator over the metric type keys in the MetricTypes object.
        :return: An iterator over the metric type keys.
        :rtype: Iterator[str]
        """
        yield from self._dict.keys()

    def __len__(self) -> int:
        """Return the number of metric types in the MetricTypes object.
        :return: The number of metric types.
        :rtype: int
        """
        return len(self._dict)
