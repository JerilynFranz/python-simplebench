"""Tests for simplebench.report.versions.v1.cpu_info.CPUInfo class."""
# ruff: noqa: F401
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
def test_cpu_info_init(testspec: TestSpec) -> None:
    """Test CPUInfo initialization."""
    testspec.run()
