"""SystemInfo report base class.

This class represents System information in a report.

It implements validation and serialization/deserialization methods to and from dictionaries
for the following JSON Schema version:

https://raw.githubusercontent.com/JerilynFranz/python-simplebench/main/schemas/v1/system-info.json

It is the base implemention of the report system info representation.
"""

from abc import ABC

from .report_element import ReportElement

__all__ = []


class BaseSystemInfo(ReportElement, ABC):
    """Class representing System information in a report."""
