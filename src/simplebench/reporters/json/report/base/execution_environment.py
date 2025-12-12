"""ExecutionEnvironment base class.

This class represents execution environment information in a MachineInfo object.

It implements validation and serialization/deserialization methods to and from dictionaries
for the environment property for following JSON Schema version:

https://raw.githubusercontent.com/JerilynFranz/python-simplebench/main/schemas/v1/machine-info.json

It is the base implemention of the environment info representation property in MachineInfo objects,
not a standalone implementation of a JSON report schema.

The implementations of EnvironmentInfo are backwards compatible with future versions
of the JSON report schema and the V1 implementation itself is essentially a frozen snapshot
of the base EnvironmentInfo representation at the time of the V1 schema release.
"""
from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any

from simplebench.exceptions import SimpleBenchTypeError

from ..exceptions import _ExecutionEnvironmentErrorTag
from ..protocols import Environment


class ExecutionEnvironment(ABC):
    """Abstract class representing the execution_environment property for a machine-info object in a JSON report.
    """
    ALLOWED_ENVIRONMENTS: dict[str, type[Environment]] = {}
    """Dictionary mapping known execution environment types to their corresponding Environment subclasses.

    This must be overridden by subclasses to include the allowed execution environment types.
    """

    @abstractmethod
    def __init__(self) -> None:
        """Initialize EnvironmentInfo."""
        raise NotImplementedError("This method must be overridden by subclasses")

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> 'ExecutionEnvironment':
        """Create an ExecutionEnvironment instance from a dictionary.

        .. code-block:: python
           :caption: Example

           environment_info = ExecutionEnvironment.from_dict(data)

        :param data: The dictionary containing execution enviornment information.
        :return: A ExecutionEnvironment instance.
        """
        if not isinstance(data, dict):
            raise SimpleBenchTypeError(
                "data must be a dictionary",
                tag=_ExecutionEnvironmentErrorTag.INVALID_DATA_ARG_TYPE)    

        # Additional allowed execution environment types can be added here

        known_keys = set(cls.ALLOWED_ENVIRONMENTS.keys())
        extra_keys = set(data.keys()) - known_keys
        if extra_keys:
            raise SimpleBenchTypeError(
                f"Unexpected keys in data dictionary: {extra_keys}",
                tag=_ExecutionEnvironmentErrorTag.INVALID_DATA_ARG_EXTRA_KEYS)

        kwargs: dict[str, Environment] = {}
        for key, value in data.items():
            if key in cls.ALLOWED_ENVIRONMENTS:
                if not isinstance(value, dict):
                    raise SimpleBenchTypeError(
                        f"Value for key '{key}' must be a dictionary",
                        tag=_ExecutionEnvironmentErrorTag.INVALID_DATA_ARG_VALUE_TYPE)
                env_type = cls.ALLOWED_ENVIRONMENTS[key]
                kwargs[key] = env_type.from_dict(value)
            else:
                raise SimpleBenchTypeError(
                    f"Unexpected key in data dictionary: {key}",
                    tag=_ExecutionEnvironmentErrorTag.INVALID_DATA_ARG_EXTRA_KEYS)

        return cls(**kwargs)

    @abstractmethod
    def to_dict(self) -> dict[str, Any]:
        """Convert the ExecutionEnvironment to a dictionary.

        :return: A dictionary representation of the ExecutionEnvironment.
        """
        raise NotImplementedError("This method must be overridden by subclasses")

    @property
    @abstractmethod
    def hash_id(self) -> str:
        """Generate a unique hash ID for the ExecutionEnvironment.

        :return: A unique hash ID.
        """
        raise NotImplementedError("This method must be overridden by subclasses")
