"""Reporter base class.

This module defines the Reporter abstract base class, which serves as the foundation
for all reporter implementations in the SimpleBench benchmarking framework.

It handles common functionality such as validating input arguments, configuring argparse CLI arguments,
managing default options, sending reports to various targets, and orchestrating report generation.

To create a new reporter, a developer must subclass `Reporter` and implement the abstract
`render()` method. For most reporters, the default `run_report()` implementation, which
renders a report for each section, is sufficient.

A `Reporter` is responsible for generating reports based on benchmark results from a `Session` and `Case`.
Reporters can produce reports in various formats and output them to different targets.
"""
from __future__ import annotations

from abc import ABC, abstractmethod
from argparse import Namespace
from pathlib import Path
from typing import TYPE_CHECKING, Any, Iterable, Optional, TypeAlias, TypeVar

from rich.table import Table
from rich.text import Text

from simplebench.defaults import BASE_INTERVAL_UNIT, BASE_MEMORY_UNIT, BASE_OPS_PER_INTERVAL_UNIT
from simplebench.enums import Format, Section, Target
from simplebench.exceptions import SimpleBenchNotImplementedError, SimpleBenchTypeError, SimpleBenchValueError
# simplebench.reporters
from simplebench.reporters.choices.choices import Choices
from simplebench.reporters.choices.choices_conf import ChoicesConf
from simplebench.reporters.protocols import ReporterCallback
# simplebench.reporters.reporter
from simplebench.reporters.reporter.exceptions import ReporterErrorTag
from simplebench.reporters.reporter.metaclasses import IReporter
from simplebench.reporters.reporter.mixins import (
    _ReporterArgparseMixin,
    _ReporterOrchestrationMixin,
    _ReporterPrioritizationMixin,
    _ReporterTargetMixin,
)
from simplebench.reporters.reporter.options import ReporterOptions
from simplebench.reporters.reporter.protocols import ReporterProtocol
from simplebench.results import Results
from simplebench.type_proxies import is_case, is_choice, is_session
from simplebench.validators import validate_bool, validate_iterable_of_type, validate_string, validate_type

Options: TypeAlias = ReporterOptions

T = TypeVar('T')

if TYPE_CHECKING:
    from simplebench.case import Case
    from simplebench.reporters.choice.choice import Choice
    from simplebench.session import Session


def deferred_core_imports() -> None:
    """Deferred import of core types to avoid circular imports during initialization.

    This imports `Choice` when needed at runtime, preventing circular import issues
    during module load time while still allowing its use in creating Choice()
    instances from ChoiceConf() instances

    Args:
        None

    Returns:
        None
    """
    global Choice  # pylint: disable=global-statement
    from simplebench.reporters.choice.choice import Choice  # pylint: disable=import-outside-toplevel


