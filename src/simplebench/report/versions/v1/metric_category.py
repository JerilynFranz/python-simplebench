"""Metric categories."""

from enum import Enum

from simplebench.doc_utils import enum_docstrings

__all__: list[str] = []


@enum_docstrings
class MetricCategory(str, Enum):
    """Type of metric"""

    VALUE = 'VALUE'
    """A metric that is aggregated into a single value for all measurements"""
    STATS = 'STATS'
    """A metric that provides statistical information for measurements, such as the average response time."""
    RAW_DATA = 'RAW_DATA'
    """A metric that represents raw measurements without any aggregation or statistical processing."""
