"""Validation functions for V1 StatsBlock properties."""
from typing import Sequence

from simplebench.exceptions import SimpleBenchTypeError, SimpleBenchValueError
from simplebench.report._error_tags import _StatsBlockErrorTag
from simplebench.types import Values
from simplebench.validators import (
    validate_float,
    validate_namespaced_identifier,
    validate_non_negative_float,
    validate_positive_float,
    validate_positive_int,
    validate_sequence_of_numbers,
    validate_string,
)


def description(value: str) -> str:
    """Validates that description is a string.

    .. note::
        The description can be empty and will be stripped of leading
        and trailing whitespace.

    :param str value: The value to validate.
    :return str: The validated string value.
    :raise SimpleBenchTypeError: If the value is not a string.
    """
    return validate_string(
                value, 'description',
                _StatsBlockErrorTag.INVALID_DESCRIPTION_TYPE,
                _StatsBlockErrorTag.INVALID_DESCRIPTION_VALUE,
                allow_blank=True, strip=True)


def mean(value: float | None, measurements_value: Values | None) -> float | None:
    """Validates that mean is a floating point number or None.

    :param float | None value: The value to validate.
    :return float | None: The validated floating point value.
    :raise SimpleBenchTypeError: If the value is not a float.
    """
    if value is None:
        return None
    if measurements_value is not None:
        raise SimpleBenchTypeError(
            "mean cannot be provided when measurements are provided",
            tag=_StatsBlockErrorTag.MEAN_AND_MEASUREMENTS_PROVIDED)
    return validate_float(
                value, 'mean',
                _StatsBlockErrorTag.INVALID_MEAN_TYPE)


def median(value: float | None, measurements_value: Values | None) -> float | None:
    """Validates that the median is a floating point number or None.

    :param float | None value: The value to validate.
    :return float | None: The validated floating point value.
    :raise SimpleBenchTypeError: If the value is not a float.
    """
    if value is None:
        return None
    if measurements_value is not None:
        raise SimpleBenchTypeError(
            "median cannot be provided when measurements are provided",
            tag=_StatsBlockErrorTag.MEDIAN_AND_MEASUREMENTS_PROVIDED)
    return validate_float(
                value, 'median',
                _StatsBlockErrorTag.INVALID_MEDIAN_TYPE)


def minimum(value: float | None, measurements_value: Values | None) -> float | None:
    """Validates that the minimum is a floating point number or None.

    :param float | None value: The value to validate.
    :return float | None: The validated floating point value.
    :raise SimpleBenchTypeError: If the value is not a float.
    """
    if value is None:
        return None
    if measurements_value is not None:
        raise SimpleBenchTypeError(
            "minimum cannot be provided when measurements are provided",
            tag=_StatsBlockErrorTag.MINIMUM_AND_MEASUREMENTS_PROVIDED)
    return validate_float(
                value, 'minimum',
                _StatsBlockErrorTag.INVALID_MINIMUM_TYPE)


def maximum(value: float | None, measurements_value: Values | None) -> float | None:
    """Validates that the maximum is a floating point number or None.

    :param float | None value: The value to validate.
    :return float | None: The validated floating point value.
    :raise SimpleBenchTypeError: If the value is not a float.
    """
    if value is None:
        return None
    if measurements_value is not None:
        raise SimpleBenchTypeError(
            "maximum cannot be provided when measurements are provided",
            tag=_StatsBlockErrorTag.MAXIMUM_AND_MEASUREMENTS_PROVIDED)
    return validate_float(
                value, 'maximum',
                _StatsBlockErrorTag.INVALID_MAXIMUM_TYPE)


