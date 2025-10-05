"""Tests for the simplebench/stats.py module."""
# Conflicts with pytest fixtures
# pylint: disable=redefined-outer-name
from enum import Enum
import statistics
from typing import Any, Sequence

import pytest

from simplebench.enums import Section
from simplebench.exceptions import SimpleBenchTypeError, SimpleBenchValueError, ErrorTag
from simplebench.iteration import Iteration
from simplebench.stats import Stats, OperationsPerInterval, OperationTimings, MemoryUsage, PeakMemoryUsage

from .testspec import TestAction, TestSet, idspec, Assert, TestSpec


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
        exception_tag=ErrorTag.STATS_INVALID_UNIT_ARG_TYPE)),
    idspec("STATS_004", TestAction(
        name="invalid unit value (empty str)",
        kwargs={'unit': '', 'scale': 1.0, 'data': [1.0, 2.0, 3.0]},
        exception=SimpleBenchValueError,
        exception_tag=ErrorTag.STATS_INVALID_UNIT_ARG_VALUE)),
    idspec("STATS_005", TestAction(
        name="invalid scale type (str)",
        kwargs={'unit': 'a unit', 'scale': 'not_a_number', 'data': [1.0, 2.0, 3.0]},
        exception=SimpleBenchTypeError,
        exception_tag=ErrorTag.STATS_INVALID_SCALE_ARG_TYPE)),
    idspec("STATS_006", TestAction(
        name="invalid scale value (zero)",
        kwargs={'unit': 'a unit', 'scale': 0, 'data': [1.0, 2.0, 3.0]},
        exception=SimpleBenchValueError,
        exception_tag=ErrorTag.STATS_INVALID_SCALE_ARG_VALUE)),
    idspec("STATS_007", TestAction(
        name="invalid scale value (negative)",
        kwargs={'unit': 'a unit', 'scale': -1.0, 'data': [1.0, 2.0, 3.0]},
        exception=SimpleBenchValueError,
        exception_tag=ErrorTag.STATS_INVALID_SCALE_ARG_VALUE)),
    idspec("STATS_008", TestAction(
        name="invalid data type (str)",
        kwargs={'unit': 'a unit', 'scale': 1.0, 'data': 'not_a_list'},
        exception=SimpleBenchTypeError,
        exception_tag=ErrorTag.STATS_INVALID_DATA_ARG_TYPE)),
    idspec("STATS_009", TestAction(
        name="invalid data value type (list with str)",
        kwargs={'unit': 'a unit', 'scale': 1.0, 'data': [1.0, 'not_a_number', 3.0]},
        exception=SimpleBenchTypeError,
        exception_tag=ErrorTag.STATS_INVALID_DATA_ARG_TYPE)),
    idspec("STATS_010", TestAction(
        name="valid initial values, correctly set",
        kwargs={'unit': 'a unit', 'scale': 1.0, 'data': [1.0, 2.0, 3.0]},
        validate_result=lambda obj: obj.unit == 'a unit' and obj.scale == 1.0 and obj.data == (1.0, 2.0, 3.0))),
])
def test_stats_init(stats_classes: list[type[Stats]], test: TestAction) -> None:
    """Test that the stats module is initialized correctly."""
    for stats_class in stats_classes:
        test.name = f"{test.name} - {stats_class.__name__}"
        test.action = stats_class
        test.run()


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
        case 0:
            assert stats_instance.mean == 0.0, "Mean should be 0.0 for empty data"
            assert stats_instance.median == 0.0, "Median should be 0.0 for empty data"
            assert stats_instance.minimum == 0.0, "Minimum should be 0.0 for empty data"
            assert stats_instance.maximum == 0.0, "Maximum should be 0.0 for empty data"
            assert stats_instance.standard_deviation == 0.0, "Standard deviation should be 0.0 for empty data"
            assert stats_instance.relative_standard_deviation == 0.0, (
                "Relative standard deviation should be 0.0 for empty data")
            assert stats_instance.percentiles == tuple([0.0] * 101), (
                "Percentiles should be all 0.0 for empty data")
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
def test_stats_as_dict(stats_data: Sequence[float | int]) -> None:
    """Test that statistics_as_dict and statistics_and_data_as_dict return correct values."""
    stats_instance = Stats(unit='unit', scale=1.0, data=list(stats_data))
    stats_dict = stats_instance.statistics_as_dict
    stats_and_data_dict = stats_instance.statistics_and_data_as_dict

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
        assert key in stats_dict, f"Key '{key}' missing from statistics_as_dict"
        assert isinstance(stats_dict[key], expected_type), (
            f"Key '{key}' in statistics_as_dict should be of type {expected_type.__name__}, "
            f"got {type(stats_dict[key]).__name__}")

    # Check that the statistics_and_data_as_dict contains the expected keys and types
    expected_keys_with_data = expected_keys.copy()
    expected_keys_with_data['data'] = tuple
    for key, expected_type in expected_keys_with_data.items():
        assert key in stats_and_data_dict, f"Key '{key}' missing from statistics_and_data_as_dict"
        assert isinstance(stats_and_data_dict[key], expected_type), (
            f"Key '{key}' in statistics_and_data_as_dict should be of type {expected_type.__name__}, "
            f"got {type(stats_and_data_dict[key]).__name__}")

    # Check that the data in statistics_and_data_as_dict matches the original data scaled
    scaled_data = tuple(value / stats_instance.scale for value in stats_instance.data)
    assert stats_and_data_dict['data'] == scaled_data, "Data in statistics_and_data_as_dict does not match scaled data"


