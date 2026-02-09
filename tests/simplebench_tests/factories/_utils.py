"""Internal utility factories for miscellaneous helper classes."""

from simplebench import Extras

from ..cache_factory import cached_factory


@cached_factory
def extras_factory(*, full_data: bool = True) -> Extras:
    """Return a default Extras instance for testing purposes.

    :param full_data: Indicates whether the extra data is full or minimal.
    :type full_data: bool, optional
    :param cache_id: An optional identifier to distinguish different cached instances.
                     If None, caching is disabled for this call.
    :type cache_id: CacheId, optional
    :return: `Extras(full_data=True)`
    :rtype: Extras
    """
    return Extras({'full_data': full_data})


def default_extras() -> Extras:
    """Return a default Extras instance for testing purposes.

    It always returns the same Extras instance created by extras_factory().

    :return: `Extras(full_data=False)`
    :rtype: Extras
    """
    return extras_factory(full_data=False, cache_id=f'{__name__}.default_extra:singleton')
