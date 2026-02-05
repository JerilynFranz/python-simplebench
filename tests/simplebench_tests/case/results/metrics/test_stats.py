"""Tests for the simplebench/stats.py module."""
# ruff: noqa: F401  # imported but unused (for type checking)

import math
import statistics
from enum import Enum
from functools import cache
from typing import Any

import pytest
from testspec import (
    Assert,
    PytestAction,
    TestSpec,
)

from simplebench.case.results.metrics.stats import Stats
from simplebench.case.results.metrics.stats._error_tags import _StatsErrorTag
from simplebench.exceptions import SimpleBenchTypeError, SimpleBenchValueError
from simplebench.simplebench_types import Values
from simplebench_tests import factories
from simplebench_tests.kwargs import StatsKWArgs


@cache
def default_values() -> Values:
    """Return default values for stats tests.

    :return: Default values.
    :rtype: Values
    """
    return Values(list(range(0, 101)))

class Nonsense(str, Enum):
    """A nonsense enum value for testing."""
    NONESENSE = 'nonsense'


@cache
def default_stats_kwargs() -> StatsKWArgs:
    """Return default StatsKWArgs for tests.

    :return: Default StatsKWArgs.
    :rtype: StatsKWArgs
    """
    return StatsKWArgs(metric=factories.default_metric(),
                       rounds=10,
                       data=default_values(),
                       timer='timer.perf_counter_ns')

@cache
def default_stats() -> Stats:
    """Fixture to return a minimal Stats instance for each class and subclass for testing.

    :return: Stats instance.
    :rtype: Stats
    """
    return Stats(**default_stats_kwargs())


@pytest.mark.parametrize("testspec", [
    PytestAction("INIT_001",
        name="Only required args (no timer)",
        action=Stats, kwargs=default_stats_kwargs() - {'timer'},
        assertion=Assert.ISINSTANCE,
        expected=Stats),
    PytestAction("INIT_002",
        name="all args (including timer)",
        action=Stats, kwargs=default_stats_kwargs(),
        assertion=Assert.ISINSTANCE,
        expected=Stats),
    PytestAction("INIT_003",
        name="invalid rounds type (str)",
        action=Stats, kwargs=default_stats_kwargs().replace(rounds='not_a_number'),
        exception=SimpleBenchTypeError,
        exception_tag=_StatsErrorTag.INVALID_ROUNDS_ARG_TYPE),
    PytestAction("INIT_004",
        name="invalid rounds value (zero)",
        action=Stats, kwargs=default_stats_kwargs().replace(rounds=0),
        exception=SimpleBenchValueError,
        exception_tag=_StatsErrorTag.INVALID_ROUNDS_ARG_VALUE),
    PytestAction("INIT_005",
        name="invalid data type (str)",
        action=Stats, kwargs=default_stats_kwargs().replace(data='not_a_list'),
        exception=SimpleBenchTypeError,
        exception_tag=_StatsErrorTag.INVALID_DATA_ARG_TYPE),
    PytestAction("INIT_006",
        name="invalid metric type (str)",
        action=Stats, kwargs=default_stats_kwargs().replace(metric='not_a_metric'),
        exception=SimpleBenchTypeError,
        exception_tag=_StatsErrorTag.INVALID_METRIC_ARG_TYPE),
    PytestAction("INIT_007",
        name="invalid timer type (int)",
        action=Stats, kwargs=default_stats_kwargs().replace(timer=123),
        exception=SimpleBenchTypeError,
        exception_tag=_StatsErrorTag.INVALID_TIMER_ARG_TYPE),
    PytestAction("INIT_008",
        name="Missing required metric argument",
        action=Stats, kwargs=default_stats_kwargs() - {'metric'},
        exception=TypeError),
    PytestAction("INIT_009",
        name="Missing required data argument",
        action=Stats, kwargs=default_stats_kwargs() - {'data'},
        exception=TypeError),
    PytestAction("INIT_010",
        name="Missing required rounds argument",
        action=Stats, kwargs=default_stats_kwargs() - {'rounds'},
        exception=TypeError),
])
def test_init(testspec: TestSpec) -> None:
    """Test that the stats module is initialized correctly for shared aspects of init.

    :param testspec: Test action.
    :type testspec: TestSpec
    """
    testspec.run()


