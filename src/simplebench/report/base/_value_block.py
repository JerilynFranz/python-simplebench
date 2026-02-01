"""Base class for value block representation."""

from abc import ABC

from ._report_element import ReportElement

__all__: list[str] = []


class BaseValueBlock(ReportElement, ABC):
    """Base class representing a value block."""
