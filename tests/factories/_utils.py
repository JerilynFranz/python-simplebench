"""Internal utility factories for miscellaneous helper classes."""
from __future__ import annotations

from ..cache_factory import cached_factory


class DefaultExtra:
    """An immutable ReporterExtra subclass for testing ChoiceConf initialization."""

    def __init__(self, full_data: bool = False) -> None:
        """Constructs a DefaultExtra instance.

        Args:
            full_data (bool, default=False):
                Indicates whether the extra data is full or minimal.

        Raises:
            TypeError: If full_data is not a bool.
        """
        if not isinstance(full_data, bool):
            raise TypeError(f'full_data must be a bool, got {full_data!r}')
        self._full_data = full_data

    @property
    def full_data(self) -> bool:
        """Indicates whether the extra data is full or minimal."""
        return self._full_data


@cached_factory
def extra_factory(*, full_data: bool = True) -> DefaultExtra:
    """Return a default DefaultExtra instance for testing purposes.

    Args:
        full_data (bool, default=True):
            Indicates whether the extra data is full or minimal.
        cache_id (CacheId, default=CACHE_DEFAULT):
            An optional identifier to distinguish different cached instances.
            If None, caching is disabled for this call.
    Returns:
        DefaultExtra: `DefaultExtra(full_data=True)`
    """
    return DefaultExtra(full_data=full_data)


def default_extra() -> DefaultExtra:
    """Return a default ReporterExtras instance for testing purposes.

    It always returns the same DefaultExtra instance created by extra_factory().

    Returns:
        DefaultExtra: `DefaultExtra(full_data=False)`
    """
    return extra_factory(full_data=False, cache_id=f'{__name__}.default_extra:singleton')
