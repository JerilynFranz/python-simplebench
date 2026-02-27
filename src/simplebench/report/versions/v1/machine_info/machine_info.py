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
from collections.abc import Mapping, Sequence
from types import MappingProxyType
from typing import TYPE_CHECKING, Any, cast

from simplebench.exceptions import SimpleBenchTypeError
from simplebench.report._error_tags import _MachineInfoErrorTag
from simplebench.report.base import BaseMachineInfo, JSONSchema
from simplebench.simplebench_types import CoreDataMapping, CoreDataSequence

from ..environment_info import EnvironmentInfoData, ImmutableEnvironmentInfoData
from . import _validate
from .machine_info_schema import MachineInfoSchema
from .typeddict_types import ImmutableMachineInfoData, ImmutableMachineInfoDict, MachineInfoData

if TYPE_CHECKING:
    from simplebench.report.versions.v1 import CPUInfo, EnvironmentInfo, MemoryInfo, SystemInfo

__all__: list[str] = []


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

    _init_params_cache: MappingProxyType[str, Any] | None = None
    """Cache for the constructor parameters of the MachineInfo class."""

    @classmethod
    def _data_params(cls) -> MappingProxyType[str, Any]:
        """Get the constructor parameters for the schema data class.

        The parameters are cached after the first call for performance.

        It is returned as a read-only mapping and includes 'type' and 'version'.

        :return MappingProxyType[str, Any]: A read-only mapping of constructor parameter names and types.
        """
        from simplebench.report.versions.v1 import CPUInfo, EnvironmentInfo, MemoryInfo, SystemInfo
        if not cls._init_params_cache:
            cls._init_params_cache = MappingProxyType({
                'hash_id': str,
                'node': str,
                'cpu': CPUInfo,
                'memory': MemoryInfo,
                'system': SystemInfo,
                'environment': Sequence[EnvironmentInfo],
                'type': str,
                'version': int,
            })
        return cls._init_params_cache

    __slots__ = (
        '_hash_id',
        '_node',
        '_environment',
        '_cpu',
        '_memory',
        '_system',
        '_to_dict',
    )
    """Slots for MachineInfo instance attributes."""
    def __init__(
        self,
        *,
        hash_id: str = '',
        node: str = '',
        cpu: 'CPUInfo',
        memory: 'MemoryInfo',
        system: 'SystemInfo',
        environment: Sequence['EnvironmentInfo'],
    ) -> None:
        """Initialize JSONMachineInfo.

        :param str hash_id: The unique hash identifier for the machine information.
        :param str node: The node string.
        :param CPUInfo cpu: The CPU information.
        :param MemoryInfo memory: The memory information.
        :param SystemInfo system: The system information.
        :param Sequence[EnvironmentInfo] environment: The execution environment information.
        :raises SimpleBenchTypeError: If any of the parameters are of incorrect type.
        :raises SimpleBenchValueError: If any of the parameters have invalid values.
        """
        self._hash_id = _validate.hash_id(hash_id)
        self._node = _validate.node(node)
        self._cpu = _validate.cpu(cpu)
        self._memory = _validate.memory(memory)
        self._system = _validate.system(system)
        self._environment = _validate.environment(environment)
        if self._hash_id == '':
            self._hash_id = self._hash_id_helper(ImmutableMachineInfoDict)
        self._to_dict: ImmutableMachineInfoDict | None = None

    @classmethod
    def from_dict(cls, data: MachineInfoData | ImmutableMachineInfoData) -> 'MachineInfo':
        """Create a MachineInfo instance from a dictionary.

        .. code-block:: python
           :caption: Example

           machine_info = MachineInfo.from_dict(data)

        :param data: The dictionary containing machine information.
        :return MachineInfo: A MachineInfo instance.
        """
        from simplebench.report.versions.v1 import (  # pylint: disable=import-outside-toplevel
            CPUInfo,
            MemoryInfo,
            SystemInfo,
        )
        allowed_keys: dict[str, type] = dict(cls._data_params())

        kwargs = cls.import_data(
            data=data,
            allowed_fields=allowed_keys,
            skip_fields={'version', 'type'},
            optional_fields={'hash_id', 'node', 'version', 'type', 'environment'},
            defaults={'hash_id': '', 'node': '', 'version': cls.VERSION, 'type': cls.TYPE, 'environment': tuple()},
            match_on={'version': cls.VERSION, 'type': cls.TYPE},
            process_as={
                'cpu': CPUInfo.from_dict,
                'memory': MemoryInfo.from_dict,
                'system': SystemInfo.from_dict,
                'environment': cls._environment_info_from_sequence,
            },
        )
        return cls(**kwargs)

    @classmethod
    def _environment_info_from_sequence(
            cls,
            environment: Sequence[EnvironmentInfoData | ImmutableEnvironmentInfoData]
        ) -> tuple['EnvironmentInfo', ...]:
        """Helper method to create a tuple of EnvironmentInfo instances from the environment data
        in the input dictionary.

        :param environment: The sequence of environment data dictionaries.
        :return tuple[EnvironmentInfo, ...]: A tuple of EnvironmentInfo instances created from the environment data.
        :raises SimpleBenchTypeError: If the 'environment' key is present but is not a sequence of dictionaries.
        """
        from simplebench.report.versions.v1 import EnvironmentInfo, PythonInfo, PythonInfoData

        python_semantic_type = PythonInfo.SEMANTIC_TYPE

        env_data: list[EnvironmentInfo] = []
        if not isinstance(environment, Sequence) or isinstance(environment, (str, bytes)):
            raise SimpleBenchTypeError(
                f"The 'environment' property must be a Sequence, got {type(environment).__name__}",
                tag=_MachineInfoErrorTag.INVALID_ENVIRONMENT_PROPERTY_TYPE,
            )
        for env in environment:
            if not isinstance(env, Mapping):
                raise SimpleBenchTypeError(
                    f"Each item in the 'environment' property must be a Mapping, got {type(env).__name__}",
                    tag=_MachineInfoErrorTag.INVALID_ENVIRONMENT_PROPERTY_TYPE,
                )
            semantic_type: str | None = env.get('semantic_type', None)
            if semantic_type is None:
                raise SimpleBenchTypeError(
                    "Each item in the 'environment' property must have a 'semantic_type' key",
                    tag=_MachineInfoErrorTag.INVALID_ENVIRONMENT_PROPERTY_TYPE,
                )
            elif semantic_type == python_semantic_type:
                env_data.append(PythonInfo.from_dict(cast(PythonInfoData, env)))
            else:
                env_data.append(EnvironmentInfo.from_dict(env))
        return tuple(env_data)

    def to_dict(self) -> ImmutableMachineInfoDict:
        """Convert the MachineInfo to a dictionary.

        The returned dictionary conforms to the MachineInfo JSON schema
        and the :class:`ImmutableMachineInfoDict` TypedDict definition.

        :return ImmutableMachineInfoDict: A dictionary representation of the MachineInfo.
        """
        if self._to_dict is None:
            self._to_dict = cast(ImmutableMachineInfoDict,
                CoreDataMapping({
                    'hash_id': self.hash_id,
                    'node': self.node,
                    'cpu': self.cpu.to_dict(),  # type: ignore
                    'memory': self.memory.to_dict(),  # type: ignore
                    'system': self.system.to_dict(),  # type: ignore
                    'environment': CoreDataSequence(tuple(env.to_dict() for env in self.environment)),  # type: ignore
                    'type': self.TYPE,
                    'version': self.VERSION,
                })) # type: ignore
        return self._to_dict

    def for_json(self) -> ImmutableMachineInfoDict:
        """Get the JSON-serializable dictionary representation of this MachineInfo.

        This method delegates to the for_json method of the dictionary returned by :meth:`to_dict`
        because the dictionary is actually an instance of :class:`CoreDataMapping`
        which has the for_json method to convert to a JSON-serializable dictionary.

        :return: The JSON-serializable dictionary representation of this MachineInfo.
        """
        return self.to_dict().for_json()  # type: ignore

    def as_json(self) -> str:
        """Get the JSON string representation of this MachineInfo.

        This method delegates to the as_json method of the dictionary returned by :meth:`to_dict`
        because the dictionary is actually an instance of :class:`CoreDataMapping`
        which has the as_json method to convert to a JSON string.

        :return: The JSON string representation of this MachineInfo.
        """
        return self.to_dict().as_json()  # type: ignore

    @property
    def hash_id(self) -> str:
        """Get the hash_id property.

        :return: The hash_id string.
        """
        return self._hash_id

    @property
    def node(self) -> str:
        """Get the node property.

        :return: The node string.
        """
        return self._node

    @property
    def environment(self) -> tuple['EnvironmentInfo', ...]:
        """Get the environment property.

        :return: The execution environment info.
        """
        return self._environment

    @property
    def cpu(self) -> 'CPUInfo':
        """Get the CPU property.

        :return: The CPU info.
        """
        return self._cpu

    @property
    def memory(self) -> 'MemoryInfo':
        """Get the memory property.

        :return: The memory info.
        """
        return self._memory

    @property
    def system(self) -> 'SystemInfo':
        """Get the system property.

        :return: The system info.
        """
        return self._system

    def __repr__(self) -> str:
        """Get the string representation of this MachineInfo instance.

        :return: The string representation of this MachineInfo instance.
        """
        return (f"MachineInfo(hash_id={self.hash_id!r}, node={self.node!r}, "
                f"cpu={self.cpu!r}, memory={self.memory!r}, system={self.system!r}, "
                f"environment={self.environment!r})")

    def __eq__(self, other: object) -> bool:
        """Check equality with another MachineInfo instance.

        Two MachineInfo instances are considered equal if their hash_id properties are equal.

        :param other: The other object to compare with.
        :return: True if the other object is a MachineInfo instance with the same hash_id, False otherwise.
        """
        if not isinstance(other, MachineInfo):
            return NotImplemented
        return self.hash_id == other.hash_id

    def __hash__(self) -> int:
        """Get the hash of this MachineInfo instance.

        The hash is based on the hash_id property which is a unique identifier for the machine information.

        :return: The hash of this MachineInfo instance.
        """
        return hash(self._hash_id)

    def __copy__(self) -> 'MachineInfo':
        """Create a copy of this MachineInfo instance.

        :return: A copy of this MachineInfo instance.
        """
        return self

    def __deepcopy__(self, memo: dict[int, object]) -> 'MachineInfo':
        """Create a deep copy of this MachineInfo instance.

        :param memo: The memoization dictionary for deep copy.
        :return: A deep copy of this MachineInfo instance.
        """
        return self
