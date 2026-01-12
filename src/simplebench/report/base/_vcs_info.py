"""VCSInfo report base class.

This class represents VCS information in a report.

It implements validation and serialization/deserialization methods to and from dictionaries
for the following JSON Schema version:

https://raw.githubusercontent.com/JerilynFranz/python-simplebench/main/schemas/v1/vcs-info.json

It is the base implemention of the report vcs info representation.
"""

from abc import ABC

from ._report_element import ReportElement


__all__ = []


class BaseVCSInfo(ReportElement, ABC):
    """Class representing VCS information in a report."""
