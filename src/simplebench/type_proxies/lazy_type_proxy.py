"""Provides a generic deferred import mechanism for any type."""
from __future__ import annotations

import importlib
from typing import Any, Generic, Type, TypeVar

_LAZY_TYPES_CACHE: dict[str, Type[Any]] = {}
_TYPE_IMPORT_MAP: dict[str, str] = {}
T = TypeVar('T')


def register_lazy_proxy(proxy_class: type, real_type_name: str, module_path: str) -> None:
    """Register a lazy proxy class with its real type information.

    The proxy class will use this information to perform runtime type checks
    without causing circular import issues.

    Usage:

    .. code-block:: python

        register_lazy_proxy(MyProxyClass, 'RealTypeName', 'path.to.module')

    :param type proxy_class: The proxy class to register.
    :param str real_type_name: The name of the real type being proxied.
    :param str module_path: The module path where the real type can be imported from.
    """
    setattr(proxy_class, '__real_type_name__', real_type_name)
    if real_type_name not in _TYPE_IMPORT_MAP:
        _TYPE_IMPORT_MAP[real_type_name] = module_path


def _get_real_type(type_name: str) -> Type[Any]:
    """Dynamically import and return the real type by its name.

    :param str type_name: The name of the type to import.
    :return: The actual type object.
    :rtype: Type[Any]
    """
    if type_name not in _LAZY_TYPES_CACHE:
        if type_name not in _TYPE_IMPORT_MAP:
            raise ImportError(f"LazyTypeProxy for '{type_name}' was not registered.")
        module = importlib.import_module(_TYPE_IMPORT_MAP[type_name])
        _LAZY_TYPES_CACHE[type_name] = getattr(module, type_name)
    return _LAZY_TYPES_CACHE[type_name]


class _LazyTypeProxyMeta(type):
    """A metaclass that enables lazy type checking for proxy classes.

    This metaclass overrides `__instancecheck__` and `__subclasscheck__` to defer
    the actual type checks until runtime, using dynamic imports to avoid circular
    dependencies.

    :param str type_name: The name of the real type being proxied.
    """
    __real_type_name__: str

    def __instancecheck__(cls, instance: Any) -> bool:
        """Check if an instance is of the proxied type at runtime.

        :param Any instance: The instance to check.
        :return: True if the instance is of the proxied type, False otherwise.
        :rtype: bool
        """
        # If this is called on the base LazyTypeProxy class, it has no real type.
        if not hasattr(cls, '__real_type_name__'):
            return False
        return isinstance(instance, _get_real_type(cls.__real_type_name__))

    def __subclasscheck__(cls, subclass: Any) -> bool:
        """Check if a subclass is of the proxied type at runtime.

        :param Any subclass: The subclass to check.
        :return: True if the subclass is of the proxied type, False otherwise.
        :rtype: bool
        """
        # If this is called on the base LazyTypeProxy class, it has no real type.
        if not hasattr(cls, '__real_type_name__'):
            return False
        try:
            return issubclass(subclass, _get_real_type(cls.__real_type_name__))
        except TypeError:
            return False

    def __repr__(cls) -> str:
        """Provide a string representation of the lazy proxy class."""
        real_type_name = getattr(cls, '__real_type_name__', None)
        if real_type_name:
            return f"<LazyProxyType for '{real_type_name}'>"
        return f"<LazyProxyType for '{cls.__name__}'>"


class LazyTypeProxy(Generic[T], metaclass=_LazyTypeProxyMeta):
    """A generic base class for creating lazy-loading type proxies.

    Usage:

    .. code-block:: python

        class MyProxy(LazyTypeProxy['RealType']):
            pass

        register_lazy_proxy(MyProxy, 'RealType', 'path.to.module')
    """
