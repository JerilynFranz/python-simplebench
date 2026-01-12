"""Tests for simplebench.report.versions.v1.cpu_info.CPUInfo class."""
import pytest

from simplebench.environment._cpu_info._cpu_info import CPUInfo as EnvCPUInfo
from simplebench.report.versions.v1.cpu_info import CPUInfo as ReportCPUInfo

from ....testspec import Assert, TestAction, TestSpec, idspec


def dummy_cpu_info() -> dict[str, str | int | list[str]]:
    """Dummy CPU info for testing purposes."""
    return {
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



@pytest.mark.parametrize(
    "testspec",
    [
       idspec("INIT_001", TestAction(
           name="Initialize CPUInfo with dict data",
           action=ReportCPUInfo,
           kwargs={"data": dummy_cpu_info()},
           assertion=Assert.ISINSTANCE,
           expected=ReportCPUInfo)),
        idspec("INIT_002", TestAction(
           name="Initialize CPUInfo from environment.CPUInfo.info property",
           action=ReportCPUInfo,
           kwargs={"data": EnvCPUInfo().info},
           assertion=Assert.ISINSTANCE,
           expected=ReportCPUInfo)),
        idspec("INIT_003", TestAction(
           name="Initialize CPUInfo directly from environment.CPUInfo instance",
           action=ReportCPUInfo,
           kwargs={"data": EnvCPUInfo()},
           assertion=Assert.ISINSTANCE,
           expected=ReportCPUInfo)),
    ]
)
def test_cpu_info_init(testspec: TestSpec) -> None:
    """Test CPUInfo initialization."""
    testspec.run()
