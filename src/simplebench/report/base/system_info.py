"""SystemInfo reporter base class.

This class represents System information in a report.

It implements validation and serialization/deserialization methods to and from dictionaries
for the following JSON Schema version:

https://raw.githubusercontent.com/JerilynFranz/python-simplebench/main/schemas/v1/system-info.json

It is the base implemention of the report system info representation.

This makes the implementations of SystemInfo backwards compatible with future versions
of the report schema and the V1 implementation itself is essentially a frozen snapshot
of the base SystemInfo representation at the time of the V1 schema release.
"""
from abc import ABC, abstractmethod
from typing import Any

from simplebench.base import Hydrator

from .json_schema import JSONSchema


class BaseSystemInfo(Hydrator, ABC):
    """Class representing System information in a JSON report."""

    VERSION: int = 0
    """The SystemInfo version number.

    It must be overridden in subclasses to specify the correct version.
    """

    TYPE: str = ""
    """The SystemInfo type property value.

    It must be overridden in subclasses to specify the correct type.
    """

    ID: str = ""
    """The SystemInfo $id property value.

    It must be overridden in subclasses to specify the correct $id.
    """

    SCHEMA: type[JSONSchema] = JSONSchema
    """The JSON schema class used to validate the SystemInfo.

    It must be overridden in subclasses to specify the correct schema class.
    """

    @abstractmethod
    def __init__(self) -> None:
        """Abstract base __init__ method for all SystemObjects."""
        raise NotImplementedError(
            "__init__ is an abstract method and must be implemented by a subclass."
        )

    @classmethod
    @abstractmethod
    def from_dict(cls, data: dict[str, Any]) -> 'BaseSystemInfo':
        """Create a SystemInfo instance from a dictionary."""
        raise NotImplementedError(
                "from_dict is an abstract class method and must be implemented by a subclass")

    @abstractmethod
    def to_dict(self) -> dict[str, Any]:
        """Convert the SystemInfo to a dictionary suitable for JSON serialization.

        This includes all properties defined in the :class:`SystemInfoSchema`
        for the version.

        :return: A dictionary representation of the SystemInfo.
        """
        raise NotImplementedError(
                "to_dict() is an abstract method must be implemented by a subclass")

    @property
    @abstractmethod
    def hash_id(self) -> str:
        """Return the hash ID of the SystemInfo."""
        raise NotImplementedError(
                "hash_id is an abstract property and must be implemented by a subclass")
