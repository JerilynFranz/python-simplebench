"""Tests for the simplebench/stats.py module."""
# Conflicts with pytest fixtures
# pylint: disable=redefined-outer-name
from enum import Enum
import statistics
from typing import Any, Sequence

import pytest

from simplebench.enums import Section
from simplebench.exceptions import SimpleBenchTypeError, SimpleBenchValueError, SimpleBenchKeyError
from simplebench.iteration import Iteration
from simplebench.stats import (Stats, StatsSummary, OperationsPerInterval, OperationTimings,
                               MemoryUsage, PeakMemoryUsage)
from simplebench.stats.exceptions import (StatsErrorTag, StatsSummaryErrorTag,
                                          MemoryUsageErrorTag, PeakMemoryUsageErrorTag,
                                          OperationsPerIntervalErrorTag, OperationTimingsErrorTag)

from .testspec import TestAction, TestGet, TestSet, idspec, Assert, TestSpec, NO_EXPECTED_VALUE


class Nonsense(str, Enum):
    """A nonsense enum value for testing."""
    NONESENSE = 'nonsense'


@pytest.fixture()
def stats_classes() -> list[type[Stats]]:
    """Fixture to return list of stats classes."""
    return [Stats, OperationsPerInterval, OperationTimings, MemoryUsage, PeakMemoryUsage]


@pytest.mark.parametrize("test", [
    idspec("STATS_001", TestAction(
        name="minimal args",
        kwargs={'unit': 'a unit', 'scale': 1.0, 'data': [1.0, 2.0, 3.0]})),
    idspec("STATS_002", TestAction(
        name="all args",
        kwargs={'unit': 'a unit', 'scale': 2.0, 'data': [1.0, 2.0, 3.0]})),
    idspec("STATS_003", TestAction(
        name="invalid unit type (int)",
        kwargs={'unit': 123, 'scale': 1.0, 'data': [1.0, 2.0, 3.0]},
        exception=SimpleBenchTypeError,
        exception_tag=StatsErrorTag.INVALID_UNIT_ARG_TYPE)),
    idspec("STATS_004", TestAction(
        name="invalid unit value (empty str)",
        kwargs={'unit': '', 'scale': 1.0, 'data': [1.0, 2.0, 3.0]},
        exception=SimpleBenchValueError,
        exception_tag=StatsErrorTag.INVALID_UNIT_ARG_VALUE)),
    idspec("STATS_005", TestAction(
        name="invalid scale type (str)",
        kwargs={'unit': 'a unit', 'scale': 'not_a_number', 'data': [1.0, 2.0, 3.0]},
        exception=SimpleBenchTypeError,
        exception_tag=StatsErrorTag.INVALID_SCALE_ARG_TYPE)),
    idspec("STATS_006", TestAction(
        name="invalid scale value (zero)",
        kwargs={'unit': 'a unit', 'scale': 0, 'data': [1.0, 2.0, 3.0]},
        exception=SimpleBenchValueError,
        exception_tag=StatsErrorTag.INVALID_SCALE_ARG_VALUE)),
    idspec("STATS_007", TestAction(
        name="invalid scale value (negative)",
        kwargs={'unit': 'a unit', 'scale': -1.0, 'data': [1.0, 2.0, 3.0]},
        exception=SimpleBenchValueError,
        exception_tag=StatsErrorTag.INVALID_SCALE_ARG_VALUE)),
    idspec("STATS_010", TestAction(
        name="valid initial values, correctly set",
        kwargs={'unit': 'a unit', 'scale': 1.0, 'data': [1.0, 2.0, 3.0]},
        validate_result=lambda obj: obj.unit == 'a unit' and obj.scale == 1.0 and obj.data == (1.0, 2.0, 3.0))),
])
def test_stats_init(stats_classes: list[type[Stats]], test: TestAction) -> None:
    """Test that the stats module is initialized correctly for shared aspects of init."""
    for stats_class in stats_classes:
        test.name = f"{test.name} - {stats_class.__name__}"
        test.action = stats_class
        test.run()


