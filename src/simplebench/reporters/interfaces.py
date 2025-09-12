# -*- coding: utf-8 -*-
"""Reporters for benchmark results."""
from __future__ import annotations
from abc import ABC, abstractmethod
from argparse import ArgumentParser
from pathlib import Path
from typing import Any, Callable, Optional, TYPE_CHECKING

from ..exceptions import ErrorTag, SimpleBenchTypeError, SimpleBenchValueError, SimpleBenchNotImplementedError

if TYPE_CHECKING:
    from .choices import Choice, Choices, Target, Format, Section
    from ..case import Case
    from ..session import Session

_lazy_classes_loaded: bool = False


"""Flag to indicate if lazy classes have been loaded."""


def _lazy_load_classes() -> None:
    """Lazily load any classes or modules that cannot be loaded during initial setup.

    This is primarily to avoid circular import issues between the session, reporter and
    choices modules in the report() method of the Reporter class.
    """
    global Session  # pylint: disable=global-statement
    global Target  # pylint: disable=global-statement
    global Format  # pylint: disable=global-statement
    global Section  # pylint: disable=global-statement
    global _lazy_classes_loaded  # pylint: disable=global-statement
    if not _lazy_classes_loaded:
        from ..session import Session  # pylint: disable=import-outside-toplevel
        from .choices import Target, Format, Section  # pylint: disable=import-outside-toplevel

        _lazy_classes_loaded = True


class Reporter(ABC):
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
    def __init__(self) -> None:
        """Initialize the reporter with Sections, Targets, and Formats."""
        raise SimpleBenchNotImplementedError(
            "Reporter subclasses must implement the __init__ method",
            ErrorTag.REPORTER_INIT_NOT_IMPLEMENTED
        )

    @abstractmethod
    def supported_formats(self) -> set[Format]:
        """Return the set of supported output formats for the reporter."""
        raise SimpleBenchNotImplementedError(
            "Reporter subclasses must implement the supported_formats method",
            ErrorTag.REPORTER_SUPPORTED_FORMATS_NOT_IMPLEMENTED
        )
        # return set([Format.CSV, Format.MARKDOWN, Format.JSON, Format.RICH_TEXT, Format.GRAPH]) --- IGNORE ---

    @abstractmethod
    def supported_sections(self) -> set[Section]:
        """Return the set of supported result sections for the reporter."""
        raise SimpleBenchNotImplementedError(
            "Reporter subclasses must implement the supported_sections method",
            ErrorTag.REPORTER_SUPPORTED_SECTIONS_NOT_IMPLEMENTED
        )
        # return set([Section.OPS, Section.TIMING, Section.MEMORY]) --- IGNORE ---

    @abstractmethod
    def supported_targets(self) -> set[Target]:
        """Return the set of supported output targets for the reporter."""
        raise SimpleBenchNotImplementedError(
            "Reporter subclasses must implement the supported_targets method",
            ErrorTag.REPORTER_SUPPORTED_TARGETS_NOT_IMPLEMENTED
        )
        # return set([Target.FILESYSTEM, Target.CALLBACK, Target.CONSOLE]) --- IGNORE ---

    @abstractmethod
    def add_flags_to_argparse(self, parser: ArgumentParser) -> None:
        """Add the reporter's command-line flags to an ArgumentParser.

        Each flag defined in the reporter's Choices should be added to the parser.
        The reporter is responsible for defining how each flag is handled.

        Args:
            parser (ArgumentParser): The ArgumentParser to add the flags to.
        """
        raise SimpleBenchNotImplementedError(
            "Reporter subclasses must implement the add_flags_to_argparse method",
            ErrorTag.REPORTER_ADD_FLAGS_NOT_IMPLEMENTED
        )

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
        _lazy_load_classes()
        if not isinstance(case, Case):
            raise SimpleBenchTypeError(
                "Expected a Case instance",
                ErrorTag.REPORTER_REPORT_INVALID_CASE_ARG)
        if not isinstance(choice, Choice):
            raise SimpleBenchTypeError(
                "Expected a Choice instance",
                ErrorTag.REPORTER_REPORT_INVALID_CHOICE_ARG)
        for section in choice.sections:
            if section not in self.supported_sections():
                raise SimpleBenchValueError(
                    f"Unsupported Section in Choice: {section}",
                    ErrorTag.REPORTER_REPORT_UNSUPPORTED_SECTION)
        for target in choice.targets:
            if target not in self.supported_targets():
                raise SimpleBenchValueError(
                    f"Unsupported Target in Choice: {target}",
                    ErrorTag.REPORTER_REPORT_UNSUPPORTED_TARGET)
        if Target.CALLBACK in choice.targets:  # pylint: disable=used-before-assignment
            if callback is not None and not callable(callback):
                raise SimpleBenchTypeError(
                    "Callback function must be callable if provided",
                    ErrorTag.REPORTER_REPORT_INVALID_CALLBACK_ARG)
        if Target.FILESYSTEM in choice.targets and not isinstance(path, Path):
            raise SimpleBenchTypeError(
                "Path must be a pathlib.Path instance when using FILESYSTEM target",
                ErrorTag.REPORTER_REPORT_INVALID_PATH_ARG)
        for output_format in choice.formats:
            if output_format not in self.supported_formats():
                raise SimpleBenchValueError(
                    f"Unsupported Format in Choice: {output_format}",
                    ErrorTag.REPORTER_REPORT_UNSUPPORTED_FORMAT)

        if session is not None and not isinstance(session, Session):
            raise SimpleBenchTypeError(
                "session must be a Session instance if provided",
                ErrorTag.REPORTER_REPORT_INVALID_SESSION_ARG)

        # Only proceed if there are results to report
        results = case.results
        if not results:
            return

        # If we reach this point, all validation has passed and execution
        # will pass through to the subclass implementation
        self.run_report(case=case, choice=choice, path=path, session=session, callback=callback)

    def known_result_targets(self) -> set[str]:
        """Return the set of known result attribute targets that can be reported on.

        This includes the attributes defined in the Results class that are
        relevant for reporting.

        Currently includes:
            - ops_per_second
            - per_round_timings

        Returns:
            set[str]: A set of Result attribute names.
        """
        return set(['ops_per_second', 'per_round_timings'])

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
            ErrorTag.REPORTER_REPORT_NOT_IMPLEMENTED)

    @property
    @abstractmethod
    def choices(self) -> Choices:
        """Return a Choices instance for the reporter, including sections, output targets, and formats."""
        raise SimpleBenchNotImplementedError(
            "Reporter subclasses must implement the choices property",
            ErrorTag.REPORTER_CHOICES_NOT_IMPLEMENTED
        )

    @property
    @abstractmethod
    def name(self) -> str:
        """Return the unique identifying name of the reporter."""
        raise SimpleBenchNotImplementedError(
            "Reporter subclasses must implement the name property",
            ErrorTag.REPORTER_NAME_NOT_IMPLEMENTED
        )

    @property
    @abstractmethod
    def description(self) -> str:
        """Return a brief description of the reporter."""
        raise SimpleBenchNotImplementedError(
            "Reporter subclasses must implement the description property",
            ErrorTag.REPORTER_DESCRIPTION_NOT_IMPLEMENTED
        )
