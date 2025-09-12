# -*- coding: utf-8 -*-
"""Choices for reporters."""
from __future__ import annotations

from collections import UserDict
from enum import Enum
from typing import Any, Optional, Sequence

from ..exceptions import SimpleBenchTypeError, SimpleBenchValueError, ErrorTag
from .interfaces import Reporter


class Section(str, Enum):
    """Categories for report sections.

    The string values are used to load the data accessor methods by attribute name in the Results class
    and name generated files."""
    OPS = 'ops_per_second'
    """Operations per second section."""
    TIMING = 'per_round_timings'
    """Time per round section."""
    MEMORY = 'memory_usage'
    """Memory usage section."""

    def __contains__(self, item: Any) -> bool:
        """Check if the item is a valid Section."""
        return isinstance(item, Section) or item in self._value2member_map_


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


class Choice:
    """Definition of a Choice option for reporters.

    A Choice represents a specific configuration of a Reporter subclass,
    including the sections to include in the report, the output targets,
    and the output formats.

    The Choice class provides a structured way to define and manage
    different reporting options within the SimpleBench framework so that
    users can select from predefined configurations and developers can
    easily add new reporting options to the framework.

    A Choice instance is immutable after creation to ensure consistency
    in reporting configurations.

    The sections, targets, and formats are descriptive only; they do not
    enforce any behavior on the associated Reporter subclass. It is the
    responsibility of the Reporter subclass to implement the behavior
    corresponding to the specified sections, targets, and formats.

    It is intended that multiple Choice instances can be created
    for a single Reporter subclass to represent different configurations
    of that reporter. For example, a JSON reporter might have one
    Choice that includes all sections and outputs to the filesystem,
    and another Choice that includes only the OPS section and outputs
    to the console. This allows users to select from a variety of
    predefined reporting configurations without needing to create
    multiple Reporter subclasses.

    Args:
        reporter (Reporter): An instance of a Reporter subclass.
        flags (Sequence[str]): A sequence of command-line flags associated with the choice.
        name (str): A unique name for the choice.
        description (str): A brief description of the choice.
        sections (Sequence[Section]): A sequence of Section enums to include in the report.
        targets (Sequence[Target]): A sequence of Target enums for output.
        formats (Sequence[Format]): A sequence of Format enums for output.
        extra (dict[str, Any], optional): A dictionary for any additional metadata.

    Raises:
        SimpleBenchTypeError: If any argument is of an incorrect type.
        SimpleBenchValueError: If any argument has an invalid value (e.g., empty strings or empty sequences).
    """
    def __init__(self,
                 reporter: Reporter,
                 flags: Sequence[str],
                 name: str,
                 description: str,
                 sections: Sequence[Section],
                 targets: Sequence[Target],
                 formats: Sequence[Format],
                 extra: Optional[dict[str, Any]] = None) -> None:
        if not isinstance(reporter, Reporter):
            raise SimpleBenchTypeError(
                "reporter must implement the Reporter interface",
                ErrorTag.CHOICE_INIT_INVALID_REPORTER_ARG)
        self._reporter: Reporter = reporter
        """The Reporter sub-class instance associated with the choice"""

        if not isinstance(flags, Sequence) or not all(isinstance(f, str) for f in flags):
            raise SimpleBenchTypeError(
                "flags must be a sequence of strings",
                ErrorTag.CHOICE_INIT_INVALID_NAME_ARG)
        self._flags: set[str] = set(flags)
        """Flags associated with the choice. These are used for command-line selection.
        They must be unique across all choices for all reporters. This is enforced
        by the ReporterManager when choices are registered.

        The flags should be in the format used on the command line,
        typically starting with '--' for long options.

        Example: ['--json', '--json-full']

        The description property of the Choice is used to provide
        help text for the flags when generating command-line help.
        """

        if not isinstance(name, str):
            raise SimpleBenchTypeError(
                "Name must be a string",
                ErrorTag.CHOICE_INIT_INVALID_NAME_ARG)
        if not name:
            raise SimpleBenchValueError(
                "Name cannot be an empty string",
                ErrorTag.CHOICE_INIT_EMPTY_STRING_NAME)
        self._name: str = name
        """Name of the choice"""

        if not isinstance(description, str):
            raise SimpleBenchTypeError(
                "Description must be a string",
                ErrorTag.CHOICE_INIT_INVALID_DESCRIPTION_ARG)
        if not description:
            raise SimpleBenchValueError(
                "Description cannot be an empty string",
                ErrorTag.CHOICE_INIT_EMPTY_STRING_DESCRIPTION)
        self._description: str = description
        """Description of the choice"""

        if not isinstance(sections, Sequence) or not all(isinstance(s, Section) for s in sections):
            raise SimpleBenchTypeError(
                "Sections must be a sequence of Section enums",
                ErrorTag.CHOICE_INIT_INVALID_SECTIONS_ARG)
        if not sections:
            raise SimpleBenchValueError(
                "Sections cannot be an empty sequence",
                ErrorTag.CHOICE_INIT_EMPTY_SECTIONS)
        self._sections: set[Section] = set(sections)
        """Sections included in the choice"""

        if not isinstance(targets, Sequence) or not all(isinstance(t, Target) for t in targets):
            raise SimpleBenchTypeError(
                "Output targets must be a sequence of Target enums",
                ErrorTag.CHOICE_INIT_INVALID_TARGETS_ARG)
        if not targets:
            raise SimpleBenchValueError(
                "Output targets cannot be an empty sequence",
                ErrorTag.CHOICE_INIT_EMPTY_TARGETS)
        self._targets: set[Target] = set(targets)
        """Output targets for the choice"""

        if not isinstance(formats, Sequence) or not all(isinstance(f, Format) for f in formats):
            raise SimpleBenchTypeError(
                "Output formats must be a sequence of Format enums",
                ErrorTag.CHOICE_INIT_INVALID_FORMATS_ARG)
        if not formats:
            raise SimpleBenchValueError(
                "Output formats cannot be an empty sequence",
                ErrorTag.CHOICE_INIT_EMPTY_FORMATS)
        self._formats: set[Format] = set(formats)
        """Output formats for the choice"""

        self._extra: dict[str, Any] = extra if extra is not None else {}
        """A dictionary for any additional metadata associated with the choice."""

    @property
    def reporter(self) -> Reporter:
        """The reporter sub-class associated with the choice."""
        return self._reporter

    @property
    def flags(self) -> set[str]:
        """Flags associated with the choice. These are used for command-line selection.
        They must be unique across all choices for all reporters. This is enforced
        by the ReporterManager when choices are registered.

        The flags should be in the format used on the command line,
        typically starting with '--' for long options.

        Example: ['--json', '--json-full']

        The description property of the Choice is used to provide
        help text for the flags when generating command-line help.
        """
        return self._flags

    @property
    def name(self) -> str:
        """Name of the choice."""
        return self._name

    @property
    def description(self) -> str:
        """Description of the choice.

        This is used as help text for the command-line flags associated with the choice."""
        return self._description

    @property
    def sections(self) -> set[Section]:
        """Sections included in the choice.

        These are the sections that the associated Reporter subclass
        is expected to include in its report when this choice is selected."""
        return self._sections

    @property
    def targets(self) -> set[Target]:
        """Output targets for the choice.

        These are the output targets that the associated Reporter subclass
        is expected to use when this choice is selected."""
        return self._targets

    @property
    def formats(self) -> set[Format]:
        """Output formats for the choice.

        These are the output formats that the associated Reporter subclass
        is expected to use when this choice is selected.

        The associated Reporter subclass is not required to support
        all specified formats; it should handle unsupported formats
        gracefully, for example by ignoring them or providing a warning.

        The formats are drawn from the Format enum defined in this module
        and represent common output formats used in reporting benchmark results.

        They imply the implementation of specific output methods in the Reporter subclass,
        such as text_report() for PLAIN_TEXT, rich_text_report() for RICH_TEXT,
        and so on.
        """
        return self._formats

    @property
    def extra(self) -> dict[str, Any]:
        """A dictionary for any additional metadata associated with the choice."""
        return self._extra


