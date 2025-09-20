# -*- coding: utf-8 -*-
"""Various enums for SimpleBench."""
from enum import Enum
from typing import Any


class Section(str, Enum):
    """Categories for case sections.

    The string values are used to load the data accessor methods by attribute name in the Results class
    and name generated files."""
    OPS = 'operations per second'
    """Operations per second section."""
    TIMING = 'per round timings'
    """Time per round section."""
    MEMORY = 'memory usage'
    """Memory usage section."""
    PEAK_MEMORY = 'peak memory usage'
    """Peak memory usage section."""

    def __contains__(self, item: Any) -> bool:
        """Check if the item is a valid Section."""
        return isinstance(item, Section) or item in self._value2member_map_


class Verbosity(int, Enum):
    """Verbosity levels for console output."""
    QUIET = 0
    """Only requested output, errors, warnings and critical messages are shown.
    Status displays are not shown during runs.

    This is incompatible with all other output levels."""

    NORMAL = 1
    """Normal messages are shown, including status displays during runs.

    This is the default verbosity level and is incompatible with quiet."""

    VERBOSE = 2
    """All messages are shown and status displays during runs.

    This is incompatible with quiet."""

    DEBUG = 5
    """All messages are shown, including debug messages and status displays during runs.

    This is incompatible with quiet."""""
