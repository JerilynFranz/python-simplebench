"""Base class for JSON metadata representation."""
from __future__ import annotations

from abc import ABC
from typing import Any

from simplebench.exceptions import SimpleBenchValueError

from .exceptions import _JSONMetadataErrorTag


class JSONMetadata(ABC):
    """Base class representing JSON metadata."""

    @classmethod
    def from_dict(cls, data: dict) -> JSONMetadata:
        """Create a JSONMetadata instance from a dictionary.

        :param data: Dictionary containing the JSON metadata.
        :return: JSONMetadata instance.
        """
        cls.validate_type(data.get('type'), 'Metadata')
        return cls()

    @classmethod
    def validate_type(cls, found: Any, expected: str) -> str:
        """Validate the type.

        :param found: The type string to validate.
        :param expected: The expected type string.
        :return: The validated type string.
        :raise SimpleBenchTypeError: If the type is not a string.
        :raises SimpleBenchValueError: If the type is invalid.
        """
        if not isinstance(found, str):
            raise SimpleBenchValueError(
                f"type must be a string, got {type(found)}",
                tag=_JSONMetadataErrorTag.INVALID_TYPE_TYPE)
        if found != expected:
            raise SimpleBenchValueError(
                f"Incorrect type for JSONStatsSummary: {found} (expected '{expected}')",
                tag=_JSONMetadataErrorTag.INVALID_TYPE_VALUE)
        return found

    def __init__(self) -> None:
        """Initialize the JSONMetadata instance."""
