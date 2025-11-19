"""ErrorTags for the si_units module."""
from ..enums import enum_docstrings
from .base import ErrorTag


@enum_docstrings
class _SIUnitsErrorTag(ErrorTag):
    """ErrorTags for si_units module."""

    # si_units.si_scale() tags
    SI_SCALE_INVALID_UNIT_ARG_TYPE = "SI_SCALE_INVALID_UNIT_ARG_TYPE"
    """The unit argument was not a str"""
    SI_SCALE_INVALID_UNIT_ARG_VALUE = "SI_SCALE_INVALID_UNIT_ARG_VALUE"
    """The unit argument was an empty str"""
    SI_SCALE_INVALID_BASE_UNIT_ARG_TYPE = "SI_SCALE_INVALID_BASE_UNIT_ARG_TYPE"
    """The base_unit argument was not a str"""
    SI_SCALE_EMPTY_BASE_UNIT_ARG = "SI_SCALE_EMPTY_BASE_UNIT_ARG"
    """The base_unit argument was an empty str"""
    SI_SCALE_UNKNOWN_SI_UNIT_PREFIX = "SI_SCALE_UNKNOWN_SI_UNIT_PREFIX"
    """The specified SI unit is not recognized"""
    SI_SCALE_UNIT_DOES_NOT_END_WITH_BASE_UNIT = "SI_SCALE_UNIT_DOES_NOT_END_WITH_BASE_UNIT"
    """The specified SI unit and base unit do not match"""

    # si_units.si_unit_base() tags
    SI_UNIT_BASE_EMPTY_UNIT_ARG = "SI_UNIT_BASE_EMPTY_UNIT_ARG"
    """The unit argument was an empty str"""
    SI_UNIT_BASE_INVALID_UNIT_ARG_TYPE = "SI_UNIT_BASE_INVALID_UNIT_ARG_TYPE"
    """The unit argument was not a str"""
    SI_UNIT_BASE_UNKNOWN_SI_UNIT_PREFIX = "SI_UNIT_BASE_UNKNOWN_SI_UNIT_PREFIX"
    """The specified SI unit prefix is not recognized"""

    # si_units.si_scale_for_smallest() tags
    SI_SCALE_FOR_SMALLEST_INVALID_NUMBERS_ARG_TYPE = "SI_SCALE_FOR_SMALLEST_INVALID_NUMBERS_ARG_TYPE"
    """The numbers argument was not a list"""
    SI_SCALE_FOR_SMALLEST_INVALID_NUMBERS_ARG_VALUES_TYPE = (
        "SI_SCALE_FOR_SMALLEST_INVALID_NUMBERS_ARG_VALUES_TYPE")
    """One or more values in the numbers argument was not an int or float"""

    # si_units.si_scale_to_unit() tags
    SI_SCALE_TO_UNIT_INVALID_BASE_UNIT_ARG_TYPE = "SI_SCALE_TO_UNIT_INVALID_BASE_UNIT_ARG_TYPE"
    """The base_unit argument was not a str"""
    SI_SCALE_TO_UNIT_EMPTY_BASE_UNIT_ARG = "SI_SCALE_TO_UNIT_EMPTY_BASE_UNIT_ARG"
    """The base_unit argument was an empty str"""
    SI_SCALE_TO_UNIT_INVALID_CURRENT_UNIT_ARG_TYPE = "SI_SCALE_TO_UNIT_INVALID_CURRENT_UNIT_ARG_TYPE"
    """The current_unit argument was not a str"""
    SI_SCALE_TO_UNIT_EMPTY_CURRENT_UNIT_ARG = "SI_SCALE_TO_UNIT_EMPTY_CURRENT_UNIT_ARG"
    """The current_unit argument was an empty str"""
    SI_SCALE_TO_UNIT_INVALID_TARGET_UNIT_ARG_TYPE = "SI_SCALE_TO_UNIT_INVALID_TARGET_UNIT_ARG_TYPE"
    """The target_unit argument was not a str"""
    SI_SCALE_TO_UNIT_EMPTY_TARGET_UNIT_ARG = "SI_SCALE_TO_UNIT_EMPTY_TARGET_UNIT_ARG"
    """The target_unit argument was an empty str"""
    SI_SCALE_TO_UNIT_INCOMPATIBLE_UNITS = "SI_SCALE_TO_UNIT_INCOMPATIBLE_UNITS"
    """The specified base_unit, current_unit, target_unit are not all compatible"""
