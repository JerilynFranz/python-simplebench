"""ErrorTags for simplebench.timers in SimpleBench."""

from enum import auto
from simplebench.doc_utils import enum_docstrings
from simplebench.exceptions import ErrorTag


@enum_docstrings
class _TimersErrorTag(ErrorTag):
    """ErrorTags for simplebench.timers in SimpleBench."""

    # timer_identifier() tags
    TIMER_IDENTIFIER_INVALID_TIMER_FUNCTION = auto()
    """The timer argument was not a supported timer function"""

    # _timer_profile_function() tags
    TIMER_PROFILE_FUNCTION_INVALID_ROUNDS_TYPE = auto()
    """The rounds argument was not an int"""
    TIMER_PROFILE_FUNCTION_INVALID_ROUNDS_VALUE = auto()
    """The rounds argument was less than 1"""
    TIMER_PROFILE_FUNCTION_ROUNDS_MUST_BE_AT_LEAST_TWO = auto()
    """The rounds argument must be at least 2 to measure time difference"""

    # _create_timers_profiles_module() tags
    TIMERS_CREATE_TIMERS_PROFILES_MODULE_SPEC_FAILED = auto()
    """Could not create spec for simplebench._timers_profiles module"""

    # timer_precision_ns() tags
    TIMER_PRECISION_NS_INVALID_TIMER_FUNCTION = auto()
    """The timer argument was not a supported timer function"""
    TIMER_PRECISION_NS_UNUSABLE_TIMER = auto()
    """The timer function cannot be used for benchmarking"""

    # timer_overhead_ns() tags
    TIMER_OVERHEAD_NS_INVALID_TIMER_FUNCTION = auto()
    """The timer argument was not a supported timer function"""
    TIMER_OVERHEAD_NS_UNUSABLE_TIMER = auto()
    """The timer function cannot be used for benchmarking"""
