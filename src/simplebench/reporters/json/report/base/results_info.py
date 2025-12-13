"""report Results base class.

This class represents Results in a JSON report.

It implements validation and serialization/deserialization methods to and from dictionaries
for the results property object in the following JSON Schema version:

https://raw.githubusercontent.com/JerilynFranz/python-simplebench/main/schemas/v1/results-info.json

It is the base implemention of the JSON results object representation.

This makes the implementations of Results backwards compatible with future versions
of the JSON report schema and the V1 implementation itself is essentially a frozen snapshot
of the results object representation at the time of the V1 schema release."""
from abc import ABC, abstractmethod

from .hydrator import Hydrator
from .json_schema import JSONSchema


class ResultsInfo(Hydrator, ABC):
    """Base class representing JSON results."""

    VERSION: int = 0
    """The JSON results version number.

    :note: This should be overridden in sub-classes."""

    TYPE: str = ""
    """The JSON results type.

    :note: This should be overridden in sub-classes."""

    ID: str = ""
    """The JSON results ID.

    :note: This should be overridden in sub-classes.
    """

    SCHEMA: type[JSONSchema] = JSONSchema
    """The JSON schema for the JSON results object.

    :note: This should be overridden in sub-classes.
    """

    @abstractmethod
    def __init__(self) -> None:
        """Initialize a ResultsInfo instance.

        :note: This should be overridden in sub-classes.
        """
        raise NotImplementedError("This method should be overridden in sub-classes")

    @abstractmethod
    @classmethod
    def from_dict(cls, data: dict) -> 'ResultsInfo':
        """Create a JSON Results object instance from a dictionary.

        :param data: Dictionary containing the JSON results object data.
        :return: JSON Results object instance.
        """
        raise NotImplementedError("This method should be overridden in sub-classes")

    @abstractmethod
    def to_dict(self) -> dict:
        """Convert the JSON Results object instance to a dictionary.

        :return: Dictionary containing the JSON results object data.
        """
        raise NotImplementedError("This method should be overridden in sub-classes")
