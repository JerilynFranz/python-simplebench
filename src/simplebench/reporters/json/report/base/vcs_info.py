"""VCSInfo reporter base class.

This class represents VCS information in a JSON report.

It implements validation and serialization/deserialization methods to and from dictionaries
for the following JSON Schema version:

https://raw.githubusercontent.com/JerilynFranz/python-simplebench/main/schemas/v1/vcs-info.json

It is the base implemention of the JSON report vcs info representation.

This makes the implementations of VCSInfo backwards compatible with future versions
of the JSON report schema and the V1 implementation itself is essentially a frozen snapshot
of the base VCSInfo representation at the time of the V1 schema release.
"""
from abc import ABC, abstractmethod
from typing import Any

from simplebench.base import Hydrator

from .json_schema import JSONSchema


class VCSInfo(Hydrator, ABC):
    """Class representing VCS information in a JSON report."""

    VERSION: int = 0
    """The VCSInfo version number.
    It must be overridden in subclasses to specify the correct version.
    """

    TYPE: str = ""
    """The VCSInfo type property value.

    It must be overridden in subclasses to specify the correct type.
    """

    ID: str = ""
    """The VCSInfo $id property value.

    It must be overridden in subclasses to specify the correct $id.
    """

    SCHEMA: type[JSONSchema] = JSONSchema
    """The JSON schema class used to validate the VCSInfo.

    It must be overridden in subclasses to specify the correct schema class.
    """

    @abstractmethod
    def __init__(self) -> None:
        """Abstract base __init__ method for all VCSObjects."""
        raise NotImplementedError(
            "__init__ is an abstract method and must be implemented by a subclass."
        )

    @classmethod
    @abstractmethod
    def from_dict(cls, data: dict[str, Any]) -> 'VCSInfo':
        """Create a VCSInfo instance from a dictionary."""
        raise NotImplementedError(
                "from_dict is an abstract class method and must be implemented by a subclass")

    @abstractmethod
    def to_dict(self) -> dict[str, Any]:
        """Convert the VCSInfo to a dictionary suitable for JSON serialization.

        This includes all properties defined in the :class:`VCSInfoSchema`
        for the version.

        :return: A dictionary representation of the VCSInfo.
        """
        raise NotImplementedError(
                "to_dict() is an abstract method must be implemented by a subclass")

    @property
    @abstractmethod
    def hash_id(self) -> str:
        """Return the hash ID of the VCSInfo."""
        raise NotImplementedError(
                "hash_id is an abstract property and must be implemented by a subclass")
