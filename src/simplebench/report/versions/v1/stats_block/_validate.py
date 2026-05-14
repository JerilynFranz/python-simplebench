"""Validation functions for V1 StatsBlock properties."""
from math import isnan, isinf
import re
from collections.abc import Sequence

from simplebench.exceptions import SimpleBenchTypeError, SimpleBenchValueError
from simplebench.report._error_tags import _StatsBlockErrorTag
from simplebench.simplebench_types import Values
from simplebench.validators import (
    validate_float,
    validate_non_negative_float,
    validate_positive_int,
    validate_sequence_of_numbers,
    validate_string,
    validate_string_with_regex,
)

from ..metric import Metric

__all__: list[str] = []


def metric(value: Metric) -> Metric:
    """Validates that metric is a Metric instance.

    :param Metric value: The value to validate.
    :return Metric: The validated Metric instance.
    :raise SimpleBenchTypeError: If the value is not a Metric instance.
    """
    if not isinstance(value, Metric):
        raise SimpleBenchTypeError(
            f'metric must be of type Metric, got {type(value)}',
            tag=_StatsBlockErrorTag.INVALID_METRIC_TYPE,
        )
    return value


_HASH_ID_REGEX: re.Pattern[str] = re.compile(r'^[a-f0-9]{64}$')
"""Regex pattern for validating hash IDs.

A valid hash ID is a 64-character hexadecimal string consisting of
lowercase letters (a-f) and digits (0-9).

We could put the empty string in the regex as well, but it's cleaner to handle that
separately in the validation function.
"""


def hash_id(value: str) -> str:
    """Validates that hash_id is a valid 64-character hexadecimal string or an empty string.

    :param str value: The value to validate.
    :return str: The validated string value.
    :raise SimpleBenchTypeError: If the value is not a string.
    :raise SimpleBenchValueError: If the value is not a valid hash ID.
    """
    validate_string(
        value,
        'hash_id',
        _StatsBlockErrorTag.INVALID_HASH_ID_TYPE,
        _StatsBlockErrorTag.INVALID_HASH_ID_VALUE,  # impossible to trigger the value error here
        allow_empty=True,
        strip=True,
    )

    if value == '':
        return value

    return validate_string_with_regex(
        value,
        'hash_id',
        _HASH_ID_REGEX,
        _StatsBlockErrorTag.INVALID_HASH_ID_TYPE,  # impossible to trigger the type error here
        _StatsBlockErrorTag.INVALID_HASH_ID_VALUE,
    )


def mean(value: float | None, measurements_value: Values | None) -> float | None:
    """Validates that mean is a floating point number or None.

    :param float | None value: The value to validate.
    :return float | None: The validated floating point value.
    :raise SimpleBenchTypeError: If the value is not a float.
    """
    if value is not None and measurements_value is not None:
        raise SimpleBenchValueError(
            'mean cannot be provided when measurements are provided',
            tag=_StatsBlockErrorTag.MEAN_AND_MEASUREMENTS_PROVIDED,
        )
    if value is None and measurements_value is None:
        raise SimpleBenchValueError(
            'mean cannot be None when measurements is None because statistics cannot be computed',
            tag=_StatsBlockErrorTag.INVALID_MEASUREMENTS_STATE,
        )
    if value is None:
        return None
    return validate_float(value, 'mean', _StatsBlockErrorTag.INVALID_MEAN_TYPE)


def median(value: float | None, measurements_value: Values | None) -> float | None:
    """Validates that the median is a floating point number or None.

    :param float | None value: The value to validate.
    :return float | None: The validated floating point value.
    :raise SimpleBenchTypeError: If the value is not a float.
    :raise SimpleBenchValueError: If the value is provided when measurements are provided,
    or if the value is None when measurements is None.
    """
    if value is not None and measurements_value is not None:
        raise SimpleBenchValueError(
            'median cannot be provided when measurements are provided',
            tag=_StatsBlockErrorTag.MEDIAN_AND_MEASUREMENTS_PROVIDED,
        )
    if value is None and measurements_value is None:
        raise SimpleBenchValueError(
            'median cannot be None when measurements is None because statistics cannot be computed',
            tag=_StatsBlockErrorTag.INVALID_MEASUREMENTS_STATE,
        )
    if value is None:
        return None
    return validate_float(value, 'median', _StatsBlockErrorTag.INVALID_MEDIAN_TYPE)


