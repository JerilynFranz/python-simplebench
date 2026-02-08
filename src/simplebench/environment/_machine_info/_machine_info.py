"""Utility functions to get machine information."""

import platform
from types import MappingProxyType
from typing import TYPE_CHECKING, ClassVar, cast

from simplebench.environment._cpu_info import CPUInfo
from simplebench.environment._memory_info import MemoryInfo
from simplebench.environment._python_info import PythonInfo
from simplebench.environment._system_info import SystemInfo

from . import _validate

if TYPE_CHECKING:
    from simplebench.report.versions import v1 as report

class MachineInfo:
    """Data class holding information about the current machine and execution environment."""

    __slots__ = ('_node', '_cpu', '_python', '_system', '_memory', '_dict_cache', '_report_machine_info')

    def __init__(self, *,
                 node: str | None, cpu: CPUInfo, python: PythonInfo, system: SystemInfo, memory: MemoryInfo) -> None:
        """Post-initialization to validate the object's fields.

        The 'execution_environment' field is constructed from the 'python' field for
        compatibility with report MachineInfo structure.

        """
        from simplebench.report.versions import v1 as report

        self._node: str | None = _validate.node(node)
        self._cpu: CPUInfo = _validate.cpu_info(cpu)
        self._python: PythonInfo = _validate.python_info(python)
        self._system: SystemInfo = _validate.system_info(system)
        self._memory: MemoryInfo = _validate.memory_info(memory)
        self._dict_cache: MappingProxyType[str, object] = MappingProxyType({
            'node': self.node,
            'cpu': self.cpu.to_dict(),
            'execution_environment': MappingProxyType({'python': self.python.to_dict()}),
            'system': self.system.to_dict(),
            'memory': self.memory.to_dict(),
        })
        self._report_machine_info: report.MachineInfo = report.MachineInfo.from_dict(self._to_dict())

    @property
    def node(self) -> str | None:
        """The node name of the machine.

        :return str | None: The node name.
        """
        return self._node

    @property
    def cpu(self) -> CPUInfo:
        """The CPU information of the machine.

        :return CPUInfo: The CPU information.
        """
        return self._cpu

    @property
    def python(self) -> PythonInfo:
        """The Python environment information of the machine.

        :return PythonInfo: The Python environment information.
        """
        return self._python

    @property
    def system(self) -> SystemInfo:
        """The system information of the machine.

        :return SystemInfo: The system information.
        """
        return self._system

    @property
    def memory(self) -> MemoryInfo:
        """The memory information of the machine.

        :return MemoryInfo: The memory information.
        """
        return self._memory

    @property
    def execution_environment(self) -> dict[str, object]:
        """The execution environment information of the machine.

        This is a dictionary containing the Python environment
        information, structured for compatibility with report MachineInfo.

        :return dict: The execution environment information.
        """
        return self._dict_cache['execution_environment']  # type: ignore[return-value]

    @property
    def as_report_machine_info(self) -> 'report.MachineInfo':
        """The :class:`simplebench.report.versions.v1.MachineInfo` representation of the
        :class:`simplebench.environment.MachineInfo` instance.

        :return report.MachineInfo: The ReportMachineInfo representation of the MachineInfo instance.
        """
        return self._report_machine_info

    def _to_dict(self) -> 'report.ImmutableMachineInfoData':
        """Convert the MachineInfo instance to a dictionary. The dictionary
        conforms to the :class:`simplebench.report.versions.v1.ImmutableMachineInfoData` type
        which means it can be directly for importing into report MachineInfo objects
        via :meth:`simplebench.report.versions.v1.MachineInfo.from_dict`.

        :return dict: A dictionary representation of the MachineInfo instance.
        """
        return cast('report.ImmutableMachineInfoData', self._dict_cache)

class MachineInfoFactory:
    """Factory for creating and caching MachineInfo instances.

    This factory uses caching to avoid redundant creation of MachineInfo instances.
    It supports caching based on a cache key and allows for fresh instances to be created
    when requested.

    It collects core information once and reuses it for subsequent instances,
    unless a fresh instance is requested.

    .. code-block:: python
        from simplebench.environment import MachineInfoFactory

        # Machine info with default node name (empty string)
        machine_info_default = MachineInfoFactory.create(node='')

        machine_info = MachineInfoFactory.create(node=None)
        # Machine info with the real node name

        machine_info_fresh = MachineInfoFactory.create(node=None, fresh=True)
        # Fresh machine info with the real node name

        machine_info_cached = MachineInfoFactory.create(cache_key='my_cache_key')
        # Cached machine info with the real node name
    """

    _cached_core_info: ClassVar[MachineInfo | None] = None
    _real_node_name: ClassVar[str] = ''
    _keyed_cache: ClassVar[dict[str, 'MachineInfo']] = {}

    @classmethod
    def _get_core_info(cls) -> MachineInfo:
        """Get core machine info, from cache or by creating it.

        :return MachineInfo: The core MachineInfo instance.
        """
        if cls._cached_core_info is None:
            cls._cached_core_info = MachineInfo(
                node='', cpu=CPUInfo(), python=PythonInfo(), system=SystemInfo(), memory=MemoryInfo()
            )
        return cls._cached_core_info

    @classmethod
    def _get_real_node_name(cls) -> str:
        """Get the real node name, from cache or by calling platform.node().

        :return str: The real node name.
        """
        if not cls._real_node_name:
            cls._real_node_name = platform.node()
        return cls._real_node_name

    @classmethod
    def create(cls, node: str | None = '', cache_key: str | None = None, fresh: bool = False) -> MachineInfo:
        """
        Create a MachineInfo instance, using caching to avoid redundant work.

        :param str | None node: The node name to use. If `None`, the real node name is used.
        :param str | None cache_key: An optional cache key to store/retrieve a MachineInfo instance.
        :param bool fresh: (default: False) Whether to create fresh CPU, Memory, and Python info instances.
        :return MachineInfo: The created or cached MachineInfo instance.
        """
        node = _validate.node(node)
        cache_key = _validate.cache_key(cache_key)
        fresh = _validate.fresh(fresh)

        if cache_key and cache_key in cls._keyed_cache:
            cached_instance = cls._keyed_cache[cache_key]
            if not fresh:
                if (node is None and cached_instance.node == cls._get_real_node_name()) or (
                    node is not None and cached_instance.node == node
                ):
                    return cached_instance

        core_info = cls._get_core_info()
        final_node = cls._get_real_node_name() if node is None else node
        cpu_info = CPUInfo() if fresh else core_info.cpu
        memory_info = MemoryInfo() if fresh else core_info.memory
        python_info = PythonInfo() if fresh else core_info.python

        instance = MachineInfo(
            node=final_node, cpu=cpu_info, python=python_info, system=core_info.system, memory=memory_info
        )

        # We DO NOT refresh the cache for existing keys
        # It would create action-at-a-distance side effects
        if cache_key and cache_key not in cls._keyed_cache:
            cls._keyed_cache[cache_key] = instance

        return instance
