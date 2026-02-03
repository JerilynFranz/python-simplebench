"""Tests for simplebench.report.versions.v1.cpu_info.CPUInfo class."""
# ruff: noqa: F401
import autopypath  # noqa: F401
from typeguard import check_type
import pytest
from testspec import Assert, PytestAction, TestAction, TestSpec, idspec

from simplebench import environment
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
           action=report.CPUInfo, kwargs={'data': environment.CPUInfo()},
           assertion=Assert.ISINSTANCE,
           expected=report.CPUInfo),
    ]
)
def test_cpu_info_init(testspec: TestSpec) -> None:
    """Test CPUInfo initialization."""
    testspec.run()
