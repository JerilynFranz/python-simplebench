"""Tests for Report() report for SimpleBench tests."""
import json
import pickle
from copy import copy, deepcopy
from typing import TypeAlias

import pytest
import simplejson
from jsonschema import Draft202012Validator
from referencing import Registry, Resource
from testspec import Assert, PytestAction, TestSpec

from simplebench._log import _log
from simplebench.exceptions import SimpleBenchTypeError, SimpleBenchValueError
from simplebench.report._error_tags import _ReportErrorTag
from simplebench.report.versions import v1 as report
from simplebench.simplebench_types import CoreDataMapping, CoreDataSequence, VariationCols, is_immutable  # noqa: F401
from simplebench.validators import is_typed_dict_mimic
from simplebench_tests.factories.report import v1 as report_factories

# Needed for repl evaluation of __repr__ string in test_repr
Report: TypeAlias = report.Report
CPUInfo: TypeAlias = report.CPUInfo
MemoryInfo: TypeAlias = report.MemoryInfo
SwapMemoryObject: TypeAlias = report.SwapMemoryObject
VirtualMemoryObject: TypeAlias = report.VirtualMemoryObject
SystemInfo: TypeAlias = report.SystemInfo
EnvironmentInfo: TypeAlias = report.EnvironmentInfo
PythonInfo: TypeAlias = report.PythonInfo
ResultsInfo: TypeAlias = report.ResultsInfo
StatsBlock: TypeAlias = report.StatsBlock
ValueBlock: TypeAlias = report.ValueBlock
RawDataBlock: TypeAlias = report.RawDataBlock
VCSInfo: TypeAlias = report.VCSInfo
MachineInfo: TypeAlias = report.MachineInfo
MetricsObject: TypeAlias = report.MetricsObject
ExtrasObject: TypeAlias = report.ExtrasObject


# JSON Schema Registry setup for validating JSON schema in tests
registry = Registry().with_resources([
    (report.CPUInfo.SCHEMA.ID, Resource.from_contents(report.CPUInfo.SCHEMA.as_dict())),
    (report.MemoryInfo.SCHEMA.ID, Resource.from_contents(report.MemoryInfo.SCHEMA.as_dict())),
    (report.EnvironmentInfo.SCHEMA.ID, Resource.from_contents(report.EnvironmentInfo.SCHEMA.as_dict())),
    (report.PythonInfo.SCHEMA.ID, Resource.from_contents(report.PythonInfo.SCHEMA.as_dict())),
    (report.SystemInfo.SCHEMA.ID, Resource.from_contents(report.SystemInfo.SCHEMA.as_dict())),
    (report.MachineInfo.SCHEMA.ID, Resource.from_contents(report.MachineInfo.SCHEMA.as_dict())),
    (report.ResultsInfo.SCHEMA.ID, Resource.from_contents(report.ResultsInfo.SCHEMA.as_dict())),
    (report.StatsBlock.SCHEMA.ID, Resource.from_contents(report.StatsBlock.SCHEMA.as_dict())),
    (report.ValueBlock.SCHEMA.ID, Resource.from_contents(report.ValueBlock.SCHEMA.as_dict())),
    (report.RawDataBlock.SCHEMA.ID, Resource.from_contents(report.RawDataBlock.SCHEMA.as_dict())),
    (report.VCSInfo.SCHEMA.ID, Resource.from_contents(report.VCSInfo.SCHEMA.as_dict())),
])

validator = Draft202012Validator(schema=report.Report.SCHEMA.as_dict(), registry=registry)


@pytest.mark.parametrize("testspec", [
    PytestAction("INIT_001",
        name="All fields provided",
        action=report.Report,
        kwargs=report_factories.report_kwargs(),
        assertion=Assert.ISINSTANCE,
        expected=report.Report),
    PytestAction("INIT_002",
        name="Only required fields provided (hash_id is optional)",
        action=report.Report,
        kwargs=report_factories.report_kwargs() - {'hash_id'},  # Remove optional fields
        assertion=Assert.ISINSTANCE,
        expected=report.Report),
    PytestAction("INIT_003",
        name="Wrong type for field (hash_id as int)",
        action=report.Report,
        kwargs=report_factories.report_kwargs().replace(hash_id=123),
        exception=SimpleBenchTypeError,
        exception_tag=_ReportErrorTag.INVALID_HASH_ID_TYPE),
    PytestAction("INIT_004",
        name="Invalid hash_id value (not 64 hex chars)",
        action=report.Report,
        kwargs=report_factories.report_kwargs().replace(hash_id='invalid_hash'),
        exception=SimpleBenchValueError,
        exception_tag=_ReportErrorTag.INVALID_HASH_ID_VALUE),
    PytestAction("INIT_005",
        name="Empty string for optional hash_id field",
        action=report.Report,
        kwargs=report_factories.report_kwargs().replace(hash_id=''),
        assertion=Assert.ISINSTANCE,
        expected=report.Report),
])
def test_init(testspec: TestSpec) -> None:
    testspec.run()