class Choices(UserDict[str, Choice]):
    """A dictionary-like container for Choice instances."""
    def __init__(self) -> None:
        self._args_index: dict[str, Choice] = {}
        self._flags_index: dict[str, Choice] = {}
        super().__init__()

    def add(self, choice: Choice) -> None:
        """Add a Choice instance to the container.

        The choice name attribute is used as the key in the container.

        Args:
            choice (Choice): The Choice instance to add.

        Raises:
            SimpleBenchTypeError: If the argument is not a Choice instance.
            SimpleBenchValueError: If a Choice with the same name already exists in the container.
        """
        if not isinstance(choice, Choice):
            raise SimpleBenchTypeError(
                "Expected a Choice instance",
                ErrorTag.CHOICES_ADD_INVALID_CHOICE_ARG)
        if choice.name in self.data:
            raise SimpleBenchValueError(
                f"A Choice with the name '{choice.name}' already exists",
                ErrorTag.CHOICES_ADD_DUPLICATE_CHOICE_NAME)
        self.data[choice.name] = choice
        self._args_index.update({arg.replace('--', '', 1).replace('-', '_'): choice for arg in choice.flags})

    def all_choice_args(self) -> set[str]:
        """Return a set of all Namespace args from all Choice instances in the container.

        Returns:
            set[str]: A set of all Namespace args from all Choice instances.
        """
        return set(self._args_index.keys())

    def all_choice_flags(self) -> set[str]:
        """Return a set of all CLI flags from all Choice instances in the container.

        Returns:
            set[str]: A set of all CLI flags from all Choice instances.
        """
        return set(self._flags_index.keys())

    def get_choice_for_arg(self, arg: str) -> Choice | None:
        """Return the Choice instance associated with the given Namespace arg.

        Args:
            arg (str): The Namespace arg to look up.

        Returns:
            Choice | None: The Choice instance associated with the arg,
                or None if no such Choice exists.
        """
        return self._args_index.get(arg, None)

    def extend(self, choices: Sequence[Choice] | Choices) -> None:
        """Add multiple Choice instances to the container.

        This method accepts either a sequence of Choice instances or a Choices
        instance and adds each Choice to the container.
        """
        if isinstance(choices, Choices):
            for choice in choices.values():
                self.add(choice)
        elif isinstance(choices, Sequence):
            for choice in choices:
                self.add(choice)
        else:
            raise SimpleBenchTypeError(
                "Expected a Sequence of Choice instances or a Choices instance",
                ErrorTag.CHOICES_EXTEND_INVALID_CHOICES_ARG)

    def remove(self, name: str) -> None:
        """Remove a Choice instance from the container by its name.

        Args:
            name (str): The name of the Choice instance to remove.

        Raises:
            SimpleBenchValueError: If no Choice with the given name exists in the container.
        """
        if name not in self.data:
            raise SimpleBenchValueError(
                f"No Choice with the name '{name}' exists",
                ErrorTag.CHOICES_REMOVE_UNKNOWN_CHOICE_NAME)
        choice = self.data[name]
        del self.data[name]
        for arg in choice.flags:
            if arg in self._flags_index:
                del self._flags_index[arg]
            arg_key = arg.replace('--', '', 1).replace('-', '_')
            if arg_key in self._args_index:
                del self._args_index[arg_key]
