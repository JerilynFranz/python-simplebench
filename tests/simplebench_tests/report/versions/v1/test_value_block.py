"""Tests for ValueBlock() report for SimpleBench tests."""
import json
import pickle
from copy import copy, deepcopy
from typing import TypeAlias

import pytest
import simplejson
from jsonschema import validate
from testspec import Assert, PytestAction, TestSpec

from simplebench.exceptions import SimpleBenchTypeError, SimpleBenchValueError
from simplebench.report._error_tags import _ValueBlockErrorTag
from simplebench.report.versions import v1 as report
from simplebench.simplebench_types import is_immutable
from simplebench.validators import is_typed_dict_mimic
from simplebench_tests.factories.report import v1 as report_factories

ValueBlock: TypeAlias = report.ValueBlock

@pytest.mark.parametrize("testspec", [
    PytestAction("INIT_001",
        name="All fields provided",
        action=report.ValueBlock,
        kwargs=report_factories.value_block_kwargs(),
        assertion=Assert.ISINSTANCE,
        expected=report.ValueBlock),
    PytestAction("INIT_002",
        name="Only required fields provided (hash_id and timer are optional)",
        action=report.ValueBlock,
        kwargs=report_factories.value_block_kwargs() - {'hash_id', 'timer'},  # Remove optional fields
        assertion=Assert.ISINSTANCE,
        expected=report.ValueBlock),
    PytestAction("INIT_003",
        name="Wrong type for field (hash_id as int)",
        action=report.ValueBlock,
        kwargs=report_factories.value_block_kwargs().replace(hash_id=123),
        exception=SimpleBenchTypeError,
        exception_tag=_ValueBlockErrorTag.INVALID_HASH_ID_TYPE),
    PytestAction("INIT_004",
        name="Invalid hash_id value (not 64 hex chars)",
        action=report.ValueBlock,
        kwargs=report_factories.value_block_kwargs().replace(hash_id='invalid_hash'),
        exception=SimpleBenchValueError,
        exception_tag=_ValueBlockErrorTag.INVALID_HASH_ID_STRUCTURE),
    PytestAction("INIT_005",
        name="Empty string for optional hash_id field",
        action=report.ValueBlock,
        kwargs=report_factories.value_block_kwargs().replace(hash_id=''),
        assertion=Assert.ISINSTANCE,
        expected=report.ValueBlock),
    PytestAction("INIT_006",
        name="Missing required field (semantic_type)",
        action=report.ValueBlock,
        kwargs=report_factories.value_block_kwargs() - {'semantic_type'},
        exception=TypeError),
    PytestAction("INIT_007",
        name="Wrong type for field (semantic_type as int)",
        action=report.ValueBlock,
        kwargs=report_factories.value_block_kwargs().replace(semantic_type=123),
        exception=SimpleBenchTypeError,
        exception_tag=_ValueBlockErrorTag.INVALID_SEMANTIC_TYPE_TYPE),
    PytestAction("INIT_008",
        name="Invalid semantic_type value (not a valid namespaced identifier)",
        action=report.ValueBlock,
        kwargs=report_factories.value_block_kwargs().replace(semantic_type='invalid semantic type'),
        exception=SimpleBenchValueError,
        exception_tag=_ValueBlockErrorTag.INVALID_SEMANTIC_TYPE_VALUE),
    PytestAction("INIT_009",
        name="Wrong type for optional timer field (timer as int)",
        action=report.ValueBlock,
        kwargs=report_factories.value_block_kwargs().replace(timer=123),
        exception=SimpleBenchTypeError,
        exception_tag=_ValueBlockErrorTag.INVALID_TIMER_TYPE),
    PytestAction("INIT_011",
        name="Missing required field (unit)",
        action=report.ValueBlock,
        kwargs=report_factories.value_block_kwargs() - {'unit'},
        exception=TypeError),
    PytestAction("INIT_012",
        name="Wrong type for field (unit as int)",
        action=report.ValueBlock,
        kwargs=report_factories.value_block_kwargs().replace(unit=123),
        exception=SimpleBenchTypeError,
        exception_tag=_ValueBlockErrorTag.INVALID_UNIT_TYPE),
    PytestAction("INIT_013",
        name="Invalid unit value (empty string)",
        action=report.ValueBlock,
        kwargs=report_factories.value_block_kwargs().replace(unit=''),
        exception=SimpleBenchValueError,
        exception_tag=_ValueBlockErrorTag.INVALID_UNIT_VALUE),
    PytestAction("INIT_014",
        name="Missing required field (scale)",
        action=report.ValueBlock,
        kwargs=report_factories.value_block_kwargs() - {'scale'},
        exception=TypeError),
    PytestAction("INIT_015",
        name="Wrong type for field (scale as str)",
        action=report.ValueBlock,
        kwargs=report_factories.value_block_kwargs().replace(scale='not a float'),
        exception=SimpleBenchTypeError,
        exception_tag=_ValueBlockErrorTag.INVALID_SCALE_TYPE),
    PytestAction("INIT_016",
        name="Invalid scale value (negative float)",
        action=report.ValueBlock,
        kwargs=report_factories.value_block_kwargs().replace(scale=-1.0),
        exception=SimpleBenchValueError,
        exception_tag=_ValueBlockErrorTag.INVALID_SCALE_VALUE),
    PytestAction("INIT_017",
        name="Missing required field (value)",
        action=report.ValueBlock,
        kwargs=report_factories.value_block_kwargs() - {'value'},
        exception=TypeError),
    PytestAction("INIT_018",
        name="Wrong type for field (value as str)",
        action=report.ValueBlock,
        kwargs=report_factories.value_block_kwargs().replace(value='not a number'),
        exception=SimpleBenchTypeError,
        exception_tag=_ValueBlockErrorTag.INVALID_VALUE_TYPE),
    PytestAction("INIT_019",
        name="Invalid value (Nan)",
        action=report.ValueBlock,
        kwargs=report_factories.value_block_kwargs().replace(value=float('nan')),
        exception=SimpleBenchValueError,
        exception_tag=_ValueBlockErrorTag.INVALID_VALUE_TYPE),
])
def test_init(testspec: TestSpec) -> None:
    testspec.run()


