"""Error tags for metrics."""

from simplebench.doc_utils import enum_docstrings
from simplebench.exceptions import ErrorTag


@enum_docstrings
class _MetricErrorTag(ErrorTag):
    """Error tags for metrics."""

    INVALID_LABEL_FIELD_TYPE = 'INVALID_LABEL_FIELD_TYPE'
    """'label' must be a string."""
    INVALID_LABEL_FIELD_VALUE = 'INVALID_LABEL_FIELD_VALUE'
    """'label' must be a non-empty string.

    It must
    - Start with an uppercase letter.
    - Contain only uppercase alphanumeric characters and underscores.
    - End with an uppercase letter or a digit.
    """
    INVALID_DESCRIPTION_FIELD = 'INVALID_DESCRIPTION_FIELD'
    """'description' must be a string."""
    INVALID_TITLE_FIELD_TYPE = 'INVALID_TITLE_FIELD_TYPE'
    """title' must be a string."""
    INVALID_TITLE_FIELD_VALUE = 'INVALID_TITLE_FIELD_VALUE'
    """title' must be a non-empty, non-blank string."""
    INVALID_METRIC_TYPE_FIELD_TYPE = 'INVALID_METRIC_TYPE_FIELD_TYPE'
    """metric_type' must be a string."""
    INVALID_METRIC_TYPE_FIELD_VALUE = 'INVALID_METRIC_TYPE_FIELD_VALUE'
    """metric_type' must be a registered metric type."""
    NOT_REGISTERED_METRIC_TYPE = 'NOT_REGISTERED_METRIC_TYPE'
    """The metric type is not registered."""
    INVALID_METRIC_TYPE = 'INVALID_METRIC_TYPE'
    """The metric type is invalid."""
