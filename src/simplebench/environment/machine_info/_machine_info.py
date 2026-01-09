"""Utility functions to get machine information."""
import platform
from dataclasses import dataclass
from typing import ClassVar

from simplebench.environment._cpu_info import CPUInfo
from simplebench.environment._memory_info import MemoryInfo
from simplebench.environment._python_info import PythonInfo
from simplebench.environment.system_info import SystemInfo

from . import validate


@dataclass(frozen=True, slots=True, kw_only=True)
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

    def __post_init__(self) -> None:
        """Post-initialization to validate the object's fields."""
        validate.node(self.node)
        validate.cpu_info(self.cpu)
        validate.python_info(self.python)
        validate.system_info(self.system)
        validate.memory_info(self.memory)

class MachineInfoFactory:
    """Factory for creating and caching MachineInfo instances."""

    _cached_core_info: ClassVar[MachineInfo | None] = None
    _real_node_name: ClassVar[str] = ''
    _keyed_cache: ClassVar[dict[str, 'MachineInfo']] = {}

    @classmethod
    def _get_core_info(cls) -> MachineInfo:
        """Get core machine info, from cache or by creating it."""
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
        """Get the real node name, from cache or by calling platform.node()."""
        if not cls._real_node_name:
            cls._real_node_name = platform.node()
        return cls._real_node_name

    @classmethod
    def create(cls,
               node: str | None = '',
               cache_key: str | None = None,
               fresh_cpu_info: bool = False,
               fresh_memory_info: bool = False
               ) -> MachineInfo:
        """
        Create a MachineInfo instance, using caching to avoid redundant work.
        """
        node = validate.node(node)
        cache_key = validate.cache_key(cache_key)
        fresh_cpu_info = validate.fresh_cpu_info(fresh_cpu_info)
        fresh_memory_info = validate.fresh_memory_info(fresh_memory_info)

        if cache_key and cache_key in cls._keyed_cache:
            cached_instance = cls._keyed_cache[cache_key]
            if not fresh_cpu_info and not fresh_memory_info:
                # If no fresh info needed, we can potentially reuse the cached one as-is
                # or just change the node
                if (node is None and cached_instance.node == cls._get_real_node_name()) or \
                   (node is not None and cached_instance.node == node):
                    return cached_instance

        core_info = cls._get_core_info()
        final_node = cls._get_real_node_name() if node is None else node
        cpu_info = CPUInfo() if fresh_cpu_info else core_info.cpu
        memory_info = MemoryInfo() if fresh_memory_info else core_info.memory

        instance = MachineInfo(
            node=final_node,
            cpu=cpu_info,
            python=core_info.python,
            system=core_info.system,
            memory=memory_info
        )

        # We DO NOT refresh the cache for existing keys
        # It would create action-at-a-distance side effects
        if cache_key and cache_key not in cls._keyed_cache:
            cls._keyed_cache[cache_key] = instance

        return instance