@pytest.mark.parametrize("testspec", [
    PytestAction("PROP_001",
        name="hash_id property set correctly",
        action=report.ValueBlock,
        kwargs=report_factories.value_block_kwargs(),
        validate_attr='hash_id',
        expected=report_factories.value_block_kwargs()['hash_id']),
    PytestAction("PROP_002",
        name="semantic_type property set correctly",
        action=report.ValueBlock,
        kwargs=report_factories.value_block_kwargs(),
        validate_attr='semantic_type',
        expected=report_factories.value_block_kwargs()['semantic_type']),
    PytestAction("PROP_003",
        name="timer property set correctly",
        action=report.ValueBlock,
        kwargs=report_factories.value_block_kwargs(),
        validate_attr='timer',
        expected=report_factories.value_block_kwargs()['timer']),
    PytestAction("PROP_004",
        name="unit property set correctly",
        action=report.ValueBlock,
        kwargs=report_factories.value_block_kwargs(),
        validate_attr='unit',
        expected=report_factories.value_block_kwargs()['unit']),
    PytestAction("PROP_005",
        name="scale property set correctly",
        action=report.ValueBlock,
        kwargs=report_factories.value_block_kwargs(),
        validate_attr='scale',
        expected=report_factories.value_block_kwargs()['scale']),
    PytestAction("PROP_006",
        name="value property set correctly",
        action=report.ValueBlock,
        kwargs=report_factories.value_block_kwargs(),
        validate_attr='value',
        expected=report_factories.value_block_kwargs()['value']),
])
def test_properties(testspec: TestSpec) -> None:
    testspec.run()


