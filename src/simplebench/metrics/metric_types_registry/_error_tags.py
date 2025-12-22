"""Error tags for metric registry operations."""
from simplebench.doc_utils import enum_docstrings
from simplebench.exceptions import ErrorTag


@enum_docstrings
class _MetricTypesRegistryErrorTag(ErrorTag):
    """Enumerates error tags for metric registry operations."""
    NOT_ITERABLE_OF_METRIC_DEFINITIONS = "NOT_ITERABLE_OF_METRIC_DEFINITIONS"
    """The provided input is not iterable or does not contain valid MetricDefinition objects."""
    DUPLICATE_METRIC_NAME = "DUPLICATE_METRIC_NAME"
    """A metric with the same name already exists in the registry."""
    NOT_METRIC_DEFINITION_OR_ITERABLE_OF_METRIC_DEFINITIONS = "NOT_METRIC_DEFINITION_OR_ITERABLE_OF_METRIC_DEFINITIONS"
    """The provided input is neither a MetricDefinition object nor an iterable of MetricDefinition objects."""
    NOT_STRING_OR_ITERABLE_OF_STRINGS = "NOT_STRING_OR_ITERABLE_OF_STRINGS"
    """The provided input is neither a string nor an iterable of strings."""
