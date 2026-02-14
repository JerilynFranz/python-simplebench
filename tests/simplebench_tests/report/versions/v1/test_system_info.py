"""Tests for SystemInfo() report for SimpleBench tests."""
import json
import pickle
from copy import copy, deepcopy
from typing import TypeAlias

import pytest
import simplejson
from jsonschema import validate
from testspec import Assert, PytestAction, TestSpec

from simplebench.exceptions import SimpleBenchTypeError, SimpleBenchValueError
from simplebench.report._error_tags import _SystemInfoErrorTag
from simplebench.report.versions import v1 as report
from simplebench.simplebench_types import is_immutable
from simplebench.validators import is_typed_dict_mimic
from simplebench_tests.factories.report import v1 as report_factories

SystemInfo: TypeAlias = report.SystemInfo

@pytest.mark.parametrize("testspec", [
    PytestAction("INIT_001",
        name="All fields provided",
        action=report.SystemInfo,
        kwargs=report_factories.system_info_kwargs(),
        assertion=Assert.ISINSTANCE,
        expected=report.SystemInfo),
    PytestAction("INIT_002",
        name="Only required fields provided (hash_id is optional)",
        action=report.SystemInfo,
        kwargs=report_factories.system_info_kwargs() - {'hash_id'},
        assertion=Assert.ISINSTANCE,
        expected=report.SystemInfo),
    PytestAction("INIT_003",
        name="Wrong type for field (hash_id as int)",
        action=report.SystemInfo,
        kwargs=report_factories.system_info_kwargs().replace(hash_id=123),
        exception=SimpleBenchTypeError,
        exception_tag=_SystemInfoErrorTag.INVALID_HASH_ID_TYPE),
    PytestAction("INIT_004",
        name="Invalid hash_id value (not 64 hex chars)",
        action=report.SystemInfo,
        kwargs=report_factories.system_info_kwargs().replace(hash_id='invalid_hash'),
        exception=SimpleBenchValueError,
        exception_tag=_SystemInfoErrorTag.INVALID_HASH_ID_VALUE),
    PytestAction("INIT_005",
        name="Empty string for optional hash_id field",
        action=report.SystemInfo,
        kwargs=report_factories.system_info_kwargs().replace(hash_id=''),
        assertion=Assert.ISINSTANCE,
        expected=report.SystemInfo),
    PytestAction("INIT_006",
        name="Missing required field (system)",
        action=report.SystemInfo,
        kwargs=report_factories.system_info_kwargs() - {'system'},
        exception=TypeError),
    PytestAction("INIT_007",
        name="Wrong type for required field (system as int)",
        action=report.SystemInfo,
        kwargs=report_factories.system_info_kwargs().replace(system=123),
        exception=SimpleBenchTypeError,
        exception_tag=_SystemInfoErrorTag.INVALID_SYSTEM_TYPE),
    PytestAction("INIT_008",
        name="Empty string for required field (system)",
        action=report.SystemInfo,
        kwargs=report_factories.system_info_kwargs().replace(system=''),
        exception=SimpleBenchValueError,
        exception_tag=_SystemInfoErrorTag.EMPTY_SYSTEM_VALUE),
    PytestAction("INIT_009",
        name="Wrong type for required field (system_version as int)",
        action=report.SystemInfo,
        kwargs=report_factories.system_info_kwargs().replace(system_version=123),
        exception=SimpleBenchTypeError,
        exception_tag=_SystemInfoErrorTag.INVALID_SYSTEM_VERSION_TYPE),
    PytestAction("INIT_010",
        name="Empty string for required field (system_version)",
        action=report.SystemInfo,
        kwargs=report_factories.system_info_kwargs().replace(system_version=''),
        exception=SimpleBenchValueError,
        exception_tag=_SystemInfoErrorTag.EMPTY_SYSTEM_VERSION_VALUE),
    PytestAction("INIT_011",
        name="Wrong type for required field (release as int)",
        action=report.SystemInfo,
        kwargs=report_factories.system_info_kwargs().replace(release=123),
        exception=SimpleBenchTypeError,
        exception_tag=_SystemInfoErrorTag.INVALID_RELEASE_TYPE),
    PytestAction("INIT_012",
        name="Empty string for required field (release)",
        action=report.SystemInfo,
        kwargs=report_factories.system_info_kwargs().replace(release=''),
        exception=SimpleBenchValueError,
        exception_tag=_SystemInfoErrorTag.EMPTY_RELEASE_VALUE),
    PytestAction("INIT_013",
        name="Wrong type for required field (machine as int)",
        action=report.SystemInfo,
        kwargs=report_factories.system_info_kwargs().replace(machine=123),
        exception=SimpleBenchTypeError,
        exception_tag=_SystemInfoErrorTag.INVALID_MACHINE_TYPE),
    PytestAction("INIT_014",
        name="Empty string for required field (machine)",
        action=report.SystemInfo,
        kwargs=report_factories.system_info_kwargs().replace(machine=''),
        exception=SimpleBenchValueError,
        exception_tag=_SystemInfoErrorTag.EMPTY_MACHINE_VALUE),
])
def test_init(testspec: TestSpec) -> None:
    testspec.run()


