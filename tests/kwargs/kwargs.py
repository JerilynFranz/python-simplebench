"""KWArgs package for creating keyword argument for testing."""

# TODO: Create a new PyPi python-testkwargs package to implement a generic KWArgs class
# using decorators to generate subclasses for specific modeled callables automatically
# similarly to dataclasses instead of manually creating and maintaining each KWArgs
# subclass as done currently. This would reduce boilerplate code and maintenance overhead
# in writing tests for new modeled callables in SimpleBench (e.g., reporters, benchmarks, etc.).
# and be generally useful for other projects as well.
#
# Proposed API:
#
# from testkwargs import kwargs_class, KWArgs
# from simplebench.reporters.reporter import Reporter
#
# @kwargs_class(Reporter, allow_missing=False, allow_mismatched_types=True)
# class ReporterKWArgs(KWArgs):
#     """A KWArgs class for Reporter, automatically generated."""
#
# The decorator would generate the __init__ method and inherit from a base KWArgs class
# that implements the replace() and __sub__() methods as currently done.
# and a new 'remove()' method to remove specified keys (functionality similar to __sub__).
#
# allow_missing=True (the default) modifies the signature to include a
# NoDefaultValue default sentinel type value for non-default parameters to allow
# their omission without type errors. This matches the current behavior of the
# manually implemented KWArgs subclasses and suppresses type checking errors
# when parameters are omitted for testing purposes.
#
# If allow_missing is set to False, then non-default parameters must be provided
# when instantiating the KWArgs subclass, matching the modeled class's __init__.
#
# allow_mismatched_types=True (the default) would disable type checking of
# the provided arguments against the modeled class's __init__ parameter types.
# This suppresses the generation of type checking errors when parameters
# are provided with types that differ from the modeled class's __init__ signature,
# which is useful for testing purposes.
#
# If allow_mismatched_types is set to False, then type checking would be enforced
# on the provided arguments to match the modeled class's __init__ parameter types.
#
# This would allow flexibility in testing scenarios while reducing boilerplate
# and maintenance overhead for KWArgs subclasses.

from __future__ import annotations

import inspect
from typing import Any, Callable, Hashable, Iterable, TypeGuard, TypeVar, cast

T = TypeVar('T')


_CALL_KWARG_PARAMS_CACHE_NAME = '_CALL_KWARG_PARAMS'


class NoDefaultValue:
    """A sentinel class to indicate no default value is provided."""


def is_kwargs(obj: object) -> TypeGuard[KWArgs]:
    """Checks a passed object is a valid KWArgs instance and
    returns true if so, false otherwise.

    This function can be used in type checking to narrow
    the type of an object to KWArgs when the check passes.

    :param obj: The object to check.
    :type obj: object
    :return: True if the object is a KWArgs instance, False otherwise.
    :rtype: bool
    """
    return isinstance(obj, KWArgs)


