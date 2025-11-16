"""Default path factories for tests."""
# import atexit
# import tempfile
from pathlib import Path
from typing import overload

from ..cache_factory import CACHE_DEFAULT, CacheId, cached_factory

# TODO: Remove once pyfakefs is used for filesystem tests
# _TEMP_DIR = tempfile.TemporaryDirectory(prefix='simplebench_test_')
# atexit.register(_TEMP_DIR.cleanup)


def temp_dir() -> Path:
    """Return the temporary directory path used for testing."""
    return Path('/simplebench_test_temp_dir')


# The overloads provide a tooltip assist for the decorated function and IDE tooltips
# This is necessary because the cache_factory decorators create a function
# with a confusing tooltip (inherently).
@overload
def path_factory() -> Path:
    """Return a default Path instance for testing purposes.

    This function is cached by default to return the same Path instance
    for identical calls, unless a different cache_id is provided.

    Args:
        cache_id (CacheId, default=CacheDefault):
            An optional identifier to distinguish different cached instances.
            If None, caching is disabled for this call.
    Returns:
        Path: `Path('/tmp/mock_report.txt')`
    """


@overload
def path_factory(*, cache_id: CacheId = CACHE_DEFAULT) -> Path:
    """Return a default Path instance for testing purposes.

    This function is cached by default to return the same Path instance
    for identical calls, unless a different cache_id is provided.

    Args:
        cache_id (CacheId, default=CacheDefault):
            An optional identifier to distinguish different cached instances.
            If None, caching is disabled for this call.
    Returns:
        Path: `Path('/tmp/mock_report.txt')`
    """


@cached_factory
def path_factory(*, cache_id: CacheId = CACHE_DEFAULT) -> Path:  # pylint: disable=unused-argument
    """Return a default Path instance for testing purposes.

    This function is cached by default to return the same Path instance
    for identical calls, unless a different cache_id is provided.

    Args:
        cache_id (CacheId, default=CacheDefault):
            An optional identifier to distinguish different cached instances.
            If None, caching is disabled for this call.

    Returns:
        Path: `Path('/tmp/mock_report.txt')`
    """
    return temp_dir()
