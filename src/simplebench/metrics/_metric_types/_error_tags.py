"""Error tags for the MetricTypes class"""

from enum import auto
from simplebench.doc_utils import enum_docstrings
from simplebench.exceptions import ErrorTag

__all__: list[str] = []


@enum_docstrings
class _MetricTypesErrorTag(ErrorTag):
    """Error tags for the Metrics class"""

    NOT_A_METRIC_TYPE = auto()
    """Value is not a MetricType object"""
    INVALID_KEY_FORMAT = auto()
    """Invalid key format for a metric key"""
    NOT_ITERABLE_ERROR = auto()
    """Error when trying to iterate over a non-iterable object"""
    TYPE_ERROR = auto()
    """Type error when trying to set a metric value"""
    MISMATCHED_KEY = auto()
    """Key in metric does not match the expected key"""
    DUPLICATE_KEY = auto()
    """Duplicate key in metrics list"""
    INVALID_METRICS_LIST_TYPE = auto()
    """metrics parameter is not a list"""
    INVALID_METRICS_LIST_ITEM_TYPE = auto()
    """An item in the metrics parameter is not a MetricType object"""