@pytest.mark.parametrize("testspec", [
    idspec("SUBCLASS_INIT_001", TestAction(
        name="Stats - invalid data type (str)",
        action=Stats,
        kwargs={'unit': 'a unit', 'scale': 1.0, 'data': 'not_a_list'},
        exception=SimpleBenchTypeError,
        exception_tag=StatsErrorTag.INVALID_DATA_ARG_TYPE)),
    idspec("SUBCLASS_INIT_002", TestAction(
        name="MemoryUsage - invalid data type (str)",
        action=MemoryUsage,
        kwargs={'unit': 'a unit', 'scale': 1.0, 'data': 'not_a_list'},
        exception=SimpleBenchTypeError,
        exception_tag=MemoryUsageErrorTag.INVALID_DATA_ARG_TYPE)),
    idspec("SUBCLASS_INIT_003", TestAction(
        name="MemoryUsage - no data or iterations provided",
        action=MemoryUsage,
        kwargs={'unit': 'a unit', 'scale': 1.0},
        exception=SimpleBenchTypeError,
        exception_tag=MemoryUsageErrorTag.NO_DATA_OR_ITERATIONS_PROVIDED)),
    idspec("SUBCLASS_INIT_004", TestAction(
        name="MemoryUsage - invalid iterations type (int)",
        action=MemoryUsage,
        kwargs={'unit': 'a unit', 'scale': 1.0, 'data': [1.0, 2.0, 3.0], 'iterations': 123},
        exception=SimpleBenchTypeError,
        exception_tag=MemoryUsageErrorTag.INVALID_ITERATIONS_ARG_TYPE)),
    idspec("SUBCLASS_INIT_005", TestAction(
        name="MemoryUsage - invalid iterations type (str)",
        action=MemoryUsage,
        kwargs={'unit': 'a unit', 'scale': 1.0, 'data': [1.0, 2.0, 3.0], 'iterations': 'not_a_number'},
        exception=SimpleBenchTypeError,
        exception_tag=MemoryUsageErrorTag.INVALID_ITERATIONS_ITEM_ARG_TYPE)),
    idspec("SUBCLASS_INIT_006", TestAction(
        name="MemoryUsage - invalid iterations item type (list with str)",
        action=MemoryUsage,
        kwargs={'unit': 'a unit', 'scale': 1.0, 'data': [1.0, 2.0, 3.0], 'iterations': [1, 'not_a_number']},
        exception=SimpleBenchTypeError,
        exception_tag=MemoryUsageErrorTag.INVALID_ITERATIONS_ITEM_ARG_TYPE)),
    idspec("SUBCLASS_INIT_007", TestAction(
        name="PeakMemoryUsage - invalid data type (str)",
        action=PeakMemoryUsage,
        kwargs={'unit': 'a unit', 'scale': 1.0, 'data': 'not_a_list'},
        exception=SimpleBenchTypeError,
        exception_tag=PeakMemoryUsageErrorTag.INVALID_DATA_ARG_TYPE)),
    idspec("SUBCLASS_INIT_008", TestAction(
        name="PeakMemoryUsage - no data or iterations provided",
        action=PeakMemoryUsage,
        kwargs={'unit': 'a unit', 'scale': 1.0},
        exception=SimpleBenchTypeError,
        exception_tag=PeakMemoryUsageErrorTag.NO_DATA_OR_ITERATIONS_PROVIDED)),
    idspec("SUBCLASS_INIT_009", TestAction(
        name="PeakMemoryUsage - invalid iterations type (int)",
        action=PeakMemoryUsage,
        kwargs={'unit': 'a unit', 'scale': 1.0, 'data': [1.0, 2.0, 3.0], 'iterations': 123},
        exception=SimpleBenchTypeError,
        exception_tag=PeakMemoryUsageErrorTag.INVALID_ITERATIONS_ARG_TYPE)),
    idspec("SUBCLASS_INIT_010", TestAction(
        name="PeakMemoryUsage - invalid iterations type (str)",
        action=PeakMemoryUsage,
        kwargs={'unit': 'a unit', 'scale': 1.0, 'data': [1.0, 2.0, 3.0], 'iterations': 'not_a_number'},
        exception=SimpleBenchTypeError,
        exception_tag=PeakMemoryUsageErrorTag.INVALID_ITERATIONS_ITEM_ARG_TYPE)),
    idspec("SUBCLASS_INIT_011", TestAction(
        name="PeakMemoryUsage - invalid iterations item type (list with str)",
        action=PeakMemoryUsage,
        kwargs={'unit': 'a unit', 'scale': 1.0, 'data': [1.0, 2.0, 3.0], 'iterations': [1, 'not_a_number']},
        exception=SimpleBenchTypeError,
        exception_tag=PeakMemoryUsageErrorTag.INVALID_ITERATIONS_ITEM_ARG_TYPE)),
    idspec("SUBCLASS_INIT_012", TestAction(
        name="OperationsPerInterval - invalid data type (str)",
        action=OperationsPerInterval,
        kwargs={'unit': 'a unit', 'scale': 1.0, 'data': 'not_a_list'},
        exception=SimpleBenchTypeError,
        exception_tag=OperationsPerIntervalErrorTag.INVALID_DATA_ARG_TYPE)),
    idspec("SUBCLASS_INIT_013", TestAction(
        name="OperationsPerInterval - no data or iterations provided",
        action=OperationsPerInterval,
        kwargs={'unit': 'a unit', 'scale': 1.0},
        exception=SimpleBenchTypeError,
        exception_tag=OperationsPerIntervalErrorTag.NO_DATA_OR_ITERATIONS_PROVIDED)),
    idspec("SUBCLASS_INIT_014", TestAction(
        name="OperationsPerInterval - invalid iterations type (int)",
        action=OperationsPerInterval,
        kwargs={'unit': 'a unit', 'scale': 1.0, 'data': [1.0, 2.0, 3.0], 'iterations': 123},
        exception=SimpleBenchTypeError,
        exception_tag=OperationsPerIntervalErrorTag.INVALID_ITERATIONS_ARG_TYPE)),
    idspec("SUBCLASS_INIT_015", TestAction(
        name="OperationsPerInterval - invalid iterations type (str)",
        action=OperationsPerInterval,
        kwargs={'unit': 'a unit', 'scale': 1.0, 'data': [1.0, 2.0, 3.0], 'iterations': 'not_a_number'},
        exception=SimpleBenchTypeError,
        exception_tag=OperationsPerIntervalErrorTag.INVALID_ITERATIONS_ITEM_ARG_TYPE)),
    idspec("SUBCLASS_INIT_016", TestAction(
        name="OperationsPerInterval - invalid iterations item type (list with str)",
        action=OperationsPerInterval,
        kwargs={'unit': 'a unit', 'scale': 1.0, 'data': [1.0, 2.0, 3.0], 'iterations': [1, 'not_a_number']},
        exception=SimpleBenchTypeError,
        exception_tag=OperationsPerIntervalErrorTag.INVALID_ITERATIONS_ITEM_ARG_TYPE)),
    idspec("SUBCLASS_INIT_017", TestAction(
        name="OperationTimings - invalid data value type (list with str)",
        action=OperationTimings,
        kwargs={'unit': 'a unit', 'scale': 1.0, 'data': [1.0, 'not_a_number', 3.0]},
        exception=SimpleBenchTypeError,
        exception_tag=OperationTimingsErrorTag.INVALID_DATA_ARG_TYPE)),
    idspec("SUBCLASS_INIT_018", TestAction(
        name="OperationTimings - no data or iterations provided",
        action=OperationTimings,
        kwargs={'unit': 'a unit', 'scale': 1.0},
        exception=SimpleBenchTypeError,
        exception_tag=OperationTimingsErrorTag.NO_DATA_OR_ITERATIONS_PROVIDED)),
    idspec("SUBCLASS_INIT_019", TestAction(
        name="OperationTimings - invalid iterations type (int)",
        action=OperationTimings,
        kwargs={'unit': 'a unit', 'scale': 1.0, 'data': [1.0, 2.0, 3.0], 'iterations': 123},
        exception=SimpleBenchTypeError,
        exception_tag=OperationTimingsErrorTag.INVALID_ITERATIONS_ARG_TYPE)),
    idspec("SUBCLASS_INIT_020", TestAction(
        name="OperationTimings - invalid iterations type (str)",
        action=OperationTimings,
        kwargs={'unit': 'a unit', 'scale': 1.0, 'data': [1.0, 2.0, 3.0], 'iterations': 'not_a_number'},
        exception=SimpleBenchTypeError,
        exception_tag=OperationTimingsErrorTag.INVALID_ITERATIONS_ITEM_ARG_TYPE)),
    idspec("SUBCLASS_INIT_021", TestAction(
        name="OperationTimings - invalid iterations item type (list with str)",
        action=OperationTimings,
        kwargs={'unit': 'a unit', 'scale': 1.0, 'data': [1.0, 2.0, 3.0], 'iterations': [1, 'not_a_number']},
        exception=SimpleBenchTypeError,
        exception_tag=OperationTimingsErrorTag.INVALID_ITERATIONS_ITEM_ARG_TYPE)),
])
def test_stats_subclasses_init(testspec: TestSpec) -> None:
    """Test aspects of init that vary by subclass."""
    testspec.run()


