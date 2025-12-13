"""Abstract Base Class for JSON reports."""
from __future__ import annotations

from abc import ABC, abstractmethod

from .hydrator import Hydrator
from .json_schema import JSONSchema


class Report(Hydrator, ABC):
    """Abstract Base class representing a JSON report."""

    VERSION: int = 0
    """The version of the JSON report schema this class implements."""

    TYPE: str = "SimpleBenchReport::V0"
    """The type of the JSON report schema this class implements."""

    SCHEMA: type[JSONSchema] = JSONSchema
    """The JSON schema class for this report version.

    Has to be overridden in subclasses.
    """
    @abstractmethod
    def __init__(self) -> None:
        """Initialize a Report base instance."""
        raise NotImplementedError("__init__ must be overridden in subclasses")

    @abstractmethod
    @classmethod
    def from_dict(cls, data: dict) -> Report:
        """Create a Report instance from a dictionary.

        :param data: Dictionary containing the JSON report data.
        :return: Report instance.
        :raises SimpleBenchValueError: If the version is not correct or if the data does not match the schema.
        """
        raise NotImplementedError("from_dict must be overridden in subclasses")

    @abstractmethod
    def to_dict(self) -> dict:
        """Convert the JSONReport instance to a dictionary.

        :return: Dictionary containing the JSON report data.
        """
        raise NotImplementedError("to_dict must be overridden in subclasses")
