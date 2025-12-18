"""Values - a validated tuple of float numbers.

This module defines the Values class, which is an immutable tuple of float numbers
that validates its contents upon creation.

This class is useful for representing a collection of numeric values in a type-safe manner,
ensuring that all elements are valid floats without requiring additional validation elsewhere in the code.

Example usage:

.. code-block:: python3

    from simplebench.types import Values
    vals = Values([1, 2.5, 3])

    if not isinstance(vals, Values):
        raise TypeError("Expected a Values instance")

    # The vals object is guaranteed to be a tuple containing only float numbers.
"""
from __future__ import annotations

from typing import Iterable


class Values(tuple):
    """
    An immutable tuple of float numbers that validates its contents upon creation.

    Inherits from tuple, so it behaves like a regular tuple otherwise.

    This class is useful for representing a collection of numeric values in a type-safe
    manner, ensuring that all elements are valid floats without requiring deep
    validation elsewhere in the code beyond checking that the type of the input iterable
    is a `Values` instance.

    Example usage:

    .. code-block:: python3

        from simplebench.types import Values
        vals = Values([1, 2.5, 3])

        if not isinstance(vals, Values):
            raise TypeError("Expected a Values instance")

        # The vals object is guaranteed to be a tuple containing only float numbers.

    :param iterable: An iterable of float or int numbers.
    :raises TypeError: If not an Iterable or contains non-numeric types.
    """

    def __new__(cls, iterable: Iterable[int | float] = ()) -> Values:
        """
        Create a new Values instance from an iterable of int or float numbers.

        Each item in the iterable is converted to a float. This method ensures
        that all elements are valid floats before the tuple is created.

        Example usage:

        .. code-block:: python3

            from simplebench.types import Values
            vals = Values([1, 2.5, 3])

            if not isinstance(vals, Values):
                raise TypeError("Expected a Values instance")

            # The vals object is guaranteed to be a tuple containing only float numbers.

        :param iterable: An iterable of float or int numbers.
        :raises TypeError: If not an Iterable or contains non-numeric types.
        """
        if not isinstance(iterable, Iterable):
            raise TypeError(f"Invalid type for iterable: {type(iterable)}. Must be an Iterable of int or float.")
        raw_iterable = list(iterable)
        if not all(isinstance(item, (int, float)) for item in raw_iterable):
            raise TypeError("All items in the iterable must be int or float")

        float_iterable = (float(item) for item in raw_iterable)
        return super().__new__(cls, float_iterable)

    def __repr__(self) -> str:
        """Return a string representation of the Values object."""
        return f"Values({super().__repr__()})"