@pytest.fixture()
def stats_instances() -> list[Stats]:
    """Fixture to return a minimal Stats instance for each class and subclass for testing."""
    return [Stats(unit='unit', scale=1.0, data=[1.0, 2.0, 3.0]),
            OperationsPerInterval(unit='ops/s', scale=1.0, data=[1.0, 2.0, 3.0]),
            OperationTimings(unit='s', scale=1.0, data=[1.0, 2.0, 3.0])]


@pytest.mark.parametrize("test", [
    idspec("SET_001", TestSet(
        name="unit property (setting read-only attribute)",
        attribute='unit',
        value='new unit',
        exception=AttributeError)),
    idspec("SET_002", TestSet(
        name="scale property (setting read-only attribute)",
        attribute='scale',
        value=2.0,
        exception=AttributeError)),
    idspec("SET_003", TestSet(
        name="data property (setting read-only attribute)",
        attribute='data',
        value=[1.0, 2.0, 3.0],
        exception=AttributeError)),
])
def test_stats_set(stats_instances: list[Stats], test: TestSet) -> None:
    """Test stats class property setters."""
    for stats_instance in stats_instances:
        test.name = f"{test.name} ({type(stats_instance).__name__})"
        test.obj = stats_instance
        test.run()


@pytest.mark.parametrize("attribute,value", [
    pytest.param('mean', 10.0, id="COMPUTED_PROPS_001 mean"),
    pytest.param('median', 10.0, id="COMPUTED_PROPS_002 median"),
    pytest.param('minimum', 10.0, id="COMPUTED_PROPS_003 minimum"),
    pytest.param('maximum', 10.0, id="COMPUTED_PROPS_004 maximum"),
    pytest.param('standard_deviation', 10.0, id="COMPUTED_PROPS_005 standard_deviation"),
    pytest.param('relative_standard_deviation', 10.0, id="COMPUTED_PROPS_006 relative_standard_deviation"),
    pytest.param('percentiles', {50: 10.0}, id="COMPUTED_PROPS_007 percentiles"),
])
def test_computed_stats_read_only(stats_instances: list[Stats], attribute: str, value: Any) -> None:
    """Test that computed stats properties exist and are read-only."""
    for stats_instance in stats_instances:
        # only way this should happen is if someone messes up the parametrize above
        if not hasattr(stats_instance, attribute):
            pytest.fail(f"Attribute {attribute} not found in {type(stats_instance).__name__}")
        with pytest.raises(AttributeError):
            setattr(stats_instance, attribute, value)


