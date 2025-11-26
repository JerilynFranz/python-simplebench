"""Section enums for SimpleBench."""

from enum import Enum
from typing import Any

from .decorators import enum_docstrings


@enum_docstrings
class Section(str, Enum):
    """Categories for case results sections in reporters.

    This is used by reporters to specify which sections of benchmark results to include
    in their output.

    Defined Sections are:
      - OPS: Operations per second section.
      - TIMING: Time per round section.
      - MEMORY: Memory usage section.
      - PEAK_MEMORY: Peak memory usage section.
      - NULL: No section. This is used when a reporter does not specify a section.
    """
    OPS = 'operations per second'
    """Operations per second section."""
    TIMING = 'per round timings'
    """Time per round section."""
    MEMORY = 'memory usage'
    """Memory usage section."""
    PEAK_MEMORY = 'peak memory usage'
    """Peak memory usage section."""
    NULL = 'null section'
    """No section. This is used when a reporter does not specify a section."""

    # Despite the source code for Enum saying this is undocumented, it is
    # part of the public API and used in various places.
    # See: https://docs.python.org/3/library/enum.html#enum.Enum._value2member_map_
    # This allows checking if a value matches a valid enum member without raising an exception.
    # and prevents the superclass __contains__ from raising a TypeError for non-enum values
    # before python 3.12
    #
    # It may be a better idea to use a custom method for this in the future as this
    # blurs the line between using in operator for membership testing and enum value checking.
    # It may be unnecessary as the codebase has evolved
    # MyPy is not very happy about this, so we need to ignore the type check here.
    #
    # TODO: Investigate if this is still needed.
    def __contains__(self, item: Any) -> bool:
        """Check if the item is a valid Section.

        It returns True if the item is either a Section enum member or a valid
        value of the Section enum.
        """
        return isinstance(item, Section) or item in self._value2member_map_  # type: ignore
