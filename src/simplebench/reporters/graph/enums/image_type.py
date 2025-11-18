"""ImageType enums for the :mod:`simplebench.graph` package."""
from enum import Enum

from simplebench.enums import enum_docstrings


@enum_docstrings
class ImageType(str, Enum):
    """Enumeration of image types for graph output."""
    SVG = "svg"
    """SVG (Scalable Vector Graphics) image format."""
    PNG = "png"
    """PNG (Portable Network Graphics) image format."""
