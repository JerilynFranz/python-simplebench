"""ErrorTags for simplebench.benchmark."""

from enum import auto
from simplebench.doc_utils import enum_docstrings
from simplebench.exceptions import ErrorTag


@enum_docstrings
class _BenchmarkErrorTag(ErrorTag):
    """ErrorTags for simplebench.decorators in SimpleBench."""

    BENCHMARK_CPU_TIMER_TYPE = auto()
    """Something other than a callable was passed as the cpu_timer"""
    BENCHMARK_CPU_TIMER_RETURN_TYPE = auto()
    """The callable passed as the cpu_timer did not return an int"""
    BENCHMARK_TIMER_TYPE = auto()
    """Something other than a callable was passed as the timer"""
    BENCHMARK_TIMER_RETURN_TYPE = auto()
    """The callable passed as the timer did not return an int"""
    BENCHMARK_GROUP_TYPE = auto()
    """Something other than a str was passed as the group"""
    BENCHMARK_GROUP_VALUE = auto()
    """The group must be a non-empty string"""
    BENCHMARK_TITLE_TYPE = auto()
    """Something other than a str was passed as the title"""
    BENCHMARK_TITLE_VALUE = auto()
    """The title must be a non-empty string"""
    BENCHMARK_ID_TYPE = auto()
    """Something other than a str was passed as the benchmark_id"""
    BENCHMARK_ID_VALUE = auto()
    """The benchmark_id must be a non-empty string"""
    BENCHMARK_DESCRIPTION_TYPE = auto()
    """Something other than a str was passed as the description"""
    BENCHMARK_DESCRIPTION_VALUE = auto()
    """The description must be a non-empty string"""
    BENCHMARK_ITERATIONS_TYPE = auto()
    """Something other than an int was passed as the iterations"""
    BENCHMARK_ITERATIONS_VALUE = auto()
    """The iterations must be a positive integer"""
    BENCHMARK_WARMUP_ITERATIONS_TYPE = auto()
    """Something other than an int was passed as the warmup_iterations"""
    BENCHMARK_WARMUP_ITERATIONS_VALUE = auto()
    """The warmup_iterations must be a non-negative integer"""
    BENCHMARK_ROUNDS_TYPE = auto()
    """Something other than an int was passed as the rounds"""
    BENCHMARK_ROUNDS_VALUE = auto()
    """The rounds must be a positive integer"""
    BENCHMARK_MIN_TIME_TYPE = auto()
    """Something other than a float was passed as the min_time"""
    BENCHMARK_MIN_TIME_VALUE = auto()
    """The min_time must be a positive float"""
    BENCHMARK_MAX_TIME_TYPE = auto()
    """Something other than a float was passed as the max_time"""
    BENCHMARK_MAX_TIME_VALUE = auto()
    """The max_time must be a positive float"""
    BENCHMARK_MAX_TIME_LESS_THAN_MIN_TIME = auto()
    """The max_time must be greater than or equal to min_time"""
    BENCHMARK_TIMEOUT_TYPE = auto()
    """Something other than a float or None was passed as the timeout"""
    BENCHMARK_TIMEOUT_VALUE = auto()
    """The timeout must be a positive float or None"""
    BENCHMARK_TIMEOUT_CANNOT_BE_ZERO_OR_NEGATIVE = auto()
    """The timeout must be greater than zero if provided"""
    BENCHMARK_VARIATION_COLS_TYPE = auto()
    """Something other than a dict was passed as the variation_cols"""
    BENCHMARK_VARIATION_COLS_VALUE = auto()
    """The variation_cols must be a non-empty dictionary"""
    BENCHMARK_KWARGS_VARIATIONS_TYPE = auto()
    """Something other than a dict was passed as the kwargs_variations"""
    BENCHMARK_KWARGS_VARIATIONS_VALUE = auto()
    """The kwargs_variations must be a non-empty dictionary"""
    BENCHMARK_OPTIONS_TYPE = auto()
    """Something other than a list was passed as the options"""
    BENCHMARK_OPTIONS_VALUE = auto()
    """The options must be a non-empty list"""
    BENCHMARK_N_TYPE = auto()
    """Something other than an int or floatwas passed as the n"""
    BENCHMARK_N_VALUE = auto()
    """The n must be a positive integer or float value"""
    BENCHMARK_USE_FIELD_FOR_N_TYPE = auto()
    """Something other than a str was passed as the use_field_for_n"""
    BENCHMARK_USE_FIELD_FOR_N_VALUE = auto()
    """The use_field_for_n must be a non-empty string"""
    BENCHMARK_N_FOR_RUN_INVALID_VALUE = auto()
    """The 'n' value determined for the benchmark run must be a positive integer."""
    BENCHMARK_USE_FIELD_FOR_N_KWARGS_VARIATIONS = auto()
    """The use_field_for_n must be a key in kwargs_variations"""
    BENCHMARK_USE_FIELD_FOR_N_VALUES = auto()
    """If use_field_for_n is provided, the matching kwargs_variations field must have positive integer values only"""
    BENCHMARK_KWARGS_VARIATIONS_KEY_TYPE = auto()
    """Something other than a str was passed as the key in kwargs_variations"""
    BENCHMARK_KWARGS_VARIATIONS_KEY_VALUE = auto()
    """The keys in kwargs_variations must be non-empty strings."""
    BENCHMARK_KWARGS_VARIATIONS_VALUE_TYPE = auto()
    """Something other than a list was passed as the value in kwargs_variations"""
    BENCHMARK_KWARGS_VARIATIONS_VALUE_VALUE = auto()
    """The values for each key in kwargs_variations must be a list of values, and cannot be an empty list."""
    BENCHMARK_VARIATION_COLS_KEY_TYPE = auto()
    """Something other than a str was passed as the key in variation_cols"""
    BENCHMARK_VARIATION_COLS_KEY_VALUE = auto()
    """The keys in variation_cols must be non-empty strings."""
    BENCHMARK_VARIATION_COLS_VALUE_TYPE = auto()
    """Something other than a non-empty str was passed as the value in variation_cols"""
    BENCHMARK_VARIATION_COLS_VALUE_VALUE = auto()
    """The values in variation_cols must be non-empty strings."""
    BENCHMARK_VARIATION_COLS_KWARGS_VARIATIONS = auto()
    """The 'variation_cols' parameter to the @benchmark decorator requires "
    that 'kwargs_variations' also be provided."""
    BENCHMARK_VARIATION_COLS_KWARGS_VARIATIONS_MISMATCH = auto()
    """The keys in variation_cols must also be present in kwargs_variations."""
    BENCHMARK_USE_FIELD_FOR_N_INVALID_VALUE = auto()
    """The value in kwargs_variations for the key specified in use_field_for_n must be a positive float or integer."""
    BENCHMARK_USE_FIELD_FOR_N_MISSING_IN_RUNNER = auto()
    """The use_field_for_n parameter was specified, but the matching field is missing
    from the kwargs from the runner."""
