"""Tests for ResultsInfo() report for SimpleBench tests."""
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
from simplebench.report._error_tags import _ResultsInfoErrorTag
from simplebench.report.versions import v1 as report
from simplebench.report.versions.v1 import (  # noqa: F401 -- imported for repr eval test
    ExtrasObject,
    MetricsObject,
    RawDataBlock,
    StatsBlock,
    ValueBlock,
)
from simplebench.simplebench_types import CoreDataMapping, is_immutable  # noqa: F401
from simplebench.validators import is_typed_dict_mimic
from simplebench_tests.factories.report import v1 as report_factories

ResultsInfo: TypeAlias = report.ResultsInfo


# JSON Schema Registry setup for validating JSON schema in tests
registry = Registry().with_resources([
    (report.ResultsInfo.SCHEMA.ID, Resource.from_contents(report.ResultsInfo.SCHEMA.as_dict())),
    (report.StatsBlock.SCHEMA.ID, Resource.from_contents(report.StatsBlock.SCHEMA.as_dict())),
    (report.ValueBlock.SCHEMA.ID, Resource.from_contents(report.ValueBlock.SCHEMA.as_dict())),
    (report.RawDataBlock.SCHEMA.ID, Resource.from_contents(report.RawDataBlock.SCHEMA.as_dict())),
])

validator = Draft202012Validator(schema=report.ResultsInfo.SCHEMA.as_dict(), registry=registry)

@pytest.mark.parametrize("testspec", [
    PytestAction("INIT_001",
        name="All fields provided",
        action=report.ResultsInfo,
        kwargs=report_factories.results_info_kwargs(),
        assertion=Assert.ISINSTANCE,
        expected=report.ResultsInfo),
    PytestAction("INIT_002",
        name="Only required fields provided (hash_id optional)",
        action=report.ResultsInfo,
        kwargs=report_factories.results_info_kwargs() - {'hash_id'},  # Remove optional fields
        assertion=Assert.ISINSTANCE,
        expected=report.ResultsInfo),
    PytestAction("INIT_003",
        name="Wrong type for field (hash_id as int)",
        action=report.ResultsInfo,
        kwargs=report_factories.results_info_kwargs().replace(hash_id=123),
        exception=SimpleBenchTypeError,
        exception_tag=_ResultsInfoErrorTag.INVALID_HASH_ID_TYPE),
    PytestAction("INIT_004",
        name="Invalid hash_id value (not 64 hex chars)",
        action=report.ResultsInfo,
        kwargs=report_factories.results_info_kwargs().replace(hash_id='invalid_hash'),
        exception=SimpleBenchValueError,
        exception_tag=_ResultsInfoErrorTag.INVALID_HASH_ID_VALUE),
    PytestAction("INIT_005",
        name="Empty string for optional hash_id field",
        action=report.ResultsInfo,
        kwargs=report_factories.results_info_kwargs().replace(hash_id=''),
        assertion=Assert.ISINSTANCE,
        expected=report.ResultsInfo),
    PytestAction("INIT_006",
        name="Missing required field (title)",
        action=report.ResultsInfo,
        kwargs=report_factories.results_info_kwargs() - {'title'},
        exception=TypeError),
    PytestAction("INIT_011",
        name="Missing required field (n)",
        action=report.ResultsInfo,
        kwargs=report_factories.results_info_kwargs() - {'n'},
        exception=TypeError),
    PytestAction("INIT_014",
        name="Missing required field (variation_marks)",
        action=report.ResultsInfo,
        kwargs=report_factories.results_info_kwargs() - {'variation_marks'},
        exception=TypeError),
])
def test_init(testspec: TestSpec) -> None:
    testspec.run()


@pytest.mark.parametrize("testspec", [
    PytestAction("PROP_001",
        name="hash_id property set correctly",
        action=report.ResultsInfo,
        kwargs=report_factories.results_info_kwargs(),
        validate_attr='hash_id',
        expected=report_factories.results_info_kwargs()['hash_id']),
])
def test_properties(testspec: TestSpec) -> None:
    testspec.run()


