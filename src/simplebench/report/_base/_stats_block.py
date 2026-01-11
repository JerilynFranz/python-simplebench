"""Base class for stats block representation.

This class represents a stats block information in a report.

It implements validation and serialization/deserialization methods to and from dictionaries
for a stats block object.

It is the base implemention of the JSON report stats block representation.
"""
from abc import ABC

from .report_element import ReportElement

__all__ = []

class BaseStatsBlock(ReportElement, ABC):
    """Abstract Base class representing a StatsBlock."""
