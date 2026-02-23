"""Tests for the ExtrasObject class in the simplebench report versions v1."""
import pytest
from testspec import Assert, PytestAction, TestSpec

from simplebench.exceptions import SimpleBenchTypeError
from simplebench.simplebench_types import CoreDataMapping, CoreDataTypes
from simplebench.report.versions.v1 import ExtrasObject


@pytest.mark.parametrize("testspec", [
    PytestAction("INIT_001",
        name="valid initialization",
        action=ExtrasObject,
        args=[{'key1': 'value1', 'key2': 123}],
        assertion=Assert.ISINSTANCE,
        expected=ExtrasObject),
    PytestAction("INIT_002",
        name="initialization with empty dict",
        action=ExtrasObject,
        args=[{}],
        assertion=Assert.ISINSTANCE,
        expected=ExtrasObject),
    PytestAction("INIT_003",
        name="initialization with non-string key",
        action=ExtrasObject,
        args=[{123: 'value'}],
        exception=SimpleBenchTypeError),
    PytestAction("INIT_004",
        name="initialization with non-CoreDataTypes value",
        action=ExtrasObject,
        args=[{'key': object()}],
        exception=SimpleBenchTypeError)
    ],
)
def test_init(testspec: TestSpec) -> None:
    """Test that the ExtrasObject can be initialized with valid data."""
    testspec.run()


@pytest.mark.parametrize("testspec", [
    PytestAction("TO_DICT_001",
        name="to_dict returns correct dictionary",
        action=ExtrasObject({'key1': 'value1', 'key2': 123}).to_dict,
        assertion=Assert.EQUAL,
        expected=CoreDataMapping({'key1': 'value1', 'key2': 123})),
    PytestAction("TO_DICT_002",
        name="to_dict with empty extras",
        action=ExtrasObject({}).to_dict,
        assertion=Assert.EQUAL,
        expected=CoreDataMapping({}))
    ],
)
def test_to_dict(testspec: TestSpec) -> None:
    """Test that the to_dict method returns the correct dictionary representation."""
    testspec.run()


@pytest.mark.parametrize("testspec", [
    PytestAction("FROM_DICT_001",
        name="from_dict creates correct ExtrasObject",
        action=ExtrasObject.from_dict,
        args=[{'key1': 'value1', 'key2': 123}],
        assertion=Assert.EQUAL,
        expected=ExtrasObject({'key1': 'value1', 'key2': 123})),
    PytestAction("FROM_DICT_002",
        name="from_dict with empty dictionary",
        action=ExtrasObject.from_dict,
        args=[{}],
        assertion=Assert.EQUAL,
        expected=ExtrasObject({}))
    ],
)
def test_from_dict(testspec: TestSpec) -> None:
    """Test that the from_dict class method creates an ExtrasObject instance from a dictionary."""
    testspec.run()


if __name__ == "__main__":
    pytest.main([__file__])
