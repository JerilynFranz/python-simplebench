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
    assignment expression within triple-quotes.

    This decorator parses the source code of the enum class to find
    docstrings for each member and attaches them to the respective enum members.

    This allows for more detailed documentation of enum members and in tools
    that can extract and display these docstrings.

    This code is adapted from:
    https://stackoverflow.com/questions/19330460/how-do-i-put-docstrings-on-enums

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


@enum_docstrings
class Target(str, Enum):
    """Categories for different output targets.

    The enums are used in generating calling parameters
    for the report() methods in the Reporter subclasses.

    Defined Targets are:
      - CONSOLE: Output to console.
      - FILESYSTEM: Output to filesystem.
      - CALLBACK: Pass generated output to a callback function.
      - CUSTOM: Output to a custom target.
      - NULL: No output.
    """
    CONSOLE = 'console'
    """Output to console."""
    FILESYSTEM = 'filesystem'
    """Output to filesystem."""
    CALLBACK = 'callback'
    """Pass generated output to a callback function."""
    CUSTOM = 'custom'
    """Output to a custom target."""
    NULL = 'null'
    """No output."""


@enum_docstrings
class Format(str, Enum):
    """Categories for different output formats.

    Defined Formats are:
      - PLAIN_TEXT: Plain text format.
      - MARKDOWN: Markdown format.
      - RICH_TEXT: Rich text format.
      - CSV: CSV format.
      - JSON: JSON format.
      - GRAPH: Graphical format.
      - CUSTOM: Custom format.

    """
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
    """Colors for console output.

    Defined Colors are:
      - BLACK: Black color.
      - RED: Red color.
      - GREEN: Green color.
      - YELLOW: Yellow color.
      - BLUE: Blue color.
      - MAGENTA: Magenta color.
      - CYAN: Cyan color.
      - WHITE: White color.
    """
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
    """Types of command-line flags for reporters.

    Available FlagTypes are:
      - BOOLEAN: Boolean flag type.
      - TARGET_LIST: List of output targets
      - INVALID: Invalid flag type. This is a testing placeholder and should not be used.

    """
    BOOLEAN = 'boolean'
    """Boolean flag type.

    This flag type represents a simple on/off or true/false option.

    Example: --verbose / --no-verbose
    """
    TARGET_LIST = 'target_list'
    """List of output targets

    This flag type represents a list of output targets for the reporter.

    This allows specifying multiple targets for the reporter to output to.

    The targets are specified as a list of strings and validated against
    the allowed Target enum values. It support passing NO targets as well,
    in which case the reporter will use the default targets.

    Example: --json console filesystem callback
    """

    INVALID = 'invalid'
    """Invalid flag type.

    This is a testing placeholder and should not be used. It is included
    to test error handling for unsupported flag types.
    """
