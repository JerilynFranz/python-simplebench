"""Tests for the simplebench/stats.py module."""
# Conflicts with pytest fixtures
# pylint: disable=redefined-outer-name
import statistics
from typing import Any, Sequence

import pytest

from simplebench.exceptions import SimpleBenchTypeError, SimpleBenchValueError, ErrorTag
from simplebench import stats

from .testspec import TestAction, TestSetGet, idspec


@pytest.fixture()
def stats_classes() -> list[type[stats.Stats]]:
    """Fixture to return list of stats classes."""
    return [stats.Stats, stats.OperationsPerInterval, stats.OperationTimings]


@pytest.mark.parametrize("test", [
    idspec("STATS_001", TestAction(
        name="minimal args",
        kwargs={'unit': 'a unit', 'scale': 1.0})),
    idspec("STATS_002", TestAction(
        name="all args",
        kwargs={'unit': 'a unit', 'scale': 2.0, 'data': [1.0, 2.0, 3.0]})),
    idspec("STATS_003", TestAction(
        name="invalid unit type (int)",
        kwargs={'unit': 123, 'scale': 1.0},
        exception=SimpleBenchTypeError,
        exception_tag=ErrorTag.STATS_INVALID_UNIT_ARG_TYPE)),
    idspec("STATS_004", TestAction(
        name="invalid unit value (empty str)",
        kwargs={'unit': '', 'scale': 1.0},
        exception=SimpleBenchValueError,
        exception_tag=ErrorTag.STATS_INVALID_UNIT_ARG_VALUE)),
    idspec("STATS_005", TestAction(
        name="invalid scale type (str)",
        kwargs={'unit': 'a unit', 'scale': 'not_a_number'},
        exception=SimpleBenchTypeError,
        exception_tag=ErrorTag.STATS_INVALID_SCALE_ARG_TYPE)),
    idspec("STATS_006", TestAction(
        name="invalid scale value (zero)",
        kwargs={'unit': 'a unit', 'scale': 0},
        exception=SimpleBenchValueError,
        exception_tag=ErrorTag.STATS_INVALID_SCALE_ARG_VALUE)),
    idspec("STATS_007", TestAction(
        name="invalid scale value (negative)",
        kwargs={'unit': 'a unit', 'scale': -1.0},
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
        exception_tag=ErrorTag.STATS_INVALID_DATA_ARG_ITEM_TYPE)),
    idspec("STATS_010", TestAction(
        name="valid initial values, correctly set",
        kwargs={'unit': 'a unit', 'scale': 1.0, 'data': [1.0, 2.0, 3.0]},
        validate_result=lambda obj: obj.unit == 'a unit' and obj.scale == 1.0 and obj.data == [1.0, 2.0, 3.0])),
])
def test_stats_init(stats_classes: list[type[stats.Stats]], test: TestAction) -> None:
    """Test that the stats module is initialized correctly."""
    for stats_class in stats_classes:
        test.name = f"{test.name} - {stats_class.__name__}"
        test.action = stats_class
        test.run()


@pytest.fixture()
def stats_instances() -> list[stats.Stats]:
    """Fixture to return a minimal Stats instance for each class and subclass for testing."""
    return [stats.Stats(unit='unit', scale=1.0),
            stats.OperationsPerInterval(unit='ops/s', scale=1.0),
            stats.OperationTimings(unit='s', scale=1.0)]


