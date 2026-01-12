"""Error tags for metric type issues."""

from simplebench.doc_utils import enum_docstrings
from simplebench.exceptions import ErrorTag


@enum_docstrings
class _MetricTypeErrorTag(ErrorTag):
    """Error tags for metric definition issues."""

    INVALID_CATEGORY_FIELD_VALUE = 'INVALID_CATEGORY_FIELD_VALUE'
    """category field is not a valid metric category value"""
    INVALID_META_METRIC_FIELD_TYPE = 'INVALID_META_METRIC_FIELD_TYPE'
    """meta_metric field is not of type boolean."""
    INVALID_LABEL_FIELD_TYPE = 'INVALID_LABEL_FIELD_TYPE'
    """label field is not of type string."""
    INVALID_LABEL_FIELD_VALUE = 'INVALID_LABEL_FIELD_VALUE'
    """label field is not a valid label value. Must be a non-empty string
    that consists of uppercase letters, digits, and underscores
    and does not start or end with an underscore or start with a digit."""
    INVALID_DESCRIPTION_FIELD = 'INVALID_DESCRIPTION_FIELD'
    """description field must be a string."""
    INVALID_UNIT_FIELD_TYPE = 'INVALID_UNIT_FIELD_TYPE'
    """unit field is not of type string."""
    INVALID_UNIT_FIELD_VALUE = 'INVALID_UNIT_FIELD_VALUE'
    """unit field is not a valid unit value. Must be a non-empty string consisting of letters only."""
    INVALID_SCALE_FIELD_TYPE = 'INVALID_SCALE_FIELD_TYPE'
    """scale field is not of type float."""
    INVALID_SCALE_FIELD_VALUE = 'INVALID_SCALE_FIELD_VALUE'
    """scale field is not a valid scale value. Must be greater than 0.0"""
    INVALID_SEMANTIC_TYPE_FIELD_TYPE = 'INVALID_SEMANTIC_TYPE_FIELD_TYPE'
    """semantic_type_field field is not of type string."""
    INVALID_SEMANTIC_TYPE_FIELD_VALUE = 'INVALID_SEMANTIC_TYPE_FIELD_VALUE'
    """semantic_type_field field is not a valid semantic type field value.
    Does not conform to the namespace identifier format'."""
