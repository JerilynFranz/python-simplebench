"""Utility functions to get machine information."""
import platform
from dataclasses import dataclass
from types import MappingProxyType
from typing import ClassVar, cast

from simplebench.environment._cpu_info import CPUInfo
from simplebench.environment._memory_info import MemoryInfo
from simplebench.environment._python_info import PythonInfo
from simplebench.environment._system_info import SystemInfo
from simplebench.report.versions.v1 import ImmutableMachineInfoData
from simplebench.report.versions.v1 import MachineInfo as ReportMachineInfo

from . import _validate


@dataclass(frozen=True, kw_only=True)
class MachineInfo:
    """Data class holding information about the current machine and execution environment."""
    node: str
    """The node name of the machine."""
    cpu: CPUInfo
    """CPU information."""
    python: PythonInfo
    """Python interpreter information."""
    system: SystemInfo
    """System information."""
    memory: MemoryInfo
    """Memory information."""

    __slots__ = ('node', 'cpu', 'python', 'execution_environment', 'system', 'memory', '_dict_cache')

    def __post_init__(self) -> None:
        """Post-initialization to validate the object's fields."""
        _validate.node(self.node)
        _validate.cpu_info(self.cpu)
        _validate.python_info(self.python)
        _validate.system_info(self.system)
        _validate.memory_info(self.memory)
        object.__setattr__(self, '_dict_cache', MappingProxyType({
                'node': self.node,
                'cpu': self.cpu.to_dict(),
                'execution_environment': MappingProxyType({'python': self.python.to_dict()}),
                'system': self.system.to_dict(),
                'memory': self.memory.to_dict()
            }))
        object.__setattr__(self, '_report_machine_info', ReportMachineInfo.from_dict(self.to_dict()))

    @property
    def as_report_machine_info(self) -> ReportMachineInfo:
        """The :class:`simplebench.report.versions.v1.MachineInfo` representation of the
        :class:`simplebench.environment.MachineInfo` instance.

        :return ReportMachineInfo: The ReportMachineInfo representation of the MachineInfo instance.
        """
        return cast(ReportMachineInfo, getattr(self, '_report_machine_info'))

    def to_dict(self) -> ImmutableMachineInfoData:
        """Convert the MachineInfo instance to a dictionary.

        :return dict: A dictionary representation of the MachineInfo instance.
        """
        return cast(ImmutableMachineInfoData, getattr(self, '_dict_cache'))


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

        machine_info_cached = MachineInfoFactory.create(cache_key="my_cache_key")
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
                node='',
                cpu=CPUInfo(),
                python=PythonInfo(),
                system=SystemInfo(),
                memory=MemoryInfo()
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
    def create(cls,
               node: str | None = '',
               cache_key: str | None = None,
               fresh: bool = False,
               ) -> MachineInfo:
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
                if (node is None and cached_instance.node == cls._get_real_node_name()) or \
                   (node is not None and cached_instance.node == node):
                    return cached_instance

        core_info = cls._get_core_info()
        final_node = cls._get_real_node_name() if node is None else node
        cpu_info = CPUInfo() if fresh else core_info.cpu
        memory_info = MemoryInfo() if fresh else core_info.memory
        python_info = PythonInfo() if fresh else core_info.python

        instance = MachineInfo(
            node=final_node,
            cpu=cpu_info,
            python=python_info,
            system=core_info.system,
            memory=memory_info
        )

        # We DO NOT refresh the cache for existing keys
        # It would create action-at-a-distance side effects
        if cache_key and cache_key not in cls._keyed_cache:
            cls._keyed_cache[cache_key] = instance

        return instance
