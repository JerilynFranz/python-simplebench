"""Reporter base class.

This module defines the Reporter abstract base class, which serves as the foundation
for all reporter implementations in the SimpleBench benchmarking framework. A Reporter
is responsible for generating reports based on benchmark results from a Session and Case.
Reporters can produce reports in various formats and output them to different targets.
"""
from __future__ import annotations
from abc import ABC, abstractmethod
from argparse import ArgumentParser, Namespace
from io import StringIO
from pathlib import Path
from typing import Optional, Iterable, TypeVar, TYPE_CHECKING

from rich.console import Console
from rich.table import Table
from rich.text import Text

from simplebench.defaults import BASE_INTERVAL_UNIT, BASE_OPS_PER_INTERVAL_UNIT, BASE_MEMORY_UNIT
from simplebench.enums import Section, Target, Format, FlagType
from simplebench.exceptions import SimpleBenchTypeError, SimpleBenchValueError, SimpleBenchNotImplementedError
from simplebench.metaclasses import ICase, ISession
from simplebench.results import Results
from simplebench.utils import collect_arg_list, first_not_none, sanitize_filename
from simplebench.validators import (validate_iterable_of_type, validate_string,
                                    validate_type, validate_filename)

# simplebench.reporters
from simplebench.reporters.choices.metaclasses import IChoices
from simplebench.reporters.choice.metaclasses import IChoice
from simplebench.reporters.protocols import ReporterCallback

# simplebench.reporters.reporter
from simplebench.reporters.reporter.exceptions import ReporterErrorTag
from simplebench.reporters.reporter.metaclasses import IReporter
from simplebench.reporters.reporter.options import ReporterOptions

if TYPE_CHECKING:
    from simplebench.case import Case
    from simplebench.session import Session
    from simplebench.reporters.choice import Choice
    from simplebench.reporters.choices import Choices

T = TypeVar('T')

NO_ATTRIBUTE = object()
"""Sentinel value for no attribute."""


