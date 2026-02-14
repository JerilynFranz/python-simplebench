"""Factories for creating report CPUInfoData instances with dummy data for testing."""
from functools import cache

from simplebench.report.versions import v1 as report
from simplebench_tests.kwargs.report import v1 as report_kwargs


@cache
def generic_environment_kwargs() -> report_kwargs.EnvironmentKWArgs:
    """EnvironmentKWArgs factory for testing purposes.

    :return: An EnvironmentKWArgs instance with dummy data.
    :rtype: report_kwargs.EnvironmentKWArgs
    """
    return report_kwargs.EnvironmentKWArgs(**generic_environment_data())


def generic_environment_data() -> report.EnvironmentData:
    """EnvironmentData factory for testing purposes.

    :return: An EnvironmentData instance with dummy data.
    :rtype: report.EnvironmentData
    """
    return report.EnvironmentData(
        total=1024,
        used=512,
        free=512,
        percent=50.0,
        swap_in=100,
        swap_out=100,
    )

