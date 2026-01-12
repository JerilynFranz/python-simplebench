"""Namespace class for metrics

This class is designed to store and manage metrics in a structured way for
use in benchmarks and reporters. Each metric is stored as an attribute of the
Metrics object, and the class ensures that all keys are valid Python identifiers
and that all values are instances of MetricDefinition. Once a metric is added, it
cannot be changed. The class also provides a method to delete a metric from the
Metrics object.

"""

import re
from collections.abc import MutableMapping
from typing import Any, Iterable, Iterator

from simplebench.exceptions import SimpleBenchDuplicateKeyError, SimpleBenchTypeError, SimpleBenchValueError
from simplebench.metrics.metric.metric import Metric

from ._error_tags import _MetricsErrorTag

__all__ = []


class Metrics(MutableMapping[str, Metric]):
    """
    A namespace class for metrics that behaves like a read-only dictionary.
    This class can be used to store and manage metrics in a structured way.
    Each metric is stored as an attribute of the Metrics object.

    The class ensures that all keys are valid Python identifiers and that all
    values are instances of MetricDefinition. Once a metric is added, it cannot
    be changed.

    The class also provides a method to delete a metric from the Metrics object.
    The key must exist in the Metrics object and contain a MetricDefinition object.
    """

    _VALID_KEY_REGEX = re.compile(r'^[A-Z](?:[A-Z0-9_]*[A-Z0-9])?$')
    """Regex pattern for a valid metric key.

    This pattern ensures that the key starts with an uppercase letter,
    followed by uppercase letters, digits, or underscores. The key cannot
    start or end with an underscore or digit.
    """

    def __init__(self, metrics: Iterable[Metric] | 'Metrics' | Metric | None = None) -> None:
        """Initialize the Metrics object with Metric objects.

        :param metrics: A Metric, an Iterable of Metric objects, or a Metrics instance to initialize the Metrics object.
        :raises SimpleBenchTypeError: If the input is not a Metric, an Iterable of Metric
            objects, or a Metrics instance.
        :raises SimpleBenchDuplicateKeyError: If a duplicate key is found.
        """
        super().__init__()
        if metrics is None:
            return
        if isinstance(metrics, Metric):
            metrics = [metrics]
        self.extend(metrics)

    def extend(self, metrics: Iterable[Metric] | 'Metrics') -> None:
        """Add multiple metrics to the Metrics object.

        :param metrics: An Iterable of Metric objects or another Metrics object.
        :raises SimpleBenchTypeError: If the input is not an Iterable of Metric
        :raises SimpleBenchDuplicateKeyError: If a duplicate key is found.
        """
        if isinstance(metrics, Metrics):
            metrics = metrics.values()

        validated_metrics = self._validate_metrics_iterable(metrics)

        for metric in validated_metrics:
            self[metric.label] = metric

    def add(self, metric: Metric) -> None:
        """Add a single Metric to the Metrics object.

        :param metric: A Metric object to add.
        :raises SimpleBenchDuplicateKeyError: If a duplicate key is found.
        """
        self[metric.label] = metric

    def _is_valid_key_name(self, key: str) -> bool:
        """Check if the key is formatted as a valid metric key .

        :param key: The key to check.
        :return: True if the key is valid, False otherwise.
        """
        return bool(isinstance(key, str) and self._VALID_KEY_REGEX.match(key))

    def _validate_metrics_iterable(self, metrics: Iterable[Metric]) -> list[Metric]:
        """Validate that the input is an Iterable of Metric objects.

        :param metrics: An Iterable of Metric objects.
        :return: A list of Metric objects.
        :raises SimpleBenchTypeError: If the input is not an Iterable of Metric.
        """
        if not isinstance(metrics, Iterable):
            raise SimpleBenchTypeError('Not an Iterable of Metric', tag=_MetricsErrorTag.NOT_ITERABLE_ERROR)

        # Convert to a list *once* to avoid exhausting the iterator.
        metrics_list = list(metrics)

        if not all(isinstance(metric, Metric) for metric in metrics_list):
            raise SimpleBenchTypeError('Not an Iterable of Metric', tag=_MetricsErrorTag.INVALID_METRICS_LIST_ITEM_TYPE)

        return metrics_list

    def _validate_key_name(self, key: str) -> str:
        """Validate that the key matches the regex pattern for a metric key.

        :param key: The key to validate.
        :return: The validated key.
        :raises SimpleBenchTypeError: If the key is not a string.
        :raises SimpleBenchValueError: If the key does not match the regex pattern.
        """
        if not isinstance(key, str):
            raise SimpleBenchTypeError('Key must be a string', tag=_MetricsErrorTag.TYPE_ERROR)
        if not self._VALID_KEY_REGEX.match(key):
            raise SimpleBenchValueError(
                'Key must start with an uppercase letter or underscore, '
                'followed by uppercase letters, digits, or underscores',
                tag=_MetricsErrorTag.INVALID_KEY_FORMAT,
            )
        return key

    def __setattr__(self, name: str, value: Any) -> None:
        """Set an attribute on the Metrics object.

        :param name: The attribute name.
        :param value: The attribute value.
        :raises AttributeError: If the key is a valid metric key and exists in the Metrics object
        """
        if self._is_valid_key_name(name):
            raise AttributeError(
                f"Cannot set metric '{name}' directly as an attribute. "
                "Use the dictionary-style assignment: metrics['{name}'] = value"
            )

        super().__setattr__(name, value)

    def __getitem__(self, name: str) -> Metric:
        """Get a mapping value from the Metrics object.

        If the key is not a string, a SimpleBenchTypeError is raised.
        If the key does not match the regex pattern for a metric key, a
        SimpleBenchValueError is raised.
        If the key does not exist in the Metrics object or does not contain a
        MetricDefinition object, a KeyError is raised.
        :param name: The key to get.
        :return: The value associated with the key.
        :raises SimpleBenchTypeError: If the key is not a string.
        :raises KeyError: If the key does not exist in the Metrics object or
            does not contain a MetricDefinition object.
        """
        if name not in self:
            raise KeyError(name)
        return getattr(self, name)

    def __setitem__(self, name: str, value: Metric) -> None:
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
        if not isinstance(value, Metric):
            raise SimpleBenchTypeError('value must be an instance of Metric', tag=_MetricsErrorTag.TYPE_ERROR)
        if name != value.label:
            raise SimpleBenchValueError(
                'Key must match the label of the Metric object', tag=_MetricsErrorTag.MISMATCHED_KEY
            )
        if hasattr(self, name):
            # If the exact same object is already registered, it's a no-op.
            if getattr(self, name) is value:
                return

            # Otherwise, it's a different object trying to use the same key.
            raise SimpleBenchDuplicateKeyError(
                f"Duplicate key '{name}' found in metrics", tag=_MetricsErrorTag.DUPLICATE_KEY
            )

        # The key is not yet present, so we can safely set it.
        # Use object.__setattr__ to bypass our custom __setattr__ method.
        object.__setattr__(self, name, value)

    def __add__(self, other: 'Metrics | Metric') -> 'Metrics':
        """Create a new Metrics object by combining two Metrics objects
        or adding a single Metric object.

        :param other: The Metrics or Metric object to add.
        :return: A new Metrics object containing the combined metrics.
        :raises TypeError: If the other object is not a Metrics instance.
        """
        if not isinstance(other, (Metrics, Metric)):
            return NotImplemented

        # Create a new Metrics object from the first one.
        new_metrics = Metrics(self)
        # Extend it with metrics from the second one.
        new_metrics.extend(other if isinstance(other, Metrics) else [other])
        return new_metrics

    def __sub__(self, other: 'Metrics | Metric') -> 'Metrics':
        """Create a new Metrics object by subtracting another Metrics or Metric object's keys.

        The new object will contain all metrics from this object, except for those
        whose keys are also present in the `other` object.

        :param other: The Metrics or Metric object whose keys will be subtracted.
        :return: A new Metrics object with the subtracted metrics.
        :raises TypeError: If the other object is not a Metrics instance.
        """
        if not isinstance(other, (Metrics, Metric)):
            return NotImplemented

        # Create an iterable of metrics from `self` that are not in `other`.
        if isinstance(other, Metric):
            metrics_to_keep = (value for key, value in self.items() if key != other.label)
        else:  # Metrics
            metrics_to_keep = (value for key, value in self.items() if key not in other)

        # Return a new Metrics object initialized with the filtered metrics.
        return Metrics(metrics_to_keep)

    def __or__(self, other: 'Metrics') -> 'Metrics':
        """Create a new Metrics object representing the union (same as +).

        :param other: The Metrics object to perform the union with.
        :return: A new Metrics object representing the union.
        """
        return self.__add__(other)

    def __and__(self, other: 'Metrics') -> 'Metrics':
        """Create a new Metrics object representing the intersection.

        The new object will contain only the metrics whose keys are present
        in both this object and the `other` object.

        :param other: The Metrics object to intersect with.
        :return: A new Metrics object representing the intersection.
        """
        if not isinstance(other, (Metric | Metrics)):
            return NotImplemented

        if isinstance(other, Metric):
            intersecting_metrics = (value for key, value in self.items() if key == other.label)
        else:
            intersecting_metrics = (value for key, value in self.items() if key in other)
        return Metrics(intersecting_metrics)

    def __xor__(self, other: 'Metrics | Metric') -> 'Metrics':
        """Create a new Metrics object representing the symmetric difference.

        The new object will contain metrics that are in either this object or
        the `other` object, but not in both.

        :param other: The Metrics or Metric object to perform the symmetric difference with.
        :return: A new Metrics object representing the symmetric difference.
        """
        if not isinstance(other, (Metrics, Metric)):
            return NotImplemented

        if isinstance(other, Metric):
            other = Metrics([other])

        sym_diff_keys = set(self.keys()) ^ set(other.keys())
        sym_diff_metrics = []
        for key in sym_diff_keys:
            if key in self:
                sym_diff_metrics.append(self[key])
            else:
                sym_diff_metrics.append(other[key])

        return Metrics(sym_diff_metrics)

    def __iadd__(self, other: 'Metrics | Metric') -> 'Metrics':
        """Perform in-place addition (extend).

        :param other: The Metrics object to add.
        :return: The modified Metrics object.
        """
        if not isinstance(other, (Metrics, Metric)):
            return NotImplemented
        self.extend(other if isinstance(other, Metrics) else [other])
        return self

    def __isub__(self, other: 'Metrics | Metric') -> 'Metrics':
        """Perform in-place subtraction.

        :param other: The Metrics object whose keys will be removed.
        :return: The modified Metrics object.
        """
        if not isinstance(other, (Metrics, Metric)):
            return NotImplemented
        if isinstance(other, Metric):
            other = Metrics([other])
        for key in other:
            if key in self:
                del self[key]
        return self

    def __delitem__(self, name: str) -> None:
        """Delete a mapping value from the Metrics object.

        If the key is not a string, a SimpleBenchTypeError is raised.
        If the key does not match the regex pattern for a metric key, a
        SimpleBenchValueError is raised.
        If the key does not exist in the Metrics object, a KeyError is raised.
        If the key does not contain a MetricDefinition object, a KeyError is raised.
        :param name: The key to delete.
        :raises SimpleBenchTypeError: If the key is not a string.
        :raises SimpleBenchValueError: If the key does not match the regex pattern for a metric key.
        :raises KeyError: If the key does not exist in the Metrics object or does not contain a MetricDefinition object.
        """
        if name not in self:
            raise KeyError(name)
        delattr(self, name)

    def __contains__(self, name: Any) -> bool:
        """Return True if the key is a valid metric key and exists in the Metrics object
        and contains a MetricDefinition object.

        :param name: The key to check.
        :return: True if the key is a valid metric key and exists in the Metrics object
            and contains a MetricDefinition object."""
        if not self._is_valid_key_name(name):
            return False
        if not hasattr(self, name):
            return False
        return isinstance(getattr(self, name), Metric)

    def __iter__(self) -> Iterator[str]:
        for key, value in self.__dict__.items():
            if self._is_valid_key_name(key) and isinstance(value, Metric):
                yield key

    def __len__(self) -> int:
        return sum(1 for _ in self)
