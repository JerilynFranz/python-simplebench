"""MachineInfo version 1 base class.

This class represents machine information in a report.

It implements validation and serialization/deserialization methods to and from dictionaries
for the following JSON Schema version:

https://raw.githubusercontent.com/JerilynFranz/python-simplebench/main/schemas/v1/machine-info.json

It is the base implemention of the JSON report machine info representation.

This makes the implementations of JSONMachineInfo backwards compatible with future versions
of the JSON report schema and the V1 implementation itself is essentially a frozen snapshot
of the base MachineInfo representation at the time of the V1 schema release.
"""
import hashlib
from typing import TYPE_CHECKING, Any

from simplebench.report._base import BaseMachineInfo, JSONSchema
from simplebench.report.versions.v1.types import MachineInfoData, MachineInfoDict

from . import validate
from .machine_info_schema import MachineInfoSchema

_DEFERRED_IMPORTS_DONE: bool = False

if TYPE_CHECKING:
    from simplebench.report.versions.v1 import CPUInfo, ExecutionEnvironment, MemoryInfo, SystemInfo
    _DEFERRED_IMPORTS_DONE = True

else:
    CPUInfo = None  # pylint: disable=invalid-name
    ExecutionEnvironment = None  # pylint: disable=invalid-name
    MemoryInfo = None  # pylint: disable=invalid-name
    SystemInfo = None  # pylint: disable=invalid-name

def _deferred_imports() -> None:
    """Perform deferred imports to avoid circular dependencies."""
    global CPUInfo, ExecutionEnvironment, MemoryInfo, SystemInfo, _DEFERRED_IMPORTS_DONE  # pylint: disable=global-statement
    if _DEFERRED_IMPORTS_DONE:
        return
    from simplebench.report.versions.v1 import (  # pylint: disable=import-outside-toplevel
        CPUInfo,
        ExecutionEnvironment,
        MemoryInfo,
        SystemInfo,
    )
    _DEFERRED_IMPORTS_DONE = True

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
                 node: str = '',
                 cpu: CPUInfo,
                 memory: MemoryInfo,
                 system: SystemInfo,
                 execution_environment: ExecutionEnvironment) -> None:
        """Initialize JSONMachineInfo.

        :param str hash_id: The unique hash identifier for the machine information.
        :param str node: The node string.
        :param CPUInfo cpu: The CPU information.
        :param MemoryInfo memory: The memory information.
        :param SystemInfo system: The system information.
        :param ExecutionEnvironment execution_environment: The execution environment information.
        """
        self._hash_id = validate.hash_id(hash_id)
        self._node = validate.node(node)
        self._cpu = validate.cpu(cpu)
        self._memory = validate.memory(memory)
        self._system = validate.system(system)
        self._execution_environment = validate.execution_environment(execution_environment)

    @classmethod
    def from_dict(cls, data: MachineInfoData) -> 'MachineInfo':
        """Create a MachineInfo instance from a dictionary.

        .. code-block:: python
           :caption: Example

           machine_info = MachineInfo.from_dict(data)

        :param data: The dictionary containing machine information.
        :return: A MachineInfo instance.
        """
        _deferred_imports()

        allowed_keys = cls.init_params()
        allowed_keys['version'] = int
        allowed_keys['type'] = str

        kwargs = cls.import_data(
            data=data,
            allowed_fields=allowed_keys,
            skip_fields={'version', 'type'},
            optional_fields={'hash_id', 'node', 'version', 'type'},
            defaults={'hash_id': '', 'node': '', 'version': cls.VERSION, 'type': cls.TYPE},
            match_on={'version': cls.VERSION, 'type': cls.TYPE},
            process_as={
                'execution_environment': ExecutionEnvironment.from_dict,
                'cpu': CPUInfo.from_dict,
                'memory': MemoryInfo.from_dict,
                'system': SystemInfo.from_dict
            })
        return cls(**kwargs)

    def to_dict(self) -> MachineInfoDict:
        """Convert the MachineInfo to a dictionary.

        :return MachineInfoDict: A dictionary representation of the MachineInfo.
        """
        cls = self.__class__
        return MachineInfoDict(
            type=cls.TYPE,
            version=cls.VERSION,
            hash_id=self.hash_id,
            node=self.node,
            execution_environment=self.execution_environment.to_dict(),
            cpu=self.cpu.to_dict(),
            memory=self.memory.to_dict(),
            system=self.system.to_dict())

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

    @property
    def node(self) -> str:
        """Get the node property.

        :return: The node string.
        """
        return self._node

    @property
    def execution_environment(self) -> ExecutionEnvironment:
        """Get the execution environment property.

        :return: The execution environment string.
        """
        return self._execution_environment

    @property
    def cpu(self) -> CPUInfo:
        """Get the CPU property.

        :return: The CPU info.
        """
        return self._cpu

    @property
    def memory(self) -> MemoryInfo:
        """Get the memory property.

        :return: The memory info.
        """
        return self._memory

    @property
    def system(self) -> SystemInfo:
        """Get the system property.

        :return: The system info.
        """
        return self._system
