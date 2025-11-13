"""A mechanism to create a lazy type proxy for the `Choice` type for runtime checks.

It allows for deferred imports and avoids circular dependencies while still enabling
runtime type checks and static type checking.

The ChoiceTypeProxy class acts as a stand-in for the actual Choice type.
"""
from __future__ import annotations

from typing import TYPE_CHECKING, TypeGuard

from .lazy_type_proxy import LazyTypeProxy, register_lazy_proxy

# For static type checkers, import the real type.
if TYPE_CHECKING:
    from simplebench.reporters.choice.choice import Choice


# Use a string literal to prevent the NameError at import time.
class ChoiceTypeProxy(LazyTypeProxy['Choice']):
    """A special proxy class that acts like the `Choice` type for runtime checks.

    It uses lazy loading to avoid circular import issues while still allowing
    runtime type checks and static type checking.

    It can be used in `isinstance` and `issubclass` checks as if it were
    the actual `Choice` type.

    WARNING: Do not attempt to import `Choice` directly from this module,
    as it will lead to circular import issues and will not work as intended.

    It is not intended to be instantiated directly; use the actual `Choice` class
    instead if an actual `Choice` instance is needed.
    """


# Explicitly register the proxy with its real type's information.
register_lazy_proxy(ChoiceTypeProxy, 'Choice', 'simplebench.reporters.choice.choice')


def is_choice(obj: object) -> TypeGuard[Choice]:
    """A type-guard function that checks if an object is an instance of `Choice`.

    This function uses the `ChoiceTypeProxy` to perform the check, allowing
    for deferred imports and avoiding circular dependencies. It has the
    same effect as `isinstance(obj, Choice)` but is safe to use without
    causing import issues. It also works seamlessly with static type checkers
    and IDEs.

    Usage:
    ```python
    if is_choice(some_object):
        # Now `some_object` is treated as a `Choice` instance by static type checkers.
    ```

    Args:
        obj (object): The object to check.

    Returns:
        TypeGuard[Choice]: True if the object is an instance of `Choice`, False otherwise
    """
    return isinstance(obj, ChoiceTypeProxy)
