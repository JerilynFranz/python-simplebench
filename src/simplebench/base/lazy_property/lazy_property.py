"""LazyProperty descriptor module


"""
import inspect
from threading import Lock
from typing import Callable, Generic, TypeVar

from simplebench.exceptions import SimpleBenchTypeError

from ._error_tags import _LazyPropertyErrorTags

_T = TypeVar("_T")


class LazyProperty(Generic[_T]):
    """A descriptor that implements lazy evaluation for a settable property.

    This is used to defer the computation of an expensive property until it
    is accessed for the first time. After the first access, the result is
    cached and returned directly on subsequent accesses.

    The value can also be manually set, which will override the cached value
    and prevent the computation function from being called if it has not been
    called yet.

    Usage:

    .. code-block:: python

        from simplebench.base import LazyProperty


        class MyClass:
            def __init__(self):
                self._heavy_computation_was_run = False

            def _compute_heavy_property(self) -> str:
                # Simulate an expensive calculation
                self._heavy_computation_was_run = True
                return "this was a lot of work"

            heavy_property: LazyProperty[str] = LazyProperty(_compute_heavy_property)

        # >>> instance = MyClass()
        # >>> instance._heavy_computation_was_run
        # False
        # >>> print(instance.heavy_property)
        # this was a lot of work
        # >>> instance._heavy_computation_was_run
        # True
        # >>> print(instance.heavy_property)  # Access again
        # this was a lot of work
        # The computation function is only called once.
    """
    def __init__(self, func: Callable[[object], _T]):
        """Initialize the descriptor.

        :param func: The function that computes the property's value.
                 This function will be called once, the first time
                 the property is accessed (unless the value is manually set
                 first). It will receive the instance of the class as its
                 only argument and must return the computed value for the property.

                 Note that `func` **IS NOT** a method bound to the instance;
                 it is a standalone function that receives the instance as its
                 only argument.
        """
        self.func: Callable[[object], _T] = self._validate_func(func)
        """The function that computes the property's value."""

        # Uses __set_name__ to get the name of the attribute
        self.name: str = ""
        """The name of the attribute this descriptor is assigned to."""

        self.lock: Lock = Lock()
        """A lock to ensure thread-safe computation of the property."""

    def __set_name__(self, owner: type, name: str) -> None:
        """Get the name of the attribute this descriptor is assigned to.

        :param type owner: The owner class.
        :param str name: The name of the attribute.
        """
        self.name = name

    def __get__(self, instance: object, owner: type) -> _T:
        """Get the property's value.

        If the value has not been computed yet, this will trigger the
        computation by calling the function provided in the constructor.
        Otherwise, it returns the cached value from the instance's __dict__.

        This method is thread-safe.

        :param instance: The instance of the class that owns the property.
        :param owner: The owner class.
        :return: The computed value of the property.
        """
        if instance is None:  # support access via class for introspection
            return self  # type: ignore

        # First check without a lock for performance
        if self.name not in instance.__dict__:
            # If not present, acquire lock and double-check
            with self.lock:
                if self.name not in instance.__dict__:
                    instance.__dict__[self.name] = self.func(instance)
        return instance.__dict__[self.name]

    def __set__(self, instance: object, value: _T) -> None:
        """Set the property's value.

        This allows the cached value to be manually overridden. The value is
        stored in the instance's __dict__. This operation is thread-safe.

        :param instance: The instance of the class that owns the property.
        :param value: The value to set for the property.
        """
        with self.lock:
            instance.__dict__[self.name] = value

    def _validate_func(self, func: Callable[[object], _T]) -> Callable[[object], _T]:
        """Validate the function provided to the LazyProperty.

        :param func: The function to validate.
        :return: The validated function.
        :raises TypeError: If the provided func is not callable.
        """
        if not callable(func):
            raise SimpleBenchTypeError(
                f"Expected a callable, got {type(func).__name__}",
                tag=_LazyPropertyErrorTags.INVALID_FUNC)
        signature = inspect.signature(func)
        if len(signature.parameters) != 1:
            raise SimpleBenchTypeError(
                f"Expected a function with exactly one parameter, got {len(signature.parameters)}",
                tag=_LazyPropertyErrorTags.INVALID_FUNC_WRONG_PARAM_COUNT)
        return func
