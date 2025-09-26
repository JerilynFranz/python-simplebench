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
    NULL = 'null section'
    """No section."""

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

    This is incompatible with quiet."""


class Target(str, Enum):
    """Categories for different output targets.

    The enums are used in generating calling parameters
    for the report() methods in the Reporter subclasses.
    """
    CONSOLE = 'to console'
    """Output to console."""
    FILESYSTEM = 'to filesystem'
    """Output to filesystem."""
    HTTP = 'to http'
    """Output to HTTP endpoint."""
    DISPLAY = 'to display'
    """Output to display device."""
    CALLBACK = 'to callback'
    """Pass generated output to a callback function."""
    CUSTOM = 'to custom target'
    """Output to a custom target."""
    NULL = 'to null'
    """No output."""


class Format(str, Enum):
    """Categories for different output formats."""
    PLAIN_TEXT = 'plain text'
    """Plain text format"""
    MARKDOWN = 'markdown'
    """Markdown format"""
    RICH_TEXT = 'rich text'
    """Rich text format"""
    CSV = 'csv'
    """CSV format"""
    JSON = 'json'
    """JSON format"""
    GRAPH = 'graph'
    """Graphical format"""
    CUSTOM = 'custom'
    """Custom format"""
