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
        raise TypeError('Expected a Values instance')

    # The vals object is guaranteed to be a tuple containing only float numbers.
"""

from collections.abc import Iterable, Sequence

from simplebench.exceptions import SimpleBenchTypeError
from simplebench.simplebench_types import CoreDataSequence, Self

from ._error_tags import _ValuesErrorTag


class Values(CoreDataSequence):
    """
    An immutable tuple of float numbers that validates its contents upon creation.

    Inherits from CoreDataSequence to provide deep immutability.

    This class is useful for representing a collection of numeric values in a type-safe
    manner, ensuring that all elements are valid floats without requiring deep
    validation elsewhere in the code beyond checking that the type of the input iterable
    is a `Values` instance.

    Example usage:

    .. code-block:: python3

        from simplebench.types import Values

        vals = Values([1, 2.5, 3])

        if not isinstance(vals, Values):
            raise TypeError('Expected a Values instance')

        # The vals object is guaranteed to be a tuple containing only float numbers.

    :param iterable: An iterable of float or int numbers.
    :raises SimpleBenchTypeError: If not an Iterable or contains non-numeric types.
    """

    def __new__(cls, iterable: Iterable[int | float] = ()) -> Self:
        """
        Create a new Values instance from an iterable of int or float numbers.

        Each item in the iterable is converted to a float. This method ensures
        that all elements are valid floats before the tuple is created.

        Example usage:

        .. code-block:: python3

            from simplebench.types import Values

            vals = Values([1, 2.5, 3])

            if not isinstance(vals, Values):
                raise TypeError('Expected a Values instance')

            # The vals object is guaranteed to be a tuple containing only float numbers.

        :param iterable: An iterable of float or int numbers.
        :raises SimpleBenchTypeError: If not an Iterable or contains non-numeric types.
        """
        if not isinstance(iterable, Iterable):
            raise SimpleBenchTypeError(
                f'Invalid type for iterable: {type(iterable)}. Must be an Iterable of int or float.',
                tag=_ValuesErrorTag.INVALID_VALUES_TYPE,
            )

        # Return early if already a Values/Values-subclass instance
        if type(iterable) is cls:
            return iterable

        # Convert to list if not already a Sequence for multiple passes
        # If all items are float, we can skip the conversion step (and its copying overhead)
        raw_iterable = iterable if isinstance(iterable, Sequence) else list(iterable)
        if all(isinstance(item, float) for item in raw_iterable):
            return super().__new__(cls, raw_iterable)

        # We've got ints or mixed types - validate all are int or float
        if not all(isinstance(item, (int, float)) for item in raw_iterable):
            raise SimpleBenchTypeError(
                'All items in the iterable must be int or float', tag=_ValuesErrorTag.INVALID_VALUES_CONTENT_TYPE
            )

        # Convert all items to float and create the Values instance
        return super().__new__(cls, list(float(item) for item in raw_iterable))

    def __repr__(self) -> str:
        """Return a string representation of the Values object."""
        return f'Values({super().__repr__()})'
