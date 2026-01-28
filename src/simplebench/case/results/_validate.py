"""Validation functions for Results objects.

Because these validators are in a performance-critical path, they do not use
the general-purpose validators from :mod:`simplebench.validators`. Instead, they
implement the necessary validation logic directly.
"""

from simplebench.exceptions import SimpleBenchTypeError, SimpleBenchValueError
from simplebench.metrics import Metric, MetricCategory
from simplebench.simplebench_types import Extras, Iterations, MetricsTimers, VariationMarks

from ._error_tags import _ResultsErrorTag


def metrics_timers(value: MetricsTimers) -> MetricsTimers:
    """Confirm that the metrics_timers argument is a MetricsTimers instance.

    :param value: The metrics_timers to validate.
    :type value: MetricsTimers
    :returns: The validated MetricsTimers instance.
    :rtype: MetricsTimers
    :raises SimpleBenchTypeError: If the value is not a :class:`MetricsTimers` instance.
    """
    if not isinstance(value, MetricsTimers):
        raise SimpleBenchTypeError(
            f'"metrics_timers" must be a MetricsTimers instance not a {type(value)}.',
            tag=_ResultsErrorTag.METRICS_TIMERS_INVALID_ARG_TYPE,)
    return value

def group(value: str) -> str:
    """Validate group name for Results.

    :param values: Group name to validate.
    :type values: str
    :return: Validated group name.
    :rtype: str
    :raises SimpleBenchValueError: If the group name is blank.
    :raises SimpleBenchTypeError: If the group name is not a string.
    """
    if not isinstance(value, str):
        raise SimpleBenchTypeError(
            f'"group" must be a string not {type(value)}.',
            tag=_ResultsErrorTag.GROUP_INVALID_ARG_TYPE,
            )
    value = value.strip()
    if not value:
        raise SimpleBenchValueError(
            '"group" must be a non-blank string.',
            tag=_ResultsErrorTag.GROUP_INVALID_ARG_VALUE
            )
    return value


def title(value: str) -> str:
    """Validate title for Results.

    :param values: Title to validate.
    :type values: str
    :return: Validated title.
    :rtype: str
    :raises SimpleBenchValueError: If the title is blank.
    :raises SimpleBenchTypeError: If the title is not a string.
    """
    if not isinstance(value, str):
        raise SimpleBenchTypeError(
            f'"title" must be a string not {type(value)}.',
            tag=_ResultsErrorTag.TITLE_INVALID_ARG_TYPE,
            )
    value = value.strip()
    if not value:
        raise SimpleBenchValueError(
            '"title" must be a non-blank string.',
            tag=_ResultsErrorTag.TITLE_INVALID_ARG_VALUE
            )
    return value


def description(value: str) -> str:
    """Validate description for Results.

    :param values: Description to validate.
    :type values: str
    :return: Validated description.
    :rtype: str
    :raises SimpleBenchValueError: If the description is blank.
    :raises SimpleBenchTypeError: If the description is not a string.
    """
    if not isinstance(value, str):
        raise SimpleBenchTypeError(
            f'"description" must be a string not {type(value)}.',
            tag=_ResultsErrorTag.DESCRIPTION_INVALID_ARG_TYPE,
            )
    value = value.strip()
    if not value:
        raise SimpleBenchValueError(
            '"description" must be a non-blank string.',
            tag=_ResultsErrorTag.DESCRIPTION_INVALID_ARG_VALUE
            )
    return value

def n(value: float) -> float:
    """Validate complexity n value for Results.

    :param values: n to validate.
    :type values: float
    :return: Validated n.
    :rtype: float
    :raises SimpleBenchValueError: If n is not a positive float (> 0).
    :raises SimpleBenchTypeError: If n is not a float.
    """
    if not isinstance(value, float):
        raise SimpleBenchTypeError(
            f'"n" must be a float not {type(value)}.',
            tag=_ResultsErrorTag.N_INVALID_ARG_TYPE,
            )
    if value <= 0.0:
        raise SimpleBenchValueError(
            '"n" must be a positive float.',
            tag=_ResultsErrorTag.N_INVALID_ARG_VALUE
            )
    return value


