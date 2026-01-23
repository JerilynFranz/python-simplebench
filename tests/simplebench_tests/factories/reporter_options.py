"""Factory for ReporterOptions related instances for testing purposes.

Separately defined to avoid circular imports.
"""
from __future__ import annotations

from collections.abc import Hashable
from typing import overload

from simplebench.reporters.reporter.options import ReporterOptions

from ..cache_factory import CACHE_DEFAULT, CacheId, cached_factory


class FactoryReporterOptions(ReporterOptions, Hashable):
    """A dummy ReporterOptions subclass for testing purposes."""
    def __init__(self) -> None:
        """Constructs a FactoryReporterOptions instance."""
        self._tag = 'default'
        super().__init__()

    @property
    def tag(self) -> str:
        """Get the tag of the FactoryReporterOptions instance.

        The tag is a string that identifies the instance for testing purposes.

        :return: The tag of the instance.
        :rtype: str
        """
        return self._tag

    @tag.setter
    def tag(self, value: str) -> None:
        self._tag = value

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, FactoryReporterOptions):
            return False
        return self._tag == other._tag

    def __hash__(self) -> int:
        return hash(self._tag)

    def __str__(self) -> str:
        return f'FactoryReporterOptions(tag={self._tag!r})'

    def __repr__(self) -> str:
        return f'FactoryReporterOptions(tag={self._tag!r})'


@cached_factory
def reporter_options_tuple_factory(  # pylint: disable=unused-argument
        *, cache_id: CacheId = CACHE_DEFAULT) -> tuple[FactoryReporterOptions]:
    """Return a tuple containing a FactoryReporterOptions instance for testing purposes.

    :param cache_id: An optional identifier to distinguish different cached instances.
                     If None, caching is disabled for this call.
    :type cache_id: CacheId, optional
    :return: A tuple containing a ReporterOptions instance.
    :rtype: tuple[ReporterOptions]
    """
    return (default_reporter_options(), )


def default_reporter_options_tuple() -> tuple[FactoryReporterOptions]:
    """Return a default tuple containing a FactoryReporterOptions instance for testing purposes.

    It always returns the same tuple created by reporter_options_tuple_factory().

    :return: A tuple containing a FactoryReporterOptions instance.
    :rtype: tuple[FactoryReporterOptions]
    """
    return reporter_options_tuple_factory(cache_id=f'{__name__}.default_reporter_options_tuple:singleton')


@cached_factory
def reporter_options_type_factory(  # pylint: disable=unused-argument
        *, cache_id: CacheId = CACHE_DEFAULT) -> type[FactoryReporterOptions]:
    """Return a default FactoryReporterOptions type for testing purposes.

    :return: `FactoryReporterOptions`
    :rtype: type[FactoryReporterOptions]
    """
    return FactoryReporterOptions


def default_reporter_options_type() -> type[FactoryReporterOptions]:
    """Return a default FactoryReporterOptions type for testing purposes.

    It always returns the same FactoryReporterOptions type returned by reporter_options_type_factory().

    :return: `FactoryReporterOptions`
    :rtype: type[FactoryReporterOptions]
    """
    return reporter_options_type_factory(cache_id=f'{__name__}.default_reporter_options_type:singleton')


@overload
def reporter_options_factory() -> FactoryReporterOptions:
    """Return a FactoryReporterOptions instance for testing purposes.

    The returned instance is cached by default.

    :param cache_id: An optional identifier to distinguish different cached instances.
                     If None, caching is disabled for this call.
    :type cache_id: CacheId, optional
    :return: A FactoryReporterOptions instance.
    :rtype: FactoryReporterOptions
    """
    return FactoryReporterOptions()


@overload
def reporter_options_factory(  # pylint: disable=unused-argument
        *, cache_id: CacheId = CACHE_DEFAULT) -> FactoryReporterOptions:
    """Return a new FactoryReporterOptions instance for testing purposes.

    It is cached by default.

    :param cache_id: An optional identifier to distinguish different cached instances.
                     If None, caching is disabled for this call.
    :type cache_id: CacheId, optional
    :return: A FactoryReporterOptions instance.
    :rtype: FactoryReporterOptions
    """


@cached_factory
def reporter_options_factory(  # pylint: disable=unused-argument
        *, cache_id: CacheId = CACHE_DEFAULT) -> FactoryReporterOptions:
    """Return a FactoryReporterOptions instance for testing purposes.

    It is cached by default.

    :param cache_id: An optional identifier to distinguish different cached instances.
                     If None, caching is disabled for this call.
    :type cache_id: CacheId, optional
    :return: A FactoryReporterOptions instance.
    :rtype: FactoryReporterOptions
    """
    return FactoryReporterOptions()


def default_reporter_options() -> FactoryReporterOptions:
    """Return a default FactoryReporterOptions instance for testing purposes.

    It always returns the same FactoryReporterOptions instance created by reporter_options_factory().

    :return: A FactoryReporterOptions instance.
    :rtype: FactoryReporterOptions
    """
    return reporter_options_factory(cache_id=f'{__name__}.default_reporter_options:singleton')
