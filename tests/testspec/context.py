"""TestSpec testing framework - context management."""
from typing import Any


class Context(dict[str, Any]):
    """A simple context dictionary for holding test parameters and state.

    This class extends the built-in dict to provide a convenient way to
    store and access context-specific data during test execution.

    It can be used to share data between different parts of a test case,
    such as setup, execution, and validation phases.
    """
    def __init__(self, /, **kwargs: Any) -> None:
        """Initialize the Context with optional keyword arguments.

        Keys must be valid python identifiers (str) and cannot shadow existing attributes or methods.

        Example:

            context = Context(param1=42, param2="value")

        :param kwargs: Key-value pairs to initialize the context dictionary.
            They must be valid python identifiers as keys (str) and can have any type as values.
        :type kwargs: Any
        :raises TypeError:
            - If any key in kwargs is not of type str.
            - If any key in kwargs is not a valid python identifier (str).
            - If any key in kwargs shadows existing attributes or methods of the Context class.
            - If any key in kwargs starts or ends with double underscores '__'.
        """
        # pylint: disable=consider-iterating-dictionary
        if not all(isinstance(key, str) for key in kwargs.keys()):
            raise TypeError("All keys in Context must be of type str")
        if not all(key.isidentifier() for key in kwargs.keys()):
            raise TypeError("All keys in Context must be valid python identifiers")
        if not all(not key.startswith('__') and not key.endswith('__') for key in kwargs.keys()):
            raise TypeError("Context keys cannot start or end with double underscores '__'")
        if not all(not hasattr(self, key) for key in kwargs.keys()):
            raise TypeError("Context keys cannot shadow existing attributes or methods")
        super().__init__(**kwargs)

    def __getattr__(self, name):
        """Get an attribute from the context dictionary.

        :param name: The name of the attribute to get.
        :type name: str
        :return: The value of the attribute.
        :rtype: Any
        :raises AttributeError: If the attribute is not found.
        """
        try:
            return self[name]
        except KeyError:
            raise AttributeError(f"'Context' object has no attribute '{name}'")  # pylint: disable=raise-missing-from
