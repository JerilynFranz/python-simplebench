"""Tests for the simplebench/iteration.py module."""
import pytest

from simplebench.defaults import DEFAULT_INTERVAL_SCALE, DEFAULT_INTERVAL_UNIT
from simplebench.enums import Section
from simplebench.exceptions import SimpleBenchTypeError, SimpleBenchValueError, _IterationErrorTag
from simplebench.iteration import Iteration

from .testspec import TestAction, idspec


@pytest.mark.parametrize("testspec", [
    idspec("ITERATION_001", TestAction(
        name="Default Values",
        action=Iteration,
        args=[],
        kwargs={},
        validate_result=lambda result: (result.n == 1 and
                                        result.elapsed == 0.0 and
                                        result.unit == DEFAULT_INTERVAL_UNIT and
                                        result.scale == DEFAULT_INTERVAL_SCALE and
                                        isinstance(result, Iteration)))),
    idspec("ITERATION_002", TestAction(
        name="Bad n arg type (str)",
        action=Iteration,
        args=[],
        kwargs={'n': 'a'},
        exception=SimpleBenchTypeError,
        exception_tag=_IterationErrorTag.N_ARG_TYPE)),
    idspec("ITERATION_003", TestAction(
        name="Bad n arg value (< 1)",
        action=Iteration,
        args=[],
        kwargs={'n': 0},
        exception=SimpleBenchValueError,
        exception_tag=_IterationErrorTag.N_ARG_VALUE)),
    idspec("ITERATION_004", TestAction(
        name="Bad elapsed arg type (str)",
        action=Iteration,
        args=[],
        kwargs={'elapsed': 'a'},
        exception=SimpleBenchTypeError,
        exception_tag=_IterationErrorTag.ELAPSED_ARG_TYPE)),
    idspec("ITERATION_005", TestAction(
        name="Bad elapsed arg value (negative)",
        action=Iteration,
        args=[],
        kwargs={'elapsed': -1.0},
        exception=SimpleBenchValueError,
        exception_tag=_IterationErrorTag.ELAPSED_ARG_VALUE)),
    idspec("ITERATION_006", TestAction(
        name="Bad unit arg type (int)",
        action=Iteration,
        args=[],
        kwargs={'unit': 1},
        exception=SimpleBenchTypeError,
        exception_tag=_IterationErrorTag.UNIT_ARG_TYPE)),
    idspec("ITERATION_007", TestAction(
        name="Bad unit arg value (empty string)",
        action=Iteration,
        args=[],
        kwargs={'unit': ''},
        exception=SimpleBenchValueError,
        exception_tag=_IterationErrorTag.UNIT_ARG_VALUE)),
    idspec("ITERATION_008", TestAction(
        name="bad scale arg type (str)",
        action=Iteration,
        args=[],
        kwargs={'scale': '1'},
        exception=SimpleBenchTypeError,
        exception_tag=_IterationErrorTag.SCALE_ARG_TYPE)),
    idspec("ITERATION_009", TestAction(
        name="bad scale arg value (non-positive float)",
        action=Iteration,
        args=[],
        kwargs={'scale': 0.0},
        exception=SimpleBenchValueError,
        exception_tag=_IterationErrorTag.SCALE_ARG_VALUE)),
    idspec("ITERATION_010", TestAction(
        name="Good args",
        action=Iteration,
        args=[],
        kwargs={'n': 5, 'rounds': 1, 'elapsed': 10.0, 'unit': 'ms', 'scale': 1e-3},
        validate_result=lambda result: (isinstance(result, Iteration) and
                                        result.n == 5 and
                                        result.rounds == 1 and
                                        result.elapsed == 10.0 and
                                        result.unit == 'ms' and
                                        result.scale == 1e-3 and
                                        result.per_round_elapsed == 0.01 and
                                        result.ops_per_second == 100.0))),
    idspec("ITERATION_011", TestAction(
        name="Good args with zero elapsed time",
        action=Iteration,
        args=[],
        kwargs={'n': 5, 'rounds': 1, 'elapsed': 0.0, 'unit': 'ms', 'scale': 1e-3},
        validate_result=lambda result: (isinstance(result, Iteration) and
                                        result.n == 5 and
                                        result.rounds == 1 and
                                        result.elapsed == 0.0 and
                                        result.unit == 'ms' and
                                        result.scale == 1e-3 and
                                        result.per_round_elapsed == 0.0 and
                                        result.ops_per_second == 0.0))),
    idspec("ITERATION_012", TestAction(
        name="unknown kw arg",
        action=Iteration,
        args=[],
        kwargs={'unknown_arg': 0},
        exception=TypeError)),
    idspec("ITERATION_013", TestAction(
        name="positional argument for kw_only field",
        action=Iteration,
        args=[1],
        kwargs={},
        exception=TypeError)),
    idspec("ITERATION_014", TestAction(
        name="Bad memory arg type (float)",
        action=Iteration,
        args=[],
        kwargs={'memory': 1.0},
        exception=SimpleBenchTypeError,
        exception_tag=_IterationErrorTag.MEMORY_ARG_TYPE)),
    idspec("ITERATION_015", TestAction(
        name="Bad peak_memory arg type (float)",
        action=Iteration,
        args=[],
        kwargs={'peak_memory': 1.0},
        exception=SimpleBenchTypeError,
        exception_tag=_IterationErrorTag.PEAK_MEMORY_ARG_TYPE)),
    ])