def minimum(value: float | None, measurements_value: Values | None) -> float | None:
    """Validates that the minimum is a floating point number or None.

    :param float | None value: The value to validate.
    :return float | None: The validated floating point value.
    :raise SimpleBenchTypeError: If the value is not a float.
    :raise SimpleBenchValueError: If the value is provided when measurements
        are provided, or if the value is None when measurements is None.
    """
    if value is not None and measurements_value is not None:
        raise SimpleBenchValueError(
            'minimum cannot be provided when measurements are provided',
            tag=_StatsBlockErrorTag.MINIMUM_AND_MEASUREMENTS_PROVIDED,
        )
    if value is None and measurements_value is None:
        raise SimpleBenchValueError(
            'minimum cannot be None when measurements is None because statistics cannot be computed',
            tag=_StatsBlockErrorTag.INVALID_MEASUREMENTS_STATE,
        )
    if value is None:
        return None
    return validate_float(value, 'minimum', _StatsBlockErrorTag.INVALID_MINIMUM_TYPE)


def maximum(value: float | None, measurements_value: Values | None) -> float | None:
    """Validates that the maximum is a floating point number or None.

    :param float | None value: The value to validate.
    :return float | None: The validated floating point value.
    :raise SimpleBenchTypeError: If the value is not a float.
    :raise SimpleBenchValueError: If the value is provided when measurements are provided,
    or if the value is None when measurements is None.
    """
    if value is not None and measurements_value is not None:
        raise SimpleBenchValueError(
            'maximum cannot be provided when measurements are provided',
            tag=_StatsBlockErrorTag.MAXIMUM_AND_MEASUREMENTS_PROVIDED,
        )
    if value is None and measurements_value is None:
        raise SimpleBenchValueError(
            'maximum cannot be None when measurements is None because statistics cannot be computed',
            tag=_StatsBlockErrorTag.INVALID_MEASUREMENTS_STATE,
        )
    if value is None:
        return None
    return validate_float(value, 'maximum', _StatsBlockErrorTag.INVALID_MAXIMUM_TYPE)


def measurements(value: Sequence[float] | Values | None) -> Values | None:
    """Validates that measurements is a None, or a Values instance, or sequence of floats.

    :param Sequence[float] | Values | None value: The value to validate.
    :return Values | None: None, or a validated Values object containing floats.
    :raise SimpleBenchTypeError: If the value is not None or a sequence of floats.
    :raise SimpleBenchValueError: If the value is a sequence with fewer than 3 items.
    """
    if value is None:
        return None

    if not isinstance(value, (Sequence, Values)):
        raise SimpleBenchTypeError(
            f'measurements must be a Sequence of float, a Values instance, or None, got {type(value)}',
            tag=_StatsBlockErrorTag.INVALID_MEASUREMENTS_TYPE,
        )
    if len(value) < 3:
        raise SimpleBenchValueError(
            'measurements must contain at least 3 values or statistics cannot be computed',
            tag=_StatsBlockErrorTag.TOO_FEW_MEASUREMENTS,
        )

    # Values instances don't need further validation because they are already validated
    if isinstance(value, Values):
        return value

    # This check only runs if value is a Sequence (not a Values instance)
    if not all(isinstance(v, float) for v in value):
        raise SimpleBenchTypeError(
            'All items in measurements must be of type float', tag=_StatsBlockErrorTag.INVALID_MEASUREMENTS_CONTENT_TYPE
        )
    return Values(value)


