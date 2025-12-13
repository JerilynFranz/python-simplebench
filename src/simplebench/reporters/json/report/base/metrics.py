"""Metrics base class.

This class represents execution environment information in a MachineInfo object.

It implements validation and serialization/deserialization methods to and from dictionaries
for the metrics property for following JSON Schema version:

https://raw.githubusercontent.com/JerilynFranz/python-simplebench/main/schemas/v1/results-info.json

It is the base implemention of the metrics representation property in ResultsInfo objects,
not a standalone implementation of a JSON report schema.

The implementations of Metrics are backwards compatible with future versions
of the JSON report schema and the V1 implementation itself is essentially a frozen snapshot
of the base Metrics representation at the time of the V1 schema release.
"""
from abc import ABC, abstractmethod
from typing import Any, TypeAlias


class Metrics(ABC):
    """Abstract class representing the metrics property for a results info object in a JSON report.
    """

    MetricItem: TypeAlias
    """Type alias for allowed metric items in the metrics property.

    Must be overridden by subclasses to specify the actual types allowed for metric items.
    """

    @abstractmethod
    def __init__(self) -> None:
        """Initialize Metrics."""
        raise NotImplementedError("This method must be overridden by subclasses")

    @abstractmethod
    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> 'Metrics':
        """Create a Metrics instance from a dictionary.

        .. code-block:: python
           :caption: Example

           metrics = Metrics.from_dict(data)

        :param data: The dictionary containing metrics information.
        :return: A Metrics instance.
        """
        raise NotImplementedError("This method must be overridden by subclasses")

    @abstractmethod
    def to_dict(self) -> dict[str, Any]:
        """Convert the Metrics to a dictionary.

        :return: A dictionary representation of the Metrics.
        """
        raise NotImplementedError("This method must be overridden by subclasses")
