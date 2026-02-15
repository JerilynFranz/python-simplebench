"""Tests for VCSInfo() report for SimpleBench tests."""
import json
import pickle
from copy import copy, deepcopy
from typing import TypeAlias

import pytest
import simplejson
from jsonschema import validate
from testspec import Assert, PytestAction, TestSpec

from simplebench.exceptions import SimpleBenchTypeError, SimpleBenchValueError
from simplebench.report._error_tags import _VCSInfoErrorTag
from simplebench.report.versions import v1 as report
from simplebench.simplebench_types import is_immutable
from simplebench.validators import is_typed_dict_mimic
from simplebench_tests.factories.report import v1 as report_factories

VCSInfo: TypeAlias = report.VCSInfo

@pytest.mark.parametrize("testspec", [
    PytestAction("INIT_001",
        name="All fields provided",
        action=report.VCSInfo,
        kwargs=report_factories.vcs_info_kwargs(),
        assertion=Assert.ISINSTANCE,
        expected=report.VCSInfo),
    PytestAction("INIT_002",
        name="Only required fields provided (hash_id is optional)",
        action=report.VCSInfo,
        kwargs=report_factories.vcs_info_kwargs() - {'hash_id'},
        assertion=Assert.ISINSTANCE,
        expected=report.VCSInfo),
    PytestAction("INIT_003",
        name="Wrong type for field (hash_id as int)",
        action=report.VCSInfo,
        kwargs=report_factories.vcs_info_kwargs().replace(hash_id=123),
        exception=SimpleBenchTypeError,
        exception_tag=_VCSInfoErrorTag.INVALID_HASH_ID_TYPE),
    PytestAction("INIT_004",
        name="Invalid hash_id value (not 64 hex chars)",
        action=report.VCSInfo,
        kwargs=report_factories.vcs_info_kwargs().replace(hash_id='invalid_hash'),
        exception=SimpleBenchValueError,
        exception_tag=_VCSInfoErrorTag.INVALID_HASH_ID_STRUCTURE),
    PytestAction("INIT_005",
        name="Empty string for optional hash_id field",
        action=report.VCSInfo,
        kwargs=report_factories.vcs_info_kwargs().replace(hash_id=''),
        assertion=Assert.ISINSTANCE,
        expected=report.VCSInfo),
    PytestAction("INIT_006",
        name="Missing required field (vcs)",
        action=report.VCSInfo,
        kwargs=report_factories.vcs_info_kwargs() - {'vcs'},
        exception=TypeError),
    PytestAction("INIT_007",
        name="Wrong type for required field (vcs as int)",
        action=report.VCSInfo,
        kwargs=report_factories.vcs_info_kwargs().replace(vcs=123),
        exception=SimpleBenchTypeError,
        exception_tag=_VCSInfoErrorTag.INVALID_VCS_TYPE),
    PytestAction("INIT_008",
        name="Empty string for required field (vcs)",
        action=report.VCSInfo,
        kwargs=report_factories.vcs_info_kwargs().replace(vcs=''),
        exception=SimpleBenchValueError,
        exception_tag=_VCSInfoErrorTag.INVALID_VCS_VALUE),
    PytestAction("INIT_009",
        name="Missing required field (commit_id)",
        action=report.VCSInfo,
        kwargs=report_factories.vcs_info_kwargs() - {'commit_id'},
        exception=TypeError),
    PytestAction("INIT_010",
        name="Wrong type for required field (commit_id as int)",
        action=report.VCSInfo,
        kwargs=report_factories.vcs_info_kwargs().replace(commit_id=123),
        exception=SimpleBenchTypeError,
        exception_tag=_VCSInfoErrorTag.INVALID_COMMIT_ID_TYPE),
    PytestAction("INIT_011",
        name="Empty string for required field (commit_id)",
        action=report.VCSInfo,
        kwargs=report_factories.vcs_info_kwargs().replace(commit_id=''),
        exception=SimpleBenchValueError,
        exception_tag=_VCSInfoErrorTag.INVALID_COMMIT_ID_VALUE),
    PytestAction("INIT_012",
        name="Missing required field (commit_datetime)",
        action=report.VCSInfo,
        kwargs=report_factories.vcs_info_kwargs() - {'commit_datetime'},
        exception=TypeError),
    PytestAction("INIT_013",
        name="Wrong type for required field (commit_datetime as int)",
        action=report.VCSInfo,
        kwargs=report_factories.vcs_info_kwargs().replace(commit_datetime=123),
        exception=SimpleBenchTypeError,
        exception_tag=_VCSInfoErrorTag.INVALID_COMMIT_DATETIME_TYPE),
    PytestAction("INIT_014",
        name="Invalid datetime string for commit_datetime field",
        action=report.VCSInfo,
        kwargs=report_factories.vcs_info_kwargs().replace(commit_datetime='invalid_datetime'),
        exception=SimpleBenchValueError,
        exception_tag=_VCSInfoErrorTag.INVALID_COMMIT_DATETIME_VALUE),
    PytestAction("INIT_015",
        name="Missing required field (branch)",
        action=report.VCSInfo,
        kwargs=report_factories.vcs_info_kwargs() - {'branch'},
        exception=TypeError),
    PytestAction("INIT_016",
        name="Wrong type for required field (branch as int)",
        action=report.VCSInfo,
        kwargs=report_factories.vcs_info_kwargs().replace(branch=123),
        exception=SimpleBenchTypeError,
        exception_tag=_VCSInfoErrorTag.INVALID_BRANCH_TYPE),
    PytestAction("INIT_017",
        name="Empty string for required field (branch)",
        action=report.VCSInfo,
        kwargs=report_factories.vcs_info_kwargs().replace(branch=''),
        exception=SimpleBenchValueError,
        exception_tag=_VCSInfoErrorTag.INVALID_BRANCH_VALUE),
    PytestAction("INIT_018",
        name="Missing required field (repository_url)",
        action=report.VCSInfo,
        kwargs=report_factories.vcs_info_kwargs() - {'repository_url'},
        exception=TypeError),
    PytestAction("INIT_019",
        name="Wrong type for required field (repository_url as int)",
        action=report.VCSInfo,
        kwargs=report_factories.vcs_info_kwargs().replace(repository_url=123),
        exception=SimpleBenchTypeError,
        exception_tag=_VCSInfoErrorTag.INVALID_REPOSITORY_URL_TYPE),
    PytestAction("INIT_020",
        name="Missing required field (is_dirty)",
        action=report.VCSInfo,
        kwargs=report_factories.vcs_info_kwargs() - {'is_dirty'},
        exception=TypeError),
    PytestAction("INIT_021",
        name="Wrong type for required field (is_dirty as int)",
        action=report.VCSInfo,
        kwargs=report_factories.vcs_info_kwargs().replace(is_dirty=123),
        exception=SimpleBenchTypeError,
        exception_tag=_VCSInfoErrorTag.INVALID_IS_DIRTY_TYPE),
])
def test_init(testspec: TestSpec) -> None:
    testspec.run()


