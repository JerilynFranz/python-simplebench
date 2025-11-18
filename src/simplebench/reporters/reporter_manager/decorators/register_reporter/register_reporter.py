"""``@register_reporter`` decorator and supporting functions."""
from simplebench.exceptions import SimpleBenchTypeError
from simplebench.reporters.reporter import Reporter
from simplebench.reporters.reporter_manager.decorators.register_reporter.exceptions import RegisterReporterErrorTag

# reporters registered by clients via the @register_reporter decorator
_REGISTERED_REPORTER_TYPES: set[type[Reporter]] = set()
_REGISTERED_REPORTER_INSTANCES: set[Reporter] = set()
"""Class-level registry of all Reporter instances registered via the @register_reporter decorator."""


def register_reporter(cls: type[Reporter]) -> type[Reporter]:
    """Class decorator to register a :class:`~simplebench.reporters.reporter.Reporter` subclass.

    This decorator can be applied to any subclass of
    :class:`~simplebench.reporters.reporter.Reporter` to register it with the system.
    """
    if not issubclass(cls, Reporter):
        raise SimpleBenchTypeError(
            "reporter_cls must be a subclass of Reporter",
            tag=RegisterReporterErrorTag.INVALID_REPORTER_TYPE_ARG
        )
    # non-base classes only because the base class cannot be instantiated without
    # required arguments and is not useful as a registered reporter by itself
    # This is mainly to prevent someone from trying to register the base Reporter class itself
    if cls is Reporter:
        raise SimpleBenchTypeError(
            "Cannot register the base Reporter class",
            tag=RegisterReporterErrorTag.BASE_REPORTER_TYPE_ARG
        )
    if cls in _REGISTERED_REPORTER_TYPES:
        # Already registered, do nothing
        return cls

    _REGISTERED_REPORTER_TYPES.add(cls)
    _REGISTERED_REPORTER_INSTANCES.add(cls())  # type: ignore[reportCallIssue, call-arg]
    return cls


def get_registered_reporters() -> set[Reporter]:
    """Get all :class:`~simplebench.reporters.reporter.Reporter` instances registered via the
    :func:`~.register_reporter` decorator.

    :return: A set of all registered :class:`~simplebench.reporters.reporter.Reporter` instances.
    :rtype: set[:class:`~simplebench.reporters.reporter.Reporter`]
    """
    return _REGISTERED_REPORTER_INSTANCES


def clear_registered_reporters() -> None:
    """Clear all registered :class:`~simplebench.reporters.reporter.Reporter` instances.

    This is primarily intended for use in unit tests to reset the state
    between tests.
    """
    _REGISTERED_REPORTER_INSTANCES.clear()
    _REGISTERED_REPORTER_TYPES.clear()
