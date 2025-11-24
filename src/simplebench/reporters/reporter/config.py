"""Base reporter configuration class."""
from __future__ import annotations

from dataclasses import dataclass

from simplebench.enums import Format, Section, Target
from simplebench.exceptions import SimpleBenchValueError
from simplebench.reporters.choices.choices_conf import ChoicesConf
from simplebench.reporters.reporter.exceptions.config import _ReporterConfigErrorTag
from simplebench.validators import validate_dirpath, validate_iterable_of_type, validate_string, validate_type


@dataclass(frozen=True, kw_only=True)
class ReporterConfig:
    """Immutable, attribute-based base configuration for a Reporter.

    This frozen dataclass serves as the foundation for all specific reporter
    configuration classes (e.g., :class:`~simplebench.reporters.rich_table.config.RichTableConfig`).
    It defines the common data structure and centralizes the validation of all parameters required
    by reporters.

    The ``sections``, ``targets``, and ``formats`` parameters act as master lists,
    constraining the values that can be used within the ``choices`` and
    ``default_targets`` parameters.

    As a frozen dataclass, instances of this class are immutable; their state
    cannot be changed after creation. Validation and normalization of inputs
    are performed automatically in the ``__post_init__`` method.

    Attributes:
        name (str): The unique name for the reporter (e.g., 'rich-table').
        description (str): A short description of what the reporter does.
        sections (frozenset[Section]): The master set of sections this reporter can handle.
        targets (frozenset[Target]): The master set of targets this reporter can output to.
        default_targets (frozenset[Target]): The default subset of ``targets`` to use.
        formats (frozenset[Format]): The master set of formats this reporter can produce.
        choices (ChoicesConf): Defines the reporter's command-line interface flags.
        file_suffix (str): The file extension for filesystem targets, without the leading dot.
        file_unique (bool): If ``True``, generate a unique filename for each output.
        file_append (bool): If ``True``, append to the output file if it already exists.
        subdir (str): The subdirectory for saved files; ``''`` means the root results directory.
    """
    name: str
    """The unique name for the reporter (e.g., 'rich-table'). Cannot be empty or blank."""

    description: str
    """A short description of what the reporter does. Cannot be empty or blank."""

    sections: frozenset[Section]
    """The master set of :class:`~.Section` enums this reporter can handle. This constrains
    the sections that can be used by any :class:`~.ChoiceConf` in the ``choices`` list.
    """

    targets: frozenset[Target]
    """The master set of :class:`~.Target` enums this reporter can output to. This constrains
    the targets that can be used by ``default_targets`` and any :class:`~.ChoiceConf`
    in the ``choices`` list.
    """

    default_targets: frozenset[Target]
    """The default subset of ``targets`` to use if not specified. Must be a subset of the
    main ``targets`` set.
    """

    formats: frozenset[Format]
    """The master set of :class:`~.Format` enums this reporter can produce. This constrains
    the formats that can be used by any :class:`~.ChoiceConf` in the ``choices`` list.
    """

    choices: ChoicesConf
    """A :class:`~.ChoicesConf` object defining the reporter's command-line interface
    flags. These flags allow end-users to precisely control report generation by
    specifying which sections to include, what output format to use, and where to
    send the report (targets). They can also control other reporter-specific options.
    """

    file_suffix: str
    """The file extension to use for filesystem targets (e.g., 'txt'), without the leading dot.

    The suffix must consist only of alphanumeric characters and be 10 characters or less in length."""

    file_unique: bool
    """If ``True``, generate a unique filename for each output.
    Mutually exclusive with ``file_append``; exactly one must be ``True``.
    """

    file_append: bool
    """If ``True``, append to the output file if it already exists.
    Mutually exclusive with ``file_unique``; exactly one must be ``True``.
    """

    subdir: str
    """The subdirectory within the results directory to save files to. An empty string
    (``''``) specifies the root of the results directory (i.e., no subdirectory).

    A subdirectory path should only contain valid directory name elements separated by
    forward slashes (``'/'``). Each element must consist only of alphanumeric, underscore, or dash
    characters, cannot be longer than 64 characters and cannot start or end with a dash or underscore.

    Empty elements (i.e., consecutive slashes) are not allowed. Paths cannot start or end with a slash.

    The total length of the subdirectory path must not exceed 255 characters.
    """

    def __post_init__(self) -> None:
        """Validate and normalize the configuration after initialization."""
        # 1. Perform all validations on the raw, incoming attribute values
        validate_string(
            self.name, 'name',
            type_error_tag=_ReporterConfigErrorTag.INVALID_NAME_TYPE,
            value_error_tag=_ReporterConfigErrorTag.INVALID_NAME_VALUE,
            allow_empty=False, allow_blank=False
        )
        validate_string(
            self.description, 'description',
            type_error_tag=_ReporterConfigErrorTag.INVALID_DESCRIPTION_TYPE,
            value_error_tag=_ReporterConfigErrorTag.INVALID_DESCRIPTION_VALUE,
            allow_empty=False, allow_blank=False
        )
        validate_iterable_of_type(
            self.sections, Section, 'sections',
            type_tag=_ReporterConfigErrorTag.INVALID_SECTIONS_TYPE,
            value_tag=_ReporterConfigErrorTag.INVALID_SECTIONS_VALUE,
            allow_empty=True
        )
        validate_iterable_of_type(
            self.targets, Target, 'targets',
            type_tag=_ReporterConfigErrorTag.INVALID_TARGETS_TYPE,
            value_tag=_ReporterConfigErrorTag.INVALID_TARGETS_VALUE,
            allow_empty=False
        )

        validate_iterable_of_type(
            self.default_targets, Target, 'default_targets',
            type_tag=_ReporterConfigErrorTag.INVALID_DEFAULT_TARGETS_TYPE,
            value_tag=_ReporterConfigErrorTag.INVALID_DEFAULT_TARGETS_VALUE
        )
        validate_iterable_of_type(
            self.formats, Format, 'formats',
            type_tag=_ReporterConfigErrorTag.INVALID_FORMATS_TYPE,
            value_tag=_ReporterConfigErrorTag.INVALID_FORMATS_VALUE,
            allow_empty=False
        )
        validate_type(
            self.choices, ChoicesConf, 'choices',
            error_tag=_ReporterConfigErrorTag.INVALID_CHOICES_TYPE
        )
        validate_string(
            self.file_suffix, 'file_suffix',
            type_error_tag=_ReporterConfigErrorTag.INVALID_FILE_SUFFIX_TYPE,
            value_error_tag=_ReporterConfigErrorTag.INVALID_FILE_SUFFIX_VALUE,
            allow_empty=False, allow_blank=False, alphanumeric_only=True
        )
        if len(self.file_suffix) > 10:
            raise SimpleBenchValueError(
                "file_suffix must be 10 characters or less in length.",
                tag=_ReporterConfigErrorTag.INVALID_FILE_SUFFIX_VALUE_TOO_LONG
            )
        validate_type(
            self.file_unique, bool, 'file_unique',
            error_tag=_ReporterConfigErrorTag.INVALID_FILE_UNIQUE_TYPE
        )
        validate_type(
            self.file_append, bool, 'file_append',
            error_tag=_ReporterConfigErrorTag.INVALID_FILE_APPEND_TYPE
        )
        subdir = validate_dirpath(self.subdir, allow_empty=True)

        # Check for (False, False) case first for clarity
        if not self.file_append and not self.file_unique:
            raise SimpleBenchValueError(
                "One of file_append or file_unique must be True.",
                tag=_ReporterConfigErrorTag.INVALID_FILE_APPEND_FILE_UNIQUE_ONE_MUST_BE_TRUE
            )
        # If the first check passes, this check now correctly isolates the (True, True) case
        if self.file_append and self.file_unique:
            raise SimpleBenchValueError(
                "file_append and file_unique cannot both be True.",
                tag=_ReporterConfigErrorTag.INVALID_FILE_APPEND_FILE_UNIQUE_COMBINATION
            )

        # After validation, convert iterables to frozenset for immutability
        # and replace subdir with the validated version
        # This uses object.__setattr__ to bypass the frozen=True restriction.
        object.__setattr__(self, 'subdir', subdir)
        object.__setattr__(self, 'sections', frozenset(self.sections))
        object.__setattr__(self, 'targets', frozenset(self.targets))
        object.__setattr__(self, 'default_targets', frozenset(self.default_targets))
        object.__setattr__(self, 'formats', frozenset(self.formats))

        # 3. Perform final cross-field validations on the normalized values
        if not self.default_targets.issubset(self.targets):
            raise SimpleBenchValueError(
                "default_targets must be a subset of targets",
                tag=_ReporterConfigErrorTag.INVALID_DEFAULT_TARGETS_VALUE
            )
