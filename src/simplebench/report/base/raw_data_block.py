"""Base class for value block representation."""
from abc import ABC

from .report_element import ReportElement


class BaseRawDataBlock(ReportElement, ABC):
    """Base class representing a raw data block."""
