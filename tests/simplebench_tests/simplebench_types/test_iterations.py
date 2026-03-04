"""Tests for simplebench.simplebench_types.Iterations class"""
# ruff: noqa: F401
from functools import cache

import pytest
from testspec import Assert, PytestAction, TestSpec

from simplebench.exceptions import SimpleBenchKeyError, SimpleBenchTypeError
from simplebench.metrics import metrics_registry
from simplebench.metrics._metrics import _MetricsErrorTag
from simplebench.simplebench_types import Iterations, Values
from simplebench.simplebench_types._iterations import _IterationsErrorTag
from simplebench_tests import factories

TIMING_STATS_METRIC = metrics_registry['STD_TIMING_STATS']
TIMING_STATS_VALUES = Values(tuple(value for value in range(1,10)))
OPS_STATS_METRIC = metrics_registry['STD_OPS_STATS']
OPS_STATS_VALUES = Values(tuple(1/value for value in range(1,10)))
DEFAULT_ITERATIONS = Iterations({
    TIMING_STATS_METRIC: TIMING_STATS_VALUES,
    OPS_STATS_METRIC: OPS_STATS_VALUES,
})


@pytest.mark.parametrize('testspec', [
    PytestAction('INIT_001',
        name="Minimal valid initialization",
        action=Iterations, args=[{}],
        assertion=Assert.ISINSTANCE,
        expected=Iterations),
    PytestAction('INIT_002',
        name="Valid initialization with multiple metrics",
        action=Iterations, args=[DEFAULT_ITERATIONS],
        assertion=Assert.ISINSTANCE,
        expected=Iterations),
    PytestAction('INIT_003',
        name="Invalid initialization with non-mapping argument",
        action=Iterations, args=[42],
        exception=SimpleBenchTypeError,
        exception_tag=_IterationsErrorTag.ITERATIONS_INVALID_ARG_TYPE),
    PytestAction('INIT_004',
        name="Invalid initialization with non-Metric keys",
        action=Iterations, args=[{42: Values((1,2,3))}],
        exception=SimpleBenchTypeError,
        exception_tag=_IterationsErrorTag.ITERATIONS_INVALID_ARG_KEY_TYPE),
    PytestAction('INIT_005',
        name="Invalid initialization with non-Values values",
        action=Iterations, args=[{TIMING_STATS_METRIC: (1,2,3)}],
        exception=SimpleBenchTypeError,
        exception_tag=_IterationsErrorTag.ITERATIONS_INVALID_ARG_VALUE_TYPE),
])
def test_init(testspec: TestSpec) -> None:
    """Test the initialization of the Iterations class."""
    testspec.run()


@pytest.mark.parametrize('testspec', [
    PytestAction('GETITEM_001',
        name="Get values for existing metric",
        action=lambda iterations: iterations[TIMING_STATS_METRIC],
        args=[DEFAULT_ITERATIONS],
        assertion=Assert.EQUAL,
        expected=TIMING_STATS_VALUES),
    PytestAction('GETITEM_002',
        name="Get values for non-included metric",
        action=lambda iterations: iterations[metrics_registry['STD_MEMORY_STATS']],
        args=[DEFAULT_ITERATIONS],
        exception=SimpleBenchKeyError,
        exception_tag=_IterationsErrorTag.ITERATIONS_KEY_ERROR),
])
def test_getitem(testspec: TestSpec) -> None:
    """Test the __getitem__ method of the Iterations class."""
    testspec.run()


@pytest.mark.parametrize('testspec', [
    PytestAction('CONTAINS_001',
        name="Check if existing metric is in Iterations",
        action=lambda iterations: TIMING_STATS_METRIC in iterations,
        args=[DEFAULT_ITERATIONS],
        assertion=Assert.TRUE),
    PytestAction('CONTAINS_002',
        name="Check if non-included metric is in Iterations",
        action=lambda iterations: metrics_registry['STD_MEMORY_STATS'] in iterations,
        args=[DEFAULT_ITERATIONS],
        assertion=Assert.FALSE),
])
def test_contains(testspec: TestSpec) -> None:
    """Test the __contains__ method of the Iterations class."""
    testspec.run()


