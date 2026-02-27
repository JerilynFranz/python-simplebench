"""Factories for creating Report instances with dummy data for testing."""
# ruff: noqa: F401
from functools import cache

from simplebench.report.versions.v1 import Report, ReportData
from simplebench.simplebench_types import VariationCols
from simplebench_tests.factories.report import v1 as report_factories
from simplebench_tests.kwargs.report.v1 import ReportKWArgs


@cache
def report_kwargs() -> ReportKWArgs:
    """ReportKWArgs factory for testing purposes.

    :return: A ReportKWArgs instance with dummy data.
    :rtype: ReportKWArgs
    """
    data = report_data()
    kwargs = ReportKWArgs(
        hash_id=data.get('hash_id', ''),
        timestamp=data['timestamp'],
        group=data['group'],
        title=data['title'],
        description=data['description'],
        variation_cols=VariationCols(data['variation_cols']),
        results=tuple(report_factories.results_info() for _ in range(2)),
        machine=report_factories.machine_info()
    )
    return kwargs


def report_data() -> ReportData:
    """ReportData factory for testing purposes.

    :return: A ReportData instance with dummy data.
    :rtype: ReportData
    """
    return ReportData(
        hash_id="e" * 64,
        version=Report.VERSION,
        type=Report.TYPE,
        timestamp="2024-01-01T00:00:00Z",
        group="test_group",
        title="Test Benchmark",
        description="This is a test benchmark report.",
        results=tuple(report_factories.results_info_data() for _ in range(2)),
        machine=report_factories.machine_info_data(),
        variation_cols={"arg1": "value1", "arg2": "value2"},
    )

def no_hash_id_report_data() -> ReportData:
    """ReportData factory for testing purposes with no hash_id.

    :return: A ReportData instance with dummy data and no hash_id.
    :rtype: ReportData
    """
    data = report_data()
    data['hash_id'] = ''
    return data


@cache
def report() -> Report:
    """Return Report with all fields set."""
    return Report(**report_kwargs())
