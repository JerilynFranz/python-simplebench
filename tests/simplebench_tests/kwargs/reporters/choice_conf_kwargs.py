"""simplebench.reporters.choice.Choice KWArgs package for SimpleBench tests."""

from collections.abc import Sequence

from simplebench.enums import FlagType, Format, Target
from simplebench.metrics._metrics_selection import MetricsSelection
from simplebench.options.reporter.options import ReporterOptions
from simplebench.reporters.choice.choice_conf import ChoiceConf
from simplebench.simplebench_types import ElementCollection, Extras

from ..kwargs import NO_DEFAULT_VALUE, KWArgs, NoDefaultValue


class ChoiceConfKWArgs(KWArgs):
    """A class to hold keyword arguments for initializing a Choice instance.

    This class is primarily used to facilitate testing of the Choice class initialization
    with various combinations of parameters, including those that are optional and those
    that have no default value.

    It provides a convenient way to construct a dictionary of parameters to be passed
    to the Choice class during initialization with linting tools guiding the types of each
    parameter without constraining the presence of or strictly enforcing the types of any parameter.
    """
    def __init__(  # pylint: disable=unused-argument
            self, *,
            flags: Sequence[str] | NoDefaultValue = NO_DEFAULT_VALUE,
            flag_type: FlagType | NoDefaultValue = NO_DEFAULT_VALUE,
            name: str | NoDefaultValue = NO_DEFAULT_VALUE,
            description: str | NoDefaultValue = NO_DEFAULT_VALUE,
            metrics: MetricsSelection | NoDefaultValue = NO_DEFAULT_VALUE,
            output_format: Format | NoDefaultValue = NO_DEFAULT_VALUE,
            targets: ElementCollection[Target] | NoDefaultValue = NO_DEFAULT_VALUE,
            default_targets: ElementCollection[Target] | NoDefaultValue = NO_DEFAULT_VALUE,
            subdir: str | NoDefaultValue = NO_DEFAULT_VALUE,
            file_suffix: str | NoDefaultValue = NO_DEFAULT_VALUE,
            file_unique: bool | NoDefaultValue = NO_DEFAULT_VALUE,
            file_append: bool | NoDefaultValue = NO_DEFAULT_VALUE,
            options: ReporterOptions | NoDefaultValue = NO_DEFAULT_VALUE,
            extra: Extras | NoDefaultValue = NO_DEFAULT_VALUE) -> None:
        """Constructs a ChoiceConfKWArgs instance. This class is used to hold keyword arguments for
        initializing a ChoiceConf instance in tests.

        :param flags: An iterable of command-line flags associated with the choice.
        :type flags: Iterable[str]
        :param flag_type: The type of command-line flag (e.g., boolean, target_list, etc.).
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
        :type extra: Any

        """
        super().__init__(call=ChoiceConf.__init__, kwargs=locals())
