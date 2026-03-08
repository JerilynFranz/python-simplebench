"""ErrorTags for the runners module."""

from enum import auto
from simplebench.doc_utils import enum_docstrings
from simplebench.exceptions import ErrorTag


@enum_docstrings
class _SimpleRunnerErrorTag(ErrorTag):
    """ErrorTags for the runners module."""

    # default_runner() tags
    SIMPLERUNNER_PROCESSING_ITERATION_RESULTS_INDEX_ERROR = auto()
    """An invalid index was accessed while processing benchmark iteration results."""

    # _create_timers_module() tags
    RUNNERS_CREATE_TIMERS_MODULE_INVALID_NAMESPACE_TYPE = auto()
    """The namespace argument for creating the timers module was not a string."""
    RUNNERS_CREATE_TIMERS_MODULE_INVALID_NAMESPACE_VALUE = auto()
    """The namespace argument for creating the timers module was not a valid identifier."""

    RUNNERS_CREATE_TIMERS_MODULE_SPEC_FAILED = auto()
    """Failed to create the timers module spec"""
    SIMPLERUNNER_TIMER_FUNCTION_INVALID_ROUNDS_TYPE = auto()
    """The rounds argument was not an int"""
    SIMPLERUNNER_TIMER_FUNCTION_INVALID_ROUNDS_VALUE = auto()
    """The rounds argument was less than 1"""
    SIMPLERUNNER_BENCHMARK_TIMEOUT = auto()
    """The benchmark execution exceeded the allowed time limit."""

    # calibrate_rounds() tags
    SIMPLERUNNER_CALIBRATE_ROUNDS_ERROR = auto()
    """An error occurred during rounds calibration"""
    SIMPLERUNNER_CALIBRATE_ROUNDS_INVALID_CALIBRATE_VALUE = auto()
    """The calibrate argument was not a valid value"""
    SIMPLERUNNER_CALIBRATE_ROUNDS_INVALID_TIMER_FUNCTION = auto()
    """The timer argument was not a supported timer function"""
    SIMPLERUNNER_CALIBRATE_ROUNDS_INVALID_CPU_TIMER_FUNCTION = (
        'SIMPLERUNNER_CALIBRATE_ROUNDS_INVALID_CPU_TIMER_FUNCTION'
    )
    """The CPU timer argument was not a supported timer function"""
    SIMPLERUNNER_CALIBRATE_ROUNDS_INVALID_KWARGS_TYPE = auto()
    """The kwargs argument was not a dict"""
    SIMPLERUNNER_CALIBRATE_ROUNDS_INVALID_KWARGS_KEY_TYPE = auto()
    """A key in the kwargs argument was not a string"""
    SIMPLERUNNER_CALIBRATE_ROUNDS_INVALID_ACTION_TYPE = auto()
    """The action argument was not a callable"""
    SIMPLERUNNER_CALIBRATE_ROUNDS_UNUSABLE_TIMER = auto()
    """The timer function cannot be used for benchmarking"""
    SIMPLERUNNER_CALIBRATE_ROUNDS_INVALID_SETUP = auto()
    """The setup argument was not a callable"""
    SIMPLERUNNER_CALIBRATE_ROUNDS_INVALID_TEARDOWN = auto()
    """The teardown argument was not a callable"""
