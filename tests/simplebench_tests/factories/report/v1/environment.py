"""Factories for creating report CPUInfoData instances with dummy data for testing."""
from functools import cache

from simplebench.report.versions import v1 as report
from simplebench_tests.kwargs.report import v1 as report_kwargs


@cache
def environment_kwargs() -> report_kwargs.EnvironmentKWArgs:
    """EnvironmentKWArgs factory for testing purposes.

    :return: An EnvironmentKWArgs instance with dummy data.
    :rtype: report_kwargs.EnvironmentKWArgs
    """
    return report_kwargs.EnvironmentKWArgs(**environment_data())  # type: ignore


def environment_data() -> report.EnvironmentData:
    """EnvironmentData factory for testing purposes.

    :return: An EnvironmentData instance with dummy data.
    :rtype: report.EnvironmentData
    """
    return report.EnvironmentData(
        hash_id='f' * 64,
        semantic_type='simplebench::generic',
        title='Generic Environment',
        description='A generic environment for testing purposes.',
        data={
           'example_key': 'example_value',
            })
