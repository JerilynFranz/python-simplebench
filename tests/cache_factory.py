"""A caching mechanism for factory functions used in tests.

This module provides a sophisticated memoization decorator, `@cache_factory`,
designed specifically for use with factory functions in a testing environment.
It improves test performance by caching factory results and provides fine-grained
control over object instantiation, which is crucial for test isolation and
setting up specific test scenarios.

Note:

    Due to the limitations of the Python type system, the decorated factory functions
    may not have completely accurate type hints in all IDEs. However, the decorator
    is designed to preserve the original function's signature as closely as possible,
    including the addition of the `cache_id` keyword argument when appropriate.

    You may see something like the following in your IDE tooltips:
    ```python

    (function) def reporter_instance(
        self: Self@CachedFactory[R_co@CachedFactory],
        ...,
        cache_id: CacheId = ...
    ) -> UnconfiguredReporter
    ```

    This indicates that the function has been wrapped by the `CachedFactory` protocol,
    which includes the `cache_id` parameter. The `...` in the parameters means that
    the original parameters are preserved, but not explicitly shown in the tooltip.

    This is a limitation of how decorators and type hinting interact in Python,
    rather than an error in the implementation.

Public API:
    - `cached_factory`: Decorator for creating cached factory functions.
    - `uncached_factory`: Decorator for creating uncached factory functions.
    - `clear_cache`: Function to clear the global factory cache.
    - `CACHE_DEFAULT`: Sentinel value for the default cache ID.
    - `CacheDefault`: Type alias for the type of `CACHE_DEFAULT`.
    - `CacheId`: Type alias for the allowed cache ID types.
    - `CachedFactory`: Protocol describing the signature of a decorated factory.

Keep in mind that this module is highly dynamic and relies on `inspect` to
rewrite function signatures on the fly. While it uses advanced `typing` concepts
like `Protocol` and `ParamSpec` to provide the best possible static analysis
experience, some tools may still struggle to perfectly understand the modified
signatures. The runtime behavior, however, is correct and predictable.

Basic @cached_factory Usage:

    Decorate a factory function to cache its return value by default.
    Subsequent calls with the same arguments will return the cached object
    without re-executing the factory.

    .. code-block:: python

        from .cache_factory import cache_factory

        @cache_factory
        def my_factory():
            print("Executing factory...")
            return "my_object"

        obj1 = my_factory()  # "Executing factory..." is printed
        obj2 = my_factory()  # Factory is NOT executed, returns cached object
        assert obj1 is obj2

Basic @uncached_factory Usage:

    Decorate a factory function to NOT cache its return value by default.
    Subsequent calls with the same arguments will re-execute the factory
    unless a `cache_id` is provided.

    .. code-block:: python
        from .cache_factory import uncached_factory
        @uncached_factory
        def my_factory():
            print("Executing factory...")
            return "my_object"
        obj1 = my_factory()  # "Executing factory..." is printed
        obj2 = my_factory()  # "Executing factory..." is printed again
        assert obj1 is not obj2

Advanced Usage:

    1. Controlling the Cache with `cache_id`:

       Pass the `cache_id` keyword argument to explicitly control the creation and retrieval of distinct
       cached instances. This is useful for creating different variations of a
       mock object within the same test.

       .. code-block:: python

           # Returns a new cached object under the "test_A" key
           obj_a = my_factory(cache_id="test_A")

           # Returns a different cached object under the "test_B" key
           obj_b = my_factory(cache_id="test_B")
           assert obj_a is not obj_b

           # This call retrieves the object from the "test_A" cache
           obj_a2 = my_factory(cache_id="test_A")
           assert obj_a is obj_a2

    2. Disabling Caching:
       Pass `cache_id=None` to explictly bypass the cache entirely for a single call,
       forcing the factory function to execute.

       .. code-block:: python

           obj1 = my_factory(cache_id=None) # Factory executes
           obj2 = my_factory(cache_id=None) # Factory executes again
           assert obj1 is not obj2

    3. Explicit `cache_id` Handling:
       If a factory function needs to know its `cache_id`, it can explicitly
       include it in its signature. The decorator will detect this and pass
       the value through instead of consuming it.

       .. code-block:: python

           @cache_factory
           def factory_aware_of_id(cache_id: CacheId = CACHE_DEFAULT):
               return f"I was created with cache_id: {repr(cache_id)}"

           result = factory_aware_of_id(cache_id="special")
           assert "special" in result

Raises:
    TypeError: If the decorated function is called with unhashable arguments,
               or if the provided `cache_id` is not a valid type (str,
               CacheDefault, or None).
"""
# --- Imports ---
from __future__ import annotations

