"""Tests for Swap Memory report."""
import json
import pickle
from copy import copy, deepcopy

import pytest
import simplejson
from testspec import Assert, PytestAction, TestSpec

from simplebench.base._hydrator import _HydratorErrorTag
from simplebench.exceptions import SimpleBenchTypeError, SimpleBenchValueError
from simplebench.report._error_tags import _SwapMemoryErrorTag
from simplebench.report.versions import v1 as report
from simplebench.validators import is_typed_dict_mimic
from simplebench_tests.factories.report import v1 as report_factories


@pytest.mark.parametrize("testspec", [
    PytestAction('INIT_001',
        name="Test good all argument SwapMemoryObject initialization",
        action=report.SwapMemoryObject,
        kwargs=report_factories.swap_memory_kwargs(),
        assertion=Assert.ISINSTANCE,
        expected=report.SwapMemoryObject),
    PytestAction('INIT_002',
        name="Test missing total argument SwapMemoryObject initialization",
        action=report.SwapMemoryObject,
        kwargs=report_factories.swap_memory_kwargs() - {"total"},
        exception=TypeError),
    PytestAction('INIT_003',
        name="Test missing used argument SwapMemoryObject initialization",
        action=report.SwapMemoryObject,
        kwargs=report_factories.swap_memory_kwargs() - {"used"},
        exception=TypeError),
    PytestAction('INIT_004',
        name="Test missing free argument SwapMemoryObject initialization",
        action=report.SwapMemoryObject,
        kwargs=report_factories.swap_memory_kwargs() - {"free"},
        exception=TypeError),
    PytestAction('INIT_005',
        name="Test missing percent argument SwapMemoryObject initialization",
        action=report.SwapMemoryObject,
        kwargs=report_factories.swap_memory_kwargs() - {"percent"},
        exception=TypeError),
    PytestAction('INIT_006',
        name="Test missing swap_in argument SwapMemoryObject initialization",
        action=report.SwapMemoryObject,
        kwargs=report_factories.swap_memory_kwargs() - {"swap_in"},
        exception=TypeError),
    PytestAction('INIT_007',
        name="Test missing swap_out argument SwapMemoryObject initialization",
        action=report.SwapMemoryObject,
        kwargs=report_factories.swap_memory_kwargs() - {"swap_out"},
        exception=TypeError),
    PytestAction('INIT_008',
        name="Test wrong type total argument SwapMemoryObject initialization",
        action=report.SwapMemoryObject,
        kwargs=report_factories.swap_memory_kwargs().replace(total="not an int"),
        exception=SimpleBenchTypeError,
        exception_tag=_SwapMemoryErrorTag.INVALID_TOTAL_TYPE),
    PytestAction('INIT_009',
        name="Test negative value total argument SwapMemoryObject initialization",
        action=report.SwapMemoryObject,
        kwargs=report_factories.swap_memory_kwargs().replace(total=-1),
        exception=SimpleBenchValueError,
        exception_tag=_SwapMemoryErrorTag.INVALID_TOTAL_VALUE),
    PytestAction('INIT_010',
        name="Test wrong type used argument SwapMemoryObject initialization",
        action=report.SwapMemoryObject,
        kwargs=report_factories.swap_memory_kwargs().replace(used="not an int"),
        exception=SimpleBenchTypeError,
        exception_tag=_SwapMemoryErrorTag.INVALID_USED_TYPE),
    PytestAction('INIT_011',
        name="Test negative value used argument SwapMemoryObject initialization",
        action=report.SwapMemoryObject,
        kwargs=report_factories.swap_memory_kwargs().replace(used=-1),
        exception=SimpleBenchValueError,
        exception_tag=_SwapMemoryErrorTag.INVALID_USED_VALUE),
    PytestAction('INIT_012',
        name="Test wrong type free argument SwapMemoryObject initialization",
        action=report.SwapMemoryObject,
        kwargs=report_factories.swap_memory_kwargs().replace(free="not an int"),
        exception=SimpleBenchTypeError,
        exception_tag=_SwapMemoryErrorTag.INVALID_FREE_TYPE),
    PytestAction('INIT_013',
        name="Test negative value free argument SwapMemoryObject initialization",
        action=report.SwapMemoryObject,
        kwargs=report_factories.swap_memory_kwargs().replace(free=-1),
        exception=SimpleBenchValueError,
        exception_tag=_SwapMemoryErrorTag.INVALID_FREE_VALUE),
    PytestAction('INIT_014',
        name="Test wrong type percent argument SwapMemoryObject initialization",
        action=report.SwapMemoryObject,
        kwargs=report_factories.swap_memory_kwargs().replace(percent="not a float"),
        exception=SimpleBenchTypeError,
        exception_tag=_SwapMemoryErrorTag.INVALID_SWAP_PERCENT_TYPE),
    PytestAction('INIT_015',
        name="Test out of range (>100) value percent argument SwapMemoryObject initialization",
        action=report.SwapMemoryObject,
        kwargs=report_factories.swap_memory_kwargs().replace(percent=150.0),
        exception=SimpleBenchValueError,
        exception_tag=_SwapMemoryErrorTag.INVALID_SWAP_PERCENT_OUT_OF_RANGE),
    PytestAction('INIT_016',
        name="Test out of range (<0) value percent argument SwapMemoryObject initialization",
        action=report.SwapMemoryObject,
        kwargs=report_factories.swap_memory_kwargs().replace(percent=-10.0),
        exception=SimpleBenchValueError,
        exception_tag=_SwapMemoryErrorTag.INVALID_SWAP_PERCENT_OUT_OF_RANGE),
    PytestAction('INIT_017',
        name="Test wrong type swap_in argument SwapMemoryObject initialization",
        action=report.SwapMemoryObject,
        kwargs=report_factories.swap_memory_kwargs().replace(swap_in="not an int"),
        exception=SimpleBenchTypeError,
        exception_tag=_SwapMemoryErrorTag.INVALID_SWAP_IN_TYPE),
    PytestAction('INIT_018',
        name="Test negative value swap_in argument SwapMemoryObject initialization",
        action=report.SwapMemoryObject,
        kwargs=report_factories.swap_memory_kwargs().replace(swap_in=-1),
        exception=SimpleBenchValueError,
        exception_tag=_SwapMemoryErrorTag.INVALID_SWAP_IN_VALUE),
    PytestAction('INIT_019',
        name="Test wrong type swap_out argument SwapMemoryObject initialization",
        action=report.SwapMemoryObject,
        kwargs=report_factories.swap_memory_kwargs().replace(swap_out="not an int"),
        exception=SimpleBenchTypeError,
        exception_tag=_SwapMemoryErrorTag.INVALID_SWAP_OUT_TYPE),
    PytestAction('INIT_020',
        name="Test negative value swap_out argument SwapMemoryObject initialization",
        action=report.SwapMemoryObject,
        kwargs=report_factories.swap_memory_kwargs().replace(swap_out=-1),
        exception=SimpleBenchValueError,
        exception_tag=_SwapMemoryErrorTag.INVALID_SWAP_OUT_VALUE),
])
def test_init(testspec: TestSpec) -> None:
    """Test the initialization of SwapMemoryObject."""
    testspec.run()