def measurements(value: Sequence[float] | Values | None) -> Values | None:
    """Validates that measurements is a None, or a Values instance, or sequence of floats.

    :param Sequence[float] | Values | None value: The value to validate.
    :return Values | None: None, or a validated Values object containing floats.
    :raise SimpleBenchTypeError: If the value is not None or a sequence of floats.
    :raise SimpleBenchValueError: If the value is a sequence with fewer than 3 items.
    """
    if not isinstance(value, (Sequence, Values)):
        raise SimpleBenchTypeError(
            f"measurements must be a Sequence of float, a Values instance, or None, got {type(value)}",
            tag=_StatsBlockErrorTag.INVALID_MEASUREMENTS_TYPE)
    if len(value) < 3:
        raise SimpleBenchValueError(
            "measurements must contain at least 3 values or statistics cannot be computed",
            tag=_StatsBlockErrorTag.TOO_FEW_MEASUREMENTS)

    # Values instances don't need further validation because they are already validated
    if isinstance(value, Values):
        return value

    # This check only runs if value is a Sequence (not a Values instance)
    if not all(isinstance(v, float) for v in value):
        raise SimpleBenchTypeError(
            "All items in measurements must be of type float",
            tag=_StatsBlockErrorTag.INVALID_MEASUREMENTS_CONTENT_TYPE)
    return Values(value)


def name(value: str) -> str:
    """Validates that name is a non-blank string.

    :param str value: The value to validate.
    :return str: The validated string value.
    :raise SimpleBenchTypeError: If the value is not a string.
    :raise SimpleBenchValueError: If the value is blank.
    """
    return validate_string(
                value, 'name',
                _StatsBlockErrorTag.INVALID_NAME_TYPE,
                _StatsBlockErrorTag.INVALID_NAME_VALUE,
                allow_blank=False)


def rounds(value: int) -> int:
    """Validates that rounds is a positive integer.

    :param int value: The value to validate.
    :return int: The validated positive integer value.
    :raise SimpleBenchTypeError: If the value is not an integer.
    :raise SimpleBenchValueError: If the value is not positive.
    """
    return validate_positive_int(
                value, "rounds",
                _StatsBlockErrorTag.INVALID_ROUNDS_TYPE,
                _StatsBlockErrorTag.INVALID_ROUNDS_VALUE)


def iterations(value: int | None, measurements_value: Values | None) -> int | None:
    """Validates that iterations is a positive integer.

    :param int | None value: The value to validate.
    :return int | None: The validated positive integer value.
    :raise SimpleBenchTypeError: If the value is not an integer.
    :raise SimpleBenchValueError: If the value is not positive.
    """
    if value is None:
        return None
    if measurements_value is not None:
        raise SimpleBenchTypeError(
            "iterations cannot be provided when measurements are provided",
            tag=_StatsBlockErrorTag.ITERATIONS_AND_MEASUREMENTS_PROVIDED)
    return validate_positive_int(
                value, "iterations",
                _StatsBlockErrorTag.INVALID_ITERATIONS_TYPE,
                _StatsBlockErrorTag.INVALID_ITERATIONS_VALUE)


def percentiles(value: Values | Sequence[float | int] | None, measurements_value: Values | None) -> Values | None:
    """Validates that percentiles is a sequence of floats or ints or None.

    :param Values | Sequence[float | int] | None value: The value to validate.
    :return Values | None: None, or a validated Values object containing floats.
    :raise SimpleBenchTypeError: If the value is not None or a sequence of floats or ints.
    :raise SimpleBenchValueError: If the value is not a sequence of 101 numbers or not sorted in ascending order.
    """
    if value is None:
        return None
    if measurements_value is not None:
        raise SimpleBenchTypeError(
            "percentiles cannot be provided when measurements are provided",
            tag=_StatsBlockErrorTag.PERCENTILES_AND_MEASUREMENTS_PROVIDED)

    # If the value is not already a Values object, validate it as a sequence of numbers
    # and convert it to a Values object containing floats
    if not isinstance(value, Values):
        validated_list = validate_sequence_of_numbers(
                value, "percentiles",
                _StatsBlockErrorTag.INVALID_PERCENTILES_TYPE,
                _StatsBlockErrorTag.INVALID_PERCENTILES_CONTENT_TYPE,
                allow_empty=False)
        validated_values = Values(float(x) for x in validated_list)

    else:
        validated_values = value

    # Verify that the percentiles list has exactly 101 items
    if len(validated_values) != 101:
        raise SimpleBenchValueError(
            "percentiles must be a sequence of 101 numbers",
            tag=_StatsBlockErrorTag.INVALID_PERCENTILES_LENGTH)

    # Verify that the percentiles are sorted in ascending order
    if Values(sorted(validated_values)) != validated_values:
        raise SimpleBenchValueError(
            "percentiles must be sorted in ascending order",
            tag=_StatsBlockErrorTag.INVALID_PERCENTILES_ORDER)

    return validated_values


