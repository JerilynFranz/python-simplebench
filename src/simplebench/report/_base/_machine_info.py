"""MachineInfo report base class.

This class represents machine information in a report.

It implements validation and serialization/deserialization methods to and from dictionaries
for the following JSON Schema version:

https://raw.githubusercontent.com/JerilynFranz/python-simplebench/main/schemas/v1/machine-info.json

It is the base implemention of the report machine info representation.
"""

from abc import ABC

from simplebench.base._hydrator import Hydrator

from .report_element import ReportElement

__all__ = []


class BaseMachineInfo(ReportElement, Hydrator, ABC):
    """Class representing machine information in a report."""