@pytest.mark.parametrize("testspec", [
    PytestAction('FROM_DICT_001',
        name="Test from_dict method with valid dictionary",
        action=report.SwapMemoryObject.from_dict,
        args=[report_factories.swap_memory_kwargs()],
        assertion=Assert.EQUAL,
        expected=report_factories.swap_memory_object()),
    PytestAction('FROM_DICT_002',
        name="Test from_dict method with missing keys in dictionary",
        action=report.SwapMemoryObject.from_dict,
        args=[report_factories.swap_memory_kwargs() - {"total"}],
        exception=SimpleBenchValueError,
        exception_tag=_HydratorErrorTag.INVALID_DATA_KEY,
        ),
    PytestAction('FROM_DICT_003',
        name="Test from_dict method with wrong type values in dictionary",
        action=report.SwapMemoryObject.from_dict,
        args=[report_factories.swap_memory_kwargs().replace(total="not an int")],
        exception=SimpleBenchTypeError,
        exception_tag=_HydratorErrorTag.INVALID_DATA_VALUE_TYPE),
])
def test_from_dict(testspec: TestSpec) -> None:
    """Test the from_dict method of SwapMemoryObject."""
    testspec.run()


@pytest.mark.parametrize(
    "testspec", [
        PytestAction(
            "PICKLE_001",
            name="Pickle and unpickle SwapMemoryObject instance preserves equality",
            action=pickle.loads,
            args=[pickle.dumps(report_factories.swap_memory_object())],
            assertion=Assert.EQUAL,
            expected=report_factories.swap_memory_object(),
        ),
        PytestAction(
            "PICKLE_002",
            name="Pickle and unpickle SwapMemoryObject preserves hash_id",
            action=pickle.loads,
            args=[pickle.dumps(report_factories.swap_memory_object())],
            validate_attr="hash_id",
            assertion=Assert.EQUAL,
            expected=report_factories.swap_memory_object().hash_id,
        ),
    ]
)
def test_pickle(testspec: TestSpec) -> None:
    """Test pickling and unpickling of SwapMemoryObject."""
    testspec.run()


@pytest.mark.parametrize(
    "testspec", [
        PytestAction(
            "EQUALITY_001",
            name="SwapMemoryObject instances with same data are equal",
            action=report.SwapMemoryObject,
            kwargs=report_factories.swap_memory_kwargs(),
            assertion=Assert.EQUAL,
            expected=report.SwapMemoryObject(**report_factories.swap_memory_kwargs())),
        PytestAction(
            "EQUALITY_002",
            name="SwapMemoryObject instances with different data are not equal",
            action=report.SwapMemoryObject,
            kwargs=report_factories.swap_memory_kwargs().replace(used=report_factories.swap_memory_object().used + 1),
            assertion=Assert.NOT_EQUAL,
            expected=report_factories.swap_memory_object()),
        PytestAction(
            "EQUALITY_003",
            name="SwapMemoryObject compared to non-SwapMemoryObject is not equal",
            action=report_factories.swap_memory_object,
            assertion=Assert.NOT_EQUAL,
            expected="not_a_swap_memory_instance"),
    ]
)
def test_equality(testspec: TestSpec) -> None:
    testspec.run()


