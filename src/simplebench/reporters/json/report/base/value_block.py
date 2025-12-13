"""Base class for JSON value block representation."""
from abc import ABC, abstractmethod

from simplebench.base import Hydrator

from .json_schema import JSONSchema


class ValueBlock(Hydrator, ABC):
    """Base class representing a value block."""

    VERSION: int = 0
    """Version of the ValueBlock class."""

    TYPE: str = ""
    """Type of the ValueBlock class."""

    ID: str = ""
    """ID of the ValueBlock class."""

    SCHEMA: type[JSONSchema] = JSONSchema
    """JSON schema for the ValueBlock class."""

    @abstractmethod
    @classmethod
    def from_dict(cls, data: dict) -> "ValueBlock":
        """Create a ValueBlock instance from a dictionary.

        :param data: Dictionary containing the JSON results data.
        :return: JSONStatsSummary instance.
        """

    @abstractmethod
    def __init__(
            self,
           ) -> None:
        """Initialize ValueBlock class."""

    @abstractmethod
    def to_dict(self) -> dict:
        """Convert the ValueBlock instance to a dictionary."""