@pytest.mark.parametrize("testspec", [
    PytestAction("PROP_001",
        name="hash_id property set correctly",
        action=report.VCSInfo,
        kwargs=report_factories.vcs_info_kwargs(),
        validate_attr='hash_id',
        expected=report_factories.vcs_info_kwargs()['hash_id']),
    PytestAction("PROP_002",
        name="vcs property set correctly",
        action=report.VCSInfo,
        kwargs=report_factories.vcs_info_kwargs(),
        validate_attr='vcs',
        expected=report_factories.vcs_info_kwargs()['vcs']),
    PytestAction("PROP_003",
        name="commit_id property set correctly",
        action=report.VCSInfo,
        kwargs=report_factories.vcs_info_kwargs(),
        validate_attr='commit_id',
        expected=report_factories.vcs_info_kwargs()['commit_id']),
    PytestAction("PROP_004",
        name="commit_datetime property set correctly",
        action=report.VCSInfo,
        kwargs=report_factories.vcs_info_kwargs(),
        validate_attr='commit_datetime',
        expected=report_factories.vcs_info_kwargs()['commit_datetime']),
    PytestAction("PROP_005",
        name="branch property set correctly",
        action=report.VCSInfo,
        kwargs=report_factories.vcs_info_kwargs(),
        validate_attr='branch',
        expected=report_factories.vcs_info_kwargs()['branch']),
    PytestAction("PROP_006",
        name="repository_url property set correctly",
        action=report.VCSInfo,
        kwargs=report_factories.vcs_info_kwargs(),
        validate_attr='repository_url',
        expected=report_factories.vcs_info_kwargs()['repository_url']),
    PytestAction("PROP_007",
        name="is_dirty property set correctly",
        action=report.VCSInfo,
        kwargs=report_factories.vcs_info_kwargs(),
        validate_attr='is_dirty',
        expected=report_factories.vcs_info_kwargs()['is_dirty']),
])
def test_properties(testspec: TestSpec) -> None:
    testspec.run()


