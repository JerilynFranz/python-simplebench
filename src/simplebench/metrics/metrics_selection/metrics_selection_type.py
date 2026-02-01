"""MetricsSelectionType enum for different types of metric selections."""

from enum import Enum

from simplebench.doc_utils import enum_docstrings

__all__: list[str] = []


@enum_docstrings
class MetricsSelectionType(str, Enum):
    """Represents the metric selection type"""

    COLLECTION = 'collection'
    """Represents a collection of metrics."""
    UNSPECIFIED = 'unspecified'
    """Represents an unspecified metric selection type."""
