"""Immutable is a protocol for user defined immutable types.

It provides mechanisms to mark types (including TypedDicts) as immutable
for validation purposes.

The intent is that data structures marked as immutable should be deeply immutable
from the perspective of the caller. No action performed by calling code should be
able to change the public state of an immutable object after creation and initialization.

If the object returns other objects (e.g. from properties or methods), those objects
cannot be used to modify the state of the immutable object. This does not mean that
the object cannot return mutable objects—but modifying those returned objects must
not alter the state of the immutable object itself.

It *may* have internal mutable state for caching or performance reasons,
but the externally visible state should not be modifiable.

Objects marked as Immutable should be safe to share across threads without additional
synchronization logic being required by code using them and be immune to
modification of their public state by other code. If internal mutable state
is used (e.g. for caching), the object is responsible for its own thread-safety.

It does not enforce immutability at runtime - it is only used for type hinting
and validation purposes. It is the responsibility of the user to ensure that
the data structure and its contents are in fact immutable according to the above definition.

For TypedDicts, it uses a special optional key `__immutable__` with a unique
sentinel type `ImmutableSentinel` that is provided by the ImmutableTypedDict class.

For example:

.. code-block:: python
    from typing import TypedDict
    from simplebench.simplebench_types import ImmutableTypedDict

    class ImmutablePoint2D(ImmutableTypedDict):
        x: float
        y: float

This indicates that ImmutablePoint2D is an immutable version of Point2D
and should be treated as such during validation and serialization.

If a data structure other than a TypedDict inherits from Immutable,
it indicates that the data structure itself and all its contents are
expected to be immutable and unchangeable after creation and initialization.

This includes nested data structures.

It uses the existence of the `__immutable__` marker (attribute for general classes,
key for `TypedDict`s specifically) to mark a user-defined class as immutable,
and registers standard Python immutable types (like `int`, `str`)
so they are automatically recognized.
"""
from abc import ABCMeta
from enum import Enum
from typing import Protocol, TypedDict, cast, is_typeddict, runtime_checkable

from simplebench.simplebench_types import Never, NotRequired

__all__ = (
    "Immutable",
    "ImmutableTypedDict",
)


@runtime_checkable
class Immutable(Protocol):
    """Protocol for user defined immutable types.

    This class can be used as a base class for user defined types
    to indicate that the type is immutable.

    Example:

    .. code-block:: python
        from simplebench.simplebench_types import Immutable

        class MyImmutableClass(Immutable):
            ...

    When applied to an existing class, it indicates that the sub-class is an immutable
    version of the base class.

    Note that the protocol does not enforce immutability at runtime - it is only used
    for type hinting and validation purposes. It is the responsibility of the user to
    ensure that the sub-class is indeed immutable.

    For example:

    .. code-block:: python

        from simplebench.simplebench_types import Immutable

        class Point2D:
            def __init__(self, x: float, y: float) -> None:
                self._x = x
                self._y = y

            @property
            def x(self) -> float:
                return self._x

            @x.setter
            def x(self, value: float) -> None:
                self._x = value

            @property
            def y(self) -> float:
                return self._y

            @y.setter
            def y(self, value: float) -> None:
                self._y = value

        class ImmutablePoint2D(Point2D, Immutable):
            '''An immutable version of Point2D.

            We inherit from Point2D to get the interface, and Immutable to mark it.
            We must override the setters to enforce immutability.
            '''
            def __init__(self, x: float, y: float) -> None:
                super().__init__(x, y)

            @property
            def x(self) -> float:
                return self._x

            @x.setter
            def x(self, value: float) -> None:
                raise AttributeError("Cannot modify immutable instance.")

            @property
            def y(self) -> float:
                return self._y

            @y.setter
            def y(self, value: float) -> None:
                raise AttributeError("Cannot modify immutable instance.")

    This indicates that ImmutablePoint2D is an immutable version of Point2D
    and should be treated as such during validation and serialization.

    It is also used for type hinting purposes to indicate immutability for
    user defined types.

    Checking against this protocol can be done using isinstance():

    .. code-block:: python
        from simplebench.simplebench_types import Immutable

        def process_immutable(obj: Immutable) -> None:
            if isinstance(obj, Immutable):
                print("Object is immutable.")
            else:
                print("Object is mutable.")

    It uses the existence of an `__immutable__` attribute to mark a user-defined class
    as immutable for validation purposes.

    Additionally, the following built-in immutable types are explicitly registered as
    virtual subclasses of this protocol:
    `bool`, `int`, `float`, `complex`, `str`, `bytes`, and `type(None)`.

    This allows isinstance checks to recognize these built-in types as immutable
    even though they do not explicitly inherit from the Immutable protocol.
    """
    __slots__ = ()

    __immutable__: bool = True
    """Attribute to indicate that the class is immutable.
    The presence of this attribute indicates immutability.
    """

    @classmethod
    def __subclasshook__(cls, other: type) -> bool:
        """Check if a class implements the Immutable protocol.

        This allows ImmutableTypedDict definitions to be recognized as subclasses
        of Immutable, even though they don't inherit from it directly.
        """
        if cls is Immutable:
            # Check if it is a TypedDict with the __immutable__ key
            if is_typeddict(other) and "__immutable__" in other.__annotations__:
                return True
        return NotImplemented


