"""Graph reporter initialization module."""
from simplebench.reporters.graph.enums.image_type import ImageType
from simplebench.reporters.graph.options import GraphOptions

SUPPORTED_IMAGE_TYPES: set[ImageType] = {ImageType.SVG, ImageType.PNG}

__all__ = [
    "ImageType",
    "GraphOptions",
    "SUPPORTED_IMAGE_TYPES",
]
