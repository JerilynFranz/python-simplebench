"""Mapping containers for collections of variation marks used in SimpleBench.

This is an immutable mapping of variation field names to their corresponding collections of Marks
defining multiple variations.
"""

from collections.abc import Iterator, Mapping

from typechecked import Immutable

from simplebench.exceptions import SimpleBenchKeyError, SimpleBenchTypeError
from simplebench.metrics import Metric
from simplebench.simplebench_types import Mark, Values
from simplebench.simplebench_types._variations._kwargs_variations._error_tags import _KWArgsVariationsErrorTag

from ._error_tags import _IterationsErrorTag


class Iterations(Mapping[Metric, Values], Immutable):
    """Mapping container for Values collections of iteration results used in SimpleBench.
    Maps Metrics to their corresponding collections of Values for a specific iteration.
    """
    __slots__ = ("__iterations",)

    def __init__(self, iterations: Mapping[Metric, Values]) -> None:
        """Construct an Iterations instance.

        :param iterations: The mapping of Metrics to their Values collections.
        :type iterations: Mapping[Metric, Values]
        :raises SimpleBenchTypeError: If the iterations argument is not a mapping of Metrics
            to :class:`Values`
        :raises SimpleBenchTypeError: If any keys are not of type :class:`Metric`.
        :raises SimpleBenchTypeError: If any values are not of type :class:`Values`.
        """
        if not isinstance(iterations, Mapping):
            raise SimpleBenchTypeError(
                f"Invalid iterations: {iterations}. Must be a mapping of Metrics to Values.",
                tag=_IterationsErrorTag.ITERATIONS_INVALID_ARG_TYPE,
            )
        if not all(isinstance(key, Metric) for key in iterations.keys()):
            raise SimpleBenchTypeError(
                "All keys in iterations must be Metrics.",
                tag=_IterationsErrorTag.ITERATIONS_INVALID_ARG_KEY_TYPE,
            )
        if not all(isinstance(values, Values) for values in iterations.values()):
            raise SimpleBenchTypeError(
                "All values in iterations must be Values.",
                tag=_IterationsErrorTag.ITERATIONS_INVALID_ARG_VALUE_TYPE,
            )
        # Shallow copy is sufficient since Metric and Values are immutable
        self._iterations: dict[Metric, Values] = dict(iterations)

    def __getitem__(self, key: Metric) -> Values:
        """Get the values for the given metric.

        :param key: The metric.
        :type key: Metric
        :returns: The corresponding Values.
        :rtype: Values
        :raises KeyError: If the key is not found.
        """
        try:
            return self._iterations[key]
        except KeyError as exc:
            raise SimpleBenchKeyError(
                f"Metric {key!r} not found in Iterations.",
                tag=_IterationsErrorTag.ITERATIONS_KEY_ERROR) from exc

    def __contains__(self, key: object) -> bool:
        """Check if the Iterations contains the given key.

        :param key: The key to check.
        :type key: object
        :returns: True if the key is in the Iterations, False otherwise.
        :rtype: bool
        """
        return key in self._iterations

    def __setitem__(self, key: Metric, value: Values) -> None:
        """Raise an error since Iterations is immutable.

        :param key: The key to set.
        :type key: Metric
        :param value: The value to set.
        :type value: Values
        :raises SimpleBenchTypeError: Always, since Iterations is immutable.
        """
        raise SimpleBenchTypeError(
            "Iterations is immutable and does not support item assignment.",
            tag=_IterationsErrorTag.ITERATIONS_IMMUTABLE,
            )

    def __iter__(self) -> Iterator[Metric]:
        """Iterate over the iteration Metric keys.

        :returns Iterator[Metric]: An iterator over the :class:`Metric` keys
        """
        return self._iterations.__iter__()

    def __len__(self) -> int:
        """Get the number of metrics.

        :returns int: The number of metrics.
        """
        return len(self._iterations)

    def __repr__(self) -> str:
        """Get the string representation of the Iterations.

        .. warning:: THIS IS FOR DEBUGGING AND TESTING PURPOSES ONLY AND WILL PROBABLY BE HUGE.

        :returns str: The string representation.
        """
        return f"Iterations({dict(self._iterations)!r})"

    def __hash__(self) -> int:
        """Get the hash of the Iterations instance.

        :returns int: The hash value.
        """
        items = ((key, self._iterations[key]) for key in sorted(self._iterations.keys()))
        return hash(frozenset(items))

    def __eq__(self, other: object) -> bool:
        """Check equality with another Iterations instance.

        :param object other: The other object to compare.
        :returns bool: True if equal, False otherwise.
        """
        if not isinstance(other, Iterations):
            return False
        return self._iterations == other._iterations
