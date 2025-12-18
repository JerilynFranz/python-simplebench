"""Container for the results of a single benchmark test."""
from __future__ import annotations

from copy import copy, deepcopy
from types import MappingProxyType
from typing import Any, Mapping, Optional, TypeAlias

import simplebench.report.versions.v1 as current_version
from simplebench.exceptions import SimpleBenchTypeError, SimpleBenchValueError
from simplebench.metric import Metric, MetricCategory
from simplebench.types import Values
from simplebench.validators import (
    validate_non_blank_string,
    validate_positive_float,
    validate_positive_int,
    validate_type,
)

from ._error_tags import _ResultsErrorTag
from .metrics import Stats

MetricsObject: TypeAlias = current_version.MetricsObject
ResultsInfo: TypeAlias = current_version.ResultsInfo
StatsBlock: TypeAlias = current_version.StatsBlock
ValueBlock: TypeAlias = current_version.ValueBlock
RawDataBlock: TypeAlias = current_version.RawDataBlock


class Results:
    """Container for the results of a single benchmark test pass.

    The Results class holds all relevant information about a benchmark test's execution and its outcomes.
    It is used to store the results of a benchmark run for a specific case and combination of parameters.

    It is immutable after creation to ensure data integrity.

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
        '_marks',
        '_extra_info',
        '_repr_cache',
        '_stats_cache',
        '_sum_cache',
        '_raw_cache',
    )

    def __init__(self,  # pylint: disable=too-many-arguments, too-many-locals
                 *,
                 group: str,
                 title: str,
                 description: str,
                 n: float,
                 rounds: int,
                 iterations: Mapping[Metric, Values],
                 variation_cols: dict[str, str] | None = None,
                 marks: dict[str, tuple[str, ...]] | None = None,
                 extra_info: Optional[dict[str, Any]] = None) -> None:
        """Initialize a Results object.

        :param group: The reporting group to which the benchmark case belongs.
        :param title: The name of the benchmark case.
        :param description: A brief description of the benchmark case.
        :param n: The O() complexity analysis size/weighting.
        :param rounds: The number of rounds the benchmark ran per iteration.
        :param iterations: A mapping of metrics to their values for the benchmark.
        :param variation_cols: The columns to use for labelling kwarg variations
            in the benchmark. Defaults to None, which results in an empty dictionary.
        :param marks: A dictionary of variation marks used to identify
            the benchmark variation. Defaults to None, which results in an empty dictionary.
        :param extra_info: Any extra information to include in the benchmark results.
            Defaults to {}.
        :raises SimpleBenchTypeError: If any of the arguments are of incorrect type.
        :raises SimpleBenchValueError: If any of the arguments have invalid values.
        """
        self._stats_cache: dict[Metric, Stats] = {}
        self._sum_cache: dict[Metric, float] = {}
        self._raw_cache: dict[Metric, Values] = {}

        self._group: str = validate_non_blank_string(
            group, 'group',
            _ResultsErrorTag.GROUP_INVALID_ARG_TYPE,
            _ResultsErrorTag.GROUP_INVALID_ARG_VALUE)
        self._title: str = validate_non_blank_string(
            title, 'title',
            _ResultsErrorTag.TITLE_INVALID_ARG_TYPE,
            _ResultsErrorTag.TITLE_INVALID_ARG_VALUE)
        self._description: str = validate_non_blank_string(
            description, 'description',
            _ResultsErrorTag.DESCRIPTION_INVALID_ARG_TYPE,
            _ResultsErrorTag.DESCRIPTION_INVALID_ARG_VALUE)
        self._n: float = validate_positive_float(
            n, 'n',
            _ResultsErrorTag.N_INVALID_ARG_TYPE,
            _ResultsErrorTag.N_INVALID_ARG_VALUE)
        self._rounds: int = validate_positive_int(
            rounds, 'rounds',
            _ResultsErrorTag.ROUNDS_INVALID_ARG_TYPE,
            _ResultsErrorTag.ROUNDS_INVALID_ARG_VALUE)
        self._iterations: MappingProxyType[Metric, Values] = self._validate_iterations(iterations)
        self._variation_cols: MappingProxyType[str, str] = self._validate_variation_cols(variation_cols)
        self._marks: MappingProxyType[str, tuple[str, ...]] = self._validate_marks(marks)
        self._extra_info = self._validate_extra_info(extra_info)
        self._repr_cache: Optional[str] = None  # cache for __repr__

    def _validate_variation_cols(self, value: dict[str, str] | None) -> MappingProxyType[str, str]:
        """Validate the variation_cols dictionary.

        Args:
            value (dict[str, str]): The variation_cols dictionary to validate.

        Returns:
            dict[str, str]: A copy of the validated variation_cols dictionary.

        Raises:
            SimpleBenchTypeError: If the variation_cols is not a dictionary or if any key or
                value is not a string.
            SimpleBenchValueError: If any value is a blank string.
        """
        if value is None:
            return MappingProxyType({})
        if not isinstance(value, dict):
            raise SimpleBenchTypeError(
                f'Invalid variation_cols: {value}. Must be a dictionary.',
                tag=_ResultsErrorTag.VARIATION_COLS_INVALID_ARG_TYPE
                )

        for key, val in value.items():
            if not isinstance(key, str):
                raise SimpleBenchTypeError(
                    f'Invalid variation_cols key type: {type(key)}. Must be of type str.',
                    tag=_ResultsErrorTag.VARIATION_COLS_INVALID_ARG_KEY_TYPE
                )
            if key == '':
                raise SimpleBenchValueError(
                    'Invalid variation_cols key value: empty string. Keys must be non-empty strings.',
                    tag=_ResultsErrorTag.VARIATION_COLS_INVALID_ARG_KEY_VALUE
                )
            if not isinstance(val, str):
                raise SimpleBenchTypeError(
                    f'Invalid variation_cols value type: {type(val)}. Must be of type str.',
                    tag=_ResultsErrorTag.VARIATION_COLS_INVALID_ARG_VALUE_TYPE
                )
        # shallow copy to prevent external mutation
        return MappingProxyType(copy(value))

    def _validate_iterations(self, iterations: Mapping[Metric, Values]) -> MappingProxyType[Metric, Values]:
        """Validate the iterations Mapping.

        Args:
            values (Mapping[Metric, Values]): The iterations Mapping to validate.
        Returns:
            MappingProxyType[Metric, Values]: A mapping proxy of the validated iterations.
        """
        if not isinstance(iterations, Mapping):
            raise SimpleBenchTypeError(
                f'Invalid iterations type: {type(iterations)}. Must be of type Mapping[Metric, Values].',
                tag=_ResultsErrorTag.ITERATIONS_INVALID_ARG_TYPE
            )
        if not all(isinstance(key, Metric) and isinstance(value, Values) for key, value in iterations.items()):
            raise SimpleBenchTypeError(
                'Invalid iterations mapping. All keys must be of type Metric and all values must be of type Values.',
                tag=_ResultsErrorTag.ITERATIONS_INVALID_ARG_IN_SEQUENCE
            )
        return MappingProxyType(iterations)

    def _validate_marks(self, value: dict[str, tuple[str, ...]] | None) -> MappingProxyType[str, tuple[str, ...]]:
        """Validate the marks dictionary.

        Performs shallow copy of the dictionary to prevent external mutation.

        Args:
            value (dict[str, tuple[str,...]]): The marks dictionary to validate.

        Returns:
            MappingProxyType[str, tuple[str, ...]]: A shallow copy of the validated marks dictionary.

        Raises:
            SimpleBenchTypeError: If the marks is not a dictionary or if any key is not a string.
            SimpleBenchValueError: If any key is a blank string.
        """
        if value is None:
            return MappingProxyType({})
        if not isinstance(value, dict):
            raise SimpleBenchTypeError(
                f'Invalid marks: {value}. Must be a dictionary.',
                tag=_ResultsErrorTag.VARIATION_MARKS_INVALID_ARG_TYPE
            )

        return_value: dict[str, tuple[str, ...]] = {}
        for key, marks_value in value.items():
            if not isinstance(key, str):
                raise SimpleBenchTypeError(
                    f'Invalid marks key type: {type(key)}. Must be of type str.',
                    tag=_ResultsErrorTag.VARIATION_MARKS_INVALID_ARG_KEY_TYPE
                )
            stripped_key = key.strip()
            if stripped_key == '':
                raise SimpleBenchValueError(
                    'Invalid marks key value: blank string. Keys must be non-blank strings.',
                    tag=_ResultsErrorTag.VARIATION_MARKS_INVALID_ARG_KEY_VALUE
                )
            if not isinstance(marks_value, tuple):
                raise SimpleBenchTypeError(
                    f'Invalid marks value type: {type(marks_value)}. Must be of type tuple[str, ...].',
                    tag=_ResultsErrorTag.VARIATION_MARKS_INVALID_ARG_VALUE_TYPE
                )
            if not all(isinstance(item, str) for item in marks_value):
                raise SimpleBenchTypeError(
                    'Invalid marks value item type. All items in the tuple must be of type str.',
                    tag=_ResultsErrorTag.VARIATION_MARKS_INVALID_ARG_VALUE_ITEM_TYPE
                )
            return_value[key] = marks_value
        return MappingProxyType(return_value)

    def _validate_extra_info(self, value: dict[str, Any] | None) -> MappingProxyType[str, Any]:
        """Validate the extra_info object if passed, or create a default one if None.

        Performs deep copy of the dictionary to help mitigate external mutation. This means
        that the extra_info dict must be deepcopy-able.

        Args:
            value (dict[str, Any] | None): The extra_info object to validate or None.

        Returns:
            dict[str, Any]: The validated or default extra_info dictionary.

        Raises:
            SimpleBenchTypeError: If the value is not None and not of type dict[str, Any]
        """
        if value is None:
            return MappingProxyType({})

        if not isinstance(value, dict):
            raise SimpleBenchTypeError(
                f'Invalid extra_info type: {type(value)}. Must be of type dict[str, Any].',
                tag=_ResultsErrorTag.EXTRA_INFO_INVALID_ARG_TYPE
            )

        # Perform deep copy to prevent external mutation
        return MappingProxyType(deepcopy(value))

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
        validate_type(
            metric, Metric, 'metric',
            _ResultsErrorTag.RESULTS_SECTION_INVALID_SECTION_ARG_TYPE)

        if not metric.metric_type.category == MetricCategory.STATISTICAL:
            raise SimpleBenchValueError(
                (f'Invalid metric: {metric}. Must be Metric with statistical type.'),
                tag=_ResultsErrorTag.RESULTS_SECTION_UNSUPPORTED_SECTION_ARG_VALUE
            )
        if metric not in self._stats_cache:
            self._stats_cache[metric] = Stats(metric=metric,
                                              rounds=self.rounds,
                                              data=self.iterations[metric])
        return self._stats_cache[metric]

    def sum(self, metric: Metric) -> float:
        """Returns the cumulative sum of the raw benchmark results for the given metric.

        The cumulative sum is the total of all raw data points for the specified metric.

        The returned sum is cached for efficiency.

        :param Metric metric: The metric of the results to return. Must be a registered metric.
        :return float: The cumulative sum of the benchmark results.
        """
        validate_type(
            metric, Metric, 'metric',
            _ResultsErrorTag.RESULTS_SECTION_INVALID_SECTION_ARG_TYPE
        )
        if not metric.metric_type.category == MetricCategory.CUMULATIVE:
            raise SimpleBenchValueError(
                (f'Invalid metric: {metric}. Must be a Metric with cumulative category.'),
                tag=_ResultsErrorTag.RESULTS_SECTION_UNSUPPORTED_SECTION_ARG_VALUE
            )
        if metric not in self._sum_cache:
            self._sum_cache[metric] = sum(self.iterations[metric])
        return self._sum_cache[metric]

    def raw(self, metric: Metric) -> Values:
        """Returns the raw data point values of the benchmark results for the given metric.

        :param Metric metric: The metric of the results to return. Must be a registered metric.
        :return Values: The raw data of the benchmark results as a Values instance.
        """
        validate_type(
            metric, Metric, 'metric',
            _ResultsErrorTag.RESULTS_SECTION_INVALID_SECTION_ARG_TYPE
        )
        if not metric.metric_type.category == MetricCategory.RAW:
            raise SimpleBenchValueError(
                (f'Invalid metric: {metric}. Must be Metric with raw type.'),
                tag=_ResultsErrorTag.RESULTS_SECTION_UNSUPPORTED_SECTION_ARG_VALUE
            )
        return self._iterations[metric]

    def results_metric(self, metric: Metric) -> Values:
        """Returns the requested metric of the benchmark results.

        :param Metric metric: The metric of the results to return. Must be a registered metric.

        :return Values: The requested metric values from the benchmark results.
        """
        if not isinstance(metric, Metric):
            raise SimpleBenchTypeError(
                f'Invalid metric type: {type(metric)}. Must be of type Metric.',
                tag=_ResultsErrorTag.RESULTS_SECTION_INVALID_SECTION_ARG_TYPE
            )
        return self.iterations[metric]

    def stats_block(self, metric: Metric, full_data: bool = False) -> StatsBlock:
        """Returns the StatsBlock representation of the Stats for the given metric.

        :param Metric metric: The metric of the results to return. Must be a registered metric.
        :param bool full_data: Whether to include the full data set in the StatsBlock. Defaults to False.

        :return StatsBlock: The StatsBlock representation of the Stats for the given metric.
        """
        stats_instance: Stats = self.stats(metric)
        if full_data:
            return stats_instance.stats_block(full_data=True)
        return stats_instance.stats_block(full_data=False)

    def sum_value_block(self, metric: Metric) -> ValueBlock:
        """Returns the ValueBlock representation of the sum for the given metric.

        :param Metric metric: The metric of the results to return. Must be a registered metric.

        :return ValueBlock: The ValueBlock representation of the sum for the given metric.
        """
        total_sum: float = self.sum(metric)
        return ValueBlock(
            semantic_type=metric.metric_type.semantic_type,
            timer=None,
            unit=metric.metric_type.unit,
            scale=metric.metric_type.scale,
            value=total_sum
        )

    def raw_block(self, metric: Metric) -> RawDataBlock:
        """Returns the RawDataBlock representation of the raw data for the given metric.

        :param Metric metric: The metric of the results to return. Must be a registered metric.

        :return RawDataBlock: The RawDataBlock representation of the raw data for the given metric.
        """
        raw_data: Values = self.raw(metric)
        return RawDataBlock(
            semantic_type=metric.metric_type.semantic_type,
            timer=None,
            unit=metric.metric_type.unit,
            scale=metric.metric_type.scale,
            data=raw_data
        )

    def results_info(self, full_data: bool = False) -> ResultsInfo:
        """Returns a summary of the benchmark results.

        :param full_data: Whether to include the full data set in the summary. Defaults to False.
        :type full_data: bool, optional

        Returns:
            results_info: A ResultsInfo object containing the summary of the benchmark results.
        """
        metrics: dict[str, MetricsObject.MetricItem] = {}
        for metric in self.iterations:
            if metric.metric_type == MetricCategory.STATISTICAL:
                metrics[metric.label] = self.stats_block(metric, full_data=full_data)
            elif metric.metric_type == MetricCategory.CUMULATIVE:
                metrics[metric.label] = self.sum_value_block(metric)
            elif metric.metric_type == MetricCategory.RAW:
                metrics[metric.label] = self.raw_block(metric)

        return ResultsInfo(
            group=self.group,
            title=self.title,
            description=self.description,
            n=self.n,
            variation_cols=self.variation_cols,
            metrics=MetricsObject(metrics),
            extra_info=self.extra_info,
        )

    def __repr__(self) -> str:
        """Return a string representation of the Results object."""
        if self._repr_cache is None:
            self._repr_cache = self._generate_repr()
        return self._repr_cache

    def _generate_repr(self) -> str:
        """Generate the string representation of the Results object."""
        return (f'{self.__class__.__name__}('
                f'group={self.group!r}, '
                f'title={self.title!r}, '
                f'description={self.description!r}, '
                f'n={self.n!r}, '
                f'variation_cols={self.variation_cols!r}, '
                f'marks={self.marks!r}, '
                f'iterations={self.iterations!r}, '
                f'rounds={self.rounds!r}, '
                f'extra_info={self.extra_info!r})')
