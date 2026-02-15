"""Factories for report.v1.value_block."""
from functools import cache

from simplebench.report.versions import v1 as report
from simplebench.validators import is_typed_dict_mimic
from simplebench_tests.kwargs.report.v1 import ValueBlockKWArgs


@cache
def value_block_kwargs() -> ValueBlockKWArgs:
    """ValueBlockKWArgs factory for testing purposes.

    :return: A ValueBlockKWArgs instance with dummy data.
    :rtype: ValueBlockKWArgs
    """
    data = value_block_data()
    return ValueBlockKWArgs(
        hash_id=data['hash_id'],  # type: ignore[call-arg]
        semantic_type=data['semantic_type'],
        timer=data['timer'], # type: ignore[call-arg]
        unit=data['unit'],
        scale=data['scale'],
        value=data['value'],
    )


@cache
def value_block() -> report.ValueBlock:
    """ValueBlock factory for testing purposes.

    :return: A ValueBlock instance with dummy data.
    :rtype: report.ValueBlock
    """
    return report.ValueBlock(**value_block_kwargs())

"""Factories for creating report ValueBlockData instances with dummy data for testing."""

def value_block_data() -> report.ValueBlockData:
    """ValueBlockData factory for testing purposes.

    :return: A ValueBlockData instance with dummy data.
    :rtype: report.ValueBlockData
    """
    info = report.ValueBlockData(
        hash_id='c' * 64,
        type=report.ValueBlockSchema.TYPE,
        version=report.ValueBlockSchema.VERSION,
        semantic_type='test::value',
        timer='test_timer',
        unit='seconds',
        scale=1.0,
        value=123.456,
      )
    if 'hash_id' not in info:  # type: ignore[typeddict-item]
        raise TypeError(f'Generated info is missing required hash_id field: {info!r}')
    if not is_typed_dict_mimic(info, report.ValueBlockData):
        raise TypeError(f'Generated info does not conform to ValueBlockData TypedDict: {info!r}')
    return info

def no_hash_id_value_block_data() -> report.ValueBlockData:
    """ValueBlockData factory for testing purposes.

    :return: A ValueBlockData instance with dummy data.
    :rtype: report.ValueBlockData
    """
    info = value_block_data()
    del info['hash_id']  # type: ignore[typeddict-item]
    if not is_typed_dict_mimic(info, report.ValueBlockData):
        raise TypeError(f'Generated info does not conform to ValueBlockData TypedDict: {info!r}')
    return info