@pytest.mark.parametrize("stats_data", [
    pytest.param([10.0], id="COMPUTED_VALUES_001 single data point"),
    pytest.param([10.0, 20.0, 30.0, 40.0, 50.0], id="COMPUTED_VALUES_002 multiple data points"),
    pytest.param([float(value) for value in range(0, 101)], id="COMPUTED_VALUES_003 larger data set"),
    pytest.param([3.0, 3.0, 3.0, 3.0, 3.0], id="COMPUTED_VALUES_004 identical data points"),
])
def test_computed_stats_values(stats_data: Sequence[float | int]) -> None:
    """Test that computed stats properties return correct values.
    """
    stats_instance = Stats(unit='unit', scale=1.0, data=list(stats_data))
    data = stats_instance.data

    match len(data):
        case 1:
            assert stats_instance.mean == 10.0, "Mean should be 10.0 for single data point"
            assert stats_instance.median == 10.0, "Median should be 10.0 for single data point"
            assert stats_instance.minimum == 10.0, "Minimum should be 10.0 for single data point"
            assert stats_instance.maximum == 10.0, "Maximum should be 10.0 for single data point"
            assert stats_instance.standard_deviation == 0.0, "Standard deviation should be 0.0 for single data point"
            assert stats_instance.relative_standard_deviation == 0.0, (
                "Relative standard deviation should be 0.0 for single data point")
            assert stats_instance.percentiles == tuple([10.0] * 101), (
                "Percentiles should be all 10.0 for single data point")
        case _:  # Multiple data points
            assert stats_instance.mean == statistics.mean(data), (
                f"Mean value incorrect: expected {statistics.mean(data)}, got {stats_instance.mean}")
            assert stats_instance.median == statistics.median(data), (
                f"Median value incorrect: expected {statistics.median(data)}, got {stats_instance.median}")
            assert stats_instance.minimum == float(min(data)), (
                f"Minimum value incorrect: expected {float(min(data))}, got {stats_instance.minimum}")
            assert stats_instance.maximum == float(max(data)), (
                f"Maximum value incorrect: expected {float(max(data))}, got {stats_instance.maximum}")
            assert stats_instance.standard_deviation == statistics.stdev(data), (
                f"Standard deviation value incorrect: expected {statistics.stdev(data)}, "
                f"got {stats_instance.standard_deviation}")
            assert stats_instance.relative_standard_deviation == (
                statistics.stdev(data) / statistics.mean(data) * 100), (
                "Relative standard deviation value incorrect: expected "
                f"{(statistics.stdev(data) / statistics.mean(data) * 100)}, "
                f"got {stats_instance.relative_standard_deviation}")
            percentiles = tuple(statistics.quantiles(data, n=102, method='inclusive'))
            assert len(percentiles) == 101, (
                f"Percentiles length incorrect: expected 101, got {len(percentiles)}")
            assert stats_instance.percentiles == percentiles, (
                f"Percentiles value incorrect: expected {percentiles}, got {stats_instance.percentiles}")


@pytest.mark.parametrize("stats_data", [
    pytest.param((10.0,), id="COMPUTED_VALUES_001 single data point"),
    pytest.param((10.0, 20.0, 30.0, 40.0, 50.0), id="COMPUTED_VALUES_002 multiple data points"),
    pytest.param((5.0, 15.0, 25.0, 35.0, 45.0, 55.0, 65.0, 75.0, 85.0, 95.0), id="COMPUTED_VALUES_003 larger data set"),
    pytest.param((3.0, 3.0, 3.0, 3.0, 3.0), id="COMPUTED_VALUES_004 identical data points"),
])
def test_as_dict(stats_data: Sequence[float | int]) -> None:
    """Test that as_dict returns correct values."""
    stats_instance = Stats(unit='unit', scale=1.0, data=list(stats_data))
    stats_only_dict = stats_instance.stats_summary.as_dict
    stats_and_data_dict = stats_instance.as_dict

    # Check that the statistics_as_dict contains the expected keys and types
    expected_keys = {
        'type': str,
        'unit': str,
        'mean': float,
        'median': float,
        'minimum': float,
        'maximum': float,
        'standard_deviation': float,
        'relative_standard_deviation': float,
        'percentiles': tuple,
    }
    for key, expected_type in expected_keys.items():
        assert key in stats_only_dict, f"Key '{key}' missing from StatsSummary(...).as_dict"
        assert isinstance(stats_only_dict[key], expected_type), (
            f"Key '{key}' in StatsSummary(...).as_dict should be of type {expected_type.__name__}, "
            f"got {type(stats_only_dict[key]).__name__}")

    # Check that the stats_and_data_dict contains the expected keys and types
    expected_keys_with_data = expected_keys.copy()
    expected_keys_with_data['data'] = tuple
    for key, expected_type in expected_keys_with_data.items():
        assert key in stats_and_data_dict, f"Key '{key}' missing from Stats(...).as_dict"
        assert isinstance(stats_and_data_dict[key], expected_type), (
            f"Key '{key}' in Stats(...).as_dict should be of type {expected_type.__name__}, "
            f"got {type(stats_and_data_dict[key]).__name__}")

    # Check that the data in stats_and_data_dict matches the original data scaled
    scaled_data = tuple(value / stats_instance.scale for value in stats_instance.data)
    assert stats_and_data_dict['data'] == scaled_data, "Data in Stats(..).as_dict does not match scaled data"


def supported_stats_sections() -> set[Section]:
    """Return a list of supported Section enum values for stats classes."""
    return {Section.OPS, Section.TIMING, Section.MEMORY, Section.PEAK_MEMORY}


@pytest.mark.parametrize("section", [
    pytest.param(section, id=f"Section.{section.name}") for section in supported_stats_sections()
])
def test_stats_initalization(section: Section) -> None:
    """Test that data is correctly initialized in stats classes."""
    iterations: list[Iteration] = []
    data: dict[str, tuple[int | float, ...]] = {
        Section.OPS: (1.0, 2.0, 4.0, 5.0, 10.0),
        Section.TIMING: (1.0, 0.5, 0.25, 0.2, 0.1),
        Section.MEMORY: (100, 200, 300, 400, 500),
        Section.PEAK_MEMORY: (150, 250, 350, 450, 550),
    }

    for index in range(len(data[section])):
        iterations.append(
            Iteration(n=1,
                      unit='s',
                      scale=1.0,
                      elapsed=data[Section.TIMING][index],
                      memory=int(data[Section.MEMORY][index]),
                      peak_memory=int(data[Section.PEAK_MEMORY][index]))
        )
    stats_instance: Stats
    try:
        match section:
            case Section.OPS:
                stats_instance = OperationsPerInterval(unit='ops/s', scale=1.0, iterations=iterations)
                ops_data = stats_instance.data
                assert ops_data == data[section], (
                    f"Ops data does not match expected values: {ops_data} != {data['ops']}")

            case Section.TIMING:
                stats_instance = OperationTimings(unit='s', scale=1.0, iterations=iterations)
                timing_data = stats_instance.data
                assert timing_data == data[section], (
                    f"Timing data does not match expected values: {timing_data} != {data['elapsed']}")

            case Section.MEMORY:
                stats_instance = MemoryUsage(unit='bytes', scale=1.0, iterations=iterations)
                memory_data = stats_instance.data
                assert memory_data == data[section], (
                    f"Memory data does not match expected values: {memory_data} != {data['memory']}")

            case Section.PEAK_MEMORY:
                stats_instance = PeakMemoryUsage(unit='bytes', scale=1.0, iterations=iterations)
                peak_memory_data = stats_instance.data
                assert peak_memory_data == data[section], (
                    f"Peak memory data does not match expected values: {peak_memory_data} != {data['peak_memory']}")

            case _:
                pytest.skip(f"Section {section} does not correspond to a tested stats class")
    except Exception as exc:  # pylint: disable=broad-exception-caught
        tag = f', {exc.tag_code.name}' if hasattr(exc, 'tag_code') else ''  # pyright: ignore[reportAttributeAccessIssue]  # pylint: disable=line-too-long  # noqa: E501
        pytest.fail(f"Unexpected error occurred for Section.{section.name} "
                    f"(data = {data[section]}): {exc.__class__.__name__}('{exc}'{tag})")


