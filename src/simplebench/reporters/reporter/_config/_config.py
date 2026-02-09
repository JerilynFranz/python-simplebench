"""Base reporter configuration class."""
from collections.abc import Hashable

from simplebench.enums import Format, Target
from simplebench.metrics import MetricsSelection
from simplebench.reporters.choices import ChoicesConf
from simplebench.simplebench_types import ElementCollection, Immutable

from . import _validate


class ReporterConfig(Immutable, Hashable):
    """Immutable, attribute-based base configuration for a Reporter.

    This immutable class serves as the foundation for all specific reporter
    configuration classes (e.g., :class:`~simplebench.reporters.rich_table.config.RichTableConfig`).
    It defines the common data structure and centralizes the validation of all parameters required
    by reporters.

    The ``metrics``, ``targets``, and ``formats`` parameters act as master lists,
    constraining the values that can be used within the ``choices`` and
    ``default_targets`` parameters.

    Instances of this class are immutable; their state
    cannot be changed after creation. Validation and normalization of inputs
    are performed automatically in the constructor using helper functions from
    the ``_validate`` module.

    Attributes:
        name (str): The unique name for the reporter (e.g., 'rich-table'). Cannot be empty or blank.
        description (str): A short description of what the reporter does. Cannot be empty or blank.
        metrics (MetricsSelection): The master set of :class:`~.Metric` enums this reporter
            can handle. This constrains the metrics that can be used by any :class:`~.ChoiceConf`
            in the ``choices`` list.
        targets (frozenset[Target]): The master set of :class:`~.Target` enums this reporter can output
            to. This constrains the targets that can be used by ``default_targets``
            and any :class:`~.ChoiceConf` in the ``choices`` list.
        default_targets (frozenset[Target]): The default subset of ``targets`` to use if not specified.
            Must be a subset of the main ``targets`` set.
        formats (frozenset[Format]): The master set of :class:`~.Format` enums this reporter can
            produce. This constrains the formats that can be used by any :class:`~.ChoiceConf`
            in the ``choices`` list.
        choices (ChoicesConf): A :class:`~.ChoicesConf` object defining the reporter's command-line interface
            flags. These flags allow end-users to precisely control report generation by
            specifying which metrics to include, what output format to use, and where to
            send the report (targets). They can also control other reporter-specific options.
        file_suffix (str): The file extension to use for filesystem targets (e.g., 'txt'), without
            the leading dot.

            The suffix must consist only of alphanumeric characters and be 10 characters or less in length.
        file_unique (bool): If ``True``, generate a unique filename for each output.
            Mutually exclusive with ``file_append``; exactly one must be ``True``.
        file_append (bool): If ``True``, append to the output file if it already exists.
            Mutually exclusive with ``file_unique``; exactly one must be ``True``.
        subdir (str): The subdirectory within the results directory to save files to. An empty string
            (``''``) specifies the root of the results directory (i.e., no subdirectory).
            The subdirectory name must meet the following criteria:

            - The directory name is a string.
            - The directory name is either empty or made of alphanumeric characters,
                underscores, or dashes, and is at least one character long.
            - The directory name does not start or end with an underscore or dash.
            - The total directory name length does not exceed 255 characters.
    """
    def __init__(self,
                 *,
                 name: str,
                 description: str,
                 metrics: MetricsSelection,
                 targets: ElementCollection[Target],
                 default_targets: ElementCollection[Target],
                 subdir: str,
                 file_suffix: str,
                 file_unique: bool,
                 file_append: bool,
                 formats: ElementCollection[Format],
                 choices: ChoicesConf) -> None:
        """Constructs an immutable ReporterConfig instance.

        :param name: The unique name for the reporter (e.g., 'rich-table'). Cannot be empty or blank.
        :type name: str
        :param description: A short description of what the reporter does. Cannot be empty or blank.
        :type description: str
        :param metrics: The master set of :class:`~.Metric` enums this reporter
            can handle. This constrains the metrics that can be used by any :class:`~.ChoiceConf`
            in the ``choices`` list.
        :type metrics: MetricsSelection
        :param targets: The master set of :class:`~.Target` enums this reporter can output
            to. This constrains the targets that can be used by ``default_targets``
            and any :class:`~.ChoiceConf` in the ``choices`` list.
        :type targets: ElementCollection[Target]
        :param default_targets: The default subset of ``targets`` to use if not specified. Must be a subset of the
            main ``targets`` set.
        :type default_targets: ElementCollection[Target]
        :param subdir: The subdirectory within the results directory to save files to. An empty string
            (``''``) specifies the root of the results directory (i.e., no subdirectory).
        :type subdir: str
        :param file_suffix: The file extension to use for filesystem targets (e.g., 'txt'), without
            the leading dot.
        :type file_suffix: str
        :param file_unique: If ``True``, generate a unique filename for each output.
            Mutually exclusive with ``file_append``; exactly one must be ``True``.
        :type file_unique: bool
        :param file_append: If ``True``, append to the output file if it already exists.
            Mutually exclusive with ``file_unique``; exactly one must be ``True``.
        :type file_append: bool
        :param formats: The master set of :class:`~.Format` enums this reporter can
            produce. This constrains the formats that can be used by any :class:`~.ChoiceConf`
            in the ``choices`` list.
        :type formats: ElementCollection[Format]
        :param choices: A :class:`~.ChoicesConf` object defining the reporter's command-line interface
            flags. These flags allow end-users to precisely control report generation by
            specifying which metrics to include, what output format to use, and where to
            send the report (targets). They can also control other reporter-specific options.
        :type choices: ChoicesConf
        :raises SimpleBenchTypeError: If any parameter is of an incorrect type.
        :raises SimpleBenchValueError: If any parameter has an invalid value.
        """
        self._name = _validate.name(name)
        self._description = _validate.description(description)
        self._metrics = _validate.metrics(metrics)
        self._targets = _validate.targets(targets)
        self._default_targets = _validate.default_targets(default_targets)
        _validate.default_targets_are_subset_of_targets( self.default_targets, self.targets)
        self._subdir = _validate.subdir(subdir)
        self._file_suffix = _validate.file_suffix(file_suffix)
        self._file_unique = _validate.file_unique(file_unique)
        self._file_append = _validate.file_append(file_append)
        _validate.validate_file_append_file_unique_combination(self.file_append, self.file_unique)
        self._formats = _validate.formats(formats)
        self._choices = _validate.choices(choices)

    @property
    def name(self) -> str:
        """The unique name for the reporter (e.g., 'rich-table')."""
        return self._name

    @property
    def description(self) -> str:
        """A short description of what the reporter does."""
        return self._description

    @property
    def metrics(self) -> MetricsSelection:
        """The master set of metrics this reporter can handle."""
        return self._metrics

    @property
    def targets(self) -> frozenset[Target]:
        """The master set of targets this reporter can output to."""
        return self._targets

    @property
    def default_targets(self) -> frozenset[Target]:
        """The default subset of ``targets`` to use."""
        return self._default_targets

    @property
    def formats(self) -> frozenset[Format]:
        """The master set of formats this reporter can produce."""
        return self._formats

    @property
    def choices(self) -> ChoicesConf:
        """Defines the reporter's command-line interface flags."""
        return self._choices

    @property
    def file_suffix(self) -> str:
        """The file extension for filesystem targets, without the leading dot."""
        return self._file_suffix

    @property
    def file_unique(self) -> bool:
        """If ``True``, generate a unique filename for each output."""
        return self._file_unique

    @property
    def file_append(self) -> bool:
        """If ``True``, append to the output file if it already exists."""
        return self._file_append

    @property
    def subdir(self) -> str:
        """The subdirectory for saved files; ``''`` means the root results directory."""
        return self._subdir


    def __hash__(self) -> int:
        """Computes the hash of the ReporterConfig instance.

        :return: The hash value.
        :rtype: int
        """
        return hash((
            self._name,
            self._description,
            self._metrics,
            self._targets,
            self._default_targets,
            self._subdir,
            self._file_suffix,
            self._file_unique,
            self._file_append,
            self._formats,
            self._choices
        ))

    def __eq__(self, other: object) -> bool:
        """Checks equality between this ReporterConfig and another object.

        :param other: The other object to compare against.
        :type other: object
        :return: ``True`` if equal, ``False`` otherwise.
        :rtype: bool
        """
        if not isinstance(other, ReporterConfig):
            return False

        return (
            self._name == other._name and
            self._description == other._description and
            self._metrics == other._metrics and
            self._targets == other._targets and
            self._default_targets == other._default_targets and
            self._subdir == other._subdir and
            self._file_suffix == other._file_suffix and
            self._file_unique == other._file_unique and
            self._file_append == other._file_append and
            self._formats == other._formats and
            self._choices == other._choices
        )

    def __repr__(self) -> str:
        """Returns a string representation of the ReporterConfig instance.

        :return: The string representation.
        :rtype: str
        """
        return (
            f"ReporterConfig(name={self._name!r}, "
            f"description={self._description!r}, "
            f"metrics={self._metrics!r}, "
            f"targets={self._targets!r}, "
            f"default_targets={self._default_targets!r}, "
            f"subdir={self._subdir!r}, "
            f"file_suffix={self._file_suffix!r}, "
            f"file_unique={self._file_unique!r}, "
            f"file_append={self._file_append!r}, "
            f"formats={self._formats!r}, "
            f"choices={self._choices!r})"
        )