def rounds(value: int) -> int:
    """Validates that rounds is a positive integer.

    :param int value: The value to validate.
    :return int: The validated positive integer value.
    :raise SimpleBenchTypeError: If the value is not an integer.
    :raise SimpleBenchValueError: If the value is not positive.
    """
    return validate_positive_int(
        value, 'rounds', _StatsBlockErrorTag.INVALID_ROUNDS_TYPE, _StatsBlockErrorTag.INVALID_ROUNDS_VALUE
    )


def iterations(value: int | None, measurements_value: Values | None) -> int | None:
    """Validates that iterations is a positive integer.

    :param int | None value: The value to validate.
    :return int | None: The validated positive integer value.
    :raise SimpleBenchTypeError: If the value is not an integer.
    :raise SimpleBenchValueError: If the value is not positive.
    :raise SimpleBenchValueError: If the value is provided when measurements are provided,
        or if the value is None when measurements is None.
    """
    if value is not None and measurements_value is not None:
        raise SimpleBenchValueError(
            'iterations cannot be provided when measurements are provided',
            tag=_StatsBlockErrorTag.ITERATIONS_AND_MEASUREMENTS_PROVIDED,
        )
    if value is None and measurements_value is None:
        raise SimpleBenchValueError(
            'iterations cannot be None when measurements is None because statistics cannot be computed',
            tag=_StatsBlockErrorTag.INVALID_MEASUREMENTS_STATE,
        )
    if value is None:
        return None
    return validate_positive_int(
        value, 'iterations', _StatsBlockErrorTag.INVALID_ITERATIONS_TYPE, _StatsBlockErrorTag.INVALID_ITERATIONS_VALUE
    )


def percentiles(value: Values | Sequence[float | int] | None, measurements_value: Values | None) -> Values | None:
    """Validates that percentiles is a sequence of floats or ints or None.

    :param Values | Sequence[float | int] | None value: The value to validate.
    :return Values | None: None, or a validated Values object containing floats.
    :raise SimpleBenchTypeError: If the value is not None or a sequence of floats or ints.
    :raise SimpleBenchValueError: If the value is not a sequence of 101 numbers or not sorted in ascending order.
    :raise SimpleBenchValueError: If the value is provided when measurements are provided,
        or if the value is None when measurements is None.
    """
    if value is not None and measurements_value is not None:
        raise SimpleBenchValueError(
            'percentiles cannot be provided when measurements are provided',
            tag=_StatsBlockErrorTag.PERCENTILES_AND_MEASUREMENTS_PROVIDED,
        )
    if value is None and measurements_value is None:
        raise SimpleBenchValueError(
            'percentiles cannot be None when measurements is None because statistics cannot be computed',
            tag=_StatsBlockErrorTag.INVALID_MEASUREMENTS_STATE,
        )
    if value is None:
        return None

    # If the value is not already a Values object, validate it as a sequence of numbers
    # and convert it to a Values object containing floats
    if not isinstance(value, Values):
        validated_list = validate_sequence_of_numbers(
            value,
            'percentiles',
            _StatsBlockErrorTag.INVALID_PERCENTILES_TYPE,
            _StatsBlockErrorTag.INVALID_PERCENTILES_CONTENT_TYPE,
            allow_empty=False,
        )
        validated_values = Values(tuple(float(x) for x in validated_list))

    else:
        validated_values = value

    # Verify that the percentiles list has exactly 101 items
    if len(validated_values) != 101:
        raise SimpleBenchValueError(
            'percentiles must be a sequence of 101 numbers', tag=_StatsBlockErrorTag.INVALID_PERCENTILES_LENGTH
        )

    # Verify that the percentiles are sorted in ascending order
    if Values(sorted(validated_values.as_tuple())) != validated_values.as_tuple():
        raise SimpleBenchValueError(
            'percentiles must be sorted in ascending order',
            tag=_StatsBlockErrorTag.INVALID_PERCENTILES_ORDER
        )

    return validated_values