def relative_stdev(value: float | None, measurements_value: Values | None) -> float | None:
    """Validates that relative_stdev is a float or None.

    It also checks that it is non-negative if it is not None.

    :param float | None value: The value to validate.
    :return float | None: The validated float value or None.
    :raise SimpleBenchTypeError: If the value is not a float.
    :raise SimpleBenchValueError: If the value is negative.
    """
    if value is None:
        return None
    if measurements_value is not None:
        raise SimpleBenchTypeError(
            "relative_stdev cannot be provided when measurements are provided",
            tag=_StatsBlockErrorTag.RELATIVE_STDEV_AND_MEASUREMENTS_PROVIDED)
    return validate_non_negative_float(
            value, 'relative_stdev',
            _StatsBlockErrorTag.INVALID_RELATIVE_STANDARD_DEVIATION_TYPE,
            _StatsBlockErrorTag.INVALID_RELATIVE_STANDARD_DEVIATION_VALUE)


def scale(value: float) -> float:
    """Validate that scale is a positive floating point number (greater than 0).

    :param float value: The value to validate.
    :return float: The validated positive floating point value.
    :raise SimpleBenchTypeError: If the value is not a float.
    :raise SimpleBenchValueError: If the value is not positive.
    """
    return validate_positive_float(
            value, 'scale',
            _StatsBlockErrorTag.INVALID_SCALE_TYPE,
            _StatsBlockErrorTag.INVALID_SCALE_VALUE)


def semantic_type(value: str) -> str:
    """Validate that semantic_type is a valid namespaced identifier

    A namespaced identifier is a string in the format "namespace::identifier"
    where "namespace" and "identifier" are non-blank strings beginning with a letter,
    followed by any combination of letters, digits, or underscores and ending with
    either a letter or a digit.

    :param str value: The value to validate.
    :return str: The validated namespaced identifier.
    :raise SimpleBenchTypeError: If the value is not a string.
    :raise SimpleBenchValueError: If the value is not a valid namespaced identifier.
    """
    return validate_namespaced_identifier(
                value, "semantic_type",
                _StatsBlockErrorTag.INVALID_SEMANTIC_TYPE_TYPE,
                _StatsBlockErrorTag.INVALID_SEMANTIC_TYPE_VALUE)


def stdev(value: float | None, measurements_value: Values | None) -> float | None:
    """Validates that stdev is a float or None.

    It also checks that it is non-negative if it is not None.

    :param float | None value: The value to validate.
    :return float | None: The validated float value or None.
    :raise SimpleBenchTypeError: If the value is not a float.
    :raise SimpleBenchValueError: If the value is negative.
    """
    if value is None:
        return None
    if measurements_value is not None:
        raise SimpleBenchTypeError(
            "stdev cannot be provided when measurements are provided",
            tag=_StatsBlockErrorTag.STDEV_AND_MEASUREMENTS_PROVIDED)
    return validate_non_negative_float(
            value, 'stdev',
            _StatsBlockErrorTag.INVALID_STANDARD_DEVIATION_TYPE,
            _StatsBlockErrorTag.INVALID_STANDARD_DEVIATION_VALUE)


def unit(value: str) -> str:
    """Validates that unit is a non-blank string.

    :param str value: The value to validate.
    :return str: The validated string value.
    :raise SimpleBenchTypeError: If the value is not a string.
    :raise SimpleBenchValueError: If the value is blank.
    """
    return validate_string(
                value, 'unit',
                _StatsBlockErrorTag.INVALID_UNIT_TYPE,
                _StatsBlockErrorTag.INVALID_UNIT_VALUE,
                allow_blank=False)
