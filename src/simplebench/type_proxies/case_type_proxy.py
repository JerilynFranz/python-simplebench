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
    from simplebench.case import Case


# Use a string literal to prevent the NameError at import time.
class CaseTypeProxy(LazyTypeProxy['Case']):
    """A special proxy class that acts like the `Case` type for runtime checks.

    It uses lazy loading to avoid circular import issues while still allowing
    runtime type checks and static type checking.

    It can be used in `isinstance` and `issubclass` checks as if it were
    the actual `Case` type.

    WARNING: Do not attempt to import `Case` directly from this module,
    as it will lead to circular import issues and will not work as intended.

    It is not intended to be instantiated directly; use the actual `Case` class instead
    if an actual `Case` instance is needed.
    """


# Explicitly register the proxy with its real type's information.
# This is safe because it only deals with strings at import time.
register_lazy_proxy(CaseTypeProxy, 'Case', 'simplebench.case')


def is_case(obj: object) -> TypeGuard[Case]:
    """A type-guard function that checks if an object is an instance of `Case`.

    This function uses the `CaseTypeProxy` to perform the check, allowing
    for deferred imports and avoiding circular dependencies. It has the
    same effect as `isinstance(obj, Case)` but is safe to use without
    causing import issues. It also works seamlessly with static type checkers
    and IDEs.

    Usage:
    ```python
    if is_case(some_object):
        # Now `some_object` is treated as a `Case` instance by static type checkers.
    ```

    Args:
        obj (object): The object to check.

    Returns:
        TypeGuard[Case]: True if the object is an instance of `Case`, False otherwise
    """
    return isinstance(obj, CaseTypeProxy)
