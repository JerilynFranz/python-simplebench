"""A Protocol representing a collection-like container of elements.

It defines the expected methods for objects that behave like sets or sequences,
such as lists, tuples, sets, and frozensets, but not including
strings, bytes, mappings, or pure iterables.

This is used to type hint parameters and return types that
are expected to have collection-like characteristics: supporting iteration,
length, and membership tests, but not necessarily ordering or indexing.
"""

from collections.abc import Mapping
from typing import Iterator, Protocol, TypeVar, runtime_checkable

T = TypeVar('T', covariant=True)

# No direct exports from this module. All exports are defined in __init__.py
__all__ = []

@runtime_checkable
class ElementCollection(Protocol[T]):
    """A runtime checkable Protocol representing a collection of elements that
    can be iterated over repeatedly, measured for length, and checked
    for membership.

    It does **not** enforce the exclusions of str, bytes, or Mapping types
    from being considered as ElementCollections by 'isinstance' checks.

    You must explicitly check using the :func:`is_element_collection` function
    rather than relying on :func:`isinstance`.

    It defines the expected methods for objects that have semantics similar to
    sequences or sets where elements can be accessed, counted, and checked for
    presence, but are not necessarily ordered or indexed.

    Exclusions are made for types that do not fit the element container-like behavior,
    such as strings, bytes, Mappings, or pure Iterables.

    Examples of such collections include built-in types
    such as lists, tuples, frozensets, sets, Set, Sequence, etc but not including
    strings, bytes, Mappings, or pure Iterables.

    This is used to type hint parameters and return types that
    are expected to have collection-like characteristics: supporting iteration,
    length, and membership tests, but not necessarily ordering or indexing.
    """
    def __iter__(self) -> Iterator[T]: ...
    def __len__(self) -> int: ...
    def __contains__(self, item: object) -> bool: ...

    @classmethod
    def __subclasshook__(cls, C: type) -> bool:
        if cls is ElementCollection:
            if issubclass(C, (str, bytes, Mapping)):
                return False
            if all(
                any("__" + method + "__" in B.__dict__ for B in C.__mro__)
                for method in ("iter", "len", "contains")
            ):
                return True
        return NotImplemented

def is_element_collection(obj: object) -> bool:
    """Return True if obj is an ElementCollection.

    This function checks if the provided object conforms to the
    ElementCollection Protocol, which requires the presence of
    `__iter__`, `__len__`, and `__contains__` methods,
    while explicitly excluding types such as strings, bytes, and Mappings.

    :param obj: The object to check.
    :type obj: Any
    :return: True if obj is an ElementCollection, False otherwise.
    :rtype: bool
    """
    return isinstance(obj, ElementCollection)and not isinstance(obj, (str, bytes, Mapping))

