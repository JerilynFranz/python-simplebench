"""Utility functions to get machine information."""
import platform
from dataclasses import dataclass
from typing import ClassVar

from simplebench.validators import validate_string

from .. import CPUInfo, PythonInfo, SystemInfo
from ._error_tags import _MachineInfoErrorTag


@dataclass(frozen=True, slots=True)
class _MachineCoreInfo:
    """Internal immutable dataclass to hold the core, expensive-to-gather info."""
    cpu: CPUInfo
    python: PythonInfo
    system: SystemInfo


class MachineInfo:
    """Data class holding information about the current machine and Python version."""

    _cached_core_info: ClassVar[_MachineCoreInfo | None] = None
    """Class-level cache for the core environment info to avoid redundant computations."""
    _cached_node: ClassVar[str] = ''
    """Class-level cache for the result of platform.node() to avoid redundant calls."""

    def __init__(self, node: str | None = '') -> None:
        """Initialize the MachineInfo instance by snapshotting the current environment.

        This constructor uses a class-level cache to ensure that expensive info-gathering
        operations (for CPU, Python, System, and node name) are only performed once across
        all instances.

        :param str | None node: The node name (optional).
            If explicitly set to `None`, the machine's actual hostname will be used.
            The default is an empty string to avoid including potentially
            sensitive information by accident.
        """
        cls = self.__class__
        if cls._cached_core_info is None:
            cls._cached_core_info = _MachineCoreInfo(
                cpu=CPUInfo(),
                python=PythonInfo(),
                system=SystemInfo(),
            )

        if node is None:
            if cls._cached_node == '':
                cls._cached_node = platform.node()
            node = cls._cached_node

        self._node: str = validate_string(
            node, 'node',
            _MachineInfoErrorTag.INVALID_NODE_PARAM,
            _MachineInfoErrorTag.INVALID_NODE_PARAM,
            allow_empty=True, allow_blank=True, strip=True
        )
        self._core = cls._cached_core_info

    @property
    def node(self) -> str:
        """The node name."""
        return self._node

    @property
    def cpu(self) -> CPUInfo:
        """CPU information."""
        return self._core.cpu

    @property
    def python(self) -> PythonInfo:
        """Python information."""
        return self._core.python

    @property
    def system(self) -> SystemInfo:
        """System information."""
        return self._core.system
