"""simplebench.reporters.reporter.Reporter KWArgs package for SimpleBench tests."""
import inspect
from typing import Any, Iterable, cast

# TODO: Create a new PyPi python-testkwargs package to implement a generic KWArgs class
# using decorators to generate subclasses for specific modeled classes automatically
# similarly to dataclasses instead of manually creating and maintaining each KWArgs
# subclass as done currently. This would reduce boilerplate code and maintenance overhead
# in writing tests for new modeled classes in SimpleBench (e.g., reporters, benchmarks, etc.).
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


class NoDefaultValue:
    """A sentinel class to indicate no default value is provided."""


class KWArgs(dict):
    """A base class to hold keyword arguments for instance initialization.

    This class is primarily used to facilitate testing of class initialization
    with various combinations of parameters, including those that are optional and those
    that have no default value.

    It provides a convenient way to construct a dictionary of parameters to be passed
    to the Reporter class during initialization with linting tools guiding the types of each
    parameter without constraining the presence of or strictly enforcing the types of any parameter.

    This class is intended to be subclassed for specific classes under test,
    with each subclass defining its own __init__ method parameters using the NoDefaultValue pattern.

    Subclass implementation example:

    ```python
    class SpecificKWArgs(KWArgs):
        '''A class to hold keyword arguments for initializing a SpecificClass instance.'''
        from tests.kwargs import KWArgs, NoDefaultValue

        def __init__(  # pylint: disable=unused-argument
                self,
                *,
                name: str | NoDefaultValue = NoDefaultValue()) -> None:
            '''Constructs a SpecificKWArgs instance. This class is used to hold keyword
            arguments for initializing a SpecificClass instance in tests.'''
            # Pass the local scope to the parent constructor. This allows the
            super().__init__(locals())
    ```
    """
    def __init__(
            self, base_class: type, kwargs: dict[str, Any]) -> None:
        """Initializes the KWArgs instance from a dictionary of arguments.

        This constructor is intended to be called from a subclass's __init__
        method via `super().__init__(locals())`. It receives the local scope
        of the subclass constructor, which contains all the keyword arguments
        defined for the specific class being modeled.

        On the first instantiation of a given subclass, this method also inspects
        the subclass and modeled class's __init__ signatures to validate that they match,
        and  cache the set of all possible parameter names for efficient use in other
        methods like `__sub__` and `replace`.

        Args:
            base_class (type): The class that this KWArgs instance is modeling.
            kwargs (dict[str, Any]): A dictionary of arguments, typically from a
                call to `locals()` in a subclass's `__init__` method.
        Raises:
            TypeError: If the provided arguments are not of the expected types.
            AssertionError: If the resulting KWArgs does not match the base class signature parameter names.

        """
        if not isinstance(self, KWArgs):
            raise TypeError("KWArgs must be subclassed.")
        if not isinstance(base_class, type):
            raise TypeError("base_class must be a class type.")
        if not isinstance(kwargs, dict):
            raise TypeError("kwargs must be a dictionary.")
        if not all(isinstance(key, str) for key in kwargs.keys()):
            raise TypeError("All keys in kwargs must be strings.")

        cls = type(self)

        # On first instantiation of this subclass, verify that the __init__ signature
        # matches the modeled class's __init__ signature and cache the base class for
        # future reference.
        if not hasattr(cls, '_BASE_KWARGS_CLASS'):
            kwargclass_matches_modeledclass(kwargs_class=cls, modeled_class=base_class)
            setattr(cls, '_BASE_KWARGS_CLASS', base_class)

        # Cache the __init__ parameter names for use in __sub__ if not already cached.
        # This ensures we get the full set of parameters defined in the subclass __init__
        # whether or not they were provided in this particular call.
        # This reduces the risk of the subclass passing incomplete kwargs to __init__
        # on the first call to the constructor.
        if not hasattr(cls, '_INIT_KWARG_PARAMS'):
            if not hasattr(base_class, '__init__'):
                raise ValueError("base_class must have an __init__ method.")
            kwargs_sig = inspect.signature(base_class.__init__)  # type: ignore[name-defined, misc]
            params = set(kwargs_sig.parameters.keys()) - {'self'}
            setattr(cls, '_INIT_KWARG_PARAMS', params)
        super().__init__(kwargs)

    def replace(self, **kwargs: Any) -> 'KWArgs':
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

        Args:
            **kwargs: Key-value pairs to replace in the new KWArgs instance.

        Returns:
            KWArgs: A new KWArgs instance with specified keys replaced.

        Raises:
            KeyError: If any key in kwargs is not a valid KWArgs key.
        """
        if not isinstance(kwargs, dict):
            raise TypeError("new_kwargs must be provided as keyword arguments.")
        cls = type(self)
        params = cast(set[str], getattr(cls, '_INIT_KWARG_PARAMS'))
        updated_kwargs: dict[str, Any] = {}
        if not all(key in params for key in kwargs):
            raise KeyError("One or more keys to replace are not valid keys.")
        for key in params:
            if key in kwargs:
                updated_kwargs[key] = kwargs[key]
            else:
                updated_kwargs[key] = self[key]
        return cls(**updated_kwargs)

    def __sub__(self, other: Iterable[str]) -> 'KWArgs':
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

        Args:
            other (Iterable[str]): An iterable of keys to be subtracted.

        Returns:
            KWArgs: A new KWArgs instance with keys from the original instance removed.

        Raises:
            KeyError: If any key in other is not a valid KWArgs key.
        """
        cls = type(self)
        params = cast(set[str], getattr(cls, '_INIT_KWARG_PARAMS'))
        new_kwargs: dict[str, Any] = {}
        for_removal = set(other)
        if not all(key in params for key in for_removal):
            raise KeyError("One or more keys to remove are not valid keys.")
        for_copying = params - for_removal
        for key in for_copying:
            new_kwargs[key] = self[key]
        return cls(**new_kwargs)


def kwargclass_matches_modeledclass(kwargs_class: type, modeled_class: type) -> None:
    """Verify KWArgs()__init__() signature matches the ModeledClass().__init__.

    Helper function to compare the __init__ signatures of two classes for testing.

    This test ensures that the KWArgsClass class has the same parameters as
    the ModeledClass class's __init__ method. This prevents discrepancies between
    the two classes that could lead to errors in tests or misunderstandings
    about the parameters required to initialize a ModeledClass instance.

    It does not check parameter types or default values, only the presence
    of parameter names.

    Raises:
        AssertionError: If there are any extra or missing parameters in the
            KWArgsClass compared to the ModeledClass.
    """
    if not hasattr(modeled_class, '__init__') or not hasattr(kwargs_class, '__init__'):
        raise ValueError("Both modeled_class and kwargs_class must have an __init__ method.")
    modeled_sig = inspect.signature(modeled_class.__init__)  # type: ignore[misc]
    kwargs_sig = inspect.signature(kwargs_class.__init__)  # type: ignore[misc]

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
