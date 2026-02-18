"""Tests for the MetricsObject implementation in the V1 JSON report schema."""
# ruff: noqa: F401
import json
import pickle
from collections.abc import Iterator
from copy import copy, deepcopy

import pytest
import simplejson
from testspec import Assert, PytestAction, TestSpec

from simplebench.exceptions import (
    SimpleBenchAttributeError,
    SimpleBenchKeyError,
    SimpleBenchTypeError,
    SimpleBenchValueError,
)
from simplebench.report._error_tags import _MetricsErrorTag
from simplebench.report.versions import v1 as report
from simplebench.report.versions.v1 import MetricsObject, RawDataBlock, StatsBlock, ValueBlock
from simplebench.simplebench_types import CoreDataMapping, Values, is_immutable
from simplebench.validators import _ValidatorsErrorTag, is_typed_dict_mimic
from simplebench_tests.factories.report import v1 as report_factories


@pytest.mark.parametrize('testspec', [
    PytestAction("INIT_001",
        name="Valid MetricsObject initialization",
        action=MetricsObject,
        args=[{'test::valueblock': report_factories.value_block(),
               'test::statsblock': report_factories.stats_block(),
               'test::rawdatablock': report_factories.raw_data_block()}],
        assertion=Assert.ISINSTANCE,
        expected=MetricsObject),
    PytestAction("INIT_002",
        name="Invalid MetricsObject initialization with non-metric item",
        action=MetricsObject,
        args=[{'test::invaliditem': 'not a metric item'}],
        exception=SimpleBenchTypeError,
        exception_tag=_MetricsErrorTag.INVALID_METRIC_ITEM_TYPE
        ),
    PytestAction("INIT_003",
        name="Invalid key type in MetricsObject initialization",
        action=MetricsObject,
        args=[{123: report_factories.value_block()}],
        exception=SimpleBenchTypeError,
        exception_tag=_ValidatorsErrorTag.INVALID_NAMESPACED_IDENTIFIER_TYPE),
    PytestAction("INIT_004",
        name="Invalid key format in MetricsObject initialization",
        action=MetricsObject,
        args=[{'invalidkey': report_factories.value_block()}],
        exception=SimpleBenchValueError,
        exception_tag=_ValidatorsErrorTag.INVALID_NAMESPACED_IDENTIFIER),
    PytestAction("INIT_005",
        name="Empty MetricsObject initialization",
        action=MetricsObject,
        args=[{}],
        assertion=Assert.ISINSTANCE,
        expected=MetricsObject),
])
def test_init(testspec: TestSpec) -> None:
    """Test that MetricsObject can be initialized with valid metric items."""
    testspec.run()


@pytest.mark.parametrize('testspec', [
    PytestAction('EQUALITY_001',
        name='MetricsObject equality comparison with identical values',
        action=MetricsObject,
        args=[{'test::valueblock': report_factories.value_block()}],
        assertion=Assert.EQUAL,
        expected=MetricsObject({'test::valueblock': report_factories.value_block()})
    ),
    PytestAction('EQUALITY_002',
        name='MetricsObject equality comparison with different values',
        action=MetricsObject,
        args=[{'test::valueblock': report_factories.value_block(),
               'test::statsblock': report_factories.stats_block()}],
        assertion=Assert.NOT_EQUAL,
        expected=MetricsObject({'test::valueblock': report_factories.value_block()})
    ),
    PytestAction('EQUALITY_003',
        name='MetricObject equality comparison with different types (not a MetricObject instance)',
        action=report_factories.metrics_object,
        assertion=Assert.NOT_EQUAL,
        expected="Not a MetricsObject instance"
    ),
])
def test_equality(testspec: TestSpec) -> None:
    """Test MetricObject equality comparison."""
    testspec.run()


def test_repr() -> None:
    """Test MetricsObject __repr__ method."""
    info = report_factories.metrics_object()
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
    PytestAction('PICKLE_001',
        name='MetricsObject instance can be pickled and unpickled correctly',
        action=lambda: pickle.loads(pickle.dumps(report_factories.metrics_object())),
        assertion=Assert.EQUAL,
        expected=report_factories.metrics_object()
    ),
])
def test_pickling(testspec: TestSpec) -> None:
    """Test that MetricsObject instances can be pickled and unpickled correctly."""
    testspec.run()