def rounds(value: int) -> int:
    """Validate rounds for Results.

    :param values: Rounds to validate.
    :type values: int
    :return: Validated rounds.
    :rtype: int
    :raises SimpleBenchValueError: If rounds is not a positive integer (> 0).
    :raises SimpleBenchTypeError: If rounds is not an int.
    """
    if not isinstance(value, int):
        raise SimpleBenchTypeError(
            f'"rounds" must be an int not {type(value)}.',
            tag=_ResultsErrorTag.ROUNDS_INVALID_ARG_TYPE,
            )
    if value <= 0:
        raise SimpleBenchValueError(
            '"rounds" must be a positive integer.',
            tag=_ResultsErrorTag.ROUNDS_INVALID_ARG_VALUE
            )
    return value


def iterations(value: Iterations) -> Iterations:
    """Validate iterations for Results.

    :param values: Iterations to validate.
    :type values: Iterations
    :return: Validated iterations.
    :rtype: Iterations
    :raises SimpleBenchValueError: If iterations is not a positive integer (> 0).
    :raises SimpleBenchTypeError: If iterations is not an int.
    """
    if not isinstance(value, Iterations):
        raise SimpleBenchTypeError(
            f'"iterations" must be an Iterations instance not {type(value)}.',
            tag=_ResultsErrorTag.ITERATIONS_INVALID_ARG_TYPE,
            )
    if not value:
        raise SimpleBenchValueError(
            '"iterations" must contain at least one iteration.',
            tag=_ResultsErrorTag.ITERATIONS_INVALID_ARG_VALUE
            )
    return value


def metric(value: Metric) -> Metric:
    """Validates an argument to ensure it is of type Metric.

    :param Metric value: The metric to validate.
    :returns Metric: The validated metric.
    :raises SimpleBenchTypeError: If the metric is not of type Metric.
    """
    if not isinstance(value, Metric):
        raise SimpleBenchTypeError(
            f'Invalid metric: {value}. Must be a Metric instance.',
            tag=_ResultsErrorTag.INVALID_METRIC_ARG_TYPE,
        )
    return value


def belongs_to_metric_category(value: Metric, metric_category: MetricCategory) -> Metric:
    """Validates that a Metric belongs to a specific MetricCategory.

    :param Metric value: The metric to validate.
    :param MetricCategory metric_category: The metric category to validate against.
    :returns Metric: The validated metric.
    :raises SimpleBenchTypeError: If the metric is not of type Metric or the metric_category is not of
        type MetricCategory.
    :raises SimpleBenchValueError: If the metric does not belong to the specified metric_category.
    """
    metric(value)
    if not isinstance(metric_category, MetricCategory):
        raise SimpleBenchTypeError(
            f'Invalid metric_category: {metric_category}. Must be a MetricCategory instance.',
            tag=_ResultsErrorTag.INVALID_METRIC_CATEGORY_ARG_TYPE,
        )
    if not value.metric_type.category == metric_category:
        raise SimpleBenchValueError(
            f'Invalid metric: {value}. Must be a Metric with {metric_category.name} category.',
            tag=_ResultsErrorTag.INVALID_METRIC_TYPE_CATEGORY_ARG_VALUE,
        )
    return value


def variation_marks(value: VariationMarks) -> VariationMarks:
    """Validate the marks dictionary.

    Performs shallow copy of the dictionary to prevent external mutation.

    :param Mapping[str, tuple[str, ...]] | None value: The marks dictionary to validate.
    :returns MappingProxyType[str, tuple[str, ...]]: A shallow copy of the validated marks dictionary.
    :raises SimpleBenchTypeError: If the marks is not a dictionary or if any key is not a string.
    :raises SimpleBenchValueError: If any key is a blank string.
    :raises SimpleBenchTypeError: If any value is not a tuple of strings.
    """
    if not isinstance(value, VariationMarks):
        raise SimpleBenchTypeError(
            f'Invalid marks: {value}. Must be a VariationMarks instance.',
            tag=_ResultsErrorTag.VARIATION_MARKS_INVALID_ARG_TYPE,
        )
    return value

def extra_info(value: Extras) -> Extras:
    """Validate the extra_info object if passed, or create a default one if None.

    Performs deep copy of the dictionary to help mitigate external mutation. This means
    that the extra_info dict must be deepcopy-able.

    :param value: The extra_info data
    :type value: Extras
    :returns: The validated Extras instance.
    :rtype: :class:`Extras`
    :raises SimpleBenchTypeError: If the value is not a :class:`Extras` instance.
    """
    if not isinstance(value, Extras):
        raise SimpleBenchTypeError(
            f'Invalid extra_info type: {type(value)}. Must be of type Extras',
            tag=_ResultsErrorTag.EXTRA_INFO_INVALID_ARG_TYPE,
        )
    return value
