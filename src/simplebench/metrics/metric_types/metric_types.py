"""Namespace class for metric types.

This class is designed to store and manage metric types in a structured way for
use in benchmarks and reporters. Each metric type is stored as an attribute of the
MetricTypes object, and the class ensures that all keys are valid Python identifiers
and that all values are instances of MetricType. Once a metric type is added, it
cannot be changed. The class also provides a method to delete a metric type from the
MetricTypes object.

"""
import re
from collections.abc import MutableMapping
from typing import Any, Iterable, Iterator

from simplebench.exceptions import SimpleBenchDuplicateKeyError, SimpleBenchTypeError, SimpleBenchValueError
from simplebench.metrics.metric_type import MetricType

from ._error_tags import _MetricTypesErrorTag


class MetricTypes(MutableMapping[str, MetricType]):
    """
    A namespace class for metric types that behaves like a read-only dictionary.
    This class can be used to store and manage metric types in a structured way.
    Each metric type is stored as an attribute of the MetricTypes object.

    The class ensures that all keys are valid Python identifiers and that all
    values are instances of MetricType. Once a metric type is added, it cannot
    be changed.

    The class also provides a method to delete a metric type from the MetricTypes object.
    The key must exist in the MetricTypes object and contain a MetricType object.
    """

    _VALID_KEY_REGEX = re.compile(r'^[A-Z](?:[A-Z0-9_]*[A-Z0-9])?$')
    """Regex pattern for a valid metric key.

    This pattern ensures that the key starts with an uppercase letter,
    followed by uppercase letters, digits, or underscores. The key cannot
    start or end with an underscore or digit.
    """

    def __init__(self, metric_types: Iterable[MetricType] | 'MetricTypes' | MetricType | None = None) -> None:
        """Initialize the MetricTypes object with an optional list of metric types.

        :param metric_types: A MetricType, an Iterable of MetricType objects, or a MetricTypes instance
            to initialize the MetricTypes object.
        :raises SimpleBenchTypeError: If the input is not a MetricType, an Iterable of MetricType,
            or a MetricTypes instance.
        """
        super().__init__()
        if metric_types is None:
            return
        if isinstance(metric_types, MetricType):
            metric_types = [metric_types]
        self.extend(metric_types)

    def extend(self, metric_types: Iterable[MetricType] | 'MetricTypes') -> None:
        """Add multiple metric types to the MetricTypes object.

        :param metric_types: An Iterable of MetricType objects or another MetricTypes object.
        :raises SimpleBenchTypeError: If the input is not an Iterable of MetricType
        :raises SimpleBenchDuplicateKeyError: If a duplicate key is found.
        """
        if isinstance(metric_types, MetricTypes):
            metric_types = metric_types.values()

        validated_metric_types = self._validate_metric_types_iterable(metric_types)

        for metric_type in validated_metric_types:
            self[metric_type.label] = metric_type

    def add(self, metric_type: MetricType) -> None:
        """Add a single MetricType to the MetricTypes object.

        :param metric_type: A MetricType object to add.
        :raises SimpleBenchDuplicateKeyError: If a duplicate key is found.
        """
        self[metric_type.label] = metric_type

    def _is_valid_key_name(self, key: str) -> bool:
        """Check if the key is formatted as a valid metric key .

        :param key: The key to check.
        :return: True if the key is valid, False otherwise.
        """
        return bool(isinstance(key, str) and self._VALID_KEY_REGEX.match(key))

    def _validate_metric_types_iterable(
            self,
            metric_types: Iterable[MetricType]) -> list[MetricType]:
        """Validate that the input is an Iterable of MetricType objects.

        :param metric_types: An Iterable of MetricType objects.
        :return: A list of MetricType objects.
        :raises SimpleBenchTypeError: If the input is not an Iterable of MetricType.
        """
        if not isinstance(metric_types, Iterable):
            raise SimpleBenchTypeError(
                "Not an Iterable of MetricType",
                tag=_MetricTypesErrorTag.NOT_ITERABLE_ERROR)

        # Convert to a list *once* to avoid exhausting the iterator.
        metric_types_list = list(metric_types)
        if not all(isinstance(metric_type, MetricType) for metric_type in metric_types_list):
            raise SimpleBenchTypeError(
                "Not an Iterable of MetricType",
                tag=_MetricTypesErrorTag.INVALID_METRICS_LIST_ITEM_TYPE)

        return metric_types_list

    def _validate_key_name(self, key: str) -> str:
        """Validate that the key matches the regex pattern for a metric type key.

        :param key: The key to validate.
        :return: The validated key.
        :raises SimpleBenchTypeError: If the key is not a string.
        :raises SimpleBenchValueError: If the key does not match the regex pattern.
        """
        if not isinstance(key, str):
            raise SimpleBenchTypeError(
                "Key must be a string",
                tag=_MetricTypesErrorTag.TYPE_ERROR)
        if not self._VALID_KEY_REGEX.match(key):
            raise SimpleBenchValueError(
                "Key must start with an uppercase letter or underscore, "
                "followed by uppercase letters, digits, or underscores",
                tag=_MetricTypesErrorTag.INVALID_KEY_FORMAT)
        return key

    def __setattr__(self, name: str, value: Any) -> None:
        """Set an attribute on the MetricTypes object.

        :param name: The attribute name.
        :param value: The attribute value.
        :raises AttributeError: If the key is a valid metric type key and exists in the MetricTypes object
        """
        if self._is_valid_key_name(name):
            raise AttributeError(
                f"Cannot set metric type '{name}' directly as an attribute. "
                "Use the dictionary-style assignment: metric_types['{name}'] = value"
            )

        super().__setattr__(name, value)

    def __getitem__(self, name: str) -> MetricType:
        """Get a mapping value from the MetricTypes object.

        If the key is not a string, a SimpleBenchTypeError is raised.
        If the key does not match the regex pattern for a metric type key, a
        SimpleBenchValueError is raised.
        If the key does not exist in the MetricTypes object or does not contain a
        MetricType object, a KeyError is raised.
        :param name: The key to get.
        :return: The value associated with the key.
        :raises SimpleBenchTypeError: If the key is not a string.
        :raises KeyError: If the key does not exist in the MetricTypes object or
            does not contain a MetricType object.
        """
        if name not in self:
            raise KeyError(name)
        return getattr(self, name)

    def __setitem__(self, name: str, value: MetricType) -> None:
        """Set a mapping value in the Metrics object.

        - If the key is not a string, a SimpleBenchTypeError is raised.
        - If the key does not match the regex pattern for a metric key, a SimpleBenchValueError is raised.
        - If the value is not an instance of MetricDefinition, a SimpleBenchTypeError is raised.
        - If the key does not match the label of the MetricDefinition object, a SimpleBenchValueError is raised.
        - If the key already exists and is associated with a different MetricDefinition object,
            a SimpleBenchDuplicateKeyError is raised.

        :param name: The key to set.
        :param value: The value to set.
        :raises SimpleBenchTypeError: If the value is not an instance of MetricDefinition.
        :raises SimpleBenchValueError: If the key does not match the label of the MetricDefinition object.
        :raises SimpleBenchDuplicateKeyError: If the key already exists in the Metrics object
        """
        name = self._validate_key_name(name)
        if not isinstance(value, MetricType):
            raise SimpleBenchTypeError(
                "value must be an instance of MetricDefinition",
                tag=_MetricTypesErrorTag.TYPE_ERROR)
        if name != value.label:
            raise SimpleBenchValueError(
                "Key must match the label of the MetricDefinition object",
                tag=_MetricTypesErrorTag.MISMATCHED_KEY)
        if hasattr(self, name):
            # If the exact same object is already registered, it's a no-op.
            if getattr(self, name) is value:
                return

            # Otherwise, it's a different object trying to use the same key.
            raise SimpleBenchDuplicateKeyError(
                f"Duplicate key '{name}' found in metrics",
                tag=_MetricTypesErrorTag.DUPLICATE_KEY)

        # The key is not yet present, so we can safely set it.
        # Use object.__setattr__ to bypass our custom __setattr__ method.
        object.__setattr__(self, name, value)

    def __add__(self, other: 'MetricTypes | MetricType') -> 'MetricTypes':
        """Create a new MetricTypes object by combining two MetricTypes objects.

        :param other: The MetricTypes or MetricType object to add.
        :return: A new MetricTypes object containing the combined metric types.
        :raises TypeError: If the other object is not a MetricTypes or MetricType instance.
        """
        if not isinstance(other, (MetricTypes, MetricType)):
            return NotImplemented

        # Create a new MetricTypes object from the first one.
        new_metric_types = MetricTypes(self)
        # Extend it with metric types from the second one.
        new_metric_types.extend(other if isinstance(other, MetricTypes) else [other])
        return new_metric_types

    def __sub__(self, other: 'MetricTypes | MetricType') -> 'MetricTypes':
        """Create a new MetricTypes object by subtracting another MetricTypes or MetricType object's keys.

        The new object will contain all metric types from this object, except for those
        whose keys are also present in the `other` object.

        :param other: The MetricTypes or MetricType object whose keys will be subtracted.
        :return: A new MetricTypes object with the subtracted metric types.
        :raises TypeError: If the other object is not a MetricTypes or MetricType instance.
        """
        if not isinstance(other, (MetricTypes, MetricType)):
            return NotImplemented

        # Create an iterable of metric types from `self` that are not in `other`.
        if isinstance(other, MetricType):
            metric_types_to_keep = (value for key, value in self.items() if key != other.label)
        else:  # MetricTypes
            metric_types_to_keep = (value for key, value in self.items() if key not in other)

        # Return a new MetricTypes object initialized with the filtered metric types.
        return MetricTypes(metric_types_to_keep)

    def __or__(self, other: 'MetricTypes | MetricType') -> 'MetricTypes':
        """Create a new MetricTypes object representing the union (same as +).

        :param other: The MetricTypes or MetricType object to perform the union with.
        :return: A new MetricTypes object representing the union.
        """
        return self.__add__(other)

    def __and__(self, other: 'MetricTypes | MetricType') -> 'MetricTypes':
        """Create a new MetricTypes object representing the intersection.

        The new object will contain only the metric types whose keys are present
        in both this object and the `other` object.

        :param other: The MetricTypes or MetricType object to intersect with.
        :return: A new MetricTypes object representing the intersection.
        """
        if not isinstance(other, (MetricTypes, MetricType)):
            return NotImplemented

        if isinstance(other, MetricType):
            intersecting_metric_types = (value for key, value in self.items() if key == other.label)
        else:
            intersecting_metric_types = (value for key, value in self.items() if key in other)
        return MetricTypes(intersecting_metric_types)

    def __xor__(self, other: 'MetricTypes | MetricType') -> 'MetricTypes':
        """Create a new MetricTypes object representing the symmetric difference.
        The new object will contain metric types that are in either this object or
        the `other` object, but not in both.

        :param other: The MetricTypes or MetricType object to perform the symmetric difference with.
        :return: A new MetricTypes object representing the symmetric difference.
        """
        if not isinstance(other, (MetricTypes, MetricType)):
            return NotImplemented

        if isinstance(other, MetricType):
            other = MetricTypes([other])

        sym_diff_keys = set(self.keys()) ^ set(other.keys())
        sym_diff_metrics = []
        for key in sym_diff_keys:
            if key in self:
                sym_diff_metrics.append(self[key])
            else:
                sym_diff_metrics.append(other[key])

        return MetricTypes(sym_diff_metrics)

    def __iadd__(self, other: 'MetricTypes | MetricType') -> 'MetricTypes':
        """Perform in-place addition (extend).

        :param other: The MetricTypes or MetricType object to add.
        :return: The modified MetricTypes object.
        """
        if not isinstance(other, (MetricTypes, MetricType)):
            return NotImplemented
        self.extend(other if isinstance(other, MetricTypes) else [other])
        return self

    def __isub__(self, other: 'MetricTypes | MetricType') -> 'MetricTypes':
        """Perform in-place subtraction.

        :param other: The MetricTypes or MetricType object whose keys will be removed.
        :return: The modified MetricTypes object.
        """
        if not isinstance(other, (MetricTypes, MetricType)):
            return NotImplemented
        if isinstance(other, MetricType):
            other = MetricTypes([other])
        for key in other:
            if key in self:
                del self[key]
        return self

    def __delitem__(self, name: str) -> None:
        """Delete a mapping value from the MetricTypes object.

        If the key is not a string, a SimpleBenchTypeError is raised.
        If the key does not match the regex pattern for a metric key, a
        SimpleBenchValueError is raised.
        If the key does not exist in the MetricTypes object, a KeyError is raised.
        If the key does not contain a MetricDefinition object, a KeyError is raised.
        :param name: The key to delete.
        :raises SimpleBenchTypeError: If the key is not a string.
        :raises SimpleBenchValueError: If the key does not match the regex pattern for a metric key.
        :raises KeyError: If the key does not exist in the MetricTypes object
            or does not contain a MetricDefinition object.
        """
        if name not in self:
            raise KeyError(name)
        delattr(self, name)

    def __contains__(self, name: Any) -> bool:
        """Return True if the key is a valid metric key and exists in the MetricTypes object
        and contains a MetricDefinition object.

        :param name: The key to check.
        :return: True if the key is a valid metric key and exists in the MetricTypes object
            and contains a MetricDefinition object."""
        if not self._is_valid_key_name(name):
            return False
        if not hasattr(self, name):
            return False
        return isinstance(getattr(self, name), MetricType)

    def __iter__(self) -> Iterator[str]:
        for key, value in self.__dict__.items():
            if self._is_valid_key_name(key) and isinstance(value, MetricType):
                yield key

    def __len__(self) -> int:
        return sum(1 for _ in self)
