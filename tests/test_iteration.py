"""Tests for the simplebench/iteration.py module."""

import pytest

from simplebench.constants import DEFAULT_INTERVAL_SCALE, DEFAULT_INTERVAL_UNIT
from simplebench.exceptions import SimpleBenchTypeError, SimpleBenchValueError, ErrorTag
from simplebench.iteration import Iteration

from .testspec import TestSpec


@pytest.mark.parametrize("testspec", [
    pytest.param(
        TestSpec(
            name="Iteration Initialization - Default Values",
            action=Iteration,
            args=[],
            kwargs={},
            validate_result=lambda result: (result.n == 1 and
                                            result.elapsed == 0 and
                                            result.unit == DEFAULT_INTERVAL_UNIT and
                                            result.scale == DEFAULT_INTERVAL_SCALE and
                                            isinstance(result, Iteration))),
        id="ITERATION_INIT_001"),
    pytest.param(
        TestSpec(
            name="Iteration Initialization - Bad n arg type (str)",
            action=Iteration,
            args=[],
            kwargs={'n': 'a'},
            exception=SimpleBenchTypeError,
            exception_tag=ErrorTag.ITERATION_INIT_N_ARG_TYPE),
        id="ITERATION_INIT_002"),
    pytest.param(
        TestSpec(
            name="Iteration Initialization - Bad n arg value (< 1)",
            action=Iteration,
            args=[],
            kwargs={'n': 0},
            exception=SimpleBenchValueError,
            exception_tag=ErrorTag.ITERATION_INIT_N_ARG_VALUE),
        id="ITERATION_INIT_003"),
    pytest.param(
        TestSpec(
            name="Iteration Initialization - Bad n arg value (float)",
            action=Iteration,
            args=[],
            kwargs={'n': 1.0},
            exception=SimpleBenchTypeError,
            exception_tag=ErrorTag.ITERATION_INIT_N_ARG_TYPE),
        id="ITERATION_INIT_004"),
    pytest.param(
        TestSpec(
            name="Iteration Initialization - Bad elapsed arg type (float)",
            action=Iteration,
            args=[],
            kwargs={'elapsed': 1.0},
            exception=SimpleBenchTypeError,
            exception_tag=ErrorTag.ITERATION_INIT_ELAPSED_ARG_TYPE),
        id="ITERATION_INIT_005"),
    pytest.param(
        TestSpec(
            name="Iteration Initialization - Bad elapsed arg value (negative)",
            action=Iteration,
            args=[],
            kwargs={'elapsed': -1},
            exception=SimpleBenchValueError,
            exception_tag=ErrorTag.ITERATION_INIT_ELAPSED_ARG_VALUE),
        id="ITERATION_INIT_006"),
    pytest.param(
        TestSpec(
            name="Iteration Initialization - Bad unit arg type (int)",
            action=Iteration,
            args=[],
            kwargs={'unit': 1},
            exception=SimpleBenchTypeError,
            exception_tag=ErrorTag.ITERATION_INIT_UNIT_ARG_TYPE),
        id="ITERATION_INIT_007"),
    pytest.param(
        TestSpec(
            name="Iteration Initialization - Bad unit arg value (empty string)",
            action=Iteration,
            args=[],
            kwargs={'unit': ''},
            exception=SimpleBenchValueError,
            exception_tag=ErrorTag.ITERATION_INIT_UNIT_ARG_VALUE),
        id="ITERATION_INIT_008"),
    pytest.param(
        TestSpec(
            name="Iteration Initialization - bad scale arg type (int)",
            action=Iteration,
            args=[],
            kwargs={'scale': 1},
            exception=SimpleBenchTypeError,
            exception_tag=ErrorTag.ITERATION_INIT_SCALE_ARG_TYPE),
        id="ITERATION_INIT_009"),
    pytest.param(
        TestSpec(
            name="Iteration Initialization - bad scale arg value (non-positive float)",
            action=Iteration,
            args=[],
            kwargs={'scale': 0.0},
            exception=SimpleBenchValueError,
            exception_tag=ErrorTag.ITERATION_INIT_SCALE_ARG_VALUE),
        id="ITERATION_INIT_010"),
    pytest.param(
        TestSpec(
            name="Iteration Initialization - Good args",
            action=Iteration,
            args=[],
            kwargs={'n': 5, 'elapsed': 10, 'unit': 'ms', 'scale': 1e-3},
            validate_result=lambda result: (result.n == 5 and
                                            result.elapsed == 10 and
                                            result.unit == 'ms' and
                                            result.scale == 1e-3 and
                                            result.per_round_elapsed == 0.002 and
                                            result.ops_per_second == 500.0)),
        id="ITERATION_INIT_011"),
    pytest.param(
        TestSpec(
            name="Iteration Initialization - Good args with zero elapsed time",
            action=Iteration,
            args=[],
            kwargs={'n': 5, 'elapsed': 0, 'unit': 'ms', 'scale': 1e-3},
            validate_result=lambda result: (result.n == 5 and
                                            result.elapsed == 0 and
                                            result.unit == 'ms' and
                                            result.scale == 1e-3 and
                                            result.per_round_elapsed == 0.0 and
                                            result.ops_per_second == 0.0)),
        id="ITERATION_INIT_012"),
    pytest.param(
        TestSpec(
            name="Iteration Initialization - unknown kw arg",
            action=Iteration,
            args=[],
            kwargs={'unknown_arg': 0},
            exception=TypeError),
        id="ITERATION_INIT_013"),
    pytest.param(
        TestSpec(
            name="Iteration Initialization - positional argument for kw_only field",
            action=Iteration,
            args=[1],
            kwargs={},
            exception=TypeError),
        id="ITERATION_INIT_014"),
    ])
def test_iteration_init(testspec: TestSpec) -> None:
    """Test the initialization of the Iteration class."""
    testspec.run()