@pytest.mark.parametrize(
      "testspec", [
         PytestAction("HASH_ID_001",
            name="Test valid hash_id value through from_dict",
            action=report.VCSInfo.from_dict,
            args=[report_factories.vcs_info_data()],
            validate_attr="hash_id",
            expected=report_factories.vcs_info_kwargs()["hash_id"]),  # type: ignore[index]
         PytestAction("HASH_ID_002",
            name="Test generated hash_id when not provided through from_dict",
            action=report.VCSInfo.from_dict,
            args=[report_factories.no_hash_id_vcs_info_data()],
            validate_attr="hash_id",
            assertion=Assert.NOT_EQUAL,
            expected=report_factories.vcs_info_kwargs()["hash_id"]),
])
def test_hash_id(testspec: TestSpec) -> None:
   """Test VCSInfo hash_id property."""
   testspec.run()


@pytest.mark.parametrize('testspec', [
    PytestAction('TO_DICT_001',
        name='VCSInfo to_dict returns a report.VCSInfoDict TypedDict mimic',
        action=is_typed_dict_mimic,
        args=[report_factories.vcs_info().to_dict(), report.VCSInfoDict],
        assertion=Assert.TRUE
    ),
    PytestAction('TO_DICT_002',
        name='VCSInfo to_dict returns a report.ImmutableVCSInfoDict TypedDict mimic',
        action=is_typed_dict_mimic,
        args=[report_factories.vcs_info().to_dict(), report.ImmutableVCSInfoDict],
        assertion=Assert.TRUE
    ),
])
def test_to_dict(testspec: TestSpec) -> None:
    """Test VCSInfo to_dict method."""
    testspec.run()


@pytest.mark.parametrize('testspec', [
    PytestAction('EQUALITY_001',
        name='VCSInfo equality comparison with identical hash_id values',
        action=lambda: report.VCSInfo(**report_factories.vcs_info_kwargs()),
        assertion=Assert.EQUAL,
        expected=report.VCSInfo(**report_factories.vcs_info_kwargs())
    ),
    PytestAction('EQUALITY_002',
        name='VCSInfo equality comparison with different hash_id values',
        action=lambda: report.VCSInfo(**report_factories.vcs_info_kwargs()),
        assertion=Assert.NOT_EQUAL,
        expected=report.VCSInfo(**report_factories.vcs_info_kwargs().replace(hash_id='d' * 64))
    ),
    PytestAction('EQUALITY_003',
        name=('VCSInfo equality comparison with different vcs values and '
            'calculated hash_id (hash_id not provided)'),
        action=lambda: report.VCSInfo(**report_factories.vcs_info_kwargs() - {'hash_id'}),
        assertion=Assert.NOT_EQUAL,
        expected=report.VCSInfo(
            **report_factories.vcs_info_kwargs().replace(vcs='other') - {'hash_id'})
    ),
    PytestAction('EQUALITY_004',
        name='VCSInfo equality comparison with same values and calculated hash_id (hash_id not provided)',
        action=lambda: report.VCSInfo(**report_factories.vcs_info_kwargs() - {'hash_id'}),
        assertion=Assert.EQUAL,
        expected=report.VCSInfo(**report_factories.vcs_info_kwargs() - {'hash_id'})
    ),
    PytestAction('EQUALITY_005',
        name='VCSInfo equality comparison with different types (not a VCSInfo instance)',
        action=lambda: report.VCSInfo(**report_factories.vcs_info_kwargs()),
        assertion=Assert.NOT_EQUAL,
        expected="Not a VCSInfo instance"
    ),
])
def test_equality(testspec: TestSpec) -> None:
    """Test VCSInfo equality comparison."""
    testspec.run()


