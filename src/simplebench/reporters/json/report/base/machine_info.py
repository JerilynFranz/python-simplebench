"""JSONMachineInfo reporter base class.

This class represents machine information in a JSON report.

It implements validation and serialization/deserialization methods to and from dictionaries
for the following JSON Schema version:

https://raw.githubusercontent.com/JerilynFranz/python-simplebench/main/schemas/v1/machine-info.json

It is the base implemention of the JSON report machine info representation.

This makes the implementations of JSONMachineInfo backwards compatible with future versions
of the JSON report schema and the V1 implementation itself is essentially a frozen snapshot
of the base JSONMachineInfo representation at the time of the V1 schema release.
"""
from abc import ABC, abstractmethod
from typing import Any

from .json_schema import JSONSchema


class MachineInfo(ABC):
    """Class representing machine information in a JSON report."""

    VERSION: int = 0
    """The JSON MachineInfo version number.

    This is a class-level property that should be set by subclasses to the appropriate
    value for their specific version of machine information.
    """

    TYPE: str = ""
    """The JSON MachineInfo type property value for reports.

    This is a class-level property that should be set by subclasses to the appropriate
    value for their specific type of machine information.
    """

    ID: str = ""
    """The JSON MachineInfo schema identifier for reports.

    This is a class-level property that should be set by subclasses to the appropriate
    value for their specific schema identifier of machine information.
    """

    SCHEMA: type[JSONSchema] = JSONSchema
    """The JSON schema class for reports."""

    def __init__(self) -> None:
        """Initialize MachineInfo."""
        raise NotImplementedError("MachineInfo is an abstract base class and cannot be instantiated")

    @classmethod
    @abstractmethod
    def from_dict(cls, data: dict[str, Any]) -> 'MachineInfo':
        """Create a MachineInfo instance from a dictionary.

        .. code-block:: python
           :caption: Example

           json_machine_info = MachineInfo.from_dict(data)

        :param data: The dictionary containing machine information.
        :return: A MachineInfo instance.
        """
        raise NotImplementedError("from_dict is an abstract method and must be implemented by subclasses")

    @abstractmethod
    def to_dict(self) -> dict[str, Any]:
        """Convert the MachineInfo to a dictionary.

        :return: A dictionary representation of the MachineInfo.
        """
        raise NotImplementedError("to_dict is an abstract method and must be implemented by subclasses")