@pytest.mark.parametrize("testspec", [
    PytestAction("PROP_001",
        name="hash_id property set correctly",
        action=report.Report,
        kwargs=report_factories.report_kwargs(),
        validate_attr='hash_id',
        expected=report_factories.report_kwargs()['hash_id']),
])
def test_properties(testspec: TestSpec) -> None:
    testspec.run()


@pytest.mark.parametrize(
      "testspec", [
         PytestAction("HASH_ID_001",
            name="Test valid hash_id value through from_dict",
            action=report.Report.from_dict,
            args=[report_factories.report_data()],
            validate_attr="hash_id",
            expected=report_factories.report_kwargs()["hash_id"]),  # type: ignore[index]
         PytestAction("HASH_ID_002",
            name="Test generated hash_id when not provided through from_dict",
            action=report.Report.from_dict,
            args=[report_factories.no_hash_id_report_data()],
            validate_attr="hash_id",
            assertion=Assert.NOT_EQUAL,
            expected=report_factories.report_kwargs()["hash_id"]),
])
def test_hash_id(testspec: TestSpec) -> None:
    """Test Report hash_id property."""
    testspec.run()


@pytest.mark.parametrize('testspec', [
    PytestAction('FROM_DICT_001',
        name='Report from_dict creates a Report instance from valid dictionary data',
        action=report.Report.from_dict,
        args=[report_factories.report_data()],
        assertion=Assert.ISINSTANCE,
        expected=report.Report
    ),
    PytestAction('FROM_DICT_002',
        name='Round-Trip test: Report from_dict with to_dict output returns an equal Report instance',
        action=report.Report.from_dict,
        args=[report_factories.report().to_dict().thaw()],  # type: ignore
        assertion=Assert.EQUAL,
        expected=report_factories.report()
    ),
])
def test_from_dict(testspec: TestSpec) -> None:
    """Test Report from_dict method."""
    testspec.run()

@pytest.mark.parametrize('testspec', [
    PytestAction('TO_DICT_001',
        name='Report to_dict returns a report.ReportDict TypedDict mimic',
        action=lambda: is_typed_dict_mimic(report_factories.report().to_dict(), report.ReportDict),
        assertion=Assert.TRUE
    ),
    PytestAction('TO_DICT_002',
        name='Report to_dict returns a report.ImmutableReportDict TypedDict mimic',
        action=lambda: is_typed_dict_mimic(report_factories.report().to_dict(), report.ImmutableReportDict),
        assertion=Assert.TRUE
    ),
])
def test_to_dict(testspec: TestSpec) -> None:
    """Test Report to_dict method."""
    testspec.run()


@pytest.mark.parametrize('testspec', [
    PytestAction('EQUALITY_001',
        name='Report equality comparison with identical hash_id values',
        action=lambda: report.Report(**report_factories.report_kwargs()),
        assertion=Assert.EQUAL,
        expected=report.Report(**report_factories.report_kwargs())
    ),
    PytestAction('EQUALITY_002',
        name='Report equality comparison with different hash_id values',
        action=lambda: report.Report(**report_factories.report_kwargs()),
        assertion=Assert.NOT_EQUAL,
        expected=report.Report(**report_factories.report_kwargs().replace(hash_id='d' * 64))
    ),
    PytestAction('EQUALITY_004',
        name='Report equality comparison with same values and calculated hash_id (hash_id not provided)',
        action=lambda: report.Report(**report_factories.report_kwargs() - {'hash_id'}),
        assertion=Assert.EQUAL,
        expected=report.Report(**report_factories.report_kwargs() - {'hash_id'})
    ),
    PytestAction('EQUALITY_005',
        name='Report equality comparison with different types (not a Report instance)',
        action=lambda: report.Report(**report_factories.report_kwargs()),
        assertion=Assert.NOT_EQUAL,
        expected="Not a Report instance"
    ),
])
def test_equality(testspec: TestSpec) -> None:
    """Test Report equality comparison."""
    testspec.run()


