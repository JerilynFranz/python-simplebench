"""CPU information utility functions.

This provides a CPUInfo class that gathers and exposes information
about the CPU environment at the time of its creation using
the :module:`cpuinfo` module.
"""
from copy import deepcopy
from dataclasses import dataclass, field
from typing import Any

from cpuinfo import get_cpu_info


@dataclass(frozen=True, slots=True)
class CPUInfo:
    """Wraps CPU information gathered from the :module:`cpuinfo` module.

    Because the CPU information can be quite detailed and complex,
    this is represented as a dictionary property called :attr:`info`
    that contains all the information returned by :func:`cpuinfo.get_cpu_info`.

    This class snapshots the CPU information at initialization,
    providing a consistent view of the CPU environment that can be
    easily passed around and used in other parts of the application
    or reporting tools and makes it possible to serialize
    (such as by pickling) this information if needed.
    """
    _info: dict[str, Any] = field(init=False, repr=False)

    def __init__(self) -> None:
        """Initializes the instance by gathering data from the `cpuinfo` module."""
        # Uses object.__setattr__ because the class is frozen
        object.__setattr__(self, '_info', get_cpu_info())

    @property
    def info(self) -> dict[str, Any]:
        """Get the CPU information dictionary.

        This is a deep copy of the dictionary returned by :func:`cpuinfo.get_cpu_info`
        at the time of this object's initialization.

        To prevent external modifications of the internal state, this property always returns a
        deep copy of the dictionary.

        :return: The CPU information dictionary.
        """
        return deepcopy(self._info)
