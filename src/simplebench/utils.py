# -*- coding: utf-8 -*-
"""Utility functions"""
from functools import cache
import itertools
import math
import platform
import re
import sys
from typing import Any, Sequence, TypedDict

from cpuinfo import get_cpu_info

from .constants import DEFAULT_SIGNIFICANT_FIGURES
from .exceptions import SimpleBenchValueError, SimpleBenchTypeError, ErrorTag


class MachineInfo(TypedDict):
    """TypedDict for machine info returned by get_machine_info()."""
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
    cpu: dict[str, str]
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
        version_info: 'sys.pypy_version_info' = sys.pypy_version_info  # pyright: ignore[reportAttributeAccessIssue] # pylint: disable=no-member # noqa: E501
        py_implementation_version = (
            f'{version_info.major:d}.{version_info.minor:d}.{version_info.micro:d}'
            f'-{version_info.releaselevel:d}{version_info.serial:d}')
    return py_implementation_version


@cache
def get_machine_info() -> MachineInfo:
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


_SI_PREFIXES: list[tuple[float, str, float]] = [
    (1e15, 'P', 1e-15),
    (1e12, 'T', 1e-12),
    (1e9, 'G', 1e-9),
    (1e6, 'M', 1e-6),
    (1e3, 'k', 1e-3),
    (1.0, '', 1.0),
    (1e-3, 'm', 1e3),
    (1e-6, 'μ', 1e6),  # 'U+03BC' Greek Small Letter Mu (SI standard)
    (1e-6, 'µ', 1e6),  # 'U+00B5' MICRO SIGN (legacy Unicode compatibility)
    (1e-9, 'n', 1e9),
    (1e-12, 'p', 1e12),
    (1e-15, 'f', 1e15),
]
"""List of SI prefixes with their scale thresholds and inverse scale factors.
Each tuple contains (scale threshold, prefix, inverse scale factor)."""

_SI_PREFIXES_SCALE = {scale[1]: scale[0] for scale in _SI_PREFIXES}
"""Mapping of SI prefixes to their scale factors."""


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
    if not numbers:
        return base_unit, 1.0

    min_n: float = min([abs(n) for n in numbers if n != 0], default=0.0)

    for threshold, prefix, scale in _SI_PREFIXES:
        if min_n >= threshold:
            return f'{prefix}{base_unit}', scale

    # Default to the smallest scale if no other matches
    if _SI_PREFIXES:
        _, prefix, scale = _SI_PREFIXES[-1]
        return f'{prefix}{base_unit}', scale

    return base_unit, 1.0


def si_scale(unit: str, base_unit: str) -> float:
    """Get the SI scale factor for a unit given the base unit.

    This method will return the scale factor for the given unit
    relative to the base unit for SI prefixes ranging from tera (T)
    to pico (p).

    Example: si_scale('ns', 's') returns 1e-9

    Args:
        unit (str): The unit to get the scale factor for.
        base_unit (str): The base unit

    Returns:
        The scale factor for the given unit.

    Raises:
        SimpleBenchValueError: If the SI unit is not recognized, if base_unit is an empty string,
            or if the unit does not end with the base_unit.
        SimpleBenchTypeError: If the unit or base_unit args are not type str.
    """
    if not isinstance(unit, str):
        raise SimpleBenchTypeError(
            "unit arg must be a str",
            ErrorTag.UTILS_SI_SCALE_INVALID_UNIT_ARG_TYPE)
    if not isinstance(base_unit, str):
        raise SimpleBenchTypeError(
            "base_unit arg must be a str",
            ErrorTag.UTILS_SI_SCALE_INVALID_BASE_UNIT_ARG_TYPE)
    if base_unit == '':
        raise SimpleBenchValueError(
            "base_unit arg must not be an empty string",
            ErrorTag.UTILS_SI_SCALE_EMPTY_BASE_UNIT_ARG)
    if not unit.endswith(base_unit):
        raise SimpleBenchValueError(
            f'Unit "{unit}" does not end with base unit "{base_unit}"',
            ErrorTag.UTILS_SI_SCALE_UNIT_DOES_NOT_END_WITH_BASE_UNIT)
    si_prefix = unit[:-len(base_unit)]
    if si_prefix in _SI_PREFIXES_SCALE:
        return _SI_PREFIXES_SCALE[si_prefix]
    raise SimpleBenchValueError(
        f'Unknown SI unit: {unit}', ErrorTag.UTILS_SI_SCALE_UNKNOWN_SI_UNIT_PREFIX)


def si_unit_base(unit: str) -> str:
    """Get the base unit from an SI unit.

    This assumes that the SI unit is a valid SI unit with an optional SI prefix.
    If the unit is a single character, it is returned as-is on the assumption
    that it is already the base unit.

    Example: si_unit_base('ns') returns 's'

    Args:
        unit (str): The SI unit to get the base unit from.

    Returns:
        The base unit.

    Raises:
        SimpleBenchValueError: If the SI unit is not recognized or if the unit is an empty string.
        SimpleBenchTypeError: If the unit arg is not of type str.
    """
    if not isinstance(unit, str):
        raise SimpleBenchTypeError(
            "unit arg must be a str",
            ErrorTag.UTILS_SI_UNIT_BASE_INVALID_UNIT_ARG_TYPE)
    if len(unit) == 0:
        raise SimpleBenchValueError(
            "unit arg must not be an empty string",
            ErrorTag.UTILS_SI_UNIT_BASE_EMPTY_UNIT_ARG)
    if len(unit) == 1:
        return unit
    prefix = unit[:1]
    if prefix in _SI_PREFIXES_SCALE:
        return unit[1:]
    raise SimpleBenchValueError(
        f'Unknown SI unit: {unit}', ErrorTag.UTILS_SI_UNIT_BASE_UNKNOWN_SI_UNIT_PREFIX)


