"""Definition for a Metrics object for the simplebench library."""
import hashlib
from collections.abc import Iterable, Iterator, Mapping, Sequence, Set
from typing import Any

from simplebench.exceptions import SimpleBenchKeyError, SimpleBenchTypeError
from simplebench.report._error_tags import _MetricsErrorTag
from simplebench.report.base import ReportElement
from simplebench.simplebench_types import CoreDataMapping, Never

from ..metric import Metric
from . import _validate

__all__: list[str] = []


class Metrics(ReportElement, Mapping[str, Metric]):
    """Definition for a Metrics object, which is a Mapping of str to Metric instances.
    """

    __slots__ = ('_dict', '_hash_id')

    def __init__(self, __metrics: 'Iterable[Metric] | Metrics') -> None:
        """Initialize a Metrics instance.

        The constructor accepts an iterable of Metric objects
        or another Metrics object to initialize this Metrics instance with.
        """
        metrics = _validate.metrics(__metrics)
        self._dict = {metric.label: metric for metric in metrics}
        self._hash_id = self._compute_hash_id()

    def _compute_hash_id(self) -> str:
        """Compute the hash ID for the Metrics object based on ordered hash IDs of the individual
        Metric objects it contains.

        The hash ID is computed by creating a tuple of the hash IDs of the individual Metric objects,
        and then hashing that tuple to produce a unique identifier for the combination of metrics.

        :return: The computed hash ID for the Metrics object.
        :rtype: str
        """
        metric_hash_ids: tuple[str, ...] = tuple(metric.hash_id for metric in sorted(
            self._dict.values(), key=lambda m: m.hash_id))
        hash_input = '\x00'.join(metric_hash_ids).encode('utf-8')
        return hashlib.sha256(hash_input).hexdigest()

    @classmethod
    def from_dict(cls, data: Mapping[str, str | float | int]) -> 'Metrics':
        """Initialize the Metrics instance from a dictionary.

        :param data: The dictionary containing the metric type data.
        :type data: Mapping[str, str | float | int]
        :return: The initialized Metrics instance.
        :rtype: Metrics
        :raises SimpleBenchTypeError: If the input data is not a mapping or if the
            values in the mapping are not valid for initializing Metric instances.
        :raises SimpleBenchKeyError: If the keys in the mapping do not match the '
            'label' fields of the corresponding Metric instances.
        """
        if not isinstance(data, Mapping):
            raise SimpleBenchTypeError(
                f"Expected a mapping to initialize Metrics, got {type(data).__name__}",
                tag=_MetricsErrorTag.INVALID_METRICS_FIELD_TYPE,
            )
        metrics_list: list[Metric] = []
        for key, value in data.items():
            if isinstance(value, Mapping):
                metric = Metric.from_dict(value)
                if metric.label != key:
                    raise SimpleBenchKeyError(
                        f"Key '{key}' in metrics mapping does not match the "
                        f"'label' field of the Metric: '{metric.label}'",
                        tag=_MetricsErrorTag.MISMATCHED_KEY,
                    )
                metrics_list.append(metric)
            else:
                raise SimpleBenchTypeError(
                    "Expected a mapping of str to Metric data mappings, but found "
                    f"value of type {type(value).__name__} for key '{key}'",
                    tag=_MetricsErrorTag.INVALID_METRICS_FIELD_TYPE,
                )
        return cls(metrics_list)

    def to_dict(self) -> CoreDataMapping:
        """Convert the Metrics instance to a dictionary.

        Returns an immutable dictionary representation of the Metrics instance.
        It is actually a :class:`~simplebench.simplebench_types.CoreDataMapping` instance.

        :return: A dictionary representation of the Metrics instance.
        :rtype: CoreDataMapping
        """
        output_dict = {metric.label: metric.to_dict() for metric in self._dict.values()}
        return CoreDataMapping(output_dict)  # type: ignore

    def for_json(self) -> CoreDataMapping:
        """Convert the Metrics instance to a JSON-serializable dictionary.

        This is the same as `to_dict` since the output of `to_dict` is already JSON-serializable.

        :return: A JSON-serializable dictionary representation of the Metrics instance.
        :rtype: CoreDataMapping
        """
        return self.to_dict()

    def as_json(self) -> str:
        """Convert the Metrics instance to a JSON string.

        :return: A JSON string representation of the Metrics instance.
        :rtype: str
        """
        return self.to_dict().as_json()  # type: ignore

    @property
    def hash_id(self) -> str:
        """The hash ID of the Metrics instance."""
        return self._hash_id

    def __repr__(self) -> str:
        """Get the string representation of the Metrics instance.

        :return: The string representation of the Metrics instance.
        :rtype: str
        """
        calling_args = tuple(self._dict.values())
        return f'{self.__class__.__name__}({calling_args!r})'

    def __hash__(self) -> int:
        """Get the hash of the Metrics instance.

        :return: The hash value.
        """
        return hash(self.hash_id)

    def __eq__(self, other: object) -> bool:
        """Check equality between two Metrics instances.

        :param other: The other object to compare.
        :return: True if equal, False otherwise.
        """
        if not isinstance(other, Metrics):
            raise SimpleBenchTypeError(
                f'Cannot compare Metrics with {type(other).__name__!r}',
                tag=_MetricsErrorTag.OPERAND_TYPE_ERROR)
        return self.hash_id == other.hash_id

    def __copy__(self) -> 'Metrics':
        """Create a copy of the Metrics instance.

        It returns self since the Metrics instance is immutable and can be shared safely.

        :return: The Metrics instance.
        :rtype: Metrics
        """
        return self

    def __deepcopy__(self, memo: dict[int, Any]) -> 'Metrics':
        """Create a deep copy of the Metrics instance.

        It returns self since the Metrics instance is immutable and can be shared safely.

        :return: The Metrics instance.
        :rtype: Metrics
        """
        return self

    def __getitem__(self, key: str) -> Metric:
        """Get the Metric for the given key. The key is the label of the Metric.

        :param key: The key.
        :type key: str
        :returns: The corresponding Metric.
        :rtype: Metric
        :raises SimpleBenchKeyError: If the key is not found.
        """
        if key in self._dict:
            return self._dict[key]
        raise SimpleBenchKeyError(
            f'Key "{key}" not found in Metrics object',
            tag=_MetricsErrorTag.METRIC_NOT_FOUND)

    def get(self, key: str) -> Metric:  # type: ignore[override]
        """Get the Metric for the given key, or raise an error if the key is not found.

        It does not support a default value since Metric is immutable and all values
        will always be Metric objects and unique.

        If a key is accessed that is not defined, it indicates a bug in the code
        that needs to be fixed, rather than a case where a default value would be appropriate.

        :param key: The key (metric label).
        :type key: str
        :returns: The corresponding Metric.
        :rtype: Metric
        """
        return self.__getitem__(key)

    def __setitem__(self, key: str, value: Never) -> None:
        """Always raises an error since Metrics is immutable and does
        not support item assignment.

        :param key: The key to set.
        :type key: str
        :param value: The value to set.
        :type value: Never
        :raises SimpleBenchTypeError: Always, since Metrics is immutable.
        """
        raise SimpleBenchTypeError(
            'Metrics is immutable and does not support item assignment.',
            tag=_MetricsErrorTag.MAPPING_IMMUTABLE)

    def __add__(self, other: 'Metrics | Metric', allow_duplicates: bool = False) -> 'Metrics':
        """Create a new Metrics object by combining two Metrics objects
        or adding a single Metric object. (The "+" operator is used for this operation.)

        This method allows for combining the metrics from two Metrics objects or adding a single Metric
        to a Metrics object. By default, it does not allow duplicate metric labels and will
        raise an error if duplicates are found.

        However, if the `allow_duplicates` parameter is set to True, it will allow duplicate
        metric labels and will not raise an error if duplicates are found (last one wins).
        In this case, the resulting Metrics object will contain all metrics from both objects,
        and if there are duplicate labels, the metric from the `other` object will overwrite
        the one from this object.

        This is not exposed behavior for the "+" operator, but is used by the `__or__` method
        to implement the union operation which allows duplicates.

        :param other: The Metrics or Metric object to add.
        :type other: Metrics or Metric
        :param allow_duplicates: (default=False) Whether to allow duplicate metric labels.
        :type allow_duplicates: bool
        :return: A new Metrics object containing the combined metrics.
        :rtype: Metrics
        :raises SimpleBenchTypeError: If the other object is not a Metrics instance or a Metric instance.
        :raises SimpleBenchKeyError: If there are duplicate metric labels when combining unless
            allow_duplicates is True.
        """
        if not isinstance(other, (Metrics, Metric)):
            raise SimpleBenchTypeError(
                'Can only add Metrics or Metric objects.',
                tag=_MetricsErrorTag.INVALID_ADDEND_TYPE
            )
        if isinstance(other, Metric):
            new_dict = dict(self._dict)
            label = other.label
            if label in new_dict and not allow_duplicates:
                raise SimpleBenchKeyError(
                    f'Duplicate metric label "{label}" found when adding Metric to Metrics object',
                    tag=_MetricsErrorTag.DUPLICATE_METRIC_LABEL)
            new_dict.update({other.label: other})
            return Metrics(new_dict.values())
        else:
            new_dict = dict(self._dict)
            for metric in other._dict.values():
                label = metric.label
                if label in new_dict and not allow_duplicates:
                    raise SimpleBenchKeyError(
                        f'Duplicate metric label "{label}" found when adding Metrics to Metrics object',
                        tag=_MetricsErrorTag.DUPLICATE_METRIC_LABEL)
                new_dict.update({label: metric})
            return Metrics(new_dict.values())

    def __sub__(self, other: 'Metrics | Metric | Sequence[str] | Set[str]') -> 'Metrics':
        """Create a new Metrics object by subtracting another Metrics or Metric object's keys
        or a sequence or set of string label identifiers.

        The new object will contain all metrics from this object, except for those
        whose keys are also present in the `other` object.

        - Subtracting a single Metric object will remove the metric with the same label as that
            Metric from the new object.
        - Subtracting a Metrics object will remove all metrics with labels that are present in the
            `other` Metrics object from the new object.
        - Subtracting a sequence or set of string label identifiers will remove all metrics with
            labels that are present in the sequence or set from the new object.

        Subtracting a non-existent key will simply be ignored and will not raise an error.

        :param other: The Metrics or Metric object or a sequence or set of string label identifiers
            whose keys will be subtracted.
        :return: A new Metrics object with the subtracted metrics.
        :raises SimpleBenchTypeError: If the other object is not a Metrics instance or
            a Metric instance or a sequence or set of string label identifiers.
        """
        if isinstance(other, (str, bytes)):
            raise SimpleBenchTypeError(
                'Cannot subtract a string or bytes object from Metrics. Expected a Metrics '
                'or Metric object or a sequence or set of string label identifiers.',
                tag=_MetricsErrorTag.INVALID_SUBTRAHEND_TYPE
            )
        if not isinstance(other, (Metrics, Metric, Sequence, Set)):
            raise SimpleBenchTypeError(
                'Can only subtract Metrics or Metric objects or Sequences or Sets of string label identifiers.',
                tag=_MetricsErrorTag.INVALID_SUBTRAHEND_TYPE
            )

        if isinstance(other, (Sequence, Set)):
            new_dict = dict(self._dict)
            for label in other:
                if not isinstance(label, str):
                    raise SimpleBenchTypeError(
                        'Expected a sequence or set of string label identifiers, but found '
                        f'an item of type {type(label).__name__!r}',
                        tag=_MetricsErrorTag.INVALID_SUBTRAHEND_TYPE
                    )
                if label in new_dict:
                    del new_dict[label]
            return Metrics(new_dict.values())

        # Create an iterable of metrics from `self` that are not in `other`.
        if isinstance(other, Metric):
            metrics_to_keep = (value for key, value in self.items() if key != other.label)
        else:  # Metrics
            metrics_to_keep = (value for key, value in self.items() if key not in other)

        # Return a new Metrics object initialized with the filtered metrics.
        return Metrics(metrics_to_keep)

    def __or__(self, other: 'Metrics') -> 'Metrics':
        """Create a new Metrics object representing the merge/union of this Metrics
        object and another Metrics object. (The "|" operator is used for this operation.)

        It allows duplicates and will not raise an error if duplicates are found.

        :param other: The Metrics object to perform the union with.
        :type other: Metrics
        :return: A new Metrics object representing the union.
        """
        return self.__add__(other, allow_duplicates=True)

    def __and__(self, other: 'Metrics') -> 'Metrics':
        """Create a new Metrics object representing the intersection.

        The new object will contain only the metrics whose keys are present
        in both this object and the `other` object.

        :param other: The Metrics object to intersect with.
        :type other: Metrics
        :return: A new Metrics object representing the intersection.
        :rtype: Metrics
        :raises SimpleBenchTypeError: If the other object is not a Metrics instance.
        """
        if not isinstance(other, Metrics):
            raise SimpleBenchTypeError(
                'Can only intersect with another Metrics object.',
                tag=_MetricsErrorTag.OPERAND_TYPE_ERROR
            )
        intersecting_metrics = (value for key, value in self.items() if key in other)
        return Metrics(intersecting_metrics)

    def __xor__(self, other: 'Metrics') -> 'Metrics':
        """Create a new Metrics object representing the symmetric difference.

        The new object will contain metrics that are in either this object or
        the `other` object, but not in both.

        :param other: The Metrics object to perform the symmetric difference with.
        :type other: Metrics
        :return: A new Metrics object representing the symmetric difference.
        :rtype: Metrics
        :raises SimpleBenchTypeError: If the other object is not a Metrics instance.
        """
        if not isinstance(other, Metrics):
            raise SimpleBenchTypeError(
                'Can only perform symmetric difference with another Metrics object.',
                tag=_MetricsErrorTag.OPERAND_TYPE_ERROR
            )

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

        Not implemented because Metrics is immutable and does not support in-place modification.
        This method will always raise a SimpleBenchTypeError.

        :param other: The Metrics object to add.
        :return: The modified Metrics object.
        :raises SimpleBenchTypeError: Always, since Metrics is immutable and does not support in-place modification.
        """
        raise SimpleBenchTypeError(
            'Metrics objects are immutable and do not support in-place addition.',
            tag=_MetricsErrorTag.MAPPING_IMMUTABLE
        )

    def __isub__(self, other: 'Metrics | Metric') -> 'Metrics':
        """Perform in-place subtraction.

        Not implemented because Metrics is immutable and does not support in-place modification.
        This method will always raise a SimpleBenchTypeError.

        :param other: The Metrics object whose keys will be removed.
        :return: The modified Metrics object.
        :raises SimpleBenchTypeError: Always, since Metrics is immutable and does not support in-place modification.
        """
        raise SimpleBenchTypeError(
            'Metrics objects are immutable and do not support in-place subtraction.',
            tag=_MetricsErrorTag.MAPPING_IMMUTABLE
        )

    def __delitem__(self, name: str) -> None:
        """Delete a mapping value from the Metrics object.

        :param name: The key to delete.
        :type name: str

        :raises SimpleBenchKeyError: Always, since Metrics is immutable and does not support item deletion.
        """
        raise SimpleBenchKeyError(
            f'Cannot delete key "{name}" from Metrics object since it is immutable.',
            tag=_MetricsErrorTag.MAPPING_IMMUTABLE
        )

    def __contains__(self, name: Any) -> bool:
        """Return True if the key exists in the Metrics object.

        :param name: The key to check.
        :type name: str
        :return: True if the key exists in the Metrics object."""
        return name in self._dict

    def __iter__(self) -> Iterator[str]:
        """Return an iterator over the metric keys in the Metrics object.
        :return: An iterator over the metric keys.
        :rtype: Iterator[str]
        """
        yield from self._dict.keys()

    def __len__(self) -> int:
        """Return the number of metrics in the Metrics object.
        :return: The number of metrics.
        :rtype: int
        """
        return len(self._dict)
