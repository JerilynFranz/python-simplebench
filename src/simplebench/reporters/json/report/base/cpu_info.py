"""JSONCPUInfo reporter base class.

This class represents CPU information in a JSON report.

It implements validation and serialization/deserialization methods to and from dictionaries
for the following JSON Schema version:

https://raw.githubusercontent.com/JerilynFranz/python-simplebench/main/schemas/v1/cpu-info.json

It is the base implemention of the JSON report cpu info representation.

This makes the implementations of JSONCPUInfo backwards compatible with future versions
of the JSON report schema and the V1 implementation itself is essentially a frozen snapshot
of the base JSONCPUInfo representation at the time of the V1 schema release.
"""
from typing import Any

from simplebench.exceptions import SimpleBenchTypeError
from simplebench.validators import validate_string, validate_type

from ..exceptions import _MachineInfoErrorTag


class CPUInfo:
    """Class representing CPU information in a JSON report."""

    def __init__(self,
                 *,
                 processor: str,
                 machine: str,
                 system: str,
                 release: str,
                 node: str = '',
                 execution_environment: JSONExecutionEnvironment,
                 cpu: JSONCPUInfo) -> None:
        """Initialize JSONMachineInfo.

        :param processor: The processor string.
        :param machine: The machine string.
        :param system: The operating system name.
        :param release: The operating system release.
        :param node: The node string.
        :param execution_environment: The execution environment information.
        :param cpu: The CPU information.
        """

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> 'CPUInfo':
        """Create a JSONCPUInfo instance from a dictionary.

        .. code-block:: python
           :caption: Example

           json_cpu_info = JSONCPUInfo.from_dict(data)

        :param data: The dictionary containing CPU information.
        :return: A JSONCPUInfo instance.
        """
        if not isinstance(data, dict):
            raise SimpleBenchTypeError(
                "data must be a dictionary",
                tag=_MachineInfoErrorTag.INVALID_DATA_ARG_TYPE)
        known_keys = {
            'processor',
            'machine',
            'system',
            'release',
            'node',
            'execution_environment',
            'cpu',
        }
        extra_keys = set(data.keys()) - known_keys
        if extra_keys:
            raise SimpleBenchTypeError(
                f"Unexpected keys in data dictionary: {extra_keys}",
                tag=_MachineInfoErrorTag.INVALID_DATA_ARG_EXTRA_KEYS)

        missing_keys = known_keys - data.keys() - {'node'}
        if missing_keys:
            raise SimpleBenchTypeError(
                f"Missing required keys in data dictionary: {missing_keys}",
                tag=_MachineInfoErrorTag.INVALID_DATA_ARG_MISSING_KEYS)

        instance = cls(
            processor=data['processor'],
            machine=data['machine'],
            system=data['system'],
            release=data['release'],
            node=data.get('node', ''),
            execution_environment=JSONExecutionEnvironment.from_dict(data['execution_environment']),
            cpu=CPUInfo.from_dict(data['cpu'])
        )

        return instance

    @property
    def processor(self) -> str:
        """Get the processor property.

        :return: The processor string.
        """
        return self._processor

    @processor.setter
    def processor(self, value: str) -> None:
        """Set the processor property.

        :param value: The processor string to set.
        """

        self._processor: str = validate_string(
            value, "processor",
            _MachineInfoErrorTag.INVALID_PROCESSOR_PROPERTY_TYPE,
            _MachineInfoErrorTag.EMPTY_PROCESSOR_PROPERTY_VALUE,
            allow_empty=False)

    @property
    def machine(self) -> str:
        """Get the machine property.

        :return: The machine string.
        """
        return self._machine

    @machine.setter
    def machine(self, value: str) -> None:
        """Set the machine property.

        :param value: The machine string to set.
        """

        self._machine: str = validate_string(
            value, "machine",
            _MachineInfoErrorTag.INVALID_MACHINE_PROPERTY_TYPE,
            _MachineInfoErrorTag.EMPTY_MACHINE_PROPERTY_VALUE,
            allow_empty=False)

    @property
    def system(self) -> str:
        """Get the system OS property.

        :return: The system OS string.
        """
        return self._system

    @system.setter
    def system(self, value: str) -> None:
        """Set the system OS property.

        :param value: The system OS string to set.
        """
        self._system: str = validate_string(
            value, "system",
            _MachineInfoErrorTag.INVALID_SYSTEM_PROPERTY_TYPE,
            _MachineInfoErrorTag.INVALID_SYSTEM_PROPERTY_VALUE,
            allow_empty=False)

    @property
    def release(self) -> str:
        """Get the OS release property.

        :return: The release string.
        """
        return self._release

    @release.setter
    def release(self, value: str) -> None:
        """Set the OS release property.

        :param value: The OS release string to set.
        """
        self._release: str = validate_string(
            value, "release",
            _MachineInfoErrorTag.INVALID_RELEASE_PROPERTY_TYPE,
            _MachineInfoErrorTag.INVALID_RELEASE_PROPERTY_VALUE,
            allow_empty=False)

    @property
    def node(self) -> str:
        """Get the node property.

        :return: The node string.
        """
        return self._node

    @node.setter
    def node(self, value: str) -> None:
        """Set the node property.

        :param value: The node string to set.
        """
        self._node: str = validate_string(
            value, "node",
            _MachineInfoErrorTag.INVALID_NODE_PROPERTY_TYPE,
            _MachineInfoErrorTag.EMPTY_NODE_PROPERTY_VALUE,
            allow_empty=True, strip=True)

    @property
    def execution_environment(self) -> JSONExecutionEnvironment:
        """Get the execution environment property.

        :return: The execution environment string.
        """
        return self._execution_environment

    @execution_environment.setter
    def execution_environment(self, value: JSONExecutionEnvironment) -> None:
        """Set the execution environment property.

        :param value: The execution environment to set.
        """
        self._execution_environment = validate_type(
            value, JSONExecutionEnvironment, "execution_environment",
            _MachineInfoErrorTag.INVALID_EXECUTION_ENVIRONMENT_PROPERTY_TYPE)

    @property
    def cpu(self) -> JSONCPUInfo:
        """Get the CPU property.

        :return: The CPU info.
        """
        return self._cpu

    @cpu.setter
    def cpu(self, value: JSONCPUInfo) -> None:
        """Set the CPU property.

        :param value: The CPU info to set.
        """
        self._cpu = validate_type(
            value, CPUInfo, "cpu",
            _MachineInfoErrorTag.INVALID_CPU_PROPERTY_TYPE)

    def to_dict(self) -> dict[str, Any]:
        """Convert the JSONMachineInfo to a dictionary.

        :return: A dictionary representation of the JSONMachineInfo.
        """
        result: dict[str, Any] = {
            'processor': self.processor,
            'machine': self.machine,
            'system': self.system,
            'release': self.release,
            'node': self.node,
            'execution_environment': self.execution_environment.to_dict(),
            'cpu': self.cpu.to_dict(),
        }
        return result
