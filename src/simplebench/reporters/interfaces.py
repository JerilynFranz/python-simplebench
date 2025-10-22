# -*- coding: utf-8 -*-
"""Reporters for benchmark results."""
from __future__ import annotations
from abc import ABC, abstractmethod
from argparse import ArgumentParser, Namespace
from pathlib import Path
from typing import Optional, Iterable, TYPE_CHECKING

from rich.console import Console

from ..defaults import BASE_INTERVAL_UNIT, BASE_OPS_PER_INTERVAL_UNIT, BASE_MEMORY_UNIT
from ..enums import Section, Target, Format, FlagType
from ..exceptions import ErrorTag, SimpleBenchTypeError, SimpleBenchValueError, SimpleBenchNotImplementedError
from ..metaclasses import ICase, ISession
from ..utils import collect_arg_list
from .metaclasses import IReporter, IChoices, IChoice
from .protocols import ReporterCallback

if TYPE_CHECKING:
    from ..case import Case
    from .choices import Choice, Choices
    from ..session import Session


NO_ATTRIBUTE = object()
"""Sentinel value for no attribute."""


class Reporter(ABC, IReporter):
    """Interface for Reporter classes.

    A Reporter is responsible for generating reports based on benchmark results
    from a Session and Case. Reporters can produce reports in various formats and
    output them to different targets.

    All Reporter subclasses must implement the methods defined in this interface.
    Reporters should handle their own output, whether to console, file system,
    HTTP endpoint, display device, via a callback or other output.

    Arguments:
        name (str): The unique identifying name of the reporter.
        description (str): A brief description of the reporter.
        choices (Choices): A Choices instance defining the sections, output targets,
            and formats supported by the reporter.
        session (Session): The Session instance containing benchmark results.
        callback (ReporterCallback): A callback function for additional processing of the report.

    Methods:
        The choices() method should return a Choices instance that accurately
        reflects the sections, output targets, and formats supported by the reporter.

        Targets are defined in the Choices instances returned by the choices() method.

        The Reporter interface ensures that all reporters provide a consistent
        set of functionalities, making it easier to manage and utilize different
        reporting options within the SimpleBench framework.
    """
    @abstractmethod
    def __init__(self,
                 *,
                 name: str,
                 description: str,
                 sections: set[Section],
                 targets: set[Target],
                 formats: set[Format],
                 choices: Choices) -> None:
        """
        Initialize the Reporter instance.

        Args:
            name (str): The unique identifying name of the reporter. Must be a non-empty string.
            description (str): A brief description of the reporter. Must be a non-empty string.
            sections (set[Section]): The set of Sections supported by the reporter.
            targets (set[Target]): The set of Targets supported by the reporter.
            formats (set[Format]): The set of Formats supported by the reporter.
            choices (Choices): A Choices instance defining the sections, output targets,
                and formats supported by the reporter. Must have at least one Choice.

        Raises:
            SimpleBenchNotImplementedError: If any of the required attributes
                are not provided
            SimpleBenchValueError: If any of the provided attributes have invalid values.
            SimpleBenchTypeError: If any of the provided attributes are of incorrect types.
        """
        self._validate_init_args(name=name,
                                 description=description,
                                 sections=sections,
                                 targets=targets,
                                 formats=formats,
                                 choices=choices)
        self._name: str = name
        self._description: str = description
        self._sections: set[Section] = sections
        self._targets: set[Target] = targets
        self._formats: set[Format] = formats
        self._choices: Choices = choices

    def _validate_init_args(self,
                            *,
                            name: str,
                            description: str,
                            sections: set[Section],
                            targets: set[Target],
                            formats: set[Format],
                            choices: Choices) -> None:
        """Validate the arguments provided to __init__.

        This method is called by __init__ to validate the arguments provided to the reporter.
        On validation failure, it raises an appropriate exception.

        Args:
            name (str): The unique identifying name of the reporter. Must be a non-empty string.
            description (str): A brief description of the reporter. Must be a non-empty string.
            sections (set[Section]): A set of Section enums that the reporter supports.
            targets (set[Target]): A set of Target enums that the reporter supports.
            formats (set[Format]): A set of Format enums that the reporter supports.
            choices (Choices): A Choices instance containing the available choices for the reporter.

        Raises:
            SimpleBenchNotImplementedError: If any of the required attributes are not provided
            SimpleBenchValueError: If any of the provided attributes have invalid values.
            SimpleBenchTypeError: If any of the provided attributes are of incorrect types.
        """
        if not isinstance(name, str):
            raise SimpleBenchNotImplementedError(
                "Reporter subclasses must provide a non-empty string for the name",
                tag=ErrorTag.REPORTER_NAME_NOT_IMPLEMENTED)

        if name.strip() == '':
            raise SimpleBenchValueError(
                "Reporter subclasses must provide a unique non-empty string for the name",
                tag=ErrorTag.REPORTER_NAME_INVALID_VALUE)

        if not isinstance(description, str):
            raise SimpleBenchNotImplementedError(
                "Reporter subclasses must provide a non-empty string for the description",
                tag=ErrorTag.REPORTER_DESCRIPTION_NOT_IMPLEMENTED)

        if description.strip() == '':
            raise SimpleBenchValueError(
                "Reporter subclasses must provide a non-empty string for the description",
                tag=ErrorTag.REPORTER_DESCRIPTION_INVALID_VALUE)

        if not isinstance(sections, set) or len(sections) == 0:
            raise SimpleBenchNotImplementedError(
                "Reporter subclasses must provide a non-empty set of Sections",
                tag=ErrorTag.REPORTER_SECTIONS_NOT_IMPLEMENTED)

        if not all(isinstance(section, Section) for section in sections):
            raise SimpleBenchTypeError(
                "All items in sections must be of type Section",
                tag=ErrorTag.REPORTER_INVALID_SECTIONS_ENTRY_TYPE)

        if not isinstance(targets, set) or len(targets) == 0:
            raise SimpleBenchNotImplementedError(
                "Reporter subclasses must provide a non-empty set of Targets",
                tag=ErrorTag.REPORTER_TARGETS_NOT_IMPLEMENTED)

        if not all(isinstance(target, Target) for target in targets):
            raise SimpleBenchTypeError(
                "All items in targets must be of type Target",
                tag=ErrorTag.REPORTER_INVALID_TARGETS_ENTRY_TYPE)

        if not isinstance(formats, set) or len(formats) == 0:
            raise SimpleBenchNotImplementedError(
                "Reporter subclasses must provide a non-empty set of Formats",
                tag=ErrorTag.REPORTER_FORMATS_NOT_IMPLEMENTED)

        if not all(isinstance(output_format, Format) for output_format in formats):
            raise SimpleBenchTypeError(
                "All items in formats must be of type Format",
                tag=ErrorTag.REPORTER_INVALID_FORMATS_ENTRY_TYPE)

        if choices is None:
            raise SimpleBenchNotImplementedError(
                "Reporter subclasses must provide a Choices instance with at least one Choice",
                tag=ErrorTag.REPORTER_CHOICES_NOT_IMPLEMENTED)

        if not isinstance(choices, IChoices):
            raise SimpleBenchTypeError(
                f"choices must be a Choices instance: cannot be a {type(choices)}",
                tag=ErrorTag.REPORTER_INVALID_CHOICES_ARG_TYPE)

        if len(choices) == 0:
            raise SimpleBenchNotImplementedError(
                "Reporter subclasses must initialize the Choices with at least one Choice",
                tag=ErrorTag.REPORTER_CHOICES_NOT_IMPLEMENTED)

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
                            tag=ErrorTag.UNSUPPORTED_TARGET_IN_ARGS)
                else:
                    raise SimpleBenchValueError(
                        f"Unknown output target specified for {flag}: {target}",
                        tag=ErrorTag.UNKNOWN_TARGET_IN_ARGS)

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
                tag=ErrorTag.REPORTER_REPORT_INVALID_ARGS_ARG_TYPE)
        if not isinstance(case, ICase):
            raise SimpleBenchTypeError(
                "Expected a Case instance",
                tag=ErrorTag.REPORTER_REPORT_INVALID_CASE_ARG)
        if not isinstance(choice, IChoice):
            raise SimpleBenchTypeError(
                "Expected a Choice instance",
                tag=ErrorTag.REPORTER_REPORT_INVALID_CHOICE_ARG)
        for section in choice.sections:
            if section not in self.supported_sections():
                raise SimpleBenchValueError(
                    f"Unsupported Section in Choice: {section}",
                    tag=ErrorTag.REPORTER_REPORT_UNSUPPORTED_SECTION)
        for target in choice.targets:
            if target not in self.supported_targets():
                raise SimpleBenchValueError(
                    f"Unsupported Target in Choice: {target}",
                    tag=ErrorTag.REPORTER_REPORT_UNSUPPORTED_TARGET)
        if Target.CALLBACK in choice.targets:  # pylint: disable=used-before-assignment
            if callback is not None and not callable(callback):
                raise SimpleBenchTypeError(
                    "Callback function must be callable if provided",
                    tag=ErrorTag.REPORTER_REPORT_INVALID_CALLBACK_ARG)
        if Target.FILESYSTEM in choice.targets and not isinstance(path, Path):
            raise SimpleBenchTypeError(
                "Path must be a pathlib.Path instance when using FILESYSTEM target",
                tag=ErrorTag.REPORTER_REPORT_INVALID_PATH_ARG)
        for output_format in choice.formats:
            if output_format not in self.supported_formats():
                raise SimpleBenchValueError(
                    f"Unsupported Format in Choice: {output_format}",
                    tag=ErrorTag.REPORTER_REPORT_UNSUPPORTED_FORMAT)

        if session is not None and not isinstance(session, ISession):
            raise SimpleBenchTypeError(
                "session must be a Session instance if provided",
                tag=ErrorTag.REPORTER_REPORT_INVALID_SESSION_ARG)

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
            tag=ErrorTag.REPORTER_RUN_REPORT_NOT_IMPLEMENTED)

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
                tag=ErrorTag.REPORTER_ADD_CHOICE_INVALID_ARG_TYPE)

        for section in choice.sections:
            if section not in self.supported_sections():
                raise SimpleBenchValueError(
                    f"Unsupported Section in Choice: {section}",
                    tag=ErrorTag.REPORTER_ADD_CHOICE_UNSUPPORTED_SECTION)
        for target in choice.targets:
            if target not in self.supported_targets():
                raise SimpleBenchValueError(
                    f"Unsupported Target in Choice: {target}",
                    tag=ErrorTag.REPORTER_ADD_CHOICE_UNSUPPORTED_TARGET)
        for output_format in choice.formats:
            if output_format not in self.supported_formats():
                raise SimpleBenchValueError(
                    f"Unsupported Format in Choice: {output_format}",
                    tag=ErrorTag.REPORTER_ADD_CHOICE_UNSUPPORTED_FORMAT)

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

    def supported_sections(self) -> set[Section]:
        """Return the set of supported Sections for the reporter.

        This is the set of Sections that the reporter can include in its reports.

        Defined Choices can only include Sections that are declared in this set.
        """
        return self._sections

    def supported_targets(self) -> set[Target]:
        """Return the set of supported Targets for the reporter.

        This is the set of Targets that the reporter can output to.

        Defined Choices can only include Targets that are declared in this set.
        """
        return self._targets

    def supported_formats(self) -> set[Format]:
        """Return the set of supported Formats for the reporter.

        This is the set of Formats that the reporter can output in.

        Defined Choices can only include Formats that are declared in this set.
        """
        return self._formats

    def target_filesystem(self, path: Path | None, subdir: str, filename: str, output: str | bytes) -> None:
        """Helper method to output report data to the filesystem.

        path, subdir, and filename are combined to form the full path to the output file.

        The type signature for path is Path | None because the overall report() method
        accepts path as Optional[Path] because it is not always required. However,
        this method should only be called when a valid Path is provided and will
        raise an exception if it is not a Path instance.

        Args:
            path (Path | None): The path to the directory where output should be saved.
            subdir (str): The subdirectory within the path to save the file to.
            filename (str): The filename to save the output as.
            output (str | bytes): The report data to write to the file.

        Raises:
            SimpleBenchTypeError: If path is not a Path instance,
                or if subdir or filename are not strings.
        """
        if not isinstance(path, Path):
            raise SimpleBenchTypeError(
                "path arg must be a pathlib.Path instance",
                tag=ErrorTag.REPORTER_TARGET_FILESYSTEM_INVALID_PATH_ARG_TYPE)
        if not isinstance(subdir, str):
            raise SimpleBenchTypeError(
                "subdir arg must be a string",
                tag=ErrorTag.REPORTER_TARGET_FILESYSTEM_INVALID_SUBDIR_ARG_TYPE)
        if not isinstance(filename, str):
            raise SimpleBenchTypeError(
                "filename arg must be a string",
                tag=ErrorTag.REPORTER_TARGET_FILESYSTEM_INVALID_FILENAME_ARG_TYPE)
        output_path = path / subdir / filename
        output_path.parent.mkdir(parents=True, exist_ok=True)
        mode = 'wb' if isinstance(output, bytes) else 'w'
        with output_path.open(mode) as f:
            f.write(output)

    def target_callback(self,
                        callback: ReporterCallback | None,
                        case: Case,
                        section: Section,
                        output_format: Format,
                        output: str | bytes) -> None:
        """Helper method to send report data to a callback function.

        Args:
            callback (ReporterCallback | None): The callback function to send the output to.
            case (Case): The Case instance representing the benchmarked code.
            section (Section): The Section of the report.
            output_format (Format): The Format of the report.
            output (str | bytes): The report data to send to the callback.

        Returns:
            None
        """
        if callback is not None:
            callback(case=case, section=section, output_format=output_format, output=output)

    def target_console(self, session: Session | None, output: str) -> None:
        """Helper method to output report data to the console.

        Args:
            output (str): The report data to print to the console.

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
                    tag=ErrorTag.REPORTER_RUN_REPORT_UNSUPPORTED_SECTION)

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
                tag=ErrorTag.REPORTER_ADD_FLAGS_INVALID_PARSER_ARG_TYPE)
        for choice in self.choices.values():
            match choice.flag_type:
                case FlagType.BOOLEAN:
                    self.add_boolean_flags_to_argparse(parser=parser, choice=choice)
                case FlagType.TARGET_LIST:
                    self.add_list_of_targets_flags_to_argparse(parser=parser, choice=choice)
                case _:
                    raise SimpleBenchValueError(
                        f"Unsupported flag type: {choice.flag_type}",
                        tag=ErrorTag.REPORTER_ADD_FLAGS_UNSUPPORTED_FLAG_TYPE)

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
                tag=ErrorTag.REPORTER_ADD_FLAGS_INVALID_PARSER_ARG_TYPE)
        if not isinstance(choice, IChoice):
            raise SimpleBenchTypeError(
                "choice arg must be a Choice instance",
                tag=ErrorTag.REPORTER_ADD_LIST_OF_TARGETS_FLAGS_INVALID_CHOICE_ARG_TYPE)
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
                tag=ErrorTag.REPORTER_ADD_FLAGS_INVALID_PARSER_ARG_TYPE)
        if not isinstance(choice, IChoice):
            raise SimpleBenchTypeError(
                "choice arg must be a Choice instance",
                tag=ErrorTag.REPORTER_ADD_BOOLEAN_FLAGS_INVALID_CHOICE_ARG_TYPE)
        for flag in choice.flags:
            parser.add_argument(flag, action='store_true', help=choice.description)
