"""Cache for type hint validation results."""
from simplebench.validators._cache import ValidationCache

_CACHE = ValidationCache(
    min_cache_size=100,
    max_cache_size=16384,
)
"""Cache for type hint validation results."""

__all__ = ('_CACHE',)