@pytest.mark.parametrize("testspec", [
    idspec("STATS_FROM_DICT_001", TestAction(
        name="Stats - valid input with unit, scale, and data in data dictionary",
        action=Stats.from_dict,
        kwargs={
            'data': {
                'type': 'Stats:statistics',
                'data': [1.0, 2.0, 3.0],
                'unit': 's',
                'scale': 1.0
            }
        },
        assertion=Assert.ISINSTANCE,
        expected=Stats)),
    idspec("STATS_FROM_DICT_002", TestAction(
        name="OperationsPerInterval - valid input with unit, scale, and data in data dictionary",
        action=OperationsPerInterval.from_dict,
        kwargs={
            'data': {
                'type': 'OperationsPerInterval:statistics',
                'data': [1.0, 2.0, 3.0],
                'unit': 'ops/s',
                'scale': 1.0
            }
        },
        assertion=Assert.ISINSTANCE,
        expected=OperationsPerInterval)),
    idspec("STATS_FROM_DICT_003", TestAction(
        name="OperationTimings - valid input with unit, scale, and data in data dictionary",
        action=OperationTimings.from_dict,
        kwargs={
            'data': {
                'type': 'OperationsTiming:statistics',
                'data': [1.0, 2.0, 3.0],
                'unit': 's',
                'scale': 1.0
            }
        },
        assertion=Assert.ISINSTANCE,
        expected=OperationTimings)),
    idspec("STATS_FROM_DICT_004", TestAction(
        name="MemoryUsage - valid input with unit, scale, and data in data dictionary",
        action=MemoryUsage.from_dict,
        kwargs={
            'data': {
                'type': 'MemoryUsage:statistics',
                'data': [100, 200, 300],
                'unit': 'bytes',
                'scale': 1.0
            }
        },
        assertion=Assert.ISINSTANCE,
        expected=MemoryUsage)),
    idspec("STATS_FROM_DICT_005", TestAction(
        name="PeakMemoryUsage valid input with unit, scale, and data in data dictionary",
        action=PeakMemoryUsage.from_dict,
        kwargs={
            'data': {
                'type': 'PeakMemoryUsage:statistics',
                'data': [150, 250, 350],
                'unit': 'bytes',
                'scale': 1.0
            }
        },
        assertion=Assert.ISINSTANCE,
        expected=PeakMemoryUsage)),
    idspec("STATS_FROM_DICT_006", TestAction(
        name="Stats - missing unit key in data dictionary",
        action=Stats.from_dict,
        kwargs={
            'data': {
                'type': 'Stats:statistics',
                'data': [1.0, 2.0, 3.0],
                'scale': 1.0
            }
        },
        exception=SimpleBenchKeyError,
        exception_tag=StatsErrorTag.FROM_DICT_MISSING_UNIT_KEY)),
    idspec("STATS_FROM_DICT_007", TestAction(
        name="Stats - data arg is not a dict (str)",
        action=Stats.from_dict,
        kwargs={
            'data': 'not_a_dict'
        },
        exception=SimpleBenchTypeError,
        exception_tag=StatsErrorTag.FROM_DICT_INVALID_DATA_ARG_TYPE
    )),
    idspec("STATS_FROM_DICT_008", TestAction(
        name="Stats - missing scale key in data dictionary",
        action=Stats.from_dict,
        kwargs={
            'data': {
                'type': 'Stats:statistics',
                'data': [1.0, 2.0, 3.0],
                'unit': 'unit',
            }
        },
        exception=SimpleBenchKeyError,
        exception_tag=StatsErrorTag.FROM_DICT_MISSING_SCALE_KEY)),
    idspec("STATS_FROM_DICT_009", TestAction(
        name="Stats - missing data key in data dictionary",
        action=Stats.from_dict,
        kwargs={
            'data': {
                'type': 'Stats:statistics',
                'unit': 'unit',
                'scale': 1.0
            }
        },
        exception=SimpleBenchKeyError,
        exception_tag=StatsErrorTag.FROM_DICT_MISSING_DATA_KEY)),
    idspec("STATS_FROM_DICT_010", TestAction(
        name="Stats - data argument not a dictionary",
        action=Stats.from_dict,
        kwargs={
            'data': ['not', 'a', 'dict']
        },
        exception=SimpleBenchTypeError,
        exception_tag=StatsErrorTag.FROM_DICT_INVALID_DATA_ARG_TYPE)),
    idspec("STATS_FROM_DICT_011", TestAction(
        name="StatsSummary - data argument not a dictionary",
        action=StatsSummary.from_dict,
        kwargs={
            'data': ['not', 'a', 'dict']
        },
        exception=SimpleBenchTypeError,
        exception_tag=StatsErrorTag.FROM_DICT_INVALID_DATA_ARG_TYPE)),
    idspec("STATS_FROM_DICT_012", TestAction(
        name="StatsSummary - All valid keys and values",
        action=StatsSummary.from_dict,
        kwargs={
            'data': {
                'type': 'StatsSummary:statistics',
                'unit': 'unit',
                'scale': 1.0,
                'mean': 50.0,
                'median': 50.0,
                'minimum': 0.0,
                'maximum': 3.0,
                'standard_deviation': 29.300170647967224,
                'relative_standard_deviation': 58.60034129593445,
                'percentiles': statistics.quantiles(
                    (float(value) for value in range(0, 101)), n=102, method='inclusive'),
                'data': tuple(float(value) for value in range(1, 101)),
            }
        },
        assertion=Assert.ISINSTANCE,
        expected=StatsSummary)),
    idspec("STATS_FROM_DICT_013", TestAction(
        name="StatsSummary - Missing unit key in data dictionary",
        action=StatsSummary.from_dict,
        kwargs={
            'data': {
                'type': 'StatsSummary:statistics',
                'scale': 1.0,
                'mean': 50.0,
                'median': 50.0,
                'minimum': 0.0,
                'maximum': 3.0,
                'standard_deviation': 29.300170647967224,
                'relative_standard_deviation': 58.60034129593445,
                'percentiles': statistics.quantiles(
                    (float(value) for value in range(0, 101)), n=102, method='inclusive'),
                'data': tuple(float(value) for value in range(1, 101)),
            }
        },
        exception=SimpleBenchKeyError,
        exception_tag=StatsSummaryErrorTag.FROM_DICT_MISSING_KEY)),
    idspec("STATS_FROM_DICT_014", TestAction(
        name="StatsSummary - Missing scale key in data dictionary",
        action=StatsSummary.from_dict,
        kwargs={
            'data': {
                'type': 'StatsSummary:statistics',
                'unit': 'unit',
                'mean': 50.0,
                'median': 50.0,
                'minimum': 0.0,
                'maximum': 3.0,
                'standard_deviation': 29.300170647967224,
                'relative_standard_deviation': 58.60034129593445,
                'percentiles': statistics.quantiles(
                    (float(value) for value in range(0, 101)), n=102, method='inclusive'),
            }
        },
        exception=SimpleBenchKeyError,
        exception_tag=StatsSummaryErrorTag.FROM_DICT_MISSING_KEY)),
    idspec("STATS_FROM_DICT_015", TestAction(
        name="StatsSummary - Missing mean key in data dictionary",
        action=StatsSummary.from_dict,
        kwargs={
            'data': {
                'type': 'StatsSummary:statistics',
                'unit': 'unit',
                'scale': 1.0,
                'median': 50.0,
                'minimum': 0.0,
                'maximum': 100.0,
                'standard_deviation': 29.300170647967224,
                'relative_standard_deviation': 58.60034129593445,
                'percentiles': statistics.quantiles(
                    (float(value) for value in range(0, 101)), n=102, method='inclusive'),
            }
        },
        exception=SimpleBenchKeyError,
        exception_tag=StatsSummaryErrorTag.FROM_DICT_MISSING_KEY)),
    idspec("STATS_FROM_DICT_016", TestAction(
        name="StatsSummary - Missing median key in data dictionary",
        action=StatsSummary.from_dict,
        kwargs={
            'data': {
                'type': 'StatsSummary:statistics',
                'unit': 'unit',
                'scale': 1.0,
                'mean': 50.0,
                'minimum': 0.0,
                'maximum': 100.0,
                'standard_deviation': 29.300170647967224,
                'relative_standard_deviation': 58.60034129593445,
                'percentiles': statistics.quantiles(
                    (float(value) for value in range(0, 101)), n=102, method='inclusive'),
            }
        },
        exception=SimpleBenchKeyError,
        exception_tag=StatsSummaryErrorTag.FROM_DICT_MISSING_KEY)),
    idspec("STATS_FROM_DICT_017", TestAction(
        name="StatsSummary - Missing minimum key in data dictionary",
        action=StatsSummary.from_dict,
        kwargs={
            'data': {
                'type': 'StatsSummary:statistics',
                'unit': 'unit',
                'scale': 1.0,
                'mean': 50.0,
                'median': 50.0,
                'maximum': 100.0,
                'standard_deviation': 29.300170647967224,
                'relative_standard_deviation': 58.60034129593445,
                'percentiles': statistics.quantiles(
                    (float(value) for value in range(0, 101)), n=102, method='inclusive'),
            }
        },
        exception=SimpleBenchKeyError,
        exception_tag=StatsSummaryErrorTag.FROM_DICT_MISSING_KEY)),
    idspec("STATS_FROM_DICT_018", TestAction(
        name="StatsSummary - Missing maximum key in data dictionary",
        action=StatsSummary.from_dict,
        kwargs={
            'data': {
                'type': 'StatsSummary:statistics',
                'unit': 'unit',
                'scale': 1.0,
                'mean': 50.0,
                'median': 50.0,
                'minimum': 0.0,
                'standard_deviation': 29.300170647967224,
                'relative_standard_deviation': 58.60034129593445,
                'percentiles': statistics.quantiles(
                    (float(value) for value in range(0, 101)), n=102, method='inclusive'),
            }
        },
        exception=SimpleBenchKeyError,
        exception_tag=StatsSummaryErrorTag.FROM_DICT_MISSING_KEY)),
    idspec("STATS_FROM_DICT_019", TestAction(
        name="StatsSummary - Missing standard_deviation key in data dictionary",
        action=StatsSummary.from_dict,
        kwargs={
            'data': {
                'type': 'StatsSummary:statistics',
                'unit': 'unit',
                'scale': 1.0,
                'mean': 50.0,
                'median': 50.0,
                'minimum': 0.0,
                'maximum': 100.0,
                'relative_standard_deviation': 58.60034129593445,
                'percentiles': statistics.quantiles(
                    (float(value) for value in range(0, 101)), n=102, method='inclusive'),
            }
        },
        exception=SimpleBenchKeyError,
        exception_tag=StatsSummaryErrorTag.FROM_DICT_MISSING_KEY)),
    idspec("STATS_FROM_DICT_020", TestAction(
        name="StatsSummary - Missing relative_standard_deviation key in data dictionary",
        action=StatsSummary.from_dict,
        kwargs={
            'data': {
                'type': 'StatsSummary:statistics',
                'unit': 'unit',
                'scale': 1.0,
                'mean': 50.0,
                'median': 50.0,
                'minimum': 0.0,
                'maximum': 100.0,
                'standard_deviation': 29.300170647967224,
                'percentiles': statistics.quantiles(
                    (float(value) for value in range(0, 101)), n=102, method='inclusive'),
            }
        },
        exception=SimpleBenchKeyError,
        exception_tag=StatsSummaryErrorTag.FROM_DICT_MISSING_KEY)),
    idspec("STATS_FROM_DICT_021", TestAction(
        name="StatsSummary - Missing percentiles key in data dictionary",
        action=StatsSummary.from_dict,
        kwargs={
            'data': {
                'type': 'StatsSummary:statistics',
                'unit': 'unit',
                'scale': 1.0,
                'mean': 50.0,
                'median': 50.0,
                'minimum': 0.0,
                'maximum': 100.0,
                'standard_deviation': 29.300170647967224,
                'relative_standard_deviation': 58.60034129593445,
            }
        },
        exception=SimpleBenchKeyError,
        exception_tag=StatsSummaryErrorTag.FROM_DICT_MISSING_KEY)),
])
def test_stats_from_dict(testspec: TestSpec) -> None:
    """Test the from_dict class method of the Stats class and sub-classes."""
    testspec.run()