def relative_stdev(value: float | None, measurements_value: Values | None) -> float | None:
    """Validates that relative_stdev is a float or None.

    It also checks that it is non-negative if it is not None.

    :param float | None value: The value to validate.
    :return float | None: The validated float value or None.
    :raise SimpleBenchTypeError: If the value is not a float.
    :raise SimpleBenchValueError: If the value is negative.
    :raise SimpleBenchValueError: If the value is provided when measurements are provided,
        or if the value is None when measurements is None.
    """
    if value is not None and measurements_value is not None:
        raise SimpleBenchValueError(
            'relative_stdev cannot be provided when measurements are provided',
            tag=_StatsBlockErrorTag.RELATIVE_STDEV_AND_MEASUREMENTS_PROVIDED,
        )
    if value is None and measurements_value is None:
        raise SimpleBenchValueError(
            'relative_stdev cannot be None when measurements is None because statistics cannot be computed',
            tag=_StatsBlockErrorTag.INVALID_MEASUREMENTS_STATE,
        )
    if value is None:
        return None
    return validate_non_negative_float(
        value,
        'relative_stdev',
        _StatsBlockErrorTag.INVALID_RELATIVE_STANDARD_DEVIATION_TYPE,
        _StatsBlockErrorTag.INVALID_RELATIVE_STANDARD_DEVIATION_VALUE,
    )


def stdev(value: float | None, measurements_value: Values | None) -> float | None:
    """Validates that stdev is a float or None.

    It is allowed to be NaN since not all data sets will have a well-defined standard deviation,
    but it is not allowed to be negative.

    It also checks that it is non-negative if it is not None.

    If the value is None, the measurements_value must be provided (not None) because the standard deviation
    can be computed from the measurements.

    :param float | None value: The value to validate.
    :return float | None: The validated float value or None.
    :raise SimpleBenchTypeError: If the value is not a float.
    :raise SimpleBenchValueError: If the value is negative, is negative infinity, or positive infinity.
    :raise SimpleBenchValueError: If the value is provided when measurements are provided,
        or if the value is None when measurements is None.
    """
    if value is not None and measurements_value is not None:
        raise SimpleBenchValueError(
            'stdev cannot be provided when measurements are provided',
            tag=_StatsBlockErrorTag.STDEV_AND_MEASUREMENTS_PROVIDED,
        )
    if value is None and measurements_value is None:
        raise SimpleBenchValueError(
            'stdev cannot be None when measurements is also None because statistics cannot be computed',
            tag=_StatsBlockErrorTag.INVALID_MEASUREMENTS_STATE,
        )

    if measurements_value is not None and not isinstance(measurements_value, Values):
        raise SimpleBenchTypeError(
            f'measurements must be of type Values when validating stdev, got {type(measurements_value)}',
            tag=_StatsBlockErrorTag.INVALID_MEASUREMENTS_TYPE_FOR_STDEV,
        )

    if value is None:
        return None

    if not isinstance(value, float):
        raise SimpleBenchTypeError(
            f'stdev must be of type float or None, got {type(value)}',
            tag=_StatsBlockErrorTag.INVALID_STANDARD_DEVIATION_TYPE,
        )
    if isnan(value):
        return value

    if value < 0.0 or isinf(value):
        raise SimpleBenchValueError(
            'stdev cannot be negative or infinity',
            tag=_StatsBlockErrorTag.INVALID_STANDARD_DEVIATION_VALUE
        )
    return value


