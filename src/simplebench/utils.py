# -*- coding: utf-8 -*-
"""Utility functions"""

import math
import platform
import re
import sys
from typing import Any, TypedDict
from cpuinfo import get_cpu_info

from .constants import DEFAULT_SIGNIFICANT_FIGURES


class MachineInfo(TypedDict):
    """TypedDict for machine info returned by pytest_benchmark_generate_machine_info()."""
    node: str
    """Computer's network name."""
    processor: str
    """Processor name."""
    machine: str
    """Machine type."""
    python_compiler: str
    """Python compiler used."""
    python_implementation: str
    """Python implementation name."""
    python_implementation_version: str
    """Python implementation version."""
    python_version: str
    """Python version."""
    python_build: tuple[str, str]
    """Python build information."""
    release: str
    """Operating system release."""
    system: str
    """Operating system name."""
    cpu: dict[str, Any]
    """CPU information."""


def python_implementation_version() -> str:
    """Return the Python implementation version.

    For CPython, this is the same as platform.python_version().
    For PyPy, this is the PyPy version (e.g., '7.3.5').

    Returns:
        str: The Python implementation version.
    """
    python_implementation: str = platform.python_implementation()
    py_implementation_version: str = platform.python_version()
    if python_implementation == 'PyPy':
        version_info: 'sys.pypy_version_info' = sys.pypy_version_info  # pyright: ignore[reportAttributeAccessIssue] # pylint: disable=no-member # noqa:UP031, E501
        py_implementation_version = (
            f'{version_info.major:d}.{version_info.minor:d}.{version_info.micro:d}'
            f'-{version_info.releaselevel:d}{version_info.serial:d}')
    return py_implementation_version


def pytest_benchmark_generate_machine_info() -> MachineInfo:
    """Return a dictionary of information about the current machine and Python version."""
    python_implementation = platform.python_implementation()
    machine_info: MachineInfo = {
        'node': platform.node(),
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


def platform_id() -> str:
    """Return a string that uniquely identifies the current machine and Python version.

    The platform ID is a lowercase string that combines the operating system, Python implementation,
    Python version, and architecture.

    Returns:
        str: The platform ID.
    """
    return '{system}-{python_impl}-{python_version}-{arch}'.format(  # pylint: disable=consider-using-f-string
          system=platform.system(),
          python_impl=platform.python_implementation(),
          python_version='.'.join(platform.python_version_tuple()[:2]),
          arch=platform.architecture()[0]).lower().replace(' ', '')


def sanitize_filename(name: str) -> str:
    """Sanitizes a filename by replacing invalid characters with _.

    Only 'a-z', 'A-Z', '0-9', '_', and '-' are allowed. All other characters
    are replaced with '_' and multiple sequential '_' characters are then collapsed to
    single '_' characters.

    Args:
        name (str): The filename to sanitize.

    Returns:
        str: The sanitized filename.
    """
    first_pass: str = re.sub(r'[^a-zA-Z0-9_-]+', '_', name)
    return re.sub(r'_+', '_', first_pass)


def si_scale_for_smallest(numbers: list[float], base_unit: str) -> tuple[str, float]:
    """Scale factor and SI unit for the smallest in list of numbers.

    The scale factor is the factor that will be applied to the numbers to convert
    them to the desired unit. The SI unit is the unit that corresponds to the scale factor.

    If passed only one number, it effectively gives the scale for that single number.
    If passed a list, it gives the scale for the smallest absolute value in the list.

    Args:
        numbers: A list of numbers to scale.
        base_unit: The base unit to use for scaling.

    Returns:
        A tuple containing the scaled unit and the scaling factor.
    """
    # smallest absolute number in list
    min_n: float = min([abs(n) for n in numbers])
    unit: str = ''
    scale: float = 1.0
    if min_n >= 1e12:
        unit, scale = 'T' + base_unit, 1e-12
    elif min_n >= 1e9:
        unit, scale = 'G' + base_unit, 1e-9
    elif min_n >= 1e6:
        unit, scale = 'M' + base_unit, 1e-6
    elif min_n >= 1e3:
        unit, scale = 'K' + base_unit, 1e-3
    elif min_n >= 1e0:
        unit, scale = base_unit, 1.0
    elif min_n >= 1e-3:
        unit, scale = 'm' + base_unit, 1e3
    elif min_n >= 1e-6:
        unit, scale = 'μ' + base_unit, 1e6
    elif min_n >= 1e-9:
        unit, scale = 'n' + base_unit, 1e9
    elif min_n >= 1e-12:
        unit, scale = 'p' + base_unit, 1e12
    return unit, scale


def si_scale(unit: str, base_unit: str) -> float:
    """Get the SI scale factor for a unit given the base unit.

    This method will return the scale factor for the given unit
    relative to the base unit for SI prefixes ranging from tera (T)
    to pico (p).

    Args:
        unit (str): The unit to get the scale factor for.
        base_unit (str): The base unit.

    Returns:
        The scale factor for the given unit.

    Raises:
        ValueError: If the SI unit is not recognized.
    """
    si_prefixes = {
        f'T{base_unit}': 1e12,
        f'G{base_unit}': 1e9,
        f'M{base_unit}': 1e6,
        f'K{base_unit}': 1e3,
        f'{base_unit}': 1.0,
        f'm{base_unit}': 1e-3,
        f'μ{base_unit}': 1e-6,
        f'n{base_unit}': 1e-9,
        f'p{base_unit}': 1e-12,
    }
    if unit in si_prefixes:
        return si_prefixes[unit]
    raise ValueError(f'Unknown SI unit: {unit}')


def si_scale_to_unit(base_unit: str, current_unit: str, target_unit: str) -> float:
    """Scale factor to convert a current SI unit to a target SI unit based on their SI prefixes.

    Example:
    scale_by: float = self.si_scale_to_unit(base_unit='s', current_unit='s', target_unit='ns')

    Args:
        numbers: A list of numbers to scale.
        current_unit: The base unit to use for unscaling.

    Returns:
        The scaling factor to return the number to the base unit
    """
    current_scale = si_scale(current_unit, base_unit)
    target_scale = si_scale(target_unit, base_unit)
    return target_scale / current_scale


def sigfigs(number: float, figures: int = DEFAULT_SIGNIFICANT_FIGURES) -> float:
    """Rounds a floating point number to the specified number of significant figures.

    If the number of significant figures is not specified, it defaults to
    DEFAULT_SIGNIFICANT_FIGURES.

    * 14.2 to 2 digits of significant figures becomes 14
    * 0.234 to 2 digits of significant figures becomes 0.23
    * 0.0234 to 2 digits of significant figures becomes 0.023
    * 14.5 to 2 digits of significant figures becomes 15
    * 0.235 to 2 digits of significant figures becomes 0.24

    Args:
        number (float): The number to round.
        figures (int): The number of significant figures to round to.

    Returns:
        The rounded number as a float.

    Raises:
        TypeError: If the number arg is not a float or the figures arg is not an int.
        ValueError: If the figures arg is not at least 1.
    """
    if not isinstance(number, float):
        raise TypeError("number arg must be a float")
    if not isinstance(figures, int):
        raise TypeError("figures arg must be an int")
    if figures < 1:
        raise ValueError("figures arg must be at least 1")

    if number == 0.0:
        return 0.0
    return round(number, figures - int(math.floor(math.log10(abs(number)))) - 1)
