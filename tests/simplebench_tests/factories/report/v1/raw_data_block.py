"""Factories for report.v1.raw_data_block."""
from functools import cache

from simplebench.report.versions import v1 as report
from simplebench.simplebench_types import Values
from simplebench.validators import is_typed_dict_mimic
from simplebench_tests.kwargs.report.v1 import RawDataBlockKWArgs


@cache
def raw_data_block_kwargs() -> RawDataBlockKWArgs:
    """RawDataBlockKWArgs factory for testing purposes.

    :return: A RawDataBlockKWArgs instance with dummy data.
    :rtype: RawDataBlockKWArgs
    """
    data = raw_data_block_data()
    return RawDataBlockKWArgs(
        hash_id=data['hash_id'],  # type: ignore[call-arg]
        metric=data['metric'],  # type: ignore[call-arg]
        rounds=data['rounds'],
        data=data['data'],
    )


@cache
def raw_data_block() -> report.RawDataBlock:
    """RawDataBlock factory for testing purposes.

    :return: A RawDataBlock instance with dummy data.
    :rtype: report.RawDataBlock
    """
    return report.RawDataBlock(**raw_data_block_kwargs())

"""Factories for creating report RawDataBlockData instances with dummy data for testing."""

def raw_data_block_data() -> report.RawDataBlockData:
    """RawDataBlockData factory for testing purposes.

    :return: A RawDataBlockData instance with dummy data.
    :rtype: report.RawDataBlockData
    """
    info = report.RawDataBlockData(
        hash_id='c' * 64,
        metric='test_metric',
        type=report.RawDataBlockSchema.TYPE,
        version=report.RawDataBlockSchema.VERSION,
        rounds=5,
        data=Values([1.0, 2.0, 3.0, 4.0, 5.0]),
      )
    if 'hash_id' not in info:  # type: ignore[typeddict-item]
        raise TypeError(f'Generated info is missing required hash_id field: {info!r}')
    if not is_typed_dict_mimic(info, report.RawDataBlockData):
        raise TypeError(f'Generated info does not conform to RawDataBlockData TypedDict: {info!r}')
    return info

def no_hash_id_raw_data_block_data() -> report.RawDataBlockData:
    """RawDataBlockData factory for testing purposes.

    :return: A RawDataBlockData instance with dummy data.
    :rtype: report.RawDataBlockData
    """
    info = raw_data_block_data()
    del info['hash_id']  # type: ignore[typeddict-item]
    if not is_typed_dict_mimic(info, report.RawDataBlockData):
        raise TypeError(f'Generated info does not conform to RawDataBlockData TypedDict: {info!r}')
    return info


