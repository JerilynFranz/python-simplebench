"""Container for metadata information about benchmarks"""

from ._error_tags import _MetadataErrorTag
from .metadata import Metadata

__all__ = [
    "Metadata",
    "_MetadataErrorTag",
]
