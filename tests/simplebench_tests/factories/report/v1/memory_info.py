"""Factories for creating report CPUInfoData instances with dummy data for testing."""
from functools import cache

from simplebench.report.versions import v1 as report
from simplebench_tests.kwargs.report import v1 as report_kwargs


@cache
def swap_memory_kwargs() -> report_kwargs.SwapMemoryObjectKWArgs:
    """SwapMemoryObjectKWArgs factory for testing purposes.

    :return: A SwapMemoryObjectKWArgs instance with dummy data.
    :rtype: report_kwargs.SwapMemoryObjectKWArgs
    """
    return report_kwargs.SwapMemoryObjectKWArgs(**swap_memory_object_dict())


def swap_memory_object_dict() -> report.SwapMemoryObjectDict:
    """SwapMemoryObjectDict factory for testing purposes.

    :return: A SwapMemoryObjectDict instance with dummy data.
    :rtype: report.SwapMemoryObjectDict
    """
    return report.SwapMemoryObjectDict(
        total=1024,
        used=512,
        free=512,
        percent=50.0,
        swap_in=100,
        swap_out=100,
    )


@cache
def swap_memory_object() -> report.SwapMemoryObject:
    """SwapMemoryObject factory for testing purposes.

    :return: A SwapMemoryObject instance with dummy data.
    :rtype: report.SwapMemoryObject
    """
    return report.SwapMemoryObject(**swap_memory_kwargs())


@cache
def virtual_memory_kwargs() -> report_kwargs.VirtualMemoryObjectKWArgs:
    """VirtualMemoryObjectKWArgs factory for testing purposes.

    :return: A VirtualMemoryObjectKWArgs instance with dummy data.
    :rtype: report_kwargs.VirtualMemoryObjectKWArgs
    """
    return report_kwargs.VirtualMemoryObjectKWArgs(**virtual_memory_object_dict())


def virtual_memory_object_dict() -> report.VirtualMemoryObjectDict:
    """VirtualMemoryObjectDict factory for testing purposes.

    :return: A VirtualMemoryObjectDict instance with dummy data.
    :rtype: report.VirtualMemoryObjectDict
    """
    return report.VirtualMemoryObjectDict(
        total=1024,
        available=512,
        used=512,
        free=512,
        percent=50.0)


@cache
def virtual_memory_object() -> report.VirtualMemoryObject:
    """VirtualMemoryObject factory for testing purposes.

    :return: A VirtualMemoryObject instance with dummy data.
    :rtype: report.VirtualMemoryObject
    """
    return report.VirtualMemoryObject(**virtual_memory_kwargs())


@cache
def memory_info_kwargs() -> report_kwargs.MemoryInfoKWArgs:
    """MemoryInfoKWArgs factory for testing purposes.

    :return: A MemoryInfoKWArgs instance with dummy data.
    :rtype: report_kwargs.MemoryInfoKWArgs
    """
    kwargs = report_kwargs.MemoryInfoKWArgs(
        hash_id="e" * 64,
        swap_memory=swap_memory_object(),
        virtual_memory=virtual_memory_object()
    )
    return kwargs


def memory_info_data() -> report.MemoryInfoData:
    """MemoryInfoData factory for testing purposes.

    :return: A MemoryInfoData instance with dummy data.
    :rtype: report.MemoryInfoData
    """
    return report.MemoryInfoData(
        hash_id="e" * 64,
        version=report.MemoryInfo.VERSION,
        type=report.MemoryInfo.TYPE,
        swap_memory=swap_memory_object_dict(),
        virtual_memory=virtual_memory_object_dict()
    )


@cache
def memory_info() -> report.MemoryInfo:
    """Return MemoryInfoKWArgs with all fields set."""
    return report.MemoryInfo(**memory_info_kwargs())
