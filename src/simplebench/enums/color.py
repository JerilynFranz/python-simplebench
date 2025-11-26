"""Color enums for SimpleBench.

Colors are primarily used for console output formatting.
"""
from enum import Enum

from .decorators import enum_docstrings


@enum_docstrings
class Color(str, Enum):
    """Colors for console output.

    Defined Colors are:
      - BLACK: Black color.
      - RED: Red color.
      - GREEN: Green color.
      - YELLOW: Yellow color.
      - BLUE: Blue color.
      - MAGENTA: Magenta color.
      - CYAN: Cyan color.
      - WHITE: White color.
    """
    BLACK = 'black'
    """Black color."""
    RED = 'red'
    """Red color."""
    GREEN = 'green'
    """Green color."""
    YELLOW = 'yellow'
    """Yellow color."""
    BLUE = 'blue'
    """Blue color."""
    MAGENTA = 'magenta'
    """Magenta color."""
    CYAN = 'cyan'
    """Cyan color."""
    WHITE = 'white'
    """White color."""
