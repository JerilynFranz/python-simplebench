"""A mechanism to create a lazy type proxy for the `Session` type for runtime checks.

It allows for deferred imports and avoids circular dependencies while still enabling
runtime type checks and static type checking.

The `SessionTypeProxy` class acts as a stand-in for the actual `Session` type."""
from __future__ import annotations

from typing import TYPE_CHECKING, TypeGuard

from .lazy_type_proxy import LazyTypeProxy, register_lazy_proxy

# For static type checkers, import the real type.
if TYPE_CHECKING:
    from simplebench.session import Session


# Use a string literal to prevent the NameError at import time.
class SessionTypeProxy(LazyTypeProxy['Session']):
    """A special proxy class that acts like the `Session` type for runtime checks.

    It can be used in `isinstance` and `issubclass` checks as if it were
    the actual `Session` type.

    .. warning::

        Do not attempt to import `Session` directly from this module,
        as it will lead to circular import issues and will not work as intended.

    It is not intended to be instantiated directly; use the actual `Session` class
    instead if an actual `Session` instance is needed.
"""


# Explicitly register the proxy with its real type's information.
register_lazy_proxy(SessionTypeProxy, 'Session', 'simplebench.session')


def is_session(obj: object) -> TypeGuard[Session]:
    """A type-guard function that checks if an object is an instance of `Session`.

    This function uses the `SessionTypeProxy` to perform the check, allowing
    for deferred imports and avoiding circular dependencies. It has the
    same effect as `isinstance(obj, Session)` but is safe to use without
    causing import issues. It also works seamlessly with static type checkers
    and IDEs.

    Usage:

    .. code-block:: python

        if is_session(some_object):
            # Now `some_object` is treated as a `Session` instance by static type checkers.

    """
    return isinstance(obj, SessionTypeProxy)
