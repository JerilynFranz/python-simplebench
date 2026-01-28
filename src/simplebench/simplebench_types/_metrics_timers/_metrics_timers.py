"""""""""Mapping containers for mappings of Metrics to the names of their timers or None.

This is an immutable mapping of Metrics to the names of their timers or None.
"""

from collections.abc import Iterator, Mapping

from typechecked import Immutable

from simplebench.exceptions import SimpleBenchKeyError, SimpleBenchTypeError
from simplebench.metrics import Metric

from ._error_tags import _MetricsTimersErrorTag


class MetricsTimers(Mapping[Metric, str | None], Immutable):
    """Mapping container for Values collections of iteration results used in SimpleBench.
    Maps Metrics to their corresponding collections of Values for a specific iteration.
    """
    __slots__ = ("__metrics_timers",)

    def __init__(self, metrics_timers: Mapping[Metric, str | None]) -> None:
        """Construct an Iterations instance.

        :param metrics_timers: The mapping of Metrics to the names of their timers or None.
        :type metrics_timers: Mapping[Metric, str | None]
        :raises SimpleBenchTypeError: If the metrics_timers argument is not a mapping of Metrics
            to :class:`str` or :obj:`None`
        :raises SimpleBenchTypeError: If any keys are not of type :class:`Metric`.
        :raises SimpleBenchTypeError: If any values are not of type :class:`str` or :obj:`None`.
        """
        if not isinstance(metrics_timers, Mapping):
            raise SimpleBenchTypeError(
                f"Invalid metrics_timers: {metrics_timers}. Must be a mapping of Metrics to str or None.",
                tag=_MetricsTimersErrorTag.METRICS_TIMERS_INVALID_ARG_TYPE,
            )
        if not all(isinstance(key, Metric) for key in metrics_timers.keys()):
            raise SimpleBenchTypeError(
                "All keys in metrics_timers must be Metrics.",
                tag=_MetricsTimersErrorTag.METRICS_TIMERS_INVALID_ARG_KEY_TYPE,
            )
        if not all(isinstance(value, (str, type(None))) for value in metrics_timers.values()):
            raise SimpleBenchTypeError(
                "All values in metrics_timers must be str or None.",
                tag=_MetricsTimersErrorTag.METRICS_TIMERS_INVALID_ARG_VALUE_TYPE,
            )
        # Shallow copy is sufficient since Metric and Values are immutable
        self._metrics_timers: dict[Metric, str | None] = dict(metrics_timers)

    def __getitem__(self, key: Metric) -> str | None:
        """Get the values for the given metric.

        :param key: The metric.
        :type key: Metric
        :returns: The corresponding Values.
        :rtype: Values
        :raises KeyError: If the key is not found.
        """
        try:
            return self._metrics_timers[key]
        except KeyError as exc:
            raise SimpleBenchKeyError(
                f"Metric {key!r} not found in MetricsTimers.",
                tag=_MetricsTimersErrorTag.METRICS_TIMERS_KEY_ERROR) from exc

    def __contains__(self, key: object) -> bool:
        """Check if the MetricsTimers contains the given key.

        :param key: The key to check.
        :type key: object
        :returns: True if the key is in the MetricsTimers, False otherwise.
        :rtype: bool
        """
        return key in self._metrics_timers

    def __setitem__(self, key: Metric, value: str | None) -> None:
        """Raise an error since MetricsTimers is immutable.

        :param key: The key to set.
        :type key: Metric
        :param value: The value to set.
        :type value: str | None
        :raises SimpleBenchTypeError: Always, since MetricsTimers is immutable.
        """
        raise SimpleBenchTypeError(
            "MetricsTimers is immutable and does not support item assignment.",
            tag=_MetricsTimersErrorTag.METRICS_TIMERS_IMMUTABLE,
            )

    def __iter__(self) -> Iterator[Metric]:
        """Iterate over the iteration Metric keys.

        :returns Iterator[Metric]: An iterator over the :class:`Metric` keys
        """
        return self._metrics_timers.__iter__()

    def __len__(self) -> int:
        """Get the number of metrics.

        :returns int: The number of metrics.
        """
        return len(self._metrics_timers)

    def __repr__(self) -> str:
        """Get the string representation of the MetricsTimers.

        :returns str: The string representation.
        """
        return f"MetricsTimers({dict(self._metrics_timers)!r})"

    def __hash__(self) -> int:
        """Get the hash of the MetricsTimers instance.
        :returns int: The hash value.
        """
        items = ((key, self._metrics_timers[key]) for key in sorted(self._metrics_timers.keys()))
        return hash(frozenset(items))

    def __eq__(self, other: object) -> bool:
        """Check equality with another MetricsTimers instance.

        :param object other: The other object to compare.
        :returns bool: True if equal, False otherwise.
        """
        if not isinstance(other, MetricsTimers):
            return False
        return self._metrics_timers == other._metrics_timers
