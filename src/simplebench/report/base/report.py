"""Abstract Base Class for JSON reports."""

from abc import ABC

from ._report_element import ReportElement

__all__ = []


class BaseReport(ReportElement, ABC):
    """Abstract base class representing a report."""
