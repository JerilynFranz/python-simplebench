"""Base class for execution environments in reports"""

from abc import ABC

from .report_element import ReportElement


class Environment(ReportElement, ABC):
    """Abstract base class for execution environments in reports.
    
    It marks the class as an execution environment for use in
    ExecutionEnvironment representations in MachineInfo objects.
    """