@pytest.mark.parametrize('testspec', [
    PytestAction("IMMUTABLE_001",
        name="Test immutability of metric items in MetricsObject",
        action=MetricsObject({'test::valueblock': report_factories.value_block()}).__setitem__,
        args=['test::valueblock', report_factories.value_block()],
        exception=SimpleBenchAttributeError,
        exception_tag=_MetricsErrorTag.METRICS_OBJECT_IMMUTABLE
    ),
    PytestAction("IMMUTABLE_002",
        name="Test Immutable subclassing of MetricsObject",
        action=is_immutable,
        args=[MetricsObject({'test::valueblock': report_factories.value_block()})],
        assertion=Assert.TRUE)
])
def test_immutable_metric_items(testspec: TestSpec) -> None:
    """Test that the metric items in MetricsObject are immutable after initialization."""
    testspec.run()


@pytest.mark.parametrize('testspec', [
    PytestAction('COPY_001',
        name='Copying a MetricsObject instance returns the same instance (since it is immutable)',
        action=copy,
        args=[report_factories.metrics_object()],
        assertion=Assert.IS,
        expected=report_factories.metrics_object()
    ),
    PytestAction('COPY_002',
        name='Deep copying a MetricsObject instance returns the same instance (since it is immutable)',
        action=deepcopy,
        args=[report_factories.metrics_object()],
        assertion=Assert.IS,
        expected=report_factories.metrics_object()
    ),
    PytestAction('COPY_003',
        name='Copying a MetricsObject instance with MetricsObject.copy returns the same instance',
        action=report_factories.metrics_object().copy,
        assertion=Assert.IS,
        expected=report_factories.metrics_object()
    ),
])
def test_copy(testspec: TestSpec) -> None:
    """Test that copying a MetricsObject instance returns the same instance (since it is immutable)."""
    testspec.run()


@pytest.mark.parametrize('testspec', [
    PytestAction("TO_DICT_001",
        name="Test to_dict method of MetricsObject",
        action=MetricsObject({'test::valueblock': report_factories.value_block()}).to_dict,
        assertion=Assert.EQUAL,
        expected=CoreDataMapping({'test::valueblock': report_factories.value_block().to_dict()})),  # type: ignore
])
def test_to_dict(testspec: TestSpec) -> None:
    """Test that MetricsObject can be converted to a dictionary correctly."""
    testspec.run()


@pytest.mark.parametrize('testspec', [
    PytestAction("FROM_DICT_001",
        name="Test from_dict class method of MetricsObject",
        action=MetricsObject.from_dict,
        args=[{
            'test::valueblock': report_factories.value_block().to_dict().thaw(),  # type: ignore
            'test::statsblock': report_factories.stats_block().to_dict().thaw(),  # type: ignore
            'test::rawdatablock': report_factories.raw_data_block().to_dict().thaw()  # type: ignore
            }],  # type: ignore
        assertion=Assert.EQUAL,
        expected=MetricsObject({
            'test::valueblock': report_factories.value_block(),
            'test::statsblock': report_factories.stats_block(),
            'test::rawdatablock': report_factories.raw_data_block()
        })
    ),
    PytestAction("FROM_DICT_002",
        name="Test from_dict with empty dictionary",
        action=MetricsObject.from_dict,
        args=[{}],
        assertion=Assert.EQUAL,
        expected=MetricsObject({})
    ),
     PytestAction("FROM_DICT_003",
        name="Test from_dict with invalid metric item type",
        action=MetricsObject.from_dict,
        args=[{'test::invaliditem': 'not a metric item'}],
        exception=SimpleBenchTypeError,
        exception_tag=_MetricsErrorTag.INVALID_METRIC_ITEM_TYPE
     ),
    PytestAction("FROM_DICT_004",
            name="Test from_dict with invalid key type",
            action=MetricsObject.from_dict,
            args=[{123: report_factories.value_block()}],
            exception=SimpleBenchTypeError,
            exception_tag=_MetricsErrorTag.INVALID_METRIC_NAME_TYPE
        ),
    PytestAction("FROM_DICT_005",
        name="Invalid type in from_dict input",
        action=MetricsObject.from_dict,
        args=[{'test::valueblock': {
            'hash_id': 'c' * 64,
            'type': 'SimpleBenchNotAValueBlock::V1',
            'version': report.ValueBlockSchema.VERSION,
            'semantic_type': 'test::value',
            'timer': 'test_timer',
            'unit': 'seconds',
            'scale': 1.0,
            'value': 123.456,}}],
        exception=SimpleBenchValueError,
        exception_tag=_MetricsErrorTag.INVALID_METRIC_ITEM_TYPE),
])
def test_from_dict(testspec: TestSpec) -> None:
    """Test that MetricsObject can be created from a dictionary correctly."""
    testspec.run()


