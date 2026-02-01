"""Base class for value block representation."""

from abc import ABC

from ._report_element import ReportElement

__all__: list[str] = []


class BaseRawDataBlock(ReportElement, ABC):
    """Base class representing a raw data block."""
