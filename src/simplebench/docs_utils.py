"""Documentation utilities."""
from typing import overload, Callable, TypeVar, Any


# A single TypeVar that can be bound to any callable, which includes
# both functions and class objects.
T = TypeVar('T', bound=Callable[..., Any])


# Overload 1: Called as @dynamic_docstring(key='value')
# It receives no positional object and returns a decorator.
@overload
def dynamic_docstring(
    cls_or_func: None = None, /, **kwargs
) -> Callable[[T], T]: ...


# Overload 2: Called as @dynamic_docstring
# It receives the class or function directly and returns it.
@overload
def dynamic_docstring(cls_or_func: T, /) -> T: ...


def dynamic_docstring(
    cls_or_func: T | None = None, /, **kwargs
) -> T | Callable[[T], T]:
    """A decorator to dynamically format the docstring of a class or function.

    Can be used with or without arguments on both classes and functions.
    It closely scopes the formatting to only the decorated object and to only
    the passed key-value pairs.

    Examples:

    ```python
    @dynamic_docstring(version="1.2.3")
    class MyClass:
        '''My class, version {version}'''
        pass

    @dynamic_docstring(author="Me")
    def my_function():
        '''A function by {author}'''
        pass
    ```

    Args:
        cls_or_func (Optional[Callable[..., Any]]):
            The class or function to decorate. If None, the decorator is being called with arguments.
        **kwargs: Key-value pairs to format the docstring.

    Returns:
        (Callable[[Callable[..., Any]], Callable[..., Any]] | Callable[..., Any]):
            The decorated class or function with the formatted docstring.

    Raises:
        TypeError: If the docstring contains format keys not provided in kwargs.
    """
    # This is the actual decorator that will be applied to the class or function.
    # It uses the 'kwargs' from the outer scope.
    def decorator(inner_obj: T) -> T:
        if inner_obj.__doc__ is not None and kwargs:
            try:
                inner_obj.__doc__ = inner_obj.__doc__.format(**kwargs)
            except KeyError as e:
                # Raise a more specific error for better debugging.
                raise TypeError(
                    f"The docstring of '{inner_obj.__name__}' has a format key {e} "
                    "that was not provided to @dynamic_docstring."
                ) from e
        return inner_obj

    # Case 1: Called with arguments, e.g., @dynamic_docstring(foo='bar')
    if cls_or_func is None:
        return decorator

    # Case 2: Called without arguments, e.g., @dynamic_docstring
    return decorator(cls_or_func)
