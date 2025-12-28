"""ReportElement base class.

This class represents a report element in a report that can be serialized.

It implements validation and serialization/deserialization methods to and from dictionaries
for a JSON Schema version.
"""
from abc import ABC, abstractmethod
from typing import Any

from simplebench.base import Hydrator

from .json_schema import JSONSchema


class ReportElement(Hydrator, ABC):
    """abstract class representing a report element in a report."""

    VERSION: int = 0
    """The report element version number.

    It must be overridden in subclasses to specify the correct version.
    """

    TYPE: str = ""
    """The report element type property value.

    It must be overridden in subclasses to specify the correct type.
    """

    ID: str = ""
    """The report element $id property value.

    It must be overridden in subclasses to specify the correct $id.
    """

    SCHEMA: type[JSONSchema] = JSONSchema
    """The JSON schema class used to validate the report element class.

    It must be overridden in subclasses to specify the correct schema class.
    """
    def __init__(self) -> None:
        """Abstract base __init__ method for all report element classes."""
        raise NotImplementedError(
            "__init__ is an abstract method and must be implemented by a subclass."
        )

    @classmethod
    @abstractmethod
    def from_dict(cls, data: dict[str, Any]) -> 'ReportElement':
        """Create an instance of the element from a dictionary."""
        raise NotImplementedError(
                "from_dict is an abstract class method and must be implemented by a subclass")

    @abstractmethod
    def to_dict(self) -> dict[str, Any]:
        """Convert the element to a dictionary suitable for JSON serialization.

        This includes all properties defined in the implementing schema
        for the version.

        :return: A dictionary representation of the element.
        """
        raise NotImplementedError(
                "to_dict() is an abstract method must be implemented by a subclass")

    @property
    @abstractmethod
    def hash_id(self) -> str:
        """Return the hash ID of the element."""
        raise NotImplementedError(
                "hash_id is an abstract property and must be implemented by a subclass")