@pytest.mark.parametrize("testspec", [
    PytestAction("PROP_001",
        name="hash_id property set correctly",
        action=report.SystemInfo,
        kwargs=report_factories.system_info_kwargs(),
        validate_attr='hash_id',
        expected=report_factories.system_info_kwargs()['hash_id']),
    PytestAction("PROP_002",
        name="system property set correctly",
        action=report.SystemInfo,
        kwargs=report_factories.system_info_kwargs(),
        validate_attr='system',
        expected=report_factories.system_info_kwargs()['system']),
    PytestAction("PROP_003",
        name="system_version property set correctly",
        action=report.SystemInfo,
        kwargs=report_factories.system_info_kwargs(),
        validate_attr='system_version',
        expected=report_factories.system_info_kwargs()['system_version']),
    PytestAction("PROP_004",
        name="release property set correctly",
        action=report.SystemInfo,
        kwargs=report_factories.system_info_kwargs(),
        validate_attr='release',
        expected=report_factories.system_info_kwargs()['release']),
    PytestAction("PROP_005",
        name="machine property set correctly",
        action=report.SystemInfo,
        kwargs=report_factories.system_info_kwargs(),
        validate_attr='machine',
        expected=report_factories.system_info_kwargs()['machine']),
])
def test_properties(testspec: TestSpec) -> None:
    testspec.run()


@pytest.mark.parametrize(
      "testspec", [
         PytestAction("HASH_ID_001",
            name="Test valid hash_id value through from_dict",
            action=report.SystemInfo.from_dict,
            args=[report_factories.system_info_data()],
            validate_attr="hash_id",
            expected=report_factories.system_info_kwargs()["hash_id"]),  # type: ignore[index]
         PytestAction("HASH_ID_002",
            name="Test generated hash_id when not provided through from_dict",
            action=report.SystemInfo.from_dict,
            args=[report_factories.no_hash_id_system_info_data()],
            validate_attr="hash_id",
            assertion=Assert.NOT_EQUAL,
            expected=report_factories.system_info_kwargs()["hash_id"]),
      ])
def test_hash_id(testspec: TestSpec) -> None:
   """Test SystemInfo hash_id property."""
   testspec.run()


@pytest.mark.parametrize('testspec', [
    PytestAction('TO_DICT_001',
        name='SystemInfo to_dict returns a report.SystemInfoDict TypedDict mimic',
        action=is_typed_dict_mimic,
        args=[report_factories.system_info().to_dict(), report.SystemInfoDict],
        assertion=Assert.TRUE
    ),
    PytestAction('TO_DICT_002',
        name='SystemInfo to_dict returns a report.ImmutableSystemInfoDict TypedDict mimic',
        action=is_typed_dict_mimic,
        args=[report_factories.system_info().to_dict(), report.ImmutableSystemInfoDict],
        assertion=Assert.TRUE
    ),
])
def test_to_dict(testspec: TestSpec) -> None:
    """Test SystemInfo to_dict method."""
    testspec.run()


@pytest.mark.parametrize('testspec', [
    PytestAction('EQUALITY_001',
        name='SystemInfo equality comparison with identical hash_id values',
        action=lambda: report.SystemInfo(**report_factories.system_info_kwargs()),
        assertion=Assert.EQUAL,
        expected=report.SystemInfo(**report_factories.system_info_kwargs())
    ),
    PytestAction('EQUALITY_002',
        name='SystemInfo equality comparison with different hash_id values',
        action=lambda: report.SystemInfo(**report_factories.system_info_kwargs()),
        assertion=Assert.NOT_EQUAL,
        expected=report.SystemInfo(**report_factories.system_info_kwargs().replace(hash_id='d' * 64))
    ),
    PytestAction('EQUALITY_003',
        name=('SystemInfo equality comparison with different system_version values and '
            'calculated hash_id (hash_id not provided)'),
        action=lambda: report.SystemInfo(**report_factories.system_info_kwargs() - {'hash_id'}),
        assertion=Assert.NOT_EQUAL,
        expected=report.SystemInfo(
            **report_factories.system_info_kwargs().replace(system_version='3.11.0') - {'hash_id'})
    ),
    PytestAction('EQUALITY_004',
        name='SystemInfo equality comparison with same values and calculated hash_id (hash_id not provided)',
        action=lambda: report.SystemInfo(**report_factories.system_info_kwargs() - {'hash_id'}),
        assertion=Assert.EQUAL,
        expected=report.SystemInfo(**report_factories.system_info_kwargs() - {'hash_id'})
    ),
    PytestAction('EQUALITY_005',
        name='SystemInfo equality comparison with different types (not a SystemInfo instance)',
        action=lambda: report.SystemInfo(**report_factories.system_info_kwargs()),
        assertion=Assert.NOT_EQUAL,
        expected="Not a SystemInfo instance"
    ),
])
def test_equality(testspec: TestSpec) -> None:
    """Test SystemInfo equality comparison."""
    testspec.run()