@pytest.mark.parametrize("testspec", [
    idspec("STATS_SUMMARY_001", TestAction(
        name="Construct StatsSummary from Stats instance using from_stats() class method",
        action=StatsSummary.from_stats,
        args=[Stats(unit='unit', scale=1.0, data=[1.0, 2.0, 3.0])],
        assertion=Assert.ISINSTANCE,
        expected=StatsSummary
    )),
    idspec("STATS_SUMMARY_002", TestGet(
        name="Get StatsSummary from Stats instance using stats_summary property",
        obj=Stats(unit='unit', scale=1.0, data=[1.0, 2.0, 3.0]),
        attribute='stats_summary',
        assertion=Assert.ISINSTANCE,
        expected=StatsSummary
    )),
    idspec("STATS_SUMMARY_003", TestGet(
        name="StatsSummary - data attribute is empty tuple",
        obj=StatsSummary.from_stats(Stats(unit='unit', scale=1.0, data=(1.0, 2.0, 3.0))),
        attribute='data',
        assertion=Assert.EQUAL,
        expected=()
    )),
])
def test_stats_summary(testspec: TestSpec) -> None:
    """Test the StatsSummary class."""
    testspec.run()


def compare_stats(stats1: Stats, stats2: Stats) -> None:
    """Helper function to compare two Stats objects for equality, considering scale and unit."""
    if stats1 != stats2:
        error = f"""Stats objects are not equal:
        stats1 = {stats1.as_dict}
        stats2 = {stats2.as_dict}"""
        raise AssertionError(error)


