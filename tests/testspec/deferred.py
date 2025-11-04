"""TestSpec testing framework - deferred execution."""
from typing import Any, Callable


class Deferred:
    """A wrapper for a value that should be resolved at runtime.

    This allows for lazy evaluation of test parameters that may depend on
    a context created within an idspec closure.

    Usage case examples:

    ```python

    @pytest.mark.parametrize('testspec', [
        # ... other tests ...

        # Example of using context instance identity
        idspec('REPORTER_XXX',
            (lambda: (
                context := Context(reporter=reporter_instance(cache_id='special_reporter')),
                TestAction(
                    name="Action and kwarg refer to the same reporter",
                    action=Deferred(lambda: context.reporter.some_method),
                    kwargs=Deferred(lambda: {
                        'reporter_to_check': context.reporter,
                        'other_param': 'foo'
                    }),
                    # ...
                )
            ))()
        ),
    ])
    def test_reporter(testspec: TestAction) -> None:
        testspec.run()
    ```
    """
    __slots__ = ('_factory',)

    def __init__(self, factory: Callable[..., Any]):
        """Initialize the Deferred context instance with a factory function.

        Args:
            factory (Callable[[], Any]): A callable that produces the actual value when called.
        """
        if not callable(factory):
            raise TypeError("factory must be a callable that takes no arguments")
        self._factory = factory
        """Callable that produces the actual value when called."""

    def resolve(self) -> Any:
        """Execute the factory to get the actual value."""
        return self._factory()


def _resolve_deferred_value(value: Any, default: Any = None) -> Any:
    """Resolves a reference to a value for lazy evaluation as Deferred.

    This is used to allow lazy evaluation of values that may depend on
    other test setup that is not available at the time of TestSpec creation.

    It checks if the value is an instance of Deferred, and if so,
    calls its resolve method to get the actual value. Otherwise, it
    returns the value unchanged.

    Args:
        value (Any):
            The value to resolve.
        default (Any, default=None):
            The default value to return if the passed value is None.

    Returns:
        Any: The resolved value.
    """
    if value is None:
        return default
    return value.resolve() if isinstance(value, Deferred) else value