@pytest.mark.parametrize(
      "testspec", [
         PytestAction("HASH_ID_001",
            name="Test valid hash_id value through from_dict",
            action=report.ValueBlock.from_dict,
            args=[report_factories.value_block_data()],
            validate_attr="hash_id",
            expected=report_factories.value_block_kwargs()["hash_id"]),  # type: ignore[index]
         PytestAction("HASH_ID_002",
            name="Test generated hash_id when not provided through from_dict",
            action=report.ValueBlock.from_dict,
            args=[report_factories.no_hash_id_value_block_data()],
            validate_attr="hash_id",
            assertion=Assert.NOT_EQUAL,
            expected=report_factories.value_block_kwargs()["hash_id"]),
])
def test_hash_id(testspec: TestSpec) -> None:
   """Test ValueBlock hash_id property."""
   testspec.run()


@pytest.mark.parametrize('testspec', [
    PytestAction('TO_DICT_001',
        name='ValueBlock to_dict returns a report.ValueBlockDict TypedDict mimic',
        action=is_typed_dict_mimic,
        args=[report_factories.value_block().to_dict(), report.ValueBlockDict],
        assertion=Assert.TRUE
    ),
    PytestAction('TO_DICT_002',
        name='ValueBlock to_dict returns a report.ImmutableValueBlockDict TypedDict mimic',
        action=is_typed_dict_mimic,
        args=[report_factories.value_block().to_dict(), report.ImmutableValueBlockDict],
        assertion=Assert.TRUE
    ),
])
def test_to_dict(testspec: TestSpec) -> None:
    """Test ValueBlock to_dict method."""
    testspec.run()


@pytest.mark.parametrize('testspec', [
    PytestAction('EQUALITY_001',
        name='ValueBlock equality comparison with identical hash_id values',
        action=lambda: report.ValueBlock(**report_factories.value_block_kwargs()),
        assertion=Assert.EQUAL,
        expected=report.ValueBlock(**report_factories.value_block_kwargs())
    ),
    PytestAction('EQUALITY_002',
        name='ValueBlock equality comparison with different hash_id values',
        action=lambda: report.ValueBlock(**report_factories.value_block_kwargs()),
        assertion=Assert.NOT_EQUAL,
        expected=report.ValueBlock(**report_factories.value_block_kwargs().replace(hash_id='d' * 64))
    ),
    PytestAction('EQUALITY_003',
        name=('ValueBlock equality comparison with different timer value and '
            'calculated hash_id (hash_id not provided)'),
        action=lambda: report.ValueBlock(**report_factories.value_block_kwargs() - {'hash_id'}),
        assertion=Assert.NOT_EQUAL,
        expected=report.ValueBlock(
            **report_factories.value_block_kwargs().replace(timer='other') - {'hash_id'})
    ),
    PytestAction('EQUALITY_004',
        name='ValueBlock equality comparison with same values and calculated hash_id (hash_id not provided)',
        action=lambda: report.ValueBlock(**report_factories.value_block_kwargs() - {'hash_id'}),
        assertion=Assert.EQUAL,
        expected=report.ValueBlock(**report_factories.value_block_kwargs() - {'hash_id'})
    ),
    PytestAction('EQUALITY_005',
        name='ValueBlock equality comparison with different types (not a ValueBlock instance)',
        action=lambda: report.ValueBlock(**report_factories.value_block_kwargs()),
        assertion=Assert.NOT_EQUAL,
        expected="Not a ValueBlock instance"
    ),
])
def test_equality(testspec: TestSpec) -> None:
    """Test ValueBlock equality comparison."""
    testspec.run()


def test_repr() -> None:
    """Test ValueBlock __repr__ method."""
    info = report_factories.value_block()
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
        name='ValueBlock instances with identical hash_id values have the same hash',
        action=hash,
        args=[report.ValueBlock(**report_factories.value_block_kwargs())],
        assertion=Assert.EQUAL,
        expected=hash(report.ValueBlock(**report_factories.value_block_kwargs()))
    ),
    PytestAction('HASH_002',
        name='ValueBlock instances with different values have different hashes',
        action=hash,
        args=[report.ValueBlock(**report_factories.value_block_kwargs() - {'hash_id'})],
        assertion=Assert.NOT_EQUAL,
        expected=hash(report.ValueBlock(
            **report_factories.value_block_kwargs().replace(timer='other')- {'hash_id'}))
    ),
])
def test_hash(testspec: TestSpec) -> None:
    """Test ValueBlock __hash__ method."""
    testspec.run()