def test_repr() -> None:
    """Test SystemInfo __repr__ method."""
    info = report_factories.system_info()
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
        name='SystemInfo instances with identical hash_id values have the same hash',
        action=hash,
        args=[report.SystemInfo(**report_factories.system_info_kwargs())],
        assertion=Assert.EQUAL,
        expected=hash(report.SystemInfo(**report_factories.system_info_kwargs()))
    ),
    PytestAction('HASH_002',
        name='SystemInfo instances with different values have different hashes',
        action=hash,
        args=[report.SystemInfo(**report_factories.system_info_kwargs() - {'hash_id'})],
        assertion=Assert.NOT_EQUAL,
        expected=hash(report.SystemInfo(
            **report_factories.system_info_kwargs().replace(system_version='3.10.1a')- {'hash_id'}))
    ),
])
def test_hash(testspec: TestSpec) -> None:
    """Test SystemInfo __hash__ method."""
    testspec.run()


@pytest.mark.parametrize('testspec', [
    PytestAction('PICKLE_001',
        name='SystemInfo instance can be pickled and unpickled correctly',
        action=lambda: pickle.loads(pickle.dumps(report_factories.system_info())),
        assertion=Assert.EQUAL,
        expected=report_factories.system_info()
    ),
])
def test_pickling(testspec: TestSpec) -> None:
    """Test that SystemInfo instances can be pickled and unpickled correctly."""
    testspec.run()


@pytest.mark.parametrize('testspec', [
    PytestAction('IMMUTABILITY_001',
        name='SystemInfo instance is immutable (attempting to set an attribute raises an exception)',
        action=lambda: setattr(report_factories.system_info(), 'system_version', '3.10.0'),
        exception=AttributeError
    ),
    PytestAction('IMMUTABILITY_002',
        name='SystemInfo instance is immutable (is_immutable returns True)',
        action=lambda: is_immutable(report_factories.system_info()),
        assertion=Assert.TRUE
    ),
])
def test_immutability(testspec: TestSpec) -> None:
    """Test that SystemInfo instances are immutable."""
    testspec.run()


@pytest.mark.parametrize('testspec', [
    PytestAction('SCHEMA_001',
        name='SystemInfo JSON schema is valid and can validate to_dict() output',
        action=validate,
        kwargs={
            'instance': report_factories.system_info().to_dict().thaw(),  # type: ignore
            'schema': report.SystemInfo.SCHEMA.as_dict()
        }
    ),
])
def test_json_schema(testspec: TestSpec) -> None:
    """Test that the JSON schema for SystemInfo is valid and can be
    used to validate a SystemInfo instance's to_dict() output."""
    testspec.run()


@pytest.mark.parametrize('testspec', [
    PytestAction('COPY_001',
        name='Copying a SystemInfo instance returns the same instance (since it is immutable)',
        action=copy,
        args=[report_factories.system_info()],
        assertion=Assert.IS,
        expected=report_factories.system_info()
    ),
    PytestAction('DEEP_COPY_001',
        name='Deep copying a SystemInfo instance returns the same instance (since it is immutable)',
        action=deepcopy,
        args=[report_factories.system_info()],
        assertion=Assert.IS,
        expected=report_factories.system_info()
    ),
])
def test_copy(testspec: TestSpec) -> None:
    """Test that copying a SystemInfo instance returns the same instance (since it is immutable)."""
    testspec.run()

# TODO: Add test for round-trip JSON serialization and deserialization of SystemInfo once a from_json method is
# implemented.
@pytest.mark.parametrize('testspec', [
     PytestAction('JSON_SERIALIZATION_001',
         name='SystemInfo can be serialized to JSON',
         action=report_factories.system_info().as_json,
         assertion=Assert.ISINSTANCE,
         expected=str),
    PytestAction('JSON_SERIALIZATION_002',
        name='SystemInfo can be directly serialized to a JSON compatible dictionary by simplejson',
        action=simplejson.dumps,
        kwargs={"obj": report_factories.system_info(),
                "sort_keys": True, "for_json": True, "iterable_as_array": True},
        assertion=Assert.ISINSTANCE,
        expected=str),
    PytestAction('JSON_SERIALIZATION_003',
            name='SystemInfo.for_json() can serialized to a JSON string by json.dumps',
            action=json.dumps,
            kwargs={"obj": report_factories.system_info().for_json(), "sort_keys": True},
            assertion=Assert.ISINSTANCE,
            expected=str),
 ])
def test_json_serialization(testspec: TestSpec) -> None:
    """Test that SystemInfo can be serialized to JSON."""
    testspec.run()

if __name__ == "__main__":
    pytest.main([__file__])
