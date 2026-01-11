"""Base class for execution environments in reports"""
from abc import ABC

from .report_element import ReportElement

__all__ = []


class Environment(ReportElement, ABC):
    """Base class for execution environments in reports.
    
    It marks the class as an execution environment for use in
    ExecutionEnvironment representations in MachineInfo objects.
    """

    @classmethod
    def from_dict(cls, data) -> 'Environment':
        """Create an Environment instance from a dictionary.

        :param data: The dictionary containing environment information.
        :return: An Environment instance.
        """
        raise NotImplementedError("from_dict must be implemented in subclasses of Environment")
