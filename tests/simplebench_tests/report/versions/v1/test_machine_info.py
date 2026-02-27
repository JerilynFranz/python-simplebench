"""Tests for MachineInfo() report for SimpleBench tests."""
import json
import pickle
from copy import copy, deepcopy
from typing import TypeAlias

import pytest
import simplejson
from jsonschema import Draft202012Validator
from referencing import Registry, Resource
from testspec import Assert, PytestAction, TestSpec

from simplebench.exceptions import SimpleBenchTypeError, SimpleBenchValueError
from simplebench.report._error_tags import _MachineInfoErrorTag
from simplebench.report.versions import v1 as report
from simplebench.simplebench_types import CoreDataMapping, CoreDataSequence, is_immutable  # noqa: F401
from simplebench.validators import is_typed_dict_mimic
from simplebench_tests.factories.report import v1 as report_factories

# Needed for repl evaluation of __repr__ string in test_repr
MachineInfo: TypeAlias = report.MachineInfo
CPUInfo: TypeAlias = report.CPUInfo
MemoryInfo: TypeAlias = report.MemoryInfo
SwapMemoryObject: TypeAlias = report.SwapMemoryObject
VirtualMemoryObject: TypeAlias = report.VirtualMemoryObject
SystemInfo: TypeAlias = report.SystemInfo
EnvironmentInfo: TypeAlias = report.EnvironmentInfo
PythonInfo: TypeAlias = report.PythonInfo


# JSON Schema Registry setup for validating JSON schema in tests
registry = Registry().with_resources([
    (report.CPUInfo.SCHEMA.ID, Resource.from_contents(report.CPUInfo.SCHEMA.as_dict())),
    (report.MemoryInfo.SCHEMA.ID, Resource.from_contents(report.MemoryInfo.SCHEMA.as_dict())),
    (report.EnvironmentInfo.SCHEMA.ID, Resource.from_contents(report.EnvironmentInfo.SCHEMA.as_dict())),
    (report.PythonInfo.SCHEMA.ID, Resource.from_contents(report.PythonInfo.SCHEMA.as_dict())),
    (report.SystemInfo.SCHEMA.ID, Resource.from_contents(report.SystemInfo.SCHEMA.as_dict())),
])

validator = Draft202012Validator(schema=report.MachineInfo.SCHEMA.as_dict(), registry=registry)


@pytest.mark.parametrize("testspec", [
    PytestAction("INIT_001",
        name="All fields provided",
        action=report.MachineInfo,
        kwargs=report_factories.machine_info_kwargs(),
        assertion=Assert.ISINSTANCE,
        expected=report.MachineInfo),
    PytestAction("INIT_002",
        name="Only required fields provided (hash_id and node are optional)",
        action=report.MachineInfo,
        kwargs=report_factories.machine_info_kwargs() - {'hash_id', 'node'},  # Remove optional fields
        assertion=Assert.ISINSTANCE,
        expected=report.MachineInfo),
    PytestAction("INIT_003",
        name="Wrong type for field (hash_id as int)",
        action=report.MachineInfo,
        kwargs=report_factories.machine_info_kwargs().replace(hash_id=123),
        exception=SimpleBenchTypeError,
        exception_tag=_MachineInfoErrorTag.INVALID_HASH_ID_PROPERTY_TYPE),
    PytestAction("INIT_004",
        name="Invalid hash_id value (not 64 hex chars)",
        action=report.MachineInfo,
        kwargs=report_factories.machine_info_kwargs().replace(hash_id='invalid_hash'),
        exception=SimpleBenchValueError,
        exception_tag=_MachineInfoErrorTag.INVALID_HASH_ID_PROPERTY_VALUE),
    PytestAction("INIT_005",
        name="Empty string for optional hash_id field",
        action=report.MachineInfo,
        kwargs=report_factories.machine_info_kwargs().replace(hash_id=''),
        assertion=Assert.ISINSTANCE,
        expected=report.MachineInfo),
])
def test_init(testspec: TestSpec) -> None:
    testspec.run()


