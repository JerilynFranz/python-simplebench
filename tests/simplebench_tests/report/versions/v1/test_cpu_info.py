"""Tests for simplebench.report.versions.v1.cpu_info.CPUInfo class."""
# ruff: noqa: F401
import pickle

import autopypath  # noqa: F401
import pytest
from testspec import Assert, PytestAction, TestSpec
from typeguard import check_type

from simplebench import environment
from simplebench.exceptions import SimpleBenchTypeError, SimpleBenchValueError
from simplebench.report._error_tags import _CPUInfoErrorTag
from simplebench.report.versions import v1 as report
from simplebench.simplebench_types import CoreDataTypes


def dummy_cpu_info() -> report.CPUInfoData:
    """Dummy CPU info for testing purposes."""
    info = report.CPUInfoData(
        hash_id='b' * 64,
        data={
            "vendor": "GenuineIntel",
            "brand": "Intel(R) Core(TM) i7-8550U CPU @ 1.80GHz",
            "hz_advertised": "1.9980 GHz",
            "hz_actual": "2.0000 GHz",
            "arch": "x86_64",
            "bits": 64,
            "count_logical": 8,
            "count_physical": 4,
            "flags": [
                "fpu",
                "vme",
                "de",
                "pse",
                "tsc",
                "msr",
                "pae",
                "mce",
                "cx8",
                "apic",
            ],
        }
    )
    check_type(info, report.CPUInfoData)
    return info


def no_hash_id_dummy_cpu_info() -> report.CPUInfoData:
    """Dummy CPU info for testing purposes."""
    info = report.CPUInfoData(
        data={
            "vendor": "GenuineIntel",
            "brand": "Intel(R) Core(TM) i7-8550U CPU @ 1.80GHz",
            "hz_advertised": "1.9980 GHz",
            "hz_actual": "2.0000 GHz",
            "arch": "x86_64",
            "bits": 64,
            "count_logical": 8,
            "count_physical": 4,
            "flags": [
                "fpu",
                "vme",
                "de",
                "pse",
                "tsc",
                "msr",
                "pae",
                "mce",
                "cx8",
                "apic",
            ],
        }
    )
    check_type(info, report.CPUInfoData)
    return info


@pytest.mark.parametrize(
    "testspec",
    [
       PytestAction("INIT_001",
           name="Initialize CPUInfo with dummy data",
           action=report.CPUInfo.from_dict, args=[dummy_cpu_info()],
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
           action=report.CPUInfo, kwargs={"data": dummy_cpu_info(), "hash_id": "a"*64},
           validate_attr="hash_id",
           expected="a"*64),
        PytestAction("INIT_005",
           name="Initialize CPUInfo with invalid hash_id type",
           action=report.CPUInfo, kwargs={"data": dummy_cpu_info(), "hash_id": 12345},
           exception=SimpleBenchTypeError,
           exception_tag=_CPUInfoErrorTag.INVALID_HASH_ID_PROPERTY_TYPE),
        PytestAction("INIT_006",
           name="Initialize CPUInfo with invalid hash_id value",
           action=report.CPUInfo, kwargs={"data": dummy_cpu_info(), "hash_id": "invalid_hash"},
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
    "testspec",
    [
        PytestAction(
            "PICKLE_001",
            name="Pickle and unpickle CPUInfo instance preserves equality",
            action=lambda: pickle.loads(pickle.dumps(report.CPUInfo.from_dict(dummy_cpu_info()))),
            assertion=Assert.EQUAL,
            expected=report.CPUInfo.from_dict(dummy_cpu_info()),
        ),
        PytestAction(
            "PICKLE_002",
            name="Pickle and unpickle CPUInfo preserves hash_id",
            action=lambda: pickle.loads(pickle.dumps(report.CPUInfo.from_dict(dummy_cpu_info()))).hash_id,
            assertion=Assert.EQUAL,
            expected=report.CPUInfo.from_dict(dummy_cpu_info()).hash_id,
        ),
        PytestAction(
            "PICKLE_003",
            name="Pickle and unpickle CPUInfo preserves data",
            action=lambda: pickle.loads(pickle.dumps(report.CPUInfo.from_dict(dummy_cpu_info()))).data,
            assertion=Assert.EQUAL,
            expected=report.CPUInfo.from_dict(dummy_cpu_info()).data,
        ),
    ]
)
def test_pickle(testspec: TestSpec) -> None:
    """Test pickling and unpickling of CPUInfo."""
    testspec.run()


@pytest.mark.parametrize(
    "testspec",
    [
        PytestAction(
            "EQUALITY_001",
            name="CPUInfo instances with same data are equal",
            action=lambda: report.CPUInfo.from_dict(dummy_cpu_info()) == report.CPUInfo.from_dict(dummy_cpu_info()),
            assertion=Assert.TRUE,
        ),
        PytestAction(
            "EQUALITY_002",
            name="CPUInfo instances with different hash_id are not equal",
            action=lambda: report.CPUInfo.from_dict(dummy_cpu_info()) != report.CPUInfo.from_dict(
                report.CPUInfoData(
                    hash_id='c' * 64,
                    data=dummy_cpu_info()["data"]
                )
            ),
            assertion=Assert.FALSE,
        ),
        PytestAction(
            "EQUALITY_003",
            name="CPUInfo instances with different data are not equal",
            action=lambda: report.CPUInfo.from_dict(dummy_cpu_info()) != report.CPUInfo.from_dict(
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
    ]
)
def test_equality(testspec: TestSpec) -> None:
    testspec.run()



@pytest.mark.parametrize(
      "testspec",
      [
         PytestAction("HASH_ID_001",
            name="Test valid hash_id value through from_dict",
            action=report.CPUInfo.from_dict, args=[dummy_cpu_info()],
            validate_attr="hash_id",
            expected=dummy_cpu_info()["hash_id"]),  # type: ignore[index]
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

if __name__ == "__main__": # pragma: no cover
    pytest.main([__file__])
