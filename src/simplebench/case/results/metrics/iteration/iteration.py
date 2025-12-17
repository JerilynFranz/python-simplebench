"""Iteration class"""
from functools import lru_cache
from typing import Sequence

from simplebench.case.results.metrics import Value
from simplebench.exceptions import SimpleBenchTypeError
from simplebench.metric import Metric, metrics_registry

from ._error_tags import _IterationErrorTag


class Iteration:
    """Immutable container for the results of a single benchmark iteration.

    An iteration represents a single run of a benchmarked action (a run may consist
    of multiple rounds and a full benchmark consists of multiple iterations).

    It holds the measurement results of a single iteration of a benchmarked action.

    The n-weight represents the O(n) type complexity of the action being benchmarked.
    For example, if the action processes a list of size n, then the n-weight would be n.

    This allows data analysis tools to better understand the performance characteristics of the action
    being benchmarked when the benchmark data is exported, although it is not used directly in
    any calculations by SimpleBench itself currently.

    :ivar values: A dictionary of metrics and their values for the iteration. (read only)
    :vartype values: tuple[Value, ...] (read only)
    """
    __slots__ = ('_values', '_index')

    def __init__(self, values: Sequence[Value]) -> None:
        """Initialize an Iteration instance.

        :param values: A sequence of Value tuples representing the metrics and their values for the iteration.
        :raises SimpleBenchTypeError: If the values Sequence is not valid.
        :raises SimpleBenchValueError: If the values Sequence is empty or contains invalid metrics.
        """
        self._values: tuple[Value, ...] = self._validate_values(values)
        """The values of the metrics for the iteration."""

        # The index is used to quickly look up the value of a metric in the iteration.
        # It is rebuilt from the validated values to ensure immutability and consistency of the iteration.
        self._index: dict[Metric, float] = dict(self._values)
        """The index is used to quickly look up the value of a metric in the iteration."""

    def _validate_values(self, values: Sequence[Value]) -> tuple[Value, ...]:
        """Validate the valueand return a sorted tuple of tuples.

        The returned tuple is a sorted tuple of Value tuples, where each tuple contains a metric and
        its corresponding value as a float. The sorting is done to ensure that the order of the metrics
        is consistent and predictable for equality checks and hashing.

        The validation checks include:
        - The values dictionary must contain at least one metric and its corresponding value.
        - The keys must be of type Metric and the values must be integers or floats.
        - The values dictionary must not be empty.

        :param values: A dictionary of metrics and their values for the iteration.
        :return: The validated values dictionary.
        """
        if isinstance(values, Sequence):
            # v[0] is the Metric, v[1] is the value
            # referencing by index to avoid unpacking overhead in the loop
            if all(isinstance(v, Value) and v[0] in metrics_registry for v in values):
                return tuple(sorted(values))
            raise SimpleBenchTypeError(
                'An item in sequence was not a Value tuple. Must be a sequence of Value tuples.',
                tag=_IterationErrorTag.VALUES_ARG_INVALID_SEQUENCE_TYPE
            )
        raise SimpleBenchTypeError(
            f'Invalid values argument type: {type(values)}. Must be a sequence of Value tuples.',
            tag=_IterationErrorTag.VALUES_ARG_INVALID_SEQUENCE_TYPE
        )

    def __eq__(self, other: object) -> bool:
        """Check equality between two Iteration instances.
        :param other: The other Iteration instance to compare with.
        :return: True if the two Iteration instances are equal, False otherwise.
        """
        return isinstance(other, Iteration) and self._values == other._values

    def __hash__(self) -> int:
        """Return a hash of the Iteration instance values."""
        return hash(self._values)

    @property
    def values(self) -> tuple[Value, ...]:
        """The values of the metrics for the iteration.

        The values are returned as a tuple of tuples, where each inner tuple contains a metric and
        its corresponding value as a float.
        """
        return self._values

    def metric(self, metric: Metric) -> float:
        """Returns the requested metric value for the iteration.

        :param metric: The metric of the results to return. Must be a registered metric.
        :return: The requested metric of the benchmark results.
        :raises SimpleBenchTypeError: If the metric is not a registered metric.
        :raises KeyError: If the metric is not found in the iteration.
        """
        if not isinstance(metric, Metric):
            raise SimpleBenchTypeError(
                f'Invalid metric type: {type(metric)}. Must be of type MetricDefinition.',
                tag=_IterationErrorTag.METRIC_INVALID_METRIC_ARG_TYPE
            )
        return self._index[metric]

    @lru_cache(maxsize=1)
    def as_dict(self) -> dict[str, float]:
        """Return the Iteration instance as a dictionary.

        The values are represented as a dictionary of metric labels and their corresponding values.
        The metric labels are used to make the dictionary more readable and to avoid confusion
        with the metric objects themselves.

        :return: A dictionary representation of the Iteration instance.
        """
        return {m.label: v for m, v in self._values}

    def __repr__(self) -> str:
        """Return a string representation of the Iteration instance.

        The values are represented as a dictionary of metric labels and their corresponding values.
        The metric labels are used to make the string representation more readable and to avoid
        confusion with the metric objects themselves. They are also used to ensure that the string
        representation is consistent across different runs of the benchmark.
        """
        values_repr = {repr(m.label): v for m, v in self._values}
        return f"Iteration(f'values={values_repr})"
