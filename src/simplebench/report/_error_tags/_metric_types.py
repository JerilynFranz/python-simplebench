"""Error tags for the MetricTypes class"""

from enum import auto
from simplebench.doc_utils import enum_docstrings
from simplebench.exceptions import ErrorTag

__all__: list[str] = []


@enum_docstrings
class _MetricTypesErrorTag(ErrorTag):
    """Error tags for the MetricTypes class"""

    INCOMPARABLE_TYPE = auto()
    """Error when trying to compare a MetricTypes object with an object of an incompatible type"""
    INVALID_METRICS_FIELD_TYPE = auto()
    """Error when the value provided for the metrics field is not a valid type"""
    INVALID_METRIC_TYPE_LABEL = auto()
    """Error when a metric type label is invalid (e.g. does not match the required pattern)"""
    INVALID_METRIC_TYPES_FIELD_TYPE = auto()
    """Error when the value provided for the metric_types field is not a valid type"""
    METRIC_TYPE_NOT_FOUND = auto()
    """Error when trying to access a metric type that does not exist in the MetricTypes object"""
    MAPPING_IMMUTABLE = auto()
    """Error when trying to modify the mapping of a MetricTypes object"""
    INVALID_ADDEND_TYPE = auto()
    """Error when trying to add a non-MetricTypes or non-MetricType object to
    a MetricTypes object"""
    INVALID_SUBTRAHEND_TYPE = auto()
    """Error when trying to subtract a non-MetricTypes or non-MetricType object
    from a MetricTypes object"""
    DUPLICATE_METRIC_TYPE_LABEL = auto()
    """Error when trying to add a MetricType with a label that already exists
    in the MetricTypes object"""
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
    INVALID_METRICS_LIST_ITEM_TYPE = auto()
    """An item in the metrics parameter is not a MetricType object"""
