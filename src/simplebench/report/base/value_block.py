"""Base class for value block representation."""
from abc import ABC

from .report_element import ReportElement


class BaseValueBlock(ReportElement, ABC):
    """Base class representing a value block."""
