"""Base benchmark statistics class."""
from __future__ import annotations

import statistics
from math import isclose, sqrt
from typing import Any, Sequence

from simplebench.case.results.metrics import Iteration
from simplebench.exceptions import SimpleBenchKeyError, SimpleBenchTypeError, SimpleBenchValueError
from simplebench.metric import Metric, metrics_registry
from simplebench.report.versions import v1
from simplebench.si_units import si_scale_to_unit, si_unit_base
from simplebench.validators import validate_positive_int

from ._error_tags import _StatsErrorTag

StatsBlock = v1.StatsBlock


class Stats:
    '''Generic container for statistics on a benchmark.

    :ivar Metric metric: The metric definition for the benchmark. (read only)
    :ivar int iterations: The total number of iterations represented by the data points. (read only)
    :ivar int rounds: The number of rounds each data point represents. (read only)
    :ivar tuple[int | float, ...] data: Sequence of data points. (read only)
    :ivar float mean: The mean of the data. (read only)
    :ivar float median: The median of the data. (read only)
    :ivar float minimum: The minimum of the data. (read only)
    :ivar float maximum: The maximum of the data. (read only)
    :ivar float standard_deviation: The estimated population standard deviation of the data. (read only)
    :ivar float relative_standard_deviation: The estimated population relative standard
        deviation of the data. (read only)
    :ivar tuple[float, ...] percentiles: Percentiles of the data. (read only)

    '''
    __slots__ = ('_metric', '_rounds', '_data', '_percentiles', '_mean', '_median',
                 '_minimum', '_maximum', '_standard_deviation', '_relative_standard_deviation',
                 '_report', '_report_with_data')

    def __init__(self, *,
                 metric: Metric,
                 data: Sequence[int | float | Iteration],
                 rounds: int) -> None:
        """Initialize the Stats object.

        :param Metric metric: The metric definition for the benchmark.
        :param Sequence[int | float | Iteration] data: Sequence of data points.
        :param int rounds: The number of rounds each data point represents.
        :raises SimpleBenchTypeError: If any of the arguments are of the wrong type.
        :raises SimpleBenchValueError: If any of the arguments have invalid values.
        """
        self._metric: Metric = self._validate_metric(metric)
        self._rounds: int = validate_positive_int(
                                rounds, 'rounds',
                                _StatsErrorTag.INVALID_ROUNDS_ARG_TYPE,
                                _StatsErrorTag.INVALID_ROUNDS_ARG_VALUE)
        # data is left unsorted to allow for time series data to be preserved
        self._data: tuple[float, ...] = self._validate_data(metric=metric, data=data)
        self._percentiles: tuple[float, ...] | None = None
        self._mean: float | None = None
        self._median: float | None = None
        self._minimum: float | None = None
        self._maximum: float | None = None
        self._standard_deviation: float | None = None
        self._relative_standard_deviation: float | None = None

    def _validate_data(self, *, metric: Metric, data: Sequence[int | float | Iteration]) -> tuple[float, ...]:
        """Validate the data argument.

        :param Metric metric: The metric definition for the benchmark.
        :param Sequence[int | float | Iteration] data: Sequence of data points.
        :raises SimpleBenchTypeError: If the data argument is of the wrong type.
        :raises SimpleBenchValueError: If the data argument has invalid values.
        :return: A tuple of validated data points as floats.
        """
        if not isinstance(data, Sequence):
            raise SimpleBenchTypeError(
                'The data argument must be a sequence of numbers or Iteration objects.',
                tag=_StatsErrorTag.INVALID_DATA_ARG_TYPE)

        validated_data: list[float] = []
        for index, item in enumerate(data):
            if isinstance(item, Iteration):
                validated_data.append(item.metric(metric))
            elif isinstance(item, (int, float)):
                validated_data.append(float(item))
            else:
                raise SimpleBenchTypeError(
                    f'The data argument contains an invalid item at index {index}. '
                    'Each item must be an integer, float, or Iteration object.',
                    tag=_StatsErrorTag.INVALID_DATA_ARG_ITEM_TYPE)

        return tuple(validated_data)

    @property
    def unit(self) -> str:
        '''The unit of the data.'''
        return self._metric.metric_type.unit

    @property
    def scale(self) -> float:
        '''The scale of the data.'''
        return self._metric.metric_type.scale

    @property
    def rounds(self) -> int:
        '''The number of rounds each data point represents.

        Each iteration represents a single measurement, which may represent multiple rounds.
        Multiple rounds are often used to reduce the impact of noise or timer precision and
        accuracy on individual measurements.

        The number of rounds is used to adjust the standard deviation calculation to estimate
        the true standard deviation of the underlying population.

        The number of rounds is typically set to a value that balances the trade-off between
        the number of measurements and the time required to perform the measurements.
        '''
        return self._rounds

    @property
    def iterations(self) -> int:
        '''The total number of iterations represented by the data points.

        Each iteration represents a single measurement, which may represent multiple rounds.
        '''
        return len(self.data)

    @property
    def data(self) -> tuple[float, ...]:
        '''The data points.'''
        return self._data

    @property
    def mean(self) -> float:
        '''The mean of the data.'''
        if self._mean is None:
            self._mean = statistics.mean(self.data) if self.data else 0.0
        return self._mean

    @property
    def median(self) -> float:
        '''The median of the data.'''
        if self._median is None:
            self._median = statistics.median(self.data) if self.data else 0.0
        return self._median

    @property
    def minimum(self) -> float:
        '''The minimum of the data.'''
        if self._minimum is None:
            self._minimum = float(min(self.data)) if self.data else 0.0
        return self._minimum

    @property
    def maximum(self) -> float:
        '''The maximum of the data.'''
        if self._maximum is None:
            self._maximum = float(max(self.data)) if self.data else 0.0
        return self._maximum

    @property
    def standard_deviation(self) -> float:
        '''The estimated population standard deviation of the data.

        This is computed using the sample standard deviation formula (Bessel's correction)
        adjusted by the square root of the number of rounds to estimate the population
        standard deviation.

        This provides a better estimate of the true standard deviation of the underlying
        population when each data point represents multiple rounds of measurement.
        '''
        if self._standard_deviation is None:
            self._standard_deviation = statistics.stdev(self.data) * sqrt(self.rounds) if len(self.data) > 1 else 0.0
        return self._standard_deviation

    @property
    def relative_standard_deviation(self) -> float:
        '''The relative standard deviation of the data.

        This is expressed as the absolute value of the standard deviation as a
        percentage of the mean.
        '''
        if self._relative_standard_deviation is None:
            self._relative_standard_deviation = abs(self.standard_deviation / self.mean * 100) if self.mean else 0.0
        return self._relative_standard_deviation

    @property
    def percentiles(self) -> tuple[float, ...]:
        '''Percentiles of the data.

        Returns the 0th through 100th percentiles of the data as an immutable tuple.
        '''
        if self._percentiles is None:
            self._percentiles = self._calculate_percentiles()
        return self._percentiles

    def _calculate_percentiles(self) -> tuple[float, ...]:
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
            return tuple(float(self.data[0]) for _ in percentiles_n)
        quantile_values = statistics.quantiles(self.data, n=102, method='inclusive')
        return tuple(quantile_values)

    @property
    def as_dict(self) -> dict[str, str | float | dict[int, float] | tuple[int | float, ...]]:
        '''Returns the statistics and data as a JSON-serializable dictionary.

        This includes all the statistics as well as the raw data points.

        The data values are scaled according to the scale factor to provide
        human-readable values using the base unit rather than the scaled unit.

        The unit is normalized to its SI base unit representation. (e.g., "ms" becomes "s")

        The dictionary is mutability-safe as all data is either a primitive or a copy.

        Returns:
            A dictionary containing the statistics and the scaled data points.
        '''
        # Immutability is preserved because all values are primitives or copies already
        stats = self.stats_summary.as_dict
        stats['type'] = f'{self.__class__.__name__}:statistics'
        stats['data'] = tuple(value / self.scale for value in self.data)
        return stats

    def stats_block(self, indent: int = 2, full_data: bool = False) -> StatsBlock:
        """Returns a ``StatsBlock`` for the statistics.

        The data values are scaled according to the scale factor to provide
        human-readable values using the base unit rather than the scaled unit.

        The unit is converted to its SI base unit representation. (e.g., "ms" becomes "s")

        This does not include raw data points, only the statistics.

        Args:
            indent (int): The number of spaces to indent each line of the output.
        """

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> Stats:
        """Construct a Stats object from a dictionary.

        Example:
            .. code-block:: python

                stats_dict = {
                    "unit": "ops/s",
                    "scale": 1,
                    "data": [1000, 2000, 1500, 3000, 2500]
                }
                stats = Stats.from_dict(stats_dict)
                print(stats.mean)  # Output: 2000.0

        :param dict data: A dictionary containing the stats data. Must contain 'data' key with a non-empty
            sequence of data points consisting of integers or floats.
        :return: A Stats object constructed from the provided dictionary.
        :raises SimpleBenchTypeError: If the data, unit, or scale arguments are of the wrong type.
        :raises SimpleBenchKeyError: If the data dictionary does not contain a 'unit' key and
            no unit argument is provided.
        :raises SimpleBenchValueError: If the data dictionary does not contain a non-empty 'data' key
            with at least one data point, if the scale argument is not greater than zero,
            or if the unit argument is an empty string
        """
        if not isinstance(data, dict):
            raise SimpleBenchTypeError('The data argument must be a dictionary.',
                                       tag=_StatsErrorTag.FROM_DICT_INVALID_DATA_ARG_TYPE)
        if 'unit' not in data:
            raise SimpleBenchKeyError('The data dictionary is missing the required "unit" key.',
                                      tag=_StatsErrorTag.FROM_DICT_MISSING_UNIT_KEY)
        if 'scale' not in data:
            raise SimpleBenchKeyError('The data dictionary is missing the required "scale" key.',
                                      tag=_StatsErrorTag.FROM_DICT_MISSING_SCALE_KEY)
        if 'rounds' not in data:
            raise SimpleBenchKeyError('The data dictionary is missing the required "rounds" key.',
                                      tag=_StatsErrorTag.FROM_DICT_MISSING_ROUNDS_KEY)
        if 'data' not in data:
            raise SimpleBenchKeyError('The data dictionary is missing the required "data" key.',
                                      tag=_StatsErrorTag.FROM_DICT_MISSING_DATA_KEY)

        return cls(unit=data['unit'],
                   scale=data['scale'],
                   rounds=data['rounds'],
                   data=data['data'])  # type: ignore[arg-type]

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

        scale_by: float = si_scale_to_unit(base_unit=self_base_unit,
                                           current_unit=other.unit,
                                           target_unit=self.unit)
        relative_scale: float = self.scale / other.scale

        if self.rounds != other.rounds:
            return False

        if not isclose(scale_by, relative_scale):
            return False

        if not (isclose(self.mean, other.mean / relative_scale) and
                isclose(self.median,  other.median / relative_scale) and
                isclose(self.minimum, other.minimum / relative_scale) and
                isclose(self.maximum, other.maximum / relative_scale) and
                isclose(self.standard_deviation, other.standard_deviation / relative_scale) and
                isclose(self.relative_standard_deviation, other.relative_standard_deviation)):
            return False

        if len(self.percentiles) != len(other.percentiles):
            return False

        for self_pct, other_pct in zip(self.percentiles, other.percentiles):
            if not isclose(self_pct, other_pct / relative_scale):
                return False

        return si_unit_base(self.unit) == si_unit_base(other.unit)

    def __repr__(self) -> str:
        return (f"{self.__class__.__name__}(unit='{self.unit}', scale={self.scale}, rounds={self.rounds}, "
                f"data=[{', '.join(str(d) for d in self.data)}])")

    def _validate_metric(self, metric: Metric) -> Metric:
        if not isinstance(metric, Metric):
            raise SimpleBenchTypeError(
                'The metric argument must be a Metric object.',
                tag=_StatsErrorTag.INVALID_METRIC_ARG_TYPE)
        if metric not in metrics_registry:
            raise SimpleBenchValueError(
                'The metric argument is not a registered metric definition.',
                tag=_StatsErrorTag.UNREGISTERED_METRIC)
        return metric
