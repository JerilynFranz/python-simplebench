"""Factories for report.v1.cpu_info."""
from functools import cache

from typeguard import check_type

from simplebench.report.versions import v1 as report
from simplebench_tests.kwargs.report.v1 import CPUInfoKWArgs


def cpu_info_kwargs() -> CPUInfoKWArgs:
    """CPUInfoKwargs factory for testing purposes.

    :return: A CPUInfoKwargs instance with dummy data.
    :rtype: CPUInfoKWArgs
    """
    return CPUInfoKWArgs(data=cpu_info_data())


@cache
def cpu_info() -> report.CPUInfo:
    """CPUInfo factory for testing purposes.

    The same instance is returned on subsequent calls since CPUInfo is immutable.

    :return: A CPUInfo instance with dummy data.
    :rtype: report.CPUInfo
    """
    return report.CPUInfo(**cpu_info_kwargs())

"""Factories for creating report CPUInfoData instances with dummy data for testing."""


def cpu_info_data() -> report.CPUInfoData:
    """CPUInfoData factory for testing purposes.

    :return: A CPUInfoData instance with dummy data.
    :rtype: report.CPUInfoData
    """
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

