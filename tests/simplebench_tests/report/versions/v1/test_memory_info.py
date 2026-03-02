"""Tests for MemoryInfo report."""
import json
import pickle
from copy import copy, deepcopy

import pytest
import simplejson
from testspec import Assert, PytestAction, TestSpec

from simplebench.base._hydrator import _HydratorErrorTag
from simplebench.exceptions import SimpleBenchTypeError, SimpleBenchValueError
from simplebench.report._error_tags import _MemoryInfoErrorTag
from simplebench.report.versions import v1 as report
from simplebench.validators import is_typed_dict_mimic
from simplebench_tests.factories.report import v1 as report_factories


@pytest.mark.parametrize("testspec", [
    PytestAction('INIT_001',
        name="Test good all argument MemoryInfo initialization",
        action=report.MemoryInfo,
        kwargs=report_factories.memory_info_kwargs(),
        assertion=Assert.ISINSTANCE,
        expected=report.MemoryInfo),
    PytestAction('INIT_002',
        name="Test missing hash_id argument MemoryInfo initialization",
        action=report.MemoryInfo,
        kwargs=report_factories.memory_info_kwargs() - {"hash_id"},
        assertion=Assert.ISINSTANCE,
        expected=report.MemoryInfo),
    PytestAction('INIT_003',
        name="Test missing swap_memory argument MemoryInfo initialization",
        action=report.MemoryInfo,
        kwargs=report_factories.memory_info_kwargs() - {"swap_memory"},
        exception=TypeError),
    PytestAction('INIT_004',
        name="Test missing used argument MemoryInfo initialization",
        action=report.MemoryInfo,
        kwargs=report_factories.memory_info_kwargs() - {"virtual_memory"},
        exception=TypeError),
    PytestAction('INIT_005',
        name="Test wrong type hash_id argument MemoryInfo initialization",
        action=report.MemoryInfo,
        kwargs=report_factories.memory_info_kwargs().replace(hash_id=12345),
        exception=SimpleBenchTypeError,
        exception_tag=_MemoryInfoErrorTag.INVALID_HASH_ID_TYPE),
    PytestAction('INIT_006',
        name="Test wrong value hash_id argument MemoryInfo initialization",
        action=report.MemoryInfo,
        kwargs=report_factories.memory_info_kwargs().replace(hash_id="not a valid hash id"),
        exception=SimpleBenchValueError,
        exception_tag=_MemoryInfoErrorTag.INVALID_HASH_ID_VALUE),
    PytestAction('INIT_007',
        name="Test wrong type swap_memory argument MemoryInfo initialization",
        action=report.MemoryInfo,
        kwargs=report_factories.memory_info_kwargs().replace(
            swap_memory="not a SwapMemoryObject"),
        exception=SimpleBenchTypeError,
        exception_tag=_MemoryInfoErrorTag.INVALID_SWAP_MEMORY_TYPE),
    PytestAction('INIT_008',
        name="Test wrong type virtual_memory argument MemoryInfo initialization",
        action=report.MemoryInfo,
        kwargs=report_factories.memory_info_kwargs().replace(
            virtual_memory="not a VirtualMemoryObject"),
        exception=SimpleBenchTypeError,
        exception_tag=_MemoryInfoErrorTag.INVALID_VIRTUAL_MEMORY_TYPE),
])
def test_init(testspec: TestSpec) -> None:
    """Test the initialization of MemoryInfo."""
    testspec.run()


