"""Session management for SimpleBench."""
from argparse import Namespace
from enum import Enum
from typing import Optional, Sequence

from rich.console import Console
from rich.progress import Progress

from .case import Case
from .exceptions import ErrorTag, SimpleBenchTypeError
from .tasks import RichProgressTasks


class Verbosity(str, Enum):
    """Verbosity levels for console output."""
    QUIET = 'quiet'
    """Only requested output, errors, warnings and critical messages are shown.
    Status displays are not shown during runs.

    This is incompatible with verbose output."""

    VERBOSE = 'verbose'
    """All messages are shown, including debug messages and status displays during runs.

    This is incompatible with quiet output."""

    NORMAL = 'normal'
    """Normal messages are shown, including status displays during runs.

    This is the default verbosity level."""


class Session:
    """Container for session related information while running benchmarks.

    Arguments:
        cases: (Sequence[Case]): A Sequence of benchmark cases for the session.
        verbosity: (Verbosity): The verbosity level for console output (default: Verbosity.NORMAL)

    Properties:
        args: (Namespace): The command line arguments for the session.
        cases: (Sequence[Case]): Sequence of benchmark cases for the session.
        verbosity: (Verbosity): Verbosity level for console output (default: Verbosity.NORMAL)
        progress: (Progress): Rich Progress instance for displaying progress bars. (read only)
        console: (Console): Rich Console instance for displaying output. (read only)
        tasks: (ProgressTasks): The ProgressTasks instance for managing progress tasks. (read only)
    """
    def __init__(self,
                 args: Optional[Namespace] = None,
                 cases: Optional[Sequence[Case]] = None,
                 verbosity: Verbosity = Verbosity.NORMAL) -> None:
        """Create a new Session.

        Args:
            args (Optional[Namespace]): The command line arguments for the session. (default: None)
            cases (Sequence[Case]): A Sequence of benchmark cases for the session (default: empty list).
            verbosity (Verbosity): The verbosity level for console output (default: Verbosity.NORMAL)

        Raises:
            SimpleBenchTypeError: If the arguments are of the wrong type.
        """
        # Initialize hidden attributes
        self._args: Optional[Namespace] = args
        self._cases: Sequence[Case] = []
        self._verbosity: Verbosity = Verbosity.NORMAL
        self._progress_tasks: RichProgressTasks = RichProgressTasks()
        self._progress: Progress = self._progress_tasks._progress
        self._console: Console = self._progress.console

        if not cases:
            cases = []
        if not isinstance(cases, Sequence):
            raise SimpleBenchTypeError(
                f'cases must be a Sequence of Case instances - cannot be a {type(cases)}',
                ErrorTag.SESSION_INIT_INVALID_CASES_SEQUENCE_ARG
            )
        for entry in cases:
            if not isinstance(entry, Case):
                error_text = f'case items must be Case instances - cannot be a {type(entry)}'
                raise SimpleBenchTypeError(error_text,
                                           ErrorTag.SESSION_INIT_INVALID_CASE_ARG_IN_SEQUENCE)
        self._cases = cases

        if not isinstance(verbosity, Verbosity):
            raise SimpleBenchTypeError(
                f'verbosity must be a Verbosity instance - cannot be a {type(verbosity)}',
                ErrorTag.SESSION_INIT_INVALID_VERBOSITY_ARG
            )
        self._verbosity = verbosity

    def run(self) -> None:
        """Run all benchmark cases in the session."""
        for case in self.cases:
            case.run(session=self)

    @property
    def args(self) -> Optional[Namespace]:
        """The command line arguments for the session."""
        return self._args

    @property
    def progress(self) -> Progress:
        """The Rich Progress instance for displaying progress bars."""
        return self._progress

    @property
    def console(self) -> Console:
        """The Rich Console instance for displaying output."""
        return self._console

    @property
    def tasks(self) -> RichProgressTasks:
        """The RichProgressTasks instance for managing progress tasks."""
        return self._progress_tasks

    @property
    def verbosity(self) -> Verbosity:
        """The Verbosity level for this session."""
        return self._verbosity

    @verbosity.setter
    def verbosity(self, value: Verbosity) -> None:
        """Set the Verbosity level for this session.

        Args:
            value (Verbosity): The new verbosity level for the session.

        Raises:
            SimpleBenchTypeError: If the value is not a Verbosity instance.
        """
        if not isinstance(value, Verbosity):
            raise SimpleBenchTypeError(
                f'verbosity must be a Verbosity instance - cannot be a {type(value)}',
                ErrorTag.SESSION_PROPERTY_INVALID_VERBOSITY_ARG
            )
        self._verbosity = value

    @property
    def cases(self) -> Sequence[Case]:
        """Sequence of Cases for this session."""
        return self._cases

    @cases.setter
    def cases(self, value: Sequence[Case]) -> None:
        """Set the Sequence of Cases for this session.

        Args:
            value (Sequence[Case]): Sequence of Cases for the Session

        Raises:
            SimpleBenchTypeError: If the value is not a Sequence of Cases.
        """
        if not isinstance(value, Sequence):
            raise SimpleBenchTypeError(
                f'value must be a Sequence of Case - cannot be a {type(value)}',
                ErrorTag.SESSION_PROPERTY_INVALID_CASES_ARG
            )
        for case in value:
            if not isinstance(case, Case):
                error_text = f'items in Sequence must be Case instances - cannot be a {type(case)}'
                raise SimpleBenchTypeError(
                    error_text,
                    ErrorTag.SESSION_PROPERTY_INVALID_CASE_ARG_IN_SEQUENCE
                )
        self._cases = value
