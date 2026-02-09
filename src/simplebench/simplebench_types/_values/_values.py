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

from collections.abc import Iterator, Sequence
from typing import overload

from simplebench._log import _log
from simplebench.exceptions import SimpleBenchTypeError
from simplebench.simplebench_types import CoreDataSequence
from simplebench.simplebench_types._element_collection import ElementCollection, is_element_collection

from ._error_tags import _ValuesErrorTag


class Values(CoreDataSequence[float]):
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
    # Because we enforce all items to be floats BEFORE passing them to the CoreDataSequence constructor,
    # we do NOT set _generic_type to float here. This is for performance since Values usually contain
    # many elements and allows us to skip the generic type check in the CoreDataSequence constructor, which would be
    # redundant and much more expensive than just validating the contents once in the Values constructor.
    _generic_type: type | None = None
    """Marker for generic type parameter for runtime checking purposes by CoreDataSequence.
    Not set to float here for performance reasons since we efficiently pre-validate contents in Values constructor."""

    def __init__(self, __values: CoreDataSequence | ElementCollection[int | float] | None = None) -> None:
        """
        Create a new Values instance from an elementcollection of int or float numbers,
        another Values instance, or a CoreDataSequence.

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
        super().__init__()

        if __values is None:
            self._data = tuple()
            _log.debug('Created empty Values instance')
            return

        if not is_element_collection(__values) and not isinstance(__values, CoreDataSequence):
            raise SimpleBenchTypeError(
                'Values must be initialized with an ElementCollection of int or float numbers '
                'or a CoreDataSequence.',
                tag=_ValuesErrorTag.VALUES_NOT_ELEMENT_COLLECTION_OR_CORE_DATA_SEQUENCE)

        if isinstance(__values, Values):
            self._data = __values._data
            _log.debug('Input is already a Values instance, returning a Values instance.')
            return

        if isinstance(__values, CoreDataSequence):
            if all(isinstance(item, (float)) for item in __values):
                _log.debug('Input is a CoreDataSequence with all float items.')
                self._data = __values._data  # type: ignore
                return
            else:
                _log.debug('Input is a CoreDataSequence but contains non-float items.')
                if not all(isinstance(item, (int, float)) for item in __values):
                    raise SimpleBenchTypeError(
                    'All items in the iterable must be int or float',
                    tag=_ValuesErrorTag.INVALID_VALUES_CONTENT_TYPE
            )
        working_copy = __values if isinstance(__values, Sequence) else list(__values)
        _log.debug('Converting contents of iterable to float for Values instance.')
        if not all(isinstance(item, (int, float)) for item in working_copy):
            raise SimpleBenchTypeError(
                'All items in the iterable must be int or float',
                tag=_ValuesErrorTag.INVALID_VALUES_CONTENT_TYPE
            )
        self._data: tuple[float, ...] = tuple(float(item) for item in working_copy)  # type: ignore[arg-type]
        _log.debug('Values instance created successfully')
        return

    @overload
    def __getitem__(self, index: int) -> float: ...

    @overload
    def __getitem__(self, index: slice) -> 'Values': ...

    def __getitem__(self, index: int | slice) -> 'float | Values':  # type: ignore[override]
        """Get the item or slice at the specified index.

        :param index: The index or slice of the item(s) to retrieve.
        :type index: int | slice
        :returns: The item at the specified index or a CoreDataSequence for a slice.
        :rtype: float | Values
        :raises IndexError: If the index is out of range.
        """
        if isinstance(index, slice):
            return Values(self._data[index])
        return self._data[index]

    def __iter__(self) -> Iterator[float]:
        """Return an iterator over the CoreDataSet.

        :returns: An iterator over the elements in the set.
        :rtype: Iterator[CoreDataTypes]
        """
        return iter(self._data)

    def __eq__(self, other: object) -> bool:
        """Check equality with another Values instance or tuple of floats."""
        if isinstance(other, CoreDataSequence):
            if self._data is other._data:
                return True
            return self._data == other._data
        if isinstance(other, tuple):
            return self._data == other

        raise NotImplementedError(
            f'Equality comparison not implemented between Values and {type(other)!r}'
        )

    def __repr__(self) -> str:
        """Return a string representation of the Values object."""
        return f'Values({self._data!r})'

    # Python disables automatic inheritance of __hash__ when __eq__ is overridden.
    # To ensure Values remains hashable (using the base implementation), we must
    # explicitly define __hash__ and delegate to the superclass.
    def __hash__(self) -> int:
        """Return the hash of the Values object."""
        return super().__hash__()

    def as_tuple(self) -> tuple[float, ...]:
        """Return the contents of the Values as a tuple.

        :returns: The contents of the Values as a tuple.
        :rtype: tuple[float, ...]
        """
        return self._data
