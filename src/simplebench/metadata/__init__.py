"""Container for metadata information about benchmarks"""

from .exceptions import _MetadataErrorTag
from .metadata import Metadata

__all__ = [
    "Metadata",
    "_MetadataErrorTag",
]
