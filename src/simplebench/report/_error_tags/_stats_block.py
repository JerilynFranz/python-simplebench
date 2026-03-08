"""Exceptions for JSON stats summary report."""

from enum import auto
from simplebench.doc_utils import enum_docstrings
from simplebench.exceptions import ErrorTag

__all__: list[str] = []


@enum_docstrings
class _StatsBlockErrorTag(ErrorTag):
    """Error tags for JSON stats summary exceptions."""

    INVALID_HASH_ID_TYPE = auto()
    """The hash_id is not a string."""
    INVALID_HASH_ID_VALUE = auto()
    """The hash_id has an invalid value."""
    INVALID_HASH_ID_STRUCTURE = auto()
    """The hash_id has an invalid structure. It must be a 64-character hexadecimal string or empty."""
    INVALID_TIMER_TYPE = auto()
    """The timer is not a string or None."""
    INVALID_TIMER_VALUE = auto()
    """The timer has an invalid value (cannot be empty)."""
    MEDIAN_AND_MEASUREMENTS_PROVIDED = auto()
    """Both median and measurements were provided, but only one is allowed."""
    MEAN_AND_MEASUREMENTS_PROVIDED = auto()
    """Both mean and measurements were provided, but only one is allowed."""
    STDEV_AND_MEASUREMENTS_PROVIDED = auto()
    """Both standard_deviation and measurements were provided, but only one is allowed."""
    RELATIVE_STDEV_AND_MEASUREMENTS_PROVIDED = auto()
    """Both relative_standard_deviation and measurements were provided, but only one is allowed."""
    PERCENTILES_AND_MEASUREMENTS_PROVIDED = auto()
    """Both percentiles and measurements were provided, but only one is allowed."""
    MINIMUM_AND_MEASUREMENTS_PROVIDED = auto()
    """Both minimum and measurements were provided, but only one is allowed."""
    MAXIMUM_AND_MEASUREMENTS_PROVIDED = auto()
    """Both maximum and measurements were provided, but only one is allowed."""
    ITERATIONS_AND_MEASUREMENTS_PROVIDED = auto()
    """Both iterations and measurements were provided, but only one is allowed."""
    INVALID_STATS_BLOCK_ARGUMENTS = auto()
    """The arguments provided to StatsBlock are invalid."""
    INVALID_PERCENTILES_ORDER = auto()
    """The percentiles are not sorted in ascending order."""
    INVALID_MEASUREMENTS_STATE = auto()
    """The measurements property is in an invalid state for the requested operation."""
    INVALID_SEMANTIC_TYPE_TYPE = auto()
    """The semantic_type is not a string."""
    INVALID_SEMANTIC_TYPE_VALUE = auto()
    """The semantic_type is not a valid namespaced identifier."""
    IMMUTABLE_VIOLATION = auto()
    """The measurements property is immutable once set."""
    TOO_FEW_MEASUREMENTS = auto()
    """There are too few measurements to compute statistics."""
    ITERATIONS_INCONSISTENT_WITH_MEASUREMENTS = auto()
    """The number of iterations does not match the number of measurements."""
    LAZY_PROPERTY_REQUIREMENTS_ERROR = auto()
    """A lazy property cannot be computed because its requirements are not met."""
    INVALID_MEASUREMENTS_TYPE = auto()
    """The measurements is not a Sequence or None."""
    INVALID_MEASUREMENTS_CONTENT_TYPE = auto()
    """One or more items in measurements are not of type float."""
    JSON_SCHEMA_VALIDATION_ERROR = auto()
    """The JSON data does not conform to the expected schema."""
    INVALID_DATA_ARG_EXTRA_KEYS = auto()
    """The data argument contains extra keys."""
    INVALID_DATA_ARG_MISSING_KEYS = auto()
    """The data argument is missing required keys."""
    INVALID_DATA_ARG_TYPE = auto()
    """The data argument is not of type dict."""
    INVALID_NAME_TYPE = auto()
    """The name is not of type string."""
    INVALID_NAME_VALUE = auto()
    """The name has an invalid value. Cannot be an empty string."""
    INVALID_DESCRIPTION_TYPE = auto()
    """The description is not of type string."""
    INVALID_DESCRIPTION_VALUE = auto()
    """The description has an invalid value."""
    INVALID_PERCENTILES_LENGTH = auto()
    """The percentiles list is not 101 items long."""
    INVALID_TYPE_TYPE = auto()
    """The type is not of type string."""
    INVALID_TYPE_VALUE = auto()
    """The type has an invalid value."""
    INVALID_UNIT_TYPE = auto()
    """The unit is not of type string."""
    INVALID_UNIT_VALUE = auto()
    """The unit has an invalid value. Cannot be an empty string."""
    INVALID_SCALE_TYPE = auto()
    """The scale is not of type float."""
    INVALID_SCALE_VALUE = auto()
    """The scale has an invalid value. Must be > 0.0"""
    INVALID_N_TYPE = auto()
    """The n is not of type integer."""
    INVALID_N_VALUE = auto()
    """The n has an invalid value. Must be >= 0."""
    INVALID_ITERATIONS_TYPE = auto()
    """The iterations is not of type integer."""
    INVALID_ITERATIONS_VALUE = auto()
    """The iterations has an invalid value. Must be >= 1."""
    INVALID_ROUNDS_TYPE = auto()
    """The rounds is not of type integer."""
    INVALID_ROUNDS_VALUE = auto()
    """The rounds has an invalid value. Must be >= 1."""
    INVALID_MEAN_TYPE = auto()
    """The mean is not of type float."""
    INVALID_MEDIAN_TYPE = auto()
    """The median is not of type float."""
    INVALID_MINIMUM_TYPE = auto()
    """The minimum is not of type float."""
    INVALID_MAXIMUM_TYPE = auto()
    """The maximum is not of type float."""
    INVALID_STANDARD_DEVIATION_TYPE = auto()
    """The standard_deviation is not of type float."""
    INVALID_STANDARD_DEVIATION_VALUE = auto()
    """The standard_deviation has an invalid value. Must be >= 0."""
    INVALID_RELATIVE_STANDARD_DEVIATION_TYPE = auto()
    """The relative_standard_deviation is not of type float."""
    INVALID_RELATIVE_STANDARD_DEVIATION_VALUE = auto()
    """The relative_standard_deviation has an invalid value. Must be >= 0."""
    INVALID_PERCENTILES_TYPE = auto()
    """The percentiles is not a Sequence."""
    INVALID_PERCENTILES_CONTENT_TYPE = auto()
    """One or more items in percentiles are not of type float or int."""
    INVALID_VERSION_TYPE = auto()
    """The version is not of type integer."""
    UNSUPPORTED_VERSION = auto()
    """The version is not supported."""
    INVALID_DRIFT_INDEX_TYPE = auto()
    """The drift_index is not of type float."""
    INVALID_DRIFT_INDEX_VALUE = auto()
    """The drift_index has an invalid value. Must be in [-1.0, 1.0]."""
    DRIFT_INDEX_AND_MEASUREMENTS_PROVIDED = auto()
    """Both drift_index and measurements were provided, but only one is allowed."""
    INVALID_AUTOCORRELATION_TYPE = auto()
    """The autocorrelation is not of type float."""
    INVALID_AUTOCORRELATION_VALUE = auto()
    """The autocorrelation has an invalid value. Must be in [-1.0, 1.0]."""
    AUTOCORRELATION_AND_MEASUREMENTS_PROVIDED = auto()
    """Both autocorrelation and measurements were provided, but only one is allowed."""
