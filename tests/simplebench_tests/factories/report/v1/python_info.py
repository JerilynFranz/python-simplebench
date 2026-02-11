"""Factories for report.v1.python_info."""
from types import MappingProxyType

from typeguard import check_type

from simplebench.report.versions import v1 as report
from simplebench_tests.kwargs.report.v1 import PythonInfoKWArgs


def report_python_info_kwargs() -> PythonInfoKWArgs:
    """PythonInfoKwargs factory for testing purposes.

    :return: A PythonInfoKwargs instance with dummy data.
    :rtype: PythonInfoWArgs
    """
    return PythonInfoKWArgs(
        python_version='3.12.3',
        implementation='CPython',
        implementation_version='3.12.3',
        compiler='Clang 13.0.0 (clang-1300.0.29.30)',
        revision='f6650f9ad7',
        buildno='v3.12.3:f6650f9ad7',
        builddate='Apr  9 2024 08:18:47',
        command_line_flags='-R -X int_max_str_digits',
        environment_variables=MappingProxyType({
            'PYTHONPATH': 'src:tests',
            'PYTHON_BASIC_REPL': '1'}),
        gc_is_enabled=True,
        gc_thresholds=(700, 10, 10),
        thread_switch_interval=0.005,
        architecture_bits='64bit',
        architecture_linkage=''
    )


def report_python_info() -> report.PythonInfo:
    """PythonInfo factory for testing purposes.

    :return: A PythonInfo instance with dummy data.
    :rtype: report.PythonInfo
    """
    return report.PythonInfo(**report_python_info_kwargs())

"""Factories for creating report PythonInfoData instances with dummy data for testing."""


def report_python_info_data() -> report.PythonInfoData:
    """PythonInfoData factory for testing purposes.

    :return: A PythonInfoData instance with dummy data.
    :rtype: report.PythonInfoData
    """
    info = report.PythonInfoData()
    )
    check_type(info, report.PythonInfoData)
    return info

