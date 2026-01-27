"""Validation functions for Results objects.

Because these validators are in a performance-critical path, they do not use
the general-purpose validators from :mod:`simplebench.validators`. Instead, they
implement the necessary validation logic directly.
"""

from simplebench.exceptions import SimpleBenchTypeError, SimpleBenchValueError
from simplebench.metrics import Metric, MetricCategory
from simplebench.simplebench_types import Iterations, Mark, VariationMarks

from ._error_tags import _ResultsErrorTag


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


def variation_cols(value: Mapping[str, str] | None) -> MappingProxyType[str, str]:
    """Validate the variation_cols dictionary.

    :param Mapping[str, str] | None value: The variation_cols dictionary to validate.
    :returns MappingProxyType[str, str]: A read-only mapping of the validated variation_cols dictionary.
    :raises SimpleBenchTypeError: If the variation_cols is not a dictionary or if any key or
        value is not a string.
    :raises SimpleBenchValueError: If any value is a blank string.
    """
    if value is None:
        return MappingProxyType({})
    if not isinstance(value, dict):
        raise SimpleBenchTypeError(
            f'Invalid variation_cols: {value}. Must be a dictionary.',
            tag=_ResultsErrorTag.VARIATION_COLS_INVALID_ARG_TYPE,
        )

    for key, val in value.items():
        if not isinstance(key, str):
            raise SimpleBenchTypeError(
                f'Invalid variation_cols key type: {type(key)}. Must be of type str.',
                tag=_ResultsErrorTag.VARIATION_COLS_INVALID_ARG_KEY_TYPE,
            )
        if key == '':
            raise SimpleBenchValueError(
                'Invalid variation_cols key value: empty string. Keys must be non-empty strings.',
                tag=_ResultsErrorTag.VARIATION_COLS_INVALID_ARG_KEY_VALUE,
            )
        if not isinstance(val, str):
            raise SimpleBenchTypeError(
                f'Invalid variation_cols value type: {type(val)}. Must be of type str.',
                tag=_ResultsErrorTag.VARIATION_COLS_INVALID_ARG_VALUE_TYPE,
            )
    # shallow copy to prevent external mutation
    return MappingProxyType(copy(value))


def variation_marks(value: VariationMarks | None) -> VariationMarks:
    """Validate the marks dictionary.

    Performs shallow copy of the dictionary to prevent external mutation.

    :param Mapping[str, tuple[str, ...]] | None value: The marks dictionary to validate.
    :returns MappingProxyType[str, tuple[str, ...]]: A shallow copy of the validated marks dictionary.
    :raises SimpleBenchTypeError: If the marks is not a dictionary or if any key is not a string.
    :raises SimpleBenchValueError: If any key is a blank string.
    :raises SimpleBenchTypeError: If any value is not a tuple of strings.
    """
    if value is None:
        return VariationMarks({})
    if not isinstance(value, Mapping):
        raise SimpleBenchTypeError(
            f'Invalid marks: {value}. Must be a Mapping.',
            tag=_ResultsErrorTag.VARIATION_MARKS_INVALID_ARG_TYPE,
        )

    return_value: dict[str, str] = {}
    for key, marks_value in value.items():
        if not isinstance(key, str):
            raise SimpleBenchTypeError(
                f'Invalid marks key type: {type(key)}. Must be of type str.',
                tag=_ResultsErrorTag.VARIATION_MARKS_INVALID_ARG_KEY_TYPE,
            )
        stripped_key = key.strip()
        if stripped_key == '':
            raise SimpleBenchValueError(
                'Invalid marks key value: blank string. Keys must be non-blank strings.',
                tag=_ResultsErrorTag.VARIATION_MARKS_INVALID_ARG_KEY_VALUE,
            )
        if not isinstance(marks_value, Mark):
            raise SimpleBenchTypeError(
                f'Invalid marks value type: {type(marks_value)}. Must be of type Mark.',
                tag=_ResultsErrorTag.VARIATION_MARKS_INVALID_ARG_VALUE_TYPE,
            )


def extra_info(value: Mapping[str, Any] | None) -> MappingProxyType[str, Any]:
    """Validate the extra_info object if passed, or create a default one if None.

    Performs deep copy of the dictionary to help mitigate external mutation. This means
    that the extra_info dict must be deepcopy-able.

    :param Mapping[str, Any] | None value: The extra_info object to validate or None.
    :returns MappingProxyType[str, Any]: The validated or default extra_info dictionary.
    :raises SimpleBenchTypeError: If the value is not None and not of type Mapping[str, Any]
    """
    if value is None:
        return MappingProxyType({})

    if not isinstance(value, Mapping):
        raise SimpleBenchTypeError(
            f'Invalid extra_info type: {type(value)}. Must be of type Mapping[str, Any].',
            tag=_ResultsErrorTag.EXTRA_INFO_INVALID_ARG_TYPE,
        )

    # Perform deep copy to prevent external mutation
    return MappingProxyType(deepcopy(value))
