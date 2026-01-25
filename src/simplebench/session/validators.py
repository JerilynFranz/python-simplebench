"""Validators for session-related objects."""

from collections.abc import Callable

from simplebench.exceptions import SimpleBenchTypeError

from ._error_tags import _SessionErrorTag


def validate_timer(timer: Callable[[], int] | None = None) -> Callable[[], int] | None:
    """Validate the timer for a benchmark case.

    :param timer: The timer to validate.
    :return float: The validated timer.
    :raises SimpleBenchTypeError: If timer is not a callable or does not return an int.
    """
    if timer is None:
        return None
    elif not callable(timer):
        raise SimpleBenchTypeError(
            f'Invalid timer: {type(timer)}. Must be a callable.', tag=_SessionErrorTag.PROPERTY_INVALID_TIMER_ARG
        )

    test_value = timer()
    if not isinstance(test_value, int):
        raise SimpleBenchTypeError(
            (f'Invalid timer: {type(timer)}. Timer callable must return an int, got {type(test_value)}.'),
            tag=_SessionErrorTag.PROPERTY_INVALID_TIMER_RETURN_TYPE,
        )

    return timer