def test_repr() -> None:
    """Test VCSInfo __repr__ method."""
    info = report_factories.vcs_info()
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
        name='VCSInfo instances with identical hash_id values have the same hash',
        action=hash,
        args=[report.VCSInfo(**report_factories.vcs_info_kwargs())],
        assertion=Assert.EQUAL,
        expected=hash(report.VCSInfo(**report_factories.vcs_info_kwargs()))
    ),
    PytestAction('HASH_002',
        name='VCSInfo instances with different values have different hashes',
        action=hash,
        args=[report.VCSInfo(**report_factories.vcs_info_kwargs() - {'hash_id'})],
        assertion=Assert.NOT_EQUAL,
        expected=hash(report.VCSInfo(
            **report_factories.vcs_info_kwargs().replace(vcs='other')- {'hash_id'}))
    ),
])
def test_hash(testspec: TestSpec) -> None:
    """Test VCSInfo __hash__ method."""
    testspec.run()


@pytest.mark.parametrize('testspec', [
    PytestAction('PICKLE_001',
        name='VCSInfo instance can be pickled and unpickled correctly',
        action=lambda: pickle.loads(pickle.dumps(report_factories.vcs_info())),
        assertion=Assert.EQUAL,
        expected=report_factories.vcs_info()
    ),
])
def test_pickling(testspec: TestSpec) -> None:
    """Test that VCSInfo instances can be pickled and unpickled correctly."""
    testspec.run()


@pytest.mark.parametrize('testspec', [
    PytestAction('IMMUTABILITY_001',
        name='VCSInfo instance is immutable (attempting to set an attribute raises an exception)',
        action=lambda: setattr(report_factories.vcs_info(), 'vcs', 'other'),
        exception=AttributeError
    ),
    PytestAction('IMMUTABILITY_002',
        name='VCSInfo instance is immutable (is_immutable returns True)',
        action=lambda: is_immutable(report_factories.vcs_info()),
        assertion=Assert.TRUE
    ),
])
def test_immutability(testspec: TestSpec) -> None:
    """Test that VCSInfo instances are immutable."""
    testspec.run()


@pytest.mark.parametrize('testspec', [
    PytestAction('SCHEMA_001',
        name='VCSInfo JSON schema is valid and can validate to_dict() output',
        action=validate,
        kwargs={
            'instance': report_factories.vcs_info().to_dict().thaw(),  # type: ignore
            'schema': report.VCSInfo.SCHEMA.as_dict()
        }
    ),
])
def test_json_schema(testspec: TestSpec) -> None:
    """Test that the JSON schema for VCSInfo is valid and can be
    used to validate a VCSInfo instance's to_dict() output."""
    testspec.run()


@pytest.mark.parametrize('testspec', [
    PytestAction('COPY_001',
        name='Copying a VCSInfo instance returns the same instance (since it is immutable)',
        action=copy,
        args=[report_factories.vcs_info()],
        assertion=Assert.IS,
        expected=report_factories.vcs_info()
    ),
    PytestAction('DEEP_COPY_001',
        name='Deep copying a VCSInfo instance returns the same instance (since it is immutable)',
        action=deepcopy,
        args=[report_factories.vcs_info()],
        assertion=Assert.IS,
        expected=report_factories.vcs_info()
    ),
])
def test_copy(testspec: TestSpec) -> None:
    """Test that copying a VCSInfo instance returns the same instance (since it is immutable)."""
    testspec.run()

# TODO: Add test for round-trip JSON serialization and deserialization of VCSInfo once a from_json method is
# implemented.
@pytest.mark.parametrize('testspec', [
     PytestAction('JSON_SERIALIZATION_001',
         name='VCSInfo can be serialized to JSON',
         action=report_factories.vcs_info().as_json,
         assertion=Assert.ISINSTANCE,
         expected=str),
    PytestAction('JSON_SERIALIZATION_002',
        name='VCSInfo can be directly serialized to a JSON compatible dictionary by simplejson',
        action=simplejson.dumps,
        kwargs={"obj": report_factories.vcs_info(),
                "sort_keys": True, "for_json": True, "iterable_as_array": True},
        assertion=Assert.ISINSTANCE,
        expected=str),
    PytestAction('JSON_SERIALIZATION_003',
            name='VCSInfo.for_json() can serialized to a JSON string by json.dumps',
            action=json.dumps,
            kwargs={"obj": report_factories.vcs_info().for_json(), "sort_keys": True},
            assertion=Assert.ISINSTANCE,
            expected=str),
 ])
def test_json_serialization(testspec: TestSpec) -> None:
    """Test that VCSInfo can be serialized to JSON."""
    testspec.run()

if __name__ == "__main__":
    pytest.main([__file__])
