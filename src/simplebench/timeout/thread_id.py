"""Thread ID type definition."""
from ..exceptions import SimpleBenchTypeError, SimpleBenchValueError
from .exceptions import TimeoutErrorTag


class ThreadId(int):
    """Thread ID Type definition.

    This is a subclass of ``int`` that represents thread identifiers in Python.

    It behaves like a standard integer but is specifically used to denote thread IDs
    and checks for type safety when used in functions that require thread identifiers.

    Usage:
        You can use this class to create thread ID objects that behave like integers.

        ```python
        tid = ThreadId(12345)
        print(tid)  # Output: 12345
        print(isinstance(tid, int))  # Output: True
        ```
    """
    def __new__(cls, value: int):
        """Create a new ThreadId instance after validating the value."""
        if not isinstance(value, int):
            raise SimpleBenchTypeError(
                "ThreadId must be initialized with an integer value",
                tag=TimeoutErrorTag.INVALID_THREAD_ID_TYPE)
        if value < 1:
            raise SimpleBenchValueError(
                "ThreadId value must be an integer greater than zero",
                tag=TimeoutErrorTag.INVALID_THREAD_ID_VALUE)

        # Call the parent's __new__ method to create the actual int object
        return super().__new__(cls, value)