@pytest.mark.parametrize("testspec", [
    PytestAction("PROP_001",
        name="hash_id property set correctly",
        action=report.MachineInfo,
        kwargs=report_factories.machine_info_kwargs(),
        validate_attr='hash_id',
        expected=report_factories.machine_info_kwargs()['hash_id']),
])
def test_properties(testspec: TestSpec) -> None:
    testspec.run()


@pytest.mark.parametrize(
      "testspec", [
         PytestAction("HASH_ID_001",
            name="Test valid hash_id value through from_dict",
            action=report.MachineInfo.from_dict,
            args=[report_factories.machine_info_data()],
            validate_attr="hash_id",
            expected=report_factories.machine_info_kwargs()["hash_id"]),  # type: ignore[index]
         PytestAction("HASH_ID_002",
            name="Test generated hash_id when not provided through from_dict",
            action=report.MachineInfo.from_dict,
            args=[report_factories.no_hash_id_machine_info_data()],
            validate_attr="hash_id",
            assertion=Assert.NOT_EQUAL,
            expected=report_factories.machine_info_kwargs()["hash_id"]),
])
def test_hash_id(testspec: TestSpec) -> None:
    """Test MachineInfo hash_id property."""
    testspec.run()


@pytest.mark.parametrize('testspec', [
    PytestAction('TO_DICT_001',
        name='MachineInfo to_dict returns a report.MachineInfoDict TypedDict mimic',
        action=lambda: is_typed_dict_mimic(report_factories.machine_info().to_dict(), report.MachineInfoDict),
        assertion=Assert.TRUE
    ),
    PytestAction('TO_DICT_002',
        name='MachineInfo to_dict returns a report.ImmutableMachineInfoDict TypedDict mimic',
        action=lambda: is_typed_dict_mimic(report_factories.machine_info().to_dict(), report.ImmutableMachineInfoDict),
        assertion=Assert.TRUE
    ),
])
def test_to_dict(testspec: TestSpec) -> None:
    """Test MachineInfo to_dict method."""
    testspec.run()


@pytest.mark.parametrize('testspec', [
    PytestAction('EQUALITY_001',
        name='MachineInfo equality comparison with identical hash_id values',
        action=lambda: report.MachineInfo(**report_factories.machine_info_kwargs()),
        assertion=Assert.EQUAL,
        expected=report.MachineInfo(**report_factories.machine_info_kwargs())
    ),
    PytestAction('EQUALITY_002',
        name='MachineInfo equality comparison with different hash_id values',
        action=lambda: report.MachineInfo(**report_factories.machine_info_kwargs()),
        assertion=Assert.NOT_EQUAL,
        expected=report.MachineInfo(**report_factories.machine_info_kwargs().replace(hash_id='d' * 64))
    ),
    PytestAction('EQUALITY_004',
        name='MachineInfo equality comparison with same values and calculated hash_id (hash_id not provided)',
        action=lambda: report.MachineInfo(**report_factories.machine_info_kwargs() - {'hash_id'}),
        assertion=Assert.EQUAL,
        expected=report.MachineInfo(**report_factories.machine_info_kwargs() - {'hash_id'})
    ),
    PytestAction('EQUALITY_005',
        name='MachineInfo equality comparison with different types (not a MachineInfo instance)',
        action=lambda: report.MachineInfo(**report_factories.machine_info_kwargs()),
        assertion=Assert.NOT_EQUAL,
        expected="Not a MachineInfo instance"
    ),
])
def test_equality(testspec: TestSpec) -> None:
    """Test MachineInfo equality comparison."""
    testspec.run()


def test_repr() -> None:
    """Test MachineInfo __repr__ method."""
    info = report_factories.machine_info()
    repr_str = repr(info)
    try:
        assert eval(repr_str) == info, (
            f"REPR_001 Evaluating __repr__ string did not produce the original object: {repr_str!r}")
    except Exception as e:
        raise AssertionError(
            f"REPR_001 Evaluating __repr__ string raised an exception: {e}\n"
            f"__repr__ string: {repr_str!r}"
        ) from e