class KWArgs(dict[str, Any], Hashable):
    """A base class to hold keyword arguments for calling a function or initializing a class.

    This class is primarily used to facilitate testing of function or method calls
    with various combinations of parameters, including those that are optional and those
    that have no default value.

    Classes derived from KWArgs should be named to reflect the function or method they are modeling.

    It provides a convenient way to construct a dictionary of parameters to be passed
    to a function or method, with linting tools guiding the types of each
    parameter without constraining the presence of or strictly enforcing the
    types of any parameter.

    This class is intended to be subclassed for specific functions or methods under test,
    with each subclass defining its own __init__ method parameters using the
    NoDefaultValue pattern.

    Subclass implementation example:

    .. code-block:: python

        class SpecificKWArgs(KWArgs):
            '''A class to hold keyword arguments for calling a specific function.'''
            from tests.kwargs import KWArgs, NoDefaultValue

            def __init__(  # pylint: disable=unused-argument
                    self,
                    *,
                    name: str | NoDefaultValue = NoDefaultValue()) -> None:
                '''Constructs a SpecificKWArgs instance. This class is used to hold keyword
                arguments for calling a specific function in tests.'''
                # Pass the local scope to the parent constructor.
                super().__init__(locals())
    """
    def __init__(
            self, call: Callable[..., Any], kwargs: dict[str, Any]) -> None:
        """Initializes the KWArgs instance from a dictionary of arguments.

        This constructor is intended to be called from a subclass's __init__
        method via `super().__init__(locals())`. It receives the local scope
        of the subclass constructor, which contains all the keyword arguments
        defined for the specific function being modeled.

        On the first instantiation of a given subclass, this method also inspects
        the subclass __init__ and modeled call signatures to validate that they match,
        and cache the set of all possible parameter names for efficient use in other
        methods like `__sub__` and `replace`.

        Because it is a dict, the KWArgs instance behaves like a standard dictionary,
        allowing access to its items via standard dictionary methods and syntax.

        This has the effect of filtering out any parameters that were not defined
        in the modeled call's signature, as well as any parameters that
        were not provided (i.e., those still set to NoDefaultValue).

        :param call: The callable that this KWArgs instance is modeling.
        :type call: Callable[..., Any]
        :param kwargs: A dictionary of arguments, typically from a
                       call to `locals()` in a subclass's `__init__` method.
        :type kwargs: dict[str, Any]
        :raises TypeError: If the provided arguments are not of the expected types.
        :raises AssertionError: If the resulting KWArgs does not match the call argument's signature parameter names.
        """
        if not callable(call):
            raise TypeError("call must be a callable.")
        if not isinstance(kwargs, dict):
            raise TypeError("kwargs must be a dictionary.")
        if not all(isinstance(key, str) for key in kwargs.keys()):
            raise TypeError("All keys in kwargs must be strings.")

        cls = self.__class__

        # On first instantiation of this subclass, verify that the __init__ signature
        # matches the modeled call's signature and cache the call for
        # future reference.
        if not hasattr(cls, '_BASE_KWARGS_CALL'):
            kwargs_class_matches_modeled_call(kwargs_class=cls, modeled_call=call)
            setattr(cls, '_BASE_KWARGS_CALL', call)

        # Cache the __init__ parameter names for use in __sub__ if not already cached.
        # This ensures we get the full set of parameters defined in the subclass __init__
        # whether or not they were provided in this particular call.
        # This reduces the risk of the subclass passing incomplete kwargs to __init__
        # on the first call to the constructor.
        if not hasattr(cls, _CALL_KWARG_PARAMS_CACHE_NAME):
            kwargs_sig = inspect.signature(call)
            params = set(kwargs_sig.parameters.keys()) - set(['self', '__class__'])
            setattr(cls, _CALL_KWARG_PARAMS_CACHE_NAME, params)
        params = cast(set[str], getattr(cls, _CALL_KWARG_PARAMS_CACHE_NAME))

        pass_through_kwargs = {}
        for key, value in kwargs.items():
            if key in params and not isinstance(value, NoDefaultValue):
                pass_through_kwargs[key] = value
        super().__init__(pass_through_kwargs)

    def __hash__(self) -> int:  # type: ignore[override]
        """Computes a hash value for the KWArgs instance based on its items.

        A KWArgs instance is Hashable if all its items are hashable.

        :return: The hash value of the KWArgs instance.
        :rtype: int
        """
        return hash(frozenset(self.items()))

    def __eq__(self, other):
        """Checks equality between this KWArgs instance and another object.

        :param other: The object to compare against.
        :type other: object
        :return: True if the other object is a KWArgs subclass instance with the same items and type,
                 False otherwise.
        :rtype: bool
        """
        if not is_kwargs(other):
            return False
        if type(self) is not type(other):
            return False
        return hash(self) == hash(other)

    def replace(self: T, **kwargs: Any) -> T:
        """Creates a new KWArgs instance with specified keys replaced by new values.

        Example (illustrative only; actual parameters will vary by subclass):

            kwargs = KWArgs(
                name='example_reporter',
                description='An example reporter for testing.',
                sections={Section.OPS, Section.LATENCY},
                targets={Target.CONSOLE, Target.FILE},
                formats={Format.PLAIN_TEXT, Format.RICH_TEXT},
                choices=ExampleChoices()
            )
            modified_kwargs = kwargs.replace(description='A modified description.')
            # modified_kwargs will now have the updated description

        :param kwargs: Key-value pairs to replace in the new KWArgs instance.
        :return: A new KWArgs instance with specified keys replaced.
        :rtype: KWArgs
        :raises KeyError: If any key in kwargs is not a valid KWArgs key.
        """
        if not isinstance(kwargs, dict):
            raise TypeError("new_kwargs must be provided as keyword arguments.")
        if not is_kwargs(self):
            raise TypeError("replace() can only be called on KWArgs and its subclasses instances.")
        cls = type(self)
        params = cast(set[str], getattr(cls, _CALL_KWARG_PARAMS_CACHE_NAME))
        if not all(key in params for key in kwargs):
            invalid_keys = [key for key in kwargs if key not in params]
            bad_keys = f"One or more keys to replace are not valid keys: {invalid_keys}"
            raise KeyError(bad_keys)
        updated_kwargs: dict[str, Any] = {}
        for key in params:
            if key not in self:  # type: ignore[operator]
                continue
            if key in kwargs:
                updated_kwargs[key] = kwargs[key]
            else:
                updated_kwargs[key] = self[key]  # type: ignore[index]
        return cls(**updated_kwargs)  # type: ignore[return-value]

    def __sub__(self: T, other: Iterable[str]) -> T:
        """Subtracts the keys listed in an iterable from this KWArgs instance
        and returns a new KWArgs instance with those keys removed.

        Example (illustrative only; actual parameters will vary by subclass):

            kwargs = KWArgs(
                name='example_reporter',
                description='An example reporter for testing.',
                sections={Section.OPS, Section.LATENCY},
                targets={Target.CONSOLE, Target.FILE},
                formats={Format.PLAIN_TEXT, Format.RICH_TEXT},
                choices=ExampleChoices()
            )
            reduced_kwargs = reporter_kwargs - ['formats', 'choices']
            # reduced_kwargs will now contain all keys except 'formats' and 'choices'

        :param other: An iterable of keys to be subtracted.
        :type other: Iterable[str]
        :return: A new KWArgs instance with keys from the original instance removed.
        :rtype: KWArgs
        :raises KeyError: If any key in other is not a valid KWArgs key.
        """
        if not is_kwargs(self):
            raise TypeError("replace() can only be called on KWArgs instances and subclasses.")
        if not isinstance(other, Iterable):
            raise TypeError("other must be an iterable of strings.")
        if not all(isinstance(key, str) for key in other):
            raise TypeError("All keys in other must be strings.")
        cls = type(self)
        params = cast(set[str], getattr(cls, _CALL_KWARG_PARAMS_CACHE_NAME))
        new_kwargs: dict[str, Any] = {}
        for_removal = set(other)
        if not all(key in params for key in for_removal):
            raise KeyError("One or more keys to remove are not valid keys.")
        for_copying = params - for_removal
        for key in for_copying:
            if key not in self:  # type: ignore[operator]
                continue
            new_kwargs[key] = self[key]  # type: ignore[index]
        return cls(**new_kwargs)  # type: ignore[return-value]


