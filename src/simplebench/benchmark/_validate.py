"""Validation utilities for benchmarks."""

from simplebench.exceptions import SimpleBenchTypeError, SimpleBenchValueError
from simplebench.simplebench_types import KWArgsVariations
from simplebench.validators import validate_non_blank_string

from ._error_tags import _BenchmarkErrorTag


def title(value: str | None) -> str | None:
    """Validate a benchmark title.

    :param value: The title to validate.
    :type value: str | None
    :returns: The validated title.
    :rtype: str | None
    :raises SimpleBenchTypeError: If the title is not a string or None.
    :raises SimpleBenchValueError: If the title is blank.
    """
    if value is None:
        return value
    return validate_non_blank_string(
        value,
        "Benchmark title",
        _BenchmarkErrorTag.BENCHMARK_TITLE_TYPE,
        _BenchmarkErrorTag.BENCHMARK_TITLE_VALUE)


def description(value: str | None) -> str | None:
    """Validate a benchmark description.

    :param value: The description to validate.
    :type value: str | None
    :returns: The validated description.
    :rtype: str | None
    :raises SimpleBenchTypeError: If the description is not a string or None.
    :raises SimpleBenchValueError: If the description is blank.
    """
    if value is None:
        return value
    return validate_non_blank_string(
        value,
        "Benchmark description",
        _BenchmarkErrorTag.BENCHMARK_DESCRIPTION_TYPE,
        _BenchmarkErrorTag.BENCHMARK_DESCRIPTION_VALUE)


def use_field_for_n(
        value: str | None, kwargs_variations_value: KWArgsVariations) -> str | None:
    """Validate the `use_field_for_n` parameter.

    :param value: The `use_field_for_n` value to validate.
    :type value: str | None
    :param kwarg_variations_value: The `kwarg_variations` value to validate against.
    :type kwarg_variations_value: KWArgsVariations
    :returns: The validated `use_field_for_n` value.
    :rtype: str | None
    :raises SimpleBenchTypeError: If the value is not a string or None.
    :raises SimpleBenchValueError: If the value is not a valid field name in `kwarg_variations`.
    """
    if use_field_for_n is None:
        return None

    if not isinstance(value, str):
        raise SimpleBenchTypeError(
            "The 'use_field_for_n' parameter to the @benchmark decorator must be a string if passed.",
            tag=_BenchmarkErrorTag.BENCHMARK_USE_FIELD_FOR_N_TYPE,
        )

    if isinstance(value, str) and isinstance(kwargs_variations_value, dict):
        if value not in kwargs_variations_value:
            raise SimpleBenchValueError(
                "The 'use_field_for_n' parameter to the @benchmark decorator must "
                f'match one of the kwargs_variations keys: {list(kwargs_variations_value.keys())!r}',
                tag=_BenchmarkErrorTag.BENCHMARK_USE_FIELD_FOR_N_KWARGS_VARIATIONS,
            )
        if not all(isinstance(v, int | float) and v > 0 for v in kwargs_variations_value[value]):
            raise SimpleBenchValueError(
                f"The values for the '{value}' entry in 'kwargs_variations' "
                "must all be positive integers or floats when used with 'use_field_for_n'.",
                tag=_BenchmarkErrorTag.BENCHMARK_USE_FIELD_FOR_N_INVALID_VALUE,
            )
    return value
