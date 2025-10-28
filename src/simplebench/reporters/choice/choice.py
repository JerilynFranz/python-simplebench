"""Choice() for reporters."""
from __future__ import annotations
from typing import Any, Iterable, Optional, Sequence, TYPE_CHECKING

from simplebench.enums import Section, Target, Format, FlagType
from simplebench.exceptions import SimpleBenchTypeError
from simplebench.validators import (validate_sequence_of_str, validate_non_blank_string, validate_string,
                                    validate_sequence_of_type, validate_type)

# simplebench.reporters.reporter
from simplebench.reporters.reporter.options import ReporterOptions
from simplebench.reporters.reporter.metaclasses import IReporter

# simplebench.reporters.choice
from simplebench.reporters.choice.exceptions import ChoiceErrorTag
from simplebench.reporters.choice.metaclasses import IChoice


if TYPE_CHECKING:
    from ..reporter.reporter import Reporter


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
        flag_type: (FlagType): The type of command-line flag (e.g., boolean, target_list, etc.).
        name (str): A unique name for the choice.
        description (str): A brief description of the choice.
        sections (set[Section]): A set of Section enums to include in the report.
        targets (set[Target]): A set of Target enums for output.
        default_targets (set[Target] | None): A set of Target enums representing the default
            targets for the choice. If None, no default targets are specified and the reporter's defaults
            will be used when generating reports.
        output_format (Format): A Format instance describing the output format.
        subdir (str | None): An optional subdirectory for output files.
            If None, reports default to the reporter's subdir.
        file_suffix (str | None): An optional file suffix for output files.
            If None, reports default to the reporter's file_suffix.
        file_unique (bool | None): Whether to make output file names unique.
            If None, reports default to the reporter's file_unique.
        file_append (bool | None): Whether to append to existing output files.
            If None, reports default to the reporter's file_append.
        options (ReporterOptions | None): An optional ReporterOptions instance
            for additional configurations specific to a specific reporter.
            If None, reports default to the reporter's default options.
        extra (Any | None): Any additional metadata associated with the choice.

    """
    __slots__ = (
        '_reporter',
        '_flags',
        '_flag_type',
        '_name',
        '_description',
        '_sections',
        '_output_format',
        '_targets',
        '_default_targets',
        '_subdir',
        '_file_suffix',
        '_file_unique',
        '_file_append',
        '_options',
        '_extra',
    )

    def __init__(self, *,
                 reporter: Reporter,
                 flags: Sequence[str],
                 flag_type: FlagType,
                 name: str,
                 description: str,
                 sections: Sequence[Section],
                 output_format: Format,
                 targets: Sequence[Target],
                 default_targets: Iterable[Target] | None = None,
                 subdir: str | None = None,
                 file_suffix: str | None = None,
                 file_unique: bool | None = False,
                 file_append: bool | None = False,
                 options: ReporterOptions | None = None,
                 extra: Any = None) -> None:
        """Construct a Choice instance.

        Args:
            reporter (Reporter): An instance of a Reporter subclass.
            flags (Sequence[str]): A sequence of command-line flags associated with the choice.
            flag_type (FlagType): The type of command-line flag (e.g., boolean, target_list, etc.).
            name (str): A unique name for the choice.
            description (str): A brief description of the choice.
            sections (Sequence[Section]): A sequence of Section enums to include in the report.
            It must be non-empty, but Section.NULL may be included to indicate no sections are
            specifically selected. The reporter is expected to include listed sections in its report.
            output_format: A Format instance describing the output format.
            targets (Sequence[Target]): A sequence of Target enums for output. It must be non-empty.
             If multiple targets are specified, the reporter is expected to handle outputting
             to all specified targets when this choice is selected.
            default_targets (Sequence[Target] | None, default=None): An optional sequence of Target enums
                representing the default targets for the choice. If None, no default targets are specified
                and the reporter's defaults will be used when generating reports.
            subdir (str | None, default=None): An optional subdirectory for output files. If None, defaults
                to the reporter's default subdir. It may only consist of alphanumeric characters
                (a-z, A-Z, 0-9) or be an empty string (to indicate no subdirectory).
                It cannot be longer than 64 characters and may be left as None to use the reporter's default.
            file_suffix (str | None, default=None): An optional file suffix for output files. If None, defaults
                to the reporter's default file_suffix when generating reports. It may only consist of
                alphanumeric characters and be no longer than 10 characters.
            file_unique (bool | None, default=None): Whether to make output file names unique by appending
                a unique identifier. If None, defaults to the reporter's default file_unique setting.
            file_append (bool | None, default=None): Whether to append to existing output files instead of
                overwriting them. If None, defaults to the reporter's default file_append setting.
            options: (ReporterOptions | None, default=None):
                An optional ReporterOptions instance for additional configuration specific to a reporter.
                The option must be of the same type as that specified by the options_type property
                of the associated Reporter subclass.
            extra (Any, default=None): Any additional metadata associated with the choice.

        Raises:
            SimpleBenchTypeError: If any argument is of an incorrect type.
            SimpleBenchValueError: If any argument has an invalid value (e.g., empty strings or empty sequences).
        """
        if not isinstance(reporter, IReporter):
            raise SimpleBenchTypeError(
                "reporter must implement the Reporter interface",
                tag=ChoiceErrorTag.INVALID_REPORTER_ARG_TYPE)
        self._reporter: Reporter = reporter
        """The Reporter subclass instance associated with the choice"""

        self._flags: frozenset[str] = frozenset(validate_sequence_of_str(
            flags, "flags",
            ChoiceErrorTag.INVALID_FLAGS_ARG_TYPE,
            ChoiceErrorTag.INVALID_FLAGS_ARGS_VALUE,
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

        if not isinstance(flag_type, FlagType):
            raise SimpleBenchTypeError(
                "flag_type must be a FlagType enum value",
                tag=ChoiceErrorTag.INVALID_FLAG_TYPE_ARG_TYPE)
        self._flag_type: FlagType = flag_type
        """The type of command-line flag (e.g., FlagType.BOOLEAN, FlagType.TARGET_LIST, etc.).
        (private backing field)"""

        self._name: str = validate_non_blank_string(
            name, "name",
            ChoiceErrorTag.INVALID_NAME_ARG_TYPE,
            ChoiceErrorTag.EMPTY_NAME_ARG_VALUE)
        """Name of the choice
        (private backing field)"""

        self._description: str = validate_non_blank_string(
            description, "description",
            ChoiceErrorTag.INVALID_DESCRIPTION_ARG_TYPE,
            ChoiceErrorTag.EMPTY_DESCRIPTION_ARG_VALUE)
        """Description of the choice
        (private backing field)"""

        self._sections: frozenset[Section] = frozenset(validate_sequence_of_type(
            sections, Section,
            "sections",
            ChoiceErrorTag.INVALID_SECTIONS_ARG_TYPE,
            ChoiceErrorTag.EMPTY_SECTIONS_ARG_VALUE,
            allow_empty=False))
        """Sections included in the choice
        (private backing field)"""

        self._targets: frozenset[Target] = frozenset(validate_sequence_of_type(
            targets, Target,
            "targets",
            ChoiceErrorTag.INVALID_TARGETS_ARG_TYPE,
            ChoiceErrorTag.EMPTY_TARGETS_ARG_VALUE,
            allow_empty=False))
        """Output targets for the choice
        (private backing field)"""

        if default_targets is None:
            self._default_targets: frozenset[Target] = frozenset()
        else:
            self._default_targets: frozenset[Target] = frozenset(validate_sequence_of_type(
                list(default_targets), Target, "default_targets",
                ChoiceErrorTag.INVALID_TARGETS_ARG_TYPE,
                ChoiceErrorTag.EMPTY_TARGETS_ARG_VALUE,
                allow_empty=True))

        self._subdir: str | None = None
        """An optional subdirectory for output files.
        (private backing field)"""
        if subdir is not None:
            self._subdir = validate_string(
                subdir, "subdir",
                ChoiceErrorTag.INVALID_SUBDIR_ARG_TYPE,
                ChoiceErrorTag.INVALID_SUBDIR_ARG_VALUE,
                allow_empty=True,
                alphanumeric_only=True)
            if len(self._subdir) > 64:
                raise SimpleBenchTypeError(
                    "subdir cannot be longer than 64 characters",
                    tag=ChoiceErrorTag.SUBDIR_TOO_LONG)

        self._file_suffix: str | None = None
        """An optional file suffix for output files.
        (private backing field)"""
        if file_suffix is not None:
            file_suffix = validate_string(
                file_suffix, "file_suffix",
                ChoiceErrorTag.INVALID_FILE_SUFFIX_ARG_TYPE,
                ChoiceErrorTag.EMPTY_FILE_SUFFIX_ARG_VALUE,
                allow_empty=True, allow_blank=False, alphanumeric_only=True)
            if len(file_suffix) > 10:
                raise SimpleBenchTypeError(
                    "file_suffix cannot be longer than 10 characters",
                    tag=ChoiceErrorTag.FILE_SUFFIX_TOO_LONG)
            self._file_suffix = file_suffix

        self._file_unique: bool | None = None
        """Whether to make output file names unique.
        (private backing field)"""
        if file_unique is not None:
            if not isinstance(file_unique, bool):
                raise SimpleBenchTypeError(
                    "file_unique arg must be a boolean value or None",
                    tag=ChoiceErrorTag.INVALID_FILE_UNIQUE_ARG_TYPE)
            self._file_unique = file_unique

        self._file_append: bool | None = None
        """Whether to append to existing output files.
        (private backing field)"""
        if file_append is not None:
            if not isinstance(file_append, bool):
                raise SimpleBenchTypeError(
                    "file_append arg must be a boolean value or None",
                    tag=ChoiceErrorTag.INVALID_FILE_APPEND_ARG_TYPE)
            self._file_append = file_append

        self._output_format: Format = validate_type(
            value=output_format, expected=Format, name="output_format",
            error_tag=ChoiceErrorTag.INVALID_OUTPUT_FORMAT_ARG_TYPE)
        """Output format for the choice
        (private backing field)"""

        if options is not None:
            if not isinstance(options, ReporterOptions):
                raise SimpleBenchTypeError(
                    "options must be a ReporterOptions instance or None",
                    tag=ChoiceErrorTag.INVALID_OPTIONS_ARG_TYPE)
        self._options: ReporterOptions | None = options
        """An optional ReporterOptions for additional configuration of the reporter.
        (private backing field)"""

        self._extra: Optional[Any] = extra
        """Additional metadata associated with the choice.
        (private backing field)"""

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
    def flag_type(self) -> FlagType:
        """The type of command-line flag (e.g., FlagType.BOOLEAN, FlagType.TARGET_LIST, etc.)."""
        return self._flag_type

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
    def default_targets(self) -> frozenset[Target] | None:
        """Default output targets for the choice.

        These are the default output targets that the associated Reporter subclass
        should use when this choice is selected, if no specific target
         is provided by the user."""
        return self._default_targets

    @property
    def subdir(self) -> str | None:
        """An optional subdirectory for output files.

        If specified, the associated Reporter subclass should
        use this subdirectory for output files when this choice
        is selected. If an empty string, no subdirectory
        should be used. If None, the reporter's default subdir
        should be used."""
        return self._subdir

    @property
    def file_suffix(self) -> str | None:
        """An optional file suffix for output files.

        If specified, the associated Reporter subclass should
        use this file suffix for output files when this choice
        is selected. If None, the reporter's default file_suffix
        should be used."""
        return self._file_suffix

    @property
    def file_unique(self) -> bool | None:
        """Whether to make output file names unique.

        If specified, the associated Reporter subclass should
        use this setting for output files when this choice
        is selected. If None, the reporter's default file_unique
        setting should be used."""
        return self._file_unique

    @property
    def file_append(self) -> bool | None:
        """Whether to append to existing output files.

        If specified, the associated Reporter subclass should
        use this setting for output files when this choice
        is selected. If None, the reporter's default file_append
        setting should be used."""
        return self._file_append

    @property
    def output_format(self) -> Format:
        """Output format for the choice.

        This is the output format that the associated Reporter subclass
        is expected to use when this choice is selected.

        Returns:
            Format: The output format.
        """
        return self._output_format

    @property
    def options(self) -> ReporterOptions | None:
        """An optional ReporterOptions instance for additional configuration."""
        return self._options

    @property
    def extra(self) -> Any:
        """Any additional metadata associated with the choice."""
        return self._extra