def kwargs_class_matches_modeled_call(kwargs_class: type[KWArgs],
                                      modeled_call: Callable[..., Any]) -> None:
    """Verify KWArgs().__init__() signature matches the modeled call signature.

    Helper function to compare the signatures for testing.

    This test ensures that the kwargs_class has the same parameters as
    the modeled_call call signature. This prevents discrepancies between
    the two that could lead to errors in tests or misunderstandings
    about the parameters required to call the modeled call.

    It does not check parameter types or default values, only the presence
    or absence of parameter names.

    :raises AssertionError: If there are any extra or missing parameters in the
                            kwargs_class compared to the modeled_call
    """
    if not hasattr(kwargs_class, '__init__'):
        raise TypeError("kwargs_class must have an __init__ method.")
    if not callable(modeled_call):
        raise TypeError("modeled_call must be a callable.")
    modeled_sig = inspect.signature(modeled_call)
    kwargs_sig = inspect.signature(kwargs_class.__init__)

    # Get parameter names (excluding 'self')
    modeled_params = set(modeled_sig.parameters.keys()) - {'self'}
    kwargs_params = set(kwargs_sig.parameters.keys()) - {'self'}
    extra_parameters = kwargs_params - modeled_params
    missing_parameters = modeled_params - kwargs_params

    error_messages = []
    if extra_parameters:
        error_messages.append(
            f"{kwargs_class.__name__} has extra parameters: {extra_parameters}")
    if missing_parameters:
        error_messages.append(
            f"{kwargs_class.__name__} is missing parameters: {missing_parameters}")
    error = "\n".join(error_messages)

    assert modeled_params == kwargs_params, error
