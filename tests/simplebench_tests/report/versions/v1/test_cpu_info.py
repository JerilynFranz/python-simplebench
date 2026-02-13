"""Tests for simplebench.report.versions.v1.cpu_info.CPUInfo class."""
import json
import pickle
from copy import copy, deepcopy

import pytest
import simplejson
from jsonschema import validate
from testspec import Assert, PytestAction, TestSpec

from simplebench import environment
from simplebench.exceptions import SimpleBenchTypeError, SimpleBenchValueError
from simplebench.report._error_tags import _CPUInfoErrorTag
from simplebench.report.versions import v1 as report
from simplebench.validators import is_typed_dict_mimic
from simplebench_tests.factories.report import v1 as report_factories


def no_hash_id_dummy_cpu_info() -> report.CPUInfoData:
    """Dummy CPU info without hash_id for testing hash_id generation."""
    info = report_factories.report_cpu_info_data()
    del info["hash_id"]
    return info


@pytest.mark.parametrize(
    "testspec", [
       PytestAction("INIT_001",
           name="Initialize CPUInfo with dummy data",
           action=report.CPUInfo.from_dict, args=[report_factories.report_cpu_info_data()],
           assertion=Assert.ISINSTANCE,
           expected=report.CPUInfo),
        PytestAction("INIT_002",
           name="Initialize CPUInfo from environment.CPUInfo.to_dict() data",
           action=report.CPUInfo.from_dict, args=[environment.CPUInfo().to_dict()],
           assertion=Assert.ISINSTANCE,
           expected=report.CPUInfo),
        PytestAction("INIT_003",
           name="Initialize CPUInfo directly from environment.CPUInfo instance",
           action=report.CPUInfo, kwargs={"data": environment.CPUInfo()},
           assertion=Assert.ISINSTANCE,
           expected=report.CPUInfo),
        PytestAction("INIT_004",
           name="Initialize CPUInfo with forced hash_id",
           action=report.CPUInfo, kwargs={"data": report_factories.report_cpu_info_data(), "hash_id": "a"*64},
           validate_attr="hash_id",
           expected="a"*64),
        PytestAction("INIT_005",
           name="Initialize CPUInfo with invalid hash_id type",
           action=report.CPUInfo, kwargs={"data": report_factories.report_cpu_info_data(), "hash_id": 12345},
           exception=SimpleBenchTypeError,
           exception_tag=_CPUInfoErrorTag.INVALID_HASH_ID_PROPERTY_TYPE),
        PytestAction("INIT_006",
           name="Initialize CPUInfo with invalid hash_id value",
           action=report.CPUInfo, kwargs={"data": report_factories.report_cpu_info_data(), "hash_id": "invalid_hash"},
           exception=SimpleBenchValueError,
           exception_tag=_CPUInfoErrorTag.INVALID_HASH_ID_PROPERTY_VALUE),
        PytestAction("INIT_007",
           name="Initialize CPUInfo with invalid data type",
           action=report.CPUInfo, kwargs={"data": "not_a_dict"},
           exception=SimpleBenchTypeError,
           exception_tag=_CPUInfoErrorTag.INVALID_DATA_PROPERTY_TYPE),
    ]
)
def test_init(testspec: TestSpec) -> None:
    """Test CPUInfo initialization."""
    testspec.run()


