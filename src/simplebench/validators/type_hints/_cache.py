"""Cache for type hint validation results."""
from simplebench.validators._cache import ValidationCache

_CACHE = ValidationCache(
    min_cache_size=1000,
    max_cache_size=65536,
)
"""Cache for type hint validation results."""

__all__ = ('_CACHE',)
