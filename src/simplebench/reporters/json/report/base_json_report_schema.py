"""Base JSON report schema classes."""
from abc import ABC, abstractmethod


class JSONReportSchema(ABC):
    """Abstract Base class representing a JSON report schema."""

    @classmethod
    @abstractmethod
    def json_schema_dict(cls) -> dict:
        """Return the JSON schema as a dictionary.

        :return: JSON schema dictionary.
        """
        raise NotImplementedError("json_schema_dict must be implemented in subclasses.")

    @abstractmethod
    def to_json_schema(self) -> str:
        """Return the JSON schema as a string.

        :return: JSON schema string.
        """
        raise NotImplementedError("to_json_schema must be implemented in subclasses.")