@pytest.mark.parametrize(
      "testspec", [
         PytestAction("HASH_ID_001",
            name="Test valid hash_id value",
            action=report_factories.swap_memory_object,
            validate_attr="hash_id",
            assertion=Assert.LEN,
            expected=64),
         PytestAction("HASH_ID_002",
            name="Test hash_id value is consistent across instances with same data",
            action=report_factories.swap_memory_object,
            validate_attr="hash_id",
            assertion=Assert.EQUAL,
            expected=report.SwapMemoryObject(**report_factories.swap_memory_kwargs()).hash_id),
        PytestAction("HASH_ID_003",
            name="Test hash_id value is different for instances with different data",
            action=report.SwapMemoryObject,
            kwargs=report_factories.swap_memory_kwargs().replace(used=report_factories.swap_memory_object().used + 1),
            validate_attr="hash_id",
            assertion=Assert.NOT_EQUAL,
            expected=report_factories.swap_memory_object().hash_id),
      ]
   )
def test_hash_id(testspec: TestSpec) -> None:
   """Test CPUInfo hash_id property."""
   testspec.run()


@pytest.mark.parametrize('testspec', [
    PytestAction('TO_DICT_001',
        name='SwapMemoryObject to_dict returns a report.SwapMemoryObjectDict TypedDict mimic',
        action=is_typed_dict_mimic,
        args=[report_factories.swap_memory_object().to_dict(), report.SwapMemoryObjectDict],
        assertion=Assert.TRUE
    ),
    PytestAction('TO_DICT_002',
        name='SwapMemoryObject to_dict returns a report.ImmutableSwapMemoryObjectDict TypedDict mimic',
        action=is_typed_dict_mimic,
        args=[report_factories.swap_memory_object().to_dict(), report.ImmutableSwapMemoryObjectDict],
        assertion=Assert.TRUE
    ),
])
def test_to_dict(testspec: TestSpec) -> None:
    """Test SwapMemoryObject to_dict method."""
    testspec.run()


@pytest.mark.parametrize('testspec', [
    PytestAction('COPY_001',
        name='Copying a SwapMemoryObject instance returns the same instance (since it is immutable)',
        action=copy,
        args=[report_factories.swap_memory_object()],
        assertion=Assert.IS,
        expected=report_factories.swap_memory_object()
    ),
    PytestAction('DEEP_COPY_001',
        name='Deep copying a SwapMemoryObject instance returns the same instance (since it is immutable)',
        action=deepcopy,
        args=[report_factories.swap_memory_object()],
        assertion=Assert.IS,
        expected=report_factories.swap_memory_object()
    ),
])
def test_copy(testspec: TestSpec) -> None:
    """Test that copying a SwapMemoryObject instance returns the same instance (since it is immutable)."""
    testspec.run()


@pytest.mark.parametrize('testspec', [
    PytestAction('HASH_001',
        name='SwapMemoryObject instances with identical values have the same hash',
        action=hash,
        args=[report_factories.swap_memory_object()],
        assertion=Assert.EQUAL,
        expected=hash(
            report.SwapMemoryObject(**report_factories.swap_memory_kwargs()))),
    PytestAction('HASH_002',
        name='SwapMemoryObject instances with different values have different hashes',
        action=hash,
        args=[report_factories.swap_memory_object()],
        assertion=Assert.NOT_EQUAL,
        expected=hash(
            report.SwapMemoryObject(**report_factories.swap_memory_kwargs().replace(free=0)))),
])
def test_hash(testspec: TestSpec) -> None:
    """Test SwapMemoryObject __hash__ method."""
    testspec.run()

# TODO: Add test for round-trip JSON serialization and deserialization of SwapMemoryObject once a from_json method is
# implemented.
@pytest.mark.parametrize('testspec', [
     PytestAction('JSON_SERIALIZATION_001',
         name='SwapMemoryObject can be serialized to JSON string by report_swap_memory_object().as_json method',
         action=report_factories.swap_memory_object().as_json,
         assertion=Assert.ISINSTANCE,
         expected=str),
    PytestAction('JSON_SERIALIZATION_002',
        name='SwapMemoryObject can be directly serialized to a JSON compatible dictionary by simplejson',
        action=simplejson.dumps,
        kwargs={"obj": report_factories.swap_memory_object(),
                "sort_keys": True, "for_json": True, "iterable_as_array": True},
        assertion=Assert.ISINSTANCE,
        expected=str),
    PytestAction('JSON_SERIALIZATION_003',
            name='SwapMemoryObject.for_json() can serialized to a JSON string by json.dumps',
            action=json.dumps,
            kwargs={"obj": report_factories.swap_memory_object().for_json(), "sort_keys": True},
            assertion=Assert.ISINSTANCE,
            expected=str),
 ])
def test_json_serialization(testspec: TestSpec) -> None:
    """Test that SwapMemoryObject can be serialized to JSON."""
    testspec.run()


if __name__ == "__main__":
    pytest.main([__file__])
