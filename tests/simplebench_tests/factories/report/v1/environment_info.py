"""Factories for creating report CPUInfoData instances with dummy data for testing."""
from functools import cache

from simplebench.report.versions import v1 as report
from simplebench_tests.kwargs.report import v1 as report_kwargs


@cache
def environment_info() -> report.EnvironmentInfo:
    """Return EnvironmentInfo with all fields set."""
    return report.EnvironmentInfo(**environment_info_kwargs())

@cache
def environment_info_kwargs() -> report_kwargs.EnvironmentInfoKWArgs:
    """EnvironmentKWArgs factory for testing purposes.

    :return: An EnvironmentKWArgs instance with dummy data.
    :rtype: report_kwargs.EnvironmentKWArgs
    """
    return report_kwargs.EnvironmentInfoKWArgs(**environment_info_data())  # type: ignore


def environment_info_data() -> report.EnvironmentInfoData:
    """EnvironmentData factory for testing purposes.

    :return: An EnvironmentData instance with dummy data.
    :rtype: report.EnvironmentData
    """
    return report.EnvironmentInfoData(
        hash_id='f' * 64,
        semantic_type='simplebench::generic',
        title='Generic Environment',
        description='A generic environment for testing purposes.',
        data={
           'example_key': 'example_value',
            })

def no_hash_id_environment_info_data() -> report.EnvironmentInfoData:
    """EnvironmentData factory for testing purposes with no hash_id.

    :return: An EnvironmentData instance with dummy data and no hash_id.
    :rtype: report.EnvironmentData
    """
    data = environment_info_data()
    data['hash_id'] = ''
    return data
