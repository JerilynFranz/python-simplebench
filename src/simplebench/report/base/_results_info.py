"""report Results base class.

This class represents Results in a report.

It implements validation and serialization/deserialization methods to and from dictionaries
for the results property object in the following JSON Schema version:

https://raw.githubusercontent.com/JerilynFranz/python-simplebench/main/schemas/v1/results-info.json
"""

from abc import ABC

from ._report_element import ReportElement

__all__ = []


class BaseResultsInfo(ReportElement, ABC):
    """Base class representing results in a report."""
