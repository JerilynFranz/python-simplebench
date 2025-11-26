"""Graph reporter base public API.

Purpose is to provide common functionality for all graph reporters
in the :mod:`~simplebench.reporters` package.

Public API
----------
- ImageType: Enum for known image types.
- GraphOptions: Base class for graph reporter options.
- SUPPORTED_IMAGE_TYPES: Set of supported image types.
"""
from .enums import ImageType
from .options import GraphOptions

SUPPORTED_IMAGE_TYPES: set[ImageType] = {ImageType.SVG, ImageType.PNG}

__all__ = [
    "ImageType",
    "GraphOptions",
    "SUPPORTED_IMAGE_TYPES",
]