@pytest.mark.parametrize(
    "testspec", [
        PytestAction(
            "PICKLE_001",
            name="Pickle and unpickle CPUInfo instance preserves equality",
            action=lambda: pickle.loads(
                pickle.dumps(report.CPUInfo.from_dict(report_factories.report_cpu_info_data()))),
            assertion=Assert.EQUAL,
            expected=report.CPUInfo.from_dict(report_factories.report_cpu_info_data()),
        ),
        PytestAction(
            "PICKLE_002",
            name="Pickle and unpickle CPUInfo preserves hash_id",
            action=lambda: pickle.loads(
                pickle.dumps(report.CPUInfo.from_dict(report_factories.report_cpu_info_data()))).hash_id,
            assertion=Assert.EQUAL,
            expected=report.CPUInfo.from_dict(report_factories.report_cpu_info_data()).hash_id,
        ),
        PytestAction(
            "PICKLE_003",
            name="Pickle and unpickle CPUInfo preserves data",
            action=lambda: pickle.loads(
                pickle.dumps(report.CPUInfo.from_dict(report_factories.report_cpu_info_data()))).data,
            assertion=Assert.EQUAL,
            expected=report.CPUInfo.from_dict(report_factories.report_cpu_info_data()).data,
        ),
    ]
)
def test_pickle(testspec: TestSpec) -> None:
    """Test pickling and unpickling of CPUInfo."""
    testspec.run()


@pytest.mark.parametrize(
    "testspec", [
        PytestAction(
            "EQUALITY_001",
            name="CPUInfo instances with same data are equal",
            action=lambda: report.CPUInfo.from_dict(
                report_factories.report_cpu_info_data()) == report.CPUInfo.from_dict(
                    report_factories.report_cpu_info_data()),
            assertion=Assert.TRUE,
        ),
        PytestAction(
            "EQUALITY_002",
            name="CPUInfo instances with different hash_id are not equal",
            action=lambda: report.CPUInfo.from_dict(
                report_factories.report_cpu_info_data()) != report.CPUInfo.from_dict(
                    report.CPUInfoData(
                        hash_id='c' * 64,
                        data=report_factories.report_cpu_info_data()["data"]
                    )
            ),
            assertion=Assert.FALSE,
        ),
        PytestAction(
            "EQUALITY_003",
            name="CPUInfo instances with different data are not equal",
            action=lambda: report.CPUInfo.from_dict(
                report_factories.report_cpu_info_data()) != report.CPUInfo.from_dict(
                    report.CPUInfoData(
                        hash_id='a' * 64,
                        data={
                            "vendor": "DifferentVendor",
                            "brand": "DifferentBrand",
                        }
                    )
            ),
            assertion=Assert.TRUE,
        ),
        PytestAction(
            "EQUALITY_004",
            name="CPUInfo compared to non-CPUInfo is not equal",
            action=report_factories.report_cpu_info,
            assertion=Assert.NOT_EQUAL,
            expected="not_a_cpu_info_instance")
    ]
)
def test_equality(testspec: TestSpec) -> None:
    testspec.run()


@pytest.mark.parametrize(
      "testspec", [
         PytestAction("HASH_ID_001",
            name="Test valid hash_id value through from_dict",
            action=report.CPUInfo.from_dict, args=[report_factories.report_cpu_info_data()],
            validate_attr="hash_id",
            expected=report_factories.report_cpu_info_data()["hash_id"]),  # type: ignore[index]
         PytestAction("HASH_ID_002",
            name="Test generated hash_id when not provided through from_dict",
            action=report.CPUInfo.from_dict, args=[no_hash_id_dummy_cpu_info()],
            validate_attr="hash_id",
            assertion=Assert.LEN,
            expected=64),
         PytestAction("HASH_ID_003",
            name="Test hash_id initialization with environment.CPUInfo instance without hash_id",
            action=report.CPUInfo, kwargs={"data": environment.CPUInfo()},
            validate_attr="hash_id",
            assertion=Assert.LEN,
            expected=64),
      ]
   )
def test_hash_id(testspec: TestSpec) -> None:
   """Test CPUInfo hash_id property."""
   testspec.run()


@pytest.mark.parametrize('testspec', [
    PytestAction('TO_DICT_001',
        name='CPUInfo to_dict returns a report.CPUInfoDict TypedDict mimic',
        action=is_typed_dict_mimic,
        args=[report_factories.report_cpu_info().to_dict(), report.CPUInfoDict],
        assertion=Assert.TRUE
    ),
    PytestAction('TO_DICT_002',
        name='CPUInfo to_dict returns a report.ImmutableCPUInfoDict TypedDict mimic',
        action=is_typed_dict_mimic,
        args=[report_factories.report_cpu_info().to_dict(), report.ImmutableCPUInfoDict],
        assertion=Assert.TRUE
    ),
])
def test_to_dict(testspec: TestSpec) -> None:
    """Test CPUInfo to_dict method."""
    testspec.run()


