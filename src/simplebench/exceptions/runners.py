"""ErrorTags for the runners module."""
from ..enums import enum_docstrings
from .base import ErrorTag


@enum_docstrings
class _RunnersErrorTag(ErrorTag):
    """ErrorTags for the runners module."""
    RUNNERS_CREATE_TIMERS_MODULE_SPEC_FAILED = "RUNNERS_CREATE_TIMERS_MODULE_SPEC_FAILED"
    """Failed to create the timers module spec"""
    SIMPLERUNNER_TIMER_FUNCTION_INVALID_ROUNDS_TYPE = "SIMPLERUNNER_TIMER_FUNCTION_INVALID_ROUNDS_TYPE"
    """The rounds argument was not an int"""
    SIMPLERUNNER_TIMER_FUNCTION_INVALID_ROUNDS_VALUE = "SIMPLERUNNER_TIMER_FUNCTION_INVALID_ROUNDS_VALUE"
    """The rounds argument was less than 1"""
