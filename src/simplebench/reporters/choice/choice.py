"""Choice() for reporters."""
from __future__ import annotations
from collections.abc import Hashable
from typing import Any, TYPE_CHECKING

from simplebench.enums import Section, Target, Format, FlagType
from simplebench.validators import validate_type

from simplebench.reporters.protocols import ChoiceProtocol
from simplebench.reporters.reporter.options import ReporterOptions
from simplebench.reporters.choice.choice_conf import ChoiceConf
from simplebench.reporters.choice.exceptions import ChoiceErrorTag
from simplebench.reporters.choice.metaclasses import IChoice


_REPORTER_IMPORTED: bool = False
"""Indicates whether Reporter has been imported yet."""


def deferred_reporter_import() -> None:
    """Deferred import of Reporter to avoid circular imports during initialization."""
    global Reporter, _REPORTER_IMPORTED  # pylint: disable=global-statement
    if _REPORTER_IMPORTED:
        return
    from simplebench.reporters.reporter.reporter import Reporter  # pylint: disable=import-outside-toplevel
    _REPORTER_IMPORTED = True


if TYPE_CHECKING:
    from simplebench.reporters.reporter.reporter import Reporter


class Choice(Hashable, IChoice, ChoiceProtocol):
    """Definition of a Choice option for live use by reporters.

    A Choice represents a specific configuration of a Reporter subclass,
    including the sections to include in the report,
    the output targets, and the output formats.

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

    Choice instances are created by the Reporter subclass from
    ChoiceConf instances during a Reporter's instantation process.

    Separating ChoiceConf and Choice allows for a clear distinction
    between the configuration data (ChoiceConf) and the live,
    operational representation (Choice) used by the Reporter subclass.

    Attributes:
        reporter (Reporter): The Reporter subclass instance associated with the choice.
        choice_conf (ChoiceConf): The ChoiceConf instance used to create the choice.
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
        '_choice_conf'
    )

    def __init__(self, *,
                 reporter: Reporter,
                 choice_conf: ChoiceConf) -> None:
        """Construct a Choice instance from a Reporter and a ChoiceConf instance.

        Args:
            reporter (Reporter): An instance of a Reporter subclass.
            choice_conf (ChoiceConf): An instance of ChoiceConf containing
                the configuration for the choice.

        Raises:
            SimpleBenchTypeError: If any argument is of an incorrect type.
            SimpleBenchValueError: If any argument has an invalid value (e.g., empty strings or empty sequences).
        """
        deferred_reporter_import()

        self._reporter: Reporter = validate_type(
            reporter, Reporter, "reporter",
            error_tag=ChoiceErrorTag.REPORTER_INVALID_ARG_TYPE)
        """The Reporter subclass instance associated with the choice
        (private backing field for attribute)"""

        self._choice_conf: ChoiceConf = validate_type(
            choice_conf, ChoiceConf, "choice_conf",
            error_tag=ChoiceErrorTag.CHOICE_CONF_INVALID_ARG_TYPE)
        """The ChoiceConf instance used to create the choice
        (private backing field for attribute)"""

    @property
    def reporter(self) -> Reporter:
        """The reporter sub-class associated with the choice."""
        return self._reporter

    @property
    def choice_conf(self) -> ChoiceConf:
        """The ChoiceConf instance used to create the choice."""
        return self._choice_conf

    # All the properties below simply proxy to the underlying ChoiceConf instance
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
        return self._choice_conf.flags

    @property
    def flag_type(self) -> FlagType:
        """The type of command-line flag (e.g., FlagType.BOOLEAN, FlagType.TARGET_LIST, etc.)."""
        return self._choice_conf.flag_type

    @property
    def name(self) -> str:
        """Name of the choice."""
        return self._choice_conf.name

    @property
    def description(self) -> str:
        """Description of the choice.

        This is used as help text for the command-line flags associated with the choice."""
        return self._choice_conf.description

    @property
    def sections(self) -> frozenset[Section]:
        """Sections included in the choice.

        These are the sections that the associated Reporter subclass
        is expected to include in its report when this choice is selected."""
        return self._choice_conf.sections

    @property
    def targets(self) -> frozenset[Target]:
        """Output targets for the choice.

        These are the output targets that the associated Reporter subclass
        is expected to use when this choice is selected."""
        return self._choice_conf.targets

    @property
    def default_targets(self) -> frozenset[Target] | None:
        """Default output targets for the choice.

        These are the default output targets that the associated Reporter subclass
        should use when this choice is selected, if no specific target
         is provided by the user."""
        return self._choice_conf.default_targets

    @property
    def subdir(self) -> str | None:
        """An optional subdirectory for output files.

        If specified, the associated Reporter subclass should
        use this subdirectory for output files when this choice
        is selected. If an empty string, no subdirectory
        should be used. If None, the reporter's default subdir
        should be used."""
        return self._choice_conf.subdir

    @property
    def file_suffix(self) -> str | None:
        """An optional file suffix for output files.

        If specified, the associated Reporter subclass should
        use this file suffix for output files when this choice
        is selected. If None, the reporter's default file_suffix
        should be used."""
        return self._choice_conf.file_suffix

    @property
    def file_unique(self) -> bool | None:
        """Whether to make output file names unique.

        If specified, the associated Reporter subclass should
        use this setting for output files when this choice
        is selected. If None, the reporter's default file_unique
        setting should be used."""
        return self._choice_conf.file_unique

    @property
    def file_append(self) -> bool | None:
        """Whether to append to existing output files.

        If specified, the associated Reporter subclass should
        use this setting for output files when this choice
        is selected. If None, the reporter's default file_append
        setting should be used."""
        return self._choice_conf.file_append

    @property
    def output_format(self) -> Format:
        """Output format for the choice.

        This is the output format that the associated Reporter subclass
        is expected to use when this choice is selected.

        Returns:
            Format: The output format.
        """
        return self._choice_conf.output_format

    @property
    def options(self) -> ReporterOptions | None:
        """An optional ReporterOptions instance for additional configuration."""
        return self._choice_conf.options

    @property
    def extra(self) -> Any:
        """Any additional metadata associated with the choice."""
        return self._choice_conf.extra

    def __hash__(self) -> int:
        """Compute a hash value for the ChoiceConf instance.

        Returns:
            int: The computed hash value.
        """
        return hash((
            self.flags,
            self.flag_type,
            self.name,
            self.description,
            self.sections,
            self.targets,
            self.default_targets,
            self.subdir,
            self.file_suffix,
            self.file_unique,
            self.file_append,
            self.output_format,
            self.options,
            self.extra,
            id(self.reporter)
        ))

    def __eq__(self, other: object) -> bool:
        """Check equality between two ChoiceConf instances.

        Args:
            other (object): The other ChoiceConf instance to compare against.

        Returns:
            bool: True if the ChoiceConf instances are equal, False otherwise.
        """
        if not isinstance(other, Choice):
            return False

        return (self.flags == other.flags and
                self.flag_type == other.flag_type and
                self.name == other.name and
                self.description == other.description and
                self.sections == other.sections and
                self.targets == other.targets and
                self.default_targets == other.default_targets and
                self.subdir == other.subdir and
                self.file_suffix == other.file_suffix and
                self.file_unique == other.file_unique and
                self.file_append == other.file_append and
                self.output_format == other.output_format and
                self.options == other.options and
                self.extra == other.extra and
                id(self.reporter) == id(other.reporter))
