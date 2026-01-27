"""Validators for the Results class."""

from collections.abc import Mapping
from copy import copy, deepcopy
from types import MappingProxyType
from typing import Any

from simplebench.exceptions import SimpleBenchTypeError, SimpleBenchValueError
from simplebench.metrics import Metric, MetricCategory
from simplebench.simplebench_types import Mark, Values, VariationMarks
from simplebench.validators import validate_type

from ._error_tags import _ResultsErrorTag


def metric(value: Metric) -> Metric:
    """Validates an argument to ensure it is of type Metric.

    :param Metric value: The metric to validate.
    :returns Metric: The validated metric.
    :raises SimpleBenchTypeError: If the metric is not of type Metric.
    """
    validate_type(value, Metric, 'metric', _ResultsErrorTag.INVALID_METRIC_ARG_TYPE)
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
    validate_type(metric_category, MetricCategory, 'metric_category', _ResultsErrorTag.INVALID_METRIC_CATEGORY_ARG_TYPE)
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


def iterations(iterations_value: Mapping[Metric, Values]) -> MappingProxyType[Metric, Values]:
    """Validate the iterations Mapping.

    :param Mapping[Metric, Values] iterations_value: The iterations Mapping to validate.
    :returns MappingProxyType[Metric, Values]: A mapping proxy of the validated iterations.
    :raises SimpleBenchTypeError: If the iterations is not a Mapping or if any key is not of type Metric
        or any value is not of type Values.
    """
    if not isinstance(iterations_value, Mapping):
        raise SimpleBenchTypeError(
            f'Invalid iterations type: {type(iterations_value)}. Must be of type Mapping[Metric, Values].',
            tag=_ResultsErrorTag.ITERATIONS_INVALID_ARG_TYPE,
        )
    if not all(isinstance(key, Metric) and isinstance(value, Values) for key, value in iterations_value.items()):
        raise SimpleBenchTypeError(
            'Invalid iterations mapping. All keys must be of type Metric and all values must be of type Values.',
            tag=_ResultsErrorTag.ITERATIONS_INVALID_ARG_IN_SEQUENCE,
        )
    return MappingProxyType(iterations_value)


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
        return MappingProxyType({})
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
