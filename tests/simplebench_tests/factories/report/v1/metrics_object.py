"""MetricsObject factory for testing."""
from functools import cache

from simplebench.report.versions import v1 as report
from simplebench_tests.factories.report import v1 as report_factories


@cache
def metrics_object() -> report.MetricsObject:
    """Factory function to create a MetricsObject with dummy data for testing.

    :return: A MetricsObject instance with dummy data.
    """
    return report.MetricsObject({
        'test::valueblock': report_factories.value_block(),
        'test::statsblock': report_factories.stats_block(),
        'test::rawdatablock': report_factories.raw_data_block(),
    })
