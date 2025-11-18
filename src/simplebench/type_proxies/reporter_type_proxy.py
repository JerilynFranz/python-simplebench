"""Provides a mechanism to create a lazy type proxy for the `Case` type for runtime checks.

The CaseTypeProxy class acts as a stand-in for the actual Case type, allowing for
deferred imports and avoiding circular dependencies while still enabling runtime type
checks and static type checking.
"""
from __future__ import annotations

from typing import TYPE_CHECKING, TypeGuard

from .lazy_type_proxy import LazyTypeProxy, register_lazy_proxy

# For static type checkers, import the real type.
if TYPE_CHECKING:
    from simplebench.reporters.reporter import Reporter


# Use a string literal to prevent the NameError at import time.
class ReporterTypeProxy(LazyTypeProxy['Reporter']):
    """A special proxy class that acts like the `Reporter` type for runtime checks.

    It uses lazy loading to avoid circular import issues while still allowing
    runtime type checks and static type checking.

    It can be used in `isinstance` and `issubclass` checks as if it were
    the actual `Reporter` type.

    .. warning::

        Do not attempt to import `Reporter` directly from this module,
        as it will lead to circular import issues and will not work as intended.

    It is not intended to be instantiated directly; use the actual `Reporter` class instead
    if an actual `Reporter` instance is needed.
    """


# Explicitly register the proxy with its real type's information.
# This is safe because it only deals with strings at import time.
register_lazy_proxy(ReporterTypeProxy, 'Reporter', 'simplebench.reporters.reporter')


def is_reporter(obj: object) -> TypeGuard[Reporter]:
    """A type-guard function that checks if an object is an instance of `Reporter`.

    This function uses the `ReporterTypeProxy` to perform the check, allowing
    for deferred imports and avoiding circular dependencies. It has the
    same effect as `isinstance(obj, Reporter)` but is safe to use without
    causing import issues. It also works seamlessly with static type checkers
    and IDEs.

    Usage:

    .. code-block:: python

        if is_reporter(some_object):
            # Now `some_object` is treated as a `Reporter` instance by static type checkers.

    :param object obj: The object to check.
    :return: True if the object is an instance of `Reporter`, False otherwise
    :rtype: TypeGuard[Reporter]
    """
    return isinstance(obj, ReporterTypeProxy)
