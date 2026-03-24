"""MetricType factory for tests"""

from simplebench.report.versions import v1 as report
from simplebench_tests.kwargs.report import v1 as report_kwargs


def metric_type() -> report.MetricType:
    """MetricType factory for testing purposes.

    :return: A MetricType instance with dummy data.
    :rtype: report.MetricType
    """
    return report.MetricType(**metric_type_kwargs())


def metric_type_kwargs() -> report_kwargs.MetricTypeKWArgs:
    """MetricTypeKWArgs factory for testing purposes.

    :return: A MetricTypeKWArgs instance with dummy data.
    :rtype: report_kwargs.MetricTypeKWArgs
    """
    data = metric_type_data()
    return report_kwargs.MetricTypeKWArgs(
        hash_id=data['hash_id'],  # type: ignore[call-arg]
        scale=data['scale'],
        unit=data['unit'],
        semantic_type=data['semantic_type'],
        label=data['label'],
        description=data['description'],
        category=report.MetricCategory[data['category']],
    )


def metric_type_data() -> report.MetricTypeData:
    """MetricTypeData factory for testing purposes.

    :return: A MetricTypeData instance with dummy data.
    :rtype: report.MetricTypeData
    """
    return report.MetricTypeData(
        hash_id='e' * 64,
        scale=1.0,
        unit='seconds',
        semantic_type='test::metric',
        label='test_label',
        description='test_description',
        category=report.MetricCategory.VALUE.value,
    )
