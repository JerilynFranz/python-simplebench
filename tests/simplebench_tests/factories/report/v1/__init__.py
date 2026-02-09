"""Factories for creating report CPUInfoData instances with dummy data for testing."""

from typeguard import check_type

from simplebench.report.versions import v1 as report
from simplebench_tests.kwargs.report import v1 as report_kwargs

def report_cpu_info_data() -> report.CPUInfoData:
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


def swap_memory_kwargs_factory() -> report_kwargs.SwapMemoryObjectKWArgs:
    """SwapMemoryObjectKWArgs factory for testing purposes.

    :return: A SwapMemoryObjectKWArgs instance with dummy data.
    :rtype: report_kwargs.SwapMemoryObjectKWArgs
    """
    return report_kwargs.SwapMemoryObjectKWArgs(
        total=1024,
        used=512,
        free=512,
        percent=50.0,
        swap_in=100,
        swap_out=100,
    )


def swap_memory_object_factory() -> report.SwapMemoryObject:
    """SwapMemoryObject factory for testing purposes.

    :return: A SwapMemoryObject instance with dummy data.
    :rtype: report.SwapMemoryObject
    """
    return report.SwapMemoryObject(**swap_memory_kwargs_factory())


def virtual_memory_kwargs_factory() -> report_kwargs.VirtualMemoryObjectKWArgs:
    """VirtualMemoryObjectKWArgs factory for testing purposes.

    :return: A VirtualMemoryObjectKWArgs instance with dummy data.
    :rtype: report_kwargs.VirtualMemoryObjectKWArgs
    """
    kwargs = report_kwargs.VirtualMemoryObjectKWArgs(
        total=1024,
        available=512,
        used=512,
        free=512,
        percent=50.0,
    )
    return kwargs


def virtual_memory_object_factory() -> report.VirtualMemoryObject:
    """VirtualMemoryObject factory for testing purposes.

    :return: A VirtualMemoryObject instance with dummy data.
    :rtype: report.VirtualMemoryObject
    """
    return report.VirtualMemoryObject(**virtual_memory_kwargs_factory())


def memory_info_kwargs_factory() -> report_kwargs.MemoryInfoKWArgs:
    """MemoryInfoKWArgs factory for testing purposes.

    :return: A MemoryInfoKWArgs instance with dummy data.
    :rtype: report_kwargs.MemoryInfoKWArgs
    """
    kwargs = report_kwargs.MemoryInfoKWArgs(
        hash_id="test_hash_id",
        swap_memory=swap_memory_object_factory(),
        virtual_memory=virtual_memory_object_factory()
    )
    return kwargs


def memory_info_factory() -> report.MemoryInfo:
    """Return MemoryInfoKWArgs with all fields set."""
    return report.MemoryInfo(**memory_info_kwargs_factory())