@pytest.mark.parametrize('testspec', [
     PytestAction('JSON_SERIALIZATION_001',
         name='MetricsObject can be serialized to JSON',
         action=report_factories.metrics_object().as_json,
         assertion=Assert.ISINSTANCE,
         expected=str),
    PytestAction('JSON_SERIALIZATION_002',
        name='MetricsObject can be directly serialized to a JSON compatible dictionary by simplejson',
        action=simplejson.dumps,
        kwargs={"obj": report_factories.metrics_object(),
                "sort_keys": True, "for_json": True, "iterable_as_array": True},
        assertion=Assert.ISINSTANCE,
        expected=str),
    PytestAction('JSON_SERIALIZATION_003',
            name='MetricsObject.for_json() can serialized to a JSON string by json.dumps',
            action=json.dumps,
            kwargs={"obj": report_factories.metrics_object().for_json(), "sort_keys": True},
            assertion=Assert.ISINSTANCE,
            expected=str),
 ])
def test_json_serialization(testspec: TestSpec) -> None:
    """Test that MetricsObject can be serialized to JSON."""
    testspec.run()



@pytest.mark.parametrize('testspec', [
    PytestAction('GETITEM_001',
        name='__getitem__ returns the correct metric item',
        action=report_factories.metrics_object().__getitem__,
        args=['test::valueblock'],
        assertion=Assert.EQUAL,
        expected=report_factories.value_block()
    ),
    PytestAction('GETITEM_002',
        name='__getitem__ with non-existent key raises KeyError',
        action=report_factories.metrics_object().__getitem__,
        args=['nonexistent::key'],
        exception=SimpleBenchKeyError,
        exception_tag=_MetricsErrorTag.KEY_ERROR_INVALID_METRIC_NAME_VALUE
    ),
])
def test_getitem(testspec: TestSpec) -> None:
    """Test various dunder methods of MetricsObject."""
    testspec.run()


@pytest.mark.parametrize('testspec', [
    PytestAction('SETITEM_001',
        name='__setitem__ raises an exception since MetricsObject is immutable',
        action=report_factories.metrics_object().__setitem__,
        args=['test::valueblock', report_factories.value_block()],
        exception=SimpleBenchAttributeError,
        exception_tag=_MetricsErrorTag.METRICS_OBJECT_IMMUTABLE
    ),
])
def test_setitem(testspec: TestSpec) -> None:
    """Test that __setitem__ raises an exception since MetricsObject is immutable."""
    testspec.run()

@pytest.mark.parametrize('testspec', [
    PytestAction('DELITEM_001',
        name='__delitem__ raises an exception since MetricsObject is immutable',
        action=report_factories.metrics_object().__delitem__,
        args=['test::valueblock'],
        exception=SimpleBenchAttributeError,
        exception_tag=_MetricsErrorTag.METRICS_OBJECT_IMMUTABLE
    ),
])
def test_delitem(testspec: TestSpec) -> None:
    """Test that __delitem__ raises an exception since MetricsObject is immutable."""
    testspec.run()


@pytest.mark.parametrize('testspec', [
    PytestAction('ITER_001',
        name='__iter__ returns an iterator over the metric items in MetricsObject',
        action=report_factories.metrics_object().__iter__,
        assertion=Assert.ISINSTANCE,
        expected=Iterator
    ),
    PytestAction('ITER_002',
        name='Iterating over MetricsObject yields the correct metric items',
        action=lambda: set(report_factories.metrics_object()),
        assertion=Assert.EQUAL,
        expected={'test::valueblock', 'test::statsblock', 'test::rawdatablock'}
    ),
])
def test_iter(testspec: TestSpec) -> None:
    """Test that iterating over MetricsObject yields an iterator."""
    testspec.run()


@pytest.mark.parametrize('testspec', [
    PytestAction('LEN_001',
        name='__len__ returns the correct number of metric items in MetricsObject',
        action=report_factories.metrics_object().__len__,
        assertion=Assert.EQUAL,
        expected=3
    ),
])
def test_len(testspec: TestSpec) -> None:
    """Test that __len__ returns the correct number of metric items in MetricsObject."""
    testspec.run()


