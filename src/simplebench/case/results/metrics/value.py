"""Value module."""

from typing import TYPE_CHECKING, NamedTuple


if TYPE_CHECKING:
    from simplebench.metrics import Metric


class Value(NamedTuple):
    """A named tuple representing the value of a measurement for a metric.

    Fields:
        metric (`Metric`): The metric being measured. (position 0)
        value (`float`): The value of the metric measurement (position 1).
    """

    metric: 'Metric'
    """The metric being measured. (position 0)"""

    value: float
    """The value of the metric measurement. (position 1)"""