@pytest.mark.parametrize("test", [
    idspec("STATS_PROPERTY_001", TestSetGet(
        name="unit property (valid)",
        attribute='unit',
        value='new unit',
        expected='new unit')),
    idspec("STATS_PROPERTY_002", TestSetGet(
        name="unit property (invalid type, int)",
        attribute='unit',
        value=123,
        set_exception=SimpleBenchTypeError,
        set_exception_tag=ErrorTag.STATS_INVALID_UNIT_ARG_TYPE)),
    idspec("STATS_PROPERTY_003", TestSetGet(
        name="unit property (invalid value, empty str)",
        attribute='unit',
        value='',
        set_exception=SimpleBenchValueError,
        set_exception_tag=ErrorTag.STATS_INVALID_UNIT_ARG_VALUE)),
    idspec("STATS_PROPERTY_004", TestSetGet(
        name="scale property (valid)",
        attribute='scale',
        value=2.0,
        expected=2.0)),
    idspec("STATS_PROPERTY_005", TestSetGet(
        name="scale property (invalid type, str)",
        attribute='scale',
        value='not_a_number',
        set_exception=SimpleBenchTypeError,
        set_exception_tag=ErrorTag.STATS_INVALID_SCALE_ARG_TYPE)),
    idspec("STATS_PROPERTY_006", TestSetGet(
        name="scale property (invalid value, zero)",
        attribute='scale',
        value=0,
        set_exception=SimpleBenchValueError,
        set_exception_tag=ErrorTag.STATS_INVALID_SCALE_ARG_VALUE)),
    idspec("STATS_PROPERTY_007", TestSetGet(
        name="scale property (invalid value, negative)",
        attribute='scale',
        value=-1.0,
        set_exception=SimpleBenchValueError,
        set_exception_tag=ErrorTag.STATS_INVALID_SCALE_ARG_VALUE)),
    idspec("STATS_PROPERTY_008", TestSetGet(
        name="data property (valid)",
        attribute='data',
        value=[1.0, 2.0, 3.0],
        expected=[1.0, 2.0, 3.0])),
    idspec("STATS_PROPERTY_009", TestSetGet(
        name="data property (invalid type, str)",
        attribute='data',
        value='not_a_list',
        set_exception=SimpleBenchTypeError,
        set_exception_tag=ErrorTag.STATS_INVALID_DATA_ARG_TYPE)),
    idspec("STATS_PROPERTY_010", TestSetGet(
        name="data property (invalid value type, list with str)",
        attribute='data',
        value=[1.0, 'not_a_number', 3.0],
        set_exception=SimpleBenchTypeError,
        set_exception_tag=ErrorTag.STATS_INVALID_DATA_ARG_ITEM_TYPE)),
    idspec("STATS_PROPERTY_011", TestSetGet(
        name="data property (clear data with None)",
        attribute='data',
        value=None,
        expected=[])),
])
def test_stats_set_get(stats_instances: list[stats.Stats], test: TestSetGet) -> None:
    """Test stats class property setters and getters."""
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
def test_computed_stats_read_only(stats_instances: list[stats.Stats], attribute: str, value: Any) -> None:
    """Test that computed stats properties exist and are read-only."""
    for stats_instance in stats_instances:
        if not hasattr(stats_instance, attribute):
            pytest.fail(f"Attribute {attribute} not found in {type(stats_instance).__name__}")
        with pytest.raises(AttributeError):
            setattr(stats_instance, attribute, value)


