"""ErrorTags for the si_units module."""

from enum import auto
from simplebench.doc_utils import enum_docstrings

from ..exceptions.error_tag import ErrorTag


@enum_docstrings
class _SIUnitsErrorTag(ErrorTag):
    """ErrorTags for si_units module."""

    # si_units.si_scale() tags
    SI_SCALE_INVALID_UNIT_ARG_TYPE = auto()
    """The unit argument was not a str"""
    SI_SCALE_INVALID_UNIT_ARG_VALUE = auto()
    """The unit argument was an empty str"""
    SI_SCALE_INVALID_BASE_UNIT_ARG_TYPE = auto()
    """The base_unit argument was not a str"""
    SI_SCALE_EMPTY_BASE_UNIT_ARG = auto()
    """The base_unit argument was an empty str"""
    SI_SCALE_UNKNOWN_SI_UNIT_PREFIX = auto()
    """The specified SI unit is not recognized"""
    SI_SCALE_UNIT_DOES_NOT_END_WITH_BASE_UNIT = auto()
    """The specified SI unit and base unit do not match"""

    # si_units.si_unit_base() tags
    SI_UNIT_BASE_EMPTY_UNIT_ARG = auto()
    """The unit argument was an empty str"""
    SI_UNIT_BASE_INVALID_UNIT_ARG_TYPE = auto()
    """The unit argument was not a str"""
    SI_UNIT_BASE_UNKNOWN_SI_UNIT_PREFIX = auto()
    """The specified SI unit prefix is not recognized"""

    # si_units.si_scale_for_largest() tags
    SI_SCALE_FOR_LARGEST_INVALID_NUMBERS_ARG_TYPE = auto()
    """The numbers argument was not a list"""
    SI_SCALE_FOR_LARGEST_INVALID_NUMBERS_ARG_VALUES_TYPE = auto()
    """One or more values in the numbers argument was not an int or float"""

    # si_units.si_scale_for_smallest() tags
    SI_SCALE_FOR_SMALLEST_INVALID_NUMBERS_ARG_TYPE = auto()
    """The numbers argument was not a list"""
    SI_SCALE_FOR_SMALLEST_INVALID_NUMBERS_ARG_VALUES_TYPE = auto()
    """One or more values in the numbers argument was not an int or float"""

    # si_units.si_scale_to_unit() tags
    SI_SCALE_TO_UNIT_INVALID_BASE_UNIT_ARG_TYPE = auto()
    """The base_unit argument was not a str"""
    SI_SCALE_TO_UNIT_EMPTY_BASE_UNIT_ARG = auto()
    """The base_unit argument was an empty str"""
    SI_SCALE_TO_UNIT_INVALID_CURRENT_UNIT_ARG_TYPE = auto()
    """The current_unit argument was not a str"""
    SI_SCALE_TO_UNIT_EMPTY_CURRENT_UNIT_ARG = auto()
    """The current_unit argument was an empty str"""
    SI_SCALE_TO_UNIT_INVALID_TARGET_UNIT_ARG_TYPE = auto()
    """The target_unit argument was not a str"""
    SI_SCALE_TO_UNIT_EMPTY_TARGET_UNIT_ARG = auto()
    """The target_unit argument was an empty str"""
    SI_SCALE_TO_UNIT_INCOMPATIBLE_UNITS = auto()
    """The specified base_unit, current_unit, target_unit are not all compatible"""