class Reporter(ABC, IReporter, _ReporterArgparseMixin, _ReporterOrchestrationMixin,
               _ReporterPrioritizationMixin, _ReporterTargetMixin, ReporterProtocol):
    """Base class for Reporter classes.

    A Reporter is responsible for generating reports based on benchmark results
    from a Session and Case. Reporters can produce reports in various formats and
    output them to different targets.

    All Reporter subclasses must implement the methods defined in this interface.
    Reporters should handle their own output, whether to console, file system,
    HTTP endpoint, display device, via a callback or other output.

    The Reporter interface ensures that all reporters provide a consistent
    set of functionalities, making it easier to manage and utilize different
    reporting options within the SimpleBench framework.
    """
    @classmethod
    def _validate_subclass_config(cls) -> None:
        """Validate that the subclass has implemented required class variables.

        This method checks that the subclass has defined the required class variables
        and that they are of the correct types.

        Subclasses m ust implement the following class variables:

            _OPTIONS_TYPE: ClassVar[type[MyOptions]] = MyOptions
            _OPTIONS_KWARGS: ClassVar[dict[str, Any]] = {...}

        _OPTIONS_TYPE must be a subclass of ReporterOptions
        and _OPTIONS_KWARGS must be a dict[str, Any] that can be used
        to instantiate the _OPTIONS_TYPE subclass.


        Raises:
            SimpleBenchNotImplementedError: If required class variables are not implemented
                or are of incorrect types.
        """
        # Verify that we are being called from a subclass of Reporter, not Reporter itself
        if cls is Reporter:
            raise SimpleBenchNotImplementedError(
                ("get_hardcoded_default_options() cannot be called directly on the Reporter class"),
                tag=ReporterErrorTag.VALIDATE_SUBCLASS_CONFIG_CANNOT_BE_REPORTER)
        if not issubclass(cls, Reporter):
            raise SimpleBenchNotImplementedError(
                ("Only sub-classes of Reporter can call get_hardcoded_default_options()"),
                tag=ReporterErrorTag.VALIDATE_SUBCLASS_CONFIG_MUST_BE_SUBCLASS_OF_REPORTER)

        # Verify that the subclass has implemented the _OPTIONS_TYPE class variable correctly
        # It must be implemented in the subclass, and it must be a subclass of ReporterOptions,
        # but not ReporterOptions itself
        if "_OPTIONS_TYPE" not in cls.__dict__:
            raise SimpleBenchNotImplementedError(
                ("Reporter subclasses must implement the class variable '_OPTIONS_TYPE' "
                 "and set it to the specific ReporterOptions subclass they use"),
                tag=ReporterErrorTag.VALIDATE_SUBCLASS_CONFIG_OPTIONS_TYPE_NOT_IMPLEMENTED)
        options = cls._OPTIONS_TYPE  # pylint: disable=no-member   # type: ignore[reportAttributeAccessIssue]
        if options is ReporterOptions:
            raise SimpleBenchNotImplementedError(
                ("Reporter subclasses must set '_OPTIONS_TYPE' to a ReporterOptions subclass, "
                 "not the base ReporterOptions class"),
                tag=ReporterErrorTag.VALIDATE_SUBCLASS_CONFIG_OPTIONS_TYPE_INVALID_TYPE)
        if not issubclass(options, ReporterOptions):
            raise SimpleBenchNotImplementedError(
                ("Reporter subclasses must implement the class variable '_OPTIONS_TYPE' "
                 "and set it to a ReporterOptions subclass."),
                tag=ReporterErrorTag.VALIDATE_SUBCLASS_CONFIG_OPTIONS_TYPE_MUST_BE_SUBCLASS)

        # Verify the subclass has implemented the _OPTIONS_KWARGS class variable correctly
        # It must be implemented in the subclass, and it must be a dict[str, Any]
        if "_OPTIONS_KWARGS" not in cls.__dict__:
            raise SimpleBenchNotImplementedError(
                ("Reporter subclasses must implement the class variable '_OPTIONS_KWARGS' "
                 "and set it to a dict of keyword arguments for the ReporterOptions subclass."),
                tag=ReporterErrorTag.VALIDATE_SUBCLASS_CONFIG_OPTIONS_KWARGS_NOT_IMPLEMENTED)
        options_kwargs = cls._OPTIONS_KWARGS  # pylint: disable=no-member   # type: ignore[reportAttributeAccessIssue]
        if not isinstance(options_kwargs, dict):
            raise SimpleBenchNotImplementedError(
                ("Reporter subclasses must implement the class variable '_OPTIONS_KWARGS' "
                 "and set it to a dict of keyword arguments for the ReporterOptions subclass."),
                tag=ReporterErrorTag.VALIDATE_SUBCLASS_CONFIG_OPTIONS_KWARGS_NOT_A_DICT)
        if not all(isinstance(k, str) for k in options_kwargs.keys()):
            raise SimpleBenchNotImplementedError(
                ("Reporter subclasses must implement the class variable '_OPTIONS_KWARGS' "
                 "as a dict with string keys."),
                tag=ReporterErrorTag.VALIDATE_SUBCLASS_CONFIG_OPTIONS_KWARGS_KEYS_MUST_BE_STR)

    @classmethod
    def get_hardcoded_default_options(cls) -> Any:
        """Get the built-in hardcoded default options for the reporter.

        This abstract method must be implemented by all Reporter subclasses.
        It defines the base class default options for a reporter and must
        be available in all Reporter subclasses.

        It returns the hardcoded default ReporterOptions sub-class instance
        specific to the reporter.

        Sub-classes must implement the following class variables:

            _OPTIONS_TYPE: ClassVar[type[MyOptions]] = MyOptions
            _OPTIONS_KWARGS: ClassVar[dict[str, Any]] = {...}

        or the method will raise an exception.

        Returns:
            (ReporterOptions-subclass): The built-in hardcoded default
            ReporterOptions instance.

        Raises:
            SimpleBenchNotImplementedError: If required class variables are not implemented
                or are of incorrect types.
        """
        cls._validate_subclass_config()
        if '_HARDCODED_DEFAULT_OPTIONS' not in cls.__dict__:
            options_type: type[ReporterOptions] = getattr(cls, '_OPTIONS_TYPE')
            options_kwargs: dict[str, Any] = getattr(cls, '_OPTIONS_KWARGS')
            setattr(cls, '_HARDCODED_DEFAULT_OPTIONS', options_type(**options_kwargs))
        return getattr(cls, '_HARDCODED_DEFAULT_OPTIONS')

    @classmethod
    def set_default_options(cls, options: Options | None = None) -> None:
        """Set the default options for the  reporter.

        Args:
            options (ReporterOptions | None, default=None): The options to set as the default.
        """
        cls._validate_subclass_config()
        options_type = getattr(cls, '_OPTIONS_TYPE')
        if options.__class__ is ReporterOptions:
            raise SimpleBenchTypeError(
                "Invalid type for options argument in set_default_options(). "
                "Expected ReporterOptions subclass instance or None and got ReporterOptions base class instance.",
                tag=ReporterErrorTag.SET_DEFAULT_OPTIONS_INVALID_OPTIONS_ARG_TYPE_BASE_CLASS_INSTANCE)
        if not isinstance(options, options_type) and options is not None:
            raise SimpleBenchTypeError(
                "Invalid type for options argument in set_default_options(). "
                f"Expected {options_type} or None and got {type(options)}.",
                tag=ReporterErrorTag.SET_DEFAULT_OPTIONS_INVALID_OPTIONS_ARG_TYPE)
        setattr(cls, '_DEFAULT_OPTIONS', options)

    @classmethod
    def get_default_options(cls) -> Options:
        """Get the default options for the reporter.

        Returns the default options set via set_default_options() if set,
        otherwise returns the built-in hardcoded default options from
        `get_hardcoded_default_options()`.

        Returns:
            ReporterOptions: The default options.
        """
        cls._validate_subclass_config()
        if '_DEFAULT_OPTIONS' in cls.__dict__:
            user_default = getattr(cls, '_DEFAULT_OPTIONS')
            if user_default is not None:
                return user_default
        return cls.get_hardcoded_default_options()

    def __init__(self,
                 *,
                 name: str,
                 description: str,
                 sections: Iterable[Section],
                 targets: Iterable[Target],
                 default_targets: Iterable[Target] | None = None,
                 subdir: str = '',
                 file_suffix: str,
                 file_unique: bool,
                 file_append: bool,
                 formats: Iterable[Format],
                 choices: ChoicesConf) -> None:
        """
        Initialize the Reporter instance.

        Note:
            Exactly one of `file_unique` or `file_append` must be `True`. If both are `False`,
            or if both are `True`, an exception will be raised.

        Args:
            name (str):
                The unique identifying name of the reporter.

                - must be a non-empty string.
            description (str):
                A brief description of the reporter.

                - must be a non-empty string.

                - If `None`, the reporter's hardcoded default options type will be used.
            sections (Iterable[Section]):
                An iterable of all Sections supported by the reporter.

                - Must include at least one Section.
            targets (Iterable[Target]):
                An iterable of all Targets supported by the reporter.

                - Must include at least one Target.
            default_targets (Iterable[Target] | None, default=None):
                An iterable of default Targets for the reporter.
            subdir (str, default=''):
                The subdirectory where report files will be saved.
                - May be an empty string (''), which indicates the base output directory.
                - Cannot contain non-alphanumeric characters (characters other than A-Z, a-z, 0-9).
                - Cannot be longer than 64 characters.
                - If empty, reports will be saved in the base output directory.
            file_suffix (str):
                An optional file suffix for reporter output files.
                - May be an empty string ('')
                - Cannot contain non-alphanumeric characters (characters other than A-Z, a-z, 0-9).
                - Cannot be longer than 10 characters.
            file_unique (bool):
                Whether output files should have unique names by default.
            file_append (bool):
                Whether output files should be appended to by default.
            formats (Iterable[Format]):
                An iterable of all Formats supported by the reporter.
                - Must include at least one Format.
            choices (ChoicesConf):
                An iterable of ChoicesConf instances defining the sections, output targets,
                and formats supported by the reporter.
                - Must have at least one ChoiceConf.

        Raises:
            SimpleBenchValueError: If any of the provided parameters have invalid values.
            SimpleBenchTypeError: If any of the provided parameters are of incorrect types.
        """
        deferred_core_imports()
        self.__class__._validate_subclass_config()

        self._name: str = validate_string(
            name, 'name',
            ReporterErrorTag.NAME_INVALID_ARG_TYPE,
            ReporterErrorTag.NAME_INVALID_ARG_VALUE,
            allow_empty=False, allow_blank=False)
        """The unique identifying name of the reporter (private backing field)"""

        self._description: str = validate_string(
            description, 'description',
            ReporterErrorTag.DESCRIPTION_INVALID_ARG_TYPE,
            ReporterErrorTag.DESCRIPTION_INVALID_ARG_VALUE,
            allow_empty=False, allow_blank=False)
        """A brief description of the reporter (private backing field)"""

        self._sections: frozenset[Section] = frozenset(
            validate_iterable_of_type(
                sections, Section, 'sections',
                ReporterErrorTag.SECTIONS_INVALID_ARG_TYPE,
                ReporterErrorTag.SECTIONS_ITEMS_ARG_VALUE,
                allow_empty=False))
        """The set of supported Sections for the reporter (private backing field)"""

        self._targets: frozenset[Target] = frozenset(
            validate_iterable_of_type(
                targets, Target, 'targets',
                ReporterErrorTag.TARGETS_INVALID_ARG_TYPE,
                ReporterErrorTag.TARGETS_ITEMS_ARG_VALUE,
                allow_empty=False))
        """The set of supported Targets for the reporter (private backing field)"""

        self._default_targets: frozenset[Target] = frozenset(
            validate_iterable_of_type(
                default_targets if default_targets is not None else set(),
                Target, 'default_targets',
                ReporterErrorTag.DEFAULT_TARGETS_INVALID_ARG_TYPE,
                ReporterErrorTag.DEFAULT_TARGETS_ITEMS_ARG_VALUE,                allow_empty=True))
        """The default set of Targets for the reporter (private backing field)"""

        subdir = validate_string(
            subdir, 'subdir',
            ReporterErrorTag.SUBDIR_INVALID_ARG_TYPE,
            ReporterErrorTag.SUBDIR_INVALID_ARG_VALUE,
            strip=False, allow_empty=True, allow_blank=False, alphanumeric_only=True)
        if len(subdir) > 64:
            raise SimpleBenchValueError(
                "subdir cannot be longer than 64 characters (passed subdir was '{subdir}')",
                tag=ReporterErrorTag.SUBDIR_TOO_LONG)
        self._subdir: str = subdir
        """The subdirectory where report files will be saved (private backing field)"""

        file_suffix = validate_string(
            file_suffix, 'file_suffix',
            ReporterErrorTag.FILE_SUFFIX_INVALID_ARG_TYPE,
            ReporterErrorTag.FILE_SUFFIX_INVALID_ARG_VALUE,
            strip=False, allow_empty=True, allow_blank=False, alphanumeric_only=True)
        if len(file_suffix) > 10:
            raise SimpleBenchValueError(
                f"file_suffix cannot be longer than 10 characters (passed suffix was '{file_suffix}')",
                tag=ReporterErrorTag.FILE_SUFFIX_ARG_TOO_LONG)
        self._file_suffix: str = file_suffix
        """The file suffix for reporter output files (private backing field)"""

        self._file_unique: bool = validate_bool(
            file_unique, 'file_unique',
            ReporterErrorTag.FILE_UNIQUE_INVALID_ARG_TYPE)
        """Whether output files should have unique names (private backing field)"""

        self._file_append: bool = validate_bool(
            file_append, 'file_append',
            ReporterErrorTag.FILE_APPEND_INVALID_ARG_TYPE)
        """Whether output files should be appended to private backing field)"""

        if self._file_unique == self._file_append:
            raise SimpleBenchValueError(
                "Exactly one of file_unique or file_append must be True",
                tag=ReporterErrorTag.FILE_UNIQUE_AND_FILE_APPEND_EXACTLY_ONE_REQUIRED)

        self._formats: frozenset[Format] = frozenset(
            validate_iterable_of_type(
                formats, Format, 'formats',
                ReporterErrorTag.FORMATS_INVALID_ARG_TYPE,
                ReporterErrorTag.FORMATS_ITEMS_ARG_VALUE,
                allow_empty=False))
        """The set of supported Formats for the reporter (private backing field)"""

        choices = validate_type(
            choices, ChoicesConf, 'choices',
            ReporterErrorTag.CHOICES_INVALID_ARG_TYPE)

        choices_list: list[Choice] = []
        for item in choices.values():
            choices_list.append(Choice(reporter=self, choice_conf=item))  # pylint: disable=used-before-assignment

        self._choices = Choices(choices_list)
        """An instance of `Choices` containing the `Choice` instances for the `Reporter`.

        This is constructed from an iterable of `Choice` instances (private backing field)"""

    @staticmethod
    def find_options_by_type(options: Iterable[ReporterOptions] | None, cls: type[T]) -> T | None:
        """Retrieve an instance of type cls (if present) from a collection of `ReporterOptions`.

        This is used to extract reporter specific options from an iterable container of generic
        `ReporterOptions` such as those associated with a `Choice` or `Case`.

        For example, a `CSVReporter` may define a `CSVReporterOptions` class that extends
        `ReporterOptions` and use this method to extract the `CSVReporterOptions` instance
        from the options iterable:

            options = Reporter.find_options_by_type(case.options, CSVReporterOptions)

        Args:
            options (Iterable[ReporterOptions]): An iterable of `ReporterOptions` instances.
            cls: (type[T]): The specific subclass type of `ReporterOptions` to find.

        Returns:
            T | None: The instance of the class `cls` if found, otherwise `None`.
        """
        if options is None:
            return None
        if not isinstance(cls, type):
            raise SimpleBenchTypeError(
                "cls argument must be a type",
                tag=ReporterErrorTag.FIND_OPTIONS_BY_TYPE_INVALID_CLS_ARG_TYPE)
        options = validate_iterable_of_type(
            options, ReporterOptions, 'options',
            ReporterErrorTag.FIND_OPTIONS_BY_TYPE_INVALID_OPTIONS_ARG,
            ReporterErrorTag.FIND_OPTIONS_BY_TYPE_INVALID_OPTIONS_ARG,
            allow_empty=True)
        for item in options:
            if isinstance(item, cls):
                return item  # type: ignore
        return None

    def report(self,
               *,
               args: Namespace,
               case: Case,
               choice: Choice,
               path: Optional[Path] = None,
               session: Optional[Session] = None,
               callback: Optional[ReporterCallback] = None) -> None:
        """Generate a report based on the benchmark results. This method
        performs validation and then calls the subclass's run_report method.

        Args:
            args (Namespace): The parsed command-line arguments.
            case (Case): The Case instance containing benchmark results.
            choice (Choice): The Choice instance specifying the report configuration.
            path (Optional[Path]): The path to the directory where the report can be saved if needed.
                Leave as None if not saving to the filesystem.
            session (Optional[Session]): The Session instance containing benchmark results.
            callback (Optional[Callable[[Case, Section, Any], None]]):
                A callback function for additional processing of the report.
        """
        if not isinstance(args, Namespace):
            raise SimpleBenchTypeError(
                "args argument must be an argparse.Namespace instance",
                tag=ReporterErrorTag.REPORT_INVALID_ARGS_ARG_TYPE)
        # is_* checks handle deferred import runtime type checking for Case, Choice, and Session
        if not is_case(case):
            raise SimpleBenchTypeError(
                "Expected a Case instance",
                tag=ReporterErrorTag.REPORT_INVALID_CASE_ARG)
        if not is_choice(choice):
            raise SimpleBenchTypeError(
                "Expected a Choice instance",
                tag=ReporterErrorTag.REPORT_INVALID_CHOICE_ARG)
        if not is_session(session) and session is not None:
            raise SimpleBenchTypeError(
                "session must be a Session instance if provided",
                tag=ReporterErrorTag.REPORT_INVALID_SESSION_ARG)

        unsupported_sections = choice.sections - self.supported_sections()
        if unsupported_sections:
            sections_error = f"Unsupported Section(s) in Choice().sections: {unsupported_sections}"
            raise SimpleBenchValueError(
                sections_error,
                tag=ReporterErrorTag.REPORT_UNSUPPORTED_SECTION)

        unsupported_targets = choice.targets - self.supported_targets()
        if unsupported_targets:
            targets_error = f"Unsupported Target(s) in Choice().targets: {unsupported_targets}"
            raise SimpleBenchValueError(
                targets_error,
                tag=ReporterErrorTag.REPORT_UNSUPPORTED_TARGET)

        if choice.output_format not in self.supported_formats():
            raise SimpleBenchValueError(
                f"Unsupported Format in Choice().output_format: {choice.output_format}",
                tag=ReporterErrorTag.REPORT_UNSUPPORTED_FORMAT)

        if Target.CALLBACK in choice.targets:
            if callback is not None and not callable(callback):
                raise SimpleBenchTypeError(
                    "Callback function must be callable if provided",
                    tag=ReporterErrorTag.REPORT_INVALID_CALLBACK_ARG)
        if Target.FILESYSTEM in choice.targets and not isinstance(path, Path):
            raise SimpleBenchTypeError(
                "Path must be a pathlib.Path instance when using FILESYSTEM target",
                tag=ReporterErrorTag.REPORT_INVALID_PATH_ARG)

        # Only proceed if there are results to report
        # TODO: THINK ABOUT THIS MORE. SHOULD WE RAISE AN EXCEPTION INSTEAD?
        results = case.results
        if not results:
            return

        # If we reach this point, all validation has passed and execution
        # will pass through to the subclass implementation
        self.run_report(args=args, case=case, choice=choice, path=path, session=session, callback=callback)

    @abstractmethod
    def render(self, *, case: "Case", section: "Section", options: "ReporterOptions") -> str | bytes | Text | Table:
        """Render the report for a specific case and section.

        This abstract method must be implemented by all Reporter subclasses. It is responsible
        for generating the actual report content for a given case and section, based on the
        provided options.

        The output can be a string, bytes, or a Rich object (Text or Table).

        Args:
            case (Case): The Case instance containing the benchmark results.
            section (Section): The specific section of the results to render.
            options (ReporterOptions): The reporter-specific options for rendering.

        Returns:
            str | bytes | Text | Table: The rendered report content.

        Raises:
            NotImplementedError: If the method is not implemented in a subclass.
        """
        raise SimpleBenchNotImplementedError(
            "Reporter subclasses must implement the render method",
            tag=ReporterErrorTag.RENDER_NOT_IMPLEMENTED)

    def run_report(self,
                   *,
                   args: Namespace,
                   case: Case,
                   choice: Choice,
                   path: Optional[Path] = None,
                   session: Optional[Session] = None,
                   callback: Optional[ReporterCallback] = None) -> None:
        """Internal method that generates the report by rendering each section.

        This default implementation calls `render_by_section` to generate the report.

        Subclasses can override this method to provide custom report generation logic,
        for example by calling `render_by_case` for reports that are generated once
        per case.

        Note:

            To process Target.CUSTOM or other non-standard targets, subclasses
            should implement their own custom logic within this method.

        This method is called by the base class's report() method after validation. The base class
        handles validation of the arguments, so subclasses can assume the arguments
        are valid. The base class also handles lazy loading of classes that could not
        be loaded at init, so subclasses can assume any required imports are available.

        Because some reporters may not need all available arguments, such as 'path',
        'session', or 'callback', the subclass implementation may choose to ignore
        any arguments that are not applicable.

        Args:
            args (Namespace): The parsed command-line arguments.
            case (Case): The Case instance representing the benchmarked code.
            choice (Choice): The Choice instance specifying the report configuration.
            path (Optional[Path]): The path to the directory where the CSV file(s) will be saved.
            session (Optional[Session]): The Session instance containing benchmark results.
            callback (Optional[ReporterCallback]): A callback function for additional processing of the report.
                The function should accept four arguments: the Case instance, the Section instance,
                the Format instance, and the report output.

                Example callback function signature:
                    def my_callback(case: Case, section: Section, output_format: Format, output: Any) -> None:
                        # Custom processing logic here

        Return:
            None

        Raises:
            SimpleBenchTypeError: If the provided arguments are not of the expected types or if
                required arguments are missing. Also raised if the callback is not callable when
                provided for a CALLBACK target or if the path is not a Path instance when a FILESYSTEM
                target is specified.
            SimpleBenchValueError: If an unsupported section or target is specified in the choice.
        """
        self.render_by_section(
            case=case,
            choice=choice,
            path=path,
            session=session,
            callback=callback,
            args=args
        )

    def add_choice(self, choice: Choice) -> None:
        """Add a Choice to the reporter's Choices.

        Args:
            choice (ChoiceConf):
                The Choice instance to add.

        Raises:
            SimpleBenchTypeError: If the provided choice is not a Choice instance.
            SimpleBenchValueError: If the choice's sections, targets, or formats
                are not supported by the reporter.
        """
        # is_choice check handles deferred import runtime type checking for Choice
        if not is_choice(choice):
            raise SimpleBenchTypeError(
                "Expected a Choice instance",
                tag=ReporterErrorTag.ADD_CHOICE_INVALID_ARG_TYPE)

        unsupported_sections = choice.sections - self.supported_sections()
        if unsupported_sections:
            raise SimpleBenchValueError(
                f"Unsupported Section(s) in Choice().sections: {unsupported_sections}",
                tag=ReporterErrorTag.ADD_CHOICE_UNSUPPORTED_SECTION)

        unsupported_targets = choice.targets - self.supported_targets()
        if unsupported_targets:
            raise SimpleBenchValueError(
                f"Unsupported Target(s) in Choice().targets: {unsupported_targets}",
                tag=ReporterErrorTag.ADD_CHOICE_UNSUPPORTED_TARGET)

        if choice.output_format not in self.supported_formats():
            raise SimpleBenchValueError(
                f"Unsupported Format in Choice().output_format: {choice.output_format}",
                tag=ReporterErrorTag.ADD_CHOICE_UNSUPPORTED_FORMAT)

        self.choices.add(choice)

    @property
    def choices(self) -> Choices:
        """Return the Choices instance for the reporter, including sections, output targets, and formats.

        The Choices instance contains one or more Choice instances, each representing a specific combination of
        sections, targets, and formats, command line flags, and descriptions.

        This property allows access to the reporter's choices for generating reports and customizing report
        output and available options.

        Returns:
            Choices: The Choices instance for the reporter.
        """
        return self._choices

    @property
    def name(self) -> str:
        """The unique identifying name of the reporter."""
        return self._name

    @property
    def description(self) -> str:
        """A brief description of the reporter."""
        return self._description

    @property
    def options_type(self) -> type[Options]:
        """The specific ReporterOptions subclass associated with this reporter.
        """
        return self.__class__.get_default_options().__class__

    @property
    def subdir(self) -> str:
        """The subdirectory where report files will be saved."""
        return self._subdir

    @property
    def default_targets(self) -> frozenset[Target]:
        """The default set of Targets for the reporter."""
        return self._default_targets

    @property
    def file_suffix(self) -> str:
        """The file suffix for reporter output files."""
        return self._file_suffix

    @property
    def file_unique(self) -> bool:
        """Whether output files should have unique names."""
        return self._file_unique

    @property
    def file_append(self) -> bool:
        """Whether output files should be appended to."""
        return self._file_append

    def supported_sections(self) -> frozenset[Section]:
        """Return the set of supported Sections for the reporter.

        This is the set of Sections that the reporter can include in its reports.

        Defined Choices can only include Sections that are declared in this set.
        """
        return self._sections

    def supported_targets(self) -> frozenset[Target]:
        """Return the set of supported Targets for the reporter.

        This is the set of Targets that the reporter can output to.

        Defined Choices can only include Targets that are declared in this set.
        """
        return self._targets

    def supported_formats(self) -> frozenset[Format]:
        """Return the set of supported Formats for the reporter.

        This is the set of Formats that the reporter can output in.

        Defined Choices can only include Formats that are declared in this set.
        """
        return self._formats

    def get_base_unit_for_section(self, section: Section) -> str:
        """Return the base unit for the specified section.

        Args:
            section (Section): The section to get the base unit for.

        Returns:
            str: The base unit for the section.
        """
        match section:
            case Section.OPS:
                return BASE_OPS_PER_INTERVAL_UNIT
            case Section.TIMING:
                return BASE_INTERVAL_UNIT
            case Section.MEMORY:
                return BASE_MEMORY_UNIT
            case Section.PEAK_MEMORY:
                return BASE_MEMORY_UNIT
            case _:
                raise SimpleBenchValueError(
                    f"Unsupported section: {section} (this should never happen)",
                    tag=ReporterErrorTag.RUN_REPORT_UNSUPPORTED_SECTION)

    def get_all_stats_values(self, results: list[Results], section: Section) -> list[float]:
        """Gathers all primary statistical values for a given section across multiple results.

        It collects mean, median, minimum, maximum, 5th percentile, 95th percentile,
        from each Results instance for the specified section.

        This method is useful in determining appropriate scaling factors or units
        for reporting by analyzing the range of values across all results.

        Adjusted standard deviation is not included in this collection because it can
        be NaN for results with insufficient data points, or orders of magnitude different
        from the other statistics, which can skew scaling calculations.
        Args:
            results (list[Results]): A list of Results instances to gather statistics from.
            section (Section): The section to gather statistics for.

        Returns:
            list[float]: A list of all gathered statistical values.
        """
        all_numbers = []
        for result in results:
            stats = result.results_section(section)
            all_numbers.extend([
                stats.mean, stats.median, stats.minimum, stats.maximum,
                stats.percentiles[5], stats.percentiles[95]
            ])
        return all_numbers