@pytest.mark.parametrize('testspec', [
    PytestAction('HASH_001',
        name='MachineInfo instances with identical hash_id values have the same hash',
        action=hash,
        args=[report.MachineInfo(**report_factories.machine_info_kwargs())],
        assertion=Assert.EQUAL,
        expected=hash(report.MachineInfo(**report_factories.machine_info_kwargs()))
    ),
    PytestAction('HASH_002',
        name='MachineInfo instances with different values have different hashes',
        action=hash,
        args=[report.MachineInfo(**report_factories.machine_info_kwargs() - {'hash_id'})],
        assertion=Assert.NOT_EQUAL,
        expected=hash(report.MachineInfo(
            **report_factories.machine_info_kwargs().replace(node='other')- {'hash_id'}))
    ),
])
def test_hash(testspec: TestSpec) -> None:
    """Test MachineInfo __hash__ method."""
    testspec.run()


@pytest.mark.parametrize('testspec', [
    PytestAction('PICKLE_001',
        name='MachineInfo instance can be pickled and unpickled correctly',
        action=lambda: pickle.loads(pickle.dumps(report_factories.machine_info())),
        assertion=Assert.EQUAL,
        expected=report_factories.machine_info()
    ),
])
def test_pickling(testspec: TestSpec) -> None:
    """Test that MachineInfo instances can be pickled and unpickled correctly."""
    testspec.run()


@pytest.mark.parametrize('testspec', [
    PytestAction('IMMUTABILITY_001',
        name='MachineInfo instance is immutable (attempting to set an attribute raises an exception)',
        action=lambda: setattr(report_factories.machine_info(), 'node', 'other'),
        exception=AttributeError
    ),
    PytestAction('IMMUTABILITY_002',
        name='MachineInfo instance is immutable (is_immutable returns True)',
        action=lambda: is_immutable(report_factories.machine_info()),
        assertion=Assert.TRUE
    ),
])
def test_immutability(testspec: TestSpec) -> None:
    """Test that MachineInfo instances are immutable."""
    testspec.run()


@pytest.mark.parametrize('testspec', [
    PytestAction('SCHEMA_001',
        name='MachineInfo JSON schema is valid and can validate to_dict() output',
        action=validator.validate,
        args=[report_factories.machine_info().to_dict().thaw()],  # type: ignore
    ),
])
def test_json_schema(testspec: TestSpec) -> None:
    """Test that the JSON schema for MachineInfo is valid and can be
    used to validate a MachineInfo instance's to_dict() output."""
    testspec.run()

@pytest.mark.parametrize('testspec', [
     PytestAction('JSON_SERIALIZATION_001',
         name='MachineInfo can be serialized to JSON',
         action=report_factories.machine_info().as_json,
         assertion=Assert.ISINSTANCE,
         expected=str),
    PytestAction('JSON_SERIALIZATION_002',
        name='MachineInfo can be directly serialized to a JSON compatible dictionary by simplejson',
        action=simplejson.dumps,
        kwargs={"obj": report_factories.machine_info(),
                "sort_keys": True, "for_json": True, "iterable_as_array": True},
        assertion=Assert.ISINSTANCE,
        expected=str),
    PytestAction('JSON_SERIALIZATION_003',
            name='MachineInfo.for_json() can serialized to a JSON string by json.dumps',
            action=json.dumps,
            kwargs={"obj": report_factories.machine_info().for_json(), "sort_keys": True},
            assertion=Assert.ISINSTANCE,
            expected=str),
 ])
def test_json_serialization(testspec: TestSpec) -> None:
    """Test that MachineInfo can be serialized to JSON."""
    testspec.run()

@pytest.mark.parametrize('testspec', [
    PytestAction('COPY_001',
        name='Copying a MachineInfo instance returns the same instance (since it is immutable)',
        action=copy,
        args=[report_factories.machine_info()],
        assertion=Assert.IS,
        expected=report_factories.machine_info()
    ),
    PytestAction('DEEP_COPY_001',
        name='Deep copying a MachineInfo instance returns the same instance (since it is immutable)',
        action=deepcopy,
        args=[report_factories.machine_info()],
        assertion=Assert.IS,
        expected=report_factories.machine_info()
    ),
])
def test_copy(testspec: TestSpec) -> None:
    """Test that copying a MachineInfo instance returns the same instance (since it is immutable)."""
    testspec.run()

if __name__ == "__main__":
    pytest.main([__file__])
