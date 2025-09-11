# -*- coding: utf-8 -*-
"""Various enums for SimpleBench."""
from enum import Enum


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
