"""Documentation utilities."""
import re
from typing import Any, Callable, TypeVar, overload

# A single TypeVar that can be bound to any callable, which includes
# both functions and class objects.
T = TypeVar('T', bound=Callable[..., Any])

_PLACEHOLDER_PATTERN = re.compile(r'\{([A-Za-z0-9_.:~ `]+)\}')
"""A regex pattern to find {key} placeholders in docstrings.

The pattern matches any sequence of characters that can form a valid Python
identifier, including letters, digits, underscores, dots,
and backticks, enclosed in curly braces.

It also allows colons, tildes, spaces and backticks to be part of the key name
to accommodate more complex placeholder names that might include formatting or
special characters commonly used in RST documentation.
"""


# Overload 1: Called as @format_docstring(key='value')
# It receives no positional object and returns a decorator.
@overload
def format_docstring(
    cls_or_func: None = None, /, **kwargs
) -> Callable[[T], T]: ...


# Overload 2: Called as @format_docstring
# It receives the class or function directly and returns it.
@overload
def format_docstring(cls_or_func: T, /) -> T: ...


def format_docstring(
    cls_or_func: T | None = None, /, **kwargs
) -> T | Callable[[T], T]:
    """A decorator to format the docstring of a class or function.

    Can be used with or without arguments on both classes and functions.
    It closely scopes the formatting to only the decorated object and to only
    the passed key-value pairs. It looks for {{key}} placeholders in the docstring
    and replaces them with the corresponding values from kwargs.

    .. note::

        - If used without arguments, the decorator will not modify the docstring.
        - {} Placeholders in the docstring that do not have corresponding keys
          in kwargs will remain unchanged. This means that if the docstring contains
          code examples or other text with braces, those will not be affected.
        - Changes will probably NOT be reflected in IDE tooltips. They are intended
          for runtime documentation access (e.g., via `help()` or `.__doc__` access)
          or for generating external documentation. Tools that read docstrings
          statically from source code will not see the changes.

          Therefore, this decorator is best suited for adding dynamic information
          such as version numbers, author names, or configuration-dependent details
          to docstrings, rather than for altering the fundamental description of
          the class or function. It should be used carefully with awareness that
          it may appear either with or without the changes so to avoid confusion
          either way.

    Examples:

    .. code-block:: python

        @format_docstring(version="1.2.3")
        class MyClass:
            '''My class, version {version}'''
            pass

        @format_docstring(author="Me")
        def my_function():
            '''A function by {author}'''
            pass

    :param cls_or_func: The class or function to decorate. If None, the decorator is being called with arguments.
    :type cls_or_func: Optional[Callable[..., Any]]
    :param kwargs: Key-value pairs to format the docstring.
    :return: The decorated class or function. If called with keyword arguments,
        returns a decorator function that is then applied to the target object.
    :rtype: T | Callable[[T], T]
    """
    # This is the actual decorator that will be applied to the class or function.
    # It uses the 'kwargs' from the outer scope.
    def decorator(inner_obj: T) -> T:
        if inner_obj.__doc__ is not None and kwargs:
            inner_obj.__doc__ = _replace_docstring_placeholders(
                                    docstring=inner_obj.__doc__,
                                    kwargs=kwargs)
        return inner_obj

    # Case 1: Called with arguments, e.g., @format_docstring(foo='bar')
    if cls_or_func is None:
        return decorator

    # Case 2: Called without arguments, e.g., @format_docstring
    return decorator(cls_or_func)


def _replace_docstring_placeholders(docstring: str, kwargs: dict) -> str:
    """Replace placeholders in the docstring with values from kwargs.

    :param docstring: The original docstring.
    :type docstring: str
    :param kwargs: A dictionary of placeholder keys and their replacement values.
    :type kwargs: dict
    :return: The modified docstring with placeholders replaced.
    :rtype: str
    """

    def replacer(match: re.Match) -> str:
        key = match.group(1)
        return str(kwargs.get(key, match.group(0)))

    return _PLACEHOLDER_PATTERN.sub(replacer, docstring)