@pytest.mark.parametrize("stats_data", [
    pytest.param([], id="COMPUTED_VALUES_001 empty data"),
    pytest.param([10.0], id="COMPUTED_VALUES_002 single data point"),
    pytest.param([10.0, 20.0, 30.0, 40.0, 50.0], id="COMPUTED_VALUES_003 multiple data points"),
    pytest.param([5.0, 15.0, 25.0, 35.0, 45.0, 55.0, 65.0, 75.0, 85.0, 95.0], id="COMPUTED_VALUES_004 larger data set"),
    pytest.param([3.0, 3.0, 3.0, 3.0, 3.0], id="COMPUTED_VALUES_005 identical data points"),
])
def test_computed_stats_values(stats_data: Sequence[float | int]) -> None:
    """Test that computed stats properties return correct values.
    """
    stats_instance = stats.Stats(unit='unit', scale=1.0, data=list(stats_data))
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
            assert stats_instance.percentiles == {5: 0.0, 10: 0.0, 25: 0.0, 50: 0.0, 75: 0.0, 90: 0.0, 95: 0.0}, (
                "Percentiles should be 0.0 for empty data")
        case 1:
            assert stats_instance.mean == 10.0, "Mean should be 10.0 for single data point"
            assert stats_instance.median == 10.0, "Median should be 10.0 for single data point"
            assert stats_instance.minimum == 10.0, "Minimum should be 10.0 for single data point"
            assert stats_instance.maximum == 10.0, "Maximum should be 10.0 for single data point"
            assert stats_instance.standard_deviation == 0.0, "Standard deviation should be 0.0 for single data point"
            assert stats_instance.relative_standard_deviation == 0.0, (
                "Relative standard deviation should be 0.0 for single data point")
            assert stats_instance.percentiles == {
                5: 10.0, 10: 10.0, 25: 10.0, 50: 10.0, 75: 10.0, 90: 10.0, 95: 10.0}, (
                "Percentiles should be 10.0 for single data point")
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
            percentiles = {p: statistics.quantiles(data, n=100)[p - 1] for p in [5, 10, 25, 50, 75, 90, 95]}
            assert stats_instance.percentiles == percentiles, (
                f"Percentiles value incorrect: expected {percentiles}, got {stats_instance.percentiles}")


@pytest.mark.parametrize("stats_data", [
    pytest.param([], id="COMPUTED_VALUES_001 empty data"),
    pytest.param([10.0], id="COMPUTED_VALUES_002 single data point"),
    pytest.param([10.0, 20.0, 30.0, 40.0, 50.0], id="COMPUTED_VALUES_003 multiple data points"),
    pytest.param([5.0, 15.0, 25.0, 35.0, 45.0, 55.0, 65.0, 75.0, 85.0, 95.0], id="COMPUTED_VALUES_004 larger data set"),
    pytest.param([3.0, 3.0, 3.0, 3.0, 3.0], id="COMPUTED_VALUES_005 identical data points"),
])
def test_stats_as_dict(stats_data: Sequence[float | int]) -> None:
    """Test that statistics_as_dict and statistics_and_data_as_dict return correct values."""
    stats_instance = stats.Stats(unit='unit', scale=1.0, data=list(stats_data))
    stats_dict = stats_instance.statistics_as_dict
    stats_and_data_dict = stats_instance.statistics_and_data_as_dict

    # Check that the statistics_as_dict contains the expected keys and types
    expected_keys = {
        'type': str,
        'unit': str,
        'scale': float,
        'mean': float,
        'median': float,
        'minimum': float,
        'maximum': float,
        'standard_deviation': float,
        'relative_standard_deviation': float,
        'percentiles': dict,
    }
    for key, expected_type in expected_keys.items():
        assert key in stats_dict, f"Key '{key}' missing from statistics_as_dict"
        assert isinstance(stats_dict[key], expected_type), (
            f"Key '{key}' in statistics_as_dict should be of type {expected_type.__name__}, "
            f"got {type(stats_dict[key]).__name__}")

    # Check that the statistics_and_data_as_dict contains the expected keys and types
    expected_keys_with_data = expected_keys.copy()
    expected_keys_with_data['data'] = list
    for key, expected_type in expected_keys_with_data.items():
        assert key in stats_and_data_dict, f"Key '{key}' missing from statistics_and_data_as_dict"
        assert isinstance(stats_and_data_dict[key], expected_type), (
            f"Key '{key}' in statistics_and_data_as_dict should be of type {expected_type.__name__}, "
            f"got {type(stats_and_data_dict[key]).__name__}")

    # Check that the data in statistics_and_data_as_dict matches the original data scaled
    scaled_data = [value / stats_instance.scale for value in stats_instance.data]
    assert stats_and_data_dict['data'] == scaled_data, "Data in statistics_and_data_as_dict does not match scaled data"