@pytest.mark.parametrize("testspec", [
    PytestAction('FROM_DICT_001',
        name="Test from_dict method with valid dictionary",
        action=report.MemoryInfo.from_dict,
        args=[report_factories.memory_info_data()],
        assertion=Assert.EQUAL,
        expected=report_factories.memory_info()),
    PytestAction('FROM_DICT_002',
        name="Test from_dict method with missing keys in dictionary",
        action=report.MemoryInfo.from_dict,
        args=[{'hash_id': 'a' * 64,
               'swap_memory': report_factories.swap_memory_object_dict()}],
        exception=SimpleBenchValueError,
        exception_tag=_HydratorErrorTag.INVALID_DATA_KEY),
    PytestAction('FROM_DICT_003',
        name="Test from_dict method with wrong type values in dictionary",
        action=report.MemoryInfo.from_dict,
        args=[{'hash_id': 'a' * 64,
               'swap_memory': report_factories.swap_memory_object_dict(),
               'virtual_memory': "not a VirtualMemoryObjectDict"}],
        exception=SimpleBenchTypeError,
        exception_tag=_HydratorErrorTag.INVALID_DATA_TYPE),
])
def test_from_dict(testspec: TestSpec) -> None:
    """Test the from_dict method of MemoryInfo."""
    testspec.run()


@pytest.mark.parametrize(
    "testspec", [
        PytestAction(
            "PICKLE_001",
            name="Pickle and unpickle MemoryInfo instance preserves equality",
            action=pickle.loads,
            args=[pickle.dumps(report_factories.memory_info())],
            assertion=Assert.EQUAL,
            expected=report_factories.memory_info(),
        ),
        PytestAction(
            "PICKLE_002",
            name="Pickle and unpickle MemoryInfo preserves hash_id",
            action=pickle.loads,
            args=[pickle.dumps(report_factories.memory_info())],
            validate_attr="hash_id",
            assertion=Assert.EQUAL,
            expected=report_factories.memory_info().hash_id,
        ),
    ]
)
def test_pickle(testspec: TestSpec) -> None:
    """Test pickling and unpickling of MemoryInfo."""
    testspec.run()


@pytest.mark.parametrize(
    "testspec", [
        PytestAction(
            "EQUALITY_001",
            name="MemoryInfo instances with same data are equal",
            action=report.MemoryInfo,
            kwargs=report_factories.memory_info_kwargs(),
            assertion=Assert.EQUAL,
            expected=report.MemoryInfo(**report_factories.memory_info_kwargs())),
        PytestAction(
            "EQUALITY_002",
            name="MemoryInfo instances with different data are not equal",
            action=report.MemoryInfo,
            kwargs=report_factories.memory_info_kwargs().replace(
                swap_memory=report.SwapMemoryObject(
                    **report_factories.swap_memory_kwargs().replace(swap_in=1))) - {"hash_id"},
            assertion=Assert.NOT_EQUAL,
            expected=report.MemoryInfo(**(report_factories.memory_info_kwargs() - {"hash_id"}))),
        PytestAction(
            "EQUALITY_003",
            name="MemoryInfo compared to non-MemoryInfo is not equal",
            action=report_factories.memory_info,
            assertion=Assert.NOT_EQUAL,
            expected="not_a_memory_info_instance"),
    ]
)
def test_equality(testspec: TestSpec) -> None:
    testspec.run()


@pytest.mark.parametrize(
      "testspec", [
         PytestAction("HASH_ID_001",
            name="Test valid hash_id value",
            action=report_factories.memory_info,
            validate_attr="hash_id",
            assertion=Assert.LEN,
            expected=64),
         PytestAction("HASH_ID_002",
            name="Test hash_id value is consistent across instances with same data",
            action=report_factories.memory_info,
            validate_attr="hash_id",
            assertion=Assert.EQUAL,
            expected=report.MemoryInfo(**report_factories.memory_info_kwargs()).hash_id),
        PytestAction("HASH_ID_003",
            name="Test hash_id value is different for instances with different data",
            action=report.MemoryInfo,
            kwargs=report_factories.memory_info_kwargs().replace(
                swap_memory=report.SwapMemoryObject(
                    **report_factories.swap_memory_kwargs().replace(swap_in=1))),
            validate_attr="hash_id",
            assertion=Assert.NOT_EQUAL,
            expected=report.MemoryInfo(**(report_factories.memory_info_kwargs() - {"hash_id"})).hash_id),
      ]
   )