@pytest.mark.parametrize('testspec', [
    PytestAction('PICKLE_001',
        name='ValueBlock instance can be pickled and unpickled correctly',
        action=lambda: pickle.loads(pickle.dumps(report_factories.value_block())),
        assertion=Assert.EQUAL,
        expected=report_factories.value_block()
    ),
])
def test_pickling(testspec: TestSpec) -> None:
    """Test that ValueBlock instances can be pickled and unpickled correctly."""
    testspec.run()


@pytest.mark.parametrize('testspec', [
    PytestAction('IMMUTABILITY_001',
        name='ValueBlock instance is immutable (attempting to set an attribute raises an exception)',
        action=lambda: setattr(report_factories.value_block(), 'timer', 'other'),
        exception=AttributeError
    ),
    PytestAction('IMMUTABILITY_002',
        name='ValueBlock instance is immutable (is_immutable returns True)',
        action=lambda: is_immutable(report_factories.value_block()),
        assertion=Assert.TRUE
    ),
])
def test_immutability(testspec: TestSpec) -> None:
    """Test that ValueBlock instances are immutable."""
    testspec.run()


@pytest.mark.parametrize('testspec', [
    PytestAction('SCHEMA_001',
        name='ValueBlock JSON schema is valid and can validate to_dict() output',
        action=validate,
        kwargs={
            'instance': report_factories.value_block().to_dict().thaw(),  # type: ignore
            'schema': report.ValueBlock.SCHEMA.as_dict()
        }
    ),
])
def test_json_schema(testspec: TestSpec) -> None:
    """Test that the JSON schema for ValueBlock is valid and can be
    used to validate a ValueBlock instance's to_dict() output."""
    testspec.run()


@pytest.mark.parametrize('testspec', [
    PytestAction('COPY_001',
        name='Copying a ValueBlock instance returns the same instance (since it is immutable)',
        action=copy,
        args=[report_factories.value_block()],
        assertion=Assert.IS,
        expected=report_factories.value_block()
    ),
    PytestAction('DEEP_COPY_001',
        name='Deep copying a ValueBlock instance returns the same instance (since it is immutable)',
        action=deepcopy,
        args=[report_factories.value_block()],
        assertion=Assert.IS,
        expected=report_factories.value_block()
    ),
])
def test_copy(testspec: TestSpec) -> None:
    """Test that copying a ValueBlock instance returns the same instance (since it is immutable)."""
    testspec.run()

# TODO: Add test for round-trip JSON serialization and deserialization of ValueBlock once a from_json method is
# implemented.
@pytest.mark.parametrize('testspec', [
     PytestAction('JSON_SERIALIZATION_001',
         name='ValueBlock can be serialized to JSON',
         action=report_factories.value_block().as_json,
         assertion=Assert.ISINSTANCE,
         expected=str),
    PytestAction('JSON_SERIALIZATION_002',
        name='ValueBlock can be directly serialized to a JSON compatible dictionary by simplejson',
        action=simplejson.dumps,
        kwargs={"obj": report_factories.value_block(),
                "sort_keys": True, "for_json": True, "iterable_as_array": True},
        assertion=Assert.ISINSTANCE,
        expected=str),
    PytestAction('JSON_SERIALIZATION_003',
            name='ValueBlock.for_json() can serialized to a JSON string by json.dumps',
            action=json.dumps,
            kwargs={"obj": report_factories.value_block().for_json(), "sort_keys": True},
            assertion=Assert.ISINSTANCE,
            expected=str),
 ])
def test_json_serialization(testspec: TestSpec) -> None:
    """Test that ValueBlock can be serialized to JSON."""
    testspec.run()

if __name__ == "__main__":
    pytest.main([__file__])
