# -*- coding: utf-8 -*-
"""Utility functions for handling SI units"""
from typing import Sequence

from .exceptions import SimpleBenchValueError, SimpleBenchTypeError, ErrorTag

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


def si_scale_for_smallest(numbers: Sequence[float | int], base_unit: str) -> tuple[str, float]:
    """Scale factor and SI unit for the smallest in a sequence of numbers.

    The scale factor is the factor that should be applied to the numbers to convert
    them to the desired unit. The SI unit is the unit that corresponds to the scale factor.

    It gives the SI prefix unit and scale for the smallest non-zero absolute value in the sequence.
    If all numbers are zero, it returns the base unit and a scale factor of 1.0.

    Args:
        numbers: A sequence of numbers to scale.
        base_unit: The base unit to use for scaling.

    Returns:
        A tuple containing the scaled unit and the scaling factor.
    """
    if not isinstance(numbers, Sequence) or isinstance(numbers, (str, bytes)):
        raise SimpleBenchTypeError(
            "numbers arg must be a Sequence of int or float",
            tag=ErrorTag.SI_UNITS_SI_SCALE_FOR_SMALLEST_INVALID_NUMBERS_ARG_TYPE)
    if not all(isinstance(n, (int, float)) for n in numbers):
        raise SimpleBenchTypeError(
            "all items in numbers arg sequence must be type int or float",
            tag=ErrorTag.SI_UNITS_SI_SCALE_FOR_SMALLEST_INVALID_NUMBERS_ARG_VALUES_TYPE)
    if not numbers or all(n == 0 for n in numbers):
        return base_unit, 1.0

    min_n: float = min([abs(n) for n in numbers if n != 0], default=0.0)

    for threshold, prefix, scale in _SI_PREFIXES:
        if min_n >= threshold:
            return f'{prefix}{base_unit}', scale

    # Default to the smallest scale if no other matches
    _, prefix, scale = _SI_PREFIXES[-1]
    return f'{prefix}{base_unit}', scale


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
            tag=ErrorTag.SI_UNITS_SI_SCALE_INVALID_UNIT_ARG_TYPE)
    if not isinstance(base_unit, str):
        raise SimpleBenchTypeError(
            "base_unit arg must be a str",
            tag=ErrorTag.SI_UNITS_SI_SCALE_INVALID_BASE_UNIT_ARG_TYPE)
    if base_unit == '':
        raise SimpleBenchValueError(
            "base_unit arg must not be an empty string",
            tag=ErrorTag.SI_UNITS_SI_SCALE_EMPTY_BASE_UNIT_ARG)
    if not unit.endswith(base_unit):
        raise SimpleBenchValueError(
            f'Unit "{unit}" does not end with base unit "{base_unit}"',
            tag=ErrorTag.SI_UNITS_SI_SCALE_UNIT_DOES_NOT_END_WITH_BASE_UNIT)
    si_prefix = unit[:-len(base_unit)]
    if si_prefix in _SI_PREFIXES_SCALE:
        return _SI_PREFIXES_SCALE[si_prefix]
    raise SimpleBenchValueError(
        f'Unknown SI unit: {unit}', tag=ErrorTag.SI_UNITS_SI_SCALE_UNKNOWN_SI_UNIT_PREFIX)


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
            tag=ErrorTag.SI_UNITS_SI_UNIT_BASE_INVALID_UNIT_ARG_TYPE)
    if len(unit) == 0:
        raise SimpleBenchValueError(
            "unit arg must not be an empty string",
            tag=ErrorTag.SI_UNITS_SI_UNIT_BASE_EMPTY_UNIT_ARG)
    if len(unit) == 1:
        return unit
    prefix = unit[:1]
    if prefix in _SI_PREFIXES_SCALE:
        return unit[1:]
    raise SimpleBenchValueError(
        f'Unknown SI unit: {unit}', tag=ErrorTag.SI_UNITS_SI_UNIT_BASE_UNKNOWN_SI_UNIT_PREFIX)


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
            tag=ErrorTag.SI_UNITS_SI_SCALE_TO_UNIT_INVALID_BASE_UNIT_ARG_TYPE)
    if base_unit == '':
        raise SimpleBenchValueError(
            "base_unit arg must not be an empty string",
            tag=ErrorTag.SI_UNITS_SI_SCALE_TO_UNIT_EMPTY_BASE_UNIT_ARG)
    if not isinstance(current_unit, str):
        raise SimpleBenchTypeError(
            "current_unit arg must be a str",
            tag=ErrorTag.SI_UNITS_SI_SCALE_TO_UNIT_INVALID_CURRENT_UNIT_ARG_TYPE)
    if current_unit == '':
        raise SimpleBenchValueError(
            "current_unit arg must not be an empty string",
            tag=ErrorTag.SI_UNITS_SI_SCALE_TO_UNIT_EMPTY_CURRENT_UNIT_ARG)
    if not isinstance(target_unit, str):
        raise SimpleBenchTypeError(
            "target_unit arg must be a str",
            tag=ErrorTag.SI_UNITS_SI_SCALE_TO_UNIT_INVALID_TARGET_UNIT_ARG_TYPE)
    if target_unit == '':
        raise SimpleBenchValueError(
            "target_unit arg must not be an empty string",
            tag=ErrorTag.SI_UNITS_SI_SCALE_TO_UNIT_EMPTY_TARGET_UNIT_ARG)

    if not si_unit_base(base_unit) == si_unit_base(current_unit) == si_unit_base(target_unit):
        raise SimpleBenchValueError(
            (f'Units are not compatible: base_unit="{base_unit}", current_unit="{current_unit}", '
                f'target_unit="{target_unit}"'),
            tag=ErrorTag.SI_UNITS_SI_SCALE_TO_UNIT_INCOMPATIBLE_UNITS)
    current_scale = si_scale(current_unit, base_unit)
    target_scale = si_scale(target_unit, base_unit)
    return target_scale / current_scale