def test_hash_id(testspec: TestSpec) -> None:
   """Test CPUInfo hash_id property."""
   testspec.run()


@pytest.mark.parametrize('testspec', [
    PytestAction('TO_DICT_001',
        name='MemoryInfo to_dict returns a report.MemoryInfoDict TypedDict mimic',
        action=is_typed_dict_mimic,
        args=[report_factories.memory_info().to_dict(), report.MemoryInfoDict],
        assertion=Assert.TRUE
    ),
    PytestAction('TO_DICT_002',
        name='MemoryInfo to_dict returns a report.ImmutableMemoryInfoDict TypedDict mimic',
        action=is_typed_dict_mimic,
        args=[report_factories.memory_info().to_dict(), report.ImmutableMemoryInfoDict],
        assertion=Assert.TRUE
    ),
])
def test_to_dict(testspec: TestSpec) -> None:
    """Test MemoryInfo to_dict method."""
    testspec.run()


@pytest.mark.parametrize('testspec', [
    PytestAction('COPY_001',
        name='Copying a MemoryInfo instance returns the same instance (since it is immutable)',
        action=copy,
        args=[report_factories.memory_info()],
        assertion=Assert.IS,
        expected=report_factories.memory_info()
    ),
    PytestAction('DEEP_COPY_001',
        name='Deep copying a MemoryInfo instance returns the same instance (since it is immutable)',
        action=deepcopy,
        args=[report_factories.memory_info()],
        assertion=Assert.IS,
        expected=report_factories.memory_info()
    ),
])
def test_copy(testspec: TestSpec) -> None:
    """Test that copying a MemoryInfo instance returns the same instance (since it is immutable)."""
    testspec.run()


@pytest.mark.parametrize('testspec', [
    PytestAction('HASH_001',
        name='MemoryInfo instances with identical values have the same hash',
        action=hash,
        args=[report_factories.memory_info()],
        assertion=Assert.EQUAL,
        expected=hash(
            report.MemoryInfo(**report_factories.memory_info_kwargs()))),
    PytestAction('HASH_002',
        name='MemoryInfo instances with different values have different hashes',
        action=hash,
        args=[report_factories.memory_info()],
        assertion=Assert.NOT_EQUAL,
        expected=hash(
            report.MemoryInfo(**report_factories.memory_info_kwargs().replace(
                swap_memory=report.SwapMemoryObject(
                    **report_factories.swap_memory_kwargs().replace(swap_in=1))) - {"hash_id"}))),
])
def test_hash(testspec: TestSpec) -> None:
    """Test MemoryInfo __hash__ method."""
    testspec.run()

# TODO: Add test for round-trip JSON serialization and deserialization of MemoryInfo once a from_json method is
# implemented.
@pytest.mark.parametrize('testspec', [
     PytestAction('JSON_SERIALIZATION_001',
         name='MemoryInfo can be serialized to JSON string by report_memory_info().as_json method',
         action=report_factories.memory_info().as_json,
         assertion=Assert.ISINSTANCE,
         expected=str),
    PytestAction('JSON_SERIALIZATION_002',
        name='MemoryInfo can be directly serialized to a JSON compatible dictionary by simplejson',
        action=simplejson.dumps,
        kwargs={"obj": report_factories.memory_info(),
                "sort_keys": True, "for_json": True, "iterable_as_array": True},
        assertion=Assert.ISINSTANCE,
        expected=str),
    PytestAction('JSON_SERIALIZATION_003',
            name='MemoryInfo.for_json() can serialized to a JSON string by json.dumps',
            action=json.dumps,
            kwargs={"obj": report_factories.memory_info().for_json(), "sort_keys": True},
            assertion=Assert.ISINSTANCE,
            expected=str),
 ])
def test_json_serialization(testspec: TestSpec) -> None:
    """Test that MemoryInfo can be serialized to JSON."""
    testspec.run()


if __name__ == "__main__":
    pytest.main([__file__])
