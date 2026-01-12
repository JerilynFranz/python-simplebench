"""VirtualMemoryObject reporter base class.

This class represents memory information in a report.

It implements validation and serialization/deserialization methods to and from dictionaries
for the following JSON Schema version:

https://raw.githubusercontent.com/JerilynFranz/python-simplebench/main/schemas/v1/memory-info.json

It is the base implemention of the report memory info representation.
"""

from abc import ABC

from simplebench.base._hydrator import Hydrator

from ._report_element import ReportElement


__all__ = []


class BaseVirtualMemoryObject(ReportElement, Hydrator, ABC):
    """Class representing virtual memory information in a report."""
