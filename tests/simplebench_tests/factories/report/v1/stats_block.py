"""Factories for report.v1.stats_block."""
import math
import statistics
from functools import cache

from simplebench.report.versions import v1 as report
from simplebench.simplebench_types import Values
from simplebench.validators import is_typed_dict_mimic
from simplebench_tests.kwargs.report.v1 import StatsBlockKWArgs


@cache
def stats_block_measurements() -> Values:
    """StatsBlockMeasurements factory for testing purposes.

    This is a Values object containing a list of 101 float measurements from
    0.0 to 100.0 inclusive, which can be used as dummy data for testing StatsBlock measurements.

    :return: A StatsBlockMeasurements instance with dummy data.
    :rtype: report.StatsBlockMeasurements
    """
    return Values(list(range(0, 100)))


@cache
def stats_block_measurements_kwargs() -> StatsBlockKWArgs:
    """StatsBlockMeasurementsKWArgs factory for testing purposes.

    This is a StatsBlockKWArgs instance containing dummy data for
    the measurements property, which can be used for testing StatsBlock
    initialization with measurements.

    It is designed to produce the exact same stats data as stats_block_kwargs, but
    with measurements instead of precomputed stats as the data source.

    This allows for testing the computation of stats from measurements in StatsBlock.

    :return: A StatsBlockKWArgs instance with dummy data.
    :rtype: StatsBlockKWArgs
    """
    data = stats_block_data()
    return StatsBlockKWArgs(
        name=data['name'],
        semantic_type=data['semantic_type'],
        unit=data['unit'],
        scale=data['scale'],
        rounds=data['rounds'],
        timer=data['timer'],  # type: ignore  # validated in stats_block_data
        description=data['description'],  # type: ignore  # validated in stats_block_data
        hash_id=data['hash_id'],  # type: ignore  # validated in stats_block_data
        measurements=stats_block_measurements(),
    )

@cache
def stats_block_kwargs() -> StatsBlockKWArgs:
    """StatsBlockKWArgs factory for testing purposes.

    :return: A StatsBlockKWArgs instance with dummy data.
    :rtype: StatsBlockKWArgs
    """
    data = stats_block_data()
    return StatsBlockKWArgs(
        name=data['name'],
        semantic_type=data['semantic_type'],
        unit=data['unit'],
        scale=data['scale'],
        iterations=data['iterations'],
        rounds=data['rounds'],
        mean=data['mean'],
        median=data['median'],
        minimum=data['minimum'],
        maximum=data['maximum'],
        stdev=data['stdev'],
        relative_stdev=data['relative_stdev'],
        percentiles=data['percentiles'],
        timer=data['timer'],  # type: ignore  # validated in stats_block_data
        description=data['description'],  # type: ignore  # validated in stats_block_data
        hash_id=data['hash_id'],  # type: ignore  # validated in stats_block_data
    )


@cache
def stats_block() -> report.StatsBlock:
    """StatsBlock factory for testing purposes.

    :return: A StatsBlock instance with dummy data.
    :rtype: report.StatsBlock
    """
    return report.StatsBlock(**stats_block_kwargs())

"""Factories for creating report StatsBlockData instances with dummy data for testing."""

def stats_block_data() -> report.StatsBlockData:
    """StatsBlockData factory for testing purposes.

    :return: A StatsBlockData instance with dummy data.
    :rtype: report.StatsBlockData
    """
    info = report.StatsBlockData(
        name='Test StatsBlock',
        semantic_type='test::stats',
        unit='seconds',
        scale=1.0,
        iterations=100,
        rounds=5,
        mean=statistics.mean(stats_block_measurements()),
        median=statistics.median(stats_block_measurements()),
        minimum=min(stats_block_measurements()),
        maximum=max(stats_block_measurements()),
        # stdev scaled by sqrt of rounds to test correct handling of stdev scaling in StatsBlock when measurements are provided, since stdev of the mean should be stdev of measurements divided by sqrt(rounds)
        stdev=statistics.stdev(stats_block_measurements()) * math.sqrt(5),
        relative_stdev= 100 * math.sqrt(5) * abs(
            statistics.stdev(stats_block_measurements()) / statistics.mean(stats_block_measurements())),
        percentiles=statistics.quantiles(stats_block_measurements(), n=102, method='inclusive'),
        timer='test_timer',
        description='This is a test StatsBlockData instance.',
        hash_id='c' * 64,
        type=report.StatsBlockSchema.TYPE,
        version=report.StatsBlockSchema.VERSION,
      )
    if 'hash_id' not in info:  # type: ignore[typeddict-item]
        raise TypeError(f'Generated info is missing required hash_id field: {info!r}')
    if not is_typed_dict_mimic(info, report.StatsBlockData):
        raise TypeError(f'Generated info does not conform to StatsBlockData TypedDict: {info!r}')
    return info

def no_hash_id_stats_block_data() -> report.StatsBlockData:
    """StatsBlockData factory for testing purposes.

    :return: A StatsBlockData instance with dummy data.
    :rtype: report.StatsBlockData
    """
    info = stats_block_data()
    del info['hash_id']  # type: ignore[typeddict-item]
    if not is_typed_dict_mimic(info, report.StatsBlockData):
        raise TypeError(f'Generated info does not conform to StatsBlockData TypedDict: {info!r}')
    return info
