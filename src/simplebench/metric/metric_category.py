"""Metric categories."""
from enum import Enum

from simplebench.doc_utils import enum_docstrings


@enum_docstrings
class MetricCategory(str, Enum):
    """Type of metric"""
    CUMULATIVE = 'cumulative'
    """A metric that is aggregated into a single value for all measurements"""
    STATISTICAL = 'statistical'
    """A metric that provides statistical information for measurements, such as the average response time."""
    RAW = 'raw'
    """A metric that represents raw measurements without any aggregation or statistical processing."""
