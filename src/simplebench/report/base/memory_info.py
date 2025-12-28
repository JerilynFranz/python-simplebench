"""JSONMemoryInfo reporter base class.

This class represents memory information in a JSON report.

It implements validation and serialization/deserialization methods to and from dictionaries
for the following JSON Schema version:

https://raw.githubusercontent.com/JerilynFranz/python-simplebench/main/schemas/v1/memory-info.json

It is the base implemention of the JSON report memory info representation.

This makes the implementations of MemoryInfo backwards compatible with future versions
of the report schema and the V1 implementation itself is essentially a frozen snapshot
of the base MemoryInfo representation at the time of the V1 schema release.
"""
from abc import ABC, abstractmethod
from typing import Any

from simplebench.base import Hydrator

from .json_schema import JSONSchema


class BaseMemoryInfo(Hydrator, ABC):
    """Class representing memory information in a report."""

    VERSION: int = 0
    """The MemoryInfo version number.

    This is a class-level property that should be set by subclasses to the appropriate
    value for their specific version of memory information.
    """

    TYPE: str = ""
    """The JSON MemoryInfo type property value for reports.

    This is a class-level property that should be set by subclasses to the appropriate
    value for their specific type of memory information.
    """

    ID: str = ""
    """The JSON MemoryInfo schema identifier for reports.

    This is a class-level property that should be set by subclasses to the appropriate
    value for their specific schema identifier of memory information.
    """

    SCHEMA: type[JSONSchema] = JSONSchema
    """The JSON schema class for reports."""

    @abstractmethod
    def __init__(self) -> None:
        """Initialize MemoryInfo."""
        raise NotImplementedError("MemoryInfo is an abstract base class and cannot be instantiated")

    @classmethod
    @abstractmethod
    def from_dict(cls, data: dict[str, Any]) -> 'BaseMemoryInfo':
        """Create a MemoryInfo instance from a dictionary.

        .. code-block:: python
           :caption: Example

           json_memory_info = MemoryInfo.from_dict(data)

        :param data: The dictionary containing memory information.
        :return: A MemoryInfo instance.
        """
        raise NotImplementedError("from_dict is an abstract method and must be implemented by subclasses")

    @abstractmethod
    def to_dict(self) -> dict[str, Any]:
        """Convert the MemoryInfo to a dictionary.

        :return: A dictionary representation of the MemoryInfo.
        """
        raise NotImplementedError("to_dict is an abstract method and must be implemented by subclasses")
