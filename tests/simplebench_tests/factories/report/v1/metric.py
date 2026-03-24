"""Factory function for creating a report Metric instance with dummy data for testing."""

from simplebench.report.versions import v1 as report
from simplebench_tests.kwargs.report import v1 as report_kwargs

from .metric_type import metric_type, metric_type_data


def metric() -> report.Metric:
    """Metric factory for testing purposes.

    :return: A Metric instance with dummy data.
    :rtype: report.Metric
    """
    return report.Metric(**metric_kwargs())


def metric_kwargs() -> report_kwargs.MetricKWArgs:
    """MetricData factory for testing purposes.

    :return: A MetricData instance with dummy data.
    :rtype: report.MetricData
    """
    data = metric_data()
    return report_kwargs.MetricKWArgs(
        hash_id=data['hash_id'],  # type: ignore[call-arg]
        label=data['label'],
        title=data['title'],
        description=data['description'],
        metric_type=metric_type())


def metric_data() -> report.MetricData:
    """MetricData factory for testing purposes.

    :return: A MetricData instance with dummy data.
    :rtype: report.MetricData
    """
    return report.MetricData(
        hash_id='f' * 64,
        label='test_label',
        title='test_title',
        description='test_description',
        metric_type=metric_type_data(),
    )