@pytest.mark.parametrize("section", [
    pytest.param(section, id=f"Section.{section.name}") for section in list(Section) + [Nonsense.NONESENSE]
])
def test_stats_initalization(section: Section) -> None:
    """Test that data is correctly initialized in stats classes."""
    iterations: list[Iteration] = []
    data: dict[str, tuple[int | float, ...]] = {
        'elapsed': (1.0, 2.0, 4.0, 5.0, 10.0),
        'ops': (1.0, 0.5, 0.25, 0.2, 0.1),
        'memory': (100, 200, 300, 400, 500),
        'peak_memory': (150, 250, 350, 450, 550),
    }

    for index in range(len(data['elapsed'])):
        iterations.append(
            Iteration(n=1,
                      unit='s',
                      scale=1.0,
                      elapsed=data['elapsed'][index],
                      memory=int(data['memory'][index]),
                      peak_memory=int(data['peak_memory'][index]))
        )
    stats_instance: Stats
    match section:
        case Section.OPS:
            stats_instance = OperationsPerInterval(unit='ops/s', scale=1.0, iterations=iterations)
            ops_data = stats_instance.data
            assert ops_data == data['ops'], (
                f"Ops data does not match expected values: {ops_data} != {data['ops']}")

        case Section.TIMING:
            stats_instance = OperationTimings(unit='s', scale=1.0, iterations=iterations)
            timing_data = stats_instance.data
            assert timing_data == data['elapsed'], (
                f"Timing data does not match expected values: {timing_data} != {data['elapsed']}")

        case Section.MEMORY:
            stats_instance = MemoryUsage(unit='bytes', scale=1.0, iterations=iterations)
            memory_data = stats_instance.data
            assert memory_data == data['memory'], (
                f"Memory data does not match expected values: {memory_data} != {data['memory']}")

        case Section.PEAK_MEMORY:
            stats_instance = PeakMemoryUsage(unit='bytes', scale=1.0, iterations=iterations)
            peak_memory_data = stats_instance.data
            assert peak_memory_data == data['peak_memory'], (
                f"Peak memory data does not match expected values: {peak_memory_data} != {data['peak_memory']}")

        case _:
            pytest.skip(f"Section {section} does not correspond to a tested stats class")


@pytest.mark.parametrize("testspec", [
    idspec("FROM_DICT_001", TestAction(
        name="Stats - valid input with unit and scale in data",
        action=Stats.from_dict,
        kwargs={
            'unit': 's',
            'scale': 1.0,
            'data': {
                'type': 'Stats:statistics',
                'data': [1.0, 2.0, 3.0],
                'unit': 's',
                'scale': 1.0
            }
        },
        assertion=Assert.ISINSTANCE,
        expected=Stats)),
    idspec("FROM_DICT_001", TestAction(
        name="OperationsPerInterval - valid input with unit and scale in data",
        action=OperationsPerInterval.from_dict,
        kwargs={
            'unit': 'ops/s',
            'scale': 1.0,
            'data': {
                'type': 'OperationsPerInterval:statistics',
                'data': [1.0, 2.0, 3.0],
                'unit': 'ops/s',
                'scale': 1.0
            }
        },
        assertion=Assert.ISINSTANCE,
        expected=OperationsPerInterval)),
])
def test_stats_from_dict(testspec: TestSpec) -> None:
    """Test the from_dict class method of the Stats class and sub-classes."""
    testspec.run()
