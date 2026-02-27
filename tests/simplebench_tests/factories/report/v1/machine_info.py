"""Factories for creating report CPUInfoData instances with dummy data for testing."""
# ruff: noqa: F401
from functools import cache

from simplebench.report.versions import v1 as report
from simplebench_tests.kwargs.report import v1 as report_kwargs

from .cpu_info import cpu_info, cpu_info_data
from .environment_info import environment_info, environment_info_data
from .memory_info import memory_info, memory_info_data
from .python_info import python_info, python_info_data
from .system_info import system_info, system_info_data


@cache
def machine_info_kwargs() -> report_kwargs.MachineInfoKWArgs:
    """MachineInfoKWArgs factory for testing purposes.

    :return: A MachineInfoKWArgs instance with dummy data.
    :rtype: report_kwargs.MachineInfoKWArgs
    """
    data = machine_info_data()
    kwargs = report_kwargs.MachineInfoKWArgs(
        hash_id=data.get('hash_id', ''),
        node=data['node'],
        cpu=cpu_info(),
        memory=memory_info(),
        system=system_info(),
        environment=(environment_info(), python_info()),
    )
    return kwargs


def machine_info_data() -> report.MachineInfoData:
    """MachineInfoData factory for testing purposes.

    :return: A MachineInfoData instance with dummy data.
    :rtype: report.MachineInfoData
    """
    return report.MachineInfoData(
        hash_id="e" * 64,
        version=report.MachineInfo.VERSION,
        type=report.MachineInfo.TYPE,
        node="test-node",
        cpu=cpu_info_data(),
        memory=memory_info_data(),
        system=system_info_data(),
        environment=[environment_info_data(), python_info_data()],
    )

def no_hash_id_machine_info_data() -> report.MachineInfoData:
    """MachineInfoData factory for testing purposes with no hash_id.

    :return: A MachineInfoData instance with dummy data and no hash_id.
    :rtype: report.MachineInfoData
    """
    data = machine_info_data()
    data['hash_id'] = ''
    return data

@cache
def machine_info() -> report.MachineInfo:
    """Return MachineInfo with all fields set."""
    return report.MachineInfo(**machine_info_kwargs())

