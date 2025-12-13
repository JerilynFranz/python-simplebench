"""MachineInfo version 1 base class.

This class represents machine information in a JSON report.

It implements validation and serialization/deserialization methods to and from dictionaries
for the following JSON Schema version:

https://raw.githubusercontent.com/JerilynFranz/python-simplebench/main/schemas/v1/machine-info.json

It is the base implemention of the JSON report machine info representation.

This makes the implementations of JSONMachineInfo backwards compatible with future versions
of the JSON report schema and the V1 implementation itself is essentially a frozen snapshot
of the base MachineInfo representation at the time of the V1 schema release.
"""
import hashlib
import re
from typing import Any

from simplebench.exceptions import SimpleBenchTypeError
from simplebench.reporters.json.report.base import CPUInfo, ExecutionEnvironment, JSONSchema
from simplebench.reporters.json.report.base import MachineInfo as BaseMachineInfo
from simplebench.reporters.json.report.exceptions import _MachineInfoErrorTag
from simplebench.validators import validate_string, validate_type

from ..cpu_info import CPUInfo as CPUInfoV1
from ..execution_environment import ExecutionEnvironment as ExecutionEnvironmentV1
from .machine_info_schema import MachineInfoSchema


class MachineInfo(BaseMachineInfo):
    """Class representing machine information in a JSON report."""

    TYPE: str = MachineInfoSchema.TYPE
    """The JSON MachineInfo type property value for version 1 reports."""

    VERSION: int = MachineInfoSchema.VERSION
    """The JSON MachineInfo version number."""

    ID: str = MachineInfoSchema.ID
    """The JSON MachineInfo schema identifier for version 1 reports."""

    SCHEMA: type[JSONSchema] = MachineInfoSchema
    """The JSON schema class for version 1 reports."""

    def __init__(self,
                 *,
                 hash_id: str = '',
                 processor: str,
                 machine: str,
                 system: str,
                 release: str,
                 node: str = '',
                 execution_environment: ExecutionEnvironment,
                 cpu: CPUInfo) -> None:
        """Initialize JSONMachineInfo.

        :param hash_id: The unique hash identifier for the machine information.
            If not provided, it defaults to an empty string and will be computed automatically.
        :param processor: The processor string.
        :param machine: The machine string.
        :param system: The operating system name.
        :param release: The operating system release.
        :param node: The node string.
        :param execution_environment: The execution environment information.
        :param cpu: The CPU information.
        """
        self.hash_id = hash_id
        self.processor = processor
        self.machine = machine
        self.system = system
        self.release = release
        self.node = node
        self.execution_environment = execution_environment
        self.cpu = cpu

    @property
    def hash_id(self) -> str:
        """Get the hash_id property.

        :return: The hash_id string.
        """
        if self._hash_id == '':
            hash_keys = sorted(k for k in self.init_params() if k != 'hash_id')

            def get_val(key: str) -> Any:
                value = getattr(self, key)
                if hasattr(value, 'hash_id'):
                    return value.hash_id
                return value

            hash_input = "\x00".join(
                f"{key}:{get_val(key)}" for key in hash_keys
            ).encode('utf-8')
            self._hash_id = hashlib.sha256(hash_input).hexdigest()
        return self._hash_id

    @hash_id.setter
    def hash_id(self, value: str) -> None:
        """Set the hash_id property.

        It is validated to be a valid SHA-256 hexadecimal string or an empty string.

        :param value: The hash_id string to set.
        """
        hash_string = validate_string(
            value, "hash_id",
            _MachineInfoErrorTag.INVALID_HASH_ID_PROPERTY_TYPE,
            _MachineInfoErrorTag.INVALID_HASH_ID_PROPERTY_VALUE,
            allow_empty=True, strip=True)
        if hash_string == '':
            self._hash_id = ''
            return

        if not re.fullmatch(r'^[a-f0-9]{64}$', hash_string):
            raise SimpleBenchTypeError(
                "hash_id must be a valid SHA-256 hexadecimal string",
                tag=_MachineInfoErrorTag.INVALID_HASH_ID_PROPERTY_VALUE)
        self._hash_id: str = hash_string

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
    def execution_environment(self) -> ExecutionEnvironment:
        """Get the execution environment property.

        :return: The execution environment string.
        """
        return self._execution_environment

    @execution_environment.setter
    def execution_environment(self, value: ExecutionEnvironment) -> None:
        """Set the execution environment property.

        :param value: The execution environment to set.
        """
        self._execution_environment = validate_type(
            value, ExecutionEnvironment, "execution_environment",
            _MachineInfoErrorTag.INVALID_EXECUTION_ENVIRONMENT_PROPERTY_TYPE)

    @property
    def cpu(self) -> CPUInfo:
        """Get the CPU property.

        :return: The CPU info.
        """
        return self._cpu

    @cpu.setter
    def cpu(self, value: CPUInfo) -> None:
        """Set the CPU property.

        :param value: The CPU info to set.
        """
        self._cpu = validate_type(
            value, CPUInfo, "cpu",
            _MachineInfoErrorTag.INVALID_CPU_PROPERTY_TYPE)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> 'MachineInfo':
        """Create a MachineInfo instance from a dictionary.

        .. code-block:: python
           :caption: Example

           machine_info = MachineInfo.from_dict(data)

        :param data: The dictionary containing machine information.
        :return: A MachineInfo instance.
        """
        allowed_keys = cls.init_params()
        allowed_keys['version'] = int
        allowed_keys['type'] = str

        kwargs = cls.import_data(
            data=data,
            allowed=allowed_keys,
            skip={'version', 'type'},
            optional={'hash_id', 'node'},
            default={'hash_id': '', 'node': ''},
            match_on={'version': cls.VERSION, 'type': cls.TYPE},
            process_as={
                'execution_environment': ExecutionEnvironmentV1.from_dict,
                'cpu': CPUInfoV1.from_dict
            })
        return cls(**kwargs)

    def to_dict(self) -> dict[str, Any]:
        """Convert the MachineInfo to a dictionary.

        :return: A dictionary representation of the MachineInfo.
        """
        data: dict[str, Any] = {}
        for key in self.init_params():
            value = getattr(self, key)
            if hasattr(value, 'to_dict'):
                data[key] = value.to_dict()
            else:
                data[key] = value

        data['type'] = self.TYPE
        data['version'] = self.VERSION
        return data
