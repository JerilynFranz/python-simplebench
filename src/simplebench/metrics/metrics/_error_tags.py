"""Error tags for the MetricTypes class"""

from simplebench.doc_utils import enum_docstrings
from simplebench.exceptions import ErrorTag

__all__ = []


@enum_docstrings
class _MetricsErrorTag(ErrorTag):
    """Error tags for the Metrics class"""

    ATTRIBUTE_CONFLICT = 'ATTRIBUTE_CONFLICT'
    """Attribute name conflicts with existing Metrics object attribute"""
    NOT_A_METRIC = 'NOT_A_METRIC'
    """Value is not a Metric object"""
    INVALID_KEY_FORMAT = 'INVALID_KEY_FORMAT'
    """Invalid key format for a metric key"""
    NOT_ITERABLE_ERROR = 'NOT_ITERABLE_ERROR'
    """Error when trying to iterate over a non-iterable object"""
    TYPE_ERROR = 'TYPE_ERROR'
    """Type error when trying to set a metric value"""
    MISMATCHED_KEY = 'MISMATCHED_KEY'
    """Key in metric does not match the expected key"""
    DUPLICATE_KEY = 'DUPLICATE_KEY'
    """Duplicate key in metrics list"""
    INVALID_METRICS_LIST_TYPE = 'INVALID_METRICS_LIST_TYPE'
    """metrics parameter is not a list"""
    INVALID_METRICS_LIST_ITEM_TYPE = 'INVALID_METRICS_LIST_ITEM_TYPE'
    """An item in the metrics parameter is not a Metric object"""
    ATTRIBUTE_SET_NOT_ALLOWED = 'ATTRIBUTE_SET_NOT_ALLOWED'
    """Setting attributes on Metrics object is not allowed"""
    METRIC_NOT_FOUND = 'METRIC_NOT_FOUND'
    """Requested metric not found in Metrics object"""

