# -*- coding: utf-8 -*-
"""Choices for reporters."""
from __future__ import annotations
from collections import UserDict
from typing import Any, Optional, Sequence, TYPE_CHECKING

from .metaclasses import IChoice, IChoices, IReporter
from ..enums import Section, Target, Format
from ..exceptions import SimpleBenchTypeError, SimpleBenchValueError, SimpleBenchKeyError, ErrorTag
from ..validators import validate_sequence_of_str, validate_non_blank_string, validate_sequence_of_type


if TYPE_CHECKING:
    from .interfaces import Reporter


class Choice(IChoice):
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

    Choices are normally created and registered with the ReporterManager
    by the Reporter subclass itself during its initialization. The reporter
    argument in the Choice constructor is expected to be initialized
    with the instance of the Reporter subclass that is creating the Choice
    instance. This establishes the association between the Choice and
    the Reporter subclass that is creating it.

    This implies that the Reporter subclass must be instantiated
    before the Choice instances can be created. Therefore, the
    typical pattern is for the Reporter subclass to create its Choice
    instances in its __init__() method before calling the super().__init__() method
    of the Reporter base class. This ensures that the Reporter subclass
    instance is available to be passed as the reporter argument when
    creating the Choice instances.

    Attributes:
        reporter (Reporter): The Reporter subclass instance associated with the choice.
        flags (set[str]): A set of command-line flags associated with the choice.
        name (str): A unique name for the choice.
        description (str): A brief description of the choice.
        sections (set[Section]): A set of Section enums to include in the report.
        targets (set[Target]): A set of Target enums for output.
        formats (set[Format]): A set of Format enums for output.
        extra (Any | None): Any additional metadata associated with the choice.

    """
    __slots__ = (
        '_reporter',
        '_flags',
        '_name',
        '_description',
        '_sections',
        '_targets',
        '_formats',
        '_extra',
    )

    def __init__(self, *,
                 reporter: Reporter,
                 flags: Sequence[str],
                 name: str,
                 description: str,
                 sections: Sequence[Section],
                 targets: Sequence[Target],
                 formats: Sequence[Format],
                 extra: Any = None) -> None:
        """Construct a Choice instance.

        Args:
            reporter (Reporter): An instance of a Reporter subclass.
            flags (Sequence[str]): A sequence of command-line flags associated with the choice.
            name (str): A unique name for the choice.
            description (str): A brief description of the choice.
            sections (Sequence[Section]): A sequence of Section enums to include in the report.
            targets (Sequence[Target]): A sequence of Target enums for output.
            formats (Sequence[Format]): A sequence of Format enums for output.
            extra (Any, default=None): Any additional metadata associated with the choice.

        Raises:
            SimpleBenchTypeError: If any argument is of an incorrect type.
            SimpleBenchValueError: If any argument has an invalid value (e.g., empty strings or empty sequences).
        """
        if not isinstance(reporter, IReporter):
            raise SimpleBenchTypeError(
                "reporter must implement the Reporter interface",
                tag=ErrorTag.CHOICE_INVALID_REPORTER_ARG_TYPE)
        self._reporter: Reporter = reporter
        """The Reporter subclass instance associated with the choice"""

        self._flags: frozenset[str] = frozenset(validate_sequence_of_str(
            flags, "flags",
            ErrorTag.CHOICE_INVALID_FLAGS_ARG_TYPE,
            ErrorTag.CHOICE_INVALID_FLAGS_ARGS_VALUE,
            allow_empty=False, allow_blank=False, allow_whitespace=False))
        """Flags associated with the choice. These are used for command-line selection.
        They must be unique across all choices for all reporters. This is enforced
        by the ReporterManager when choices are registered.

        The flags should be in the format used on the command line,
        typically starting with '--' for long options.

        Example: ['--json', '--json-full']

        The description property of the Choice is used to provide
        help text for the flags when generating command-line help.
        """

        self._name: str = validate_non_blank_string(
            name, "name",
            ErrorTag.CHOICE_INVALID_NAME_ARG_TYPE,
            ErrorTag.CHOICE_EMPTY_NAME_ARG_VALUE)
        """Name of the choice"""

        self._description: str = validate_non_blank_string(
            description, "description",
            ErrorTag.CHOICE_INVALID_DESCRIPTION_ARG_TYPE,
            ErrorTag.CHOICE_EMPTY_DESCRIPTION_ARG_VALUE)
        """Description of the choice"""

        self._sections: frozenset[Section] = frozenset(validate_sequence_of_type(
            sections, Section,
            "sections",
            ErrorTag.CHOICE_INVALID_SECTIONS_ARG_TYPE,
            ErrorTag.CHOICE_EMPTY_SECTIONS_ARG_VALUE,
            allow_empty=False))
        """Sections included in the choice"""

        self._targets: frozenset[Target] = frozenset(validate_sequence_of_type(
            targets, Target,
            "targets",
            ErrorTag.CHOICE_INVALID_TARGETS_ARG_TYPE,
            ErrorTag.CHOICE_EMPTY_TARGETS_ARG_VALUE,
            allow_empty=False))
        """Output targets for the choice"""

        self._formats: frozenset[Format] = frozenset(validate_sequence_of_type(
            formats, Format,
            "formats",
            ErrorTag.CHOICE_INVALID_FORMATS_ARG_TYPE,
            ErrorTag.CHOICE_EMPTY_FORMATS_ARG_VALUE,
            allow_empty=False))
        """Output formats for the choice"""

        self._extra: Optional[Any] = extra
        """Additional metadata associated with the choice."""

    @property
    def reporter(self) -> Reporter:
        """The reporter sub-class associated with the choice."""
        return self._reporter

    @property
    def flags(self) -> frozenset[str]:
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
    def sections(self) -> frozenset[Section]:
        """Sections included in the choice.

        These are the sections that the associated Reporter subclass
        is expected to include in its report when this choice is selected."""
        return self._sections

    @property
    def targets(self) -> frozenset[Target]:
        """Output targets for the choice.

        These are the output targets that the associated Reporter subclass
        is expected to use when this choice is selected."""
        return self._targets

    @property
    def formats(self) -> frozenset[Format]:
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
    def extra(self) -> Any:
        """Any additional metadata associated with the choice."""
        return self._extra


class Choices(UserDict[str, Choice], IChoices):
    """A dictionary-like container for Choice instances."""
    def __init__(self, choices: Sequence[Choice] | Choices | None = None) -> None:
        """Construct a Choices container.

        Args:
            choices (Sequence[Choice] | Choices): An optional sequence of Choice instances
                or another Choices instance to initialize the container with.
                If not provided, the container will be initialized empty."""
        self._args_index: dict[str, Choice] = {}
        self._flags_index: dict[str, Choice] = {}
        super().__init__()
        choices_list: list[Choice] = []
        if isinstance(choices, Sequence) and not isinstance(choices, str):
            choices_list = validate_sequence_of_type(
                choices, Choice, "choices",
                ErrorTag.CHOICES_INVALID_CHOICES_ARG_SEQUENCE_TYPE,
                ErrorTag.CHOICES_INVALID_CHOICES_ITEM_VALUE,
                allow_empty=True)
        elif choices is not None:
            if isinstance(choices, Choices):
                choices_list = list(choices.values())
            else:
                raise SimpleBenchTypeError(
                    f"Expected a Sequence of Choice instances or a Choices instance but got {type(choices)}",
                    tag=ErrorTag.CHOICES_INVALID_CHOICES_ARG_TYPE)

        if choices_list:
            self.extend(choices_list)

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
                tag=ErrorTag.CHOICES_ADD_INVALID_CHOICE_ARG_TYPE)
        self[choice.name] = choice

    def all_choice_args(self) -> set[str]:
        """Return a set of all Namespace arg names from all Choice instances in the container.

        Returns:
            set[str]: A set of all Namespace arg names from all Choice instances.
        """
        return set(self._args_index.keys())

    def all_choice_flags(self) -> set[str]:
        """Return a set of all CLI flags from all Choice instances in the container.

        Returns:
            set[str]: A set of all CLI flags from all Choice instances.
        """
        return set(self._flags_index.keys())

    def get_choice_for_arg(self, arg: str) -> Choice | None:
        """Return the Choice instance associated with the given Namespace arg name.

        Args:
            arg (str): The Namespace arg name to look up.

        Returns:
            Choice | None: The Choice instance associated with the arg,
                or None if no such Choice exists.

        Raises:
            SimpleBenchTypeError: If the arg is not a string.
        """
        if not isinstance(arg, str):
            raise SimpleBenchTypeError(
                "arg must be a string",
                tag=ErrorTag.CHOICES_GET_CHOICE_FOR_ARG_INVALID_ARG_TYPE)
        return self._args_index.get(arg, None)

    def extend(self, choices: Sequence[Choice]) -> None:
        """Add Choice instances to the container.

        Args:
            choices (Sequence[Choice] | Choices): A sequence of Choice instances or an instance of Choices.

        Raises:
            SimpleBenchTypeError: If the choices argument is not a Sequence of Choice instances or a Choices instance.
            SimpleBenchValueError: If any Choice in the sequence has a duplicate name that already exists in
                the container.
        """
        if isinstance(choices, Choices):
            for choice in choices.values():
                self.add(choice)
        else:
            choices_list = validate_sequence_of_type(
                choices, Choice, "choices",
                ErrorTag.CHOICES_EXTEND_INVALID_CHOICES_ARG_SEQUENCE_TYPE,
                ErrorTag.CHOICES_EXTEND_INVALID_CHOICES_ITEM_VALUE,
                allow_empty=True)
            for choice in choices_list:
                self.add(choice)

    def remove(self, name: str) -> None:
        """Remove a Choice instance from the container by its name.

        Args:
            name (str): The name of the Choice instance to remove.
        Raises:
            SimpleBenchKeyError: If no Choice under the given name exists in the container.
        """
        del self[name]

    # custom __delitem__ method to maintain indexes
    def __delitem__(self, key: str) -> None:
        """Remove a Choice instance from the container by its name.

        Args:
            name (str): The name of the Choice instance to remove.

        Raises:
            SimpleBenchKeyError: If no Choice under the given name exists in the container.
        """
        if key not in self.data:
            raise SimpleBenchKeyError(
                f"No Choice key with the name '{key}' exists",
                tag=ErrorTag.CHOICES_DELITEM_UNKNOWN_CHOICE_NAME)
        choice = self[key]
        for arg in choice.flags:
            if arg in self._flags_index:
                del self._flags_index[arg]
            arg_key = arg.replace('--', '', 1).replace('-', '_')
            if arg_key in self._args_index:
                del self._args_index[arg_key]
        super().__delitem__(key)

    # custom __setitem__ method to make Choices into a type restricted dict
    def __setitem__(self, key: str, value: Choice) -> None:
        """Set a value in the Choices container.

        This restricts setting values to only Choice instances with string keys
        and raises an error otherwise. It also prevents duplicate Choice names.

        It also restricts the key to match the Choice.name attribute and updates
        the internal indexes accordingly.

          Example:
            choices = Choices()
            choice = Choice(...)
            choices['my_choice'] = choice

        Args:
            key (str): The key under which to store the Choice instance.
            value (Choice): The Choice instance to store.

        Raises:
            SimpleBenchTypeError: If the key is not a string or the value is not a Choice instance.
            SimpleBenchValueError: If a Choice with the same name already exists
                in the container; if the key does not match the Choice.name attribute;
                or if a Choice with the same flag already exists in the container.
        """
        if not isinstance(key, str):
            raise SimpleBenchTypeError(
                "Choice key must be a string",
                tag=ErrorTag.CHOICES_SETITEM_INVALID_KEY_TYPE)
        if not isinstance(value, Choice):
            raise SimpleBenchTypeError(
                "Only Choice instances can be added to Choices",
                tag=ErrorTag.CHOICES_SETITEM_INVALID_VALUE_TYPE)
        if key != value.name:
            raise SimpleBenchValueError(
                "Choice key must match the Choice.name attribute",
                tag=ErrorTag.CHOICES_SETITEM_KEY_NAME_MISMATCH)
        if value.name in self.data:
            raise SimpleBenchValueError(
                f"A Choice with the name '{value.name}' already exists",
                tag=ErrorTag.CHOICES_SETITEM_DUPLICATE_CHOICE_NAME)

        self._args_index.update({flag.replace('--', '', 1).replace('-', '_'): value for flag in value.flags})
        for flag in value.flags:
            if flag in self._flags_index:
                raise SimpleBenchValueError(
                    f"A Choice with the flag '{flag}' already exists",
                    tag=ErrorTag.CHOICES_SETITEM_DUPLICATE_CHOICE_FLAG)
            self._flags_index[flag] = value
        super().__setitem__(key, value)
