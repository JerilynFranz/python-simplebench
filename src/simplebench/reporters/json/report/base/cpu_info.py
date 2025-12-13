"""CPUInfo reporter base class.

This class represents CPU information in a JSON report.

It implements validation and serialization/deserialization methods to and from dictionaries
for the following JSON Schema version:

https://raw.githubusercontent.com/JerilynFranz/python-simplebench/main/schemas/v1/cpu-info.json

It is the base implemention of the JSON report cpu info representation.

This makes the implementations of CPUInfo backwards compatible with future versions
of the JSON report schema and the V1 implementation itself is essentially a frozen snapshot
of the base CPUInfo representation at the time of the V1 schema release.
"""
from abc import ABC, abstractmethod
from typing import Any

from .hydrator import Hydrator
from .json_schema import JSONSchema


class CPUInfo(Hydrator, ABC):
    """Class representing CPU information in a JSON report."""

    VERSION: int = 0
    """The CPUInfo version number.

    It must be overridden in subclasses to specify the correct version.
    """

    TYPE: str = ""
    """The CPUInfo type property value.

    It must be overridden in subclasses to specify the correct type.
    """

    ID: str = ""
    """The CPUInfo $id property value.

    It must be overridden in subclasses to specify the correct $id.
    """

    SCHEMA: type[JSONSchema] = JSONSchema
    """The JSON schema class used to validate the CPUInfo.

    It must be overridden in subclasses to specify the correct schema class.
    """

    @abstractmethod
    def __init__(self) -> None:
        """Abstract base __init__ method for all CPUObjects."""
        raise NotImplementedError(
            "__init__ is an abstract method and must be implemented by a subclass."
        )

    @abstractmethod
    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> 'CPUInfo':
        """Create a CPUInfo instance from a dictionary."""
        raise NotImplementedError(
                "from_dict is an abstract class method and must be implemented by a subclass")

    @abstractmethod
    def to_dict(self) -> dict[str, Any]:
        """Convert the CPUInfo to a dictionary suitable for JSON serialization.

        This includes all properties defined in the :class:`CPUInfoSchema`
        for the version.

        :return: A dictionary representation of the CPUInfo.
        """
        raise NotImplementedError(
                "to_dict() is an abstract method must be implemented by a subclass")

    @property
    @abstractmethod
    def hash_id(self) -> str:
        """Return the hash ID of the CPUInfo."""
        raise NotImplementedError(
                "hash_id is an abstract property and must be implemented by a subclass")
