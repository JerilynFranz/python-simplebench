"""Metrics base class.

This class represents execution environment information in a Metrics object.

It implements validation and serialization/deserialization methods to and from dictionaries
for the metrics property for following JSON Schema version:

https://raw.githubusercontent.com/JerilynFranz/python-simplebench/main/schemas/v1/results-info.json

It is the base implemention of the metrics representation property in ResultsInfo objects,
not a standalone implementation of a JSON report schema.
"""

from abc import ABC
from typing import TypeAlias

from ._report_element import ReportElement

__all__ = []


class Metrics(ReportElement, ABC):
    """Abstract class representing the metrics property for a results info object in a JSON report."""

    MetricItem: TypeAlias
    """Type alias for allowed metric items in the metrics property.

    Must be overridden by subclasses to specify the actual types allowed for metric items.
    """
