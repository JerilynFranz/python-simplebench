"""Factories for report.v1.results_info."""
from functools import cache

from simplebench.report.versions import v1 as report
from simplebench.validators import is_typed_dict_mimic
from simplebench_tests.factories.report import v1 as report_factories
from simplebench_tests.kwargs.report.v1 import ResultsInfoKWArgs


@cache
def results_info_kwargs() -> ResultsInfoKWArgs:
    """ResultsInfoKWArgs factory for testing purposes.

    :return: A ResultsInfoKWArgs instance with dummy data.
    :rtype: ResultsInfoKWArgs
    """
    data = results_info_data()
    return ResultsInfoKWArgs(
        hash_id=data['hash_id'],  # type: ignore[typeddict-item]
        group=data['group'],
        title=data['title'],
        description=data['description'],
        n=data['n'],
        variation_marks=data['variation_marks'],
        metrics=report.MetricsObject({'test_metric::value': report_factories.value_block()}),
        extra_info=report.ExtrasObject(data['extra_info']),
    )


@cache
def results_info() -> report.ResultsInfo:
    """ResultsInfo factory for testing purposes.

    :return: A ResultsInfo instance with dummy data.
    :rtype: report.ResultsInfo
    """
    return report.ResultsInfo(**results_info_kwargs())

"""Factories for creating report ResultsInfoData instances with dummy data for testing."""

def results_info_data() -> report.ResultsInfoData:
    """ResultsInfoData factory for testing purposes.

    :return: A ResultsInfoData instance with dummy data.
    :rtype: report.ResultsInfoData
    """
    info = report.ResultsInfoData(
        group='test_group',
        title='Test Results',
        description='This is a test ResultsInfoData instance.',
        n=1000.0,
        variation_marks={'test_variation': 'test_value'},
        metrics={'test_metric::value': report_factories.value_block_data()},
        extra_info={'test_extra': 'extra_value'},
        hash_id='c' * 64,
        type=report.ResultsInfoSchema.TYPE,
        version=report.ResultsInfoSchema.VERSION,
      )
    if 'hash_id' not in info:  # type: ignore[typeddict-item]
        raise TypeError(f'Generated info is missing required hash_id field: {info!r}')
    if not is_typed_dict_mimic(info, report.ResultsInfoData):
        raise TypeError(f'Generated info does not conform to ResultsInfoData TypedDict: {info!r}')
    return info

def no_hash_id_results_info_data() -> report.ResultsInfoData:
    """ResultsInfoData factory for testing purposes.

    :return: A ResultsInfoData instance with dummy data.
    :rtype: report.ResultsInfoData
    """
    info = results_info_data()
    del info['hash_id']  # type: ignore[typeddict-item]
    if not is_typed_dict_mimic(info, report.ResultsInfoData):
        raise TypeError(f'Generated info does not conform to ResultsInfoData TypedDict: {info!r}')
    return info


