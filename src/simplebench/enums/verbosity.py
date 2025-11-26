"""Verbosity level enums for SimpleBench."""
from enum import Enum

from .decorators import enum_docstrings


@enum_docstrings
class Verbosity(int, Enum):
    """Verbosity level enums for console output.

    Defined levels are:
      - QUIET: Only requested output, errors, warnings and critical messages are shown.
      - NORMAL: Normal messages are shown, including status displays during runs.
      - VERBOSE: All messages are shown and status displays during runs.
      - DEBUG: All messages are shown, including debug messages and status displays during runs.
    """
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

    This is incompatible with quiet."""