@pytest.mark.parametrize(
      "testspec", [
         PytestAction("HASH_ID_001",
            name="Test valid hash_id value through from_dict",
            action=report.ResultsInfo.from_dict,
            args=[report_factories.results_info_data()],
            validate_attr="hash_id",
            expected=report_factories.results_info_kwargs()["hash_id"]),  # type: ignore[index]
         PytestAction("HASH_ID_002",
            name="Test generated hash_id when not provided through from_dict",
            action=report.ResultsInfo.from_dict,
            args=[report_factories.no_hash_id_results_info_data()],
            validate_attr="hash_id",
            assertion=Assert.NOT_EQUAL,
            expected=report_factories.results_info_kwargs()["hash_id"]),
])
def test_hash_id(testspec: TestSpec) -> None:
   """Test ResultsInfo hash_id property."""
   testspec.run()


@pytest.mark.parametrize('testspec', [
    PytestAction('TO_DICT_001',
        name='ResultsInfo to_dict returns a report.ResultsInfoDict TypedDict mimic',
        action=is_typed_dict_mimic,
        args=[report_factories.results_info().to_dict(), report.ResultsInfoDict],
        assertion=Assert.TRUE
    ),
    PytestAction('TO_DICT_002',
        name='ResultsInfo to_dict returns a report.ImmutableResultsInfoDict TypedDict mimic',
        action=is_typed_dict_mimic,
        args=[report_factories.results_info().to_dict(), report.ImmutableResultsInfoDict],
        assertion=Assert.TRUE
    ),
])
def test_to_dict(testspec: TestSpec) -> None:
    """Test ResultsInfo to_dict method."""
    testspec.run()


@pytest.mark.parametrize('testspec', [
    PytestAction('EQUALITY_001',
        name='ResultsInfo equality comparison with identical hash_id values',
        action=lambda: report.ResultsInfo(**report_factories.results_info_kwargs()),
        assertion=Assert.EQUAL,
        expected=report.ResultsInfo(**report_factories.results_info_kwargs())
    ),
    PytestAction('EQUALITY_002',
        name='ResultsInfo equality comparison with different hash_id values',
        action=lambda: report.ResultsInfo(**report_factories.results_info_kwargs()),
        assertion=Assert.NOT_EQUAL,
        expected=report.ResultsInfo(**report_factories.results_info_kwargs().replace(hash_id='d' * 64))
    ),
    PytestAction('EQUALITY_003',
        name=('ResultsInfo equality comparison with different description value and '
            'calculated hash_id (hash_id not provided)'),
        action=lambda: report.ResultsInfo(**report_factories.results_info_kwargs() - {'hash_id'}),
        assertion=Assert.NOT_EQUAL,
        expected=report.ResultsInfo(
            **report_factories.results_info_kwargs().replace(description='other') - {'hash_id'})
    ),
    PytestAction('EQUALITY_004',
        name='ResultsInfo equality comparison with same values and calculated hash_id (hash_id not provided)',
        action=lambda: report.ResultsInfo(**report_factories.results_info_kwargs() - {'hash_id'}),
        assertion=Assert.EQUAL,
        expected=report.ResultsInfo(**report_factories.results_info_kwargs() - {'hash_id'})
    ),
    PytestAction('EQUALITY_005',
        name='ResultsInfo equality comparison with different types (not a ResultsInfo instance)',
        action=lambda: report.ResultsInfo(**report_factories.results_info_kwargs()),
        assertion=Assert.NOT_EQUAL,
        expected="Not a ResultsInfo instance"
    ),
])
def test_equality(testspec: TestSpec) -> None:
    """Test ResultsInfo equality comparison."""
    testspec.run()


def test_repr() -> None:
    """Test ResultsInfo __repr__ method."""
    info = report_factories.results_info()
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
        name='ResultsInfo instances with identical hash_id values have the same hash',
        action=hash,
        args=[report.ResultsInfo(**report_factories.results_info_kwargs())],
        assertion=Assert.EQUAL,
        expected=hash(report.ResultsInfo(**report_factories.results_info_kwargs()))
    ),
    PytestAction('HASH_002',
        name='ResultsInfo instances with different values have different hashes',
        action=hash,
        args=[report.ResultsInfo(**report_factories.results_info_kwargs() - {'hash_id'})],
        assertion=Assert.NOT_EQUAL,
        expected=hash(report.ResultsInfo(
            **report_factories.results_info_kwargs().replace(description='other')- {'hash_id'}))
    ),
])
def test_hash(testspec: TestSpec) -> None:
    """Test ResultsInfo __hash__ method."""
    testspec.run()


