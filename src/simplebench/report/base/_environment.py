"""Base class for execution environments in reports"""

from abc import ABC, abstractmethod
from collections.abc import Mapping

from simplebench.simplebench_types import CoreDataTypes

from ._report_element import ReportElement

__all__ = []


class Environment(ReportElement, ABC):
    """Base class for execution environments in reports.

    It marks the class as an execution environment for use in
    ExecutionEnvironment representations in MachineInfo objects.
    """

    @classmethod
    def from_dict(cls, data: Mapping[str, CoreDataTypes]) -> 'Environment':
        """Create an Environment instance from a dictionary.

        :param data: The dictionary containing environment information.
        :return: An Environment instance.
        """
        raise NotImplementedError('from_dict must be implemented in subclasses of Environment')

    @property
    @abstractmethod
    def hash_id(self) -> str:
        """Get the hash_id property.

        :return: A 64-character hexadecimal hash_id string.
        """
        ...
