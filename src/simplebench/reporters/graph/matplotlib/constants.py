"""Constants for the matplotlib graph reporters."""
from typing import Final
from ..enums import ImageType

SUPPORTED_IMAGE_TYPES: Final[frozenset[ImageType]] = frozenset({ImageType.SVG, ImageType.PNG})
"""Supported image types for graph reporters."""
