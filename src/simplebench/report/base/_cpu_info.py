"""CPUInfo reporter base class.

This class represents CPU information in a JSON report.

It implements validation and serialization/deserialization methods to and from dictionaries
for the following JSON Schema version:

https://raw.githubusercontent.com/JerilynFranz/python-simplebench/main/schemas/v1/cpu-info.json

It is the base implemention of the JSON report cpu info representation.

This makes the implementations of CPUInfo backwards compatible with future versions
of the JSON report schema and the V1 implementation itself is essentially a frozen snapshot
of the base CPUInfo representation at the time of the V1 schema release.
"""

from abc import ABC

from simplebench.report.base._report_element import ReportElement

__all__ = []


class BaseCPUInfo(ReportElement, ABC):
    """Class representing CPU information in a JSON report."""
