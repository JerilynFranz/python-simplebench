"""Base class for all PythonInfo classes."""
from abc import ABC, abstractmethod
from typing import Any

from simplebench.base import Hydrator

from ..protocols import Environment
from .json_schema import JSONSchema


class PythonInfo(ABC, Environment, Hydrator):
    """Base class for all PythonInfo classes."""

    SCHEMA: type[JSONSchema] = JSONSchema
    """The JSON schema class for the PythonInfo class.

    It must be overridden in subclasses to specify the correct JSON schema class.
    """

    VERSION: int = 0
    """The PythonInfo version number.

    It must be overridden in subclasses to specify the correct version.
    """

    TYPE: str = ""
    """The PythonInfo type property value.

    It must be overridden in subclasses to specify the correct type.
    """

    ID: str = ""
    """The PythonInfo $id property value.

    It must be overridden in subclasses to specify the correct $id.
    """

    @abstractmethod
    def __init__(self) -> None:
        """Initialize the PythonInfo class."""
        raise NotImplementedError("This method should be overridden by subclasses")

    @classmethod
    @abstractmethod
    def from_dict(cls, data: dict[str, Any]) -> 'PythonInfo':
        """Create a PythonInfo object from a dictionary."""
        raise NotImplementedError("This method should be overridden by subclasses")

    @abstractmethod
    def to_dict(self) -> dict:
        """Convert the PythonInfo object to a dictionary."""
        raise NotImplementedError("This method should be overridden by subclasses")

    def is_execution_environment(self) -> None:
        """Declare that the PythonInfo object is an execution environment.

        This method's existence is required by the Environment protocol.
        It does not need to be overridden by subclasses - it is a placeholder
        for the protocol and marks the subclasses as an execution environment
        for the ExecutionEnvironment class.
        """
