"""Container for the results of a single benchmark test."""
from copy import copy
from typing import Any

import simplebench.report.versions.v1 as reports
from simplebench.metrics import Metric, MetricCategory
from simplebench.simplebench_types import Extras, Iterations, MetricsTimers, Values, VariationMarks

from . import _validate
from .metrics import Stats


class Results:
    """Immutable Container for the results of a single benchmark test pass.

    The Results class holds all relevant information about a benchmark test's execution and its outcomes.
    It is used to store the results of a benchmark run for a specific case and combination of parameters.

    It is shallow immutable after creation; its properties cannot be modified.

    Because the types of things stored in extras are not completely controlled by SimpleBench,
    it is not possible to guarantee deep immutability of the contents of the extras property.

    :ivar group: The reporting group to which the benchmark case belongs. (read only)
    :vartype group: str
    :ivar title: The name of the benchmark case. (read only)
    :vartype title: str
    :ivar description: A brief description of the benchmark case. (read only)
    :vartype description: str
    :ivar n: The n weighting the benchmark assigned to the iteration for purposes of Big O analysis. (read only)
    :vartype n: float
    :ivar rounds: The number of rounds in the benchmark case. (read only)
    :vartype rounds: int
    :ivar iterations: A dictionary of Value instances representing each iteration of the benchmark. (read only)
    :vartype iterations: Iterations
    :ivar metrics_timers: A dictionary mapping Metrics to their associated timer names. (read only)
    :vartype metrics_timers: MetricsTimers
    :ivar variation_marks: A dictionary of variation marks used to identify the benchmark variation. (read only)
    :vartype variation_marks: VariationMarks
    :ivar extra_info: Additional information about the benchmark run. This is a
        read-only property that returns a mapping proxy to prevent external mutation. (read only)
    :vartype extra_info: Extras
    """

    _skip_slots = set(['_repr_cache', '_results_info_cache'])
    """Slots to skip for pickling because they can be recomputed on demand"""

    __slots__ = (
        '_group',
        '_title',
        '_description',
        '_n',
        '_rounds',
        '_iterations',
        '_metrics_timers',
        '_variation_marks',
        '_extra_info',
        '_repr_cache',
        '_results_info_cache',
    )

    def __init__(
        self,
        *,
        group: str,
        title: str,
        description: str,
        n: float,
        rounds: int,
        iterations: Iterations,
        metrics_timers: MetricsTimers,
        variation_marks: VariationMarks | None = None,
        extra_info: Extras,
    ) -> None:
        """Initialize a Results object.

        :param group: The reporting group to which the benchmark case belongs.
        :type group: str
        :param title: The name of the benchmark case.
        :type title: str
        :param description: A brief description of the benchmark case.
        :type description: str
        :param n: The O() complexity analysis size/weighting.
        :type n: float
        :param rounds: The number of rounds the benchmark ran per iteration.
        :type rounds: int
        :param iterations: A mapping of Metrics to Values for the benchmark.
        :type iterations: Iterations
        :param metrics_timers: A mapping of Metrics to their associated timer names.
        :type metrics_timers: MetricsTimers
        :param variation_marks: A dictionary of variation marks used to identify
            the benchmark variation. Defaults to :obj:`None`, which results in an empty dictionary.
        :type variation_marks: VariationMarks | None, optional
        :param Optional[Mapping[str, Any]] extra_info: Any extra information to include in the benchmark results.
            Defaults to {}.
        :raises SimpleBenchTypeError: If any of the arguments are of incorrect type.
        :raises SimpleBenchValueError: If any of the arguments have invalid values.
        """
        self._group: str = _validate.group(group)
        self._title: str = _validate.title(title)
        self._description: str = _validate.description(description)
        self._n: float = _validate.n(n)
        self._rounds: int = _validate.rounds(rounds)
        self._iterations: Iterations = _validate.iterations(iterations)
        self._metrics_timers: MetricsTimers = _validate.metrics_timers(metrics_timers)
        self._variation_marks: VariationMarks = _validate.variation_marks(variation_marks)
        self._extra_info = _validate.extra_info(extra_info)
        self._repr_cache: str | None = None  # cache for __repr__

    @property
    def group(self) -> str:
        """The reporting group to which the benchmark case belongs.

        :return: The reporting group that the results belong to.
        :rtype: str
        """
        return self._group

    @property
    def title(self) -> str:
        """The name of the benchmark case."""
        return self._title

    @property
    def description(self) -> str:
        """A brief description of the benchmark case."""
        return self._description

    @property
    def n(self) -> float:
        """The O() complexity analysis size/weighting."""
        return self._n

    @property
    def iterations(self) -> Iterations:
        """The iterations from the benchmark run."""
        return self._iterations

    @property
    def rounds(self) -> int:
        """The number of rounds the benchmark ran per iteration."""
        return self._rounds

    @property
    def variation_marks(self) -> VariationMarks:
        """A dictionary of variation marks used to identify the benchmark variation.

        :returns: A read-only mapping of variation mark names to their values.
        """
        return self._variation_marks

    @property
    def extra_info(self) -> Extras:
        """Additional information about the benchmark run.

        Returns a read-only mapping to mitigate external mutation.
        """
        return self._extra_info

    def stats(self, metric: Metric) -> Stats:
        """Returns the statistical summary of the benchmark results for the given metric.

        The statistical summary includes metrics such as mean, median, standard deviation, etc.

        The returned Stats object is cached for efficiency.

        :param Metric metric: The metric of the results to return. Must be a registered metric.
        :return Stats: The statistical summary of the benchmark results.
        """
        _validate.belongs_to_metric_category(metric, MetricCategory.STATISTICAL)
        timer = self._metrics_timers.get(metric)
        return Stats(metric=metric, rounds=self.rounds, data=self.iterations[metric], timer=timer)

    def sum(self, metric: Metric) -> float:
        """Returns the cumulative sum of the raw benchmark results for the given metric.

        The cumulative sum is the total of all raw data points for the specified metric.

        The returned sum is cached for efficiency.

        :param Metric metric: The metric of the results to return. Must be a registered metric.
        :return float: The cumulative sum of the benchmark results.
        """
        _validate.belongs_to_metric_category(metric, MetricCategory.CUMULATIVE)
        return sum(self.iterations[metric])

    def raw(self, metric: Metric) -> Values:
        """Returns the raw data point values of the benchmark results for the given metric.

        :param Metric metric: The metric of the results to return. Must be a registered metric.
        :return Values: The raw data of the benchmark results as a Values instance.
        """
        _validate.belongs_to_metric_category(metric, MetricCategory.RAW)
        return self._iterations[metric]

    def results_metric(self, metric: Metric) -> Values:
        """Returns the requested metric of the benchmark results.

        :param Metric metric: The metric of the results to return. Must be a registered metric.

        :return Values: The requested metric values from the benchmark results.
        """
        _validate.metric(metric)
        return self.iterations[metric]

    def stats_block(self, metric: Metric) -> reports.StatsBlock:
        """Returns the StatsBlock representation of the Stats for the given metric.

        :param Metric metric: The metric of the results to return. Must be a registered metric.
        :param bool full_data: Whether to include the full data set in the StatsBlock. Defaults to False.

        :return reports.StatsBlock: The StatsBlock representation of the Stats for the given metric.
        """
        _validate.metric(metric)
        stats_instance: Stats = self.stats(metric)
        return stats_instance.stats_block()

    def sum_value_block(self, metric: Metric) -> reports.ValueBlock:
        """Returns the ValueBlock representation of the sum for the given metric.

        :param Metric metric: The metric of the results to return. Must be a registered metric.

        :return ValueBlock: The ValueBlock representation of the sum for the given metric.
        """
        _validate.metric(metric)
        total_sum: float = self.sum(metric)
        return reports.ValueBlock(
            semantic_type=metric.metric_type.semantic_type,
            timer=None,
            unit=metric.metric_type.unit,
            scale=metric.metric_type.scale,
            value=total_sum,
        )

    def raw_block(self, metric: Metric) -> reports.RawDataBlock:
        """Returns the RawDataBlock representation of the raw data for the given metric.

        :param metric: The metric of the results to return. Must be a registered metric.
        :type: Metric
        :return: The RawDataBlock representation of the raw data for the given metric.
        :rtype: reports.RawDataBlock
        """
        _validate.metric(metric)
        raw_data: Values = self.raw(metric)
        return reports.RawDataBlock(
            name=metric.label,
            description=metric.description,
            semantic_type=metric.metric_type.semantic_type,
            timer=None,
            rounds=self.rounds,
            unit=metric.metric_type.unit,
            scale=metric.metric_type.scale,
            data=raw_data,
        )

    def results_info(self) -> reports.ResultsInfo:
        """Returns a summary of the benchmark results.

        :return: A :class:`ResultsInfo` object containing the summary of the benchmark results.
        :rtype: reports.ResultsInfo
        """
        if self._results_info_cache is None:
            metrics: dict[str, reports.MetricItem] = {}
            for metric in self.iterations:
                match metric.metric_type:
                    case MetricCategory.STATISTICAL:
                        metrics[metric.label] = self.stats_block(metric)
                    case MetricCategory.CUMULATIVE:
                        metrics[metric.label] = self.sum_value_block(metric)
                    case MetricCategory.RAW:
                        metrics[metric.label] = self.raw_block(metric)

            self._results_info_cache = reports.ResultsInfo(
                group=self.group,
                title=self.title,
                description=self.description,
                n=self.n,
                variation_marks=self.variation_marks,
                metrics=reports.MetricsObject(metrics),
                extra_info=self.extra_info,
            )
        return self._results_info_cache

    def __repr__(self) -> str:
        """Return a string representation of the Results object.

        :return: The string representation of the Results object.
        :rtype: str
        """
        if self._repr_cache is None:
            self._repr_cache = self._generate_repr()
        return self._repr_cache

    def _generate_repr(self) -> str:
        """Generate the string representation of the Results object.

        :return: String representation of the Results instance.
        :rtype: str
        """
        return (
            f'{self.__class__.__name__}('
            f'group={self.group!r}, '
            f'title={self.title!r}, '
            f'description={self.description!r}, '
            f'n={self.n!r}, '
            f'variation_marks={self.variation_marks!r}, '
            f'iterations={self.iterations!r}, '
            f'rounds={self.rounds!r}, '
            f'extra_info={self.extra_info!r})'
        )

    def __getstate__(self) -> tuple[dict[str, Any] | None, tuple[Any, ...]]:
        """Prepare the object's state for pickling, prioritizing size.

        This method ensures that the pickled representation of the Results
        is as compact as possible. It achieves this by skipping all
        cached data that can be recomputed on demand.

        This prioritizes a small pickled size and fast subsequent unpickling over
        preserving the lazy-evaluation state for reports across serialization.

        :return: A state tuple for pickling.
        :rtype: tuple[dict[str, Any] | None, tuple[Any, ...]]
        """
        # sweep all slots, skipping the slots used for cached values
        # that can be recomputed after being unpickled
        slot_values: list[Any] = []
        for slot in self.__slots__:
            attr_name = slot.lstrip('_')
            if attr_name not in self._skip_slots:
                slot_values.append(getattr(self, attr_name))
            else:
                slot_values.append(None)

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
            # Use object.__setattr__ to bypass our immutable setters.
            object.__setattr__(self, slot, value)

    def __deepcopy__(self, memo: dict[int, Any]) -> 'Results':
        """Return a shallow copy of the instance as an optimized deep copy.

        Since the ResultsInfo instance is immutable and composed of immutable components,
        a shallow copy is functionally identical to a deep copy. This method overrides
        the default `copy.deepcopy` behavior to perform a more efficient shallow copy instead.

        :param memo: The memoization dictionary used by `copy.deepcopy`.
                     It is not used in this optimized implementation.
        :return ResultsInfo: A new, shallow-copied instance of the ResultsInfo.
        """
        # because the ResultsInfo is immutable, we can return a copy of self
        # instead of performing a full deep copy.
        return copy(self)