@pytest.mark.parametrize("attribute,value", [
    pytest.param('mean', 10.0, id="IMMUTABLE_001 mean"),
    pytest.param('median', 10.0, id="IMMUTABLE_002 median"),
    pytest.param('minimum', 10.0, id="IMMUTABLE_003 minimum"),
    pytest.param('maximum', 10.0, id="IMMUTABLE_004 maximum"),
    pytest.param('standard_deviation', 10.0, id="IMMUTABLE_005 standard_deviation"),
    pytest.param('relative_standard_deviation', 10.0, id="IMMUTABLE_006 relative_standard_deviation"),
    pytest.param('percentiles', {50: 10.0}, id="IMMUTABLE_007 percentiles"),
    pytest.param('metric', factories.default_metric(), id="IMMUTABLE_008 metric"),
    pytest.param('rounds', 10, id="IMMUTABLE_009 rounds"),
    pytest.param('timer', 'timer.perf_counter_ns', id="IMMUTABLE_010 timer"),
    pytest.param('data', Values(), id="IMMUTABLE_011 data"),
])
def test_immutability(attribute: str, value: Any) -> None:
    """Test that all public properties of Stats are immutable.

    :param attribute: Attribute name.
    :type attribute: str
    :param value: Value to set.
    :type value: Any
    """
    with pytest.raises(AttributeError):
        setattr(default_stats(), attribute, value)


def _valid_computed_stats_data(stats: Stats, data: list[float], rounds: int, ident: str) -> None:
    """Tests that computed stats properties return correct values for different data inputs.

    We compute the expected values using the statistics module and compare them to the values
    returned by the Stats instance.

    :param stats: Stats instance to test.
    :type stats: Stats
    :param data: Data to test with.
    :type data: Values
    :param rounds: Number of rounds per data point (used for standard deviation calculation).
    :type rounds: int
    :param ident: Identifier for the test case.
    :type ident: str
    """
    expected_mean: float = statistics.mean(data)
    expected_median: float = statistics.median(data)
    expected_minimum: float = float(min(data))
    expected_maximum: float = float(max(data))
    expected_standard_deviation: float = statistics.stdev(data) * math.sqrt(rounds) if len(data) > 1 else 0.0
    expected_relative_standard_deviation: float = (
        100 * expected_standard_deviation / expected_mean) if expected_mean != 0 else 0.0
    expected_percentiles: Values = Values(statistics.quantiles(data, n=102, method='inclusive')
        ) if len(data) > 1 else Values([float(data[0])] * 101)

    assert stats.mean == expected_mean, (
        f"{ident}: Expected mean {expected_mean}, but got {stats.mean} for {data}")
    assert stats.median == expected_median, (
        f"{ident}: Expected median {expected_median}, but got {stats.median} for {data}")
    assert stats.minimum == expected_minimum, (
        f"{ident}: Expected minimum {expected_minimum}, but got {stats.minimum} for {data}")
    assert stats.maximum == expected_maximum, (
        f"{ident}: Expected maximum {expected_maximum}, but got {stats.maximum} for {data}")
    assert stats.standard_deviation == expected_standard_deviation, (
        f"{ident}: Expected standard deviation {expected_standard_deviation}, "
        f"but got {stats.standard_deviation} for {data}")
    assert stats.relative_standard_deviation == expected_relative_standard_deviation, (
        f"{ident}: Expected relative standard deviation {expected_relative_standard_deviation}, "
        f" but got {stats.relative_standard_deviation} for {data}")
    assert stats.percentiles == expected_percentiles, (
        f"{ident}: Expected percentiles {expected_percentiles}, but got {stats.percentiles} for {data}")


@pytest.mark.parametrize("rounds, data, ident", [
    [1, [10.0], 'COMPUTED_VALUES_001 1 round, single data point'],
    [1, [10.0, 20.0, 30.0, 40.0, 50.0], 'COMPUTED_VALUES_002 1 round, multiple data points'],
    [1, [float(value) for value in range(0, 101)], "COMPUTED_VALUES_003 1 round, 101 data points from 0 to 100"],
    [1, [3.0, 3.0, 3.0, 3.0, 3.0], "COMPUTED_VALUES_004 1 round, 5 identical data points"],
    [4, [10.0], 'COMPUTED_VALUES_005 4 rounds, single data point'],
    [4, [10.0, 20.0, 30.0, 40.0, 50.0], 'COMPUTED_VALUES_006 4 rounds, multiple data points'],
    [4, [float(value) for value in range(0, 101)], "COMPUTED_VALUES_007 4 rounds, 101 data points from 0 to 100"],
    [4, [3.0, 3.0, 3.0, 3.0, 3.0], "COMPUTED_VALUES_008 4 rounds, 5 identical data points"],
])
def test_computed_stats_values(rounds: int, data: list[float], ident: str) -> None:
    """Test that computed stats properties return correct values.

    :param rounds: Number of rounds per data point (used for standard deviation calculation).
    :type rounds: int
    :param data: Sequence of stats data.
    :type data: Sequence[float]
    :param ident: Identifier for the test case.
    :type ident: str
    """
    stats = Stats(**(default_stats_kwargs().replace(data=Values(data), rounds=rounds)))
    _valid_computed_stats_data(stats=stats, data=data, rounds=rounds, ident=ident)


if __name__ == "__main__":
    pytest.main([__file__])
