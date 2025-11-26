"""Format enums for SimpleBench."""
from enum import Enum

from .decorators import enum_docstrings


@enum_docstrings
class Format(str, Enum):
    """Categories for different output formats.

    Defined Formats are:
      - PLAIN_TEXT: Plain text format.
      - RICH_TEXT: Rich text format.
      - CSV: CSV format.
      - JSON: JSON format.
      - GRAPH: Graphical format.
      - CUSTOM: Custom format.
    """
    PLAIN_TEXT = 'plain text'
    """Plain text format"""
    RICH_TEXT = 'rich text'
    """Rich text format"""
    CSV = 'csv'
    """CSV format"""
    JSON = 'json'
    """JSON format"""
    GRAPH = 'graph'
    """Graphical format"""
    CUSTOM = 'custom'
    """Custom format"""