@pytest.mark.parametrize('testspec', [
    PytestAction('IMMUTABILITY_001',
        name="Test immutability of Iterations",
        action=lambda iterations: iterations.__setitem__(TIMING_STATS_METRIC, TIMING_STATS_VALUES),
        args=[DEFAULT_ITERATIONS],
        exception=SimpleBenchTypeError,
        exception_tag=_IterationsErrorTag.ITERATIONS_IMMUTABLE),
])
def test_immutability(testspec: TestSpec) -> None:
    """Test the immutability of the Iterations class."""
    testspec.run()


@pytest.mark.parametrize('testspec', [
    PytestAction('ITER_001',
        name="Test Iterations with 2 metrics",
        action=lambda iterations: set(metric for metric in iterations),
        args=[DEFAULT_ITERATIONS],
        assertion=Assert.LEN,
        expected=2),
    PytestAction('ITER_002',
        name="Test Iterations with no metrics",
        action=lambda iterations: set(metric for metric in iterations),
        args=[Iterations({})],
        assertion=Assert.LEN,
        expected=0),
    PytestAction('ITER_003',
        name="Test Iterations with one metric",
        action=lambda iterations: set(metric for metric in iterations),
        args=[Iterations({TIMING_STATS_METRIC: TIMING_STATS_VALUES})],
        assertion=Assert.EQUAL,
        expected=set([TIMING_STATS_METRIC])),
    PytestAction('ITER_004',
        name="Test Iterations with 2 keys for metrics identities",
        action=lambda iterations: set(metric for metric in iterations),
        args=[DEFAULT_ITERATIONS],
        assertion=Assert.EQUAL,
        expected=set([TIMING_STATS_METRIC, OPS_STATS_METRIC])),
])
def test_iteration(testspec: TestSpec) -> None:
    """Test the iteration over the Iterations class."""
    testspec.run()


@pytest.mark.parametrize('testspec', [
    PytestAction('LEN_001',
        name="Test length of Iterations with 2 metrics",
        action=lambda: DEFAULT_ITERATIONS,
        assertion=Assert.LEN,
        expected=2),
    PytestAction('LEN_002',
        name="Test length of Iterations with no metrics",
        action=Iterations, args=[{}],
        assertion=Assert.LEN,
        expected=0),
    PytestAction('LEN_003',
        name="Test length of Iterations with one metric",
        action=Iterations, args=[{TIMING_STATS_METRIC: TIMING_STATS_VALUES}],
        assertion=Assert.LEN,
        expected=1),
])
def test_length(testspec: TestSpec) -> None:
    """Test the length of the Iterations class."""
    testspec.run()


@pytest.mark.parametrize('testspec', [
    PytestAction('EQUALS_001',
        name="Test equality of Iterations with same metrics and values",
        action=lambda: DEFAULT_ITERATIONS,
        assertion=Assert.EQUAL,
        expected=Iterations({
            TIMING_STATS_METRIC: TIMING_STATS_VALUES,
            OPS_STATS_METRIC: OPS_STATS_VALUES,
        })),
    PytestAction('EQUALS_002',
        name="Test equality of Iterations with different metrics",
        action=lambda: DEFAULT_ITERATIONS,
        assertion=Assert.NOT_EQUAL,
        expected=Iterations({
            TIMING_STATS_METRIC: TIMING_STATS_VALUES,
        })),
    PytestAction('EQUALS_003',
        name="Test equality of Iterations with different values",
        action=lambda: DEFAULT_ITERATIONS,
        assertion=Assert.NOT_EQUAL,
        expected=Iterations({
            TIMING_STATS_METRIC: Values((1,2,3)),
            OPS_STATS_METRIC: OPS_STATS_VALUES,
        })),
    PytestAction('EQUALS_004',
        name="Test equality of with non-Iterations object",
        action=lambda: DEFAULT_ITERATIONS,
        assertion=Assert.NOT_EQUAL,
        expected="Not an Iterations object"),
])
def test_equality(testspec: TestSpec) -> None:
    """Test the equality of the Iterations class."""
    testspec.run()


@pytest.mark.parametrize('testspec', [
    PytestAction('HASH_001',
        name="Test hash of Iterations with same metrics and values",
        action=hash, args=[DEFAULT_ITERATIONS],
        assertion=Assert.EQUAL,
        expected=hash(Iterations({
            TIMING_STATS_METRIC: TIMING_STATS_VALUES,
            OPS_STATS_METRIC: OPS_STATS_VALUES,
        }))),
])
def test_hash(testspec: TestSpec) -> None:
    """Test the __hash__ method of the Iterations class."""
    testspec.run()


if __name__ == "__main__":
    pytest.main([__file__])