import inspect
import threading
from functools import wraps
from typing import Any, Callable, Final, NamedTuple, ParamSpec, Protocol, TypeAlias, TypeVar

# --- Exports ---
__all__ = [
    'cached_factory',
    'uncached_factory',
    'clear_cache',
    'CACHE_DEFAULT',
    'CacheDefault',
    'CacheId',
]


P = ParamSpec('P')
R_co = TypeVar('R_co', covariant=True)


class CachedFactory(Protocol[R_co]):
    """A protocol describing a factory function after being decorated.

    It can be called with arbitrary arguments, plus the `cache_id` keyword.
    """
    def __call__(self, *args: Any, cache_id: 'CacheId' = ..., **kwargs: Any) -> R_co:
        ...

    # Also provide the __signature__ attribute for type checkers
    __signature__: inspect.Signature


class CacheDefault:
    """A sentinel value to indicate the default cache ID."""
    def __repr__(self) -> str:
        return "CACHE_DEFAULT"


CacheId: TypeAlias = str | CacheDefault | None
"""Defines the allowable types for a cache ID."""

CACHE_DEFAULT: Final[CacheDefault] = CacheDefault()
"""The sentinel value used for the default cache ID.

This indicates that the default caching id should be used.
"""


class CacheKey(NamedTuple):
    """A unique tuple based key for caching factory function results.

    The key is based on the package name, factory function name,
    a hash of the calling signature, and the cache ID.

    :param package_name: The name of the package where the factory function is defined.
    :type package_name: str
    :param factory_name: The name of the factory function.
    :type factory_name: str
    :param calling_signature_hash: A hash representing the arguments with which the factory was called.
    :type calling_signature_hash: int
    :param cache_id: The cache ID used for fine-grained cache control.
    :type cache_id: CacheId

    :ivar package_name: The name of the package where the factory function is defined.
    :vartype package_name: str
    :ivar factory_name: The name of the factory function.
    :vartype factory_name: str
    :ivar calling_signature_hash: A hash representing the arguments with which the factory was called.
    :vartype calling_signature_hash: int
    :ivar cache_id: The cache ID used for fine-grained cache control.
    :vartype cache_id: CacheId
    """
    package_name: str
    factory_name: str
    calling_signature_hash: int
    cache_id: CacheId


_CACHE: dict[CacheKey, Any] = {}
"""A global cache dictionary for cached factory results."""
_CACHE_MISS = object()
"""A global cache dictionary sentinel value."""
_CACHE_LOCK = threading.Lock()
"""A global cache lock for thread-safe access."""