@pytest.mark.parametrize('testspec', [
    PytestAction('SCHEMA_001',
        name='CPUInfo JSON schema is valid and can validate to_dict() output',
        action=validate,
        kwargs={
            'instance': report_factories.report_cpu_info().to_dict().thaw(),  # type: ignore
            'schema': report.CPUInfo.SCHEMA.as_dict()
        }
    ),
])
def test_json_schema(testspec: TestSpec) -> None:
    """Test that the JSON schema for CPUInfo is valid and can be
    used to validate a CPUInfo instance's to_dict() output."""
    testspec.run()


@pytest.mark.parametrize('testspec', [
    PytestAction('COPY_001',
        name='Copying a CPUInfo instance returns the same instance (since it is immutable)',
        action=copy,
        args=[report_factories.report_cpu_info()],
        assertion=Assert.IS,
        expected=report_factories.report_cpu_info()
    ),
    PytestAction('DEEP_COPY_001',
        name='Deep copying a CPUInfo instance returns the same instance (since it is immutable)',
        action=deepcopy,
        args=[report_factories.report_cpu_info()],
        assertion=Assert.IS,
        expected=report_factories.report_cpu_info()
    ),
])
def test_copy(testspec: TestSpec) -> None:
    """Test that copying a CPUInfo instance returns the same instance (since it is immutable)."""
    testspec.run()


@pytest.mark.parametrize('testspec', [
    PytestAction('HASH_001',
        name='CPUInfo instances with identical hash_id values have the same hash',
        action=hash,
        args=[report.CPUInfo(**report_factories.report_cpu_info_kwargs())],
        assertion=Assert.EQUAL,
        expected=hash(report.CPUInfo(**report_factories.report_cpu_info_kwargs()))
    ),
    PytestAction('HASH_002',
        name='CPUInfo instances with different hash_id values have different hashes',
        action=hash,
        args=[report.CPUInfo(**report_factories.report_cpu_info_kwargs() - {'hash_id'})],
        assertion=Assert.NOT_EQUAL,
        expected=hash(report.CPUInfo.from_dict({'data': no_hash_id_dummy_cpu_info()}))  # type: ignore
    ),
])
def test_hash(testspec: TestSpec) -> None:
    """Test CPUInfo __hash__ method."""
    testspec.run()

# TODO: Add test for round-trip JSON serialization and deserialization of CPUInfo once a from_json method is
# implemented.
@pytest.mark.parametrize('testspec', [
     PytestAction('JSON_SERIALIZATION_001',
         name='CPUInfo can be serialized to JSON string by report_cpu_info().as_json method',
         action=report_factories.report_cpu_info().as_json,
         assertion=Assert.ISINSTANCE,
         expected=str),
    PytestAction('JSON_SERIALIZATION_002',
        name='CPUInfo can be directly serialized to a JSON compatible dictionary by simplejson',
        action=simplejson.dumps,
        kwargs={"obj": report_factories.report_cpu_info(),
                "sort_keys": True, "for_json": True, "iterable_as_array": True},
        assertion=Assert.ISINSTANCE,
        expected=str),
    PytestAction('JSON_SERIALIZATION_003',
            name='CPUInfo.for_json() can serialized to a JSON string by json.dumps',
            action=json.dumps,
            kwargs={"obj": report_factories.report_cpu_info().for_json(), "sort_keys": True},
            assertion=Assert.ISINSTANCE,
            expected=str),
 ])
def test_json_serialization(testspec: TestSpec) -> None:
    """Test that CPUInfo can be serialized to JSON."""
    testspec.run()


if __name__ == "__main__": # pragma: no cover
    pytest.main([__file__])
