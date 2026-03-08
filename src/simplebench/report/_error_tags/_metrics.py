"""Error tags for the MetricTypes class"""

from enum import auto
from simplebench.doc_utils import enum_docstrings
from simplebench.exceptions import ErrorTag

__all__: list[str] = []


@enum_docstrings
class _MetricsErrorTag(ErrorTag):
    """Error tags for the Metrics class"""

    OPERAND_TYPE_ERROR = auto()
    """The other object is not a Metrics instance for comparison."""
    INVALID_SUBTRAHEND_TYPE = auto()
    """Invalid type for subtrahend in Metrics subtraction. Expected Metrics or Metric instance."""
    INVALID_ADDEND_TYPE = auto()
    """Invalid type for addend in Metrics addition. Expected Metrics or Metric instance."""
    MAPPING_IMMUTABLE = auto()
    """The mapping of metrics is immutable and cannot be modified."""
    DUPLICATE_METRIC_LABEL = auto()
    """Duplicate metric label found in metrics iterable."""
    INVALID_METRICS_FIELD_TYPE = auto()
    """The 'metrics' field must be an iterable of Metric instances or a Metrics instance."""
    MISMATCHED_KEY = auto()
    """Key in metric does not match the expected key"""
    DUPLICATE_KEY = auto()
    """Duplicate key in metrics list"""
    METRIC_NOT_FOUND = auto()
    """Requested metric not found in Metrics object"""

