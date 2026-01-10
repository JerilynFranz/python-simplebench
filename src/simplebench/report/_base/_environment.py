"""Base class for execution environments in reports"""

from abc import ABC, abstractmethod
from collections.abc import Mapping

from .report_element import ReportElement


class Environment(ReportElement, ABC):
    """Abstract base class for execution environments in reports.
    
    It marks the class as an execution environment for use in
    ExecutionEnvironment representations in MachineInfo objects.
    """
    @abstractmethod
    @classmethod
    def from_dict(cls, data: Mapping[str, object]) -> 'Environment':
        """Create an Environment instance from a dictionary.

        :param data: The dictionary containing environment information.
        :return: An Environment instance.
        """
