"""Base class for execution environments in reports"""

from abc import ABC, abstractmethod
from typing import Any

from .report_element import ReportElement


class Environment(ReportElement, ABC):
    """Abstract base class for execution environments in reports.
    
    It marks the class as an execution environment for use in
    ExecutionEnvironment representations in MachineInfo objects.
    """
    @classmethod
    @abstractmethod
    def from_dict(cls, data: dict[str, Any]) -> 'Environment':
        """Create an instance of the element from a dictionary."""
        raise NotImplementedError(
                "from_dict is an abstract class method and must be implemented by a subclass")
