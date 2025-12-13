"""Base class for all PythonInfo classes."""
from abc import ABC, abstractmethod
from typing import Any

from simplebench.base import Hydrator

from ..protocols import Environment


class PythonInfo(ABC, Environment, Hydrator):
    """Base class for all PythonInfo classes."""

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

    @abstractmethod
    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> 'PythonInfo':
        """Create a PythonInfo object from a dictionary."""
        raise NotImplementedError("This method should be overridden by subclasses")

    @abstractmethod
    def to_dict(self) -> dict:
        """Convert the PythonInfo object to a dictionary."""
        raise NotImplementedError("This method should be overridden by subclasses")

    @property
    @abstractmethod
    def hash_id(self) -> str:
        """Return the hash ID of the PythonInfo object.

        The hash ID is a unique identifier for the PythonInfo object and
        is used to uniquely identify the PythonInfo object in a collection.

        It must be overridden in subclasses to specify the correct hash ID
        for the subclass. It is a required property and must match the
        following pattern: ^[a-f0-9]{64}$
        """
        raise NotImplementedError("This method should be overridden by subclasses")

    @hash_id.setter
    @abstractmethod
    def hash_id(self, value: str) -> None:
        """Set the hash ID of the PythonInfo object."""
        raise NotImplementedError("This method should be overridden by subclasses")

    @property
    def version(self) -> int:
        """Return the version of the PythonInfo object."""
        return self.VERSION

    @property
    def type(self) -> str:
        """Return the type of the PythonInfo object."""
        return self.TYPE

    @property
    def schema_id(self) -> str:
        """Return the JSON Schema $id of the PythonInfo object."""
        return self.ID

    def is_execution_environment(self) -> None:
        """Declare that the PythonInfo object is an execution environment.

        This method's existence is required by the Environment protocol.
        It does not need to be overridden by subclasses - it is a placeholder
        for the protocol and marks the subclasses as an execution environment
        for the ExecutionEnvironment class.
        """
