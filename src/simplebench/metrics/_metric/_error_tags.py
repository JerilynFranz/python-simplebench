"""Error tags for metrics."""

from enum import auto
from simplebench.doc_utils import enum_docstrings
from simplebench.exceptions import ErrorTag


@enum_docstrings
class _MetricErrorTag(ErrorTag):
    """Error tags for metrics."""

    INVALID_LABEL_FIELD_TYPE = auto()
    """'label' must be a string."""
    INVALID_LABEL_FIELD_VALUE = auto()
    """'label' must be a non-empty string.

    It must
    - Start with an uppercase letter.
    - Contain only uppercase alphanumeric characters and underscores.
    - End with an uppercase letter or a digit.
    """
    INVALID_DESCRIPTION_FIELD = auto()
    """'description' must be a string."""
    INVALID_TITLE_FIELD_TYPE = auto()
    """title' must be a string."""
    INVALID_TITLE_FIELD_VALUE = auto()
    """title' must be a non-empty, non-blank string."""
    INVALID_METRIC_TYPE_FIELD_TYPE = auto()
    """metric_type' must be a string."""
    INVALID_METRIC_TYPE_FIELD_VALUE = auto()
    """metric_type' must be a registered metric type."""
    NOT_REGISTERED_METRIC_TYPE = auto()
    """The metric type is not registered."""
    INVALID_METRIC_TYPE = auto()
    """The metric type is invalid."""
