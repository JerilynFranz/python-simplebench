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

from abc import ABC

from ._environment import Environment
from .report_element import ReportElement

__all__ = []


class BaseExecutionEnvironment(ReportElement, ABC):
    """Abstract class representing the execution_environment property for a machine-info object in a JSON report."""

    ALLOWED_ENVIRONMENTS: dict[str, type[Environment]] = {}
    """Dictionary mapping known execution environment types to their corresponding Environment subclasses.

    This must be overridden by subclasses to include the allowed execution environment types.
    """
