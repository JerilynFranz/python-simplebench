"""``Choice()`` for reporters."""
from __future__ import annotations

from collections.abc import Hashable
from typing import TYPE_CHECKING, Any

from simplebench.enums import FlagType, Format, Section, Target
from simplebench.reporters.choice.choice_conf import ChoiceConf
from simplebench.reporters.choice.exceptions import ChoiceErrorTag
from simplebench.reporters.choice.metaclasses import IChoice
from simplebench.reporters.protocols import ChoiceProtocol
from simplebench.reporters.reporter.options import ReporterOptions
from simplebench.validators import validate_type

_REPORTER_IMPORTED: bool = False
"""Indicates whether Reporter has been imported yet."""


def deferred_reporter_import() -> None:
    """Deferred import of :class:`~simplebench.reporters.reporter.Reporter`
    to avoid circular imports during initialization.
    """
    global Reporter, _REPORTER_IMPORTED  # pylint: disable=global-statement
    if _REPORTER_IMPORTED:
        return
    from simplebench.reporters.reporter.reporter import Reporter  # pylint: disable=import-outside-toplevel
    _REPORTER_IMPORTED = True


if TYPE_CHECKING:
    from simplebench.reporters.reporter.reporter import Reporter


class Choice(Hashable, IChoice, ChoiceProtocol):
    """Definition of a :class:`~.Choice` option for live use by reporters.

    A :class:`~.Choice` represents a specific configuration of a
    :class:`~simplebench.reporters.reporter.Reporter` subclass,
    including the sections to include in the report,
    the output targets, and the output formats.

    The :class:`~.Choice` class provides a structured way to define and manage
    different reporting options within the SimpleBench framework so that
    users can select from predefined configurations and developers can
    easily add new reporting options to the framework.

    A :class:`~.Choice` instance is immutable after creation to ensure consistency
    in reporting configurations.

    The sections, targets, and formats are descriptive only; they do not
    enforce any behavior on the associated :class:`~simplebench.reporters.reporter.Reporter`
    subclass. It is the responsibility of the :class:`~simplebench.reporters.reporter.Reporter`
    subclass to implement the behavior corresponding to the specified sections, targets,
    and formats.

    It is intended that multiple :class:`~.Choice` instances can be created
    for a single :class:`~simplebench.reporters.reporter.Reporter` subclass to represent
    different configurations of that reporter. For example, a JSON reporter might have one
    :class:`~.Choice` that includes all sections and outputs to the filesystem,
    and another :class:`~.Choice` that includes only the OPS section and outputs
    to the console. This allows users to select from a variety of
    predefined reporting configurations without needing to create
    multiple :class:`~simplebench.reporters.reporter.Reporter` subclasses.

    :class:`~.Choice` instances are created by the :class:`~simplebench.reporters.reporter.Reporter`
    subclass from :class:`~.ChoiceConf` instances during a
    :class:`~simplebench.reporters.reporter.Reporter`'s instantation process.

    Separating :class:`~.ChoiceConf` and :class:`~.Choice` allows for a clear distinction
    between the configuration data (:class:`~.ChoiceConf`) and the live,
    operational representation (:class:`~.Choice`) used by the
    :class:`~simplebench.reporters.reporter.Reporter` subclass.

    :param reporter: The :class:`~simplebench.reporters.reporter.Reporter` subclass instance
                     associated with the choice.
    :type reporter: :class:`~simplebench.reporters.reporter.Reporter`
    :param choice_conf: The :class:`~.ChoiceConf` instance used to create the choice.
    :type choice_conf: :class:`~.ChoiceConf`
    :param flags: A set of command-line flags associated with the choice.
    :type flags: set[str]
    :param flag_type: The type of command-line flag (e.g., boolean, target_list, etc.).
    :type flag_type: :class:`~simplebench.enums.FlagType`
    :param name: A unique name for the choice.
    :type name: str
    :param description: A brief description of the choice.
    :type description: str
    :param sections: A set of :class:`~simplebench.enums.Section` enums to include in the report.
    :type sections: set[:class:`~simplebench.enums.Section`]
    :param targets: A set of :class:`~simplebench.enums.Target` enums for output.
    :type targets: set[:class:`~simplebench.enums.Target`]
    :param default_targets: A set of :class:`~simplebench.enums.Target` enums representing the
                            default targets for the choice. If ``None``, no default targets are
                            specified and the reporter's defaults will be used when generating
                            reports.
    :type default_targets: set[:class:`~simplebench.enums.Target`] | None
    :param output_format: A :class:`~simplebench.enums.Format` instance describing the output
                          format.
    :type output_format: :class:`~simplebench.enums.Format`
    :param subdir: An optional subdirectory for output files. If ``None``, reports default to
                   the reporter's subdir.
    :type subdir: str | None
    :param file_suffix: An optional file suffix for output files. If ``None``, reports default
                        to the reporter's file_suffix.
    :type file_suffix: str | None
    :param file_unique: Whether to make output file names unique. If ``None``, reports default
                        to the reporter's file_unique.
    :type file_unique: bool | None
    :param file_append: Whether to append to existing output files. If ``None``, reports default
                        to the reporter's file_append.
    :type file_append: bool | None
    :param options: An optional :class:`~simplebench.reporters.reporter.options.ReporterOptions`
                    instance for additional configurations specific to a specific reporter.
                    If ``None``, reports default to the reporter's default options.
    :type options: :class:`~simplebench.reporters.reporter.options.ReporterOptions` | None
    :param extra: Any additional metadata associated with the choice.
    :type extra: Any | None
    """
    __slots__ = (
        '_reporter',
        '_choice_conf'
    )

    def __init__(self, *,
                 reporter: Reporter,
                 choice_conf: ChoiceConf) -> None:
        """Construct a :class:`~.Choice` instance from a
        :class:`~simplebench.reporters.reporter.Reporter` and a :class:`~.ChoiceConf` instance.

        :param reporter: An instance of a :class:`~simplebench.reporters.reporter.Reporter`
                         subclass.
        :type reporter: :class:`~simplebench.reporters.reporter.Reporter`
        :param choice_conf: An instance of :class:`~.ChoiceConf` containing the configuration
                            for the choice.
        :type choice_conf: :class:`~.ChoiceConf`
        :raises SimpleBenchTypeError: If any argument is of an incorrect type.
        :raises SimpleBenchValueError: If any argument has an invalid value (e.g., empty strings
                                       or empty sequences).
        """
        deferred_reporter_import()

        # mypy raises a [type-abstract] error because Reporter is an Abstract Base Class
        # (ABC). We are using the Reporter ABC itself as a type argument in the
        # validate_type function, which mypy flags because ABCs cannot be instantiated.
        # We use type: ignore because we know at runtime we will only ever receive
        # concrete subclasses of Reporter, not the abstract Reporter itself.
        self._reporter: Reporter = validate_type(
            reporter, Reporter, "reporter",  # type: ignore[type-abstract]
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
        """The :class:`~simplebench.reporters.reporter.Reporter` sub-class associated with the choice."""
        return self._reporter

    @property
    def choice_conf(self) -> ChoiceConf:
        """The :class:`~.ChoiceConf` instance used to create the choice."""
        return self._choice_conf

    # All the properties below simply proxy to the underlying ChoiceConf instance
    @property
    def flags(self) -> frozenset[str]:
        """Flags associated with the choice. These are used for command-line selection.
        They must be unique across all choices for all reporters. This is enforced
        by the :class:`~simplebench.reporters.reporter_manager.ReporterManager` when choices
        are registered.

        The flags should be in the format used on the command line,
        typically starting with ``--`` for long options.

        .. code-block:: python

            ['--json', '--json-full']

        The :attr:`~.description` property of the :class:`~.Choice` is used to provide
        help text for the flags when generating command-line help.
        """
        return self._choice_conf.flags

    @property
    def flag_type(self) -> FlagType:
        """The type of command-line flag (e.g., :attr:`~simplebench.enums.FlagType.BOOLEAN`,
        :attr:`~simplebench.enums.FlagType.TARGET_LIST`, etc.)."""
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

        These are the sections that the associated
        :class:`~simplebench.reporters.reporter.Reporter` subclass
        is expected to include in its report when this choice is selected."""
        return self._choice_conf.sections

    @property
    def targets(self) -> frozenset[Target]:
        """Output targets for the choice.

        These are the output targets that the associated
        :class:`~simplebench.reporters.reporter.Reporter` subclass
        is expected to use when this choice is selected."""
        return self._choice_conf.targets

    @property
    def default_targets(self) -> frozenset[Target] | None:
        """Default output targets for the choice.

        These are the default output targets that the associated
        :class:`~simplebench.reporters.reporter.Reporter` subclass
        should use when this choice is selected, if no specific target
         is provided by the user."""
        return self._choice_conf.default_targets

    @property
    def subdir(self) -> str | None:
        """An optional subdirectory for output files.

        If specified, the associated :class:`~simplebench.reporters.reporter.Reporter` subclass
        should use this subdirectory for output files when this choice
        is selected. If an empty string, no subdirectory
        should be used. If ``None``, the reporter's default subdir
        should be used."""
        return self._choice_conf.subdir

    @property
    def file_suffix(self) -> str | None:
        """An optional file suffix for output files.

        If specified, the associated :class:`~simplebench.reporters.reporter.Reporter` subclass
        should use this file suffix for output files when this choice
        is selected. If ``None``, the reporter's default file_suffix
        should be used."""
        return self._choice_conf.file_suffix

    @property
    def file_unique(self) -> bool | None:
        """Whether to make output file names unique.

        If specified, the associated :class:`~simplebench.reporters.reporter.Reporter` subclass
        should use this setting for output files when this choice
        is selected. If ``None``, the reporter's default file_unique
        setting should be used."""
        return self._choice_conf.file_unique

    @property
    def file_append(self) -> bool | None:
        """Whether to append to existing output files.

        If specified, the associated :class:`~simplebench.reporters.reporter.Reporter` subclass
        should use this setting for output files when this choice
        is selected. If ``None``, the reporter's default file_append
        setting should be used."""
        return self._choice_conf.file_append

    @property
    def output_format(self) -> Format:
        """Output format for the choice.

        This is the output format that the associated
        :class:`~simplebench.reporters.reporter.Reporter` subclass
        is expected to use when this choice is selected.

        :return: The output format.
        :rtype: :class:`~simplebench.enums.Format`
        """
        return self._choice_conf.output_format

    @property
    def options(self) -> ReporterOptions | None:
        """An optional :class:`~simplebench.reporters.reporter.options.ReporterOptions`
        instance for additional configuration."""
        return self._choice_conf.options

    @property
    def extra(self) -> Any:
        """Any additional metadata associated with the choice."""
        return self._choice_conf.extra

    def __hash__(self) -> int:
        """Compute a hash value for the :class:`~.ChoiceConf` instance.

        :return: The computed hash value.
        :rtype: int
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
        """Check equality between two :class:`~.ChoiceConf` instances.

        :param other: The other :class:`~.ChoiceConf` instance to compare against.
        :type other: object
        :return: ``True`` if the :class:`~.ChoiceConf` instances are equal, ``False`` otherwise.
        :rtype: bool
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
