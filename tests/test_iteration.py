"""Tests for the simplebench/iteration.py module."""
import pytest

from simplebench.constants import DEFAULT_INTERVAL_SCALE, DEFAULT_INTERVAL_UNIT
from simplebench.enums import Section
from simplebench.exceptions import SimpleBenchTypeError, SimpleBenchValueError, ErrorTag
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
        exception_tag=ErrorTag.ITERATION_SET_N_ARG_TYPE)),
    idspec("ITERATION_003", TestAction(
        name="Bad n arg value (< 1)",
        action=Iteration,
        args=[],
        kwargs={'n': 0},
        exception=SimpleBenchValueError,
        exception_tag=ErrorTag.ITERATION_SET_N_ARG_VALUE)),
    idspec("ITERATION_004", TestAction(
        name="Bad n arg value (float)",
        action=Iteration,
        args=[],
        kwargs={'n': 1.0},
        exception=SimpleBenchTypeError,
        exception_tag=ErrorTag.ITERATION_SET_N_ARG_TYPE)),
    idspec("ITERATION_005", TestAction(
        name="Bad elapsed arg type (int)",
        action=Iteration,
        args=[],
        kwargs={'elapsed': 1},
        exception=SimpleBenchTypeError,
        exception_tag=ErrorTag.ITERATION_INIT_ELAPSED_ARG_TYPE)),
    idspec("ITERATION_006", TestAction(
        name="Bad elapsed arg value (negative)",
        action=Iteration,
        args=[],
        kwargs={'elapsed': -1.0},
        exception=SimpleBenchValueError,
        exception_tag=ErrorTag.ITERATION_INIT_ELAPSED_ARG_VALUE)),
    idspec("ITERATION_007", TestAction(
        name="Bad unit arg type (int)",
        action=Iteration,
        args=[],
        kwargs={'unit': 1},
        exception=SimpleBenchTypeError,
        exception_tag=ErrorTag.ITERATION_INIT_UNIT_ARG_TYPE)),
    idspec("ITERATION_008", TestAction(
        name="Bad unit arg value (empty string)",
        action=Iteration,
        args=[],
        kwargs={'unit': ''},
        exception=SimpleBenchValueError,
        exception_tag=ErrorTag.ITERATION_INIT_UNIT_ARG_VALUE)),
    idspec("ITERATION_009", TestAction(
        name="bad scale arg type (int)",
        action=Iteration,
        args=[],
        kwargs={'scale': 1},
        exception=SimpleBenchTypeError,
        exception_tag=ErrorTag.ITERATION_INIT_SCALE_ARG_TYPE)),
    idspec("ITERATION_010", TestAction(
        name="bad scale arg value (non-positive float)",
        action=Iteration,
        args=[],
        kwargs={'scale': 0.0},
        exception=SimpleBenchValueError,
        exception_tag=ErrorTag.ITERATION_INIT_SCALE_ARG_VALUE)),
    idspec("ITERATION_011", TestAction(
        name="Good args",
        action=Iteration,
        args=[],
        kwargs={'n': 5, 'elapsed': 10.0, 'unit': 'ms', 'scale': 1e-3},
        validate_result=lambda result: (result.n == 5 and
                                        result.elapsed == 10.0 and
                                        result.unit == 'ms' and
                                        result.scale == 1e-3 and
                                        result.per_round_elapsed == 0.002 and
                                        result.ops_per_second == 500.0))),
    idspec("ITERATION_012", TestAction(
        name="Good args with zero elapsed time",
        action=Iteration,
        args=[],
        kwargs={'n': 5, 'elapsed': 0.0, 'unit': 'ms', 'scale': 1e-3},
        validate_result=lambda result: (result.n == 5 and
                                        result.elapsed == 0.0 and
                                        result.unit == 'ms' and
                                        result.scale == 1e-3 and
                                        result.per_round_elapsed == 0.0 and
                                        result.ops_per_second == 0.0))),
    idspec("ITERATION_013", TestAction(
        name="unknown kw arg",
        action=Iteration,
        args=[],
        kwargs={'unknown_arg': 0},
        exception=TypeError)),
    idspec("ITERATION_014", TestAction(
        name="positional argument for kw_only field",
        action=Iteration,
        args=[1],
        kwargs={},
        exception=TypeError)),
    idspec("ITERATION_015", TestAction(
        name="Bad memory arg type (float)",
        action=Iteration,
        args=[],
        kwargs={'memory': 1.0},
        exception=SimpleBenchTypeError,
        exception_tag=ErrorTag.ITERATION_SET_MEMORY_ARG_TYPE)),
    idspec("ITERATION_016", TestAction(
        name="Bad peak_memory arg type (float)",
        action=Iteration,
        args=[],
        kwargs={'peak_memory': 1.0},
        exception=SimpleBenchTypeError,
        exception_tag=ErrorTag.ITERATION_SET_PEAK_MEMORY_ARG_TYPE)),
    ])