@pytest.mark.parametrize('testspec', [
    PytestAction('PICKLE_001',
        name='ResultsInfo instance can be pickled and unpickled correctly',
        action=lambda: pickle.loads(pickle.dumps(report_factories.results_info())),
        assertion=Assert.EQUAL,
        expected=report_factories.results_info()
    ),
])
def test_pickling(testspec: TestSpec) -> None:
    """Test that ResultsInfo instances can be pickled and unpickled correctly."""
    testspec.run()


@pytest.mark.parametrize('testspec', [
    PytestAction('IMMUTABILITY_001',
        name='ResultsInfo instance is immutable (attempting to set an attribute raises an exception)',
        action=lambda: setattr(report_factories.results_info(), 'description', 'other'),
        exception=AttributeError
    ),
    PytestAction('IMMUTABILITY_002',
        name='ResultsInfo instance is immutable (is_immutable returns True)',
        action=lambda: is_immutable(report_factories.results_info()),
        assertion=Assert.TRUE
    ),
])
def test_immutability(testspec: TestSpec) -> None:
    """Test that ResultsInfo instances are immutable."""
    testspec.run()


@pytest.mark.parametrize('testspec', [
    PytestAction('SCHEMA_001',
        name='ResultsInfo JSON schema is valid and can validate to_dict() output',
        action=validator.validate,
        args=[report_factories.results_info().to_dict().thaw()],  # type: ignore
    ),
])
def test_json_schema(testspec: TestSpec) -> None:
    """Test that the JSON schema for ResultsInfo is valid and can be
    used to validate a ResultsInfo instance's to_dict() output."""
    testspec.run()

@pytest.mark.parametrize('testspec', [
    PytestAction('COPY_001',
        name='Copying a ResultsInfo instance returns the same instance (since it is immutable)',
        action=copy,
        args=[report_factories.results_info()],
        assertion=Assert.IS,
        expected=report_factories.results_info()
    ),
    PytestAction('DEEP_COPY_001',
        name='Deep copying a ResultsInfo instance returns the same instance (since it is immutable)',
        action=deepcopy,
        args=[report_factories.results_info()],
        assertion=Assert.IS,
        expected=report_factories.results_info()
    ),
])
def test_copy(testspec: TestSpec) -> None:
    """Test that copying a ResultsInfo instance returns the same instance (since it is immutable)."""
    testspec.run()

# TODO: Add test for round-trip JSON serialization and deserialization of ResultsInfo once a from_json method is
# implemented.
@pytest.mark.parametrize('testspec', [
     PytestAction('JSON_SERIALIZATION_001',
         name='ResultsInfo can be serialized to JSON',
         action=report_factories.results_info().as_json,
         assertion=Assert.ISINSTANCE,
         expected=str),
    PytestAction('JSON_SERIALIZATION_002',
        name='ResultsInfo can be directly serialized to a JSON compatible dictionary by simplejson',
        action=simplejson.dumps,
        kwargs={"obj": report_factories.results_info(),
                "sort_keys": True, "for_json": True, "iterable_as_array": True},
        assertion=Assert.ISINSTANCE,
        expected=str),
    PytestAction('JSON_SERIALIZATION_003',
            name='ResultsInfo.for_json() can serialized to a JSON string by json.dumps',
            action=json.dumps,
            kwargs={"obj": report_factories.results_info().for_json(), "sort_keys": True},
            assertion=Assert.ISINSTANCE,
            expected=str),
 ])
def test_json_serialization(testspec: TestSpec) -> None:
    """Test that ResultsInfo can be serialized to JSON."""
    testspec.run()

if __name__ == "__main__":
    pytest.main([__file__])
