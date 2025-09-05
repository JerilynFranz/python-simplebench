# -*- coding: utf-8 -*-
"""Reporters for benchmark results."""
from __future__ import annotations
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from .choices import Choices
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
        session (Session): The Session instance containing benchmark results.
        case (Case): The Case instance representing the benchmarked code.
        sections (Sequence[str]): The sections to include in the report.

    Methods:
        choices() -> Choices: Return a Choices instance for the reporter,
            including sections, output targets, and formats.
        name() -> str: Return the unique identifying name of the reporter.
        description() -> str: Return a brief description of the reporter.
        text_report() -> Optional[str]: Return a plain text (UTF-8) report
            suitable for output.
        rich_text_report() -> Optional[str]: Return a rich text report
            suitable for console output.
        run_report() -> None: Run the report and handle output internally
            to the Reporter.
        save_report(output_path: str) -> None: Save the report to the
            specified output path.

        Reporters must implement the abstract methods defined in this interface that
        are consistent with their Choices configuration.

        The choices() method should return a Choices instance that accurately
        reflects the sections, output targets, and formats supported by the reporter.

        The output methods (text_report, rich_text_report, run_report, save_report)
        should be implemented based on the reporter's capabilities and the targets
        it supports.

        Targets are defined in the Choices instances returned by the choices() method.

        * FILESYSTEM targets should be handled by the save_report method.
        * CONSOLE targets should be handled by the run_report method.
        * HTTP targets can be handled by either run_report or save_report,
          depending on the reporter's design.
        * DISPLAY targets should be handled by the display_report method.
        * CALLER targets should be handled by the appropriate output method,
        typically returning the report as a string.

        Formats and targets not supported by a specific reporter can return None
        or raise NotImplementedError as appropriate.

        The Reporter interface ensures that all reporters provide a consistent
        set of functionalities, making it easier to manage and utilize different
        reporting options within the SimpleBench framework.
    """
    @abstractmethod
    def __init__(self, session: Session, case: Case) -> None:
        """Initialize the reporter with a session, case, and sections."""
        raise NotImplementedError

    @property
    @abstractmethod
    def choices(self) -> Choices:
        """Return a Choices instance for the reporter, including sections, output targets, and formats."""
        raise NotImplementedError

    @property
    @abstractmethod
    def name(self) -> str:
        """Return the unique identifying name of the reporter."""
        raise NotImplementedError

    @property
    @abstractmethod
    def description(self) -> str:
        """Return a brief description of the reporter."""
        raise NotImplementedError