class Reporter(ABC, IReporter):
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

    _HARDCODED_DEFAULT_OPTIONS: ReporterOptions = ReporterOptions()
    """Built-in default CSVReporterOptions instance for the reporter used if none is specified
    in a passed `Case`, `Choice`, or by `_DEFAULT_OPTIONS`. It forms the basis for the
    dynamic default options functionality provided by the `set_default_options()` and
    `get_default_options()` methods.

    Subclasses **SHOULD** override this with their own default specific options instances
    as appropriate for the reporter to provide sensible defaults.
    """

    @classmethod
    def get_hardcoded_default_options(cls) -> ReporterOptions:
        """Get the built-in hardcoded default options for the reporter.

        Returns:
            ReporterOptions: The built-in hardcoded default ReporterOptions instance.
        """
        return cls._HARDCODED_DEFAULT_OPTIONS

    _DEFAULT_OPTIONS: ReporterOptions | None = None
    """Default ReporterOptions instance for the reporter.

    Note:
        The value None indicates that the built-in hardcoded default options
        `get_hardcoded_default_options()` should be used.

        See the `get_default_options()` method for details.
    """
    @classmethod
    def set_default_options(cls, options: ReporterOptions | None = None) -> None:
        """Set the default options for the  reporter.

        Args:
            options (ReporterOptions | None, default=None): The options to set as the default.
        """
        if options is None or isinstance(options, ReporterOptions):
            cls._DEFAULT_OPTIONS = options

        else:
            raise SimpleBenchTypeError(
                f"Invalid type for options argument in set_default_options(). "
                f"Expected ReporterOptions or None and got {type(options)}.",
                tag=ReporterErrorTag.GET_OPTIONS_INVALID_OPTIONS_ARG_TYPE)

    @classmethod
    def get_default_options(cls) -> ReporterOptions:
        """Get the default options for the reporter.

        Returns the default options set via set_default_options() if set,
        otherwise returns the built-in hardcoded default options from
        `get_hardcoded_default_options()`.

        Returns:
            ReporterOptions | None: The default options.
        """
        if cls._DEFAULT_OPTIONS is None:
            return cls.get_hardcoded_default_options()
        return cls._DEFAULT_OPTIONS

    @abstractmethod
    def __init__(self,
                 *,
                 name: str,
                 description: str,
                 options_type: type[ReporterOptions],
                 sections: set[Section],
                 targets: set[Target],
                 default_targets: set[Target] | None = None,
                 subdir: str = '',
                 file_suffix: str,
                 file_unique: bool,
                 file_append: bool,
                 formats: set[Format],
                 choices: Choices) -> None:
        """
        Initialize the Reporter instance.

        Note:

            file_append and file_unique are mutually exclusive options. They cannot both be True.

        Args:
            name (str): The unique identifying name of the reporter. Must be a non-empty string.
            description (str): A brief description of the reporter. Must be a non-empty string.
            options_type (type[ReporterOptions] | None): The specific ReporterOptions subclass
                associated with this reporter, or None if no specific options are defined.
            sections (set[Section]): The set of all Sections supported by the reporter.
            targets (set[Target]): The set of all Targets supported by the reporter.
            default_targets (set[Target] | None, default=None): The default set of Targets for the reporter.
            subdir (str, default=''): The subdirectory where report files will be saved.
            file_suffix (str): An optional file suffix for reporter output files.
                - May be an empty string ('')
                - Cannot contain non-alphanumeric characters (characters other than A-Z, a-z, 0-9).
                - Cannot be longer than 10 characters.
            file_unique (bool): Whether output files should have unique names.
            file_append (bool): Whether output files should be appended to.
            formats (set[Format]): The set of Formats supported by the reporter.
            choices (Choices): A Choices instance defining the sections, output targets,
                and formats supported by the reporter. Must have at least one Choice.

        Raises:
            SimpleBenchNotImplementedError: If any of the required attributes
                are not provided
            SimpleBenchValueError: If any of the provided attributes have invalid values.
            SimpleBenchTypeError: If any of the provided attributes are of incorrect types.
        """
        self._name: str = validate_string(
            name, 'name',
            ReporterErrorTag.NAME_INVALID_ARG_TYPE,
            ReporterErrorTag.NAME_INVALID_ARG_VALUE)
        """The unique identifying name of the reporter.
        (private backing field)"""

        self._description: str = validate_string(
            description, 'description',
            ReporterErrorTag.DESCRIPTION_INVALID_ARG_TYPE,
            ReporterErrorTag.DESCRIPTION_INVALID_ARG_VALUE)
        """A brief description of the reporter.
        (private backing field)"""

        if not issubclass(options_type, ReporterOptions):
            raise SimpleBenchTypeError(
                "options_type must be a subclass of ReporterOptions",
                tag=ReporterErrorTag.OPTIONS_TYPE_INVALID_VALUE)
        self._options_type: type[ReporterOptions] = options_type
        """The specific ReporterOptions subclass associated with this reporter.
        (private backing field)"""

        if not isinstance(sections, set):
            raise SimpleBenchTypeError(
                "sections must be a set of Section enums and cannot be empty",
                tag=ReporterErrorTag.INVALID_SECTIONS_ARG_TYPE)
        if len(sections) == 0:
            raise SimpleBenchTypeError(
                "sections cannot be an empty set",
                tag=ReporterErrorTag.EMPTY_SECTIONS_ARG_VALUE)
        if not all(isinstance(section, Section) for section in sections):
            raise SimpleBenchTypeError(
                "All items in sections must be of type Section",
                tag=ReporterErrorTag.INVALID_SECTIONS_ENTRY_TYPE)
        self._sections: frozenset[Section] = frozenset(sections)
        """The set of supported Sections for the reporter.
        (private backing field)"""

        if not isinstance(targets, set):
            raise SimpleBenchTypeError(
                "Reporter subclasses must provide a non-empty set of Targets",
                tag=ReporterErrorTag.TARGETS_NOT_IMPLEMENTED)
        if len(targets) == 0:
            raise SimpleBenchTypeError(
                "targets cannot be an empty set",
                tag=ReporterErrorTag.EMPTY_TARGETS_ARG_VALUE)
        if not all(isinstance(target, Target) for target in targets):
            raise SimpleBenchTypeError(
                "All items in targets must be of type Target",
                tag=ReporterErrorTag.INVALID_TARGETS_ENTRY_TYPE)
        self._targets: frozenset[Target] = frozenset(targets)
        """The set of supported Targets for the reporter.
        (private backing field)"""

        if default_targets is None:
            default_targets = set()
        if not isinstance(default_targets, set):
            raise SimpleBenchTypeError(
                "default_targets must be a set of Target enums",
                tag=ReporterErrorTag.INVALID_DEFAULT_TARGETS_ARG_TYPE)
        if not all(isinstance(target, Target) for target in default_targets):
            raise SimpleBenchTypeError(
                "All items in default_targets must be of type Target",
                tag=ReporterErrorTag.INVALID_DEFAULT_TARGETS_ENTRY_TYPE)
        self._default_targets: frozenset[Target] = frozenset(default_targets)
        """The default set of Targets for the reporter.
        (private backing field)"""

        self._subdir: str = validate_string(
            subdir, 'subdir',
            ReporterErrorTag.INVALID_SUBDIR_ARG_TYPE,
            ReporterErrorTag.INVALID_SUBDIR_ARG_VALUE,
            strip=False, allow_empty=False, allow_blank=False, alphanumeric_only=True)
        """The subdirectory where report files will be saved.
        (private backing field)"""
        if len(self._subdir) > 64:
            raise SimpleBenchValueError(
                "subdir cannot be longer than 64 characters (passed subdir was '{subdir}')",
                tag=ReporterErrorTag.SUBDIR_TOO_LONG)

        validate_string(
            file_suffix, 'file_suffix',
            ReporterErrorTag.FILE_SUFFIX_INVALID_ARG_TYPE,
            ReporterErrorTag.FILE_SUFFIX_INVALID_ARG_VALUE,
            strip=False, allow_empty=True, allow_blank=False, alphanumeric_only=True)
        if len(file_suffix) > 10:
            raise SimpleBenchValueError(
                f"file_suffix cannot be longer than 10 characters (passed suffix was '{file_suffix}')",
                tag=ReporterErrorTag.FILE_SUFFIX_ARG_TOO_LONG)
        self._file_suffix: str = file_suffix
        """The file suffix for reporter output files.
        (private backing field)"""

        self._file_unique: bool = validate_type(
            value=file_unique, expected=bool, name='file_unique',
            error_tag=ReporterErrorTag.FILE_UNIQUE_INVALID_ARG_TYPE)
        """Whether output files should have unique names.
        (private backing field)"""

        self._file_append: bool = validate_type(
            value=file_append, expected=bool, name='file_append',
            error_tag=ReporterErrorTag.FILE_APPEND_INVALID_ARG_TYPE)
        """Whether output files should be appended to.
        (private backing field)"""

        if not isinstance(formats, set) or len(formats) == 0:
            raise SimpleBenchNotImplementedError(
                "Reporter subclasses must provide a non-empty set of Formats",
                tag=ReporterErrorTag.FORMATS_NOT_IMPLEMENTED)
        if not all(isinstance(output_format, Format) for output_format in formats):
            raise SimpleBenchTypeError(
                "All items in formats must be of type Format",
                tag=ReporterErrorTag.INVALID_FORMATS_ENTRY_TYPE)
        self._formats: frozenset[Format] = frozenset(formats)
        """The set of supported Formats for the reporter.
        (private backing field)"""

        if not isinstance(choices, IChoices):
            raise SimpleBenchTypeError(
                f"choices must be a Choices instance: cannot be a {type(choices)}",
                tag=ReporterErrorTag.INVALID_CHOICES_ARG_TYPE)
        if len(choices) == 0:
            raise SimpleBenchNotImplementedError(
                "Reporter subclasses must initialize the Choices with at least one Choice",
                tag=ReporterErrorTag.INVALID_CHOICES_ARG_VALUE)
        self._choices: Choices = choices
        """The Choices instance defining the sections, output targets,
        and formats supported by the reporter.
        (private backing field)"""

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
        options = validate_iterable_of_type(
            options, ReporterOptions, 'options',
            ReporterErrorTag.GET_OPTIONS_INVALID_OPTIONS_ARG_TYPE,
            ReporterErrorTag.GET_OPTIONS_INVALID_OPTIONS_ARG_VALUE,
            allow_empty=True)
        for item in options:
            if isinstance(item, cls):
                return item
        return None

    def select_targets_from_args(
            self, *,
            args: Namespace, choice: Choice, default_targets: Iterable[Target]) -> set[Target]:
        """Select the output targets based on command-line arguments and choice configuration.

        It checks the command-line arguments for any flags corresponding to the choice
        and collects the specified targets. The default target(s) are any Target enums defined
        in the arg values for the flags. They are discarded if there are explicit targets specified
        in the args as strings. Finally, it ensures that the selected targets are valid for the
        given choice.

        An exception is raised if an unsupported target is specified in the arguments.

        Args:
            args (Namespace): The parsed command-line arguments.
            choice (Choice): The Choice instance specifying the report configuration.
            default_targets (Iterable[Target]]): The default targets to use if no targets
                are specified in the command-line arguments.

        Returns:
            A set of Target enums representing the selected output targets.

        Raises:
            SimpleBenchTypeError: If args is not an argparse.Namespace instance.
            SimpleBenchValueError: If an unsupported target is specified in the arguments.
        """
        selected_targets: set[Target] = set()
        target_members = Target.__members__
        reverse_target_map = {v.value: v for k, v in target_members.items()}
        for flag in choice.flags:
            target_names = collect_arg_list(
                args=args, flag=flag, include_comma_separated=True)
            if not target_names:
                continue  # No targets specified for this flag, skip to next flag
            for target in target_names:
                target_enum = reverse_target_map.get(target, None)
                if target_enum is not None:
                    if target_enum in choice.targets:
                        selected_targets.add(target_enum)
                    else:
                        raise SimpleBenchValueError(
                            f"Output target {target} is not supported by {flag}.",
                            tag=ReporterErrorTag.UNSUPPORTED_TARGET_IN_ARGS)
                else:
                    raise SimpleBenchValueError(
                        f"Unknown output target specified for {flag}: {target}",
                        tag=ReporterErrorTag.UNKNOWN_TARGET_IN_ARGS)

        return set(default_targets) if not selected_targets else selected_targets

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
        Raises:
            NotImplementedError: If the method is not implemented in a subclass.
        """
        if not isinstance(args, Namespace):
            raise SimpleBenchTypeError(
                "args argument must be an argparse.Namespace instance",
                tag=ReporterErrorTag.REPORT_INVALID_ARGS_ARG_TYPE)
        if not isinstance(case, ICase):
            raise SimpleBenchTypeError(
                "Expected a Case instance",
                tag=ReporterErrorTag.REPORT_INVALID_CASE_ARG)
        if not isinstance(choice, IChoice):
            raise SimpleBenchTypeError(
                "Expected a Choice instance",
                tag=ReporterErrorTag.REPORT_INVALID_CHOICE_ARG)
        for section in choice.sections:
            if section not in self.supported_sections():
                raise SimpleBenchValueError(
                    f"Unsupported Section in Choice: {section}",
                    tag=ReporterErrorTag.REPORT_UNSUPPORTED_SECTION)
        for target in choice.targets:
            if target not in self.supported_targets():
                raise SimpleBenchValueError(
                    f"Unsupported Target in Choice: {target}",
                    tag=ReporterErrorTag.REPORT_UNSUPPORTED_TARGET)
        if Target.CALLBACK in choice.targets:  # pylint: disable=used-before-assignment
            if callback is not None and not callable(callback):
                raise SimpleBenchTypeError(
                    "Callback function must be callable if provided",
                    tag=ReporterErrorTag.REPORT_INVALID_CALLBACK_ARG)
        if Target.FILESYSTEM in choice.targets and not isinstance(path, Path):
            raise SimpleBenchTypeError(
                "Path must be a pathlib.Path instance when using FILESYSTEM target",
                tag=ReporterErrorTag.REPORT_INVALID_PATH_ARG)

        if session is not None and not isinstance(session, ISession):
            raise SimpleBenchTypeError(
                "session must be a Session instance if provided",
                tag=ReporterErrorTag.REPORT_INVALID_SESSION_ARG)

        # Only proceed if there are results to report
        # TODO: THINK ABOUT THIS MORE
        results = case.results
        if not results:
            return

        # If we reach this point, all validation has passed and execution
        # will pass through to the subclass implementation
        self.run_report(args=args, case=case, choice=choice, path=path, session=session, callback=callback)

    @abstractmethod
    def run_report(self,
                   *,
                   args: Namespace,
                   case: Case,
                   choice: Choice,
                   path: Optional[Path] = None,
                   session: Optional[Session] = None,
                   callback: Optional[ReporterCallback] = None) -> None:
        """Internal method to be implemented by subclasses to actually generate the report.

        Output the benchmark results.

        This is a hook method that must be implemented by subclasses to perform the actual
        report generation based on the provided arguments.

        The concrete implementation of this method will typically just call the
        base class's render_by_section() (for reports that are rendered for each
        individual section) or the render_by_case() (for reports that only
        are generated once per case) as appropriate to handle the rendering of
        the report by section or entire case.

        This reduces the amount of boilerplate code that needs to be implemented
        in each reporter subclass to a minimum.

        If those two methods are not suitable, the subclass can implement its own custom
        report generation logic within this method instead.

        Note:

            To process Target.CUSTOM or other non-standard targets, subclasses
            should implement their own custom logic within this method.

        This method is called by the base class's report() method after validation. The base class
        handles validation of the arguments, so subclasses can assume the arguments
        are valid. The base class also handles lazy loading of classes that could not
        be loaded at init, so subclasses can assume any required imports are available.

        Because this method is a concrete implementation of an abstract method, it must be
        implemented by the subclass. However, because some reporters may not need all
        available arguments, such as 'path', 'session', or 'callback', the subclass implementation
        may choose to ignore any arguments that are not applicable.

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
            NotImplementedError: If the method is not implemented in a subclass.
        """
        raise SimpleBenchNotImplementedError(
            "Reporter subclasses must implement the report method",
            tag=ReporterErrorTag.RUN_REPORT_NOT_IMPLEMENTED)

    def add_choice(self, choice: Choice) -> None:
        """Add a Choice to the reporter's Choices.

        Args:
            choice (Choice): The Choice instance to add.

        Raises:
            SimpleBenchTypeError: If the provided choice is not a Choice instance.
            SimpleBenchValueError: If the choice's sections, targets, or formats
                are not supported by the reporter.
        """
        if not isinstance(choice, IChoice):
            raise SimpleBenchTypeError(
                "Expected a Choice instance",
                tag=ReporterErrorTag.ADD_CHOICE_INVALID_ARG_TYPE)

        for section in choice.sections:
            if section not in self.supported_sections():
                raise SimpleBenchValueError(
                    f"Unsupported Section in Choice: {section}",
                    tag=ReporterErrorTag.ADD_CHOICE_UNSUPPORTED_SECTION)
        for target in choice.targets:
            if target not in self.supported_targets():
                raise SimpleBenchValueError(
                    f"Unsupported Target in Choice: {target}",
                    tag=ReporterErrorTag.ADD_CHOICE_UNSUPPORTED_TARGET)
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
        """Return the unique identifying name of the reporter."""
        return self._name

    @property
    def description(self) -> str:
        """Return a brief description of the reporter."""
        return self._description

    @property
    def options_type(self) -> type[ReporterOptions]:
        """Return the specific ReporterOptions subclass associated with this reporter.
        """
        return self._options_type

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

    def target_filesystem(self, *,
                          path: Path | None,
                          subdir: str,
                          filename: str,
                          output: str | bytes | Text | Table,
                          unique: bool = False,
                          append: bool = False) -> None:
        """Helper method to output report data to the filesystem.

        path, subdir, and filename are combined to form the full path to the output file.

        If unique is True, the filename will be made unique by prepending a counter
        starting from 001 to the filename and counting up until a unique filename is found.
        E.g. 001_filename.txt, 002_filename.txt, etc.

        If append is True, the output will be appended to the file if it already exists.
        Otherwise, an exception will be raised if the file already exists. Note that
        append mode is not compatible with unique mode.

        The type signature for path is Path | None because the overall report() method
        accepts path as Optional[Path] because it is not always required. However,
        this method should only be called when a valid Path is provided and will
        raise an exception if it is not a Path instance.

        Args:
            path (Path | None): The path to the directory where output should be saved.
            subdir (str): The subdirectory within the path to save the file to.
            filename (str): The filename to save the output as.
            output (str | bytes | Text | Table): The report data to write to the file.
            unique (bool): If True, ensure the filename is unique by prepending a counter as needed.
            append (bool): If True, append to the file if it already exists. Otherwise, raise an error.

        Raises:
            SimpleBenchTypeError: If path is not a Path instance,
                or if subdir or filename are not strings.
            SimpleBenchValueError: If both append and unique are True. Or if the output file
                already exists and neither append nor unique options were specified.
        """
        path = validate_type(
            value=path, expected=Path, name='path',
            error_tag=ReporterErrorTag.TARGET_FILESYSTEM_INVALID_PATH_ARG_TYPE)
        subdir = validate_string(
            subdir, 'subdir',
            ReporterErrorTag.TARGET_FILESYSTEM_INVALID_SUBDIR_ARG_TYPE,
            ReporterErrorTag.TARGET_FILESYSTEM_INVALID_SUBDIR_ARG_VALUE,
            strip=False, allow_empty=True, allow_blank=False, alphanumeric_only=True)
        filename = validate_filename(filename)
        append = validate_type(
            value=append, expected=bool, name='append',
            error_tag=ReporterErrorTag.TARGET_FILESYSTEM_INVALID_APPEND_ARG_TYPE)
        unique = validate_type(
            value=unique, expected=bool, name='unique',
            error_tag=ReporterErrorTag.TARGET_FILESYSTEM_INVALID_UNIQUE_ARG_TYPE)
        if not isinstance(output, (str, bytes, Text, Table)):
            raise SimpleBenchTypeError(
                "output must be of type str, bytes, Text, or Table",
                tag=ReporterErrorTag.TARGET_FILESYSTEM_INVALID_OUTPUT_ARG_TYPE)
        if append and unique:
            raise SimpleBenchValueError(
                "append and unique options are not compatible when writing to filesystem",
                tag=ReporterErrorTag.TARGET_FILESYSTEM_APPEND_UNIQUE_INCOMPATIBLE_ARGS)
        if unique:
            counter = 1
            while (path / subdir / f"{counter:03d}_{filename}").exists():
                counter += 1
            filename = f"{counter:03d}_{filename}"

        if isinstance(output, (Text, Table)):
            output = self.rich_text_to_plain_text(output)
        output_path = path / subdir / filename
        output_path.parent.mkdir(parents=True, exist_ok=True)
        mode = 'wb' if isinstance(output, bytes) else 'w'
        if append:
            mode = 'ab' if isinstance(output, bytes) else 'a'
        if output_path.exists() and not append:
            raise SimpleBenchValueError(
                f"Output file already exists and neither append nor unique options were specified: {output_path}",
                tag=ReporterErrorTag.TARGET_FILESYSTEM_OUTPUT_FILE_EXISTS)
        with output_path.open(mode=mode) as f:
            f.write(output)

    def target_callback(self,
                        callback: ReporterCallback | None,
                        case: Case,
                        section: Section,
                        output_format: Format,
                        output: str | bytes | Text | Table) -> None:
        """Helper method to send report data to a callback function.

        Args:
            callback (ReporterCallback | None): The callback function to send the output to.
            case (Case): The Case instance representing the benchmarked code.
            section (Section): The Section of the report.
            output_format (Format): The Format of the report.
            output (str | bytes | Text | Table): The report data to send to the callback.

        Returns:
            None
        """
        if isinstance(output, (Text, Table)):
            output = self.rich_text_to_plain_text(output)
        if callback is not None:
            callback(case=case, section=section, output_format=output_format, output=output)

    def target_console(self, session: Session | None, output: str | bytes | Text | Table) -> None:
        """Helper method to output report data to the console.

        It uses the Rich Console instance from the Session if provided, otherwise
        it creates a new Console instance.

        It can accept output as a string, Rich Text, or Rich Table.

        Args:
            output (str | bytes | Text | Table): The report data to print to the console.

        Returns:
            None
        """
        console = session.console if session is not None else Console()
        console.print(output)

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

    def add_flags_to_argparse(self, parser: ArgumentParser) -> None:
        """Add the reporter's command-line flags to an ArgumentParser.

        This is an interface method for adding flags of different types to an ArgumentParser.

        Choices can define different types of flags, such as boolean flags or
        flags that accept multiple values (lists). This method allows adding
        flags of the specified type to the ArgumentParser.

        Args:
            parser (ArgumentParser): The ArgumentParser to add the flags to.
        """
        if not isinstance(parser, ArgumentParser):
            raise SimpleBenchTypeError(
                "parser arg must be an argparse.ArgumentParser instance",
                tag=ReporterErrorTag.ADD_FLAGS_INVALID_PARSER_ARG_TYPE)
        for choice in self.choices.values():
            match choice.flag_type:
                case FlagType.BOOLEAN:
                    self.add_boolean_flags_to_argparse(parser=parser, choice=choice)
                case FlagType.TARGET_LIST:
                    self.add_list_of_targets_flags_to_argparse(parser=parser, choice=choice)
                case _:
                    raise SimpleBenchValueError(
                        f"Unsupported flag type: {choice.flag_type}",
                        tag=ReporterErrorTag.ADD_FLAGS_UNSUPPORTED_FLAG_TYPE)

    def add_list_of_targets_flags_to_argparse(self, parser: ArgumentParser, choice: Choice) -> None:
        """Add a Choice's command-line flags to an ArgumentParser.

        This is a default implementation of adding flags that accept multiple
        values for each Choice's flags to specify the output targets for the reporter.

        Example:
            For a Choice with flags ['--json'], this method will add an argument
            to the parser that accepts multiple target values, like so:

            --json                             # default target
            --json console filesystem callback # multiple targets
            --json filesystem                  # single target

        Subclasses can override this method if they need custom behavior such as adding
        arguments with different types or more complex logic.

        Args:
            parser (ArgumentParser): The ArgumentParser to add the flags to.
            choice (Choice): The Choice instance for which to add the flags.

        Raises:
            SimpleBenchTypeError: If the parser arg is not an ArgumentParser instance.
        """
        if not isinstance(parser, ArgumentParser):
            raise SimpleBenchTypeError(
                "parser arg must be an argparse.ArgumentParser instance",
                tag=ReporterErrorTag.ADD_FLAGS_INVALID_PARSER_ARG_TYPE)
        if not isinstance(choice, IChoice):
            raise SimpleBenchTypeError(
                "choice arg must be a Choice instance",
                tag=ReporterErrorTag.ADD_LIST_OF_TARGETS_FLAGS_INVALID_CHOICE_ARG_TYPE)
        targets = [target.value for target in choice.targets]
        for flag in choice.flags:
            parser.add_argument(flag,
                                action='append',
                                nargs='*',
                                choices=targets,
                                help=choice.description)

    def add_boolean_flags_to_argparse(self, parser: ArgumentParser, choice: Choice) -> None:
        """Adds a Choice's command-line flags to an ArgumentParser.

        This is a default implementation that adds boolean flags for each Choice's flags.
        Subclasses can override this method if they need custom behavior such as
        adding arguments with different types or more complex logic.

        Args:
            parser (ArgumentParser): The ArgumentParser to add the flags to.
            choice (Choice): The Choice instance for which to add the flags.
        """
        if not isinstance(parser, ArgumentParser):
            raise SimpleBenchTypeError(
                "parser arg must be an argparse.ArgumentParser instance",
                tag=ReporterErrorTag.ADD_FLAGS_INVALID_PARSER_ARG_TYPE)
        if not isinstance(choice, IChoice):
            raise SimpleBenchTypeError(
                "choice arg must be a Choice instance",
                tag=ReporterErrorTag.ADD_BOOLEAN_FLAGS_INVALID_CHOICE_ARG_TYPE)
        for flag in choice.flags:
            parser.add_argument(flag, action='store_true', help=choice.description)

    def get_all_stats_values(self, results: list[Results], section: Section) -> list[float]:
        """Gathers all primary statistical values for a given section across multiple results.

        It collects mean, median, minimum, maximum, 5th percentile, 95th percentile,
        and standard deviation from each Results instance for the specified section.

        This method is useful in determining appropriate scaling factors or units
        for reporting by analyzing the range of values across all results.
        """
        all_numbers = []
        for result in results:
            stats = result.results_section(section)
            all_numbers.extend([
                stats.mean, stats.median, stats.minimum, stats.maximum,
                stats.percentiles[5], stats.percentiles[95], stats.standard_deviation
            ])
        return all_numbers

    def get_prioritized_options(self, case: Case, choice: Choice) -> ReporterOptions:
        """Get the reporter-specific options from the case, choice, or default options.
        This method retrieves reporter-specific options of type `options_cls` by
        checking the `case` options first, then the `choice` options, and finally
        falling back to the reporter's default options if none are found.

        The actual type of `ReporterOptions` to retrieve is determined by the
        reporter's `options_type` property - it will always be a specific subclass
        of `ReporterOptions` defined by the reporter.

        Args:
            case (Case): The Case instance containing benchmark results.
            choice (Choice): The Choice instance specifying the report configuration.

        Returns:
            ReporterOptions: The prioritized instance of the class `ReporterOptions`.
                More specifically, it will be an instance of the reporter's specific
                `ReporterOptions` subclass as defined by the reporter's `options_type` property.

        Raises:
            SimpleBenchNotImplementedError: If no ReporterOptions instance can be found
        """
        cls = type(self)
        options_cls = self.options_type
        # case.options is a list of ReporterOptions because Case.options is used
        # for all reporters. Thus, we need to filter by the specific type here
        # to find the reporter-specific options.
        case_options = cls.find_options_by_type(options=case.options, cls=options_cls)
        # Since different reporters can have different options types,
        # we need to filter the options by the specific type here as well in case
        # a less specific type was used in the current default options.
        default_options = cls.get_default_options()
        if default_options is None:
            raise SimpleBenchNotImplementedError(
                "Reporter subclasses must set __HARDCODED_DEFAULT_OPTIONS to a"
                "a valid ReporterOptions subclass to provide default options",
                tag=ReporterErrorTag.HARDCODED_DEFAULT_OPTIONS_NOT_IMPLEMENTED)
        options = first_not_none([case_options, choice.options, default_options])
        if options is None:
            raise SimpleBenchNotImplementedError(
                "Reporter subclasses must provide ReporterOptions via Case, Choice, or default options",
                tag=ReporterErrorTag.REPORTER_OPTIONS_NOT_IMPLEMENTED)
        return options

    def get_prioritized_default_targets(self, choice: Choice) -> frozenset[Target]:
        """Get the prioritized default targets from the choice or reporter defaults.

        This method retrieves the default targets for the reporter by first checking
        the `choice` default_targets, and if none are found, falling back to the reporter's
        default targets.

        Args:
            choice (Choice): The Choice instance specifying the report configuration.
        Returns:
            frozenset[Target]: The set of default targets.
        """
        if choice.default_targets is not None:
            return choice.default_targets
        return self._default_targets

    def get_prioritized_subdir(self, choice: Choice) -> str:
        """Get the prioritized subdirectory from the choice or reporter defaults.

        This method retrieves the subdirectory for the reporter by first checking
        the `choice` subdir, and if none is found, falling back to the reporter's
        default subdir.

        Args:
            choice (Choice): The Choice instance specifying the report configuration.
        Returns:
            str: The subdirectory for saving report files.
        """
        if choice.subdir is not None:
            return choice.subdir
        return self._subdir

    def get_prioritized_file_suffix(self, choice: Choice) -> str:
        """Get the prioritized file suffix from the choice or reporter.

        This method retrieves the file suffix for the reporter by first checking
        the `choice` file_suffix, and if None is found falling back to the reporter's
        file_suffix.

        Args:
            choice (Choice): The Choice instance specifying the report configuration.
        Returns:
            str: The file suffix for report files.
        """
        if choice.file_suffix is not None:
            return choice.file_suffix
        return self._file_suffix

    def get_prioritized_file_unique(self, choice: Choice) -> bool:
        """Get the prioritized file unique flag from the choice or reporter.

        This method retrieves the file unique flag for the reporter by first checking
        the `choice` file_unique, and if None is found falling back to the reporter's
        file_unique.

        Args:
            choice (Choice): The Choice instance specifying the report configuration.
        Returns:
            bool: The file unique flag for report files.
        """
        if choice.file_unique is not None:
            return choice.file_unique
        return self._file_unique

    def get_prioritized_file_append(self, choice: Choice) -> bool:
        """Get the prioritized file append flag from the choice or reporter.

        This method retrieves the file append flag for the reporter by first checking
        the `choice` file_append, and if None is found falling back to the reporter's
        file_append.

        Args:
            choice (Choice): The Choice instance specifying the report configuration.
        Returns:
            bool: The file append flag for report files.
        """
        if choice.file_append is not None:
            return choice.file_append
        return self._file_append

    def render_by_section(self, *,
                          args: Namespace,
                          case: Case,
                          choice: Choice,
                          path: Path | None = None,
                          session: Session | None = None,
                          callback: ReporterCallback | None = None) -> None:
        """Render the report for each section individually.

        This method is called by the subclass's run_report() method to run one report per section
        that is then processed according to the specified targets.

        It calls the subclass's render() method to actually generate the report output.

        Args:
            args (Namespace): The parsed command-line arguments.
            case (Case): The Case instance representing the benchmarked code.
            choice (Choice): The Choice instance specifying the report configuration.
            path (Optional[Path]): The path to the directory where the CSV file(s) will be saved.
            session (Optional[Session]): The Session instance containing benchmark results.
            callback (Optional[ReporterCallback]):
                A callback function for additional processing of the report.
                The function should accept two arguments: the Case instance and the CSV data as a string.
                Leave as None if no callback is needed.

        Return:
            None

        Raises:
            SimpleBenchTypeError: If the provided arguments are not of the expected types or if
                required arguments are missing. Also raised if the callback is not callable when
                provided for a CALLBACK target or if the path is not a Path instance when a FILESYSTEM
                target is specified.
            SimpleBenchValueError: If an unsupported section or target is specified in the choice.
        """
        default_targets = self.get_prioritized_default_targets(choice=choice)
        subdir = self.get_prioritized_subdir(choice=choice)
        options = self.get_prioritized_options(case=case, choice=choice)

        targets: set[Target] = self.select_targets_from_args(
            args=args, choice=choice, default_targets=default_targets)
        for section in choice.sections:
            output = self.render(case=case, section=section, options=options)

            for output_target in targets:
                match output_target:
                    case Target.FILESYSTEM:
                        filename: str = sanitize_filename(section.value)
                        if self._file_suffix:
                            filename += f'.{self._file_suffix}'
                        if isinstance(output, (Text, Table)):
                            output = self.rich_text_to_plain_text(output)
                        self.target_filesystem(
                            path=path,
                            subdir=subdir,
                            filename=filename,
                            output=output,
                            unique=self._file_unique,
                            append=self._file_append)

                    case Target.CALLBACK:
                        if isinstance(output, (Text, Table)):
                            output = self.rich_text_to_plain_text(output)
                        self.target_callback(
                            callback=callback,
                            case=case,
                            section=section,
                            output_format=choice.output_format,
                            output=output)

                    case Target.CONSOLE:
                        self.target_console(session=session, output=output)

                    case _:
                        raise SimpleBenchValueError(
                            f'Unsupported target for {type(self)}: {output_target}',
                            tag=ReporterErrorTag.RENDER_BY_SECTION_UNSUPPORTED_TARGET)

    def render_by_case(self, *,
                       args: Namespace,
                       case: Case,
                       choice: Choice,
                       path: Path | None = None,
                       session: Session | None = None,
                       callback: ReporterCallback | None = None) -> None:
        """Render the report for an entire case at once across all applicable sections.

        This method is called by the subclass's run_report() method to run one report per case
        that is then processed according to the specified targets.

        It calls the subclass's render() method to actually generate the report output.

        Args:
            args (Namespace): The parsed command-line arguments.
            case (Case): The Case instance representing the benchmarked code.
            choice (Choice): The Choice instance specifying the report configuration.
            path (Optional[Path]): The path to the directory where the CSV file(s) will be saved.
            session (Optional[Session]): The Session instance containing benchmark results.
            callback (Optional[ReporterCallback]):
                A callback function for additional processing of the report.
                The function should accept two arguments: the Case instance and the CSV data as a string.
                Leave as None if no callback is needed.

        Return:
            None

        Raises:
            SimpleBenchTypeError: If the provided arguments are not of the expected types or if
                required arguments are missing. Also raised if the callback is not callable when
                provided for a CALLBACK target or if the path is not a Path instance when a FILESYSTEM
                target is specified.
            SimpleBenchValueError: If an unsupported section or target is specified in the choice.
        """
        default_targets = self.get_prioritized_default_targets(choice=choice)
        subdir = self.get_prioritized_subdir(choice=choice)
        file_suffix = self.get_prioritized_file_suffix(choice=choice)
        file_unique = self.get_prioritized_file_unique(choice=choice)
        file_append = self.get_prioritized_file_append(choice=choice)
        options = self.get_prioritized_options(case=case, choice=choice)

        targets: set[Target] = self.select_targets_from_args(
            args=args, choice=choice, default_targets=default_targets)
        output = self.render(case=case, section=Section.NULL, options=options)

        for output_target in targets:
            match output_target:
                case Target.FILESYSTEM:
                    filename: str = sanitize_filename(case.title)
                    if file_suffix:
                        filename += f'.{file_suffix}'
                    self.target_filesystem(
                        path=path,
                        subdir=subdir,
                        filename=filename,
                        output=output,
                        unique=file_unique,
                        append=file_append)

                case Target.CALLBACK:
                    self.target_callback(
                        callback=callback,
                        case=case,
                        section=Section.NULL,
                        output_format=Format.JSON,
                        output=output)

                case Target.CONSOLE:
                    self.target_console(session=session, output=output)

                case _:
                    raise SimpleBenchValueError(
                        f'Unsupported target for {type(self).__name__}: {output_target}',
                        tag=ReporterErrorTag.RENDER_BY_CASE_UNSUPPORTED_TARGET)

    @abstractmethod
    def render(self, *, case: Case, section: Section, options: ReporterOptions) -> str | bytes | Text | Table:
        """Renders the benchmark results for one section and returns the result as a str, bytes,
        rich.Text, or rich.Table.

        While required in the interface, the value of the section argument shouldbe ignored by reporters that do not
        render reports by section. It will be set to Section.NULL by the render_by_case() method.

        Args:
            case (Case): The Case instance representing the benchmarked code.
            section (Section): The Section of the report to render (ignore value if not applicable to reporter).
            options (ReporterOptions): The reporter-specific options.

        Returns:
            str | bytes | Text | Table: The rendered report data as a str, bytes, rich.Text, or rich.Table.
        """
        raise SimpleBenchNotImplementedError(
            "Reporter subclasses must implement the render method",
            tag=ReporterErrorTag.RENDER_NOT_IMPLEMENTED)

    def rich_text_to_plain_text(self, rich_text: Text | Table) -> str:
        """Convert Rich Text or Table to plain text by stripping formatting.

        Applies a virtual console width to ensure proper line wrapping. The console
        width simulates how the text would appear in a terminal of the specified width.

        As rich text is normally mainly used for console output, this method
        provides a way to convert it to plain text while preserving the intended
        layout as much as possible for non-console output targets.

        Args:
            rich_text (Text | Table): The Rich Text or Table instance to convert.
        Returns:
            str: The plain text representation of the Rich Text.
        """
        if not isinstance(rich_text, (Text, Table)):
            raise SimpleBenchTypeError(
                f'rich_text argument is of invalid type: {type(rich_text)}. '
                f'Must be rich.Text or rich.Table.',
                tag=ReporterErrorTag.RICH_TEXT_TO_PLAIN_TEXT_INVALID_RICH_TEXT_ARG_TYPE)

        output_io = StringIO()  # just a string buffer to capture console output
        console = Console(file=output_io, width=None, record=True)
        console.print(rich_text)
        text_output = console.export_text(styles=False, clear=False)
        output_io.close()

        return text_output
