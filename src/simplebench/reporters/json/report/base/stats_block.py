"""Base class for JSON stats block representation.

This class represents a stats block information in a JSON report.

It implements validation and serialization/deserialization methods to and from dictionaries
for a stats block object.

It is the base implemention of the JSON report stats block representation.

This makes the implementations of StatsBlock backwards compatible with future versions
of the JSON report schema and the V1 implementation itself is essentially a frozen snapshot
of the base CPUInfo representation at the time of the V1 schema release.

"""
from abc import ABC, abstractmethod

from .hydrator import Hydrator
from .json_schema import JSONSchema


class StatsBlock(Hydrator, ABC):
    """Abstract Base class representing a JSON StatsBlock."""

    VERSION: int = 0
    """The version of the JSON stats block schema this class implements."""

    TYPE: str = ""
    """The type of the JSON stats block schema this class implements."""

    SCHEMA: type[JSONSchema] = JSONSchema
    """The JSON schema class for this report version.

    Has to be overridden in subclasses.
    """
    @abstractmethod
    def __init__(self) -> None:
        """Initialize a StatsBlock base instance."""
        raise NotImplementedError("__init__ must be overridden in subclasses")

    @abstractmethod
    @classmethod
    def from_dict(cls, data: dict) -> 'StatsBlock':
        """Create a StatsBlock instance from a dictionary.

        :param data: Dictionary containing the JSON stats block data.
        :return: StatsBlock instance.
        :raises SimpleBenchValueError: If the version is not correct or if the data does not match the schema.
        """
        raise NotImplementedError("from_dict must be overridden in subclasses")

    @abstractmethod
    def to_dict(self) -> dict:
        """Convert the StatsBlock instance to a dictionary.

        :return: Dictionary containing the JSON stats block data.
        """
        raise NotImplementedError("to_dict must be overridden in subclasses")
