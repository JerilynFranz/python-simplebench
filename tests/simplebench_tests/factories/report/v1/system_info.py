"""Factories for report.v1.system_info."""
from functools import cache

from simplebench.report.versions import v1 as report
from simplebench.validators import is_typed_dict_mimic
from simplebench_tests.kwargs.report.v1 import SystemInfoKWArgs


@cache
def system_info_kwargs() -> SystemInfoKWArgs:
    """SystemInfoKwargs factory for testing purposes.

    :return: A SystemInfoKwargs instance with dummy data.
    :rtype: SystemInfoWArgs
    """
    data = system_info_data()
    return SystemInfoKWArgs(
        hash_id=data['hash_id'],  # type: ignore[typeddict-item]
        system=data['system'],
        system_version=data['system_version'],
        release=data['release'],
        machine=data['machine'])

@cache
def system_info() -> report.SystemInfo:
    """SystemInfo factory for testing purposes.

    :return: A SystemInfo instance with dummy data.
    :rtype: report.SystemInfo
    """
    return report.SystemInfo(**system_info_kwargs())

def system_info_data() -> report.SystemInfoData:
    """SystemInfoData factory for testing purposes.

    :return: A SystemInfoData instance with dummy data.
    :rtype: report.SystemInfoData
    """
    info = report.SystemInfoData(
        hash_id='c' * 64,
        type=report.SystemInfo.TYPE,
        version=report.SystemInfo.VERSION,
        system='TestOS',
        system_version='1.0',
        release='1.0',
        machine='x86_64')
    if 'hash_id' not in info:  # type: ignore[typeddict-item]
        raise TypeError(f'Generated info is missing required hash_id field: {info!r}')
    if not is_typed_dict_mimic(info, report.SystemInfoData):
        raise TypeError(f'Generated info does not conform to SystemInfoData TypedDict: {info!r}')
    return info

def no_hash_id_system_info_data() -> report.SystemInfoData:
    """SystemInfoData factory for testing purposes.

    :return: A SystemInfoData instance with dummy data.
    :rtype: report.SystemInfoData
    """
    info = system_info_data()
    del info['hash_id']  # type: ignore[typeddict-item]
    if not is_typed_dict_mimic(info, report.SystemInfoData):
        raise TypeError(f'Generated info does not conform to SystemInfoData TypedDict: {info!r}')
    return info
