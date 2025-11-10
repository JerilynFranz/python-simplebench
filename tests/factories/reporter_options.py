"""Factory for ReporterOptions related instances for testing purposes.

Separately defined to avoid circular imports.
"""
from __future__ import annotations

from simplebench.reporters.reporter.options import ReporterOptions

from ..cache_factory import cached_factory, CacheId, CACHE_DEFAULT


@cached_factory
def reporter_options_tuple_factory(  # pylint: disable=unused-argument
        *, cache_id: CacheId = CACHE_DEFAULT) -> tuple[ReporterOptions]:
    """Return a tuple containing a ReporterOptions instance for testing purposes.

    Args:
        cache_id (CacheId, default=CACHE_DEFAULT):
            An optional identifier to distinguish different cached instances.
            If None, caching is disabled for this call.

    Returns:
        tuple[ReporterOptions]: A tuple containing a ReporterOptions instance.
    """
    return (default_reporter_options(), )


def default_reporter_options_tuple() -> tuple[ReporterOptions]:
    """Return a default tuple containing a ReporterOptions instance for testing purposes.

    It always returns the same tuple created by reporter_options_tuple_factory().

    Returns:
        tuple[ReporterOptions]: A tuple containing a ReporterOptions instance.
    """
    return reporter_options_tuple_factory(cache_id=f'{__name__}.default_reporter_options_tuple:singleton')


@cached_factory
def reporter_options_type_factory(  # pylint: disable=unused-argument
        *, cache_id: CacheId = CACHE_DEFAULT) -> type[ReporterOptions]:
    """Return a default ReporterOptions type for testing purposes.

    Returns:
        type[ReporterOptions]: `ReporterOptions`
    """
    return ReporterOptions


def default_reporter_options_type() -> type[ReporterOptions]:
    """Return a default ReporterOptions type for testing purposes.

    It always returns the same ReporterOptions type returned by reporter_options_type_factory().

    Returns:
        type[ReporterOptions]: `ReporterOptions`
    """
    return reporter_options_type_factory(cache_id=f'{__name__}.default_reporter_options_type:singleton')


@cached_factory
def reporter_options_factory(  # pylint: disable=unused-argument
        *, cache_id: CacheId = CACHE_DEFAULT) -> ReporterOptions:
    """Return a ReporterOptions instance for testing purposes.

    Args:
        cache_id (CacheId, default=CACHE_DEFAULT):
            An optional identifier to distinguish different cached instances.
            If None, caching is disabled for this call.

    Returns:
        ReporterOptions: `ReporterOptions`
    """
    return ReporterOptions()


def default_reporter_options() -> ReporterOptions:
    """Return a default ReporterOptions instance for testing purposes.

    It always returns the same ReporterOptions instance created by reporter_options_factory().

    Returns:
        ReporterOptions: `ReporterOptions`
    """
    return reporter_options_factory(cache_id=f'{__name__}.default_reporter_options:singleton')
