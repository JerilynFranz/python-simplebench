"""Base class for JSON value block representation."""
from abc import ABC, abstractmethod
from collections.abc import Hashable

from simplebench.base import Hydrator

from .json_schema import JSONSchema


class RawDataBlock(Hydrator, Hashable, ABC):
    """Base class representing a raw data block."""

    VERSION: int = 0
    """Version of the RawDataBlock class."""

    TYPE: str = ""
    """Type of the RawDataBlock class."""

    ID: str = ""
    """ID of the RawDataBlock class."""

    SCHEMA: type[JSONSchema] = JSONSchema
    """JSON schema for the RawDataBlock class."""

    @classmethod
    @abstractmethod
    def from_dict(cls, data: dict) -> "RawDataBlock":
        """Create a RawDataBlock instance from a dictionary.

        :param data: Dictionary containing the JSON results data.
        :return: RawDataBlock instance.
        """

    @abstractmethod
    def __init__(
            self,
           ) -> None:
        """Initialize RawDataBlock class."""

    @abstractmethod
    def to_dict(self) -> dict:
        """Convert the RawDataBlock instance to a dictionary."""
