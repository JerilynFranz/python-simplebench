"""Value module."""

from typing import NamedTuple

from simplebench.metric import Metric


class Value(NamedTuple):
    """A named tuple representing the value of a measurement for a metric.

    Fields:
        metric (`Metric`): The metric being measured. (position 0)
        value (`float`): The value of the metric measurement (position 1).
    """
    metric: Metric
    """The metric being measured. (position 0)"""

    value: float
    """The value of the metric measurement. (position 1)"""