# --- Main Implementation ---
class FactoryDecorator:
    """A class-based decorator that provides factory caching features.

    This class is not intended to be used directly. Use the singleton instances
    `_CACHED_FACTORY` or `_UNCACHED_FACTORY` instead.
    """
    def __init__(self, default_cache_id_value: CacheId):
        self.default_cache_id_value = default_cache_id_value

    def __call__(self, func: Callable[P, R_co]) -> CachedFactory[R_co]:
        # --- DECORATOR SETUP ---
        func_sig = inspect.signature(func)
        has_explicit_cache_id = 'cache_id' in func_sig.parameters

        # The signature for our wrapper will be the function's own signature,
        # unless we need to add the implicit cache_id parameter.
        wrapper_sig = func_sig
        if not has_explicit_cache_id:
            cache_id_param = inspect.Parameter('cache_id',
                                               inspect.Parameter.KEYWORD_ONLY,
                                               default=self.default_cache_id_value)
            params = list(func_sig.parameters.values())
            params.append(cache_id_param)
            wrapper_sig = inspect.Signature(params)

        @wraps(func)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> R_co:
            # Bind the incoming arguments to the correct signature
            bound_args = wrapper_sig.bind(*args, **kwargs)
            bound_args.apply_defaults()

            if has_explicit_cache_id:
                cache_id = bound_args.arguments['cache_id']
            else:
                cache_id = bound_args.arguments.pop('cache_id')

            if cache_id is None:
                # Caching is disabled. Call the original function with its arguments.
                return func(*bound_args.args, **bound_args.kwargs)

            if not isinstance(cache_id, (str, CacheDefault)):
                raise TypeError("cache_id must be a string, None, or CacheDefault")

            # Hash the actual arguments that will be passed to the function.
            try:
                hashed_args = hash(bound_args.args)
                hashed_kwargs = hash(frozenset(bound_args.kwargs.items()))
            except TypeError as e:
                raise TypeError(
                    f"All arguments to a cached factory must be hashable. "
                    f"Factory '{func.__name__}' was called with an unhashable argument."
                ) from e

            hash_combined = hash((hashed_args, hashed_kwargs))

            cache_key = CacheKey(package_name=func.__module__,
                                 factory_name=func.__name__,
                                 calling_signature_hash=hash_combined,
                                 cache_id=cache_id)

            with _CACHE_LOCK:
                cached_value = _CACHE.get(cache_key, _CACHE_MISS)

            if cached_value is not _CACHE_MISS:
                return cached_value

            # Run the function with the correct arguments and store the result.
            result = func(*bound_args.args, **bound_args.kwargs)

            with _CACHE_LOCK:
                _CACHE[cache_key] = result

            return result

        # THIS IS THE MOST IMPORTANT PART FOR THE IDE TOOLTIP
        wrapper.__signature__ = wrapper_sig  # type: ignore[attr-defined]
        return wrapper  # type: ignore[return-value]


_CACHED_FACTORY: Final[FactoryDecorator] = FactoryDecorator(default_cache_id_value=CACHE_DEFAULT)
_UNCACHED_FACTORY: Final[FactoryDecorator] = FactoryDecorator(default_cache_id_value=None)


def cached_factory(func: Callable[P, R_co]) -> CachedFactory[R_co]:
    """A decorator to automatically cache the result of a factory function.

    By default, this decorator caches results. Caching can be disabled on a
    per-call basis by passing `cache_id=None`.

    The `cache_id` keyword argument provides fine-grained cache control.
    By default, the decorator consumes this argument, but if the wrapped
    function explicitly includes `cache_id` in its signature, the value is
    passed through.

    To enable caching for a specific call, use a string for the cache_id.

    To use the standard shared cache common to other factories, you can explicitly
    pass cache_id=CACHE_DEFAULT. It is guaranteed to be different from `None` or
    any other values that may be used and will not ever conflict with other cache IDs.

    :param func: The factory function to be decorated.
    :type func: Callable[P, R_co]
    :return: The wrapped function with caching capabilities and an added `cache_id` keyword argument.
    :rtype: CachedFactory[P, R_co]
    :raises TypeError: If any arguments passed to the decorated function are not hashable,
        or if the provided `cache_id` is not a valid type.
    """
    return _CACHED_FACTORY(func)  # type: ignore[return-value]


def uncached_factory(func: Callable[P, R_co]) -> CachedFactory[R_co]:
    """A decorator that provides factory features without caching by default.

    By default, this decorator does NOT cache results. Caching can be enabled on a
    per-call basis by passing a string to the `cache_id` argument.

    The `cache_id` keyword argument provides fine-grained cache control of
    the caching behavior.

    By default, the decorator consumes this argument, but if the wrapped
    function explicitly includes `cache_id` in its signature, the value is
    passed through.

    The standard cache_id for collision avoidance with explictly set cache_ids
    is `CACHE_DEFAULT`. It is guaranteed to be different from `None` or any other values
    that may be used.

    :param func: The factory function to be decorated.
    :type func: Callable[P, R_co]
    :return: The wrapped function with caching capabilities and an added `cache_id` keyword argument.
    :rtype: CachedFactory[P, R_co]
    :raises TypeError: If any arguments passed to the decorated function are not hashable,
        or if the provided `cache_id` is not a valid type.
    """
    return _UNCACHED_FACTORY(func)  # type: ignore[return-value]


def clear_cache() -> None:
    """Clears all cached factory results."""
    with _CACHE_LOCK:
        _CACHE.clear()