class ImmutableTypedDict(TypedDict):
    """TypedDict subclass to mark a TypedDict as immutable.

    This class can be used as a base class for user defined TypedDicts
    to indicate that the TypedDict is intended to be immutable.

    .. note::
        This class does not enforce immutability at runtime and does not modify the
        runtime behavior of the TypedDict. It simply adds a special key `__immutable__`
        to the definition of the TypedDict to serve as a marker for validation purposes.

        That special key uses the `NotRequired` and `Never` types to indicate that
        the key should not be provided in instances of the TypedDict.

        It can be manually added to existing TypedDict definitions to mark them as immutable
        without needing to inherit from this class directly. Because the key is marked as
        `NotRequired[Never]`, type checkers will enforce that the key is NOT provided
        when creating instances. It has to be added to the TypedDict definition itself
        using a a 'total=False' TypedDict inheritance to avoid making the key required.

        Example:

        .. code-block:: python
            from typing import TypedDict

            class Point2D(TypedDict):
                x: float
                y: float

            class ImmutablePoint2D(Point2D, total=False):
                __immutable__: NotRequired[Never] # Mark as immutable

    If a TypedDict inherits from `ImmutableTypedDict`, simplebench.simplebench_types will treat instances
    of that TypedDict as immutable for 'is_immutable' checks and validation.

    Instances are still standard Python `dict` objects by default, so it is the responsibility
    of the user to ensure they are not modified after creation. This class does not prevent
    runtime modification; its primary purpose is to help static type checkers and validation
    tools to detect and flag such misuse.

    The runtime enforcement of immutability is outside the scope of this class, though
    it can be implemented separately using a wrapper, proxy, or 'mimic' class that
    structurally matches the TypedDict but is not a regular Python dict if desired.

    If a TypedDict definition is generated from a `ImmutableTypedDict` and
    a proxy or wrapper class is created to enforce immutability at runtime,
    that wrapper class should use the `Immutable` protocol to indicate its immutability
    rather than inheriting from `ImmutableTypedDict` because it is not a `TypedDict` itself.

    It can be checked against the Immutable protocol using issubclass():

    Example:

    .. code-block:: python
        from simplebench.simplebench_types import ImmutableTypedDict, Immutable

        class Point2D(ImmutableTypedDict):
            x: float
            y: float

        assert issubclass(Point2D, Immutable)

    .. note:: `isinstance()` checks will not work for TypedDict instances; use `issubclass()` on the type instead.

        While the *class* definition is a subclass of `Immutable`, *instances* are standard Python `dict` objects
        at runtime and cannot be distinguished from mutable dictionaries.
    """
    __immutable__: NotRequired[Never]
    """Sentinel key to indicate that the TypedDict is immutable.

    The presence of this key in the TypedDict definition with the type
    indicates immutability. The key is not allowed to actually have a value
    in instances of the TypedDict. Type checkers will enforce that the key is not
    provided when creating instances.
    """


# Register built-in immutable types so they pass isinstance(x, Immutable) checks
for _t in (bool, int, float, complex, str, bytes, type(None), Enum, range):
    cast(ABCMeta, Immutable).register(_t)
