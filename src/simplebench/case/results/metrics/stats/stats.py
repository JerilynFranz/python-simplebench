"""Base benchmark statistics class."""

from __future__ import annotations

import statistics
from math import isclose, sqrt

from simplebench.metrics import Metric
from simplebench.report.versions import v1 as reports
from simplebench.si_units import si_scale_to_unit, si_unit_base
from simplebench.simplebench_types import Values

from . import _validate

class Stats:
    """Generic container for statistics on a benchmark.

    :ivar Metric metric: The metric definition for the benchmark. (read only)
    :ivar int iterations: The total number of iterations represented by the data points. (read only)
    :ivar int rounds: The number of rounds each data point represents. (read only)
    :ivar Values data: Tuple of floating point data points. (read only)
    :ivar float mean: The mean of the data. (read only)
    :ivar float median: The median of the data. (read only)
    :ivar float minimum: The minimum of the data. (read only)
    :ivar float maximum: The maximum of the data. (read only)
    :ivar float standard_deviation: The estimated population standard deviation of the data. (read only)
    :ivar float relative_standard_deviation: The estimated population relative standard
        deviation of the data. (read only)
    :ivar tuple[float, ...] percentiles: Percentiles of the data. (read only)

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
        '_stats_block',
    )

    def __init__(self, *, metric: Metric, data: Values, rounds: int, timer: str | None) -> None:
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

    @property
    def metric(self) -> Metric:
        """The metric of the benchmark."""
        return self._metric

    # This takes advantage of the fact that Values is immutable
    # to allow us to keep references to it without copying.
    # So this has nearly zero overhead for memory or performance.
    @property
    def data(self) -> Values:
        """The data points of the benchmark."""
        return self._data

    @property
    def name(self) -> str:
        """The name of the metric."""
        return self.metric.title

    @property
    def semantic_type(self) -> str:
        """The semantic type of the metric"""
        return self.metric.metric_type.semantic_type

    @property
    def description(self) -> str:
        """"The description of the metric"""
        return self.metric.metric_type.description

    @property
    def unit(self) -> str:
        """The unit of the data."""
        return self.metric.metric_type.unit

    @property
    def scale(self) -> float:
        """The scale of the data."""
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

        Each iteration represents a single measurement, which may represent multiple rounds.
        """
        return len(self.data)

    @property
    def mean(self) -> float:
        """The mean of the data."""
        if self._mean is None:
            self._mean = statistics.mean(self.data) if self.data else 0.0
        return self._mean

    @property
    def median(self) -> float:
        """The median of the data."""
        if self._median is None:
            self._median = statistics.median(self.data) if self.data else 0.0
        return self._median

    @property
    def minimum(self) -> float:
        """The minimum of the data."""
        if self._minimum is None:
            self._minimum = float(min(self.data)) if self.data else 0.0
        return self._minimum

    @property
    def maximum(self) -> float:
        """The maximum of the data."""
        if self._maximum is None:
            self._maximum = float(max(self.data)) if self.data else 0.0
        return self._maximum

    @property
    def standard_deviation(self) -> float:
        """The estimated population standard deviation of the data.

        This is computed using the sample standard deviation formula (Bessel's correction)
        adjusted by the square root of the number of rounds to estimate the population
        standard deviation.

        This provides a better estimate of the true standard deviation of the underlying
        population when each data point represents multiple rounds of measurement.
        """
        if self._standard_deviation is None:
            self._standard_deviation = statistics.stdev(self.data) * sqrt(self.rounds) if len(self.data) > 1 else 0.0
        return self._standard_deviation

    @property
    def relative_standard_deviation(self) -> float:
        """The relative standard deviation of the data.

        This is expressed as the absolute value of the standard deviation as a
        percentage of the mean.
        """
        if self._relative_standard_deviation is None:
            self._relative_standard_deviation = abs(self.standard_deviation / self.mean * 100) if self.mean else 0.0
        return self._relative_standard_deviation

    @property
    def percentiles(self) -> Values:
        """Percentiles of the data.

        Returns the 0th through 100th percentiles of the data as an immutable tuple.
        """
        if self._percentiles is None:
            self._percentiles = self._calculate_percentiles()
        return self._percentiles

    def _calculate_percentiles(self) -> Values:
        """Helper to calculate percentiles.

        Note:

            statistics.quantiles with n=102 and method='inclusive' is used
            to calculate the percentiles from 0 to 100 inclusive (it generates 101
            cut points, which correspond to percentiles 0 through 100).

        Returns:
            A tuple of percentiles keyed positionally by percent from 0 to 100.
        """
        percentiles_n: list[int] = list(range(0, 101))
        if len(self.data) == 1:
            return Values(float(self.data[0]) for _ in percentiles_n)
        quantile_values = statistics.quantiles(self.data, n=102, method='inclusive')
        return Values(quantile_values)

    def stats_block(self) -> reports.StatsBlock:
        """Returns a ``StatsBlock`` for the statistics.

        The data values are scaled according to the scale factor to provide
        human-readable values using the base unit rather than the scaled unit.

        The unit is converted to its SI base unit representation. (e.g., "ms" becomes "s")

        This does not include raw data points, only the statistical data.

        The returned StatsBlock is cached for efficiency.

        :returns: A StatsBlock object representing the statistics.
        :rtype: reports.StatsBlock
        """
        if self._stats_block is None:
             self._stats_block = reports.StatsBlock(
                name=self.name,
                semantic_type=self.semantic_type,
                description=self.description,
                unit=self.unit,
                scale=self.scale,
                rounds=self.rounds,
                timer=self.timer,
                measurements=self.data
            )
        return self._stats_block

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

        for self_pct, other_pct in zip(self.percentiles, other.percentiles, strict=True):
            if not isclose(self_pct, other_pct / relative_scale):
                return False

        return si_unit_base(self.unit) == si_unit_base(other.unit)

    def __repr__(self) -> str:
        """The string representation of the Stats object.

        .. warning::
            This representation is intended for debugging purposes only
            and may change without notice in future releases. Do not
            rely on this format for programmatic access.

            The data points are not included in the representation
            to avoid excessive output.

        :returns: The string representation of the Stats object.
        :rtype: str

        """
        return (f"{self.__class__.__name__}("
                f"metric='{self.metric}', "
                f"rounds={self.rounds}, "
                f"timer={self.timer!r}"
                f"data=...)")