def test_iteration_init(testspec: TestAction) -> None:
    """Test the initialization of the Iteration class."""
    testspec.run()


@pytest.mark.parametrize("testspec", [
    idspec("ITERATION_001", TestAction(
        name="Iteration Section - Section.OPS",
        action=Iteration(elapsed=4.0, scale=1.0).iteration_section,
        args=[Section.OPS],
        validate_result=lambda result: (result == 0.25))),
    idspec("ITERATION_002", TestAction(
        name="Iteration Section - Section.TIMING",
        action=Iteration(elapsed=4.0, scale=1.0).iteration_section,
        args=[Section.TIMING],
        validate_result=lambda result: (result == 4.0))),
    idspec("ITERATION_003", TestAction(
        name="Iteration Section - Section.MEMORY",
        action=Iteration(memory=1024).iteration_section,
        args=[Section.MEMORY],
        validate_result=lambda result: (result == 1024))),
    idspec("ITERATION_004", TestAction(
        name="Iteration Section - Section.PEAK_MEMORY",
        action=Iteration(peak_memory=2048).iteration_section,
        args=[Section.PEAK_MEMORY],
        validate_result=lambda result: (result == 2048))),
    idspec("ITERATION_005", TestAction(
        name="Iteration Section - Section.NULL",
        action=Iteration().iteration_section,
        args=[Section.NULL],
        exception=SimpleBenchValueError,
        exception_tag=ErrorTag.ITERATION_ITERATION_SECTION_UNSUPPORTED_SECTION_ARG_VALUE)),
    idspec("ITERATION_006", TestAction(
        name="Iteration Section - Bad section type (str)",
        action=Iteration().iteration_section,
        args=['bad_section'],
        exception=SimpleBenchTypeError,
        exception_tag=ErrorTag.ITERATION_ITERATION_SECTION_INVALID_SECTION_ARG_TYPE))
])
def test_iteration_section(testspec: TestAction) -> None:
    """Test the iteration_section method of the Iteration class."""
    testspec.run()


def test_repr() -> None:
    """Test the __repr__ method of the Iteration class."""
    it = Iteration(n=10, elapsed=5.0, unit='ms', scale=1e-3, memory=512, peak_memory=1024)
    repr_str = repr(it)
    expected_str = ("Iteration(n=10, elapsed=5.0, unit='ms', "
                    "scale=0.001, memory=512, peak_memory=1024)")
    assert repr_str == expected_str, f"Unexpected repr string: {repr_str}"


def test_eq() -> None:
    """Test the equality operator of the Iteration class."""
    it1 = Iteration(n=10, elapsed=5.0, unit='ms', scale=1e-3, memory=512, peak_memory=1024)
    it2 = Iteration(n=10, elapsed=5.0, unit='ms', scale=1e-3, memory=512, peak_memory=1024)
    it3 = Iteration(n=5, elapsed=2.5, unit='ms', scale=1e-3, memory=256, peak_memory=512)
    assert it1 == it2, "Identical Iteration instances should be equal"
    assert it1 != it3, "Different Iteration instances should not be equal"
    assert it1 != "not an iteration", "Iteration should not be equal to a different type"
