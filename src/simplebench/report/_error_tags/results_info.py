"""Exceptions for JSONResults"""

from enum import auto

from simplebench.doc_utils import enum_docstrings
from simplebench.exceptions import ErrorTag

__all__: list[str] = []


@enum_docstrings
class _ResultsInfoErrorTag(ErrorTag):
    """Error tags for JSONResults v1 exceptions."""

    INPUT_DATA_NOT_A_MAPPING = auto()
    """The input data for Report.from_dict must be a mapping type (e.g., dict)"""
    INVALID_HASH_ID_TYPE = auto()
    """The hash_id is not of type str."""
    INVALID_HASH_ID_VALUE = auto()
    """The hash_id is not a valid 64-character hexadecimal string."""
    INVALID_VARIATION_MARKS_TYPE = auto()
    """The variation_marks is not of type dict."""
    INVALID_VARIATION_MARKS_CONTENT = auto()
    """One or more keys or values in variation_marks are not strings."""
    INVALID_RESULTS_TYPE = auto()
    """The results is not of type Sequence[case.Results]."""
    INVALID_RESULTS_VALUE = auto()
    """Content of results does not match specified restrictions such as number of items."""
    INVALID_DATA_ARG_TYPE = auto()
    """The data is not of type dict."""
    UNSUPPORTED_VERSION = auto()
    """The version is not supported."""
    INVALID_TYPE_TYPE = auto()
    """The type is not of type string."""
    INVALID_TYPE_VALUE = auto()
    """The type has an invalid value."""
    INVALID_METRICS_TYPE = auto()
    """The metrics is not of type list."""
    INVALID_METRICS_CONTENT = auto()
    """One or more items in metrics are not a valid MetricItem type."""
    INVALID_DATA_ARG_EXTRA_KEYS = auto()
    """The data argument contains unexpected extra keys."""
    INVALID_DATA_ARG_MISSING_KEYS = auto()
    """The data argument is missing required keys."""
    INVALID_OPS_PER_INTERVAL_UNIT_TYPE = auto()
    """The ops_per_interval_unit is not of type string."""
    INVALID_OPS_PER_INTERVAL_UNIT_VALUE = auto()
    """The ops_per_interval_unit has an invalid value. Cannot be an empty string."""
    INVALID_OPS_PER_INTERVAL_SCALE_TYPE = auto()
    """The ops_per_interval_scale is not of type float."""
    INVALID_OPS_PER_INTERVAL_SCALE_VALUE = auto()
    """The ops_per_interval_scale has an invalid value. Must be > 0.0"""
    INVALID_INTERVAL_UNIT_TYPE = auto()
    """The interval_unit is not of type string."""
    INVALID_INTERVAL_UNIT_VALUE = auto()
    """The interval_unit has an invalid value. Cannot be an empty string."""
    INVALID_INTERVAL_SCALE_TYPE = auto()
    """The interval_scale is not of type float."""
    INVALID_INTERVAL_SCALE_VALUE = auto()
    """The interval_scale has an invalid value. Must be > 0.0"""
    INVALID_VARIATION_COLS_TYPE = auto()
    """The variation_cols is not of type dict."""
    INVALID_VARIATION_COLS_CONTENT = auto()
    """One or more keys or values in variation_cols are not strings."""
    INVALID_N_TYPE = auto()
    """The n is not of type float."""
    INVALID_N_VALUE = auto()
    """The n has an invalid value. Must be >= 1.0"""
    INVALID_DESCRIPTION_TYPE = auto()
    """The description is not of type string."""
    INVALID_DESCRIPTION_EMPTY_STRING = auto()
    """The description has an invalid value. Cannot be an empty string."""
    INVALID_TITLE_TYPE = auto()
    """The title is not of type string."""
    INVALID_TITLE_VALUE_EMPTY_STRING = auto()
    """The title has an invalid value. Cannot be an empty string."""
    INVALID_GROUP_TYPE = auto()
    """The group is not of type string."""
    INVALID_GROUP_VALUE_EMPTY_STRING = auto()
    """The group has an invalid value. Cannot be an empty string."""
    INVALID_VERSION_TYPE = auto()
    """The version is not of type integer."""
    INVALID_VERSION_VALUE = auto()
    """The version has an invalid value."""
    MISSING_INIT_IMPLEMENTATION = auto()
    """The __init__ method is not implemented in a subclass."""
    FROM_DICT_INVALID_DATA_TYPE = auto()
    """The input data is not of type dictionary."""
    FROM_DICT_INVALID_DATA_KEYS_TYPE = auto()
    """One or more keys in the input data are not strings."""
    INVALID_EXTRA_INFO_TYPE = auto()
    """The extra_info is not of type Extras."""
