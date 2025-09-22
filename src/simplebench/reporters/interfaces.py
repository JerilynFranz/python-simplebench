# -*- coding: utf-8 -*-
"""Reporters for benchmark results."""
from __future__ import annotations
from abc import ABC, abstractmethod
from argparse import ArgumentParser
from pathlib import Path
from typing import Any, Callable, Optional, TYPE_CHECKING

from .metaclasses import IReporter, IChoices
from ..enums import Section, Target, Format
from ..exceptions import ErrorTag, SimpleBenchTypeError, SimpleBenchValueError, SimpleBenchNotImplementedError
from ..metaclasses import ICase, ISession

if TYPE_CHECKING:
    from ..case import Case
    from .choices import Choice, Choices
    from ..session import Session


class Reporter(ABC, IReporter):
    """Interface for Reporter classes.

    A Reporter is responsible for generating reports based on benchmark results
    from a Session and Case. Reporters can produce reports in various formats and
    output them to different targets.

    All Reporter subclasses must implement the methods defined in this interface.
    Reporters should handle their own output, whether to console, file system,
    HTTP endpoint, or display device.

    Attributes:
        name (str): The unique identifying name of the reporter.
        description (str): A brief description of the reporter.
        choices (Choices): A Choices instance defining the sections, output targets,
            and formats supported by the reporter.
        session (Session): The Session instance containing benchmark results.
        callback (Callable[..., Any]): A callback function for additional processing of the report.

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
                 name: Optional[str] = None,
                 description: Optional[str] = None,
                 sections: Optional[set[Section]] = None,
                 targets: Optional[set[Target]] = None,
                 formats: Optional[set[Format]] = None,
                 choices: Optional[Choices] = None) -> None:
        """Initialize the Reporter instance.

        Args:
            name (Optional[str]): The unique identifying name of the reporter.
            description (Optional[str]): A brief description of the reporter.
            sections (Optional[set[Section]]): The set of Sections supported by the reporter.
            targets (Optional[set[Target]]): The set of Targets supported by the reporter.
            formats (Optional[set[Format]]): The set of Formats supported by the reporter.
            choices (Optional[Choices]): A Choices instance defining the sections,
                output targets, and formats supported by the reporter.

        The name and description must be non-empty strings provided by the subclass.

        The name, description, sections, targets, and formats must be provided by the subclass
        and cannot actually be None when calling the superclass __init__ method.

        If any of these are None, a SimpleBenchNotImplementedError will be raised.

        The Choices property is loaded by calling the _load_choices() method,
        which must be implemented by the subclass and return a valid Choices instance
        with at least one Choice defined.
        """
        if not isinstance(name, str) or name.strip() == '':
            raise SimpleBenchValueError(
                "Reporter subclasses must provide a non-empty string for the name",
                tag=ErrorTag.REPORTER_NAME_NOT_IMPLEMENTED)

        if not isinstance(description, str) or description.strip() == '':
            raise SimpleBenchValueError(
                "Reporter subclasses must provide a non-empty string for the description",
                tag=ErrorTag.REPORTER_DESCRIPTION_NOT_IMPLEMENTED)

        if not isinstance(sections, set) or len(sections) == 0:
            raise SimpleBenchValueError(
                "Reporter subclasses must provide a non-empty set of Sections",
                tag=ErrorTag.REPORTER_SUPPORTED_SECTIONS_NOT_IMPLEMENTED)

        if not isinstance(targets, set) or len(targets) == 0:
            raise SimpleBenchValueError(
                "Reporter subclasses must provide a non-empty set of Targets",
                tag=ErrorTag.REPORTER_SUPPORTED_TARGETS_NOT_IMPLEMENTED)

        if not isinstance(formats, set) or len(formats) == 0:
            raise SimpleBenchValueError(
                "Reporter subclasses must provide a non-empty set of Formats",
                tag=ErrorTag.REPORTER_SUPPORTED_FORMATS_NOT_IMPLEMENTED)

        if not isinstance(choices, IChoices):
            raise SimpleBenchTypeError(
                f"choices must be a Choices instance: cannot be a {type(choices)}",
                tag=ErrorTag.REPORTER_CHOICES_NOT_IMPLEMENTED)

        if len(choices) == 0:
            raise SimpleBenchValueError(
                "Reporter subclasses must initialize the Choices with at least one Choice",
                tag=ErrorTag.REPORTER_LOAD_CHOICES_NOT_IMPLEMENTED)

        self._name: str = name
        self._description: str = description
        self._sections: set[Section] = sections
        self._targets: set[Target] = targets
        self._formats: set[Format] = formats
        self._choices: Choices = choices

    @abstractmethod
    def _load_choices(self) -> Choices:
        """Return a Choices instance defining the reporter's choices.
        This method should be implemented by subclasses to define the specific
        choices supported by the reporter.

        Without Choices, the reporter cannot be used.

        See the `Choices` and `Choice` classes for details on defining choices.

        Raises:
            SimpleBenchNotImplementedError: If the method is not implemented in a subclass.
        """
        raise SimpleBenchNotImplementedError(
            "Reporter subclasses must implement the _init_choices method",
            tag=ErrorTag.REPORTER_LOAD_CHOICES_NOT_IMPLEMENTED)

    def add_flags_to_argparse(self, parser: ArgumentParser) -> None:
        """Add the reporter's command-line flags to an ArgumentParser.

        Args:
            parser (ArgumentParser): The ArgumentParser to add the flags to.
        """
        for choice in self.choices.values():
            for flag in choice.flags:
                parser.add_argument(flag, action='store_true', help=choice.description)

    def report(self,
               case: Case,
               choice: Choice,
               path: Optional[Path] = None,
               session: Optional[Session] = None,
               callback: Optional[Callable[[Case, Section, Format, Any], None]] = None) -> None:
        """Generate a report based on the benchmark results. This method
        performs validation and then calls the subclass's run_report method.

        Args:
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
        if not isinstance(case, ICase):
            raise SimpleBenchTypeError(
                "Expected a Case instance",
                tag=ErrorTag.REPORTER_REPORT_INVALID_CASE_ARG)
        if not isinstance(choice, Choice):
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
        results = case.results
        if not results:
            return

        # If we reach this point, all validation has passed and execution
        # will pass through to the subclass implementation
        self.run_report(case=case, choice=choice, path=path, session=session, callback=callback)

    @abstractmethod
    def run_report(self,
                   case: Case,
                   choice: Choice,
                   path: Optional[Path] = None,
                   session: Optional[Session] = None,
                   callback: Optional[Callable[[Case, Section, Format, Any], None]] = None) -> None:
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
            case (Case): The Case instance representing the benchmarked code.
            choice (Choice): The Choice instance specifying the report configuration.
            path (Optional[Path]): The path to the directory where the CSV file(s) will be saved.
            session (Optional[Session]): The Session instance containing benchmark results.
            callback (Optional[Callable[[Case, Section, Format, Any], None]]):
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
            NotImplementedError: If the method is not implemented in a subclass.
        """
        raise SimpleBenchNotImplementedError(
            "Reporter subclasses must implement the report method",
            tag=ErrorTag.REPORTER_REPORT_NOT_IMPLEMENTED)

    @property
    def choices(self) -> Choices:
        """Return the Choices instance for the reporter, including sections, output targets, and formats."""
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
        """Return the set of supported Sections for the reporter."""
        return self._sections

    def supported_targets(self) -> set[Target]:
        """Return the set of supported Targets for the reporter."""
        return self._targets

    def supported_formats(self) -> set[Format]:
        """Return the set of supported Formats for the reporter."""
        return self._formats
