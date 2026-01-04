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
    from simplebench.types import ImmutableTypedDict

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

import sys
from abc import ABCMeta
from typing import Any, Protocol, TypedDict, TypeGuard, cast, runtime_checkable

if sys.version_info >= (3, 11):
    from typing import NotRequired
else:
    try:
        from typing_extensions import NotRequired
    except ImportError as e:
        raise ImportError(
            "SimpleBench requires 'typing_extensions' for Python < 3.11 "
            "to support NotRequired.") from e

if sys.version_info >= (3, 10):
    from typing import is_typeddict
else:
    try:
        from typing_extensions import is_typeddict
    except ImportError as e:
        raise ImportError(
            "SimpleBench requires 'typing_extensions' for Python < 3.10 "
            "to support is_typeddict.") from e


class ImmutableSentinel:
    """Sentinel type to indicate immutability in TypedDicts.

    Used as the type for the optional `__immutable__` key in a TypedDict
    to mark the TypedDict as immutable.

    Example:

    .. code-block:: python
        from simplebench.types import ImmutableTypedDict

        class Point2D(ImmutableTypedDict):
            x: float
            y: float

    The presence of a (NotRequired) `__immutable__` key with this type in the
    TypedDict definition indicates that the TypedDict is immutable.

    No such key should actually be present in instances of the TypedDict - it is only used
    for type hinting purposes and the sentinel type cannot be instantiated.
    """
    def __init__(self) -> None:
        """
        This class is not meant to be instantiated.
        """
        raise TypeError("ImmutableSentinel is a sentinel type and cannot be instantiated.")

@runtime_checkable
class Immutable(Protocol):
    """Protocol for user defined immutable types.

    This class can be used as a base class for user defined types
    to indicate that the type is immutable.

    Example:

    .. code-block:: python
        from simplebench.types import Immutable

        class MyImmutableClass(Immutable):
            ...

    When applied to an existing class, it indicates that the sub-class is an immutable
    version of the base class.

    Note that the protocol does not enforce immutability at runtime - it is only used
    for type hinting and validation purposes. It is the responsibility of the user to
    ensure that the sub-class is indeed immutable.

    For example:

    .. code-block:: python

        from simplebench.types import Immutable
    
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
        from simplebench.types import Immutable

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
    to indicate that the TypedDict is immutable.

    .. note::
        This class does not enforce immutability at runtime and does not modify the
        runtime behavior of the TypedDict. It simply adds a special key `__immutable__`
        to the definition of the TypedDict to serve as a marker for validation purposes.

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
        from simplebench.types import ImmutableTypedDict, Immutable

        class Point2D(ImmutableTypedDict):
            x: float
            y: float

        assert issubclass(Point2D, Immutable)

    .. note:: `isinstance()` checks will not work for TypedDict instances; use `issubclass()` on the type instead.

        While the *class* definition is a subclass of `Immutable`, *instances* are standard Python `dict` objects
        at runtime and cannot be distinguished from mutable dictionaries.
    """
    __immutable__: NotRequired[ImmutableSentinel]
    """Sentinel key to indicate that the TypedDict is immutable.
    The presence of this key in the TypedDict definition with the type
    `ImmutableSentinel` indicates immutability.

    The key is NotRequired so it does not need to be present in instances
    - and in fact should not be present in instances. It is only used for
    type hinting purposes and the sentinel type cannot be instantiated.
    """

# Register built-in immutable types so they pass isinstance(x, Immutable) checks
for _t in (bool, int, float, complex, str, bytes, type(None)):
    cast(ABCMeta, Immutable).register(_t)

def is_immutable_typeddict_typehint(type_hint: Any) -> TypeGuard[type[ImmutableTypedDict]]:
    """
    Safely check if a type hint inherits from :class:`~simplebench.types.ImmutableTypedDict`.

    This function is a TypeGuard, which allows static type checkers to understand
    that if this function returns True, the given `type_hint` is a class
    that inherits from ImmutableTypedDict.

    :param Any type_hint: The type hint to check.
    :return bool: True if the type hint inherits from ImmutableTypedDict, False otherwise.
    """
    if not is_typeddict(type_hint):
        return False
    try:
        # Check the MRO directly to see if it inherits from ImmutableTypedDict.
        # This avoids the static checker issue with issubclass and TypedDict.
        return ImmutableTypedDict in type_hint.__mro__
    except (TypeError, AttributeError):
        # issubclass would raise TypeError; __mro__ might raise AttributeError
        # if type_hint is not a class.
        return False
