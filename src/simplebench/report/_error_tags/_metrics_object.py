"""Metrics exceptions for JSON report v1."""

from simplebench.doc_utils import enum_docstrings
from simplebench.exceptions import ErrorTag

__all__: list[str] = []


@enum_docstrings
class _MetricsObjectErrorTag(ErrorTag):
    """Error tags for JSON Metrics v1 exceptions."""

    KEY_ERROR_INVALID_METRIC_NAME_VALUE = 'KEY_ERROR_INVALID_METRIC_NAME_VALUE'
    """The metric name key does not exist in metrics."""
    METRICS_OBJECT_IMMUTABLE = 'METRICS_OBJECT_IMMUTABLE'
    """The MetricsObject is immutable and cannot be modified after initialization."""
    INVALID_METRIC_ITEM_SEMANTIC_TYPE = 'INVALID_METRIC_ITEM_SEMANTIC_TYPE'
    """The semantic type of a metric item is invalid."""
    INVALID_VERSION_TYPE = 'INVALID_VERSION_TYPE'
    """The version is not of type int."""
    UNSUPPORTED_VERSION = 'UNSUPPORTED_VERSION'
    """The version is not supported."""
    INVALID_VARIATION_COLS_TYPE = 'INVALID_VARIATION_COLS_TYPE'
    """The variation_cols is not of type dict."""
    INVALID_VARIATION_COLS_CONTENT = 'INVALID_VARIATION_COLS_CONTENT'
    """One or more keys or values in variation_cols are not strings."""
    INVALID_METRICS_TYPE = 'INVALID_METRICS_TYPE'
    """The metrics is not of type list."""
    INVALID_METRICS_CONTENT = 'INVALID_METRICS_CONTENT'
    INVALID_N_TYPE = 'INVALID_N_TYPE'
    """The n is not of type float."""
    INVALID_N_VALUE = 'INVALID_N_VALUE'
    """The n has an invalid value. Must be >= 1.0"""
    INVALID_GROUP_TYPE = 'INVALID_GROUP_TYPE'
    """The group is not of type string."""
    INVALID_GROUP_VALUE_EMPTY_STRING = 'INVALID_GROUP_VALUE_EMPTY_STRING'
    """The group has an invalid value. Cannot be an empty string."""
    INVALID_TITLE_TYPE = 'INVALID_TITLE_TYPE'
    """The title is not of type string."""
    INVALID_TITLE_VALUE_EMPTY_STRING = 'INVALID_TITLE_VALUE_EMPTY_STRING'
    """The title has an invalid value. Cannot be an empty string."""
    INVALID_DESCRIPTION_TYPE = 'INVALID_DESCRIPTION_TYPE'
    """The description is not of type string."""
    INVALID_DESCRIPTION_EMPTY_STRING = 'INVALID_DESCRIPTION_EMPTY_STRING'
    """The description has an invalid value. Cannot be an empty string."""
    INVALID_TYPE_TYPE = 'INVALID_TYPE_TYPE'
    """The type is not of type string."""
    INVALID_TYPE_VALUE = 'INVALID_TYPE_VALUE'
    """The type has an invalid value."""
    INVALID_DATA_ARG_EXTRA_KEYS = 'INVALID_DATA_ARG_EXTRA_KEYS'
    """The data argument contains unexpected extra keys."""
    INVALID_DATA_ARG_MISSING_KEYS = 'INVALID_DATA_ARG_MISSING_KEYS'
    """The data argument is missing required keys."""
    INVALID_METRIC_NAME_TYPE = 'INVALID_METRIC_NAME_TYPE'
    """A metric name is not a string."""
    INVALID_METRIC_NAME_VALUE = 'INVALID_METRIC_NAME_VALUE'
    """A metric name does not match the required pattern."""
    INVALID_METRIC_ITEM_TYPE = 'INVALID_METRIC_ITEM_TYPE'
    """A metric item is not of type StatsBlock or ValueBlock."""
