"""Factories for report.v1.value_block."""
from functools import cache

from simplebench.report.versions import v1 as report
from simplebench.validators import is_typed_dict_mimic
from simplebench_tests.kwargs.report.v1 import ValueBlockKWArgs

_METRIC = report.Metric(
    label='TESTMETRIC',
    title='test_metric',
    description='test metric description',
    metric_type=report.MetricType(
        label='TESTMETRICTYPE',
        description='test_metric_type',
        semantic_type='test::metric_type',
        unit='seconds',
        scale=1.0,
        category=report.MetricCategory.VALUE,)
)


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
        metric=_METRIC,
        value=data['value'],
    )


@cache
def value_block() -> report.ValueBlock:
    """ValueBlock factory for testing purposes.

    :return: A ValueBlock instance with dummy data.
    :rtype: report.ValueBlock
    """
    return report.ValueBlock(**value_block_kwargs())


def value_block_data() -> report.ValueBlockData:
    """ValueBlockData factory for testing purposes.

    :return: A ValueBlockData instance with dummy data.
    :rtype: report.ValueBlockData
    """
    info = report.ValueBlockData(
        hash_id='c' * 64,
        semantic_type='test::value',
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
