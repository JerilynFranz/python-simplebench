# -*- coding: utf-8 -*-
"""Reporters for benchmark results."""
from __future__ import annotations
from abc import ABC, abstractmethod
from argparse import ArgumentParser
from pathlib import Path
from typing import Any, Callable, Optional, TYPE_CHECKING

from ..exceptions import ErrorTag, SimpleBenchNotImplementedError

if TYPE_CHECKING:
    from .choices import Choices, Choice, Section, Format
    from ..case import Case
    from ..session import Session


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
        """Generate a report based on the benchmark results.

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
