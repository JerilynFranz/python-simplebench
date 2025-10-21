# -*- coding: utf-8 -*-
"""Various enums for SimpleBench."""
import ast
import inspect
from enum import Enum
from functools import partial
from operator import is_
from typing import Any, TypeVar

E = TypeVar("E", bound=Enum)


# Decorator to attach docstrings to enum members
# See: https://stackoverflow.com/questions/19330460/how-do-i-put-docstrings-on-enums
def enum_docstrings(enum: type[E]) -> type[E]:
    '''Attach docstrings to enum members.

    Docstrings are string literals that appear directly below the enum member
    assignment expression:

    Example:
        @enum_docstrings
        class SomeEnum(Enum):
            """Docstring for the SomeEnum enum"""

            foo_member = "foo_value"
            """Docstring for the foo_member enum member"""

        SomeEnum.foo_member.__doc__  # 'Docstring for the foo_member enum member'

    Args:
        enum (type[Enum]): The enum class to process.
    Returns:
        The same enum class with member docstrings attached.
    '''
    try:
        mod = ast.parse(inspect.getsource(enum))
    except OSError:
        # no source code available
        return enum

    if mod.body and isinstance(class_def := mod.body[0], ast.ClassDef):
        # An enum member docstring is unassigned if it is the exact same object
        # as enum.__doc__.
        unassigned = partial(is_, enum.__doc__)
        names = enum.__members__.keys()
        member: E | None = None
        for node in class_def.body:
            match node:
                case ast.Assign(targets=[ast.Name(id=name)]) if name in names:
                    # Enum member assignment, look for a docstring next
                    member = enum[name]
                    continue

                case ast.Expr(
                    value=ast.Constant(value=str(docstring))
                ) if member and unassigned(member.__doc__):
                    # docstring immediately following a member assignment
                    member.__doc__ = docstring

                case _:
                    pass

            member = None

    return enum


@enum_docstrings
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


@enum_docstrings
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


@enum_docstrings
class Target(str, Enum):
    """Categories for different output targets.

    The enums are used in generating calling parameters
    for the report() methods in the Reporter subclasses.
    """
    CONSOLE = 'console'
    """Output to console."""
    FILESYSTEM = 'filesystem'
    """Output to filesystem."""
    HTTP = 'http'
    """Output to HTTP endpoint."""
    DISPLAY = 'display'
    """Output to display device."""
    CALLBACK = 'callback'
    """Pass generated output to a callback function."""
    CUSTOM = 'custom'
    """Output to a custom target."""
    NULL = 'null'
    """No output."""


@enum_docstrings
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


@enum_docstrings
class Color(str, Enum):
    """Colors for console output."""
    BLACK = 'black'
    """Black color."""
    RED = 'red'
    """Red color."""
    GREEN = 'green'
    """Green color."""
    YELLOW = 'yellow'
    """Yellow color."""
    BLUE = 'blue'
    """Blue color."""
    MAGENTA = 'magenta'
    """Magenta color."""
    CYAN = 'cyan'
    """Cyan color."""
    WHITE = 'white'
    """White color."""


@enum_docstrings
class FlagType(str, Enum):
    """Types of command-line flags for reporters."""
    BOOLEAN = 'boolean'
    """Boolean flag type.

    This flag type represents a simple on/off or true/false option.
    """
    TARGET_LIST = 'target_list'
    """List of output targets

    This flag type represents a list of output targets for the reporter.
    """