def drift_index(value: float | None, measurements_value: Values | None) -> float | None:
    """Validates that drift_index is a float in the range [-1.0, 1.0], NaN, or None.

    If value is not None, it must be a float in the range [-1.0, 1.0] or NaN.
    It is allowed to be NaN since not all data sets will have a well-defined drift index,
    but it is not allowed to be less than -1.0 or greater than 1.0.

    If the value is None, the measurements_value must be provided (not None) because the drift index
    can be computed from the measurements.

    :param float | None value: The value to validate.
    :return float | None: The validated float value or None.
    :raise SimpleBenchTypeError: If the value is not a float or None.
    :raise SimpleBenchValueError: If the value is not in the range [-1.0, 1.0] or NaN.
    :raise SimpleBenchValueError: If the value is provided when measurements are provided,
        or if the value is None when measurements is None.
    """
    if value is not None and measurements_value is not None:
        raise SimpleBenchValueError(
            'drift_index cannot be provided when measurements are provided',
            tag=_StatsBlockErrorTag.DRIFT_INDEX_AND_MEASUREMENTS_PROVIDED,
        )
    if value is None and measurements_value is None:
        raise SimpleBenchValueError(
            'drift_index cannot be None when measurements is None because statistics cannot be computed',
            tag=_StatsBlockErrorTag.INVALID_MEASUREMENTS_STATE,
        )

    if measurements_value is not None and not isinstance(measurements_value, Values):
        raise SimpleBenchTypeError(
            f'measurements must be of type Values when validating drift_index, got {type(measurements_value)}',
            tag=_StatsBlockErrorTag.INVALID_MEASUREMENTS_TYPE_FOR_DRIFT_INDEX,
        )

    if value is None:
        return None

    if not isinstance(value, float):
        raise SimpleBenchTypeError(
            f'drift_index must be of type float or None, got {type(value)}',
            tag=_StatsBlockErrorTag.INVALID_DRIFT_INDEX_TYPE,
        )

    if isnan(value):
        return value

    if not -1.0 <= value <= 1.0:
        raise SimpleBenchValueError(
            f'drift_index must be in range [-1.0, 1.0], got {value}',
            tag=_StatsBlockErrorTag.INVALID_DRIFT_INDEX_VALUE,
        )
    return value


def autocorrelation(value: float | None, measurements_value: Values | None) -> float | None:
    """Validates that autocorrelation is a float in range [-1.0, 1.0], NaN, or None.

    If value is not None, it must be a float in the range [-1.0, 1.0] or NaN.
    It is allowed to be NaN since not all data sets will have a well-defined autocorrelation,
    but it is not allowed to be less than -1.0 or greater than 1.0.

    If the value is None, the measurements_value must be provided (not None) because the autocorrelation
    can be computed from the measurements.

    :param float | None value: The value to validate.
    :return float | None: The validated float value or None.
    :raise SimpleBenchTypeError: If the value is not a float or None
    :raise SimpleBenchValueError: If the value is not a number in the range [-1.0, 1.0] or NaN.
    :raise SimpleBenchValueError: If the value is provided when measurements are provided,
        or if the value is None when measurements is None.
    """
    if value is not None and measurements_value is not None:
        raise SimpleBenchValueError(
            'autocorrelation cannot be provided when measurements are provided',
            tag=_StatsBlockErrorTag.AUTOCORRELATION_AND_MEASUREMENTS_PROVIDED,
        )
    if value is None and measurements_value is None:
        raise SimpleBenchValueError(
            'autocorrelation cannot be None when measurements is None because statistics cannot be computed',
            tag=_StatsBlockErrorTag.INVALID_MEASUREMENTS_STATE,
        )

    if measurements_value is not None and not isinstance(measurements_value, Values):
        raise SimpleBenchTypeError(
            f'measurements must be of type Values when validating autocorrelation, got {type(measurements_value)}',
            tag=_StatsBlockErrorTag.INVALID_MEASUREMENTS_TYPE_FOR_AUTOCORRELATION,
        )

    if value is None:
        return None
    if not isinstance(value, float):
        raise SimpleBenchTypeError(
            f'autocorrelation must be of type float or None, got {type(value)}',
            tag=_StatsBlockErrorTag.INVALID_AUTOCORRELATION_TYPE,
        )
    if isnan(value):
        return value

    if not -1.0 <= value <= 1.0:
        raise SimpleBenchValueError(
            f'autocorrelation must be in range [-1.0, 1.0], got {value}',
            tag=_StatsBlockErrorTag.INVALID_AUTOCORRELATION_VALUE,
        )
    return value