def si_scale_to_unit(base_unit: str, current_unit: str, target_unit: str) -> float:
    """Scale factor to convert a current SI unit to a target SI unit based on their SI prefixes.

    Example:
    scale_by: float = self.si_scale_to_unit(base_unit='s', current_unit='s', target_unit='ns')

    Args:
        base_unit: The base unit to use for scaling.
        current_unit: The current unit of the number.
        target_unit: The target unit to scale the number to.

    Returns:
        The scaling factor to convert the current unit to the target unit.

    Raises:
        SimpleBenchValueError: If the SI prefix units are not recognized; if base_unit,
            current_unit, or target_unit is an empty string; or if the units are not compatible
            (i.e., do not share the same base unit (i.e. 'seconds' vs 'meters')).
        SimpleBenchTypeError: If the unit, base_unit, current_unit, or target_unit args are not type str.
    """
    if not isinstance(base_unit, str):
        raise SimpleBenchTypeError(
            "base_unit arg must be a str",
            ErrorTag.UTILS_SI_SCALE_TO_UNIT_INVALID_BASE_UNIT_ARG_TYPE)
    if base_unit == '':
        raise SimpleBenchValueError(
            "base_unit arg must not be an empty string",
            ErrorTag.UTILS_SI_SCALE_TO_UNIT_EMPTY_BASE_UNIT_ARG)
    if not isinstance(current_unit, str):
        raise SimpleBenchTypeError(
            "current_unit arg must be a str",
            ErrorTag.UTILS_SI_SCALE_TO_UNIT_INVALID_CURRENT_UNIT_ARG_TYPE)
    if current_unit == '':
        raise SimpleBenchValueError(
            "current_unit arg must not be an empty string",
            ErrorTag.UTILS_SI_SCALE_TO_UNIT_EMPTY_CURRENT_UNIT_ARG)
    if not isinstance(target_unit, str):
        raise SimpleBenchTypeError(
            "target_unit arg must be a str",
            ErrorTag.UTILS_SI_SCALE_TO_UNIT_INVALID_TARGET_UNIT_ARG_TYPE)
    if target_unit == '':
        raise SimpleBenchValueError(
            "target_unit arg must not be an empty string",
            ErrorTag.UTILS_SI_SCALE_TO_UNIT_EMPTY_TARGET_UNIT_ARG)

    if not si_unit_base(base_unit) == si_unit_base(current_unit) == si_unit_base(target_unit):
        raise SimpleBenchValueError(
            (f'Units are not compatible: base_unit="{base_unit}", current_unit="{current_unit}", '
                f'target_unit="{target_unit}"'),
            ErrorTag.UTILS_SI_SCALE_TO_UNIT_INCOMPATIBLE_UNITS)
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
        raise SimpleBenchTypeError(
            "number arg must be a float",
            ErrorTag.UTILS_SIGFIGS_INVALID_NUMBER_ARG_TYPE)
    if not isinstance(figures, int):
        raise SimpleBenchTypeError(
            "figures arg must be an int",
            ErrorTag.UTILS_SIGFIGS_INVALID_FIGURES_ARG_TYPE)
    if figures < 1:
        raise SimpleBenchValueError(
            "figures arg must be at least 1",
            ErrorTag.UTILS_SIGFIGS_INVALID_FIGURES_ARG_VALUE)

    if number == 0.0:
        return 0.0
    return round(number, figures - int(math.floor(math.log10(abs(number)))) - 1)


def kwargs_variations(kwargs: dict[str, Sequence[Any]]) -> list[dict[str, Any]]:
    '''Variations of keyword arguments for the benchmark.

    This function takes a dictionary where each key is a keyword argument name
    and the value is a Sequence of possible values for that argument. It returns a list
    of dictionaries, each dictionary representing a unique combination of keyword arguments and
    their values.

    Example
    -------
    If the input is:
    {
        'arg1': [1, 2],
        'arg2': ['a', 'b']
    }
    The output will be:
    [
        {'arg1': 1, 'arg2': 'a'},
        {'arg1': 1, 'arg2': 'b'},
        {'arg1': 2, 'arg2': 'a'},
        {'arg1': 2, 'arg2': 'b'}
    ]

    Args:
        kwargs (dict[str, Sequence[Any]]): A dictionary of keyword arguments and their possible values.
        The value must be a Sequence (e.g., list, tuple, set), but not a str or bytes instance.

    Returns:
        A list of dictionaries, each representing a unique combination of keyword arguments and values.
    '''
    if not isinstance(kwargs, dict):
        raise SimpleBenchTypeError(
            "kwargs arg must be a dict or dict sub-class",
            ErrorTag.UTILS_KWARGS_VARIATIONS_INVALID_KWARGS_ARG_TYPE
        )
    for key, value in kwargs.items():
        if not isinstance(value, Sequence) or isinstance(value, (str, bytes)):
            raise SimpleBenchTypeError(
                ("kwargs arg values must be a Sequence (not str or bytes); "
                 f"key '{key}' has invalid value type {type(value)}"),
                ErrorTag.UTILS_KWARGS_VARIATIONS_INVALID_KWARGS_VALUE_TYPE
            )

    keys = kwargs.keys()
    if not keys:
        return [{}]
    values = [kwargs[key] for key in keys]
    return [dict(zip(keys, v)) for v in itertools.product(*values)]
