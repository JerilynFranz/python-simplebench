"""Container for the results of a single benchmark test."""
from collections.abc import Mapping
from types import MappingProxyType
from typing import Any

import simplebench.report.versions.v1 as reports
from simplebench.metrics import Metric, MetricCategory
from simplebench.simplebench_types import Iterations, Values, VariationMarks

from . import _validate
from .metrics import Stats


class Results:
    """Container for the results of a single benchmark test pass.

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
    :vartype n: int | float
    :ivar rounds: The number of rounds in the benchmark case. (read only)
    :vartype rounds: int
    :ivar iterations: A dictionary of Value instances representing each iteration of
        the benchmark. (read only)
    :vartype iterations: MappingProxyType[Metric, Values]
    :ivar marks: A dictionary of variation marks used to identify the
        benchmark variation. (read only)
    :vartype marks: MappingProxyType[str, tuple[str, ...]]
    :ivar variation_cols: The columns to use for labelling kwarg marks in
        the benchmark. (read only)
    :vartype variation_cols: MappingProxyType[str, str]
    :ivar extra_info: Additional information about the benchmark run. This is a
        read-only property that returns a mapping proxy to prevent external mutation. (read only)
    :vartype extra_info: MappingProxyType[str, Any]
    """

    __slots__ = (
        '_group',
        '_title',
        '_description',
        '_n',
        '_rounds',
        '_iterations',
        '_variation_cols',
        '_variation_marks',
        '_extra_info',
        '_repr_cache',
        '_stats_cache',
        '_sum_cache',
        '_raw_cache',
    )

    def __init__(
        self,  # pylint: disable=too-many-arguments, too-many-locals
        *,
        group: str,
        title: str,
        description: str,
        n: float,
        rounds: int,
        iterations: Iterations,
        variation_marks: VariationMarks | None = None,
        extra_info: Mapping[str, Any] | None = None,
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
        :param variation_marks: A dictionary of variation marks used to identify
            the benchmark variation. Defaults to :obj:`None`, which results in an empty dictionary.
        :type variation_marks: VariationMarks | None, optional
        :param Optional[Mapping[str, Any]] extra_info: Any extra information to include in the benchmark results.
            Defaults to {}.
        :raises SimpleBenchTypeError: If any of the arguments are of incorrect type.
        :raises SimpleBenchValueError: If any of the arguments have invalid values.
        """
        self._stats_cache: dict[Metric, Stats] = {}
        self._sum_cache: dict[Metric, float] = {}
        self._raw_cache: dict[Metric, Values] = {}

        self._group: str = _validate.group(group)
        self._title: str = _validate.title(title)
        self._description: str = _validate.description(description)
        self._n: float = _validate.n(n)
        self._rounds: int = _validate.rounds(rounds)
        self._iterations: Iterations = _validate.iterations(iterations)
        self._variation_marks: VariationMarks = _validate.variation_marks(variation_marks)
        self._extra_info = _validate.extra_info(extra_info)
        self._repr_cache: str | None = None  # cache for __repr__

    @property
    def group(self) -> str:
        """The reporting group to which the benchmark case belongs."""
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
    def iterations(self) -> MappingProxyType[Metric, Values]:
        """The iterations from the benchmark run."""
        return self._iterations

    @property
    def rounds(self) -> int:
        """The number of rounds the benchmark ran per iteration."""
        return self._rounds

    @property
    def variation_cols(self) -> MappingProxyType[str, str]:
        """The columns to use for labelling kwarg variations in the benchmark.

        :returns: A read-only mapping of variation column names to their labels.
        """
        return self._variation_cols

    @property
    def marks(self) -> MappingProxyType[str, tuple[str, ...]]:
        """A dictionary of variation marks used to identify the benchmark variation.

        :returns: A read-only mapping of variation mark names to their values.
        """
        return self._marks

    @property
    def extra_info(self) -> MappingProxyType[str, Any]:
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
        validate.belongs_to_metric_category(metric, MetricCategory.STATISTICAL)
        if metric not in self._stats_cache:
            self._stats_cache[metric] = Stats(metric=metric, rounds=self.rounds, data=self.iterations[metric])
        return self._stats_cache[metric]

    def sum(self, metric: Metric) -> float:
        """Returns the cumulative sum of the raw benchmark results for the given metric.

        The cumulative sum is the total of all raw data points for the specified metric.

        The returned sum is cached for efficiency.

        :param Metric metric: The metric of the results to return. Must be a registered metric.
        :return float: The cumulative sum of the benchmark results.
        """
        validate.belongs_to_metric_category(metric, MetricCategory.CUMULATIVE)
        if metric not in self._sum_cache:
            self._sum_cache[metric] = sum(self.iterations[metric])
        return self._sum_cache[metric]

    def raw(self, metric: Metric) -> Values:
        """Returns the raw data point values of the benchmark results for the given metric.

        :param Metric metric: The metric of the results to return. Must be a registered metric.
        :return Values: The raw data of the benchmark results as a Values instance.
        """
        validate.belongs_to_metric_category(metric, MetricCategory.RAW)
        return self._iterations[metric]

    def results_metric(self, metric: Metric) -> Values:
        """Returns the requested metric of the benchmark results.

        :param Metric metric: The metric of the results to return. Must be a registered metric.

        :return Values: The requested metric values from the benchmark results.
        """
        validate.metric(metric)
        return self.iterations[metric]

    def stats_block(self, metric: Metric, full_data: bool = False) -> reports.StatsBlock:
        """Returns the StatsBlock representation of the Stats for the given metric.

        :param Metric metric: The metric of the results to return. Must be a registered metric.
        :param bool full_data: Whether to include the full data set in the StatsBlock. Defaults to False.

        :return reports.StatsBlock: The StatsBlock representation of the Stats for the given metric.
        """
        validate.metric(metric)
        stats_instance: Stats = self.stats(metric)
        if full_data:
            return stats_instance.stats_block(full_data=True)
        return stats_instance.stats_block(full_data=False)

    def sum_value_block(self, metric: Metric) -> reports.ValueBlock:
        """Returns the ValueBlock representation of the sum for the given metric.

        :param Metric metric: The metric of the results to return. Must be a registered metric.

        :return ValueBlock: The ValueBlock representation of the sum for the given metric.
        """
        validate.metric(metric)
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

        :param Metric metric: The metric of the results to return. Must be a registered metric.
        :return RawDataBlock: The RawDataBlock representation of the raw data for the given metric.
        """
        validate.metric(metric)
        raw_data: Values = self.raw(metric)
        return reports.RawDataBlock(
            semantic_type=metric.metric_type.semantic_type,
            timer=None,
            unit=metric.metric_type.unit,
            scale=metric.metric_type.scale,
            data=raw_data,
        )

    def results_info(self, full_data: bool = False) -> reports.ResultsInfo:
        """Returns a summary of the benchmark results.

        :param full_data: Whether to include the full data set in the summary. Defaults to False.
        :type full_data: bool, optional

        Returns:
            results_info: A ResultsInfo object containing the summary of the benchmark results.
        """
        metrics: dict[str, reports.MetricItem] = {}
        for metric in self.iterations:
            match metric.metric_type:
                case MetricCategory.STATISTICAL:
                    metrics[metric.label] = self.stats_block(metric, full_data=full_data)
                case MetricCategory.CUMULATIVE:
                    metrics[metric.label] = self.sum_value_block(metric)
                case MetricCategory.RAW:
                    metrics[metric.label] = self.raw_block(metric)

        return reports.ResultsInfo(
            group=self.group,
            title=self.title,
            description=self.description,
            n=self.n,
            variation_marks=self.marks,
            metrics=reports.MetricsObject(metrics),
            extra_info=self.extra_info,
        )

    def __repr__(self) -> str:
        """Return a string representation of the Results object.

        :returns str: The string representation of the Results object.
        """
        if self._repr_cache is None:
            self._repr_cache = self._generate_repr()
        return self._repr_cache

    def _generate_repr(self) -> str:
        """Generate the string representation of the Results object."""
        return (
            f'{self.__class__.__name__}('
            f'group={self.group!r}, '
            f'title={self.title!r}, '
            f'description={self.description!r}, '
            f'n={self.n!r}, '
            f'variation_cols={self.variation_cols!r}, '
            f'marks={self.marks!r}, '
            f'iterations={self.iterations!r}, '
            f'rounds={self.rounds!r}, '
            f'extra_info={self.extra_info!r})'
        )
