"""Tests for the simplebench/stats.py module."""
# Conflicts with pytest fixtures
# pylint: disable=redefined-outer-name
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
])
def test_stats_set_get(stats_instances: list[stats.Stats], test: TestSetGet) -> None:
    """Test stats class property setters and getters."""
    for stats_instance in stats_instances:
        test.name = f"{test.name} ({type(stats_instance).__name__})"
        test.obj = stats_instance
        test.run()
