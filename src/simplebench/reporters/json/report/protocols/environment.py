"""Protocol for execution environments."""
# pylint: disable=unnecessary-ellipsis
from typing import Any, Protocol, runtime_checkable


@runtime_checkable
class Environment(Protocol):
    """A protocol for classes that represent a specific execution environment."""

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> 'Environment':
        """Creates an instance from a dictionary."""
        ...

    def to_dict(self) -> dict[str, Any]:
        """Converts the instance to a dictionary."""
        ...

    def is_execution_environment(self) -> None:
        """This is a discriminator flag to indicate that the class is a
        valid environment for the purposes of this protocol. It is
        used to ensure that the class can be used as an environment in the
        execution environment.

        It takes and returns no values. It is a no-op.
        """
        ...