@pytest.mark.parametrize("testspec", [
    idspec("EQUALITY_001", TestAction(
        name="Stats - equal to exported StatsSummary",
        action=Stats.from_dict,
        kwargs={
            'data': {
                'type': 'Stats:statistics',
                'data': [1.0, 2.0, 3.0],
                'unit': 's',
                'scale': 1.0
            }
        },
        validate_result=lambda obj: obj == obj.stats_summary
        )),
    idspec("EQUALITY_002", TestAction(
        name="Stats - equal to seperately defined Stats instance",
        action=Stats,
        kwargs={
            'unit': 's',
            'scale': 1.0,
            'data': [1.0, 2.0, 3.0]
        },
        validate_result=lambda obj: obj == Stats(unit='s', scale=1.0, data=[1.0, 2.0, 3.0])
        )),
    idspec("EQUALITY_003", TestAction(
        name="Stats - equal to Stats with different scales",
        action=compare_stats,
        kwargs={
            'stats1': Stats(unit='ms', scale=0.001, data=[1.0, 2.0, 3.0]),
            'stats2': Stats(unit='s', scale=1.0, data=[0.001, 0.002, 0.003])
        },
        expected=NO_EXPECTED_VALUE
    )),
    idspec("EQUALITY_004", TestAction(
        name="Stats - not equal to Stats with different data",
        action=compare_stats,
        kwargs={
            'stats1': Stats(unit='s', scale=1.0, data=[1.0, 2.0, 3.0]),
            'stats2': Stats(unit='s', scale=1.0, data=[1.0, 2.0, 4.0])
        },
        exception=AssertionError)),
    idspec("EQUALITY_005", TestAction(
        name="Stats - not equal to Stats because different units",
        action=compare_stats,
        kwargs={
            'stats1': Stats(unit='s', scale=1.0, data=[1.0, 2.0, 3.0]),
            'stats2': Stats(unit='ms', scale=1.0, data=[1.0, 2.0, 3.0])
        },
        exception=AssertionError)),
    idspec("EQUALITY_006", TestAction(
        name="Stats - not equal to Stats because different scales",
        action=compare_stats,
        kwargs={
            'stats1': Stats(unit='s', scale=1.0, data=[1.0, 2.0, 3.0]),
            'stats2': Stats(unit='s', scale=0.001, data=[1.0, 2.0, 3.0])
        },
        exception=AssertionError)),
    idspec("EQUALITY_007", TestAction(
        name="Stats - not equal to non-Stats object",
        action=compare_stats,
        kwargs={
            'stats1': Stats(unit='s', scale=1.0, data=[1.0, 2.0, 3.0]),
            'stats2': "not_a_stats_object"  # type: ignore[arg-type]
        },
        exception=AttributeError)),
    idspec("EQUALITY_008", TestAction(
        name="Stats - equal to itself through export as StatsSummary",
        action=compare_stats,
        kwargs={
            'stats1': Stats(unit='s', scale=1.0, data=[1.0, 2.0, 3.0]),
            'stats2': Stats(unit='s', scale=1.0, data=[1.0, 2.0, 3.0]).stats_summary
        })),
    idspec("EQUALITY_009", TestAction(
        name="Stats - equal to itself through export to dict and rehydrate",
        action=compare_stats,
        kwargs={
            'stats1': Stats(unit='s', scale=1.0, data=[1.0, 2.0, 3.0]),
            'stats2': Stats.from_dict(data=Stats(unit='s', scale=1.0, data=[1.0, 2.0, 3.0]).as_dict)
        })),
    idspec("EQUALITY_010", TestAction(
        name="Stats - not equal to Stats with different base unit",
        action=compare_stats,
        kwargs={
            'stats1': Stats(unit='s', scale=1.0, data=[1.0, 2.0, 3.0]),
            'stats2': Stats(unit='min', scale=60.0, data=[1.0, 2.0, 3.0])
        },
        exception=AssertionError)),
    idspec("EQUALITY_011", TestAction(
        name="Stats - equal to Stats with different SI prefix and scale but equivalent data",
        action=compare_stats,
        kwargs={
            'stats1': Stats(unit='s', scale=1.0, data=[0.001, 0.002, 0.003]),
            'stats2': Stats(unit='ms', scale=0.001, data=[1.0, 2.0, 3.0])
        })),
    idspec("EQUALITY_012", TestAction(
        name="StatsSummary - not equal to Stats with different percentiles data",
        action=compare_stats,
        kwargs={
            'stats1': Stats(unit='s', scale=1.0, data=[1.0, 2.0, 3.0]).stats_summary,
            'stats2': StatsSummary.from_dict(
                Stats(unit='s', scale=1.0, data=[1.0, 2.0, 3.0]).as_dict | {'percentiles': (1.0, 2.0, 4.0)})
        },
        exception=AssertionError)),
    idspec("EQUALITY_013", TestAction(
        name="differing length percentiles but otherwise identical StatsSummary are not equal",
        action=compare_stats,
        kwargs={
            'stats1': StatsSummary.from_dict({
                'type': 'StatsSummary:statistics',
                'unit': 'unit',
                'scale': 1.0,
                'mean': 50.0,
                'median': 50.0,
                'minimum': 0.0,
                'maximum': 100.0,
                'standard_deviation': 29.300170647967224,
                'relative_standard_deviation': 58.60034129593445,
                'percentiles': statistics.quantiles(
                    (float(value) for value in range(0, 101)), n=102, method='inclusive'),
            }),
            'stats2': StatsSummary.from_dict({
                'type': 'StatsSummary:statistics',
                'unit': 'unit',
                'scale': 1.0,
                'mean': 50.0,
                'median': 50.0,
                'minimum': 0.0,
                'maximum': 100.0,
                'standard_deviation': 29.300170647967224,
                'relative_standard_deviation': 58.60034129593445,
                'percentiles': tuple(float(value) for value in range(1, 101)),
            }),
        },
        exception=AssertionError)),
    idspec("EQUALITY_014", TestAction(
        name="StatsSummary - differing percentile values but otherwise identical StatsSummary are not equal",
        action=compare_stats,
        kwargs={
            'stats1': StatsSummary.from_dict({
                'type': 'StatsSummary:statistics',
                'unit': 'unit',
                'scale': 1.0,
                'mean': 50.0,
                'median': 50.0,
                'minimum': 0.0,
                'maximum': 100.0,
                'standard_deviation': 29.300170647967224,
                'relative_standard_deviation': 58.60034129593445,
                'percentiles': statistics.quantiles(
                    (float(value) for value in range(0, 101)), n=102, method='inclusive'),
            }),
            'stats2': StatsSummary.from_dict({
                'type': 'StatsSummary:statistics',
                'unit': 'unit',
                'scale': 1.0,
                'mean': 50.0,
                'median': 50.0,
                'minimum': 0.0,
                'maximum': 100.0,
                'standard_deviation': 29.300170647967224,
                'relative_standard_deviation': 58.60034129593445,
                'percentiles': statistics.quantiles(
                    (float(value + 0.1) for value in range(0, 101)), n=102, method='inclusive'),
            }),
        },
        exception=AssertionError)),
])
def test_stats_equality(testspec: TestSpec) -> None:
    """Test the equality operator of the Stats class and sub-classes."""
    testspec.run()


@pytest.mark.parametrize("testspec", [
    idspec("FROM_STATS_001", TestAction(
        name="StatsSummary.from_stats() - input is not a Stats instance (str)",
        action=StatsSummary.from_stats,
        args=['not_a_stats_instance'],
        exception=SimpleBenchTypeError,
        exception_tag=StatsSummaryErrorTag.FROM_STATS_INVALID_STATS_ARG_TYPE)),
])
def test_stats_summaryfrom_stats_error_cases(testspec: TestSpec) -> None:
    """Test StatsSummary.from_stats()"""
    testspec.run()
