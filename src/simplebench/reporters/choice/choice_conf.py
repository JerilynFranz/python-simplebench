"""``ChoiceConf()`` for reporters."""
from collections.abc import Hashable
from typing import Any, Iterable, Sequence

from typechecked import Immutable

from simplebench.enums import FlagType, Format, Target
from simplebench.exceptions import SimpleBenchTypeError
from simplebench.metrics.metrics_selection import MetricsSelection
from simplebench.reporters.choice._error_tags import _ChoiceConfErrorTag
from simplebench.reporters.protocols import ChoiceProtocol
from simplebench.reporters.reporter.options import ReporterOptions

from . import _validate


class ChoiceConf(Hashable, ChoiceProtocol, Immutable):
    """Definition of a :class:`~.Choice` configuration for reporters.

    A :class:`~.ChoiceConf` represents a specific configuration of an implied :class:`~.Choice`
    that can be registered with a :class:`~simplebench.reporters.reporter.Reporter` subclass.
    It defines the metrics to include in the report, the output targets, the output format,
    and various other options related to reporting.

    The :class:`~.ChoiceConf` class provides a structured way to define different
    reporting options within the SimpleBench framework so that
    users can select from predefined configurations and developers can
    easily add new reporting options to the framework.

    A :class:`~.ChoiceConf` instance is immutable after creation to ensure consistency
    in reporting configurations.

    The metrics, targets, and formats are descriptive only; they do not
    enforce any behavior on the associated :class:`~simplebench.reporters.reporter.Reporter`
    subclass. It is the responsibility of the :class:`~simplebench.reporters.reporter.Reporter`
    subclass to implement the behavior corresponding to the specified metrics, targets,
    and formats.

    The :class:`~.ChoiceConf` is intended to be used in defining configurations for
    reporters without depending on being embedded in the
    :meth:`~simplebench.reporters.reporter.Reporter.__init__`
    method for definition. This allows for more flexible and reusable
    reporter configurations. The live counterpart to :class:`~.ChoiceConf` is the
    :class:`~.Choice` class, which is used at runtime with actual :class:`~.Choice` instances
    created by :class:`~simplebench.reporters.reporter.Reporter` from
    :class:`~.ChoiceConf` definitions.

    :param flags: A set of command-line flags associated with the choice.
    :type flags: set[str]
    :param flag_type: The type of command-line flag (e.g., boolean, target_list, etc.).
    :type flag_type: :class:`~simplebench.enums.FlagType`
    :param name: A unique name for the choice.
    :type name: str
    :param description: A brief description of the choice.
    :type description: str
    :param metrics: A :class:`~simplebench.metric.MetricsSelection`.
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
    :param options: An optional
                    :class:`~simplebench.reporters.reporter.options.ReporterOptions`
                    instance for additional configurations specific to a specific reporter.
                    If ``None``, reports default to the reporter's default options.
    :type options: :class:`~simplebench.reporters.reporter.options.ReporterOptions` | None
    :param extra: Any additional metadata associated with the choice.
    :type extra: Any | None
    """
    __slots__ = (
        '_flags',
        '_flag_type',
        '_name',
        '_description',
        '_metrics',
        '_targets',
        '_default_targets',
        '_subdir',
        '_file_suffix',
        '_file_unique',
        '_file_append',
        '_output_format',
        '_options',
        '_extra',
        '_hash_id',
    )


    def __init__(
        self,
        *,
        flags: Sequence[str],
        flag_type: FlagType,
        name: str,
        description: str,
        metrics: MetricsSelection,
        output_format: Format,
        targets: Iterable[Target],
        default_targets: Iterable[Target] | None = None,
        subdir: str | None = None,
        file_suffix: str | None = None,
        file_unique: bool | None = None,
        file_append: bool | None = None,
        options: ReporterOptions | None = None,
        extra: Hashable | None = None,
    ) -> None:
        """Construct a :class:`~.ChoiceConf` instance.

        :param flags: Iterable of flags associated with the choice.

            These are used for command-line selection.
            They must be unique across all choices for all reporters. This is enforced
            by the ReporterManager when choices are registered.

            The flags should be in the format used on the command line,
            typically starting with '--' for long options.

            Example: ['--json', '--json-full']

            The description property of the Choice is used to provide
            help text for the flags when generating command-line help.
        :type flags: Iterable[str]
        :param flag_type: The type of command-line flag (e.g., The type of command-line
            flag (e.g., :data:`~simplebench.enums.FlagType.BOOLEAN`,
            :data:`~simplebench.enums.FlagType.TARGET_LIST`, etc.).
        :type flag_type: :class:`~simplebench.enums.FlagType`
        :param name: A unique name for the choice.
        :type name: str
        :param description: A brief description of the choice.
        :type description: str
        :param metrics: An iterable of :class:`~simplebench.metric.Metric` enums to include
                         in the report. It must be non-empty, but
                         :attr:`~simplebench.metric.Metric.NULL` may be included to indicate
                         no metrics are specifically selected. The reporter is expected to
                         include listed metrics in its report.
        :type metrics: Iterable[:class:`~simplebench.metric.Metric`]
        :param output_format: A :class:`~simplebench.enums.Format` instance describing the
                              output format.
        :type output_format: :class:`~simplebench.enums.Format`
        :param targets: An iterable of :class:`~simplebench.enums.Target` enums for output.
                        It must be non-empty. If multiple targets are specified, the reporter
                        is expected to handle outputting to all specified targets when this
                        choice is selected.
        :type targets: Iterable[:class:`~simplebench.enums.Target`]
        :param default_targets: An optional iterable of default
                                :class:`~simplebench.enums.Target` enums.
                                The enums represent the default targets for the choice.
                                If ``None``, no default targets are specified and the
                                reporter's defaults will be used when generating reports.
        :type default_targets: Iterable[:class:`~simplebench.enums.Target`] | None
        :param subdir: An optional subdirectory for output files. If ``None``, defaults to the
                       reporter's default subdir. It may only consist of alphanumeric
                       characters (a-z, A-Z, 0-9) or be an empty string (to indicate no
                       subdirectory). It cannot be longer than 64 characters and may be left
                       as ``None`` to use the reporter's default.
        :type subdir: str | None
        :param file_suffix: An optional file suffix for output files. If ``None``, defaults to
                            the reporter's default file_suffix when generating reports.
                            It may only consist of alphanumeric characters (a-z, A-Z, 0-9),
                            and be no longer than 10 characters. It may be left as ``None``
                            to use the reporter's default.
        :type file_suffix: str | None
        :param file_unique: Whether to make output file names unique by appending a unique
                            identifier. Mutually exclusive with `file_append`; both cannot be
                            ``True`` or ``False`` at the same time. If ``None``, defaults to
                            the reporter's default file_unique setting.
        :type file_unique: bool | None
        :param file_append: Whether to append to existing output files instead of overwriting
                            them. Mutually exclusive with `file_unique`; both cannot be
                            ``True`` or ``False`` at the same time. If ``None``, defaults to
                            the reporter's default file_append setting.
        :type file_append: bool | None
        :param options: An optional
                        :class:`~simplebench.reporters.reporter.options.ReporterOptions`
                        instance for additional configuration specific to a reporter.
                        The option must be of the same type as that specified by the
                        ``options_type`` property of the associated
                        :class:`~simplebench.reporters.reporter.Reporter` subclass.
        :type options: :class:`~simplebench.reporters.reporter.options.ReporterOptions` | None
        :param extra: Any additional metadata associated with the choice. This can be used to
                      store custom information relevant to the choice and the core
                      benchmarking framework does not interpret or enforce any structure on
                      this data. :class:`~simplebench.reporters.reporter.Reporter` subclasses
                      may choose to utilize this field for their own purposes.

                      The value must be hashable and immutable to support the immutability
                      of the :class:`~.ChoiceConf` instance.
        :type extra: Hashable | None
        :raises SimpleBenchTypeError: If any argument is of an incorrect type.
        :raises SimpleBenchValueError: If any argument has an invalid value (e.g., empty
                                       strings or empty sequences).
        """
        self._flags: frozenset[str] = _validate.flags(flags)
        self._flag_type = _validate.flag_type(flag_type)
        self._name: str = _validate.name(name)
        self._description: str = _validate.description(description)
        self._metrics: MetricsSelection = _validate.metrics(metrics)
        self._targets: frozenset[Target] = _validate.targets(targets)
        self._default_targets: frozenset[Target] = _validate.default_targets(default_targets)
        self._subdir: str | None = _validate.subdir(subdir)
        self._file_suffix: str | None = _validate.file_suffix(file_suffix)
        self._file_unique: bool | None = _validate.file_unique(file_unique)
        self._file_append: bool | None = _validate.file_append(file_append)

        # Ensure that if one is None and the other is not, we set the None one
        # to the opposite of the other to maintain mutual exclusivity
        # and to prevent prioritization logic from having to handle the case
        # where only one is None.
        if self._file_unique is None and self._file_append is not None:
            self._file_unique = not self._file_append
        elif self._file_append is None and self._file_unique is not None:
            self._file_append = not self._file_unique
        if self._file_unique is not None and self._file_append is not None and self._file_unique == self._file_append:
            raise SimpleBenchTypeError(
                'file_unique and file_append are mutually exclusive; both cannot be True or False at the same time',
                tag=_ChoiceConfErrorTag.FILE_UNIQUE_FILE_APPEND_MUTUALLY_EXCLUSIVE,
            )

        self._output_format: Format = _validate.output_format(output_format)
        self._options: ReporterOptions | None = _validate.options(options)
        self._extra: Hashable | None = _validate.extra(extra)

        hash_fields = (slot_key for slot_key in self.__slots__ if slot_key != '_hash_id')
        hash_values = tuple(hash(getattr(self, key)) for key in hash_fields)
        self._hash_id: int = hash(hash_values)

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
        return self._flags

    @property
    def flag_type(self) -> FlagType:
        """The type of command-line flag (e.g., :attr:`~simplebench.enums.FlagType.BOOLEAN`,
        :attr:`~simplebench.enums.FlagType.TARGET_LIST`, etc.)."""
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
    def metrics(self) -> MetricsSelection:
        """Metrics included in the choice.

        These are the metrics that the associated
        :class:`~simplebench.reporters.reporter.Reporter` subclass
        is expected to include in its report when this choice is selected."""
        return self._metrics

    @property
    def targets(self) -> frozenset[Target]:
        """Output targets for the choice.

        These are the output targets that the associated
        :class:`~simplebench.reporters.reporter.Reporter` subclass
        is expected to use when this choice is selected."""
        return self._targets

    @property
    def default_targets(self) -> frozenset[Target] | None:
        """Default output targets for the choice.

        These are the default output targets that the associated
        :class:`~simplebench.reporters.reporter.Reporter` subclass
        should use when this choice is selected, if no specific target
         is provided by the user."""
        return self._default_targets

    @property
    def subdir(self) -> str | None:
        """An optional subdirectory for output files.

        If specified, the associated :class:`~simplebench.reporters.reporter.Reporter` subclass
        should use this subdirectory for output files when this choice
        is selected. If an empty string, no subdirectory
        should be used. If ``None``, the reporter's default subdir
        should be used."""
        return self._subdir

    @property
    def file_suffix(self) -> str | None:
        """An optional file suffix for output files.

        If specified, the associated :class:`~simplebench.reporters.reporter.Reporter` subclass
        should use this file suffix for output files when this choice
        is selected. If ``None``, the reporter's default file_suffix
        should be used."""
        return self._file_suffix

    @property
    def file_unique(self) -> bool | None:
        """Whether to make output file names unique.

        If specified, the associated :class:`~simplebench.reporters.reporter.Reporter` subclass
        should use this setting for output files when this choice
        is selected. If ``None``, the reporter's default file_unique
        setting should be used."""
        return self._file_unique

    @property
    def file_append(self) -> bool | None:
        """Whether to append to existing output files.

        If specified, the associated :class:`~simplebench.reporters.reporter.Reporter` subclass
        should use this setting for output files when this choice
        is selected. If ``None``, the reporter's default file_append
        setting should be used."""
        return self._file_append

    @property
    def output_format(self) -> Format:
        """Output format for the choice.

        This is the output format that the associated
        :class:`~simplebench.reporters.reporter.Reporter` subclass
        is expected to use when this choice is selected.

        :return: The output format.
        :rtype: :class:`~simplebench.enums.Format`
        """
        return self._output_format

    @property
    def options(self) -> ReporterOptions | None:
        """An optional :class:`~simplebench.reporters.reporter.options.ReporterOptions`
        instance for additional configuration."""
        return self._options

    @property
    def extra(self) -> Any:
        """Any additional metadata associated with the choice."""
        return self._extra

    def __hash__(self) -> int:
        """The hash value for the :class:`~.ChoiceConf` instance.

        :return: The hash value.
        :rtype: int
        """
        return self._hash_id

    def __eq__(self, other: object) -> bool:
        """Check equality between two :class:`~.ChoiceConf` instances.

        :param other: The other :class:`~.ChoiceConf` instance to compare against.
        :type other: object
        :return: ``True`` if the :class:`~.ChoiceConf` instances are equal, ``False`` otherwise.
        :rtype: bool
        """
        if not isinstance(other, ChoiceConf):
            return False

        return self.__hash__() == other.__hash__()

    def __repr__(self) -> str:
        """String representation of the :class:`~.ChoiceConf` instance.

        :return: The string representation.
        :rtype: str
        """
        return (
            f"ChoiceConf(name={self._name!r}, flags={sorted(self._flags)!r}, "
            f"flag_type={self._flag_type!r}, description={self._description!r}, "
            f"metrics={self._metrics!r}, targets={sorted(self._targets)!r}, "
            f"default_targets={sorted(self._default_targets)!r}, "
            f"output_format={self._output_format!r}, subdir={self._subdir!r}, "
            f"file_suffix={self._file_suffix!r}, file_unique={self._file_unique!r}, "
            f"file_append={self._file_append!r}, options={self._options!r}, "
            f"extra={self._extra!r})"
        )
