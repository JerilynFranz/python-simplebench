"""Metrics exceptions for JSON report v1."""

from enum import auto
from simplebench.doc_utils import enum_docstrings
from simplebench.exceptions import ErrorTag

__all__: list[str] = []


@enum_docstrings
class _MetricsObjectErrorTag(ErrorTag):
    """Error tags for JSON Metrics v1 exceptions."""

    KEY_ERROR_INVALID_METRIC_NAME_VALUE = auto()
    """The metric name key does not exist in metrics."""
    METRICS_OBJECT_IMMUTABLE = auto()
    """The MetricsObject is immutable and cannot be modified after initialization."""
    INVALID_METRIC_ITEM_SEMANTIC_TYPE = auto()
    """The semantic type of a metric item is invalid."""
    INVALID_VERSION_TYPE = auto()
    """The version is not of type int."""
    UNSUPPORTED_VERSION = auto()
    """The version is not supported."""
    INVALID_VARIATION_COLS_TYPE = auto()
    """The variation_cols is not of type dict."""
    INVALID_VARIATION_COLS_CONTENT = auto()
    """One or more keys or values in variation_cols are not strings."""
    INVALID_METRICS_TYPE = auto()
    """The metrics is not of type list."""
    INVALID_METRICS_CONTENT = auto()
    INVALID_N_TYPE = auto()
    """The n is not of type float."""
    INVALID_N_VALUE = auto()
    """The n has an invalid value. Must be >= 1.0"""
    INVALID_GROUP_TYPE = auto()
    """The group is not of type string."""
    INVALID_GROUP_VALUE_EMPTY_STRING = auto()
    """The group has an invalid value. Cannot be an empty string."""
    INVALID_TITLE_TYPE = auto()
    """The title is not of type string."""
    INVALID_TITLE_VALUE_EMPTY_STRING = auto()
    """The title has an invalid value. Cannot be an empty string."""
    INVALID_DESCRIPTION_TYPE = auto()
    """The description is not of type string."""
    INVALID_DESCRIPTION_EMPTY_STRING = auto()
    """The description has an invalid value. Cannot be an empty string."""
    INVALID_TYPE_TYPE = auto()
    """The type is not of type string."""
    INVALID_TYPE_VALUE = auto()
    """The type has an invalid value."""
    INVALID_DATA_ARG_EXTRA_KEYS = auto()
    """The data argument contains unexpected extra keys."""
    INVALID_DATA_ARG_MISSING_KEYS = auto()
    """The data argument is missing required keys."""
    INVALID_METRIC_NAME_TYPE = auto()
    """A metric name is not a string."""
    INVALID_METRIC_NAME_VALUE = auto()
    """A metric name does not match the required pattern."""
    INVALID_METRIC_ITEM_TYPE = auto()
    """A metric item is not of type StatsBlock or ValueBlock."""