def test_repr() -> None:
    """Test Report __repr__ method."""
    info = report_factories.report()
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
        name='Report instances with identical hash_id values have the same hash',
        action=hash,
        args=[report.Report(**report_factories.report_kwargs())],
        assertion=Assert.EQUAL,
        expected=hash(report.Report(**report_factories.report_kwargs()))
    ),
    PytestAction('HASH_002',
        name='Report instances with different values have different hashes',
        action=hash,
        args=[report.Report(**report_factories.report_kwargs() - {'hash_id'})],
        assertion=Assert.NOT_EQUAL,
        expected=hash(report.Report(
            **report_factories.report_kwargs().replace(description='other')- {'hash_id'}))
    ),
])
def test_hash(testspec: TestSpec) -> None:
    """Test Report __hash__ method."""
    testspec.run()


@pytest.mark.parametrize('testspec', [
    PytestAction('PICKLE_001',
        name='Report instance can be pickled and unpickled correctly',
        action=lambda: pickle.loads(pickle.dumps(report_factories.report())),
        assertion=Assert.EQUAL,
        expected=report_factories.report()
    ),
])
def test_pickling(testspec: TestSpec) -> None:
    """Test that Report instances can be pickled and unpickled correctly."""
    testspec.run()


@pytest.mark.parametrize('testspec', [
    PytestAction('IMMUTABILITY_001',
        name='Report instance is immutable (attempting to set an attribute raises an exception)',
        action=lambda: setattr(report_factories.report(), 'description', 'other'),
        exception=AttributeError
    ),
    PytestAction('IMMUTABILITY_002',
        name='Report instance is immutable (is_immutable returns True)',
        action=lambda: is_immutable(report_factories.report()),
        assertion=Assert.TRUE
    ),
])
def test_immutability(testspec: TestSpec) -> None:
    """Test that Report instances are immutable."""
    testspec.run()


@pytest.mark.parametrize('testspec', [
    PytestAction('SCHEMA_001',
        name='Report JSON schema is valid and can validate to_dict() output',
        action=validator.validate,
        args=[report_factories.report().to_dict().thaw()]  # type: ignore
    ),
])
def test_json_schema(testspec: TestSpec) -> None:
    """Test that the JSON schema for Report is valid and can be
    used to validate a Report instance's to_dict() output."""
    _log.setLevel('DEBUG')
    testspec.run()
    _log.setLevel('INFO')

@pytest.mark.parametrize('testspec', [
     PytestAction('JSON_SERIALIZATION_001',
         name='Report can be serialized to JSON',
         action=report_factories.report().as_json,
         assertion=Assert.ISINSTANCE,
         expected=str),
    PytestAction('JSON_SERIALIZATION_002',
        name='Report can be directly serialized to a JSON compatible dictionary by simplejson',
        action=simplejson.dumps,
        kwargs={"obj": report_factories.report(),
                "sort_keys": True, "for_json": True, "iterable_as_array": True},
        assertion=Assert.ISINSTANCE,
        expected=str),
    PytestAction('JSON_SERIALIZATION_003',
            name='Report.for_json() can serialized to a JSON string by json.dumps',
            action=json.dumps,
            kwargs={"obj": report_factories.report().for_json(), "sort_keys": True},
            assertion=Assert.ISINSTANCE,
            expected=str),
 ])
def test_json_serialization(testspec: TestSpec) -> None:
    """Test that Report can be serialized to JSON."""
    testspec.run()

@pytest.mark.parametrize('testspec', [
    PytestAction('COPY_001',
        name='Copying a Report instance returns the same instance (since it is immutable)',
        action=copy,
        args=[report_factories.report()],
        assertion=Assert.IS,
        expected=report_factories.report()
    ),
    PytestAction('DEEP_COPY_001',
        name='Deep copying a Report instance returns the same instance (since it is immutable)',
        action=deepcopy,
        args=[report_factories.report()],
        assertion=Assert.IS,
        expected=report_factories.report()
    ),
])
def test_copy(testspec: TestSpec) -> None:
    """Test that copying a Report instance returns the same instance (since it is immutable)."""
    testspec.run()

if __name__ == "__main__":
    pytest.main([__file__])
