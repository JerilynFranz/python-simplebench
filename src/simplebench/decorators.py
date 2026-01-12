"""A collection of decorators for simplebench."""

from functools import wraps

from .exceptions import SimpleBenchAttributeError
from .report._error_tags import _StatsBlockErrorTag


def immutable(setter_method):
    """Decorator to make a property immutable after its initial setting.

    This decorator wraps a property's setter method. On the first call to the
    setter, it allows the value to be set. On any subsequent call, it raises
    a `SimpleBenchAttributeError`, preventing the property from being changed.

    It assumes the property's value is stored in a private attribute with the
    same name as the property, but prefixed with an underscore (e.g., `_name`
    for a property named `name`).

    .. note:: This is not a good general-purpose immutability solution. It is intended
       for specific use cases within simplebench where certain properties with
       complex validation requirements need to be set only once. For broader
       immutability needs, consider using frozen dataclasses or other established patterns.

    :param setter_method: The setter method of the property to be decorated.
    :return: The wrapped setter method with immutability enforcement.
    :raise SimpleBenchAttributeError: If the property is set more than once.
    """
    private_name = f'_{setter_method.__name__}'

    @wraps(setter_method)
    def wrapper(self, value):
        if hasattr(self, private_name):
            raise SimpleBenchAttributeError(
                f'property {setter_method.__name__} is immutable once set',
                tag=_StatsBlockErrorTag.IMMUTABLE_VIOLATION,
                name=setter_method.__name__,
            )
        return setter_method(self, value)

    return wrapper