def test_iteration_init(testspec: TestAction) -> None:
    """Test the initialization of the Iteration class.

    :param testspec: The test specification to run.
    :type testspec: TestAction
    """
    testspec.run()


@pytest.mark.parametrize("testspec", [
    idspec("ITERATION_016", TestAction(
        name="Iteration Section - Section.OPS",
        action=Iteration(elapsed=4.0, scale=1.0).iteration_section,
        args=[Section.OPS],
        validate_result=lambda result: (result == 0.25))),
    idspec("ITERATION_017", TestAction(
        name="Iteration Section - Section.TIMING",
        action=Iteration(elapsed=4.0, scale=1.0).iteration_section,
        args=[Section.TIMING],
        validate_result=lambda result: (result == 4.0))),
    idspec("ITERATION_018", TestAction(
        name="Iteration Section - Section.MEMORY",
        action=Iteration(memory=1024).iteration_section,
        args=[Section.MEMORY],
        validate_result=lambda result: (result == 1024))),
    idspec("ITERATION_019", TestAction(
        name="Iteration Section - Section.PEAK_MEMORY",
        action=Iteration(peak_memory=2048).iteration_section,
        args=[Section.PEAK_MEMORY],
        validate_result=lambda result: (result == 2048))),
    idspec("ITERATION_020", TestAction(
        name="Iteration Section - Section.NULL",
        action=Iteration().iteration_section,
        args=[Section.NULL],
        exception=SimpleBenchValueError,
        exception_tag=_IterationErrorTag.ITERATION_SECTION_UNSUPPORTED_SECTION_ARG_VALUE)),
    idspec("ITERATION_021", TestAction(
        name="Iteration Section - Bad section type (str)",
        action=Iteration().iteration_section,
        args=['bad_section'],
        exception=SimpleBenchTypeError,
        exception_tag=_IterationErrorTag.ITERATION_SECTION_INVALID_SECTION_ARG_TYPE))
])
def test_iteration_section(testspec: TestAction) -> None:
    """Test the iteration_section method of the Iteration class.

    :param testspec: The test specification to run.
    :type testspec: TestAction
    """
    testspec.run()


def test_repr() -> None:
    """Test the ``__repr__`` method of the Iteration class."""
    it = Iteration(n=10, elapsed=5.0, unit='ms', scale=1e-3, memory=512, peak_memory=1024)
    repr_str = repr(it)
    expected_str = ("Iteration(n=10.0, elapsed=5.0, unit='ms', "
                    "scale=0.001, rounds=1, memory=512, peak_memory=1024)")
    assert repr_str == expected_str, f"Unexpected repr string: {repr_str}"


def test_eq() -> None:
    """Test the equality operator of the Iteration class."""
    it1 = Iteration(n=10, elapsed=5.0, unit='ms', scale=1e-3, memory=512, peak_memory=1024)
    it2 = Iteration(n=10, elapsed=5.0, unit='ms', scale=1e-3, memory=512, peak_memory=1024)
    it3 = Iteration(n=5, elapsed=2.5, unit='ms', scale=1e-3, memory=256, peak_memory=512)
    assert it1 == it2, "Identical Iteration instances should be equal"
    assert it1 != it3, "Different Iteration instances should not be equal"
    assert it1 != "not an iteration", "Iteration should not be equal to a different type"
