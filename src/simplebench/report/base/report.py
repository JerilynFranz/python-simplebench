"""Abstract Base Class for JSON reports."""
from abc import ABC

from .report_element import ReportElement


class BaseReport(ReportElement, ABC):
    """Abstract base class representing a report."""
