from simplebench.exceptions import SimpleBenchTypeError, SimpleBenchValueError
from simplebench.metrics import Metric, MetricCategory
from simplebench.simplebench_types import Values

from ._error_tags import _RawErrorTag


def timer(value: str | None) -> str | None:
    """Validate that the timer arg is a str if not None.

    :param value: 'timer' parameter
    :type value: str | None
    :returns: The validated timer string or None.
    :rtype: str | None
    :raises SimpleBenchTypeError: If the timer is not a str or None.
    :raises SimpleBenchValueError: If the timer is a blank str.
    """
    if value is None:
        return value
    if not isinstance(value, str):
        raise SimpleBenchTypeError(
            f'timer arg must be a str: {type(value)}',
            tag=_RawErrorTag.INVALID_TIMER_ARG_TYPE)
    if value.strip() == '':
        raise SimpleBenchValueError(
            f'timer arg must be a non-blank string: "{value}"',
            tag=_RawErrorTag.INVALID_TIMER_ARG_VALUE)
    return value


def data(value: Values) -> Values:
    """Validate that the data arg is a :class:`~simplebench.simplebench_types.Values`
    instance.

    :param value: 'data' parameter
    :type value: Values
    """
    if not isinstance(value, Values):
        raise SimpleBenchTypeError(
            f'data must be a Values instance: {type(value)}',
            tag=_RawErrorTag.INVALID_DATA_ARG_TYPE)
    return value


def rounds(value: int) -> int:
    """Validates that the rounds is an int that is > 0

    :param value: Number of rounds per iteration
    :type value: int
    :raises SimpleBenchTypeError: If rounds is not an int
    :raises SimpleBenchValueError: If rounds < 1
    """
    if not isinstance(value, int):
        raise SimpleBenchTypeError(
            'rounds must be an integer',
            tag=_RawErrorTag.INVALID_ROUNDS_ARG_TYPE)
    if value <= 0:
        raise SimpleBenchValueError(
            f'rounds must be > 0: {value}',
            tag=_RawErrorTag.INVALID_ROUNDS_ARG_VALUE
        )
    return value


def metric(value: Metric) -> Metric:
    """Validates that that it is a :class:`~simplebench.metric.Metric` and belongs
    to the :data:`~simplebench.metrics.MetricCategory.RAW` category

    :param value: The metric to validate.
    :type value: Metric
    :return: The validated metric.
    :rtype: Metric
    :raises SimpleBenchTypeError: If the metric is not of type :class:`~simplebench.metric.Metric`
    :raises SimpleBenchValueError: If the metric does not belong to
        :data:`~simplebench.metrics.MetricCategory.RAW`

    """
    if not isinstance(value, Metric):
        raise SimpleBenchTypeError(
            f'metric is not a Metric instance: {type(value)}',
            _RawErrorTag.INVALID_METRIC_ARG_TYPE
        )
    metric_category = value.metric_type.category
    if  metric_category != MetricCategory.RAW:
        raise SimpleBenchValueError(
            f'Invalid metric_category: {metric_category._name_}. Must be a MetricCategory.RAW instance.',
            tag=_RawErrorTag.INVALID_METRIC_CATEGORY,
        )
    return value
