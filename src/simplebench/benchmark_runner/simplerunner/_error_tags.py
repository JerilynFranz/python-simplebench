"""ErrorTags for the runners module."""

from simplebench.doc_utils import enum_docstrings
from simplebench.exceptions import ErrorTag


@enum_docstrings
class _SimpleRunnerErrorTag(ErrorTag):
    """ErrorTags for the runners module."""

    # _create_timers_module() tags
    RUNNERS_CREATE_TIMERS_MODULE_INVALID_NAMESPACE_TYPE = 'RUNNERS_CREATE_TIMERS_MODULE_INVALID_NAMESPACE_TYPE'
    """The namespace argument for creating the timers module was not a string."""
    RUNNERS_CREATE_TIMERS_MODULE_INVALID_NAMESPACE_VALUE = 'RUNNERS_CREATE_TIMERS_MODULE_INVALID_NAMESPACE_VALUE'
    """The namespace argument for creating the timers module was not a valid identifier."""

    RUNNERS_CREATE_TIMERS_MODULE_SPEC_FAILED = 'RUNNERS_CREATE_TIMERS_MODULE_SPEC_FAILED'
    """Failed to create the timers module spec"""
    SIMPLERUNNER_TIMER_FUNCTION_INVALID_ROUNDS_TYPE = 'SIMPLERUNNER_TIMER_FUNCTION_INVALID_ROUNDS_TYPE'
    """The rounds argument was not an int"""
    SIMPLERUNNER_TIMER_FUNCTION_INVALID_ROUNDS_VALUE = 'SIMPLERUNNER_TIMER_FUNCTION_INVALID_ROUNDS_VALUE'
    """The rounds argument was less than 1"""
    SIMPLERUNNER_BENCHMARK_TIMEOUT = 'SIMPLERUNNER_BENCHMARK_TIMEOUT'
    """The benchmark execution exceeded the allowed time limit."""

    # calibrate_rounds() tags
    SIMPLERUNNER_CALIBRATE_ROUNDS_INVALID_TIMER_FUNCTION = 'SIMPLERUNNER_CALIBRATE_ROUNDS_INVALID_TIMER_FUNCTION'
    """The timer argument was not a supported timer function"""
    SIMPLERUNNER_CALIBRATE_ROUNDS_INVALID_CPU_TIMER_FUNCTION = (
        'SIMPLERUNNER_CALIBRATE_ROUNDS_INVALID_CPU_TIMER_FUNCTION'
    )
    """The CPU timer argument was not a supported timer function"""
    SIMPLERUNNER_CALIBRATE_ROUNDS_INVALID_KWARGS_TYPE = 'SIMPLERUNNER_CALIBRATE_ROUNDS_INVALID_KWARGS_TYPE'
    """The kwargs argument was not a dict"""
    SIMPLERUNNER_CALIBRATE_ROUNDS_INVALID_KWARGS_KEY_TYPE = 'SIMPLERUNNER_CALIBRATE_ROUNDS_INVALID_KWARGS_KEY_TYPE'
    """A key in the kwargs argument was not a string"""
    SIMPLERUNNER_CALIBRATE_ROUNDS_INVALID_ACTION_TYPE = 'SIMPLERUNNER_CALIBRATE_ROUNDS_INVALID_ACTION_TYPE'
    """The action argument was not a callable"""
    SIMPLERUNNER_CALIBRATE_ROUNDS_UNUSABLE_TIMER = 'SIMPLERUNNER_CALIBRATE_ROUNDS_UNUSABLE_TIMER'
    """The timer function cannot be used for benchmarking"""
    SIMPLERUNNER_CALIBRATE_ROUNDS_INVALID_SETUP = 'SIMPLERUNNER_CALIBRATE_ROUNDS_INVALID_SETUP'
    """The setup argument was not a callable"""
    SIMPLERUNNER_CALIBRATE_ROUNDS_INVALID_TEARDOWN = 'SIMPLERUNNER_CALIBRATE_ROUNDS_INVALID_TEARDOWN'
    """The teardown argument was not a callable"""
