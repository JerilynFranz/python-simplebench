"""Error tags for the MetricTypes class"""

from simplebench.doc_utils import enum_docstrings
from simplebench.exceptions import ErrorTag

__all__: list[str] = []


@enum_docstrings
class _MetricTypesErrorTag(ErrorTag):
    """Error tags for the MetricTypes class"""

    INCOMPARABLE_TYPE = 'INCOMPARABLE_TYPE'
    """Error when trying to compare a MetricTypes object with an object of an incompatible type"""
    INVALID_METRICS_FIELD_TYPE = 'INVALID_METRICS_FIELD_TYPE'
    """Error when the value provided for the metrics field is not a valid type"""
    INVALID_METRIC_TYPE_LABEL = 'INVALID_METRIC_TYPE_LABEL'
    """Error when a metric type label is invalid (e.g. does not match the required pattern)"""
    INVALID_METRIC_TYPES_FIELD_TYPE = 'INVALID_METRIC_TYPES_FIELD_TYPE'
    """Error when the value provided for the metric_types field is not a valid type"""
    METRIC_TYPE_NOT_FOUND = 'METRIC_TYPE_NOT_FOUND'
    """Error when trying to access a metric type that does not exist in the MetricTypes object"""
    MAPPING_IMMUTABLE = 'MAPPING_IMMUTABLE'
    """Error when trying to modify the mapping of a MetricTypes object"""
    INVALID_ADDEND_TYPE = 'INVALID_ADDEND_TYPE'
    """Error when trying to add a non-MetricTypes or non-MetricType object to
    a MetricTypes object"""
    INVALID_SUBTRAHEND_TYPE = 'INVALID_SUBTRAHEND_TYPE'
    """Error when trying to subtract a non-MetricTypes or non-MetricType object
    from a MetricTypes object"""
    DUPLICATE_METRIC_TYPE_LABEL = 'DUPLICATE_METRIC_TYPE_LABEL'
    """Error when trying to add a MetricType with a label that already exists
    in the MetricTypes object"""
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
    INVALID_METRICS_LIST_ITEM_TYPE = 'INVALID_METRICS_LIST_ITEM_TYPE'
    """An item in the metrics parameter is not a MetricType object"""