@pytest.mark.parametrize('testspec', [
    PytestAction('CONTAINS_001',
        name='__contains__ returns True for existing metric item keys',
        action=lambda: 'test::valueblock' in report_factories.metrics_object(),
        assertion=Assert.TRUE
    ),
    PytestAction('CONTAINS_002',
        name='__contains__ returns False for non-existent metric item keys',
        action=lambda: 'nonexistent::key' in report_factories.metrics_object(),
        assertion=Assert.FALSE
    ),
])
def test_contains(testspec: TestSpec) -> None:
    """Test that __contains__ returns the correct boolean value for metric item keys."""
    testspec.run()


@pytest.mark.parametrize('testspec', [
    PytestAction('OR_001',
        name='__or__ returns a new MetricsObject with combined metric items',
        action=lambda: (report_factories.metrics_object()
                         | MetricsObject({'test::additional': report_factories.value_block()})),
        assertion=Assert.EQUAL,
        expected=MetricsObject({
            'test::valueblock': report_factories.value_block(),
            'test::statsblock': report_factories.stats_block(),
            'test::rawdatablock': report_factories.raw_data_block(),
            'test::additional': report_factories.value_block()
        })
    ),
    PytestAction('OR_002',
        name='__or__ with non-MetricsObject returns NotImplemented',
        action=lambda: report_factories.metrics_object() | "Not a MetricsObject",
        exception=TypeError
    ),
])
def test_or(testspec: TestSpec) -> None:
    """Test that __or__ returns a new MetricsObject with combined metric items."""
    testspec.run()


@pytest.mark.parametrize('testspec', [
    PytestAction('ROR_001',
        name='__ror__ returns a new MetricsObject with combined metric items',
        action=MetricsObject({'test::additional': report_factories.value_block()}).__ror__,
        args=[report_factories.metrics_object()],
        assertion=Assert.EQUAL,
        expected=MetricsObject({
            'test::additional': report_factories.value_block(),
            'test::valueblock': report_factories.value_block(),
            'test::statsblock': report_factories.stats_block(),
            'test::rawdatablock': report_factories.raw_data_block()
        })
    ),
    PytestAction('ROR_002',
        name='__ror__ with non-MetricsObject returns NotImplemented',
        action=MetricsObject({'test::additional': report_factories.value_block()}).__ror__,
        args=["Not a MetricsObject"],
        expected=NotImplemented
    ),
])
def test_ror(testspec: TestSpec) -> None:
    """Test that __ror__ returns a new MetricsObject with combined metric items."""
    testspec.run()


@pytest.mark.parametrize('testspec', [
    PytestAction('IOR_001',
        name='__ior__ updates the MetricsObject with combined metric items',
        action=lambda: (report_factories.metrics_object().__ior__(
            MetricsObject({'test::additional': report_factories.value_block()}))),
        assertion=Assert.EQUAL,
        expected=NotImplemented  # Since MetricsObject is immutable, __ior__ should return NotImplemented
    ),
])
def test_ior(testspec: TestSpec) -> None:
    """Test that __ior__ returns NotImplemented."""
    testspec.run()


@pytest.mark.parametrize('testspec', [
    PytestAction('FROMKEYS_001',
        name='fromkeys class method returns NotImplemented',
        action=MetricsObject.fromkeys,
        args=[['test::key1', 'test::key2'], report_factories.value_block()],
        assertion=Assert.EQUAL,
        expected=NotImplemented  # Since MetricsObject is immutable, fromkeys should return NotImplemented
    ),
])
def test_fromkeys(testspec: TestSpec) -> None:
    """Test that fromkeys class method returns NotImplemented."""
    testspec.run()


@pytest.mark.parametrize('testspec', [
    PytestAction('HASH_001',
        name='__hash__ returns a consistent hash value for the same MetricsObject instance',
        action=hash,
        args=[report_factories.metrics_object()],
        assertion=Assert.EQUAL,
        expected=hash(report_factories.metrics_object())
    ),
    PytestAction('HASH_002',
        name='__hash__ returns different hash values for different MetricsObject instances',
        action=hash,
        args=[report_factories.metrics_object()],
        assertion=Assert.NOT_EQUAL,
        expected=hash(MetricsObject({'test::valueblock': report_factories.value_block()}))
    ),
])
def test_hash(testspec: TestSpec) -> None:
    """Test that __hash__ returns a consistent hash value for the same MetricsObject instance."""
    testspec.run()


if __name__ == "__main__":
    pytest.main([__file__])
