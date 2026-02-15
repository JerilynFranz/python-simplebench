"""Factories for report.v1.vcs_info."""
from functools import cache

from simplebench.report.versions import v1 as report
from simplebench.validators import is_typed_dict_mimic
from simplebench_tests.kwargs.report.v1 import VCSInfoKWArgs


@cache
def vcs_info_kwargs() -> VCSInfoKWArgs:
    """VCSInfoKWArgs factory for testing purposes.

    :return: A VCSInfoKWArgs instance with dummy data.
    :rtype: VCSInfoKWArgs
    """
    data = vcs_info_data()
    return VCSInfoKWArgs(
        hash_id=data['hash_id'],  # type: ignore[call-arg]
        vcs=data['vcs'],
        commit_id=data['commit_id'],
        commit_datetime=data['commit_datetime'],
        branch=data['branch'],
        repository_url=data['repository_url'],
        is_dirty=data['is_dirty'],
    )


@cache
def vcs_info() -> report.VCSInfo:
    """VCSInfo factory for testing purposes.

    :return: A VCSInfo instance with dummy data.
    :rtype: report.VCSInfo
    """
    return report.VCSInfo(**vcs_info_kwargs())

"""Factories for creating report VCSInfoData instances with dummy data for testing."""

def vcs_info_data() -> report.VCSInfoData:
    """VCSInfoData factory for testing purposes.

    :return: A VCSInfoData instance with dummy data.
    :rtype: report.VCSInfoData
    """
    info = report.VCSInfoData(
        hash_id='c' * 64,
        type=report.VCSInfoSchema.TYPE,
        version=report.VCSInfoSchema.VERSION,
        vcs='git',
        commit_id='0aa249cb4f7d923eabfe4583f8b378b01b676471',
        commit_datetime='2025-02-11T19:13:15+00:00',
        branch='main',
        repository_url='https://github.com/JerilynFranz/python-simplebench.git',
        is_dirty=False,
      )
    if 'hash_id' not in info:  # type: ignore[typeddict-item]
        raise TypeError(f'Generated info is missing required hash_id field: {info!r}')
    if not is_typed_dict_mimic(info, report.VCSInfoData):
        raise TypeError(f'Generated info does not conform to VCSInfoData TypedDict: {info!r}')
    return info

def no_hash_id_vcs_info_data() -> report.VCSInfoData:
    """VCSInfoData factory for testing purposes.

    :return: A VCSInfoData instance with dummy data.
    :rtype: report.VCSInfoData
    """
    info = vcs_info_data()
    del info['hash_id']  # type: ignore[typeddict-item]
    if not is_typed_dict_mimic(info, report.VCSInfoData):
        raise TypeError(f'Generated info does not conform to VCSInfoData TypedDict: {info!r}')
    return info


