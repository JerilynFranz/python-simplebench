"""Utility functions to get machine information."""
import platform
import sys
from functools import cache
from typing import TypedDict

from cpuinfo import get_cpu_info  # type: ignore[import-untyped]


class MachineInfo(TypedDict):
    """TypedDict for machine info returned by :func:`get_machine_info`.

    :ivar processor: Processor name.
    :vartype processor: str
    :ivar machine: Machine type.
    :vartype machine: str
    :ivar python_compiler: Python compiler used.
    :vartype python_compiler: str
    :ivar python_implementation: Python implementation name.
    :vartype python_implementation: str
    :ivar python_implementation_version: Python implementation version.
    :vartype python_implementation_version: str
    :ivar python_version: Python version.
    :vartype python_version: str
    :ivar python_build: Python build information.
    :vartype python_build: tuple[str, str]
    :ivar release: Operating system release.
    :vartype release: str
    :ivar system: Operating system name.
    :vartype system: str
    :ivar cpu: CPU information.
    :vartype cpu: dict[str, str]
    """
    processor: str
    machine: str
    python_compiler: str
    python_implementation: str
    python_implementation_version: str
    python_version: str
    python_build: tuple[str, str]
    release: str
    system: str
    cpu: dict[str, str]


@cache
def python_implementation_version() -> str:
    """Return the Python implementation version.

    For CPython, this is the same as :func:`platform.python_version`.
    For PyPy, this is the PyPy version (e.g., '7.3.5').

    :return: The Python implementation version.
    :rtype: str
    """
    python_implementation: str = platform.python_implementation()
    py_implementation_version: str = platform.python_version()
    if python_implementation == 'PyPy':
        version_info = getattr(sys, 'pypy_version_info', None)
        if version_info is not None:
            py_implementation_version = (
                f'{version_info.major:d}.{version_info.minor:d}.{version_info.micro:d}'
                f'-{version_info.releaselevel:d}{version_info.serial:d}')
        else:
            py_implementation_version = 'unknown'
    return py_implementation_version


@cache
def get_machine_info() -> MachineInfo:
    """Return a dictionary of information about the current machine and Python version."""
    python_implementation = platform.python_implementation()
    machine_info: MachineInfo = {
        'processor': platform.processor(),
        'machine': platform.machine(),
        'python_compiler': platform.python_compiler(),
        'python_implementation': python_implementation,
        'python_implementation_version': python_implementation_version(),
        'python_version': platform.python_version(),
        'python_build': platform.python_build(),
        'release': platform.release(),
        'system': platform.system(),
        'cpu': get_cpu_info(),
    }
    return machine_info


@cache
def platform_processor() -> str:
    """Return the current processor name.

    :return: The processor name.
    :rtype: str
    """
    return platform.processor()


@cache
def platform_machine() -> str:
    """Return the current machine type.

    :return: The machine type.
    :rtype: str
    """
    return platform.machine()


@cache
def platform_id() -> str:
    """Return a string that uniquely identifies the current machine and Python version.

    The platform ID is a lowercase string that combines the operating system, Python implementation,
    Python version, and architecture.

    :return: The platform ID.
    :rtype: str
    """
    return '{system}-{python_impl}-{python_version}-{arch}'.format(  # pylint: disable=consider-using-f-string
          system=platform.system(),
          python_impl=platform.python_implementation(),
          python_version='.'.join(platform.python_version_tuple()[:2]),
          arch=platform.architecture()[0]).lower().replace(' ', '')


@cache
def platform_system() -> str:
    """Return the current operating system name.

    :return: The operating system name.
    :rtype: str
    """
    return platform.system()


@cache
def platform_implementation() -> str:
    """Return the current Python implementation name.

    See :func:`platform.python_implementation` for details.

    :return: The Python implementation name.
    :rtype: str
    """
    return platform.python_implementation()


@cache
def platform_version() -> str:
    """Return the current Python version.

    :return: The Python version.
    :rtype: str
    """
    return '.'.join(platform.python_version_tuple()[:2])


@cache
def platform_architecture() -> str:
    """Return the current architecture.

    :return: The architecture.
    :rtype: str
    """
    return platform.architecture()[0]
