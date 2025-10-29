"""KWArgs packages for SimpleBench tests."""
import inspect


class NoDefaultValue:
    """A sentinel class to indicate no default value is provided."""


def kwargclass_matches_modeledclass(kwargs_class: type, modeled_class: type) -> None:
    """Verify KWArgs()__init__() signature matches the ModeledClass().__init__.

    Helper function to compare the __init__ signatures of two classes for testing.

    This test ensures that the KWArgsClass class has the same parameters as
    the ModeledClass class's __init__ method. This prevents discrepancies between
    the two classes that could lead to errors in tests or misunderstandings
    about the parameters required to initialize a ModeledClass instance.
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
