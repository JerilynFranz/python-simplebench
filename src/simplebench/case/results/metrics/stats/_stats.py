"""Base benchmark statistics class."""

import statistics
from math import isclose, sqrt

from simplebench.simplebench_types import Immutable

from simplebench.metrics import Metric
from simplebench.report.versions import v1 as reports
from simplebench.si_units import si_scale_to_unit, si_unit_base
from simplebench.simplebench_types import Values

from . import _validate


class Stats(Immutable):
    """Generic container for statistics on a benchmark.

    :ivar Metric metric: The metric definition for the benchmark. (read only)
    :ivar int iterations: The total number of iterations represented by the data points. (read only)
    :ivar int rounds: The number of rounds each data point represents. (read only)
    :ivar Values data: Tuple of floating point data points. (read only)
    :ivar timer: The timer used for the measurement. (read only)
    :itype timer: str | None
    :ivar float mean: The mean of the data. (read only)
    :ivar float median: The median of the data. (read only)
    :ivar float minimum: The minimum of the data. (read only)
    :ivar float maximum: The maximum of the data. (read only)
    :ivar float standard_deviation: The estimated population standard deviation of the data. (read only)
    :ivar float relative_standard_deviation: The estimated population relative standard
        deviation of the data. (read only)
    :ivar Percentiles percentiles: Percentiles of the data. (read only)

    """

    __slots__ = (
        '_metric',
        '_data',
        '_timer',
        '_rounds',
        '_percentiles',
        '_mean',
        '_median',
        '_minimum',
        '_maximum',
        '_standard_deviation',
        '_relative_standard_deviation',
        '_cached_stats_block',
    )

    def __init__(self, *, metric: Metric, data: Values, rounds: int, timer: str | None = None) -> None:
        """Initialize the Stats object.

        :param metric: The metric definition for the benchmark.
        :type metric: Metric
        :param data: Values tuple of data points.
        :type data: Values
        :param rounds: The number of rounds each data point represents.
        :type rounds: int
        :param timer: The timer used for the measurement.
        :type timer: str | None
        :raises SimpleBenchTypeError: If any of the arguments are of the wrong type.
        :raises SimpleBenchValueError: If any of the arguments have invalid values.
        """
        self._metric: Metric = _validate.metric(metric)
        self._rounds: int = _validate.rounds(rounds)
        self._timer: str | None = _validate.timer(timer)
        self._data: Values = _validate.data(data)

        self._mean: float | None = None
        self._median: float | None = None
        self._minimum: float | None = None
        self._maximum: float | None = None
        self._standard_deviation: float | None = None
        self._relative_standard_deviation: float | None = None
        self._percentiles: Values | None = None
        self._cached_stats_block: reports.StatsBlock | None = None

    @property
    def metric(self) -> Metric:
        """The :class:`Metric` metric for the stats..

        :return: The metric for the stats.
        :rtype: Metric
        """
        return self._metric

    @property
    def name(self) -> str:
        """The name of the metric.

        :return: The name of the metric.
        :rtype: str
        """
        return self.metric.title

    @property
    def semantic_type(self) -> str:
        """The semantic type of the metric

        :return: The semantic type of the underlying :class:`Metric`.
        :rtype: str
        """
        return self.metric.metric_type.semantic_type

    @property
    def description(self) -> str:
        """"The description of the underlying :class:`Metric`.

        :return: The description of the underlying :class:`Metric`.
        :rtype: str
        """
        return self.metric.metric_type.description

    @property
    def unit(self) -> str:
        """The unit of the data :class:`Metric`.

        e.g., "s" for seconds, "B" for bytes, 'items' for a count of items, etc.

        :return: The unit of the data.
        :rtype: str
        """
        return self.metric.metric_type.unit

    @property
    def scale(self) -> float:
        """The scale of the data :class:`Metric`.

        This is the factor by which the raw data points are scaled to convert them to the base unit.

        :return: The scale of the data.
        :rtype: float
        """
        return self.metric.metric_type.scale

    @property
    def rounds(self) -> int:
        """The number of rounds each data point represents.

        Each iteration represents a single measurement, which may represent multiple rounds.
        Multiple rounds are often used to reduce the impact of noise or timer precision and
        accuracy on individual measurements.

        The number of rounds is used to adjust the standard deviation calculation to estimate
        the true standard deviation of the underlying population.

        The number of rounds is typically set to a value that balances the trade-off between
        the number of measurements and the time required to perform the measurements.

        :return: The number of rounds each data point represents.
        :rtype: int
        """
        return self._rounds

    @property
    def timer(self) -> str | None:
        """The timer used for the measurement.

        :return: The timer name or None if not specified.
        :rtype: str | None
        """
        return self._timer

    @property
    def iterations(self) -> int:
        """The total number of iterations represented by the data points.

        Each iteration represents a single measurement, which may represent multiple rounds
        averaged together to produce a single data point.

        :return: The total number of iterations represented by the data points.
        :rtype: int
        """
        return len(self._data)

    @property
    def mean(self) -> float:
        """The mean of the data.

        :return: The mean of the data.
        :rtype: float
        """
        if self._mean is None:
            self._mean = statistics.mean(self._data.as_tuple()) if self._data else 0.0
        return self._mean

    @property
    def median(self) -> float:
        """The median of the data.

        :return: The median of the data.
        :rtype: float
        """
        if self._median is None:
            self._median = statistics.median(self._data.as_tuple()) if self._data else 0.0
        return self._median

    @property
    def minimum(self) -> float:
        """The minimum of the data.

        :return: The minimum value in the data.
        :rtype: float
        """
        if self._minimum is None:
            self._minimum = float(min(self._data.as_tuple())) if self._data else 0.0
        return self._minimum

    @property
    def maximum(self) -> float:
        """The maximum of the data.

        :return: The maximum value in the data.
        :rtype: float
        """
        if self._maximum is None:
            self._maximum = float(max(self._data.as_tuple())) if self._data else 0.0
        return self._maximum

    @property
    def standard_deviation(self) -> float:
        """The estimated population standard deviation of the data.

        This is computed using the sample standard deviation formula (Bessel's correction)
        adjusted by the square root of the number of rounds to estimate the population
        standard deviation.

        This provides a much better estimate of the true standard deviation of the underlying
        population when each data point represents multiple rounds of measurement.

        .. note::
            Standard deviation is not mathematically defined for datasets with fewer than 2 data points.

            In such cases, a StatisticsError is typically raised. However, in this implementation,
            we return 0.0 for datasets with fewer than 2 data points to avoid raising an exception
            and to provide a reasonablly interpreted value for this edge case.

            In practice, a standard deviation of 0.0 for a dataset with fewer than 2 data points can be interpreted as
            indicating that there is no variability in the data, which is consistent with the fact that we cannot
            compute a meaningful standard deviation from such a small dataset.

            In practice this can only occur when the number of iterations is 1 which is typically not a
            useful case for benchmarking, but this implementation allows it to be handled gracefully
            without raising an exception.

        :return: The estimated population standard deviation of the data.
        :rtype: float
        """
        if self._standard_deviation is None:
            self._standard_deviation = statistics.stdev(
                self._data.as_tuple()) * sqrt(self.rounds) if len(self._data) > 1 else 0.0
        return self._standard_deviation

    @property
    def relative_standard_deviation(self) -> float:
        """The relative standard deviation of the data.

        This is expressed as the absolute value of the standard deviation as a
        percentage of the mean.

        If the mean is **exactly** zero, the relative standard deviation is defined
        to be zero to avoid division by zero and to provide a reasonable interpretation of this edge case.

        :return: The relative standard deviation of the data as a percentage.
        :rtype: float
        """
        if self._relative_standard_deviation is None:
            self._relative_standard_deviation = abs(100 * self.standard_deviation / self.mean) if self.mean else 0.0
        return self._relative_standard_deviation

    @property
    def percentiles(self) -> Values:
        """Percentiles of the data.

        Returns the 0th through 100th percentiles of the data as an immutable Values tuple of floats.

        The 0th percentile is the minimum value, the 50th percentile is the median, and the 100th
        percentile is the maximum value.

        :return: The percentiles of the data as an immutable Values tuple of 101 floats.
        :rtype: Values
        """
        if self._percentiles is None:
            self._percentiles = self._calculate_percentiles()
        return self._percentiles

    def _calculate_percentiles(self) -> Values:
        """Helper to calculate percentiles.

        .. note::
            statistics.quantiles with n=102 and method='inclusive' is used
            to calculate the percentiles from 0 to 100 inclusive (it generates 101
            cut points, which correspond to percentiles 0 through 100).

        :return: A tuple of percentiles keyed positionally by percent from 0 to 100.
        :rtype: Values
        """
        percentiles_n: list[int] = list(range(0, 101))
        if len(self._data) == 1:
            value = self._data.as_tuple()[0]
            return Values(tuple([value] * len(percentiles_n)))
        quantile_values = statistics.quantiles(self._data.as_tuple(), n=102, method='inclusive')
        return Values(quantile_values)

    def stats_block(self) -> reports.StatsBlock:
        """Returns a :class:`reports.StatsBlock` for the statistics.

        The data values are scaled according to the scale factor to provide
        human-readable values using the base unit rather than the scaled unit.

        The unit is converted to its SI base unit representation. (e.g., "ms" becomes "s")

        This does not include raw data points, only the statistical data.

        The returned StatsBlock is cached for efficiency.

        :returns: A StatsBlock object representing the statistics.
        :rtype: reports.StatsBlock
        """
        if self._cached_stats_block is None:
             self._cached_stats_block = reports.StatsBlock(
                name=self.name,
                semantic_type=self.semantic_type,
                description=self.description,
                unit=self.unit,
                scale=self.scale,
                rounds=self.rounds,
                timer=self.timer,
                measurements=self._data
            )
        return self._cached_stats_block

    def __eq__(self, other: object) -> bool:
        """Compare two Stats objects for equality.

        Equality is based on stats statistics and not on object identity.

        It handles scale differences between two Stats objects and compares
        the statistics accordingly using an appropriate tolerance for floating-point comparisons.

        It also verifies that the units are equivalent when converted to their SI base units.

        It does not consider the raw data points in the comparison as they will differ
        between a basic Stats object and a StatsSummary object derived from it.

        :param object other: The other object to compare against.
        :return: True if the objects are considered equal, False otherwise.
        :raises SimpleBenchValueError: If either Stats object has a scale of zero.
        """
        if not isinstance(other, Stats):
            return NotImplemented

        # this handles scale differences between two Stats objects
        self_base_unit: str = si_unit_base(self.unit)
        other_base_unit: str = si_unit_base(other.unit)
        if self_base_unit != other_base_unit:
            return False

        scale_by: float = si_scale_to_unit(base_unit=self_base_unit, current_unit=other.unit, target_unit=self.unit)
        relative_scale: float = self.scale / other.scale

        if self.rounds != other.rounds:
            return False

        if not isclose(scale_by, relative_scale):
            return False

        if not (
            isclose(self.mean, other.mean / relative_scale)
            and isclose(self.median, other.median / relative_scale)
            and isclose(self.minimum, other.minimum / relative_scale)
            and isclose(self.maximum, other.maximum / relative_scale)
            and isclose(self.standard_deviation, other.standard_deviation / relative_scale)
            and isclose(self.relative_standard_deviation, other.relative_standard_deviation)
        ):
            return False

        if len(self.percentiles) != len(other.percentiles):
            return False

        for self_pct, other_pct in zip(self.percentiles.as_tuple(), other.percentiles.as_tuple(), strict=True):
            if not isclose(self_pct, other_pct / relative_scale):
                return False

        return si_unit_base(self.unit) == si_unit_base(other.unit)

    def __repr__(self) -> str:
        """The string representation of the Stats object.

        .. note:: The data points used to create the statistics are not included
            in the representation because there are typically many thousands
            of data points - so the repr cannot be used to recreate a Stats object.

        It is not intended to be used to recreate a Stats object, but rather
        to provide a human-readable summary of the metadata of the Stats object.

        It is **not** a stable representation and may change in future versions
        without warning, so it should not be relied upon for parsing or other
        programmatic uses.

        Illustrative output
        -------------------

        .. code-block:: python
            Stats(
                rounds=1000,
                timer='timer.perf_counter_ns',
                metric=Metric(
                    label='STD_TIMING_STATS',
                    title='Timing',
                    description='Time per measurement statistics',
                    metric_type=MetricType(
                        label='STD_TIMING_STATS',
                        description='Time per measurement metric statistics',
                        category=MetricCategory.STATISTICAL,
                        semantic_type='simplebench_std::time_per_operation_stats',
                        unit='s',
                        scale=1.0)))

        :returns: A string representation of the Stats object.
        :rtype: str
        """
        metrics_lines = repr(self.metric).splitlines()
        metrics_repr = '\n        '.join(metrics_lines)
        timer_repr = repr(self.timer)
        return (f"{self.__class__.__name__}(\n"
                f"    rounds={self.rounds!r}, "
                f"    timer={timer_repr},"
                f"    metric={metrics_repr})")
